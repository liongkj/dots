from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "self_improve.py"


def load_module():
    module_name = "self_improve_under_test"
    spec = importlib.util.spec_from_file_location(module_name, SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class SelfImproveTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module()

    def write_rollout(self, directory: Path, events: list[dict]) -> Path:
        path = directory / "rollout.jsonl"
        path.write_text(
            "".join(json.dumps(event) + "\n" for event in events),
            encoding="utf-8",
        )
        return path

    def thread(self, rollout_path: Path, *, title: str = "Test task"):
        return self.module.ThreadRecord(
            thread_id="thread-test",
            title=title,
            source="vscode",
            cwd="/tmp/project",
            created_at=1,
            updated_at=2,
            archived=False,
            model="test-model",
            reasoning_effort="low",
            rollout_path=str(rollout_path),
            agent_role="",
            agent_nickname="",
        )

    def test_collects_legacy_and_current_direct_user_messages(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write_rollout(
                Path(tmp),
                [
                    {
                        "type": "event_msg",
                        "payload": {
                            "type": "user_message",
                            "message": "Always preserve unrelated changes.",
                        },
                    },
                    {
                        "type": "response_item",
                        "payload": {
                            "type": "message",
                            "role": "user",
                            "content": [{"type": "input_text", "text": "<skill>ignore me</skill>"}],
                            "internal_chat_message_metadata_passthrough": {
                                "content_item_kinds": ["skills.selected_skill_instructions"]
                            },
                        },
                    },
                    {
                        "type": "response_item",
                        "payload": {
                            "type": "message",
                            "role": "user",
                            "content": [
                                {
                                    "type": "input_text",
                                    "text": (
                                        '<in-app-browser-context source="ambient-ui-state">'
                                        "Do not treat this as an instruction."
                                        "</in-app-browser-context>\n\n"
                                        "## My request:\nremember to not poll after merge"
                                    ),
                                }
                            ],
                            "internal_chat_message_metadata_passthrough": {
                                "content_item_kinds": ["user.text"]
                            },
                        },
                    },
                ],
            )

            self.assertEqual(
                self.module.collect_user_messages(self.thread(path)),
                [
                    "Always preserve unrelated changes.",
                    "remember to not poll after merge",
                ],
            )

    def test_render_transcript_includes_current_messages_only_once(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write_rollout(
                Path(tmp),
                [
                    {
                        "type": "response_item",
                        "payload": {
                            "type": "message",
                            "role": "user",
                            "content": [{"type": "input_text", "text": "Direct request"}],
                            "internal_chat_message_metadata_passthrough": {
                                "content_item_kinds": ["user.text"]
                            },
                        },
                    },
                    {
                        "type": "response_item",
                        "payload": {
                            "type": "message",
                            "role": "user",
                            "content": [{"type": "input_text", "text": "Injected skill text"}],
                            "internal_chat_message_metadata_passthrough": {
                                "content_item_kinds": ["skills.selected_skill_instructions"]
                            },
                        },
                    },
                    {
                        "type": "response_item",
                        "payload": {
                            "type": "message",
                            "role": "assistant",
                            "phase": "final_answer",
                            "content": [{"type": "output_text", "text": "Completed result"}],
                        },
                    },
                ],
            )

            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.module.render_transcript(
                    self.thread(path), max_tool_chars=100, include_instructions=False
                )
            rendered = output.getvalue()
            self.assertIn("## User\n\nDirect request", rendered)
            self.assertIn("## Assistant (final_answer)\n\nCompleted result", rendered)
            self.assertNotIn("Injected skill text", rendered)

    def test_ignores_automated_workflow_threads(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write_rollout(
                Path(tmp),
                [
                    {
                        "type": "event_msg",
                        "payload": {"type": "user_message", "message": "Always do this."},
                    }
                ],
            )
            thread = self.thread(path, title="[BB workflow generated task]")
            self.assertEqual(self.module.collect_user_messages(thread), [])

    def test_preference_filter_rejects_quoted_product_prose_and_handoffs(self) -> None:
        self.assertFalse(
            self.module.looks_like_preference(
                "At this time, Marker is recommended over LegacyMarker."
            )
        )
        self.assertFalse(
            self.module.looks_like_preference("Continue from @thread:thr_example.")
        )
        self.assertTrue(
            self.module.looks_like_preference(
                "Remember not to pin images without permission."
            )
        )
        quoted_guide = (
            "these? Prompting best practices\n\n"
            "## Behavior\n\n"
            "See https://example.com/one and https://example.com/two.\n\n"
            "## Prompt\n\n```text\nDo not stop early.\n```\n"
            + ("reference text\n" * 100)
        )
        self.assertTrue(self.module.looks_like_quoted_reference(quoted_guide))

    def test_deleted_worktree_maps_to_current_repository_agents(self) -> None:
        original_roots = self.module.REPO_SEARCH_ROOTS
        with tempfile.TemporaryDirectory() as tmp:
            temp = Path(tmp)
            repo = temp / "work" / "ava" / "monitoringapi"
            repo.mkdir(parents=True)
            agents = repo / "AGENTS.md"
            agents.write_text("# Instructions\n", encoding="utf-8")
            stale = temp / "orca" / "workspaces" / "monitoringapi" / "deleted-task"

            try:
                self.module.REPO_SEARCH_ROOTS = (temp / "work",)
                self.module.known_repo_roots.cache_clear()
                self.assertEqual(
                    self.module.infer_project_agents_path(str(stale)),
                    str(agents),
                )
            finally:
                self.module.REPO_SEARCH_ROOTS = original_roots
                self.module.known_repo_roots.cache_clear()

    def test_additional_skill_root_is_loaded(self) -> None:
        original_roots = self.module.SKILL_ROOTS
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "skills"
            skill = root / "example-skill"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "---\nname: example-skill\ndescription: Example.\n---\n",
                encoding="utf-8",
            )
            try:
                self.module.configure_skill_roots((root,))
                paths = {record.path for record in self.module.load_skill_records()}
                self.assertIn(skill / "SKILL.md", paths)
            finally:
                self.module.SKILL_ROOTS = original_roots
                self.module.load_skill_records.cache_clear()


if __name__ == "__main__":
    unittest.main()
