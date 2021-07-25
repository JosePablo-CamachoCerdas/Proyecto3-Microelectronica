# import numpy as np
# from scipy.stats.kde import gaussian_kde
# import matplotlib.pyplot as plt
 
# Importing Libraries
import re

def heatmapmetal(path, DEBUG):
    
    string1 = 'NETS' # Key Strings
    string2 = 'metal4'
    xmax = 'DIEAREA'
  
    file = open(path, "r") #Open Text File

    counter = 0 # Local Variables
    component = 0
    component_found = False

    X1 = [] # Ejes X1, X2 y Y
    X2 = [] 
    Y = []

    for line in file: # Loop Line by Line

        if(xmax in line): # If Key Word 'DIEAREA' found 
            dimensions = re.findall(r'\(([^()]+)\)', line)
            dimensions[1] = dimensions[1].rstrip() # Delete whitespace of second parenthesis
            dimensions[1] = dimensions[1].lstrip()
            max_long_x = list(dimensions[1].split(' ')) #Convert to a list of strings
            max_long_x = int(max_long_x[0]) # max_long_x is the limit of X axis

        if(component_found): # If Key Word 'NETS' found
            if(string2 in line): # If METAL4 in Line
                counter += 1 # Counter of metal 4
                coordinates = re.findall(r'\(([^()]+)\)', line) # Look for expressions between ( * )

                # Logic for first (), this parenthesis have x1 and y info
                coordinates[0] = coordinates[0].rstrip() # Delete whitespace
                coordinates[0] = coordinates[0].lstrip()
                first_coordinates_int = list(coordinates[0].split(' ')) #Convert to a list of strings
                X1.append(first_coordinates_int[0]) # Append X1 and Y values to each axis list
                Y.append(first_coordinates_int[1])
        
                # Logic for second (), this parenthesis have x2 info
                coordinates[1] = coordinates[1].rstrip() # Delete whitespace
                coordinates[1] = coordinates[1].lstrip()
                second_coordinates_int = list(coordinates[1].split(' ')) #Convert to a list of strings
                if(second_coordinates_int[0] == '*'): # If * is on the first coordinate, put max_long_x
                    X2.append(max_long_x)
                else: #If not, append on X2 the respective coordinate
                    X2.append(int(second_coordinates_int[0]))

        if string1 in line: # If 'NETS' is on line
            component_found = True
            component += 1
            if (component == 2): # If we have seen 2 times 'NETS'
                break
    
    if (DEBUG): # Showing info of coordinates
        print("Cantidad de coordenadas en X1:")
        print(len(X1))

        print("Cantidad de coordenadas en X2:")
        print(len(X2))

        print("Cantidad de coordenadas en Y:")
        print(len(Y))
    
    for i in range(0, len(X1)): # Converting both lists to int lists (X1 and Y)
        X1[i] = int(X1[i])    
    for j in range(0, len(Y)):
        Y[j] = int(Y[j])
    
    # # Number of used TRACKS out of 800 
    # k = [(x, Y.count(x)) for x in set(Y)]
    # print(len(k))

    if(DEBUG):
        print('Se encontraron ', counter, ' metales número 4.')
        
    file.close() # Close Text File

    # # Plotting Heatmap
    # size_x = len(X) # Important information(max, min, size)
    # size_y = len(Y)
    # max_x = max(X)
    # min_x = min(X)
    # max_y = max(Y)
    # min_y = min(Y)
    # # Using Gaussian kde
    # k = gaussian_kde(np.vstack([X, Y])) 
    # xi, yi = np.mgrid[min_x:max_x:size_x**0.5*1j,min_y:max_y:size_y**0.5*1j] # Setting the grid
    # zi = k(np.vstack([xi.flatten(), yi.flatten()]))
    
    # # Figure settings
    # fig = plt.figure(figsize=(9, 10)) 
    # ax1 = fig.add_subplot(211)
    # ax2 = fig.add_subplot(212)
    
    # # Plot settings
    # ax1.pcolormesh(xi, yi, zi.reshape(xi.shape), alpha=1) # Alpha Change Transparent Level
    # ax2.contourf(xi, yi, zi.reshape(xi.shape), alpha=1)

    # # Setting plot limits
    # ax1.set_xlim(min_x, max_x)
    # ax1.set_ylim(min_y, max_y)
    # ax2.set_xlim(min_x, max_x)
    # ax2.set_ylim(min_y, max_y)
    
    return 
    
path = "layout/systemcomplete.def"
heatmapmetal(path, True)