# Cruise Ship Tourism
Master's Thesis in Big Data Analysis in Economics and Business

## Order to generate data for the model <br>
1. getdatapalma.py
    * Download data from google sites.
    * Stored as palmapointsofinterest.csv
2. cleanpalmadata.ipynb
    * Clean data according to the model.
    * Stored as palmapointsofinterest_cleaned.csv
3. addpenalty.py
    * Add penalty function to each place.
    * Stored as palmapointsofinterest_cln_pnl.csv

4. simulation.py
    * Execute the simulation for a desired number of tourists and time.
        ```
        python simulation.py --ntourists <ntourists> --time <time>
        ```
      or
        ```
        python simulation.py -n <ntourists> -t <time>
        ```
    * Output.
        * Tourist routes: <br>
            stored as palma_poi_troutes_\<ntourists>_\<time>.csv
            
        * Data summary by place and time: <br>
            stored as palma_poi_summary_\<ntourists>_\<time>.csv
            
5. simulation_plots <br>
   * Import function plots
        - get_tourist_route: select a tourist by nubmer and plot his route.
        - get_time_plots: for each time, plot the number of tourists by location.
        - get_time_plots_gif: merge time plots in a gif.
        
   * Execute get_time_plots and get_time_plots_gif.
     ```
     python simulation_plots.py --ntourists <ntourists> --time <time>
     ```
     or
     ```
     python simulation_plots.py -n <ntourists> -t <time>
     ```
