import requests
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()
SERVER_URL = os.getenv("SERVER_URL")

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
        sequence = "".join(lines[1:]).replace(" ", "")
        
        if not sequence:
            raise ValueError(f"No sequence found in {path}")
            
        return header, sequence

def run_structure_prediction(header: str, sequence: str) -> str:
    """
    Sends a structure prediction request to a remote ColabFold server.
    
    Args:
        header: full FASTA header (without ">")
        sequence: protein sequence
        
    Returns:
        PDB file content as string
    """
    print(f"Predicting structure for {header}")
    print(f"Sequence length: {len(sequence)}")

    payload = {
        "header": header,
        "sequence": sequence
    }

    res = requests.post(SERVER_URL, json=payload)
    res.raise_for_status()
    
    return res.json()["pdb"]  # Return PDB content directly

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
            pdb_content = run_structure_prediction(header, sequence)
            print(f"Received PDB structure of length: {len(pdb_content)}")
        except Exception as e:
            print(f"Error processing {fasta_path}: {e}")
