#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Cognitive network over IEEE 802.15.4
# Author: Ariel Marques
# Generated: Wed May  3 17:13:44 2017
##################################################

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from File_Recorder import File_Recorder  # grc-generated hier_block
from Get_Power import Get_Power  # grc-generated hier_block
from IEEE_802_15_4 import IEEE_802_15_4  # grc-generated hier_block
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import pmt_cpp
import time


class Cog_sense(gr.top_block):

    def __init__(self, samp_rate=4e6):
        gr.top_block.__init__(self, "Cognitive network over IEEE 802.15.4")

        ##################################################
        # Parameters
        ##################################################
        self.samp_rate = samp_rate

        ##################################################
        # Variables
        ##################################################
        self.bw = bw = 1000e3

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
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(6000000000, 0)
        self.uhd_usrp_source_0.set_gain(30, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.uhd_usrp_source_0.set_bandwidth(bw, 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(('', "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(6000000000, 0)
        self.uhd_usrp_sink_0.set_gain(89, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0.set_bandwidth(bw, 0)
        self.pmt_cpp_wait_first_ack_0 = pmt_cpp.wait_first_ack()
        self.pmt_cpp_transmission_data_0 = pmt_cpp.transmission_data()
        self.pmt_cpp_start_share_0 = pmt_cpp.start_share()
        self.pmt_cpp_start_sense_0 = pmt_cpp.start_sense()
        self.pmt_cpp_set_ccc_0 = pmt_cpp.set_ccc()
        self.pmt_cpp_send_file_ACK_2 = pmt_cpp.send_file_ACK()
        self.pmt_cpp_pmt_extract2_0 = pmt_cpp.pmt_extract2()
        self.pmt_cpp_file_connect_0 = pmt_cpp.file_connect()
        self.pmt_cpp_ACK_0 = pmt_cpp.ACK()
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.IEEE_802_15_4_0 = IEEE_802_15_4()
        self.Get_Power_0 = Get_Power()
        self.File_Recorder_0 = File_Recorder()

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.File_Recorder_0, 'file_ready'), (self.pmt_cpp_send_file_ACK_2, 'file_ready'))
        self.msg_connect((self.IEEE_802_15_4_0, 'rxout'), (self.pmt_cpp_pmt_extract2_0, 'in_pdu'))
        self.msg_connect((self.pmt_cpp_ACK_0, 'msg'), (self.IEEE_802_15_4_0, 'msg'))
        self.msg_connect((self.pmt_cpp_ACK_0, 'first'), (self.pmt_cpp_wait_first_ack_0, 'fisrt_message'))
        self.msg_connect((self.pmt_cpp_file_connect_0, 'bool'), (self.File_Recorder_0, 'in_pdu'))
        self.msg_connect((self.pmt_cpp_pmt_extract2_0, 'info_neighbor'), (self.IEEE_802_15_4_0, 'msg'))
        self.msg_connect((self.pmt_cpp_pmt_extract2_0, 'sense'), (self.pmt_cpp_start_sense_0, 'pmt::dict'))
        self.msg_connect((self.pmt_cpp_pmt_extract2_0, 'share'), (self.pmt_cpp_start_share_0, 'pmt::dict'))
        self.msg_connect((self.pmt_cpp_send_file_ACK_2, 'pdu'), (self.pmt_cpp_ACK_0, 'File_Ready'))
        self.msg_connect((self.pmt_cpp_set_ccc_0, 'ccc'), (self.uhd_usrp_sink_0, 'command'))
        self.msg_connect((self.pmt_cpp_set_ccc_0, 'ccc'), (self.uhd_usrp_source_0, 'command'))
        self.msg_connect((self.pmt_cpp_start_sense_0, 'bool'), (self.File_Recorder_0, 'bool'))
        self.msg_connect((self.pmt_cpp_start_sense_0, 'bool'), (self.pmt_cpp_file_connect_0, 'in_pdu'))
        self.msg_connect((self.pmt_cpp_start_sense_0, 'pmt::mp'), (self.uhd_usrp_sink_0, 'command'))
        self.msg_connect((self.pmt_cpp_start_sense_0, 'pmt::mp'), (self.uhd_usrp_source_0, 'command'))
        self.msg_connect((self.pmt_cpp_start_share_0, 'bool'), (self.IEEE_802_15_4_0, 'msg'))
        self.msg_connect((self.pmt_cpp_start_share_0, 'bool'), (self.pmt_cpp_set_ccc_0, 'flag'))
        self.msg_connect((self.pmt_cpp_start_share_0, 'bool'), (self.pmt_cpp_transmission_data_0, 'signal_in'))
        self.msg_connect((self.pmt_cpp_start_share_0, 'pmt::mp'), (self.uhd_usrp_sink_0, 'command'))
        self.msg_connect((self.pmt_cpp_start_share_0, 'pmt::mp'), (self.uhd_usrp_source_0, 'command'))
        self.msg_connect((self.pmt_cpp_transmission_data_0, 'signal_out'), (self.Get_Power_0, 'in_pdu'))
        self.msg_connect((self.pmt_cpp_transmission_data_0, 'packet'), (self.IEEE_802_15_4_0, 'msg'))
        self.msg_connect((self.pmt_cpp_wait_first_ack_0, 'message_repeat'), (self.IEEE_802_15_4_0, 'msg'))
        self.connect((self.IEEE_802_15_4_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.pmt_cpp_file_connect_0, 0), (self.File_Recorder_0, 0))
        self.connect((self.pmt_cpp_file_connect_0, 1), (self.blocks_null_sink_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.Get_Power_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.IEEE_802_15_4_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.pmt_cpp_file_connect_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw
        self.uhd_usrp_source_0.set_bandwidth(self.bw, 0)
        self.uhd_usrp_sink_0.set_bandwidth(self.bw, 0)


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--samp-rate", dest="samp_rate", type="eng_float", default=eng_notation.num_to_str(4e6),
        help="Set samp_rate [default=%default]")
    return parser


def main(top_block_cls=Cog_sense, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(samp_rate=options.samp_rate)
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
