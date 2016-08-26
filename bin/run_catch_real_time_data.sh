#!/bin/bash

while : 
do
    python get_stock_real_time_data.py 600276 &
    python get_stock_real_time_data.py 600714 &
    sleep 3
done
