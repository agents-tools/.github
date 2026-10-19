import os
import json
from io import BytesIO
from pathlib import Path
import shutil
import subprocess
import sys
import textwrap
import unittest
from unittest import mock
from urllib.error import URLError

from test_profile import ROOT, load_script


policy = load_script('policy', 'check-policy.py')
generator = load_script('policy_generator', 'sync-policy-workflow.py')


def dependabot_metadata(sha):
    return {'sha': sha, 'author': {'login': 'dependabot[bot]', 'type': 'Bot'},
            'committer': {'login': 'web-flow', 'type': 'User'},
            'commit': {'verification': {'verified': True, 'reason': 'valid'}}}


def github_response(metadata):
    return BytesIO(json.dumps(metadata).encode())


class PolicyTests(unittest.TestCase):
    def test_subject_syntax_and_allowed_types(self):
        for kind in policy.TYPES.split('|'):
            self.assertEqual(policy.message_findings('commit', kind + '(cli)!: improve behavior'), [])
        for subject in ('Initial commit', 'feat:no space', 'feature: text', 'fix: ', 'fix(): text', 'fix: text '):
            self.assertTrue(policy.message_findings('commit', subject), subject)

    def test_attribution_in_body_and_legitimate_product_names(self):
        self.assertEqual(policy.message_findings('commit', 'feat: support Codex and Claude\n\nKeep notices.'), [])
        for trailer in ('Co-authored-by', 'Generated-by', 'Signed-off-by', 'Assisted-by'):
            self.assertTrue(policy.message_findings('commit', 'fix: change\n\n' + trailer + ': someone'))

    def test_dependabot_exception_is_exact_and_preserves_other_trailer_bans(self):
        signoff = policy.DEPENDABOT_SIGNOFF
        for trailer in (signoff.lower(), ' ' + signoff, signoff + ' ', signoff + '\r',
                        signoff.replace('support@github.com', 'someone@example.com'),
                        'Co-authored-by: someone', 'Generated-by: tool', 'Generated-with: tool',
                        'Made-with: tool', 'Assisted-by: tool', 'Powered-by: tool'):
            with self.subTest(trailer=trailer):
                self.assertTrue(policy.message_findings(
                    'commit', 'chore(deps): update\n\n' + signoff + '\n' + trailer, dependabot=True))
        self.assertTrue(policy.message_findings('PR title', 'chore: update\n' + signoff))
        self.assertTrue(policy.added_findings('@@ -0,0 +1 @@\n+' + signoff + '\n'))

    def test_only_added_lines_are_scanned(self):
        patch = 'diff --git a/file b/file\n--- a/file\n+++ b/file\n@@ -1,2 +1 @@\n-<<<<<<< old\n-Generated-by: old\n+Useful documentation about Codex\n'
        self.assertEqual(policy.added_findings(patch), [])
        patch += '@@ -10 +10,3 @@\n+<<<<<<< bad\n+=======\n+Generated-by: tool\n'
        findings = policy.added_findings(patch)
        self.assertEqual(len(findings), 3)
        self.assertTrue(any('b/file:12' in line for line in findings))

    def test_generated_workflow_is_current(self):
        self.assertEqual(generator.render(), (ROOT / '.github/workflows/policy.yml').read_text())

    def test_event_ranges_reject_bad_or_unsupported_inputs(self):
        for event, name in (({}, 'workflow_dispatch'), ({'deleted': True}, 'push'),
                            ({'before': 'not-a-sha', 'after': 'a' * 40}, 'push')):
            with self.assertRaises((ValueError, KeyError)):
                policy.source_range(event, name)


class GeneratedWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.root = ROOT / '.build/test-policy-workflow'
        self.root.mkdir(parents=True)
        self.addCleanup(shutil.rmtree, self.root)
        for relative in ('Scripts/check-policy.py', 'Scripts/sync-policy-workflow.py',
                         '.github/workflows/policy.yml'):
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, destination)
        self.workflow = self.root / '.github/workflows/policy.yml'
        self.original = self.workflow.read_text(encoding='utf-8')
        self.uses = next(line for line in self.original.splitlines()
                         if line.startswith('      - uses: actions/checkout@'))

    def run_generator(self, *arguments):
        return subprocess.run(
            [sys.executable, str(self.root / 'Scripts/sync-policy-workflow.py'), *arguments],
            cwd=self.root, capture_output=True, text=True,
        )

    def test_dependabot_pin_only_update_passes_and_survives_regeneration(self):
        bumped = self.original.replace(self.uses, '      - uses: actions/checkout@' + 'f' * 40 + ' # v99.0.0')
        self.assertNotEqual(bumped, self.original)
        self.workflow.write_text(bumped, encoding='utf-8')
        for arguments in (('--check',), ()):
            with self.subTest(arguments=arguments):
                result = self.run_generator(*arguments)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(self.workflow.read_text(encoding='utf-8'), bumped)
        self.assertEqual(generator.render(self.root), bumped)

    def test_hand_edit_of_embedded_policy_fails_and_regeneration_restores_source(self):
        edited = self.original.replace('sys.exit(main())', 'sys.exit(0)')
        self.assertNotEqual(edited, self.original)
        self.workflow.write_text(edited, encoding='utf-8')
        result = self.run_generator('--check')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Regenerate policy.yml', result.stderr)
        self.assertEqual(self.workflow.read_text(encoding='utf-8'), edited)
        result = self.run_generator()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.workflow.read_text(encoding='utf-8'), self.original)

    def test_hand_edit_of_workflow_structure_fails(self):
        for before, after in (('persist-credentials: false', 'persist-credentials: true'),
                              ('python3 -I -', 'python3 -')):
            with self.subTest(before=before):
                edited = self.original.replace(before, after)
                self.assertNotEqual(edited, self.original)
                self.workflow.write_text(edited, encoding='utf-8')
                self.assertNotEqual(self.run_generator('--check').returncode, 0)

    def test_checkout_requires_one_full_sha_pin_and_version_comment(self):
        for uses in ('', self.uses + '\n' + self.uses,
                     '      - uses: actions/checkout@v99',
                     '      - uses: actions/checkout@' + 'f' * 40,
                     self.uses.replace('actions/checkout@', 'other/checkout@')):
            with self.subTest(uses=uses):
                edited = self.original.replace(self.uses, uses)
                self.workflow.write_text(edited, encoding='utf-8')
                for arguments in (('--check',), ()):
                    result = self.run_generator(*arguments)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(self.workflow.read_text(encoding='utf-8'), edited)


class GitRangeTests(unittest.TestCase):
    def setUp(self):
        self.root = ROOT / '.build/test-policy'
        self.root.mkdir(parents=True)
        self.addCleanup(shutil.rmtree, self.root)
        self.git('init', '-q', '--initial-branch=main')
        self.git('config', 'user.name', 'Policy fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.git('config', 'commit.gpgsign', 'false')
        (self.root / 'file').write_text('old content\n')
        self.base = self.commit('Initial legacy commit')
        self.git('update-ref', 'refs/remotes/origin/main', self.base)
        original = policy.git
        def git(*arguments):
            return original('-C', str(self.root), *arguments)
        self.patch = mock.patch.object(policy, 'git', side_effect=git)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.cwd = Path.cwd()
        os.chdir(self.root)
        self.addCleanup(os.chdir, self.cwd)

    def git(self, *arguments):
        return subprocess.check_output(['git', '-C', str(self.root), *arguments], text=True).strip()

    def commit(self, message):
        self.git('add', '.')
        self.git('commit', '-q', '-m', message)
        return self.git('rev-parse', 'HEAD')

    def event(self, head, title='fix: update content'):
        return {'repository': {'full_name': 'owner/member'},
                'pull_request': {'base': {'sha': self.base}, 'head': {'sha': head}, 'title': title}}

    def dependency_update(self):
        (self.root / 'file').write_text('updated dependency\n')
        self.git('config', 'user.name', 'dependabot[bot]')
        self.git('config', 'user.email', '49699333+dependabot[bot]@users.noreply.github.com')
        return self.commit('chore(deps): bump dependency from 1.0 to 1.1\n\n' + policy.DEPENDABOT_SIGNOFF)

    @mock.patch.dict(os.environ, {'GH_TOKEN': 'test-token'})
    def test_authenticated_dependabot_update_passes_on_pr_and_push(self):
        head = self.dependency_update()
        events = ((self.event(head), 'pull_request'),
                  ({'repository': {'full_name': 'owner/member'}, 'before': self.base, 'after': head}, 'push'))
        for event, name in events:
            with self.subTest(event=name), mock.patch.object(
                policy, 'urlopen', return_value=github_response(dependabot_metadata(head))
            ) as get:
                self.assertEqual(policy.check(event, name), [])
                request = get.call_args.args[0]
                self.assertEqual(request.full_url, 'https://api.github.com/repos/owner/member/commits/' + head)
                self.assertEqual(request.get_method(), 'GET')
                self.assertEqual(request.get_header('Authorization'), 'Bearer test-token')

    @mock.patch.dict(os.environ, {'GH_TOKEN': 'test-token'})
    def test_same_signoff_fails_without_authenticated_dependabot_authorship(self):
        head = self.dependency_update()
        variants = [
            {'author': {'login': 'contributor', 'type': 'User'}},
            {'author': {'login': 'dependabot[bot]', 'type': 'User'}},
            {'author': None}, {'author': 'dependabot[bot]'},
            {'committer': {'login': 'contributor', 'type': 'User'}},
            {'commit': {'verification': {'verified': False, 'reason': 'unsigned'}}},
            {'commit': {'verification': {'verified': True, 'reason': 'invalid'}}},
            {'commit': {'verification': None}}, {'commit': None},
            {'sha': 'a' * 40},
        ]
        for changed in variants:
            with self.subTest(metadata=changed), mock.patch.object(
                policy, 'urlopen', return_value=github_response({**dependabot_metadata(head), **changed})
            ):
                self.assertEqual(policy.check(self.event(head), 'pull_request'),
                                 [head + ': forbidden attribution trailer'])

    def test_commit_message_carriage_return_does_not_match_exact_signoff(self):
        (self.root / 'file').write_text('updated dependency\n')
        self.git('add', '.')
        self.git('commit', '-q', '--cleanup=verbatim', '-m',
                 'chore(deps): update dependency\n\n' + policy.DEPENDABOT_SIGNOFF + '\r\n')
        head = self.git('rev-parse', 'HEAD')
        with mock.patch.object(policy, 'authenticated_dependabot_commit') as authenticate:
            self.assertEqual(policy.check(self.event(head), 'pull_request'),
                             [head + ': forbidden attribution trailer'])
            authenticate.assert_not_called()

    @mock.patch.dict(os.environ, {'GH_TOKEN': 'test-token'})
    def test_dependabot_pr_does_not_exempt_another_authors_commit(self):
        first = self.dependency_update()
        self.git('config', 'user.name', 'Contributor')
        self.git('config', 'user.email', 'contributor@example.invalid')
        (self.root / 'file').write_text('another dependency update\n')
        second = self.commit('chore(deps): update another dependency\n\n' + policy.DEPENDABOT_SIGNOFF)
        other = {**dependabot_metadata(second), 'author': {'login': 'contributor', 'type': 'User'}}
        event = self.event(second)
        event['pull_request']['user'] = {'login': 'dependabot[bot]', 'type': 'Bot'}
        with mock.patch.object(policy, 'urlopen', side_effect=[
            github_response(dependabot_metadata(first)), github_response(other)
        ]) as get:
            self.assertEqual(policy.check(event, 'pull_request'), [second + ': forbidden attribution trailer'])
            self.assertEqual(get.call_count, 2)

    @mock.patch.dict(os.environ, {'GH_TOKEN': 'test-token'})
    def test_dependabot_authentication_fails_closed_when_unavailable_or_malformed(self):
        head = self.dependency_update()
        with mock.patch.object(policy, 'urlopen', side_effect=URLError('unavailable')):
            with self.assertRaises(URLError):
                policy.check(self.event(head), 'pull_request')
        with mock.patch.object(policy, 'urlopen', return_value=github_response([])):
            self.assertTrue(policy.check(self.event(head), 'pull_request'))
        with mock.patch.object(policy, 'urlopen', return_value=BytesIO(b'not JSON')):
            with self.assertRaises(ValueError):
                policy.check(self.event(head), 'pull_request')
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(KeyError):
                policy.check(self.event(head), 'pull_request')

    def test_new_branch_does_not_rescan_legacy_ancestors(self):
        (self.root / 'file').write_text('new content\n')
        head = self.commit('fix: update content')
        event = {'before': policy.ZERO, 'after': head, 'repository': {'default_branch': 'main'}}
        self.assertEqual(policy.check(event, 'push'), [])

    def test_title_commit_whitespace_and_conflict_failures(self):
        (self.root / 'file').write_text('bad whitespace  \n<<<<<<< branch\n')
        head = self.commit('Invalid subject\n\nGenerated-by: tool')
        findings = policy.check(self.event(head, 'Bad title'), 'pull_request')
        for reason in ('PR title', 'Conventional Commit', 'attribution', 'whitespace', 'conflict marker'):
            self.assertTrue(any(reason in line for line in findings), reason)

    def test_pr_merge_base_ignores_independent_base_branch_additions(self):
        self.git('checkout', '-q', '-b', 'topic')
        (self.root / 'topic').write_text('safe content\n')
        head = self.commit('feat: add content')
        self.git('checkout', '-q', 'main')
        (self.root / 'base-only').write_text('not part of PR  \n')
        self.base = self.commit('chore: update base')
        self.assertEqual(policy.check(self.event(head), 'pull_request'), [])

    def test_new_branch_uses_merge_base_when_default_has_advanced(self):
        self.git('checkout', '-q', '-b', 'topic')
        (self.root / 'topic').write_text('safe content\n')
        head = self.commit('feat: add content')
        self.git('checkout', '-q', 'main')
        (self.root / 'base-only').write_text('independent change\n')
        self.commit('chore: update base')
        self.git('update-ref', 'refs/remotes/origin/main', 'HEAD')
        event = {'before': policy.ZERO, 'after': head, 'repository': {'default_branch': 'main'}}
        base, _ = policy.source_range(event, 'push')
        self.assertEqual(base, self.base)
        self.assertEqual(policy.check(event, 'push'), [])

    def test_consumer_python_modules_cannot_replace_embedded_policy_imports(self):
        (self.root / 'json.py').write_text('raise SystemExit(0)\n')
        head = self.commit('test: add import shadow fixture')
        event_file = self.root / 'event.json'
        event_file.write_text(json.dumps(self.event(head, 'Invalid title')))
        workflow = generator.render()
        command = textwrap.dedent(workflow.split('        run: |\n', 1)[1])
        result = subprocess.run(
            ['bash', '-eo', 'pipefail', '-c', command], cwd=self.root,
            env={**os.environ, 'GITHUB_EVENT_PATH': str(event_file), 'GITHUB_EVENT_NAME': 'pull_request'},
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('PR title', result.stdout)

    def test_attributes_cannot_hide_text_or_disable_whitespace_policy(self):
        (self.root / '.gitattributes').write_text('* -diff -whitespace\n')
        (self.root / 'file').write_text('trailing spaces  \n<<<<<<< branch\nGenerated-by: tool\n\n')
        head = self.commit('test: add attribute fixture')
        findings = policy.check(self.event(head), 'pull_request')
        for reason in ('whitespace', 'conflict marker', 'attribution', 'blank line at end'):
            self.assertTrue(any(reason in finding for finding in findings), reason)

    def test_binary_content_is_not_interpreted_as_text(self):
        (self.root / 'image').write_bytes(b'\x00\n<<<<<<< bytes\nGenerated-by: bytes  \n')
        head = self.commit('test: add binary fixture')
        self.assertEqual(policy.check(self.event(head), 'pull_request'), [])

    def test_filename_pathspec_characters_cannot_hide_added_lines(self):
        (self.root / '[a]').write_text('trailing whitespace  \n')
        (self.root / 'a').write_text('safe content\n')
        head = self.commit('test: add wildcard filename fixture')
        self.assertTrue(any('whitespace' in finding for finding in policy.check(self.event(head), 'pull_request')))

    def test_gitlinks_are_not_treated_as_text_blobs(self):
        self.git('update-index', '--add', '--cacheinfo', '160000,' + self.base + ',dependency')
        self.git('commit', '-q', '-m', 'test: add gitlink fixture')
        head = self.git('rev-parse', 'HEAD')
        self.assertEqual(policy.check(self.event(head), 'pull_request'), [])
