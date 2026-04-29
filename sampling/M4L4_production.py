import stk

# Produce a Fe+2 atom with 6 functional groups.
iron_atom = stk.BuildingBlock(
    smiles='[Fe+2]',
    functional_groups=(
        stk.SingleAtom(stk.Fe(0, charge=2))
        for i in range(6)
    ),
    position_matrix=[[0, 0, 0]],
)

# Define coordinating ligand with dummy bromine groups and
# metal coordinating functional groups.
bb_imide = stk.BuildingBlock(
    smiles='C1=CC=NC(=C1)C=NBr', #smiles of imide coord at Fe
    functional_groups=[
        stk.SmartsFunctionalGroupFactory(
            smarts='[#6]~[#7X2]~[#35]',
            bonders=(1, ),
            deleters=(),
        ),
        stk.SmartsFunctionalGroupFactory(
            smarts='[#6]~[#7X2]~[#6]',
            bonders=(1, ),
            deleters=(),
        ),
    ],
)



# Build iron complex with delta stereochemistry.
iron_oct_delta = stk.ConstructedMolecule(
    topology_graph=stk.metal_complex.OctahedralDelta(
        metals=iron_atom,
        ligands=bb_imide,
    ),
)

# Assign Bromo functional groups to the metal complex.
iron_oct_delta = stk.BuildingBlock.init_from_molecule(
    molecule=iron_oct_delta,
    functional_groups=[stk.BromoFactory()],
)
# stk.MolWriter().write(bb_imide, 'bb_test.mol')

smile = 'C1(N=C(N(C2C=CC(Br)=CC=2)C)N=C(N(C2C=CC(Br)=CC=2)C)N=1)N(C1C=CC(Br)=CC=1)C' #smiles of triamide
# Define spacer building block.
bb3 = stk.BuildingBlock(
    smiles=(smile),
    functional_groups=[stk.BromoFactory()],
)

# Build an M4L6 Tetrahedron with a spacer.
cage2 = stk.ConstructedMolecule(
    topology_graph=stk.cage.M4L4Tetrahedron(
        building_blocks=(
            iron_oct_delta,
            bb3,
        ),
        optimizer = stk.MCHammer(),
    ),
)

stk.MolWriter().write(cage2, 'M4L4.mol')

