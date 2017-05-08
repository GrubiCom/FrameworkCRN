#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: IEEE 802.15.4 Transceiver using OQPSK PHY
# Generated: Wed May  3 16:51:12 2017
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from IEEE_802_15_4 import IEEE_802_15_4  # grc-generated hier_block
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import pmt_cpp
import time
import wx


class master(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="IEEE 802.15.4 Transceiver using OQPSK PHY")

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(('', "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(4000000)
        self.uhd_usrp_source_0.set_center_freq(6000000000, 0)
        self.uhd_usrp_source_0.set_gain(40, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.uhd_usrp_source_0.set_bandwidth(1000e3, 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(('', "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(4000000)
        self.uhd_usrp_sink_0.set_center_freq(6000000000, 0)
        self.uhd_usrp_sink_0.set_gain(89, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0.set_bandwidth(1000e3, 0)
        self.pmt_cpp_timer_0 = pmt_cpp.timer()
        self.pmt_cpp_time_transmission_cycle_0 = pmt_cpp.time_transmission_cycle()
        self.pmt_cpp_time_0 = pmt_cpp.time()
        self.pmt_cpp_set_new_config_master_0 = pmt_cpp.set_new_config_master()
        self.pmt_cpp_set_ccc_master_0 = pmt_cpp.set_ccc_master()
        self.pmt_cpp_preprocessor_master_0 = pmt_cpp.preprocessor_master()
        self.pmt_cpp_pmt_extract_master_0 = pmt_cpp.pmt_extract_master()
        self.pmt_cpp_message_generation_0 = pmt_cpp.message_generation()
        self.pmt_cpp_data_extract_master_0 = pmt_cpp.data_extract_master('/tmp/res_sense.txt')
        self.pmt_cpp_annp_0 = pmt_cpp.annp()
        self.IEEE_802_15_4_0 = IEEE_802_15_4()

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.IEEE_802_15_4_0, 'rxout'), (self.pmt_cpp_pmt_extract_master_0, 'in_pdu'))
        self.msg_connect((self.pmt_cpp_annp_0, 'out'), (self.IEEE_802_15_4_0, 'msg'))
        self.msg_connect((self.pmt_cpp_message_generation_0, 'msg'), (self.IEEE_802_15_4_0, 'msg'))
        self.msg_connect((self.pmt_cpp_message_generation_0, 'mp'), (self.uhd_usrp_sink_0, 'command'))
        self.msg_connect((self.pmt_cpp_message_generation_0, 'mp'), (self.uhd_usrp_source_0, 'command'))
        self.msg_connect((self.pmt_cpp_pmt_extract_master_0, 'Ack'), (self.IEEE_802_15_4_0, 'msg'))
        self.msg_connect((self.pmt_cpp_pmt_extract_master_0, 'data'), (self.pmt_cpp_data_extract_master_0, 'pdus'))
        self.msg_connect((self.pmt_cpp_pmt_extract_master_0, 'freq'), (self.pmt_cpp_set_ccc_master_0, 'flag'))
        self.msg_connect((self.pmt_cpp_pmt_extract_master_0, 'share'), (self.pmt_cpp_set_ccc_master_0, 'flag'))
        self.msg_connect((self.pmt_cpp_pmt_extract_master_0, 'share'), (self.pmt_cpp_set_new_config_master_0, 'pmt::dict'))
        self.msg_connect((self.pmt_cpp_pmt_extract_master_0, 'data'), (self.pmt_cpp_time_0, 'Ack'))
        self.msg_connect((self.pmt_cpp_pmt_extract_master_0, 'freq'), (self.pmt_cpp_time_transmission_cycle_0, 'in_signal'))
        self.msg_connect((self.pmt_cpp_pmt_extract_master_0, 'share'), (self.pmt_cpp_time_transmission_cycle_0, 'in_signal'))
        self.msg_connect((self.pmt_cpp_pmt_extract_master_0, 'freq'), (self.uhd_usrp_sink_0, 'command'))
        self.msg_connect((self.pmt_cpp_pmt_extract_master_0, 'freq'), (self.uhd_usrp_source_0, 'command'))
        self.msg_connect((self.pmt_cpp_preprocessor_master_0, 'rna_file'), (self.pmt_cpp_annp_0, 'in'))
        self.msg_connect((self.pmt_cpp_preprocessor_master_0, 'rna_file'), (self.pmt_cpp_timer_0, 'in2'))
        self.msg_connect((self.pmt_cpp_preprocessor_master_0, 'tuned'), (self.uhd_usrp_sink_0, 'command'))
        self.msg_connect((self.pmt_cpp_preprocessor_master_0, 'tuned'), (self.uhd_usrp_source_0, 'command'))
        self.msg_connect((self.pmt_cpp_set_ccc_master_0, 'signal'), (self.pmt_cpp_message_generation_0, 'signal'))
        self.msg_connect((self.pmt_cpp_set_ccc_master_0, 'ccc'), (self.uhd_usrp_sink_0, 'command'))
        self.msg_connect((self.pmt_cpp_set_ccc_master_0, 'ccc'), (self.uhd_usrp_source_0, 'command'))
        self.msg_connect((self.pmt_cpp_set_new_config_master_0, 'bool'), (self.IEEE_802_15_4_0, 'msg'))
        self.msg_connect((self.pmt_cpp_set_new_config_master_0, 'pmt::mp'), (self.uhd_usrp_sink_0, 'command'))
        self.msg_connect((self.pmt_cpp_set_new_config_master_0, 'pmt::mp'), (self.uhd_usrp_source_0, 'command'))
        self.msg_connect((self.pmt_cpp_time_0, 'Ack_repeat'), (self.IEEE_802_15_4_0, 'msg'))
        self.msg_connect((self.pmt_cpp_time_0, 'id_neighbor'), (self.pmt_cpp_preprocessor_master_0, 'id_neighbor'))
        self.msg_connect((self.pmt_cpp_time_0, 'Feed_back'), (self.pmt_cpp_time_0, 'Ack'))
        self.msg_connect((self.pmt_cpp_time_0, 'id_neighbor'), (self.pmt_cpp_timer_0, 'in'))
        self.msg_connect((self.pmt_cpp_time_transmission_cycle_0, 'out_signal'), (self.pmt_cpp_message_generation_0, 'signal'))
        self.msg_connect((self.pmt_cpp_time_transmission_cycle_0, 'out_signal'), (self.pmt_cpp_set_ccc_master_0, 'flag'))
        self.msg_connect((self.pmt_cpp_timer_0, 'out'), (self.pmt_cpp_annp_0, 'in'))
        self.connect((self.IEEE_802_15_4_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.IEEE_802_15_4_0, 0))


def main(top_block_cls=master, options=None):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
