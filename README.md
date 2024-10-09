# Cruise Ship Tourism
Master's Thesis in Big Data Analysis in Economics and Business

## Requirements

* python packages: requirements.txt
* system packages: proj 6.3.2-1. Cartopy py-package doesn't work with future versions.

## Order to generate data for the model and simulate the tourist flow <br>
1. getdatapalma.py
    * Download data from google sites.
    * Stored as palmapointsofinterest.csv
    
2. cleanpalmadata.ipynb
    * Clean data according to the model.
    * Stored as palmapointsofinterest_cleaned.csv
    
3. simulation.py
    * Add penalty function to each place.
    * Execute the simulation for a desired number of tourists and time, the aggregation function, and the one-step decision function.
        ```
        python simulation.py --ntourists <ntourists> --time <time> --aggregation_function <aggregation_function> --decision_method <decision_method> --noise_mean <noise_sigma> --af_weight <af_weight> --ct_agglomeration <ct_agglomeration>
        ```
      or
        ```
        python simulation.py -n <ntourists> -t <time> -a <aggregation_function> -d <decision_method> -s <noise_sigma> -w <af_weight> -i <niterations> -g <ct_agglomeration>
        ```
    Examples:
        ```
            python simulation.py -n 10 -t 3 -a product -d maximum -s 0.25 -w "[]" -i 2 -g 4
            python simulation.py -n 10 -t 3 -a minimum -d maximum -s 0.25 -w "[]" -i 2 -g 4
            python simulation.py -n 10 -t 3 -a harmonic_mean -d maximum -s 0.25 -w "[]" -i 2 -g 4
            python simulation.py -n 10 -t 3 -a owa -d maximum -s 0.25 -w "[0.5, 0.4, 0.1]" -i 2 -g 4
            python simulation.py -n 10 -t 3 -a weighted_minimum -d maximum -s 0.25 -w "[0.05, 0.01, 0.03]" -i 2 -g 4
            python simulation.py -n 10 -t 3 -a all_or_nothing -d maximum -s 0.25 -w "[]" -i 2 -g 4
            python simulation.py -n 10 -t 3 -a wmean_of_mean_minimum -d maximum -s 0.25 -w "[0.5]" -i 2 -g 42
            python simulation.py -n 10 -t 3 -a luk_weighted_mean -d maximum -s 0.25 -w "[0.2,0.4,0.6]" -i 2 -g 4
            python simulation.py -n 10 -t 3 -a weighted_mean -d maximum -s 0.25 -w "[0.2,0.4,0.6]" -i 2 -g 4
            python simulation.py -n 10 -t 3 -a dombi_mean -d maximum -s 0.25 -w "[0.2,0.4,0.6]" -i 2 -g 4
        ```

    * Output.
        * Tourist routes: <br>
            stored as palma_poi_troutes_\<ntourists>_\<time>_\<aggregation_function>_\<decision_method>.csv
            
        * Data summary by place and time: <br>
            stored as palma_poi_summary_\<ntourists>_\<time>_\<aggregation_function>_\<decision_method>.csv
            
4. simulation_plots <br>
   * Make the tourist flow plots
        - get_tourist_route: select a tourist by nubmer and plot his route.
        - get_time_plots: for each time, plot the number of tourists by location.
        - get_time_plots_gif: merge time plots in a gif.
        
   * Execute get_time_plots and get_time_plots_gif.
     ```
     python simulation_plots.py --ntourists <ntourists> --time <time> --aggregation_function <aggregation_function> --decision_method <decision_method>
     ```
     or
     ```
     python simulation_plots.py -n <ntourists> -t <time> -a <aggregation_function> -d <decision_method>
     ```

5. simulation_results <br>
    * Make a heatmap for the desired simulation summary CSV. 

    * Execute simulation_results.py
     ```
     python simulation_results.py --ntourists <ntourists> --time <time> --aggregation_function <aggregation_function> --decision_method <decision_method>
     ```
     or
     ```
     python imulation_results.py -n <ntourists> -t <time> -a <aggregation_function> -d <decision_method>
     ```