# Importing Libraries
import numpy as np
from scipy.stats.kde import gaussian_kde
import matplotlib.pyplot as plt

def heatmapcells(path, DEBUG):
    
    string1 = 'COMPONENTS' # Key Strings
    string2 = 'FILL'
  
    file = open(path, "r") #Open Text File
  
    counter = 0 # Local Variables
    component = 0
    component_found = False

    X = [] # Ejes X y Y 
    Y = []

    for line in file: # Loop Line by Line
        if(component_found): # If Key Word 'COMPONENT' found
            if(string2 not in line): # If FILL Not in Line
                counter += 1 
                coordinates = line[line.find("(")+1:line.find(")")] # Take string in parenthesis 
                coordinates = coordinates.rstrip() # Delete whitespace
                coordinates = coordinates.lstrip()
                coordinates_int = list(coordinates.split(' ')) #Convert to a list of strings
                X.append(coordinates_int[0]) # Append X and Y values to each axis list
                Y.append(coordinates_int[1])   
                
        if string1 in line: # If 'COMPONENT' is on line
            component_found = True
            component += 1
            if (component == 2): # If we have seen 2 times 'COMPONENTS'
                break
            
    X.pop() # Deleting last component of the list, unuseful info
    Y.pop()
    
    if (DEBUG):
        print("Cantidad de coordenadas en X:")
        print(len(X))
        print("Cantidad de coordenadas en Y:")
        print(len(Y))
    
    for i in range(0, len(X)): # Converting both lists to int lists
        X[i] = int(X[i])    
    for j in range(0, len(Y)):
        Y[j] = int(Y[j])
          
    if(DEBUG):
        print('Se encontraron ', counter-1, ' celdas útiles.')
        
    file.close() # Close Text File

    # Plotting Heatmap
    size_x = len(X) # Important information(max, min, size)
    size_y = len(Y)
    max_x = max(X)
    min_x = min(X)
    max_y = max(Y)
    min_y = min(Y)
    # Using Gaussian kde
    k = gaussian_kde(np.vstack([X, Y])) 
    xi, yi = np.mgrid[min_x:max_x:size_x**0.5*1j,min_y:max_y:size_y**0.5*1j] # Setting the grid
    zi = k(np.vstack([xi.flatten(), yi.flatten()]))
    
    # Figure settings
    fig = plt.figure(figsize=(9, 10)) 
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    
    # Plot settings
    ax1.pcolormesh(xi, yi, zi.reshape(xi.shape), alpha=1) # Alpha Change Transparent Level
    ax2.contourf(xi, yi, zi.reshape(xi.shape), alpha=1)

    # Setting plot limits
    ax1.set_xlim(min_x, max_x)
    ax1.set_ylim(min_y, max_y)
    ax2.set_xlim(min_x, max_x)
    ax2.set_ylim(min_y, max_y)
    
    return 
    
path = "layout/systemcomplete.def"
heatmapcells(path, True)
