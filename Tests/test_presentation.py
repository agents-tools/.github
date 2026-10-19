import hashlib
import os
import re
import shlex
import shutil
import subprocess
import sys
import textwrap
import unittest

from test_profile import ROOT, checks


WORKFLOW = (ROOT / '.github/workflows/presentation.yml').read_text()
FIXTURE = ROOT / 'Tests/Fixtures/Presentation'
VENDOR = ROOT / 'Scripts/vendor'


def step(name):
    return WORKFLOW.split('      - name: ' + name + '\n', 1)[1].split('      - name:', 1)[0]


def command(name):
    return textwrap.dedent(step(name).split('        run: |\n', 1)[1])


class PresentationContractTests(unittest.TestCase):
    def test_vendor_matches_recorded_upstream_digests(self):
        rows = re.findall(r'^\| `([^`]+)` \| `([^`]+)` \| `([0-9a-f]{64})` \|$',
                          (VENDOR / 'README.md').read_text(), re.M)
        self.assertEqual({name for name, _, _ in rows},
                         {'render_terminal.py', 'presentation.py', 'LICENSE'})
        for name, _, digest in rows:
            with self.subTest(file=name):
                self.assertEqual(hashlib.sha256((VENDOR / name).read_bytes()).hexdigest(), digest)

    def test_standard_checkout_is_bound_to_executing_workflow(self):
        checkout = step('Check out pinned standard')
        self.assertIn('repository: agents-tools/.github\n', checkout)
        self.assertIn('ref: ${{ job.workflow_sha }}\n', checkout)
        self.assertIn('path: standard\n', checkout)
        self.assertIn('STANDARD_SHA: ${{ job.workflow_sha }}\n', step('Validate workflow revision'))
        self.assertIn('path: caller\n', step('Check out caller'))
        self.assertNotIn('ref:', step('Check out caller'))
        self.assertEqual(WORKFLOW.count('persist-credentials: false'), 2)
        self.assertEqual(WORKFLOW.count('permissions:\n'), 2)
        self.assertEqual(re.findall(r'^\s+contents: (\w+)$', WORKFLOW, re.M), ['read', 'read'])
        self.assertNotRegex(WORKFLOW, r': write\b')
        self.assertIn('group: shared-presentation-${{ github.workflow }}-', WORKFLOW)
        self.assertIn('  presentation:\n    name: presentation\n', WORKFLOW)
        for action in re.findall(r'^\s+uses: (\S+)', WORKFLOW, re.M):
            self.assertRegex(action, r'^actions/[\w-]+@[0-9a-f]{40}$')

    def test_missing_or_mutable_workflow_revision_fails_before_checkout(self):
        for revision, valid in [('a' * 40, True), ('', False), ('master', False),
                                ('a' * 39, False), ('a' * 40 + '\n', False)]:
            with self.subTest(revision=revision):
                result = subprocess.run(
                    ['bash', '-eo', 'pipefail', '-c', command('Validate workflow revision')],
                    env={**os.environ, 'STANDARD_SHA': revision}, capture_output=True, text=True,
                )
                self.assertEqual(result.returncode == 0, valid, result.stdout + result.stderr)

    def test_self_call_uses_fixture_and_only_cli_members_require_context(self):
        ci = (ROOT / '.github/workflows/ci.yml').read_text()
        self.assertIn('  presentation:\n    uses: ./.github/workflows/presentation.yml\n', ci)
        for key, path in [('record', 'record.json'), ('recipe', 'recipe.json'), ('output-directory', '')]:
            self.assertIn(f'      {key}: Tests/Fixtures/Presentation' + ('/' + path if path else '') + '\n', ci)
        members = checks.settings.load_declaration()['repositories']
        self.assertEqual({name for name, member in members.items()
                          if 'presentation / presentation' in member['required_checks']},
                         {'agents-tools/cli', 'skill-cli/cli'})


class PresentationRunTests(unittest.TestCase):
    def setUp(self):
        self.root = ROOT / '.build/test-presentation'
        self.root.mkdir(parents=True)
        self.addCleanup(shutil.rmtree, self.root)
        self.caller = self.root / 'caller'
        self.demo = self.caller / 'Demo with spaces'
        shutil.copytree(FIXTURE, self.demo)
        shutil.copytree(VENDOR, self.root / 'standard/Scripts/vendor')

    def run_check(self, **environment):
        shell = command('Check committed terminal SVGs')
        shell = shell.replace('python ', shlex.quote(sys.executable) + ' ', 1)
        return subprocess.run(
            ['bash', '-eo', 'pipefail', '-c', shell], cwd=self.caller,
            env={**os.environ, 'GITHUB_WORKSPACE': str(self.root),
                 'RECORD': 'Demo with spaces/record.json', 'RECIPE': 'Demo with spaces/recipe.json',
                 'OUTPUT_DIRECTORY': 'Demo with spaces', **environment},
            capture_output=True, text=True,
        )

    def snapshot(self):
        return {path.relative_to(self.root): path.read_bytes()
                for path in self.root.rglob('*') if path.is_file()}

    def test_fixture_passes_without_writes(self):
        before = self.snapshot()
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.snapshot(), before)

    def test_each_missing_or_stale_svg_fails_without_repair(self):
        for theme in ('light', 'dark'):
            path = self.demo / f'Demo-{theme}.svg'
            original = path.read_bytes()
            for missing in (False, True):
                with self.subTest(theme=theme, missing=missing):
                    if missing:
                        path.unlink()
                    else:
                        path.write_text('stale SVG\n')
                    before = self.snapshot()
                    result = self.run_check()
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(f'Demo-{theme}.svg differs', result.stderr)
                    self.assertEqual(self.snapshot(), before)
                    path.write_bytes(original)

    def test_caller_modules_cannot_bypass_drift_check(self):
        for name in ('json.py', 'presentation.py', 'sitecustomize.py'):
            (self.caller / name).write_text('raise SystemExit(0)\n')
        (self.demo / 'Demo-dark.svg').write_text('stale SVG\n')
        result = self.run_check(PYTHONPATH=str(self.caller))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Demo-dark.svg differs', result.stderr)

    def test_stale_design_binding_fails(self):
        (self.demo / 'DESIGN.md').write_text('Changed design\n')
        (self.demo / 'recipe.json').write_text(
            '{"design_source": "DESIGN.md", "design_sha256": "' + '0' * 64 + '"}\n')
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('DESIGN binding is stale', result.stderr)


if __name__ == '__main__':
    unittest.main()
