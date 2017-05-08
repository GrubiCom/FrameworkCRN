/* -*- c++ -*- */
/* 
 * Copyright 2015 Ariel Marques.
 * Universidade Federal de Lavras - UFLA
 * Departamento de Ciencia da Computacao - DCC
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

#ifndef INCLUDED_PMT_CPP_MESSAGE_TYPE_IMPL_H
#define INCLUDED_PMT_CPP_MESSAGE_TYPE_IMPL_H

#include <pmt_cpp/message_type.h>

namespace gr {
  namespace pmt_cpp {

    class message_type_impl : public message_type
    {
     private:
      // Nothing to declare in this block.
        void run(message_type_impl *instance);
        boost::thread *d_thread;
	gr::thread::mutex d_mutex;

     public:
        message_type_impl();
        ~message_type_impl();
        void set_nmsg(int nmsg);
        int get_nmsg();

        void set_delay(float delay);
        float get_delay();

        void start_tx();
        void stop_tx();
        bool is_running();

    
    };

  } // namespace pmt_cpp
} // namespace gr

#endif /* INCLUDED_PMT_CPP_MESSAGE_TYPE_IMPL_H */

