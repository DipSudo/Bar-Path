import matplotlib.pyplot as plt
import numpy as np 


def plot_centroid_path(centroid_path,time):
    if not centroid_path:
        print("No centroid path to plot.")
        return

    # Extract x and y coordinates
    x = [coord[0] for coord in centroid_path]
    y = [coord[1] for coord in centroid_path]
    
    r = np.sqrt(x**2 + y**2)
    t = np.array(time)
    

    # Plotting the path
    plt.figure()
    plt.plot(t, r, marker='o', linestyle='-', color='b')
    plt.title('Centroid Path Over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Distance from Origin (r)')
    plt.grid(True)
    plt.show()