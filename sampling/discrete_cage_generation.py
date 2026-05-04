'''Generates discrete cages with iron(II) centers and imide ligands.'''
import stk

def build_iron_atom():
    return stk.BuildingBlock(
        smiles='[Fe+2]',
        functional_groups=(
            stk.SingleAtom(stk.Fe(0, charge=2))
            for i in range(6)
        ),
        position_matrix=[[0, 0, 0]],
    )


def build_iron_oct_delta(ligand_smiles, use_optimizer=False):
    bb_imide = stk.BuildingBlock(
        smiles=ligand_smiles,
        functional_groups=[
            stk.SmartsFunctionalGroupFactory(
                smarts='[#6]~[#7X2]~[#35]',
                bonders=(1,),
                deleters=(),
            ),
            stk.SmartsFunctionalGroupFactory(
                smarts='[#6]~[#7X2]~[#6]',
                bonders=(1,),
                deleters=(),
            ),
        ],
    )

    kwargs = dict(metals=build_iron_atom(), ligands=bb_imide)
    if use_optimizer:
        kwargs['optimizer'] = stk.MCHammer()

    iron_oct_delta = stk.ConstructedMolecule(
        topology_graph=stk.metal_complex.OctahedralDelta(**kwargs),
    )

    return stk.BuildingBlock.init_from_molecule(
        molecule=iron_oct_delta,
        functional_groups=[stk.BromoFactory()],
    )


topology_info = {
    'm4l6': {
        'ligand_smiles': 'C1=NC(C=NBr)=CC=C1',
        'use_optimizer_for_metal_complex': True,
        'spacer_smiles': (
            'COS(=O)(=O)C1=C(C=CC(=C1)Br)C2=C(C=C(C=C2)Br)S(=O)(=O)OC'
        ),
        'topology': stk.cage.M4L6TetrahedronSpacer,
        'output_file': 'M4L6.mol',
    },
    'm4l4': {
        'ligand_smiles': 'C1=CC=NC(=C1)C=NBr',
        'use_optimizer_for_metal_complex': False,
        'spacer_smiles': (
            'C1(N=C(N(C2C=CC(Br)=CC=2)C)N=C(N(C2C=CC(Br)=CC=2)C)N=1)'
            'N(C1C=CC(Br)=CC=1)C'
        ),
        'topology': stk.cage.M4L4Tetrahedron,
        'output_file': 'M4L4.mol',
    },
}


def build_cage(geometry: str):
    geometry = geometry.lower()
    if geometry not in topology_info:
        raise ValueError(f"Unknown geometry '{geometry}'. Choose from: {list(topology_info)}")

    cfg = topology_info[geometry]

    iron_oct_delta = build_iron_oct_delta(
        ligand_smiles=cfg['ligand_smiles'],
        use_optimizer=cfg['use_optimizer_for_metal_complex'],
    )

    spacer = stk.BuildingBlock(
        smiles=cfg['spacer_smiles'],
        functional_groups=[stk.BromoFactory()],
    )

    cage = stk.ConstructedMolecule(
        topology_graph=cfg['topology'](
            building_blocks=(iron_oct_delta, spacer),
            optimizer=stk.MCHammer(),
        ),
    )

    stk.MolWriter().write(cage, cfg['output_file'])
    print(f"Written: {cfg['output_file']}")


if __name__ == '__main__':
    # Change this to 'm4l4' or 'm4l6' as needed
    build_cage('m4l6')

