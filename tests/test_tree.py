import csv
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree
from ebele_tree import DecisionTreeClassifier, entropy, information_gain

class TreeTests(unittest.TestCase):
    def setUp(self):
        with (Path(__file__).resolve().parents[1] / "examples/tennis.csv").open() as f:
            rows = list(csv.DictReader(f))
        self.y = [r["Play_Tennis"] for r in rows]
        self.X = [{k:v for k,v in r.items() if k not in ("Day", "Play_Tennis")} for r in rows]

    def test_entropy(self):
        self.assertEqual(entropy([]), 0)
        self.assertEqual(entropy(["Yes"] * 3), 0)
        self.assertEqual(entropy(["Yes", "No"]), 1)
        self.assertAlmostEqual(entropy(self.y), 0.9402859587)

    def test_known_information_gain(self):
        self.assertAlmostEqual(information_gain([r["Outlook"] for r in self.X], self.y), 0.2467498198)

    def test_tennis_structure_and_predictions(self):
        m = DecisionTreeClassifier().fit(self.X, self.y)
        self.assertEqual(m.tree_["feature"], "Outlook")
        self.assertEqual(m.tree_["children"]["Sunny"]["feature"], "Humidity")
        self.assertEqual(m.tree_["children"]["Rain"]["feature"], "Wind")
        self.assertEqual(m.predict(self.X), self.y)

    def test_depth_limit(self):
        m = DecisionTreeClassifier(max_depth=0).fit(self.X, self.y)
        self.assertNotIn("feature", m.tree_)
        self.assertEqual(m.predict(self.X), ["Yes"] * 14)
        m = DecisionTreeClassifier(max_depth=1).fit(self.X, self.y)
        self.assertTrue(all("feature" not in c for c in m.tree_["children"].values()))

    def test_unseen_category_fallback(self):
        m = DecisionTreeClassifier().fit(self.X, self.y)
        row = dict(self.X[0], Outlook="Snow")
        self.assertEqual(m.predict([row]), ["Yes"])

    def test_no_gain_and_min_samples(self):
        m = DecisionTreeClassifier().fit([{"a":"x"}, {"a":"x"}], ["N", "Y"])
        self.assertNotIn("feature", m.tree_)
        m = DecisionTreeClassifier(min_samples_split=15).fit(self.X, self.y)
        self.assertNotIn("feature", m.tree_)

    def test_svg_is_valid(self):
        m = DecisionTreeClassifier().fit(self.X, self.y)
        with tempfile.TemporaryDirectory() as tmp:
            path = m.export_svg(Path(tmp) / "tree.svg")
            root = ElementTree.parse(path).getroot()
            texts = [e.text for e in root.iter() if e.tag.endswith("}text")]
            self.assertIn("Outlook", texts)
            self.assertIn("Humidity", texts)
            self.assertIn("Wind", texts)

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            DecisionTreeClassifier().predict(self.X)
        with self.assertRaises(ValueError):
            DecisionTreeClassifier(max_depth=-1)
        with self.assertRaises(ValueError):
            DecisionTreeClassifier().fit([], [])
        with self.assertRaises(ValueError):
            DecisionTreeClassifier().fit([{"a":None}], ["Y"])
        with self.assertRaises(ValueError):
            DecisionTreeClassifier().fit([{"a":1}, {"b":2}], ["Y", "N"])

if __name__ == "__main__":
    unittest.main()
