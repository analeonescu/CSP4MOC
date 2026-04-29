import stk

metal = stk.BuildingBlock(
    smiles='[Fe+2]',
    functional_groups=(
        stk.SingleAtom(stk.Fe(0, charge=2))
        for i in range(6)
    ),
    position_matrix=[[0, 0, 0]],
)

bidentate = stk.BuildingBlock(
    smiles='OCC(CBr)N=Cc1ccccn1',
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
    ]
)

complex = stk.ConstructedMolecule(
    topology_graph=stk.metal_complex.OctahedralLambda(
        metals=metal,
        ligands=bidentate,
        optimizer=stk.MCHammer(),
    ),
)

stk.MolWriter().write(molecule=complex, path='complex.mol')



core1 = stk.BuildingBlock(
    smiles="N(F)(F)F",
    functional_groups=stk.FluoroFactory(bonders =(0),deleters=(0, 1, 2)),
)
arm = stk.BuildingBlock.init_from_file('complex.mol', functional_groups= stk.BromoFactory(deleters=(0, 1, 2)))

trial = stk.cage.OnePlusOne((arm, core1))

ncore = stk.ConstructedMolecule(stk.small.NCore(
    core_building_block=core1,
    arm_building_blocks=arm,
    repeating_unit="A",  # 'AAA' would work too.
))