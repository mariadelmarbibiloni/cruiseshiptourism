import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys_arguments as sa

if __name__ == "__main__":
    ntourists, time, af, dm = sa.get_sysarg()
    if not (ntourists or time or af or dm):
        message = """
        You must introduce all the parameters:
            simulation.py -n <ntourists> -t <time> -a <aggregation_function> -d <decision_method>
        """
        raise Exception(message)

    results = pd.read_csv(
                f"palmadata/palma_poi_summary_{ntourists}_{time}_{af}_{dm}.csv",
                header=0,
            )

    # ncols = len(results.columns) # Uncomment if the user does not want task labels
    # results.columns = range(0, ncols)
    results.columns = ['cruise ship', 'Catedral de Mallorca',
       'Castell de Bellver', 'La Almudaina', 'Tren Soller',
       "Es Baluard", 'Plaza Mayor',
       'Poble Espanyol', 'Lonja de Mallorca', 'Born de Palma',
       'Port of Palma', 'Arab Baths',
       'Mercat de l’Olivar', 'Sant @en.francesc',
       'Museu F. Juan March', 'Parc de la Mar', 'Plaça de Cort',
       'Mercado Gastr. S.Juan', 'Hort del Rei',
       'Església de St. Eulàlia', 'Can Pere Antoni', 'Casal Solleric',
       'Museo de Mallorca', 'Ayuntamiento de Palma',
       'Plaça de toros', 'Gran Hotel', 'Convent de Santa Clara',
       'Rambla', 'Plaza España', 'Museu Diocesà',
       'Basilica of St. Michael', 'Sa Feixina Park',
       'F. Bartolomé March', 'Avenida Jaime III', 'Mercat Pere Garau',
       'Can Forteza Rey', 'Gerhardt Braun Gallery', 'CaixaForum Palma',
       'Consolat de Mar', 'Passeig Mallorca', 'Parque Sa Riera',
       'C.C. Can Balaguer', 'Balearic Transfer',
       'Escape Room Mallorca', 'Plaza Del Mercat',
       'Parc de les Estacions', 'Device to Root out Evil',
       'Roman Catholic Diocese', 'Estàtua "Es Foner"', 'Can Vivot',
       'Plaça Rei Joan Carles I', 'tapas-tour',
       "GOB",
       "Ca'n Oms", 'La Misericòrdia', 'ABA ART LAB']
    
    data = results.T
    data = data.drop(0, 1)

    ax = plt.subplots(figsize=(35, 40))
    plt.title(f'Aggregation function: {af}\n'
            + f'Decision methon:      {dm} \n',
            fontsize=40,
            weight='bold')

    sns.set(font_scale=3)
    res = sns.heatmap(data, cmap="viridis")
   
    res.set_xticklabels(res.get_xmajorticklabels(), fontsize = 30)
    res.set_yticklabels(res.get_ymajorticklabels(), fontsize = 22) 

    plt.savefig(f'palmadata/summary_plots/summary_heat_map_{ntourists}_{time}_{af}_{dm}.png', dpi=199)
