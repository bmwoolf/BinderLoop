import os 
import json
import requests
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

SERVER_URL = os.getenv("SERVER_URL")
OUTPUTS_DIR = Path("outputs")

def parse_fasta(path: str | Path) -> tuple[str, str]:
    """
    Parse any FASTA file to get header and sequence.
    
    Args:
        path: Path to FASTA file
        
    Returns:
        tuple: (header without '>', concatenated sequence)
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"FASTA file not found: {path}")
        
    with open(path, "r") as f:
        lines = f.read().strip().split("\n")
        if not lines or not lines[0].startswith(">"):
            raise ValueError(f"Invalid FASTA format in {path}")
            
        header = lines[0][1:].strip()
        # Join all non-header lines and remove whitespace
        sequence = "".join(lines[1:]).replace(" ", "")
        
        if not sequence:
            raise ValueError(f"No sequence found in {path}")
            
        return header, sequence

# Meta pipeline manager- we can eventually move to something like Airflow
# Send the sequence to ColabFold
def run_structure_prediction(header: str, sequence: str, output_dir: Path = OUTPUTS_DIR) -> Path:
    """
    Sends a structure prediction request to a remote ColabFold server.
    
    Args:
        header: full FASTA header (without ">")
        sequence: protein sequence
        output_dir: directory to save results
        
    Returns:
        Path to the local output directory containing results
    """
    print(f"Predicting structure for {header}")
    print(f"Sequence length: {len(sequence)}")

    # Create unique output directory for this prediction
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = header.split("|")[0].strip()  # Use first part of header as name
    run_dir = output_dir / f"{name}_{timestamp}"
    run_dir.mkdir(exist_ok=True)

    payload = {
        "header": header,
        "sequence": sequence
    }

    # Save input for reproducibility
    with open(run_dir / "input.json", "w") as f:
        json.dump(payload, f, indent=2)

    # Make prediction request
    res = requests.post(SERVER_URL, json=payload)
    res.raise_for_status()
    
    # Save response
    pdb_path = run_dir / "prediction.pdb"
    with open(pdb_path, "w") as f:
        f.write(res.json()["pdb"])
        
    # Save metadata
    with open(run_dir / "metadata.json", "w") as f:
        json.dump({
            "timestamp": timestamp,
            "header": header,
            "sequence_length": len(sequence),
            "files": {
                "input": "input.json",
                "prediction": "prediction.pdb"
            }
        }, f, indent=2)

    return run_dir

if __name__ == "__main__":
    # Example usage with different FASTA files
    fasta_files = [
        "data/scntx.fasta",  # Short-chain neurotoxin
        "data/shrt.fasta",   # SHRT binder
    ]
    
    for fasta_path in fasta_files:
        try:
            header, sequence = parse_fasta(fasta_path)
            print(f"\nProcessing {fasta_path}")
            output_dir = run_structure_prediction(header, sequence)
            print(f"Results saved to: {output_dir}")
        except Exception as e:
            print(f"Error processing {fasta_path}: {e}")
