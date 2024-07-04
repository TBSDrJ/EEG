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
    data = data['preprocessed_eeg_data']
    # Just restrict to the first image for now.
    data = data[0]
    return data

def plot_all_electrodes(data: np.ndarray) -> None:
    """Draws 1 subplot for each electrode in one graph."""
    t = np.arange(100)
    fig, axs = plt.subplots(3,6,)
    for ax, elec_data in zip(axs.flat[:17], data):
        ax.plot(
            t, elec_data[0], 'b-',
            t, elec_data[1], 'r-',
            t, elec_data[2], 'g-',
            t, elec_data[3], 'k-',
        )
    plt.show()

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
    plot_all_electrodes(data)

if __name__ == "__main__":
    main()