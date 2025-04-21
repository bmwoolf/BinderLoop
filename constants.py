"""
PDB (Protein Data Bank) structure IDs for various protein complexes and toxins.
See: https://www.rcsb.org/
"""

PDB_STRUCTURES = {
    # Identifier type
    "protein_id_type": "uniprot_id",
    
    # Three-finger toxins
    "3ftx": "1QKD",                    # Basic three-finger toxin
    "type_ia_cytotoxin": "5NQ4",       # Type IA cytotoxin
    
    # Acetylcholine-related structures
    "ach_receptor": "7Z14",            # Torpedo receptor
    "achbp_binding": "3WIP",           # AChBP binding site
    
    # Complex structures
    "cobra_achbp": "1Y15",             # α-cobratoxin-AChBP complex
    "neurotoxin": "7Z14",              # Short-chain α-neurotoxin
    "lng_complex": "9BK5",             # LNG binder complex
    "b10_cytx": "9BK6",                # B10 CYTX binder complex
    "shrt": "9BK7",                    # SHRT binder complex
}