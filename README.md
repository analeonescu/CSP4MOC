# Crystal structure prediction pipeline for Metal-Organic Cages

Repository containing simulation workflows and analysis tools used for material discovery in the field of metal-organic cages (MOCs).

## Overview

This repository contains code for:
- Running geometry optimizations with multiple methods (GULP/UFF, GFNn-xTB, DFT)
- High-throughput screening of crystal structures
- Analysis and post-processing of simulation outputs
- Converting between file formats (CIF, XYZ, EXTXYZ)

## Theory Levels

| Method | Code | Typical Use Case |
|--------|------|------------------|
| Force Field | GULP with UFF | Fast screening, initial geometry |
| Semi-empirical | xTB with GFN-FF | Improved energetics, fast |
| DFT | CP2K | Accurate energies, properties |

## Project Structure

```
.
├── src/
│   ├── calcs/           # Simulation drivers
│   ├── analysis/        # Post-processing scripts
│   └── converters/      # File format converters
├── workflows/           # High-level workflows
├── cluster_scripts/     # Job submission scripts
├── notebooks/           # Jupyter notebooks for analysis
├── configs/             # Input templates
└── data/                # Structures and results
```

## Requirements

- Python 3.8+
- ASE (Atomic Simulation Environment)
- Scientific Python stack (numpy, pandas, matplotlib)

### Method-Specific

- **GULP**: For force field calculations
- **xtb**: For semi-empirical GFN-FF calculations
- **CP2K**: For DFT calculations (optional)

## Usage

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
