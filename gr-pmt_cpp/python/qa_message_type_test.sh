#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/python
export GR_CONF_CONTROLPORT_ON=False
export PATH=/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/python:$PATH
export LD_LIBRARY_PATH=/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/lib:$LD_LIBRARY_PATH
export PYTHONPATH=/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/swig:$PYTHONPATH
/usr/bin/python2 /home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/python/qa_message_type.py 
