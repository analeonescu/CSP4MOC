# CSP4MOC - Crystal Structure Prediction for Metal-Organic Cages

Simulation workflows and analysis tools for crystal structure prediction (CSP) of metal-organic cages (MOCs), developed as part of my PhD thesis and an accompanying publication (in preparation). The pipeline was used to study and analyse four cage systems.

## Background

Metal-organic cages (MOCs) are supramolecular porous materials made of discrete clusters of metal-ion corners linked by organic ligands. These clusters are typically charged and will be isolated with a counterion, and are of interest for their host–guest chemistry. Even simple cages contain over ~300 atoms, and their bulk packing is dominated by long-range dispersion interactions. This, combined with substantial conformational disorder and retained solvent in cavities and channels, makes experimental crystallisation difficult - motivating CSP as a complementary computational approach for their characterisation and rationalisation.

This repository covers the full pipeline used for that work:
- generating candidate crystal structures (random cell/cluster sampling)
- geometry optimisation across multiple levels of theory (force field → semi-empirical → MLIP → DFT)
- converting between file formats at each handoff (.cif, .xyz, .extxyz, GULP's own `.gin`)
- HPC job creation and submission for each calculation type
- extracting energies/ densities from outputs
- data post-processing for analysis, visualisation, and noise filtering


## Theory levels

| Method | Package | Role in the pipeline |
|---|---|---|
| Force field | GULP with UFF | Fast initial screening, coarse geometry |
| Semi-empirical | xTB with GFN-FF | Improved energetics, still fast |
| MLIP | janus with MACE | Fast screening, geometry optimisation, and MD |
| DFT | CP2K | Accurate energies and properties on shortlisted structures |

Structures are generally funnelled from cheap to expensive methods: bulk sampling and UFF screening narrow down candidates before promoting the top performers to xTB, MLIP, and finally DFT.

## Repository structure

```
.
├── sampling/                 # Generate candidate cage/counterion structures
├── converters/                # File format conversion between pipeline stages
├── analysis/                  # Energy/density extraction, database building, visualisation
│   └── notebooks/             # Notebooks for MACE/janus and GULP post-processing
├── src/csp4moc/               # Reusable package built alongside the original scripts
│   ├── io.py                  # Structure and calculation-output readers
│   ├── analysis.py            # Ranking and result-processing helpers
│   └── plotting.py            # Reusable analysis plots
├── cluster_management/        # HPC job creation, submission, and CP2K input examples
│   ├── calcs/
│   ├── cp2k_examples/
│   └── job_scripts/
├── others/                     # Legacy/one-off scripts kept for reference
├── LICENSE
└── README.md
```

The original scripts and notebooks are retained for reproducibility. New code can
import reusable functionality from `csp4moc` without requiring the existing
workflow to be reorganised.

## Requirements

- Python 3.8+
- Scientific Python stack: `numpy`, `pandas`, `ase`, `plotly`
- `stk` for cage construction (requires `rdkit`, install via `conda install -c conda-forge rdkit` before other packages)
- `pyxtal` for random crystal/cluster sampling
- `chemiscope` for interactive structure/energy visualisation

See `requirements.txt` for a pinned install list.

To install the reusable package in editable mode from the repository root:

```bash
python -m pip install -e .
```

External codes (must be installed separately and available on `PATH`):

| Tool | Version used | Notes |
|---|---|---|
| GULP | 6.1.2 | Academic licence required |
| xTB | 6.3.3 | Available on local machines|
| janus | 0.7.0 | MLIP driver for MACE |
| CP2K | 8.2 | Academic licence required |
| Zeo++ | 0.3 | Available open-source |

The MLIP (janus/MACE) stage additionally requires a CUDA-capable GPU.

The calculations behind the published results were run on UCL's HPC clusters: Myriad (xTB, GULP), Young (janus/MACE, GPU nodes), and Kathleen (CP2K).

## Methodology

The pipeline follows a hierarchical CSP funnel (cheap → expensive), applied to four Fe₄ tetrahedral cage systems (each with more than one counterion variant):

1. Gas-phase screening. For each cage–counterion stoichiometric unit, 2,000 configurations were randomly generated with PyXtal (no periodic boundary conditions), geometry-optimised with xTB/GFN-FF (vtight convergence), and ranked by cohesive energy.

2. Periodic sampling (force field). The top 1,000 lowest-energy gas-phase configurations were used to seed periodic unit cells - 3 cells per space group across 7 commonly observed space groups (P1, P-1, P2, Cc, P2₁/c, P2₁2₁2₁, Pna2₁), giving ~21,000 candidate structures, geometry-optimised with GULP/UFF under the rigid-unit + minimum-image approximation (BFGS, force convergence 0.1 eV Å⁻¹).

3. MLIP-driven refinement. For the four systems taken forward, unit cells of 1, 2, and 4 cages were sampled in the P1 space group only (2,000 configurations per cell size, 10 Å cutoffs), then optimised with MACE-MOF-v2 via janus-core using a staged-pressure protocol (high external pressure first, e.g. 5–50 GPa depending on cell size, then relaxed at 0 GPa; force convergence 0.005 eV Å⁻¹). The lowest-energy structures were validated with NVT molecular dynamics (300 K, 20,000 steps, 0.5 fs timestep) to confirm they sat in genuine energy minima rather than sampling artefacts.

4. DFT refinement. The lowest-energy candidates from each stage were refined with CP2K (PBE + D3, GTH pseudopotentials, MOLOPT basis sets, 300 Ry cutoff) for a final accuracy check and to benchmark the MLIP energies (R² = 0.934 against MACE across all sampled cell sizes).

5. Porosity analysis. Zeo++ was used to compute the largest cavity diameter (Di) and pore-limiting diameter (Df) for the MACE-optimised structures, to compare relative porosities across cage/counterion combinations.

Full derivations, convergence-criteria justifications, and the force-field comparison (UFF vs. pGFN-FF) that motivated the final workflow choices are in Chapter 3 and Appendix A2 of the thesis.

## Usage

The pipeline runs roughly in this order:

**1. Generate candidate structures** (`sampling/`)
Build discrete cages and generate randomised gas-phase or crystalline cluster/counterion arrangements as starting points for optimisation.
```bash
python sampling/discrete_cage_generation.py
python sampling/random_xtal_cells_constraints.py
```

**2. Optimise geometries** at the desired level of theory using the scripts in `cluster_management/calcs/` (job creation/submission for GULP, xTB, and janus/MACE) and the CP2K examples in `cluster_management/cp2k_examples/` for DFT. See `cluster_management/job_scripts/` for the corresponding HPC submission templates.

**3. Convert formats** between stages as needed (`converters/`):
```bash
# CIF -> EXTXYZ, e.g. for chemiscope visualisation
python converters/cif_to_extxyz.py --input "*.cif" --output combined.extxyz

# xTB output -> EXTXYZ
python converters/xtb_output_to_extxyz.py --input "*/xtbopt.xyz" --output combined.extxyz

# CP2K restart -> CIF
python converters/cp2k_to_cif.py input.restart output.cif

# Modify GULP .gin files between theory levels
python converters/modify_gin_file.py --theory gfnff --dir . --pattern "xtal_*.gin"
```

**4. Analyse results** (`analysis/`):
```bash
# Extract energy/density from GULP output, build the ranked structure list
python analysis/gulp_read_energy.py
python analysis/gulp_top_performers.py

# Extract energies from xTB optimisations
python analysis/xtb_read_energy.py

# Build a Chemiscope-ready dataset of energy vs. density by space group
python analysis/chemiscope_energy_density.py
```
Notebooks in `analysis/notebooks/` cover MACE/janus-specific post-processing (porosity, MD trajectories) and GULP energy/density visualisation.

New notebooks can use the package, for example:

```python
from csp4moc.analysis import load_gulp_results, rank_structures

results = load_gulp_results("results/gulp")
ranked = rank_structures(results)
```

## Citation

A publication describing this pipeline is currently in preparation. Citation details will be added here once available - check back or open an issue if you'd like to cite this work in the meantime.

## License

MIT License — see [LICENSE](LICENSE) for details.