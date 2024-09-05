import matplotlib.pyplot as plt
import numpy as np 


def plot_centroid_path(centroid_path,time):
    if not centroid_path:
        print("No centroid path to plot.")
        return

    # Extract x and y coordinates
    x = np.array([coord[0] for coord in centroid_path])
    y = np.array([coord[1] for coord in centroid_path])
    
    r = np.sqrt(x**2 + y**2)
    t = np.array(time)
    

    # Plotting the path
    plt.figure()
    plt.scatter(t, r, marker='o', linestyle='-', color='b')
    plt.title('Centroid Path Over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Radial distance from Origin (px)')
    plt.grid(True)
    plt.show()