import tempfile
import unittest
from pathlib import Path
from study_planner import add_task, complete_task, load_tasks

class StudyPlannerTests(unittest.TestCase):
    def test_add_task(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tasks.json"
            task_id = add_task(path, "Revise BFS", "AI", "2026-10-30")
            self.assertEqual(task_id, 1)
            self.assertEqual(load_tasks(path)[0]["title"], "Revise BFS")

    def test_complete_task(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tasks.json"
            add_task(path, "Revise DFS", "AI", "2026-10-30")
            complete_task(path, 1)
            self.assertTrue(load_tasks(path)[0]["done"])

    def test_invalid_date(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(ValueError):
                add_task(Path(folder) / "tasks.json", "Revise", "AI", "not-a-date")

if __name__ == "__main__":
    unittest.main()
