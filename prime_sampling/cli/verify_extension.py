"""Check the extension [162, 651/4] cell by cell with the official probe. Python 3.10+."""
import json
from fractions import Fraction as F
from pathlib import Path
from ..accounting.ledger import probe, fmt

HERE = Path(__file__).resolve().parents[2] / "data" / "ext162"


def main():
    cells = json.loads((HERE / "manifest.json").read_text())
    cells.sort(key=lambda c: F(c["l"]))
    assert F(cells[0]["l"]) == 162 and F(cells[-1]["r"]) == F(651, 4)
    assert all(F(x["r"]) == F(y["l"]) for x, y in zip(cells, cells[1:]))
    worst = {}
    for c in cells:
        a, z = F(c["l"]), F(c["r"])
        tables = [("extra", k, a, z, g, HERE / f) for k, g, f in c["t"]]
        res = probe(a, z, tables, [HERE / f for f in c["b"]])
        for br, r in res.items():
            assert r[1] > 0, (a, z, br, r)
            worst[br] = r[1] if br not in worst else min(worst[br], r[1])
        print(f"[{a}, {z}]", *(f"{br} margin={fmt(r[1])}" for br, r in res.items()), flush=True)
    print(len(cells), "adjoining cells cover [162, 651/4];", *(f"{b} min {fmt(v)}" for b, v in worst.items()))


if __name__ == "__main__":
    main()
