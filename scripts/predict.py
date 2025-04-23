import os 
import requests
from dotenv import load_dotenv

load_dotenv()
server_url = os.getenv("SERVER_URL")

# Meta pipeline manager- we can eventually move to something like Airflow
# Send the sequence to ColabFold
def run_structure_prediction(header: str, sequence: str) -> str:
    """
    Sends a structure prediction request to a ColabFold server.
    Arguments:
        header: full FASTA header (without ">")
        sequence: protein sequence
        server_url: URL of the running ColabFold server
    Returns:
        Path to the predicted PDB file (on the server side)
    """
    print("calling backend")

    payload = {
        "header": header,
        "sequence": sequence
    }

    # Collect response from remote server hosting ColabFold
    res = requests.post(server_url, json=payload)
    res.raise_for_status()
    return res.json()["pdb"]


# Test- will need to take in full FASTA file and forward
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    # Example values (can pull from test file, input file, etc.)
    header = "ScNtx | P01391 | Short neurotoxin 1 (Naja naja)"
    sequence = "MKTLLLTLVVVTIVCLDLGYTSGCNLVCKTKDGKPCRGKRLDRCNKLSECCPKKAEYCNKCCTPKTPACPAGQN"

    result = run_structure_prediction(header, sequence)
    print("Returned PDB path:", result)
