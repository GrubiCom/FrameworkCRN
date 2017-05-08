# Install script for directory: /home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/grc

# Set the install prefix
IF(NOT DEFINED CMAKE_INSTALL_PREFIX)
  SET(CMAKE_INSTALL_PREFIX "/usr/local")
ENDIF(NOT DEFINED CMAKE_INSTALL_PREFIX)
STRING(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
IF(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  IF(BUILD_TYPE)
    STRING(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  ELSE(BUILD_TYPE)
    SET(CMAKE_INSTALL_CONFIG_NAME "Release")
  ENDIF(BUILD_TYPE)
  MESSAGE(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
ENDIF(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)

# Set the component getting installed.
IF(NOT CMAKE_INSTALL_COMPONENT)
  IF(COMPONENT)
    MESSAGE(STATUS "Install component: \"${COMPONENT}\"")
    SET(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  ELSE(COMPONENT)
    SET(CMAKE_INSTALL_COMPONENT)
  ENDIF(COMPONENT)
ENDIF(NOT CMAKE_INSTALL_COMPONENT)

# Install shared libraries without execute permission?
IF(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  SET(CMAKE_INSTALL_SO_NO_EXE "1")
ENDIF(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gnuradio/grc/blocks" TYPE FILE FILES
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/grc/pmt_cpp_pmt_extract.xml"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/grc/pmt_cpp_message_type.xml"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/grc/pmt_cpp_pmt_extract2.xml"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/grc/pmt_cpp_start_sense.xml"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/grc/pmt_cpp_file_connect.xml"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/grc/pmt_cpp_PDU_remove_all_tags.xml"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/grc/pmt_cpp_PDU_json.xml"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/grc/pmt_cpp_send_file.xml"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/grc/pmt_cpp_data_extract_master.xml"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/grc/pmt_cpp_send_file_ACK.xml"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/grc/pmt_cpp_start_share.xml"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/grc/pmt_cpp_ACK.xml"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/grc/pmt_cpp_pmt_extract_master.xml"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/grc/pmt_cpp_time.xml"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/grc/pmt_cpp_decide.xml"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/grc/pmt_cpp_message_generation.xml"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/grc/pmt_cpp_annp.xml"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/grc/pmt_cpp_wait_first_ack.xml"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/grc/pmt_cpp_preprocessor_master.xml"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/grc/pmt_cpp_Noise.xml"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/grc/pmt_cpp_set_new_config_master.xml"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/grc/pmt_cpp_set_ccc.xml"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/grc/pmt_cpp_transmission_data.xml"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/grc/pmt_cpp_time_transmission_cycle.xml"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/grc/pmt_cpp_cogmac.xml"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/grc/pmt_cpp_timer.xml"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/grc/pmt_cpp_ahp.xml"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/grc/pmt_cpp_set_ccc_master.xml"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

