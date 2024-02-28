import matplotlib.pyplot as plt
import numpy as np

def shell_weight(mussel_size):
    return np.exp(-10.1 + 3.13 * np.log(mussel_size))

def flesh_weight(mussel_size):
    return np.exp(-11.6 + 2.7 * np.log(mussel_size))

def plotSizeWeightPlot():
    mussel_size = np.linspace(0,41,100)
    #print(mussel_size)
    plt.plot(mussel_size,shell_weight(mussel_size), label="shell weight (g)")
    plt.plot(mussel_size,10*flesh_weight(mussel_size), label="flesh weight (10*g)")
    plt.xlabel("shell size (mm)")
    plt.legend()
    plt.grid()
    plt.show()

def generateSizeDistibutiondata(slice=0):
    pixel_values = np.array([69,194,295,449,520,491,397,262,126,89,78,36,68,10,21,10,10,6,1,0])
    mussel_size = np.array([5+i*2 for i in range(len(pixel_values))])
    pixel_sum = pixel_values.sum()
    pixel_percent = pixel_values/pixel_sum

    # Frac small shells
    small_shell_frac = pixel_percent[:slice].sum()

    #Slice off small shells
    pixel_values = pixel_values[slice:]
    mussel_size =mussel_size[slice:]
    print(mussel_size)
    pixel_sum = pixel_values.sum()
    pixel_percent = pixel_values/pixel_sum
    return pixel_values,mussel_size,pixel_percent, small_shell_frac

def plotMusselHistogram(slice=0):
    pixel_values,mussel_size,pixel_percent, small_shell_frac = generateSizeDistibutiondata(slice)
    plt.bar(mussel_size,pixel_percent)
    plt.grid()
    plt.show()

def get_mean_weight(weight_function, slice=0):
    pixel_values,mussel_size,pixel_percent, small_shell_frac = generateSizeDistibutiondata(slice)
    return sum(weight_function(mussel_size)*pixel_percent)

def weightOutput(slice=0):
    pixel_values,mussel_size,pixel_percent, small_shell_frac = generateSizeDistibutiondata(slice)
    mean_shell_weight=get_mean_weight(shell_weight, slice)
    mean_flesh_weight=get_mean_weight(flesh_weight, slice)
    mean_total_weight = mean_flesh_weight+mean_shell_weight
    mean_shell_frac = mean_shell_weight/(mean_shell_weight+mean_flesh_weight)
    return mean_shell_weight, mean_flesh_weight, mean_total_weight,mean_shell_frac,small_shell_frac
     
def printWeightOutput(slice=0):
    mean_shell_weight, mean_flesh_weight, mean_total_weight,mean_shell_frac, small_shell_frac = weightOutput(slice)
    print("Dry shell weight: ",mean_shell_weight)
    print("Dry flesh weight: ",mean_flesh_weight)
    print("Total dry weight: ",mean_total_weight)
    print("Dry shell fraction: ", mean_shell_frac)
    return mean_shell_weight, mean_flesh_weight, mean_total_weight,mean_shell_frac, small_shell_frac

printWeightOutput(slice=10)