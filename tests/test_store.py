import tempfile, unittest
from pathlib import Path
from daymark.store import TaskStore

class StoreTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.store=TaskStore(Path(self.temp.name)/"tasks.db"); self.store.initialize()
    def tearDown(self): self.temp.cleanup()
    def test_add_filter_and_complete(self):
        first=self.store.add("Write tests","high"); self.store.add("Read docs","low")
        self.store.set_done(first, True)
        self.assertEqual([t.title for t in self.store.list("Read")],["Read docs"])
        self.assertEqual([t.title for t in self.store.list(show_done=False)],["Read docs"])
    def test_rejects_blank_title(self):
        with self.assertRaisesRegex(ValueError,"title is required"): self.store.add(" ","low")
    def test_delete(self):
        task=self.store.add("Temporary","medium"); self.store.delete(task); self.assertEqual(self.store.list(),[])

if __name__ == "__main__": unittest.main()

