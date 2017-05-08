#!/bin/bash 

# Plot results on master node

INPUT_LOG="/tmp/res_sense.txt"
TMP_DAT=".tmp_res_sense.dat"

cp $INPUT_LOG ./$TMP_DAT

sed -i 's/;/\n/g' $TMP_DAT
sed -i 's/\.:/./g' $TMP_DAT
sed -i 's/:\././g' $TMP_DAT
sed -i '/^[0-9]\+:[0-9]\+\(\.[0-9]\+\)*:\(-\)*[0-9]\+\(\.[0-9]\+\)*$/!d' $TMP_DAT
sed -i 's/^[0-9]*://g' $TMP_DAT

gnuplot <<PDF_PLOT
	set terminal pdf size 6,3 font "Courier Bold"
	set style line 81 lt 0  
	set style line 81 lt rgb "#808080"
	set style line 101 lt 1 lc -1 lw 3 ps 0.5
	set grid back linestyle 81
	set datafile separator ":"
	set nokey
	set xlabel "Frequency (GHz)"
	set ylabel "Noise Level (dBm)" center offset 0.8,0 
	set output 'master_freq.pdf'
	plot '$TMP_DAT' using 1:2 t "x" ls 101 axes x1y1
PDF_PLOT

gnuplot <<TERMINAL_PLOT
	set terminal dumb
	set datafile separator ":"
	set nokey
	set tics scale 0
	set xlabel "Frequency (GHz)"
	set ylabel "Noise Level (dBm)" center
	plot '$TMP_DAT' using 1:2 w points pt "*" axes x1y1
TERMINAL_PLOT

rm $TMP_DAT
