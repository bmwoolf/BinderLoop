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

    # Call ColabFold’s CLI (colabfold_batch) from Python since it's not natively available in Python
    subprocess.run([
        "colabfold_batch",
        str(fasta_path),
        str(output_path),
        "--num-recycle", "3",
        "--use-gpu-relax"
    ], check=True)

    return str(output_path / "ranked_0.pdb")