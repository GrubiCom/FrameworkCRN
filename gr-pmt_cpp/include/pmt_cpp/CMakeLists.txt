# Copyright 2011,2012 Free Software Foundation, Inc.
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

########################################################################
# Install public header files
########################################################################
install(FILES
    api.h
    pmt_extract.h
    message_type.h
    pmt_extract2.h
    start_sense.h
    file_connect.h
    PDU_remove_all_tags.h
    send_file.h
    send_file_ACK.h
    start_share.h
    ACK.h
    pmt_extract_master.h
    time.h
    decide.h
    message_generation.h
    wait_first_ack.h
    wait_first_ack.h
    preprocessor_master.h
    Noise.h
    set_new_config_master.h
    set_ccc.h
    transmission_data.h
    time_transmission_cycle.h
    timer.h
    ahp.h
    set_ccc_master.h DESTINATION include/pmt_cpp
)
