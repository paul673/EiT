from utilities.utilities import get_mmass, get_co2_content, co2_per_mass
from .weight import weightOutput, co2_per_area, calculate_mussel_density,calcculate_whole_mussel_weight_fracs
from .respiration import respiration

def print_init_overview(molecule, mussel_farm_area, mussel_density, mussel_mass_density,mussel_mean_weight,shell_weight_fraction, print_width,mussel_harvest_size,time_period):
    print(f"Initial values: ")
    print(f"{'Molecule':<30}{molecule:>20}")
    print(f"{'Mussel farm Area [m^2]':<30}{mussel_farm_area:>20}")
    print(f"{'Mussel havest size [mm]':<30}{mussel_harvest_size:>20}")
    #print(f"{'Mussel density [mussel/m^2]':<30}{mussel_density:>20}")
    print(f"{'Mussel density [g/m^2]':<30}{mussel_mass_density:>20}")
    print(f"{'Time period [years]':<30}{time_period:>20}")
    #print(f"{'Mussel mean weight [g]':<30}{mussel_mean_weight:>20}")
    print(f"{'Mussel shell fraction':<30}{shell_weight_fraction:>20}")
    print()
    print(f"#"*print_width)
    print()

def mussel_main():
    mussel_harvest_size=60 #mm
    time_period=16/12 #years
    #mean_shell_weight, mean_flesh_weight, mean_total_weight,mean_shell_frac, small_shell_frac = weightOutput(mussel_harvest_size,slice=10)
    mean_shell_frac = 0.365
    #print(small_shell_frac)
    molecule = 'CaCO3'
    mussel_density = 1000 # in correct size per year#10000*(1-small_shell_frac) # mussel/m^2 Mussels lagre enough to get harvested
    mussel_mass_density = calculate_mussel_density(mean_shell_frac)#709.6209325961993#234.375#3_000_000/(7.5*5) #g/ m^2
    shell_weight_fraction = mean_shell_frac # g_shell/g_mussel (1 - 150/500)
    mussel_farm_area = 4000e+6#44000 # m^2
    mussel_mean_weight = None#mean_total_weight # g

    print_width = 50
    print(f"#"*print_width)
    print(f"{'Mussel calculator':^50}")
    print(f"#"*print_width)
    print()
    print_init_overview(molecule, mussel_farm_area, mussel_density, mussel_mass_density,mussel_mean_weight,shell_weight_fraction, print_width,mussel_harvest_size, time_period)

    customize = input("Customize variables (y/N): ")
    if customize == "y":
        molecule = str(input(f"{'Molecule: '}").strip() or molecule)
        mussel_farm_area = float(input(f"{'Mussel farm Area [m^2]: '}").strip() or mussel_farm_area)
        #mussel_density = float(input(f"{'Mussel density [mussel/m^2]: '}").strip() or mussel_density)
        mussel_mass_density = float(input(f"{'Mussel density [g/m^2]: '}").strip() or mussel_mass_density)
        #mussel_mean_weight = float(input(f"{'Mussel mean weight [g]: '}").strip() or mussel_mean_weight)
        #shell_weight_fraction = float(input(f"{'Mussel shell fraction: '}").strip() or shell_weight_fraction)
        mussel_harvest_size = float(input(f"{'Mussel harvest size [mm]: '}").strip() or mussel_harvest_size)
        time_period = float(input(f"{'Mussel harvest size [mm]: '}").strip() or time_period)
        #mean_shell_weight, mean_flesh_weight, mean_total_weight,mean_shell_frac, small_shell_frac = weightOutput(mussel_harvest_size,slice=10)
        shell_weight_fraction = mean_shell_frac
        print()
        print(f"#"*print_width)
        print()
        print_init_overview(molecule, mussel_farm_area, mussel_density, mussel_mass_density,mussel_mean_weight,shell_weight_fraction, print_width)


    print(f"#"*print_width)
    print()
    print("Result:")
    print("mass shell: ", mussel_mass_density*mussel_farm_area/(1000*1000))
    shellweight_per_year = mussel_mass_density*mussel_farm_area*shell_weight_fraction/time_period
    stored = co2_per_mass(shellweight_per_year, molecule)*10**(-6)
    print(f"{'CO2 stored [ton]':<30}{stored:>20_}")
    
    emitted = respiration(time_period, shellweight_per_year,mussel_harvest_size)
    print(f"{'CO2 emitted [ton]':<30}{emitted:>20_}")
    print(f"{'Netto CO2 stored [ton]':<30}{stored-emitted:>20_}")

    co2_per_area(1000, 400000,mussel_mass_density,shell_weight_fraction, molecule, time_period)


#NB! USE RESPIRATION SIZE DEPENDENT file:///C:/Users/paulj/Downloads/Growth_metabolism_and_lipid_peroxidation_in_Mytilu.pdf

