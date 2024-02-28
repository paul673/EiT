from utilities.utilities import get_mmass, get_co2_content, co2_per_mass
from .weight import weightOutput

def print_init_overview(molecule, mussel_farm_area, mussel_density,mussel_mean_weight,shell_weight_fraction, print_width):
    print(f"Initial values: ")
    print(f"{'Molecule':<30}{molecule:>20}")
    print(f"{'Mussel farm Area [m^2]':<30}{mussel_farm_area:>20}")
    print(f"{'Mussel density [mussel/m^2]':<30}{mussel_density:>20}")
    print(f"{'Mussel mean weight [g]':<30}{mussel_mean_weight:>20}")
    print(f"{'Mussel shell fraction':<30}{shell_weight_fraction:>20}")
    print()
    print(f"#"*print_width)
    print()

def mussel_main():
    mean_shell_weight, mean_flesh_weight, mean_total_weight,mean_shell_frac, small_shell_frac = weightOutput(slice=10)
    print(small_shell_frac)
    molecule = 'CaCO3'
    mussel_density = 1000 # in correct size per year#10000*(1-small_shell_frac) # mussel/m^2 Mussels lagre enough to get harvested
    shell_weight_fraction = mean_shell_frac # g_shell/g_mussel (1 - 150/500)
    mussel_farm_area = 4000e+6#44000 # m^2
    mussel_mean_weight = mean_total_weight # g

    print_width = 50
    print(f"#"*print_width)
    print(f"{'Mussel calculator':^50}")
    print(f"#"*print_width)
    print()
    print_init_overview(molecule, mussel_farm_area, mussel_density,mussel_mean_weight,shell_weight_fraction, print_width)

    customize = input("Customize variables (y/N): ")
    if customize == "y":
        molecule = str(input(f"{'Molecule: '}").strip() or molecule)
        mussel_farm_area = float(input(f"{'Mussel farm Area [m^2]: '}").strip() or mussel_farm_area)
        mussel_density = float(input(f"{'Mussel density [mussel/m^2]: '}").strip() or mussel_density)
        mussel_mean_weight = float(input(f"{'Mussel mean weight [g]: '}").strip() or mussel_mean_weight)
        shell_weight_fraction = float(input(f"{'Mussel shell fraction: '}").strip() or shell_weight_fraction)
        print()
        print(f"#"*print_width)
        print()
        print_init_overview(molecule, mussel_farm_area, mussel_density,mussel_mean_weight,shell_weight_fraction, print_width)


    print(f"#"*print_width)
    print()
    print("Result:")
    
    shellweight = mussel_density*mussel_farm_area*mussel_mean_weight*shell_weight_fraction
    print(f"{'CO2 stored [ton]':<30}{co2_per_mass(shellweight, molecule)*10**(-6):>20}")
    print()
