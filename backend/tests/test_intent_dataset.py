"""Validate the Phase 9 intent evaluation dataset before using it with either provider."""

import json
import unittest
from collections import Counter
from pathlib import Path

from app.schemas.intent import Intent


class IntentDatasetTests(unittest.TestCase):
    def test_has_ten_examples_for_every_intent(self) -> None:
        path = Path(__file__).parent / "data" / "intent_test_cases.json"
        cases = json.loads(path.read_text(encoding="utf-8"))
        counts = Counter(case["intent"] for case in cases)
        self.assertEqual(len(cases), 80)
        self.assertEqual(set(counts), {intent.value for intent in Intent})
        self.assertTrue(all(count == 10 for count in counts.values()))


if __name__ == "__main__":
    unittest.main()
