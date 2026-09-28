import tempfile
import unittest
from pathlib import Path
from daymark.store import TaskStore


class LiteralSearchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = TaskStore(Path(self.temp.name) / "tasks.db")
        self.store.initialize()

    def test_search_treats_wildcards_and_escape_character_as_text(self):
        titles = ["Reach 100%", "Reach 1000", "Rename file_name", "Rename fileXname",
                  "Remember !", "Remember !!", "Check !%_"]
        for title in titles:
            self.store.add(title, "medium")
        for search, expected in [
            ("100%", {"Reach 100%"}),
            ("file_name", {"Rename file_name"}),
            ("!!", {"Remember !!"}),
            ("!%_", {"Check !%_"})]:
            with self.subTest(search=search):
                self.assertEqual({task.title for task in self.store.list(search)}, expected)

    def test_literal_search_respects_completion_filter(self):
        done = self.store.add("Done 50%", "high")
        self.store.add("Open 50%", "low")
        self.store.add("Open 500", "medium")
        self.store.set_done(done, True)
        self.assertEqual([task.title for task in self.store.list(" 50% ", False)], ["Open 50%"])
