#!/usr/bin/env bash

# Notify me the time

# Need this for notify-send to work in cron job
export DISPLAY=:0.0

hour=`date +%-l`
if [[ `date +%M` == "00" ]]; then
    msg="It's $hour o'clock!"
else
    msg="It's `date +%l:%M`!"
fi

case "$hour" in
    9) msg+=" Good morning!";;
    1) msg+=" Time for lunch?";;
    5) msg+=" Almost done!";;
    6) msg+=" Time to go!";;
    *) msg+=" Drink some water!"
esac

img=`shuf -n1 -e face-angel face-cool face-laugh face-smile face-smile-big stock_smiley-1 stock_smiley-3`
notify-send -i $img 'Hey!' "$msg"
# Play a random sound
export cur_path=`dirname $0/`
play "$cur_path/sounds/`ls -1 $cur_path/sounds | shuf -n1`"
