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
# Setup library
########################################################################
include(GrPlatform) #define LIB_SUFFIX

include_directories(${Boost_INCLUDE_DIR})
link_directories(${Boost_LIBRARY_DIRS})
list(APPEND pmt_cpp_sources
    pmt_extract_impl.cc
    message_type_impl.cc
    pmt_extract2_impl.cc
    start_sense_impl.cc
    file_connect_impl.cc
    PDU_remove_all_tags_impl.cc
    send_file_impl.cc
    send_file_ACK_impl.cc
    start_share_impl.cc
    ACK_impl.cc
    pmt_extract_master_impl.cc
    time_impl.cc
    decide_impl.cc
    message_generation_impl.cc
    wait_first_ack_impl.cc
    preprocessor_master_impl.cc
    Noise_impl.cc
    set_new_config_master_impl.cc
    set_ccc_impl.cc
    transmission_data_impl.cc
    time_transmission_cycle_impl.cc
    timer_impl.cc
    ahp_impl.cc
    set_ccc_master_impl.cc )

set(pmt_cpp_sources "${pmt_cpp_sources}" PARENT_SCOPE)
if(NOT pmt_cpp_sources)
	MESSAGE(STATUS "No C++ sources... skipping lib/")
	return()
endif(NOT pmt_cpp_sources)

add_library(gnuradio-pmt_cpp SHARED ${pmt_cpp_sources})
target_link_libraries(gnuradio-pmt_cpp ${Boost_LIBRARIES} ${GNURADIO_ALL_LIBRARIES})
set_target_properties(gnuradio-pmt_cpp PROPERTIES DEFINE_SYMBOL "gnuradio_pmt_cpp_EXPORTS")

if(APPLE)
    set_target_properties(gnuradio-pmt_cpp PROPERTIES
        INSTALL_NAME_DIR "${CMAKE_INSTALL_PREFIX}/lib"
    )
endif(APPLE)

########################################################################
# Install built library files
########################################################################
install(TARGETS gnuradio-pmt_cpp
    LIBRARY DESTINATION lib${LIB_SUFFIX} # .so/.dylib file
    ARCHIVE DESTINATION lib${LIB_SUFFIX} # .lib file
    RUNTIME DESTINATION bin              # .dll file
)

########################################################################
# Build and register unit test
########################################################################
include(GrTest)

include_directories(${CPPUNIT_INCLUDE_DIRS})

list(APPEND test_pmt_cpp_sources
    ${CMAKE_CURRENT_SOURCE_DIR}/test_pmt_cpp.cc
    ${CMAKE_CURRENT_SOURCE_DIR}/qa_pmt_cpp.cc
    ${CMAKE_CURRENT_SOURCE_DIR}/qa_message_type.cc
)

add_executable(test-pmt_cpp ${test_pmt_cpp_sources})

target_link_libraries(
  test-pmt_cpp
  ${GNURADIO_RUNTIME_LIBRARIES}
  ${Boost_LIBRARIES}
  ${CPPUNIT_LIBRARIES}
  gnuradio-pmt_cpp
)

GR_ADD_TEST(test_pmt_cpp test-pmt_cpp)
