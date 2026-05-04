"""Obtain file names for top performers of UFF rigid calculations,
and convert them to GIN files for pgfn FF using atomsk.

NOTE: CIF files output from GULP need to be slightly modified
before they can be used safely by atomsk."""

import pandas as pd
import os

sys_name = 'xtal_OH_pf6'
csv_path = r'C:\Users\aleon\OneDrive\Desktop\oh_pf6_top10_each_relevant_sg_uff_rigid.csv'
spgs = [1, 2, 3, 9, 14, 19, 33]


def get_top_performers(csv_path: str, space_groups: list, n_rows: int = 99) -> dict:
    """
    Read top-performing structure indices from a CSV file.

    Args:
        csv_path (str): Path to the CSV file.
        space_groups (list): Space group numbers, one per column pair.
        n_rows (int): Number of rows to read per space group.

    Returns:
        dict: {space_group: [entry_indices]}
    """
    df = pd.read_csv(csv_path)
    top_performers = {}

    for index, spg in enumerate(space_groups):
        col = 1 + index * 3
        if col < df.shape[1]:
            entries = df.iloc[:n_rows, col].fillna(0).astype(int).tolist()
            top_performers[spg] = entries

    return top_performers


def convert_cif_to_gin(sys_name: str, top_performers: dict) -> None:
    """
    Convert CIF files to GIN format using atomsk.

    Args:
        sys_name (str): System name used in file naming.
        top_performers (dict): {space_group: [entry_indices]}
    """
    for spg, entries in top_performers.items():
        for entry in entries:
            cif_file = f"{sys_name}_sg_{spg}_{entry}_uff_rigid.cif"
            gin_file = f"pgfnff_{sys_name}_sg_{spg}_{entry}.gin"
            os.system(f"atomsk {cif_file} {gin_file}")


if __name__ == "__main__":
    top_performers = get_top_performers(csv_path, spgs)
    convert_cif_to_gin(sys_name, top_performers)

