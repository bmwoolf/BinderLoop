from scripts.predict import run_colabfold
import os

def test_colabfold_runs(tmp_path):
    fasta = "data/scntx.fasta"
    out = tmp_path / "result"
    run_colabfold(fasta, str(out))
    assert any("ranked_0.pdb" in f.name for f in out.glob("*"))
