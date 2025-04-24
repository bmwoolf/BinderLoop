import json
import time
import pytest
from pathlib import Path
from scripts.predict import parse_fasta, run_structure_prediction

def test_structure_prediction_pipeline(tmp_path):
    """Test the full structure prediction pipeline with file outputs"""
    start = time.time()
    
    # Setup test output directory
    test_output = tmp_path / "outputs"
    test_output.mkdir()
    
    # Read and parse FASTA
    fasta_path = Path("data/scntx.fasta")
    header, sequence = parse_fasta(fasta_path)
    
    # Run prediction
    result_dir = run_structure_prediction(
        header=header,
        sequence=sequence,
        output_dir=test_output
    )
    
    # Verify outputs
    assert result_dir.exists(), "Result directory not created"
    assert (result_dir / "prediction.pdb").exists(), "PDB file not created"
    assert (result_dir / "input.json").exists(), "Input file not created"
    assert (result_dir / "metadata.json").exists(), "Metadata file not created"
    
    # Verify input contents
    with open(result_dir / "input.json") as f:
        input_data = json.load(f)
        assert input_data["header"] == header
        assert input_data["sequence"] == sequence
    
    # Verify metadata contents
    with open(result_dir / "metadata.json") as f:
        metadata = json.load(f)
        assert metadata["header"] == header
        assert metadata["sequence_length"] == len(sequence)
        assert "timestamp" in metadata
        assert metadata["files"]["prediction"] == "prediction.pdb"
    
    # Verify PDB file is not empty
    assert (result_dir / "prediction.pdb").stat().st_size > 0, "PDB file is empty"
    
    duration = time.time() - start
    print(f"\nPipeline runtime: {duration:.2f} seconds")

def test_parse_fasta_invalid_file():
    """Test FASTA parsing with invalid file"""
    with pytest.raises(FileNotFoundError):
        parse_fasta("nonexistent.fasta")

def test_parse_fasta_invalid_format(tmp_path):
    """Test FASTA parsing with invalid format"""
    bad_fasta = tmp_path / "bad.fasta"
    bad_fasta.write_text("Not a FASTA file")
    
    with pytest.raises(ValueError, match="Invalid FASTA format"):
        parse_fasta(bad_fasta)

def test_parse_fasta_empty_sequence(tmp_path):
    """Test FASTA parsing with empty sequence"""
    empty_fasta = tmp_path / "empty.fasta"
    empty_fasta.write_text(">header\n")
    
    with pytest.raises(ValueError, match="No sequence found"):
        parse_fasta(empty_fasta)

def test_multiple_sequences():
    """Test processing multiple sequences"""
    sequences = [
        "data/scntx.fasta",
        "data/shrt.fasta"
    ]
    
    for fasta_path in sequences:
        header, sequence = parse_fasta(fasta_path)
        assert len(sequence) > 0, f"Empty sequence in {fasta_path}"
