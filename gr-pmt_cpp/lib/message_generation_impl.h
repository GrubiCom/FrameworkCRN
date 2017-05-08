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

#ifndef INCLUDED_PMT_CPP_MESSAGE_GENERATION_IMPL_H
#define INCLUDED_PMT_CPP_MESSAGE_GENERATION_IMPL_H

#include <pmt_cpp/message_generation.h>

namespace gr {
  namespace pmt_cpp {

    class message_generation_impl : public message_generation
    {
     private:
        void run(message_generation_impl *instance);
        int d_nmsg_left;
        int count;
        int cycle;
        int gain;
        bool d_finished;
        int init;
        double new_freq;
        double old_freq;
        bool neighbors_msg;
        float d_interval;
        pmt::pmt_t d_msg;
        boost::thread *d_thread;
        gr::thread::mutex d_mutex;
        double min,max,dif;
     public:
        message_generation_impl();
        ~message_generation_impl();
        void set_nmsg(int nmsg);
        int get_nmsg();

        void set_delay(float delay);
        float get_delay();
        void set_de_finished(pmt::pmt_t pdu);
        void start_tx();
        void stop_tx();
        bool is_running();
        void send_sense();
      // Where all the action really happens
      
    };

  } // namespace pmt_cpp
} // namespace gr

#endif /* INCLUDED_PMT_CPP_MESSAGE_GENERATION_IMPL_H */

