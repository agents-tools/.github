import os
import json
from pathlib import Path
import shutil
import subprocess
import textwrap
import unittest
from unittest import mock

from test_profile import ROOT, load_script


policy = load_script('policy', 'check-policy.py')
generator = load_script('policy_generator', 'sync-policy-workflow.py')


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
        return {'pull_request': {'base': {'sha': self.base}, 'head': {'sha': head}, 'title': title}}

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
