import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import skillforge as sf  # noqa: E402


class LibraryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = sf.load_all()

    def test_library_validates(self):
        self.assertEqual(sf.validate(self.lib), [])

    def test_tax_pack_present(self):
        names = {e.name for e in self.lib["atom"]}
        for required in ("swarm", "tax-engine-kit", "tax-money-math", "tax-progressive-brackets",
                         "tax-rules-as-data", "tax-golden-test-vectors"):
            self.assertIn(required, names)

    def test_blend_count_formula(self):
        self.assertEqual(sf.blend_count(3, 0, 0), 7)       # 3 + 3 + 1 atom sets
        self.assertEqual(sf.blend_count(4, 1, 2), (4 + 6 + 4) * 2 * 3)
        a, l, d = (len(self.lib[k]) for k in ("atom", "lens", "domain"))
        expected = sum(math.comb(a, k) for k in (1, 2, 3)) * (l + 1) * (d + 1)
        self.assertEqual(sf.build_index(self.lib)["counts"]["blends"], expected)

    def test_compose_structure(self):
        text = sf.compose(self.lib, ["tax-money-math", "tax-progressive-brackets"],
                          "adversarial", "us-federal-income-tax")
        meta, body = sf.parse_frontmatter(text)
        self.assertTrue(meta["name"].startswith("blend-tax-money-math"))
        for part in ("## Lens: adversarial", "## Domain: us-federal-income-tax",
                     "## Atom 1: tax-money-math", "## Atom 2: tax-progressive-brackets"):
            self.assertIn(part, body)

    def test_compose_keeps_code_comments(self):
        # A comment line inside a fenced block must not be demoted to a heading.
        text = sf.compose(self.lib, ["tax-golden-test-vectors"], None, None)
        self.assertIn("\n# tests/golden/", text)
        self.assertNotIn("## tests/golden/", text)

    def test_compose_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            sf.compose(self.lib, ["nope"], None, None)
        with self.assertRaises(ValueError):
            sf.compose(self.lib, ["tax-money-math"] * 2, None, None)
        with self.assertRaises(ValueError):
            sf.compose(self.lib, ["swarm", "tax-money-math", "api-design", "spec-writing"], None, None)
        with self.assertRaises(ValueError):
            sf.compose(self.lib, ["swarm"], "no-such-lens", None)

    def test_search_finds_vat(self):
        hits = sf.search(self.lib, "vat invoice rounding")
        self.assertEqual(hits[0][1].name, "tax-sales-and-vat")

    def test_demote_headings_skips_fences(self):
        src = "# Title\n```\n# comment\n```\n## Sub"
        self.assertEqual(sf.demote_headings(src), "## Title\n```\n# comment\n```\n### Sub")


if __name__ == "__main__":
    unittest.main()
