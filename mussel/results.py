from .respiration import respiration
from .weight import co2_per_mass

def calculate_result(mussel_mass_density,mussel_farm_area,time_period,molecule,mussel_harvest_size,shell_weight_fraction):

    mass_mussel_per_year=mussel_mass_density*mussel_farm_area/(1000*1000)/time_period
    shellweight_per_year = mussel_mass_density*mussel_farm_area*shell_weight_fraction/time_period
    stored = co2_per_mass(shellweight_per_year, molecule)*10**(-6)
    
    emitted = respiration(time_period, shellweight_per_year,mussel_harvest_size)
    netto = stored-emitted
    return mass_mussel_per_year,stored,emitted,shellweight_per_year, netto