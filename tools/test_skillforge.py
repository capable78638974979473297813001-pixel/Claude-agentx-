import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT))
import skillforge as sf  # noqa: E402


class SkillforgeCliTest(unittest.TestCase):
    def test_stats_counts_verified_skills(self):
        completed = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "skillforge.py"), "stats"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        self.assertIn("verified skills   43", completed.stdout)
        self.assertIn("curated skills", completed.stdout)
        self.assertNotIn("blends", completed.stdout)

    def test_route_vat_and_abstain(self):
        vat = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "skillforge.py"), "route", "vat invoice rounding"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(vat.returncode, 0)
        self.assertIn("tax-sales-and-vat", vat.stdout)
        vague = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "skillforge.py"), "route", "help me code"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(vague.returncode, 2)
        self.assertIn("fallback: reason without a skill", vague.stdout)

    def test_removed_paths_stay_gone(self):
        self.assertFalse((ROOT / ".claude" / "agents").exists())
        self.assertFalse((ROOT / ".claude" / "skills" / "swarm").exists())
        self.assertFalse((ROOT / ".claude" / "skills" / "tax-engine-kit").exists())
        self.assertFalse((ROOT / ".claude" / "skills" / "prompt-engineering").exists())
        self.assertFalse((ROOT / "catalog" / "kits.json").exists())
        self.assertFalse(list((ROOT / "forge" / "lenses").glob("claude-*.md")))
        self.assertFalse(list((ROOT / "forge" / "lenses").glob("gpt-*.md")))
        self.assertTrue((ROOT / "forge" / "lenses" / "adversarial.md").is_file())

    def test_index_shape(self):
        code = sf.cmd_index(argparse_namespace())
        self.assertEqual(code, 0)
        payload = json.loads((ROOT / "catalog" / "index.json").read_text(encoding="utf-8"))
        self.assertEqual(payload["verified"], 43)
        self.assertNotIn("blends", payload)
        self.assertGreaterEqual(payload["curated"], 30)
        ids = {item["id"] for item in payload["skills"]}
        self.assertIn("tax-money-math", ids)
        self.assertIn("react-19-ref-as-prop", ids)
        self.assertNotIn("swarm", ids)


def argparse_namespace():
    return type("Args", (), {})()


if __name__ == "__main__":
    unittest.main()
