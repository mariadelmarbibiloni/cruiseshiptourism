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

    data = results.T
    data = data.drop(0, 1)

    ax = plt.subplots(figsize=(30, 20))
    plt.title(f'Aggregation function: {af}\n'
            + f'Decision methon:      {dm} \n', fontsize=20)
    sns.heatmap(data, cmap="viridis")

    plt.savefig(f'palmadata/summary_plots/summary_heat_map_{ntourists}_{time}_{af}_{dm}.png', dpi=199)
