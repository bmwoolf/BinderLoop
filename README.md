![BinderLoop Banner](assets/github_banner.png)

# BinderLoop
End to end, closed loop, de novo binder generation for any molecule in computational space.

## What are we trying to measure?
A good question to ask is: "What are we trying to measure?" What do we need to use in order to measure this effectively? What is the point of this pipeline, and what can we measure that we can't do effectively with other methods?

TODO: answer these questions

## Pipeline
```bash
# Step 1: Get toxin sequence manually from UniProt
Input: UniProt ID (str)
Output: FASTA (str)

# Step 2: Predict toxin structure with AlphaFold
Input: FASTA (str)
Output: PDB structure (str or Path)

# Step 3: Generate binder candidate with RFdiffusion2
Input: Target PDB (str or Path)
Output: Binder PDB (str or Path), Binder AA sequence (str)

# Step 4: Predict binder structure with AlphaFold
Input: Binder AA sequence (str)
Output: Binder PDB (str or Path)

# Step 5: Assess binding affinity with FoldX / Rosetta
Input: Toxin PDB (str), Binder PDB (str)
Output: ΔΔG score (float)

# Step 6: Codon optimize binder with DNA Chisel / Vector Builder
Input: Binder AA sequence (str)
Output: Optimized DNA sequence (str)

# Step 7: Design expression plasmid with Benchling / SnapGene
Input: DNA sequence (str)
Output: Annotated plasmid map (file or JSON)

# Step 8: Express protein in E. coli via wet lab — BL21(DE3)
Input: Plasmid (file or DNA string)
Output: Protein (biomass / wet sample)

# Step 9: Purify protein with His-tag column, SDS-PAGE
Input: Cell lysate (wet sample)
Output: Purified protein (wet sample)

# Step 10: Test binding via ELISA or neutralization assay
Input: Protein + Toxin (wet samples)
Output: Binding efficacy (float or % neutralization)

# Step 11: Analyze + iterate with a reinforcement learning loop
Input: Binding efficacy (float)
Output: New design params (dict or config file)
```

## Running locally  
```bash
python3.10 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Testing
```
# Run tests
pytest

# Run tests with coverage
pytest --cov=models --cov-report=html
```

## Notes
- UniProt ID: protein sequence (FASTA)
- PDB ID: protein structure (3D atomic coordinates)
- setup.py is used to create a package that can be installed with pip
- AF2 downloads weights to run prediction locally 
- alphafold2_ptm = version of AF2 with predicted TM-score, which is a confidence score. ColabFold auto-downloads these
- all of this is happening locally on the backend server
- ptxas is a lib that is needed to compile models for the GPU at runtime
- ColabFold uses ptxas at runtime to compile GPU kernels optimized for your hardware + input
- XLA = accelerated linear algebra, JAX's backend that makes models run fast on GPUs by compiling operations (matmul, conv2d, relu, softmax, etc.)