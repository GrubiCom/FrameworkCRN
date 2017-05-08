#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/lib
export GR_CONF_CONTROLPORT_ON=False
export PATH=/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/lib:$PATH
export LD_LIBRARY_PATH=/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$PYTHONPATH
test-pmt_cpp 
