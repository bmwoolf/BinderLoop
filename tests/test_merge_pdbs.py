import pytest
from pathlib import Path
from scripts.merge_pdbs import merge_pdbs, run_interface_analyzer

def test_merge_pdbs(tmp_path):
    """Test merging PDB files"""
    # Setup
    outputs = Path("outputs")
    scntx_dir = sorted(outputs.glob("7Z14_5_*"))[-1]
    shrt_dir = sorted(outputs.glob("9BK7_1_*"))[-1]
    
    protein_pdb = scntx_dir / "prediction.pdb"
    binder_pdb = shrt_dir / "prediction.pdb"
    merged_pdb = tmp_path / "merged.pdb"
    
    # Test merging
    result_path = merge_pdbs(protein_pdb, binder_pdb, merged_pdb)
    
    # Verify
    assert result_path.exists()
    content = result_path.read_text()
    assert "ATOM" in content
    assert "TER" in content
    assert "END" in content
    
    # Verify chain IDs
    assert "ATOM      1  N   " in content
    protein_lines = [l for l in content.split("\n") if l.startswith("ATOM")]
    assert any(" A " in line for line in protein_lines)  # Chain A exists
    assert any(" B " in line for line in protein_lines)  # Chain B exists

@pytest.mark.skipif(not Path("/path/to/rosetta").exists(),
                   reason="Rosetta not installed")
def test_interface_analyzer(tmp_path):
    """Test Rosetta interface analysis"""
    # Setup - use merged PDB from previous test
    outputs = Path("outputs")
    merged_pdb = outputs / "merged" / "complex.pdb"
    
    # Run analysis
    results = run_interface_analyzer(merged_pdb)
    
    # Verify results contain expected keys
    assert "stdout" in results
    # Add more specific assertions based on expected Rosetta output 