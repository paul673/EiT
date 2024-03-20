import matplotlib.pyplot as plt
import numpy as np
from .weight import colorpallete, flesh_weight_derivative,flesh_weight, get_dry_per_wet_factor, shell_weight
from scipy.integrate import quad
from utilities.utilities import get_mmass

def respiration_rate_per_g(wet_tissue_weight):
    """
    Calculates the respiration rate in mol year^-1 g_wet_tissue^-1
    """
    return (3.88*wet_tissue_weight**(-0.248))*10**(-6)*365*24

def respiration_rate(wet_tissue_weight):
    """
    Calculates the respiration rate in mol year^-1 
    """
    return respiration_rate_per_g(wet_tissue_weight)*wet_tissue_weight

def groth_increment(age):
    """
    Calculated the relative weight increment g_wet/g_wet
    """
    return 64.6*age**(-3.44)

def interpolate_groth_increment(age, age_range=[2,3]):
    x = np.linspace(age_range[0], age_range[1],100)
    y = groth_increment(x)
    a, b = np.polyfit(x,y,deg=1)
    return a*age+b

def growth_approximation_slope(adult_size=60, adult_age=16/12):
    """
    Assume linear growth. Size 0mm in at time 0. 
    adult_size: Størrelse i mm when harvestet
    adult_age: Shell age when harvestet (year)
    return growth rate in mm/year 
    """
    return (adult_size/adult_age)

def growth_approximation(age, adult_size=60, adult_age=16/12):
    return age* growth_approximation_slope(adult_size=adult_size, adult_age=adult_age)


def respiration_rate_from_age(age):
    """
    Return respiration rate per year of a mussel of a certain age
    """
    return respiration_rate(flesh_weight(mussel_size=growth_approximation(age))/ get_dry_per_wet_factor())

def respirationrate_per_shell(adult_age=16/12):
    sol = quad(respiration_rate_from_age, 0, adult_age)
    #print("Integration solution: ", sol)
    return sol[0]

def plot_groth_increment_with_interpolation(age_range=[0, 2]):
    x = np.linspace(age_range[0],age_range[1],100)
    plt.plot(x, growth_approximation(x),label="Relative weight increment", color=colorpallete[1])
    plt.xlabel(r"Age [y]")
    plt.ylabel(r"Length increment [mm]")
    plt.grid()
    plt.show()
    return None


def plot_respiration_rate(wet_tissue_weight_range=[0, 10]):
    x = np.linspace(wet_tissue_weight_range[0],wet_tissue_weight_range[1],100)
    plt.plot(x, respiration_rate(x))
    plt.xlabel(r"Wet tissue weight [g]")
    plt.ylabel(r"Respiration rate $\left(\frac{mol}{y}\right)$")
    plt.grid()
    plt.show()
    return None

def respiration(time_period, shellweight_per_year,mussel_size):
    
    respiration_per_mussel=respirationrate_per_shell(adult_age=time_period) #molCO2/mussel
    respiration_per_mussel = respiration_per_mussel*get_mmass('CO2') #gCO2/mussel
    total_shellweight = time_period*shellweight_per_year
    shellweight_per_mussel = shell_weight(mussel_size)
    mussels=total_shellweight/shellweight_per_mussel

    # CO2 O2 ratio 1:1
    return (respiration_per_mussel*mussels/1000)/1000 #tonCO2
    # Times antall mussel 
    # Antall mussel = shellvekt/shellvekt per mussel 


if __name__ == "__main__":
    #print(co2_per_mass(100, 'C6H10O5O2'))
    #plot_groth_increment_with_interpolation()
    #plot_respiration_rate()
    plot_groth_increment_with_interpolation()
