from data.data import get_periodic_table
from utilities.utilities import get_mmass,get_co2_content,co2_per_mass
from mussel.mussel import mussel_main
from mussel.weight import plotSizeWeightPlot,get_dry_per_wet_factor
from mussel.respiration import plot_groth_increment_with_interpolation, respirationrate_per_shell



def main():

    return


if __name__ == "__main__":
    #print(co2_per_mass(100, 'C6H10O5O2'))
    mussel_main()
    #print(get_dry_per_wet_factor())
    #plotSizeWeightPlot()