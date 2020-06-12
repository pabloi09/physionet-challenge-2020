import numpy as np
import os
import sys
from scipy.io import loadmat
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
import json
from get_12ECG_features import get_features

def load_challenge_data(filename):

    x = loadmat(filename)
    data = np.asarray(x['val'], dtype=np.float64)

    new_file = filename.replace('.mat', '.hea')
    input_header_file = os.path.join(new_file)

    with open(input_header_file, 'r') as f:
        header_data = f.readlines()

    return data, header_data

def getMap(system):
    input_directory1 = system.argv[1]
    input_directory2 = system.argv[2]
    print(len(os.listdir(input_directory1)))
    # Find files.
    input_files = []
    for f in os.listdir(input_directory1):
        if os.path.isfile(os.path.join(input_directory1, f)) and not f.lower().startswith('.') and f.lower().endswith('mat'):
            input_files.append(f)


    # Iterate over files.
    print('Extracting 12ECG features...')
    num_files = len(input_files)
    
    snomed_ct = {}

    for i, f in enumerate(input_files):
        print('    {}/{}...'.format(i+1, num_files))
        
        tmp_input_file1 = os.path.join(input_directory1, f)
        data1, header_data1 = load_challenge_data(tmp_input_file1)
        
        tmp_input_file2 = os.path.join(input_directory2, f)
        data2, header_data2 = load_challenge_data(tmp_input_file2)
        
        data_dict1 = get_features(data1,header_data1)
        data_dict2 = get_features(data2,header_data2)

        if data_dict1["output"] not in snomed_ct:
            snomed_ct[data_dict2["output"]] = data_dict1["output"]

    with open("snomed_dict.json", 'w') as fp:
        json.dump(snomed_ct,fp)
    print('Done.')

def getValidFiles(system):
    input_directory = system.argv[1]
    output_directory = system.argv[2]

    input_files = []
    for f in os.listdir(input_directory):
        if os.path.isfile(os.path.join(input_directory, f)) and not f.lower().startswith('.') and f.lower().endswith('mat'):
            input_files.append(f)

    snomed_ct = {}
    with open("snomed_dict.json", 'r') as fp:
        snomed_ct = json.load(fp)

    # Iterate over files.
    print('Extracting 12ECG features...')
    num_files = len(input_files)

    for i, f in enumerate(input_files):
        print('    {}/{}...'.format(i+1, num_files))
        
        tmp_input_file = os.path.join(input_directory, f)
        data, header_data = load_challenge_data(tmp_input_file)
        
        data_dict = get_features(data,header_data)
        for c in data_dict["output"].split(","):
            if c in snomed_ct:
                os.system("cp {} {}".format(tmp_input_file,output_directory))
                os.system("cp {} {}".format(tmp_input_file.replace(".mat",".hea"),output_directory))
                break

    print("Done.")


if __name__ == '__main__':
    # Parse arguments.
    if len(sys.argv) != 3:
        raise Exception('Include the input and output directories as arguments, e.g., python driver.py input output.')
    
    getValidFiles(sys)
