import stk

iron_atom = stk.BuildingBlock(
    smiles='[Fe+2]',
    functional_groups=(
        stk.SingleAtom(stk.Fe(0, charge=2))
        for i in range(6)
    ),
    position_matrix=[[0, 0, 0]],
)
bb_imide = stk.BuildingBlock(
    smiles='C1=NC(C=NBr)=CC=C1',
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

iron_oct_delta = stk.ConstructedMolecule(
    topology_graph=stk.metal_complex.OctahedralDelta(
        metals=iron_atom,
        ligands=bb_imide,
        # NEW.
        optimizer=stk.MCHammer(),
    ),
)

# Assign Bromo functional groups to the metal complex.
iron_oct_delta = stk.BuildingBlock.init_from_molecule(
    molecule=iron_oct_delta,
    functional_groups=[stk.BromoFactory()],
)

# Define spacer building block.
bb3 = stk.BuildingBlock(
    smiles=(
        'COS(=O)(=O)C1=C(C=CC(=C1)Br)C2=C(C=C(C=C2)Br)S(=O)(=O)OC'
    ),
    functional_groups=[stk.BromoFactory()],
)

# Build an M4L4 Tetrahedron with a spacer.

cage2 = stk.ConstructedMolecule(
    topology_graph=stk.cage.M4L6TetrahedronSpacer(
        building_blocks=(
            iron_oct_delta,
            bb3,
        ),
        optimizer=stk.MCHammer(),
    ),
)
stk.MolWriter().write(cage2, 'M4L6.mol')

