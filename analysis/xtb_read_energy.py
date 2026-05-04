"""Reads all xtbopt.xyz files in the specified directory, 
extracts energy values, and saves them to a CSV file."""


import pandas as pd

def find_energy(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                print(line.split())
                if line.split()[0] =='energy:':
                    energy_value = float(line.split()[1])
                    return energy_value
        print("No line starting with 'energy:' found in the file.")
        return None
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

energy_dict = {}
for file_num in range(1, 2001):
    file_path = fr"C:\Users\aleon\OneDrive\Desktop\new_xtb_structures\{file_num}\xtbopt.xyz"
    energy_value = find_energy(file_path)
    if energy_value:
        energy_dict[file_num] = energy_value

energy_df = pd.DataFrame(energy_dict.items(), columns=['Conformation no.', 'Energy/ Eh'])
energy_df.sort_values(by='Energy/ Eh', inplace=True)
energy_df.to_csv('xtb_energiest.csv', index=False)


