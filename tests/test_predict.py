from pathlib import Path
from scripts.predict import run_structure_prediction

def test_colabfold_runs(tmp_path):
    # Read the sequence from the FASTA file
    fasta_path = Path("data/scntx.fasta")
    with open(fasta_path) as f:
        # Skip the header line
        next(f)
        # Get the sequence
        sequence = f.read().strip()
        print(f"sequence: {sequence}")
    
    # Run prediction
    out = tmp_path / "result"
    run_structure_prediction(
        sequence=sequence,
        name="scntx",
        output_dir=str(out)
    )
    
    assert any("ranked_0.pdb" in f.name for f in out.glob("*"))
