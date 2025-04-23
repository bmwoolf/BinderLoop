import os 
import subprocess
from pathlib import Path

# Meta pipeline manager- we can eventually move to something like Airflow
# Send the sequence to ColabFold
def run_structure_prediction(sequence: str, name: str, output_dir: str = "outputs") -> str:
    """
    Sends a structure prediction request to a ColabFold server.
    Arguments:
        header: full FASTA header (without ">")
        sequence: protein sequence
        server_url: URL of the running ColabFold server
    Returns:
        Path to the predicted PDB file (on the server side)
    """

    payload = {
        "header": header,
        "sequence": sequence
    }

    # Collect response from remote server hosting ColabFold
    res = requests.post(server_url, json=payload)
    res.raise_for_status()
    return res.json()["pdb_file"]