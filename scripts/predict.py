import os 
import subprocess
from pathlib import Path

# Meta pipeline manager- we can eventually move to something like Airflow
def run_structure_prediction(sequence: str, name: str, output_dir: str = "outputs") -> str:
    """Runs ColabFold on an amino acid sequence."""
    output_path = Path(output_dir) / f"{name}_af"
    fasta_path = Path(output_dir) / f"{name}.fasta"
    os.makedirs(output_path, exist_ok=True)

    with open(fasta_path, "w") as f:
        f.write(f">{name}\n{sequence}\n")

    # Call ColabFold's CLI with Metal acceleration
    subprocess.run([
        "colabfold_batch",
        str(fasta_path),
        str(output_path),
        "--num-recycle", "3",
        "--use-gpu"  # This will use Metal on Apple Silicon
    ], check=True)

    final_model = output_path / "ranked_0.pdb"
    
    if not final_model.exists():
        raise FileNotFoundError(f"No ranked_0.pdb found in {output_path}")
    return str(final_model)
    