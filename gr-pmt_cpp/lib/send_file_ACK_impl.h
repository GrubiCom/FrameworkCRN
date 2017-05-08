/* -*- c++ -*- */
/* 
 * Copyright 2015 <+YOU OR YOUR COMPANY+>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifndef INCLUDED_PMT_CPP_SEND_FILE_ACK_IMPL_H
#define INCLUDED_PMT_CPP_SEND_FILE_ACK_IMPL_H

#include <pmt_cpp/send_file_ACK.h>

namespace gr {
  namespace pmt_cpp {

    class send_file_ACK_impl : public send_file_ACK
    {
     private:
      void run(send_file_ACK_impl *instance);

      // Nothing to declare in this block.
      int d_nmsg_total;
        int d_nmsg_left;
        bool d_debug;
        bool d_quit;
        bool d_finished;
        float d_interval;
        std::string d_msg;
        boost::thread *d_thread;
        gr::thread::mutex d_mutex;
      bool ready;   
      
     public:
      send_file_ACK_impl();
      ~send_file_ACK_impl();

      void handle_msg();
      void trigger(pmt::pmt_t msg);
      void send();
    };

  } // namespace pmt_cpp
} // namespace gr

#endif /* INCLUDED_PMT_CPP_SEND_FILE_IMPL_H */

