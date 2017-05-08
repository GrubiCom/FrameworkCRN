#!/bin/bash 

# Plot the best frequency selected and spectrum sensing

SLAVE_SENSE="/tmp/sense.txt"
MASTER_SENSE="tmp/res_sense.txt"
BEST_CHANNEL="/tmp/master_channels.txt"
SENSE_DATA=".tmp_res_sense.dat"
CH_RESULT=".tmp_best_channel.dat"

if [ -e $BEST_CHANNEL ]; then
	
	cp $BEST_CHANNEL ./$CH_RESULT
	echo "..."
	
else
	
	echo "ERROR: best channel information not found!"
	exit 1
fi

if [ -e $SLAVE_SENSE ]; then
	
	cp $SLAVE_SENSE ./$SENSE_DATA
	
gnuplot <<PDF_PLOT
	set terminal pdf size 6,3 font "Courier Bold"
	set style line 81 lt 0  
	set style line 81 lt rgb "#808080"
	set style line 101 lt 1 lc -1 lw 3 ps 0.5
	set style line 102 lt 2 lc 1 lw 4 ps 1
	set grid back linestyle 81
	set datafile separator ":"
	set key box width 1 left bottom samplen 0.7
	sense_data = system('cat $CH_RESULT')
	set for [w in sense_data] arrow from first w, graph 0 to first w, graph 1 linewidth 4 linecolor rgb 'red' nohead
	set xlabel "Frequency (GHz)"
	set ylabel "Noise Level (dBm)" center offset 0.8,0
	set output 'best_channel_slave.pdf'
	plot '$SENSE_DATA' using (\$2/1000000000):3 notitle ls 101, \
	NaN with points ls 101 title "Noise", \
	NaN ls 102 title "Best Ch."
PDF_PLOT

gnuplot <<TERMINAL_PLOT
	set terminal dumb
	set datafile separator ":"
	set nokey
	set tics scale 0
	set xlabel "Frequency (GHz)"
	set ylabel "Noise Level (dBm)" center
	sense_data = system('cat $CH_RESULT')
	set for [w in sense_data] arrow from first w, graph 0 to first w, graph 1 linewidth 4 linecolor rgb 'red' nohead
	plot '$SENSE_DATA' using (\$2/1000000000):3 w points pt "*" axes x1y1
TERMINAL_PLOT
	
elif [ -e $MASTER_SENSE ]; then
	
	cp $MASTER_SENSE ./$SENSE_DATA
	sed -i 's/;/\n/g' $SENSE_DATA
	sed -i 's/\.:/./g' $SENSE_DATA
	sed -i 's/:\././g' $SENSE_DATA
	sed -i '/^[0-9]\+:[0-9]\+\(\.[0-9]\+\)*:\(-\)*[0-9]\+\(\.[0-9]\+\)*$/!d' $SENSE_DATA
	
gnuplot <<PDF_PLOT
	set terminal pdf size 6,3 font "Courier Bold"
	set style line 81 lt 0  
	set style line 81 lt rgb "#808080"
	set style line 101 lt 1 lc -1 lw 3 ps 0.5
	set style line 102 lt 2 lc 1 lw 4 ps 1
	set grid back linestyle 81
	set datafile separator ":"
	set key box width 1 left bottom samplen 0.7
	sense_data = system('cat $CH_RESULT')
	set for [w in sense_data] arrow from first w, graph 0 to first w, graph 1 linewidth 4 linecolor rgb 'red' nohead
	set xlabel "Frequency (GHz)"
	set ylabel "Noise Level (dBm)" center offset 0.8,0
	set output 'best_channel_master.pdf'
	plot '$SENSE_DATA' using 2:3 notitle ls 101, \
	NaN with points ls 101 title "Noise", \
	NaN ls 102 title "Best Ch."
PDF_PLOT

gnuplot <<TERMINAL_PLOT
	set terminal dumb
	set datafile separator ":"
	set nokey
	set tics scale 0
	set xlabel "Frequency (GHz)"
	set ylabel "Noise Level (dBm)" center
	sense_data = system('cat $CH_RESULT')
	set for [w in sense_data] arrow from first w, graph 0 to first w, graph 1 linewidth 4 linecolor rgb 'red' nohead
	plot '$SENSE_DATA' using 2:3 w points pt "*" axes x1y1
TERMINAL_PLOT

else
	
	echo "ERROR: no log files found!"
	exit 1
fi

rm $SENSE_DATA
rm $CH_RESULT
