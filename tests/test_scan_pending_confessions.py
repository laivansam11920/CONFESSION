import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import Mock


REPO_ROOT = Path("/home/runner/work/CONFESSION/CONFESSION")
SCAN_MODULE_PATH = (
    REPO_ROOT / "app/services/moderation/scan_pending_confessions.py"
)
UPDATE_UNCERTAIN_MODULE_PATH = (
    REPO_ROOT / "app/services/update_cfs/update_uncertain.py"
)


def _load_module(module_path: Path, module_name: str, module_mocks: dict):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    original_modules = {}
    for name, value in module_mocks.items():
        original_modules[name] = sys.modules.get(name)
        sys.modules[name] = value

    try:
        spec.loader.exec_module(module)  # type: ignore[union-attr]
        return module
    finally:
        for name, original in original_modules.items():
            if original is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = original


class TestScanPendingConfessions(unittest.TestCase):
    def _load_scan_module(self, *, moderation_on=True, threshold=55, cfs_value=1):
        fake_docs = Mock()
        fake_db = types.SimpleNamespace(docs=fake_docs)
        cfs_mock = Mock(return_value=cfs_value)
        logger_module = types.ModuleType("app.utils.logger")
        logger_module.console = types.SimpleNamespace(error=Mock())

        module = _load_module(
            SCAN_MODULE_PATH,
            "scan_pending_confessions_test_module",
            {
                "app.database": types.SimpleNamespace(db=fake_db),
                "app.utils.get_cfs_count": types.SimpleNamespace(cfs_nums=cfs_mock),
                "app.utils.logger": logger_module,
                "configs": types.SimpleNamespace(
                    Config=types.SimpleNamespace(
                        MODERATION_CONFESSION=moderation_on,
                        MAX_MODERATION_SCORE=threshold,
                    )
                ),
            },
        )

        return module, fake_docs, cfs_mock

    def test_auto_approved_confession_gets_tag_number(self):
        module, fake_docs, cfs_mock = self._load_scan_module(cfs_value=97)
        fake_docs.find.return_value = [
            {
                "confession_id": "cfs-1",
                "ai_data": {"score": 88, "uncertain": False},
                "humans_check_safe": False,
            }
        ]
        fake_docs.find_one.return_value = {"cfs": 0, "safe_to_post": False}

        stats = module.ModerationQueueScanner.scan()

        self.assertEqual(stats["approved"], 1)
        self.assertEqual(stats["errors"], 0)
        cfs_mock.assert_called_once()
        fake_docs.update_one.assert_called_with(
            {"confession_id": "cfs-1", "send": False},
            {"$set": {"safe_to_post": True, "status": "approved_by_auto_scan", "cfs": 97}},
        )

    def test_flagged_confession_goes_to_manual_review(self):
        module, fake_docs, cfs_mock = self._load_scan_module()
        fake_docs.find.return_value = [
            {
                "confession_id": "cfs-2",
                "ai_data": {"score": 40, "uncertain": True},
            }
        ]

        stats = module.ModerationQueueScanner.scan()

        self.assertEqual(stats["need_human_review"], 1)
        cfs_mock.assert_not_called()
        fake_docs.update_one.assert_called_with(
            {"confession_id": "cfs-2", "send": False, "safe_to_post": False},
            {"$set": {"status": "need_human_review"}},
        )

    def test_human_checked_confession_keeps_existing_tag_when_rescanned(self):
        module, fake_docs, cfs_mock = self._load_scan_module()
        fake_docs.find.return_value = [
            {
                "confession_id": "cfs-3",
                "humans_check_safe": True,
                "ai_data": {},
            }
        ]
        fake_docs.find_one.return_value = {"cfs": 12, "safe_to_post": False}

        stats = module.ModerationQueueScanner.scan()

        self.assertEqual(stats["approved"], 1)
        cfs_mock.assert_not_called()
        fake_docs.update_one.assert_called_with(
            {"confession_id": "cfs-3", "send": False},
            {"$set": {"safe_to_post": True, "status": "approved_by_human"}},
        )

    def test_scan_handles_unexpected_error(self):
        module, fake_docs, _ = self._load_scan_module()
        fake_docs.find.return_value = [
            {
                "confession_id": "cfs-4",
                "ai_data": {"score": 88, "uncertain": False},
            }
        ]
        fake_docs.find_one.return_value = {"cfs": 0, "safe_to_post": False}
        fake_docs.update_one.side_effect = RuntimeError("db failed")

        stats = module.ModerationQueueScanner.scan()

        self.assertEqual(stats["errors"], 1)


class TestUpdateUncertain(unittest.TestCase):
    def test_manual_accept_and_reject_use_queue_scanner(self):
        scanner_module = types.ModuleType("app.services.moderation.scan_pending_confessions")
        scanner_module.ModerationQueueScanner = types.SimpleNamespace(
            approve_by_human=Mock(return_value=True),
            reject_by_human=Mock(return_value=True),
        )
        logger_module = types.ModuleType("app.utils.logger")
        logger_module.console = types.SimpleNamespace(error=Mock())

        module = _load_module(
            UPDATE_UNCERTAIN_MODULE_PATH,
            "update_uncertain_test_module",
            {
                "app.services.moderation.scan_pending_confessions": scanner_module,
                "app.utils.logger": logger_module,
            },
        )

        self.assertTrue(module.UpdateUncertain.update_uncertain("cfs-5", True))
        self.assertTrue(module.UpdateUncertain.update_uncertain("cfs-5", False))

        scanner_module.ModerationQueueScanner.approve_by_human.assert_called_once_with(
            "cfs-5"
        )
        scanner_module.ModerationQueueScanner.reject_by_human.assert_called_once_with(
            "cfs-5"
        )


if __name__ == "__main__":
    unittest.main()
