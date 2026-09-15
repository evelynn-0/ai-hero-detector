import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("score", ROOT / "scripts/score.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def unit(values, uid="U1"):
    return {"id": uid, "quote": "synthetic calculation fixture", "scores": dict(zip(module.KEYS, values))}

class ScoreTests(unittest.TestCase):
    def test_endpoints(self):
        self.assertEqual(module.calculate({"units": [unit([4,4,4,4,4,0])]})["score"], 100)
        self.assertEqual(module.calculate({"units": [unit([0,0,0,0,0,4])]})["score"], 0)

    def test_information_gap_only(self):
        self.assertEqual(module.calculate({"units": [unit([0,0,0,0,0,0])]})["score"], 15)

    def test_empty_abstains(self):
        self.assertIsNone(module.calculate({"units": []})["score"])

    def test_equal_weight_and_half_up(self):
        data = {"units": [unit([0,0,0,0,0,4]), unit([1,0,0,0,0,4], "U2")]}
        result = module.calculate(data)
        self.assertEqual(result["raw_score"], 2.5)
        self.assertEqual(result["score"], 3)

    def test_v_monotonic(self):
        results = [module.calculate({"units": [unit([2,2,2,2,2,v])]})["raw_score"] for v in range(5)]
        self.assertTrue(all(a > b for a,b in zip(results, results[1:])))

    def test_examples(self):
        for name, expected in (("01",91),("02",0)):
            data = json.loads((ROOT / f"examples/annotations-{name}.json").read_text())
            self.assertEqual(module.calculate(data)["score"], expected)

    def test_reject_bad_values(self):
        for bad in (-1,5,1.5,True,"3",None):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                module.calculate({"units": [unit([bad,0,0,0,0,4])]})

    def test_reject_missing_dimension(self):
        u = unit([0,0,0,0,0,4]); del u["scores"]["V"]
        with self.assertRaises(ValueError): module.calculate({"units": [u]})

    def test_reject_duplicate_ids(self):
        with self.assertRaises(ValueError): module.calculate({"units": [unit([0]*6), unit([0]*6)]})

    def test_reject_empty_evidence(self):
        u = unit([0]*6); u["quote"] = " "
        with self.assertRaises(ValueError): module.calculate({"units": [u]})

if __name__ == "__main__":
    unittest.main()
