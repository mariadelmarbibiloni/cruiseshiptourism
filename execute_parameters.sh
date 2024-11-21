#!/bin/bash

# agg -> [utilitie, distance, agglomeration]

python simulation_results.py -n 6500 -t 20 -a product -d maximum -s 0.25 -w "[]" -i 1 -g 6500
python simulation_results.py -n 6500 -t 20 -a minimum -d maximum -s 0.25 -w "[]" -i 1 -g 6500
python simulation_results.py -n 6500 -t 20 -a harmonic_mean -d maximum -s 0.25 -w "[]" -i 1 -g 6500
python simulation_results.py -n 6500 -t 20 -a owa -d maximum -s 0.25 -w "[0.5, 0.3, 0.2]" -i 1 -g 6500
python simulation_results.py -n 6500 -t 20 -a owa -d maximum -s 0.25 -w "[0.2, 0.3, 0.5]" -i 1 -g 6500
python simulation_results.py -n 6500 -t 20 -a weighted_minimum -d maximum -s 0.25 -w "[0.5, 0.3, 0.2]" -i 1 -g 6500
python simulation_results.py -n 6500 -t 20 -a weighted_minimum -d maximum -s 0.25 -w "[0.2, 0.3, 0.5]" -i 1 -g 6500
python simulation_results.py -n 6500 -t 20 -a all_or_nothing -d maximum -s 0.25 -w "[]" -i 1 -g 6500
python simulation_results.py -n 6500 -t 20 -a wmean_of_mean_minimum -d maximum -s 0.25 -w "[0.5]" -i 1 -g 6500
python simulation_results.py -n 6500 -t 20 -a wmean_of_mean_minimum -d maximum -s 0.25 -w "[0.25]" -i 1 -g 6500
python simulation_results.py -n 6500 -t 20 -a wmean_of_mean_minimum -d maximum -s 0.25 -w "[0.75]" -i 1 -g 6500
python simulation_results.py -n 6500 -t 20 -a luk_weighted_mean -d maximum -s 0.25 -w "[0.5, 0.3, 0.2]" -i 1 -g 6500
python simulation_results.py -n 6500 -t 20 -a luk_weighted_mean -d maximum -s 0.25 -w "[0.2, 0.3, 0.5]" -i 1 -g 6500
python simulation_results.py -n 6500 -t 20 -a weighted_mean -d maximum -s 0.25 -w "[0.5, 0.3, 0.2]" -i 1 -g 6500
python simulation_results.py -n 6500 -t 20 -a weighted_mean -d maximum -s 0.25 -w "[0.2, 0.3, 0.5]" -i 1 -g 6500
python simulation_results.py -n 6500 -t 20 -a dombi_mean -d maximum -s 0.25 -w "[0.5, 0.3, 0.2]" -i 1 -g 6500
python simulation_results.py -n 6500 -t 20 -a dombi_mean -d maximum -s 0.25 -w "[0.2, 0.3, 0.5]" -i 1 -g 6500
