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

#ifndef INCLUDED_PMT_CPP_TIME_IMPL_H
#define INCLUDED_PMT_CPP_TIME_IMPL_H

#include <pmt_cpp/time.h>

namespace gr {
  namespace pmt_cpp {

    class time_impl : public time
    {
     private:
      // Nothing to declare in this block.

     public:
      time_impl();
      ~time_impl();

      // Where all the action really happens
      void handle_msg(pmt::pmt_t msg);
      
      
    };

  } // namespace pmt_cpp
} // namespace gr

#endif /* INCLUDED_PMT_CPP_TIME_IMPL_H */

