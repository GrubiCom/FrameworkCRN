# Copyright 2011 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
install(FILES
    pmt_cpp_pmt_extract.xml
    pmt_cpp_message_type.xml
    pmt_cpp_pmt_extract2.xml
    pmt_cpp_start_sense.xml
    pmt_cpp_file_connect.xml
    pmt_cpp_PDU_remove_all_tags.xml
    pmt_cpp_PDU_json.xml
    pmt_cpp_send_file.xml
    pmt_cpp_data_extract_master.xml
    pmt_cpp_send_file_ACK.xml
    pmt_cpp_start_share.xml
    pmt_cpp_ACK.xml
    pmt_cpp_pmt_extract_master.xml
    pmt_cpp_time.xml
    pmt_cpp_decide.xml
    pmt_cpp_message_generation.xml
    pmt_cpp_annp.xml
    pmt_cpp_wait_first_ack.xml
    pmt_cpp_preprocessor_master.xml
    pmt_cpp_Noise.xml
    pmt_cpp_set_new_config_master.xml
    pmt_cpp_set_ccc.xml
    pmt_cpp_transmission_data.xml
    pmt_cpp_time_transmission_cycle.xml
    pmt_cpp_cogmac.xml
    pmt_cpp_timer.xml
    pmt_cpp_ahp.xml
    pmt_cpp_set_ccc_master.xml
    pmt_cpp_RandomForest.xml DESTINATION share/gnuradio/grc/blocks
)
