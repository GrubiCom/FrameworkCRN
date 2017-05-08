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

#ifndef INCLUDED_PMT_CPP_PMT_EXTRACT_IMPL_H
#define INCLUDED_PMT_CPP_PMT_EXTRACT_IMPL_H

#include <pmt_cpp/pmt_extract.h>
//I'm trying to run two executables consecutively using this c code:
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/wait.h>

namespace gr {
  namespace pmt_cpp {

    class pmt_extract_impl : public pmt_extract
    {
     private:
      // Nothing to declare in this block.

     public:
      pmt_extract_impl();
      void handle_msg(pmt::pmt_t msg);
      int exitreason(pid_t cid, int status);
      
    };

  } // namespace pmt_cpp
} // namespace gr

#endif /* INCLUDED_PMT_CPP_PMT_EXTRACT_IMPL_H */

