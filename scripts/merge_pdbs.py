from Bio.PDB import PDBParser, PDBIO
import sys

def merge_pdbs(toxin_path, binder_path, output_path="merged.pdb"):
    parser = PDBParser(QUIET=True)
    toxin = parser.get_structure("toxin", toxin_path)
    binder = parser.get_structure("binder", binder_path)

    # Rename chain IDs to avoid conflicts
    for i, chain in enumerate(toxin.get_chains()):
        chain.id = "A"
    for i, chain in enumerate(binder.get_chains()):
        chain.id = "B"

    io = PDBIO()
    io.set_structure(toxin)
    io.save(output_path)

    with open(output_path, "a") as f:
        f.write("\n")
        io.set_structure(binder)
        io.save(f)

    print(f"Merged PDB saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python merge_pdbs.py toxin.pdb binder.pdb")
        sys.exit(1)
    merge_pdbs(sys.argv[1], sys.argv[2])
