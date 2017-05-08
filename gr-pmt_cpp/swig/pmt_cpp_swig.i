/* -*- c++ -*- */

#define PMT_CPP_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "pmt_cpp_swig_doc.i"

%{
#include "pmt_cpp/pmt_extract.h"
#include "pmt_cpp/message_type.h"
#include "pmt_cpp/pmt_extract2.h"
#include "pmt_cpp/start_sense.h"
#include "pmt_cpp/file_connect.h"
#include "pmt_cpp/PDU_remove_all_tags.h"
#include "pmt_cpp/send_file.h"
#include "pmt_cpp/send_file_ACK.h"
#include "pmt_cpp/start_share.h"
#include "pmt_cpp/ACK.h"
#include "pmt_cpp/pmt_extract_master.h"
#include "pmt_cpp/time.h"
#include "pmt_cpp/decide.h"
#include "pmt_cpp/message_generation.h"
#include "pmt_cpp/wait_first_ack.h"
#include "pmt_cpp/preprocessor_master.h"
#include "pmt_cpp/Noise.h"
#include "pmt_cpp/set_new_config_master.h"
#include "pmt_cpp/set_ccc.h"
#include "pmt_cpp/transmission_data.h"
#include "pmt_cpp/time_transmission_cycle.h"
#include "pmt_cpp/timer.h"
#include "pmt_cpp/ahp.h"
#include "pmt_cpp/set_ccc_master.h"
%}


%include "pmt_cpp/pmt_extract.h"
GR_SWIG_BLOCK_MAGIC2(pmt_cpp, pmt_extract);

%include "pmt_cpp/message_type.h"
GR_SWIG_BLOCK_MAGIC2(pmt_cpp, message_type);

%include "pmt_cpp/pmt_extract2.h"
GR_SWIG_BLOCK_MAGIC2(pmt_cpp, pmt_extract2);
%include "pmt_cpp/start_sense.h"
GR_SWIG_BLOCK_MAGIC2(pmt_cpp, start_sense);
%include "pmt_cpp/file_connect.h"
GR_SWIG_BLOCK_MAGIC2(pmt_cpp, file_connect);
%include "pmt_cpp/PDU_remove_all_tags.h"
GR_SWIG_BLOCK_MAGIC2(pmt_cpp, PDU_remove_all_tags);
%include "pmt_cpp/send_file.h"
GR_SWIG_BLOCK_MAGIC2(pmt_cpp, send_file);

%include "pmt_cpp/send_file_ACK.h"
GR_SWIG_BLOCK_MAGIC2(pmt_cpp, send_file_ACK);
%include "pmt_cpp/start_share.h"
GR_SWIG_BLOCK_MAGIC2(pmt_cpp, start_share);
%include "pmt_cpp/ACK.h"
GR_SWIG_BLOCK_MAGIC2(pmt_cpp, ACK);
%include "pmt_cpp/pmt_extract_master.h"
GR_SWIG_BLOCK_MAGIC2(pmt_cpp, pmt_extract_master);
%include "pmt_cpp/time.h"
GR_SWIG_BLOCK_MAGIC2(pmt_cpp, time);
%include "pmt_cpp/decide.h"
GR_SWIG_BLOCK_MAGIC2(pmt_cpp, decide);
%include "pmt_cpp/message_generation.h"
GR_SWIG_BLOCK_MAGIC2(pmt_cpp, message_generation);

%include "pmt_cpp/wait_first_ack.h"
GR_SWIG_BLOCK_MAGIC2(pmt_cpp, wait_first_ack);
%include "pmt_cpp/preprocessor_master.h"
GR_SWIG_BLOCK_MAGIC2(pmt_cpp, preprocessor_master);
%include "pmt_cpp/Noise.h"
GR_SWIG_BLOCK_MAGIC2(pmt_cpp, Noise);
%include "pmt_cpp/set_new_config_master.h"
GR_SWIG_BLOCK_MAGIC2(pmt_cpp, set_new_config_master);
%include "pmt_cpp/set_ccc.h"
GR_SWIG_BLOCK_MAGIC2(pmt_cpp, set_ccc);
%include "pmt_cpp/transmission_data.h"
GR_SWIG_BLOCK_MAGIC2(pmt_cpp, transmission_data);
%include "pmt_cpp/time_transmission_cycle.h"
GR_SWIG_BLOCK_MAGIC2(pmt_cpp, time_transmission_cycle);

%include "pmt_cpp/timer.h"
GR_SWIG_BLOCK_MAGIC2(pmt_cpp, timer);
%include "pmt_cpp/ahp.h"
GR_SWIG_BLOCK_MAGIC2(pmt_cpp, ahp);
%include "pmt_cpp/set_ccc_master.h"
GR_SWIG_BLOCK_MAGIC2(pmt_cpp, set_ccc_master);
