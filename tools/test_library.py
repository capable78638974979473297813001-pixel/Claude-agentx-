import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from library.load import load_library, load_verified  # noqa: E402
from library.model import Skill  # noqa: E402
from library.router import Router  # noqa: E402
from library.textutil import jaccard, shingles  # noqa: E402
from library.validate import (  # noqa: E402
    PROSE_JACCARD_LIMIT,
    validate_graph,
    validate_skill_shape,
    validate_verified,
)


def _skill(body: str, skill_id: str = "sample-skill") -> Skill:
    return Skill(
        id=skill_id,
        name=skill_id,
        area="languages",
        topic="python",
        task="sample",
        title="Sample",
        description="A long enough description for the shape checker to accept this fixture.",
        body=body,
        path=f"library/skills/languages/{skill_id}.md",
        kind="verified",
        triggers=("alpha beta", "gamma delta", "epsilon zeta"),
        aliases=("sample",),
        related=("other-skill",),
        sources=("https://example.com/doc",),
        commands=("python3 library/examples/sample/check.py",),
    )


class LibraryValidationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skills = load_library()
        cls.verified = load_verified()

    def test_verified_shape_graph_and_examples(self):
        errors = validate_verified(self.verified, run=True, check_urls=True)
        self.assertEqual(errors, [], "\n".join(errors[:20]))

    def test_banned_filler_is_rejected(self):
        body = (
            "https://example.com/doc\n"
            "python3 library/examples/sample/check.py\n"
            "```py file=library/examples/sample/incorrect.py\nx = 1\n```\n"
            "```py file=library/examples/sample/correct.py\nx = 2\n```\n"
            "Use best practices as needed for the 1 thing.\n"
        )
        errors = validate_skill_shape(_skill(body))
        self.assertTrue(any("best practices" in err for err in errors))

    def test_generic_advice_is_rejected(self):
        sentence = "Lists store ordered values and callers iterate them when they want each item. "
        body = (
            "https://example.com/doc\n"
            "python3 library/examples/sample/check.py\n"
            + sentence * 12
            + "```py file=library/examples/sample/incorrect.py\n"
            + "values = [1, 2, 3, 4, 5]\nreturn values\n```\n"
            + "```py file=library/examples/sample/correct.py\n"
            + "values = [1, 2, 3, 4, 6]\nreturn values\n```\n"
        )
        errors = validate_skill_shape(_skill(body))
        self.assertTrue(any("mostly generic advice" in err for err in errors), errors)

    def test_near_duplicate_bodies_are_rejected(self):
        left = _skill("one two three four five six seven eight nine ten " * 30, "left-skill")
        right = _skill("one two three four five six seven eight nine ten " * 30, "right-skill")
        self.assertGreater(jaccard(shingles(left.body), shingles(right.body)), PROSE_JACCARD_LIMIT)
        errors = validate_graph([left, right])
        self.assertTrue(any("near-duplicate" in err for err in errors))

    def test_router_abstains_and_hits_tax(self):
        router = Router(self.skills)
        vague = router.route("help me code")
        self.assertFalse(vague.confident)
        self.assertEqual(vague.hits, ())
        bug = router.route("fix the bug")
        self.assertFalse(bug.confident)
        vat = router.route("vat invoice rounding", k=5)
        self.assertTrue(vat.confident)
        self.assertEqual(vat.hits[0].skill_id, "tax-sales-and-vat")
        ref = router.route("React 19 ref callback stays null forwardRef", k=5)
        self.assertTrue(ref.confident)
        self.assertEqual(ref.hits[0].skill_id, "react-19-ref-as-prop")
        self.assertLessEqual(len(ref.hits), 5)
        tied = router.route("python error")
        self.assertFalse(tied.confident)
        cross = router.route(
            "SQLite name != 'Ada' drops the NULL row, and f-string name = '{payload}' "
            "with payload quote OR 1=1 returns Ada. Use a ? placeholder and OR name IS NULL.",
            k=5,
        )
        self.assertTrue(cross.confident)
        found = {hit.skill_id for hit in cross.hits}
        self.assertIn("sqlite-null-comparisons-are-unknown", found)
        self.assertIn("sql-fstring-interpolates-untrusted-input", found)


if __name__ == "__main__":
    unittest.main()
