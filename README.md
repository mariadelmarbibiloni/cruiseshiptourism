# cruiseshiptourism
Master's Thesis in Big Data Analysis in Economics and Business

## Order to generate data for the model. <br>
1. getdatapalma.py
    * Download data from google sites.
    * Stored as palmapointsofinterest.csv
2. cleanpalmadata.ipynb
    * Clean data according to the model.
    * Stored as palmapointsofinterest_cleaned.csv
3. addpenalitation.ipynb
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