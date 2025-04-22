import time
from pathlib import Path
from scripts.predict import run_structure_prediction

def test_colabfold_runs(tmp_path):
    start = time.time()
    
    # Read the sequence from the FASTA file
    fasta_path = Path("data/scntx.fasta")
    print(f"fasta_path: {fasta_path}")
    with open(fasta_path) as f:
        # Skip the header line
        next(f)
        # Get the sequence
        sequence = f.read().strip()
        print(f"sequence: {sequence}")
    print(f"tmp_path: {tmp_path}")
    # Run prediction
    out = tmp_path / "result"
    print(f"out: {out}")
    run_structure_prediction(
        sequence=sequence,
        name="scntx",
        output_dir=str(out)
    )

    duration = time.time() - start
    print(f"\nColabFold runtime: {duration:.2f} seconds")
    
    assert any("ranked_0.pdb" in f.name for f in out.glob("*"))
