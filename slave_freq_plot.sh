#!/bin/bash 

# Plot sensing results

INPUT_LOG="/tmp/sense.txt"

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
	set output 'slave_freq.pdf'
	plot '$INPUT_LOG' using (\$2/1000000000):3 t "x" ls 101 axes x1y1
PDF_PLOT

gnuplot <<TERMINAL_PLOT
	set terminal dumb
	set datafile separator ":"
	set nokey
	set tics scale 0
	set xlabel "Frequency (GHz)"
	set ylabel "Noise Level (dBm)" center
	plot '$INPUT_LOG' using (\$2/1000000000):3 w points pt "*" axes x1y1
TERMINAL_PLOT