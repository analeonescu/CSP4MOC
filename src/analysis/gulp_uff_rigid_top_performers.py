'''obtain file name for top performers of uff rigid,
    and create gin files for pgfn ff using atomsk
    NOTE that atm the cif files output from gulp need to be
    slightly modified to be used safely by atomsk!!!!!!!
'''

import pandas as pd
import os

sys_name = 'xtal_OH_pf6'
csv_path = fr'C:\Users\aleon\OneDrive\Desktop\oh_pf6_top10_each_relevant_sg_uff_rigid.csv'

def get_top_performers(file_name: str = csv_path):
    df = pd.read_csv(file_name)
    dic_values = {}
    keys = [1,2,3,9,14,19,33]
    
    for index, key in enumerate(keys):
        start_column = 1 + index * 3
        if start_column < df.shape[1]:
            values = df.iloc[:99, start_column].fillna(0).astype(int).tolist()
            dic_values[key] = values
    
    return dic_values

your_files = get_top_performers()
print(your_files)

for sg, num_entry in your_files.items():
    for i in sg:
        for entry in num_entry:
            os.system(fr"atomsk {sys_name}_sg_{i}_{entry}_uff_rigid.cif pgfnff_{sys_name}_sg_{i}_{entry}.gin")

