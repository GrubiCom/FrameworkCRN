#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: IEEE 802.15.4 Transceiver using OQPSK PHY
# Generated: Thu Apr 27 01:47:47 2017
##################################################

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from IEEE_802_15_4 import IEEE_802_15_4  # grc-generated hier_block
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
from spectrum_decision import spectrum_decision  # grc-generated hier_block
from spectrum_mobility_M import spectrum_mobility_M  # grc-generated hier_block
from spectrum_sensing_M import spectrum_sensing_M  # grc-generated hier_block
from spectrum_sharing_M import spectrum_sharing_M  # grc-generated hier_block
from usrp_master import usrp_master  # grc-generated hier_block
import pmt_cpp


class master(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "IEEE 802.15.4 Transceiver using OQPSK PHY")

        ##################################################
        # Blocks
        ##################################################
        self.usrp_master_0 = usrp_master()
        self.spectrum_sharing_M_0 = spectrum_sharing_M()
        self.spectrum_sensing_M_0 = spectrum_sensing_M()
        self.spectrum_mobility_M_0 = spectrum_mobility_M()
        self.spectrum_decision_0 = spectrum_decision()
        self.pmt_cpp_time_transmission_cycle_0 = pmt_cpp.time_transmission_cycle()
        self.pmt_cpp_pmt_extract_master_0 = pmt_cpp.pmt_extract_master()
        self.pmt_cpp_message_generation_0 = pmt_cpp.message_generation()
        self.IEEE_802_15_4_0 = IEEE_802_15_4()

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.IEEE_802_15_4_0, 'rxout'), (self.pmt_cpp_pmt_extract_master_0, 'in_pdu'))
        self.msg_connect((self.pmt_cpp_message_generation_0, 'msg'), (self.IEEE_802_15_4_0, 'msg'))
        self.msg_connect((self.pmt_cpp_pmt_extract_master_0, 'Ack'), (self.IEEE_802_15_4_0, 'msg'))
        self.msg_connect((self.pmt_cpp_pmt_extract_master_0, 'freq'), (self.pmt_cpp_time_transmission_cycle_0, 'in_signal'))
        self.msg_connect((self.pmt_cpp_pmt_extract_master_0, 'share'), (self.pmt_cpp_time_transmission_cycle_0, 'in_signal'))
        self.msg_connect((self.pmt_cpp_pmt_extract_master_0, 'share'), (self.spectrum_mobility_M_0, 'flag'))
        self.msg_connect((self.pmt_cpp_pmt_extract_master_0, 'data'), (self.spectrum_sensing_M_0, 'data_sensing'))
        self.msg_connect((self.pmt_cpp_pmt_extract_master_0, 'share'), (self.spectrum_sharing_M_0, 'sharing_message'))
        self.msg_connect((self.pmt_cpp_time_transmission_cycle_0, 'out_signal'), (self.pmt_cpp_message_generation_0, 'signal'))
        self.msg_connect((self.pmt_cpp_time_transmission_cycle_0, 'out_signal'), (self.spectrum_mobility_M_0, 'flag'))
        self.msg_connect((self.spectrum_decision_0, 'out'), (self.IEEE_802_15_4_0, 'msg'))
        self.msg_connect((self.spectrum_mobility_M_0, 'signal'), (self.pmt_cpp_message_generation_0, 'signal'))
        self.msg_connect((self.spectrum_mobility_M_0, 'ccc'), (self.usrp_master_0, 'command_sink'))
        self.msg_connect((self.spectrum_mobility_M_0, 'ccc'), (self.usrp_master_0, 'command_source'))
        self.msg_connect((self.spectrum_sensing_M_0, 'ack_repeat'), (self.IEEE_802_15_4_0, 'msg'))
        self.msg_connect((self.spectrum_sensing_M_0, 'ok'), (self.spectrum_decision_0, 'in'))
        self.msg_connect((self.spectrum_sensing_M_0, 'rna_file'), (self.spectrum_decision_0, 'in'))
        self.msg_connect((self.spectrum_sensing_M_0, 'tuned'), (self.usrp_master_0, 'command_sink'))
        self.msg_connect((self.spectrum_sensing_M_0, 'tuned'), (self.usrp_master_0, 'command_source'))
        self.msg_connect((self.spectrum_sharing_M_0, 'bool'), (self.IEEE_802_15_4_0, 'msg'))
        self.msg_connect((self.spectrum_sharing_M_0, 'new_frequency'), (self.usrp_master_0, 'command_sink'))
        self.msg_connect((self.spectrum_sharing_M_0, 'new_frequency'), (self.usrp_master_0, 'command_source'))
        self.connect((self.IEEE_802_15_4_0, 0), (self.usrp_master_0, 0))
        self.connect((self.usrp_master_0, 0), (self.IEEE_802_15_4_0, 0))


def main(top_block_cls=master, options=None):

    tb = top_block_cls()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
