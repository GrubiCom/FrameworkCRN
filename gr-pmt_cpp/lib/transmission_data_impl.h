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

#ifndef INCLUDED_PMT_CPP_TRANSMISSION_DATA_IMPL_H
#define INCLUDED_PMT_CPP_TRANSMISSION_DATA_IMPL_H

#include <pmt_cpp/transmission_data.h>
#include <ctime>

namespace gr {
  namespace pmt_cpp {

    class transmission_data_impl : public transmission_data
    {
     private:
         
         double d_power;
         
     public:
      transmission_data_impl();
      ~transmission_data_impl();
      double get_power();

      void handle(pmt::pmt_t pdu);
      
    };

  } // namespace pmt_cpp
} // namespace gr

#endif /* INCLUDED_PMT_CPP_TRANSMISSION_DATA_IMPL_H */

