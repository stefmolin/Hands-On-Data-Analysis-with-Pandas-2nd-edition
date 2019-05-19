#!/usr/bin/env bash

LOGS="logs"

# make a directory for our logs
if ! [ -d  "$LOGS" ]; then
    mkdir "$LOGS"
fi

# run the simulations
echo 'Simulating January 2018...'
python simulate.py -s 1 --stealthy -l "$LOGS"/jan_2018.csv -hl "$LOGS"/hackers_jan_2018.csv 31 "2018-01-01" 0.01 0.5

printf '\nSimulating February 2018...\n'
python simulate.py -s 2 --stealthy -l "$LOGS"/feb_2018.csv -hl "$LOGS"/hackers_feb_2018.csv 28 "2018-02-01" 0.005 0.25

printf '\nSimulating March 2018...\n'
python simulate.py -s 3 --stealthy -l "$LOGS"/mar_2018.csv -hl "$LOGS"/hackers_mar_2018.csv 31 "2018-03-01" 0.001 0.10

printf '\nSimulating April 2018...\n'
python simulate.py -s 4 --stealthy -l "$LOGS"/apr_2018.csv -hl "$LOGS"/hackers_apr_2018.csv 30 "2018-04-01" 0.01 0.65

printf '\nSimulating May 2018...\n'
python simulate.py -s 5 --stealthy -l "$LOGS"/may_2018.csv -hl "$LOGS"/hackers_may_2018.csv 31 "2018-05-01" 0.0001 0.05

printf '\nSimulating June 2018...\n'
python simulate.py -s 6 --stealthy -l "$LOGS"/jun_2018.csv -hl "$LOGS"/hackers_jun_2018.csv 30 "2018-06-01" 0.0005 0.05

printf '\nSimulating July 2018...\n'
python simulate.py -s 7 --stealthy -l "$LOGS"/jul_2018.csv -hl "$LOGS"/hackers_jul_2018.csv 31 "2018-07-01" 0.01 0.15

printf '\nSimulating August 2018...\n'
python simulate.py -s 8 --stealthy -l "$LOGS"/aug_2018.csv -hl "$LOGS"/hackers_aug_2018.csv 31 "2018-08-01" 0.005 0.1

printf '\nSimulating September 2018...\n'
python simulate.py -s 9 -l "$LOGS"/sep_2018.csv -hl "$LOGS"/hackers_sep_2018.csv 30 "2018-09-01" 0.005 0.1

printf '\nSimulating October 2018...\n'
python simulate.py -s 10 -l "$LOGS"/oct_2018.csv -hl "$LOGS"/hackers_oct_2018.csv 31 "2018-10-01" 0.002 0.12

printf '\nSimulating November 2018...\n'
python simulate.py -s 11 --stealthy -l "$LOGS"/nov_2018.csv -hl "$LOGS"/hackers_nov_2018.csv 30 "2018-11-01" 0.007 0.17

printf '\nSimulating December 2018...\n'
python simulate.py -s 12 --stealthy -l "$LOGS"/dec_2018.csv -hl "$LOGS"/hackers_dec_2018.csv 31 "2018-12-01" 0.08 0.88

printf '\nSimulating January 2019...\n'
python simulate.py -s 13 --stealthy -l "$LOGS"/jan_2019.csv -hl "$LOGS"/hackers_jan_2019.csv 31 "2019-01-01" 0.008 0.08

printf '\nSimulating February 2019...\n'
python simulate.py -s 14 --stealthy -l "$LOGS"/feb_2019.csv -hl "$LOGS"/hackers_feb_2019.csv 28 "2019-02-01" 0.01 0.18

printf '\nSimulating March 2019...\n'
python simulate.py -s 15 --stealthy -l "$LOGS"/mar_2019.csv -hl "$LOGS"/hackers_mar_2019.csv 31 "2019-03-01" 0.01 0.18

# combine the files
echo 'Merging files...'
python merge_logs.py

# remove unnecessary files
echo 'Cleaning up...'
cd "$LOGS"
echo "$(ls)" | grep -E "(^[a-z]{3}_{1})|(hackers_[a-z]{3})" | xargs rm
cd ..

echo 'Success!'
