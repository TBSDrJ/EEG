import math
import numpy as np
import matplotlib.pyplot as plt

def get_data() -> np.ndarray:
    """Read data from disk. 
    
    I chose the last subject for no particular reason, starting w/train data.
    The data comes back as a 0-dim ndarray containing a dictionary.
    The 'preprocessed_eeg_data' key contains 16540 images worth of eeg
        readings.  Each image is seen 4 times, readings from 17 electrodes,
        at 100 time steps.
    """
    path = 'osfstorage-archive/sub-10/'
    filename = path + 'preprocessed_eeg_training.npy'
    with open(filename, 'rb') as fin:
        data = np.lib.format.read_array(
            fin, 
            allow_pickle=True
        )
    # Extract the dictionary from the 0-dim ndarray
    data = data.item()
    print(data['ch_names'])
    data = data['preprocessed_eeg_data']
    # Just restrict to the first image for now.
    data = data[1]
    return data

def plot_all_electrodes(data: np.ndarray, filename: str = None) -> None:
    """Draws 1 subplot for each electrode in one graph."""
    t = np.arange(100)
    fig, axs = plt.subplots(3,6, figsize=(15,10))
    for ax, elec_data in zip(axs.flat[:17], data):
        ax.plot(
            t, elec_data[0], 'b-',
            t, elec_data[1], 'r-',
            t, elec_data[2], 'g-',
            t, elec_data[3], 'k-',
        )
    if filename is not None:
        plt.savefig(filename)
    else:
        plt.show()

def align_peaks(data: np.ndarray) -> np.ndarray:
    """Shift trials to encourage alignment of peaks."""
    # Compare the 2nd -> 4th to the 1st
    for i in range(17):
        for j in range(1,4):
            min_l1_dist = float('inf')
            min_l2_dist = float('inf')
            l1_shift = 0
            l2_shift = 0
            # How much to shift by, 0 -> 9 time steps
            for s in range(10):
                total_l1_dist = 0
                total_l2_dist = 0
                for x in range(20, 100):
                    total_l1_dist += abs(data[i][0][x] - data[i][j][x-s])
                    total_l2_dist += (data[i][0][x] - data[i][j][x-s])**2
                if total_l1_dist < min_l1_dist:
                    min_l1_dist = total_l1_dist
                    l1_shift = s
                if total_l2_dist < min_l2_dist:
                    min_l2_dist = total_l2_dist
                    l2_shift = s
            print(l1_shift, min_l1_dist, end=" ")
            # if l1_shift != l2_shift:
            #     print(i, j, l1_shift, l2_shift)
            for x in range(99, l1_shift-1, -1):
                data[i][j][x] = data[i][j][x-l1_shift]
            for x in range(l1_shift):
                data[i][j][x] = 0
        print()
    return data
        

def main():
    # Gets only the EEG data for the first image:
    # shape = (4, 17, 100)
    #   dim 0 = Subject sees image 4 times
    #   dim 1 = Electrode 
    #   dim 2 = Time steps, 100 readings
    data = get_data()
    # Re-organize data matrix so the 17 electrodes are outermost dimension
    # Then iterating through data will generate 17 subplots
    data = np.transpose(data, [1,0,2])
    # plot_all_electrodes(data, "as_is.png")
    plot_all_electrodes(data)
    data = align_peaks(data)
    # plot_all_electrodes(data, "shifted.png")
    plot_all_electrodes(data)

if __name__ == "__main__":
    main()