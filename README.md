# Crystal structure prediction pipeline for Metal-Organic Cages

Repository containing simulation workflows and analysis tools used for material discovery in the field of metal-organic cages (MOCs).

## Introduction

Metal-organic cages (MOCs) are a class of supramolecular porous materials consisting of discrete clusters of metal ion corners linked by organic ligands. They are typically charged, requiring co-crystallisation with a counterion, and have attracted significant interest due to their diverse host-guest chemistry. They are large and complex systems - even simple examples contain ~300 atoms per cage - and their bulk interactions are dominated by long-range dispersion. MOCs exhibit many degrees of freedom, leading to substantial disorder in the bulk solid state, where solvent is often retained in cavities and channels. This makes experimental crystallisation challenging, motivating the use of crystal structure prediction (CSP) as a complementary computational approach.

This repository contains code for:
- Running geometry optimizations with multiple methods (traditional FFs, semi-empirical methods, MLIPs, DFT)
- High-throughput screening of crystal structures
- Analysis and post-processing of simulation outputs
- Converting between file formats (CIF, XYZ, EXTXYZ)

## Theory Levels

| Method | Package | Application |
|--------|------|------------------|
| Force Field | GULP with UFF | Fast screening, initial geometry |
| Semi-empirical | xTB with GFN-FF | Improved energetics, fast |
| MLIPs | janus with MACE | Fast screening, initial geometry and MD |
| DFT | CP2K | Accurate energies, properties |

## Project Structure

```
.
├── src/
│   ├── calcs/           # Simulation drivers
│   ├── analysis/        # Post-processing scripts
│   └── converters/      # File format converters
├── sampling/            # Sampling scripts
├── cluster_scripts/     # Job submission scripts
├── notebooks/           # Jupyter notebooks for analysis
├── configs/             # Input templates
└── data/                # Structures and results
```

## Requirements

This project requires Python 3.8+. Python dependencies are listed in 'requirements.txt' and can be installed via 'pip install -r requirements.txt'. Note that 'stk' requires 'rdkit', which must be installed separately via conda ('conda install -c conda-forge rdkit') before installing the remaining packages.
Four external packages must be installed independently and available on your PATH:  GULP (v6.1.2, academic licence required), xTB (v6.3.3), janus (v0.7.0) and CP2K (v8.2). The MLIP workflow stages additionally require a CUDA-capable GPU. Job submission scripts for HPC environments are provided in cluster_management/.

## Usage

Starting with initial .xyz file of the cage cluster and corresponding counterion, .cif or .xyz files can be produced with the scripts in 'sampling'. Then, depending on the level of theory desired, they can be geometry optimised with one of the scripts in 'calcs'. The output format can be converted depending on the next step.

### MLIP driven CSP

### FF and semi-empirical driven CSP

### Running Calculations

```bash
# Force field optimization with GULP
python src/calcs/run_gulp_rigid_uff.py --input structures.cif

# xTB calculation
python src/calcs/run_xtb_gfn_ff.py --input structures.cif
```

### Analysis

```bash
# Extract energies from GULP output
python src/analysis/read_info_uff_rigid.py --results results/
```

## License

MIT License - See LICENSE file for details.

## Citation

If you use this code in your research, please cite the relevant papers.
