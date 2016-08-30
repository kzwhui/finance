#!/bin/bash

while : 
do
    python get_stock_real_time_data.py 600276,600714,600297,600105,000002 &
    sleep 3
done
