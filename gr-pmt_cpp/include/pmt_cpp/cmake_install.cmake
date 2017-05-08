# Install script for directory: /home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/include/pmt_cpp

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
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/pmt_cpp" TYPE FILE FILES
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/include/pmt_cpp/api.h"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/include/pmt_cpp/pmt_extract.h"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/include/pmt_cpp/message_type.h"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/include/pmt_cpp/pmt_extract2.h"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/include/pmt_cpp/start_sense.h"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/include/pmt_cpp/file_connect.h"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/include/pmt_cpp/PDU_remove_all_tags.h"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/include/pmt_cpp/send_file.h"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/include/pmt_cpp/send_file_ACK.h"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/include/pmt_cpp/start_share.h"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/include/pmt_cpp/ACK.h"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/include/pmt_cpp/pmt_extract_master.h"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/include/pmt_cpp/time.h"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/include/pmt_cpp/decide.h"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/include/pmt_cpp/message_generation.h"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/include/pmt_cpp/wait_first_ack.h"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/include/pmt_cpp/wait_first_ack.h"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/include/pmt_cpp/preprocessor_master.h"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/include/pmt_cpp/Noise.h"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/include/pmt_cpp/set_new_config_master.h"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/include/pmt_cpp/set_ccc.h"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/include/pmt_cpp/transmission_data.h"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/include/pmt_cpp/time_transmission_cycle.h"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/include/pmt_cpp/timer.h"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/include/pmt_cpp/ahp.h"
    "/home/ariel/Documentos/GNURADIO/Blocks_trunk/gr-pmt_cpp/include/pmt_cpp/set_ccc_master.h"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

