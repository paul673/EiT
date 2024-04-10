import matplotlib.pyplot as plt
import numpy as np
from .results import calculate_result
"""
• CO2 opptak/lagret for økende tetthet.
• CO2 opptak/lagret for økende harvest areal(?)
• CO2 opptak/lagret for varierende skjell størrelse feks. 10-100mm(?)
• CO2 opptak/lageret for prosentvis avvik av vekt/størrelse/høstingsperiode. Tornado chart

"""

colorpallete= ["#b30000", "#7c1158", "#4421af", "#1a53ff", "#0d88e6", "#00b7c7", "#5ad45a", "#8be04e", "#ebdc78"]

def generate_plot(variable_name,pmfrac,legenddict, **kwargs):
    mussel_mass_density = kwargs["mussel_mass_density"]
    mussel_farm_area = kwargs["mussel_farm_area"]
    time_period = kwargs["time_period"]
    molecule = kwargs["molecule"]
    mussel_harvest_size = kwargs["mussel_harvest_size"]
    shell_weight_fraction = kwargs["shell_weight_fraction"]

    kwargs[variable_name] = np.linspace(kwargs[variable_name]*pmfrac, kwargs[variable_name]*(1+pmfrac), 100)

    

    mass_mussel_per_year,stored,emitted,shellweight_per_year, netto = calculate_result(
        kwargs["mussel_mass_density"],
        kwargs["mussel_farm_area"],
        kwargs["time_period"],
        kwargs["molecule"],
        kwargs["mussel_harvest_size"],
        kwargs["shell_weight_fraction"]
        )

    plt.plot(kwargs[variable_name]*legenddict["unitscale"], netto, color=colorpallete[1])
    plt.xlabel(legenddict["xlabel"])
    plt.ylabel(legenddict["ylabel"])
    plt.title(legenddict["title"])
    plt.grid()
    plt.tight_layout()
    plt.savefig(f"mussel/figures/{variable_name}.pdf")
    plt.show()

def plot_tornado(frac, labels,**kwargs):
    originaldata =kwargs.copy()
    resultdict ={}
    for key, value in kwargs.items():
        if isinstance(value, int) or isinstance(value, float):
            variable_name = key
            datacopylst = [originaldata.copy() for i in range(3)]
            datacopylst[0][variable_name] = value * frac
            datacopylst[-1][variable_name] = value * (1+frac)
            results = []
            for datacopy in datacopylst:
                mass_mussel_per_year,stored,emitted,shellweight_per_year, netto = calculate_result(
                datacopy["mussel_mass_density"],
                datacopy["mussel_farm_area"],
                datacopy["time_period"],
                datacopy["molecule"],
                datacopy["mussel_harvest_size"],
                datacopy["shell_weight_fraction"]
                )
                results.append(netto)
            resultdict[key] = results
    center = list(resultdict.values())[0][1]
    upper = np.array([result[-1] for result  in resultdict.values()])-center
    lower = np.array([result[0] for result  in resultdict.values()])-center
    label = [labels[key] for key in resultdict.keys()]
    fig, ax = plt.subplots()
    ax.grid(zorder=0)
    width=0.5
    ax.barh(list(resultdict.keys()), upper, height=width, left=center, color=colorpallete[1], label=f"{(1+frac)*100}% ", zorder=3, tick_label=label)
    ax.barh(list(resultdict.keys()), lower, height=width, left=center, color=colorpallete[6],label=f"{(frac)*100}%", zorder=3, tick_label=label)
    plt.legend()
    plt.xlabel(r"CO$_2$ fanget $[ton]$")
    plt.tight_layout()
    plt.savefig("mussel/figures/tornado.pdf")
    plt.show()