import subprocess
import os 

def run_colabfold(input_fasta: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    cmd = [
        "colabfold_batch",
        input_fasta,
        output_dir,
        "--num-recycle", "3",
        "--use-gpu-relax"
    ]
    subprocess.run(cmd, check=True)