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

#ifndef INCLUDED_PMT_CPP_PMT_EXTRACT_IMPL_H
#define INCLUDED_PMT_CPP_PMT_EXTRACT_IMPL_H

#include <pmt_cpp/pmt_extract2.h>
#include <pmt/pmt.h>
#include <iostream>
#include <stdlib.h>

namespace gr {
  namespace pmt_cpp {

    class pmt_extract2_impl : public pmt_extract2
    {
     private:
      // Nothing to declare in this block.
         
     public:
      pmt_extract2_impl();
      ~pmt_extract2_impl();
      void handle_msg(pmt::pmt_t msg);
      
      
    };

  } // namespace pmt_cpp
} // namespace gr

#endif /* INCLUDED_PMT_CPP_PMT_EXTRACT_IMPL_H */

