""" EEG Electrodes list/map: we have data from 17 electrodes
0 = Pz, on center line
1 = P3, mirror of 6, P4
2 = P7, mirror of 7, P8
3 = O1, mirror of 5, O2
4 = Oz, on center line
5 = O2, mirror of 3, O1
6 = P4, mirror of 1, P3
7 = P8, mirror of 3, P7
8 = P1, mirror of 16, P2
9 = P5, mirror of 15, P6
10 = PO7, mirror of 14, PO8
11 = PO3, mirror of 13, PO4
12 = POz, on center line
13 = PO4, mirror of 11, PO3
14 = PO8, mirror of 10, PO7
15 = P6, mirror of 9, P5
16 = P2, mirror of 8, P1

So, for example, to swap O1 with O2, you would use:
swap_electrodes([0, 1, 2, 5, 4, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
"""
import numpy as np

def swap_electrodes(new_order: list[int]):
    # Make sure the original data is in folder data_original
    # Only looking at subject #1, change *both* of the next two lines if you 
    #    want a different subject
    # TODO
    path_orig = 'data_original/thingseeg2_preproc/sub-01/'
    # TODO
    path_new = 'data/thingseeg2_preproc/sub-01/'

    # First, swap the training data
    filename = path_orig + 'preprocessed_eeg_training.npy'
    with open(filename, 'rb') as fin:
        data = np.lib.format.read_array(
            fin, 
            allow_pickle=True
        )
    # Extract the dictionary from the 0-dim ndarray
    data_dict = data.item()
    print("EEG Channels: ", data_dict['ch_names'])
    # Get the actual EEG readings
    data_eeg = data_dict['preprocessed_eeg_data']
    # Print the first value for *each* electrode you want to swap
    # TODO
    print("Electrode values:")
    print(data_eeg[0][0][3][0])
    print(data_eeg[0][0][5][0])
    print()
    # Move the electrodes to the first dimension to make it easy to swap
    data_eeg = np.transpose(data_eeg, [2, 1, 0, 3])
    # This is where you swap electrodes
    data_eeg = data_eeg[new_order]
    # Move the electrodes back so the shape of the data is where it was
    data_eeg = np.transpose(data_eeg, [2, 1, 0, 3])
    # Re-assign the EEG readings in the data object to the newly swapped data
    data_dict['preprocessed_eeg_data'] = data_eeg
    # Print out the first value for each electrode you swapped to verify
    # TODO
    print("Swapped electrode values:")
    print(data_eeg[0][0][3][0])
    print(data_eeg[0][0][5][0])
    print()
    filename = path_new + 'preprocessed_eeg_training.npy'
    np.save(filename, data, allow_pickle=True)

    # Next, do it again with the test data
    filename = path_orig + 'preprocessed_eeg_test.npy'
    with open(filename, 'rb') as fin:
        data = np.lib.format.read_array(
            fin, 
            allow_pickle=True
        )
    # Extract the dictionary from the 0-dim ndarray
    data_dict = data.item()
    # Get the actual EEG readings
    data_eeg = data_dict['preprocessed_eeg_data']
    print(data_eeg.shape)
    # Print the first value for each electrode you want to swap
    # TODO
    print("Electrode values:")
    print(data_eeg[0][0][3][0])
    print(data_eeg[0][0][5][0])
    print()
    # Move the electrodes to the first dimension to make it easy to swap
    data_eeg = np.transpose(data_eeg, [2, 1, 0, 3])
    # This is where you swap electrodes
    data_eeg = data_eeg[new_order]
    # Move the electrodes back so the shape of the data is where it was
    data_eeg = np.transpose(data_eeg, [2, 1, 0, 3])
    # Re-assign the EEG readings in the data object to the newly swapped data
    data_dict['preprocessed_eeg_data'] = data_eeg
    # Print out the first value for each electrode you swapped to verify
    # TODO
    print("Swapped electrode values:")
    print(data_eeg[0][0][3][0])
    print(data_eeg[0][0][5][0])
    print()
    filename = path_new + 'preprocessed_eeg_test.npy'
    np.save(filename, data, allow_pickle=True)


# TODO
swap_electrodes([0, 1, 2, 5, 4, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
