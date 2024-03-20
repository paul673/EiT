import matplotlib.pyplot as plt
import numpy as np
from utilities.utilities import co2_per_mass

colorpallete= ["#b30000", "#7c1158", "#4421af", "#1a53ff", "#0d88e6", "#00b7c7", "#5ad45a", "#8be04e", "#ebdc78"]

def shell_weight(mussel_size):
    return np.exp(-10.1 + 3.13 * np.log(mussel_size))

def flesh_weight(mussel_size):
    return np.exp(-11.6 + 2.7 * np.log(mussel_size))

def flesh_weight_derivative(mussel_size):
    return np.exp(-11.6)*2.7*mussel_size**(1.7)

def get_dry_per_wet_factor():
    """
    Shell sizes from "Growth, metabolism and lipid peroxidation in Mytilus edulis: age and size effects"
    Small:
        wet tissue weight = 0.23 g
        length 20-25 mm
    Medium:
        wet tissue weight = 0.52 g, 
        length 30-35 mm
    Large:
        wet tissue weight = 1.05 g
        length 40-50 mm

    Use medium as reference
    """
    size = (35+30)/2 #mm
    wet_weight = 0.52 # g
    dry_weight = flesh_weight(size)
    ratio = dry_weight/wet_weight
    return ratio

def plotSizeWeightPlot():
    mussel_size = np.linspace(0,41,100)
    colors= colorpallete

    


    #############################

    fig, ax1 = plt.subplots()

    ax1.set_xlabel(r"Skjell lengde [mm]")
    ax1.set_ylabel("Skjell vekt [g]")
    plot1 = ax1.plot(mussel_size,shell_weight(mussel_size),label="Skjell vekt",color=colors[1] )
    ax1.tick_params(axis='y')
    ax1.set_ylim(top=5, bottom=-0.25)
    ax1.grid()
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    
    ax2.set_ylabel('Tørket kjøtt vekt [g]')  # we already handled the x-label with ax1
    plot2 = ax2.plot(mussel_size,flesh_weight(mussel_size),label="Tørket kjøtt vekt",color=colors[2])
    ax2.tick_params(axis='y')
    ax2.grid()
    ax2.set_ylim(top=0.5, bottom=-0.025)
    lns = plot1+plot2
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc=0)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.grid()
    
    plt.show()
    ###########################
    """
    #print(mussel_size)
    plt.plot(mussel_size,shell_weight(mussel_size), label="shell weight")
    plt.plot(mussel_size,flesh_weight(mussel_size), label="flesh weight")
    plt.xlabel("shell size [mm]")
    plt.ylabel("weight [g]")
    plt.legend()
    plt.grid()
    plt.show()
    """

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
    #print(mussel_size)
    pixel_sum = pixel_values.sum()
    pixel_percent = pixel_values/pixel_sum
    return pixel_values,mussel_size,pixel_percent, small_shell_frac

def plotMusselHistogram(slice=0):
    pixel_values,mussel_size,pixel_percent, small_shell_frac = generateSizeDistibutiondata(slice)
    
    plt.grid(zorder=0)
    plt.bar(mussel_size,pixel_percent*100, zorder=3, color=colorpallete[1])
    plt.xticks(np.arange(mussel_size[0], mussel_size[-1]+2, step=2))
    plt.ylabel("Populasjonsfraksjon [%]")
    plt.xlabel("Lengde [mm]")
    plt.show()

def get_mean_weight(weight_function,mussel_harvest_size, slice=0):
    pixel_values,mussel_size,pixel_percent, small_shell_frac = generateSizeDistibutiondata(slice)
    #return sum(weight_function(mussel_size)*pixel_percent)
    return weight_function(mussel_harvest_size)

def weightOutput(mussel_harvest_size, slice=0):
    pixel_values,mussel_size,pixel_percent, small_shell_frac = generateSizeDistibutiondata(slice)
    mean_shell_weight=get_mean_weight(shell_weight,mussel_harvest_size, slice)
    mean_flesh_weight=get_mean_weight(flesh_weight,mussel_harvest_size, slice)
    mean_total_weight = mean_flesh_weight+mean_shell_weight
    mean_shell_frac = mean_shell_weight/(mean_shell_weight+mean_flesh_weight)
    return mean_shell_weight, mean_flesh_weight, mean_total_weight,mean_shell_frac,small_shell_frac
     
def printWeightOutput(mussel_harvest_size,slice=0):
    mean_shell_weight, mean_flesh_weight, mean_total_weight,mean_shell_frac, small_shell_frac = weightOutput(mussel_harvest_size,slice)
    print("Dry shell weight: ",mean_shell_weight)
    print("Dry flesh weight: ",mean_flesh_weight)
    print("Total dry weight: ",mean_total_weight)
    print("Dry shell fraction: ", mean_shell_frac)
    return mean_shell_weight, mean_flesh_weight, mean_total_weight,mean_shell_frac, small_shell_frac

#plotSizeWeightPlot()
#plotMusselHistogram()
#plotMusselHistogram(slice=10)

def co2_per_area(min, max,mussel_mass_density,shell_weight_fraction, molecule,time_period):
    mussel_farm_area_array = np.linspace(min,max,500)
    shellweight_array_per_year = mussel_mass_density*mussel_farm_area_array*shell_weight_fraction/time_period
    co2_array = co2_per_mass(shellweight_array_per_year, molecule)*10**(-6)
    plt.plot(mussel_farm_area_array*10**(-6), co2_array,color=colorpallete[1], label=r"CO$_2$ per $year$")
    plt.xlabel(r"Area [$km^2$]")
    plt.ylabel(r"CO$_2$ [ton]")
    plt.grid()
    plt.legend()
    plt.show()
    return

def calcculate_whole_mussel_weight_fracs(mean_shell_frac):

    size =60 #mm

    dry_weight = flesh_weight(size)
    dry_shell_weight = shell_weight(size)
    wet_weight = dry_weight/get_dry_per_wet_factor()
    wet_shell_weight=dry_shell_weight
    total_mussel_weight = wet_shell_weight/mean_shell_frac
    mean_wet_flesh_frac = wet_weight/total_mussel_weight
    mean_water_frac = 1- mean_shell_frac- mean_wet_flesh_frac
    """print("shellfrac: ", mean_shell_frac)
    print("waterfrac: ", mean_water_frac)
    print("Wet flesh frac:",  mean_wet_flesh_frac)
    print("60 mm shell total weight: ", total_mussel_weight)"""
    return mean_shell_frac, mean_water_frac,mean_wet_flesh_frac
    
    

    

def calculate_mussel_density(mean_shell_frac):
    mean_shell_frac, mean_water_frac,mean_wet_flesh_frac=calcculate_whole_mussel_weight_fracs(mean_shell_frac)
    areal = 750*10000 #m^2
    farm_area=3.5*1000 #m^2
    weight_produced = 350*1000*1000/mean_wet_flesh_frac # g
    area_density = weight_produced/areal
    return area_density




