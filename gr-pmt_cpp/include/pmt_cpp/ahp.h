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


#ifndef INCLUDED_PMT_CPP_AHP_H
#define INCLUDED_PMT_CPP_AHP_H

#include <pmt_cpp/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace pmt_cpp {

    /*!
     * \brief <+description of block+>
     * \ingroup pmt_cpp
     *
     */
    class PMT_CPP_API ahp : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<ahp> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of pmt_cpp::ahp.
       *
       * To avoid accidental use of raw pointers, pmt_cpp::ahp's
       * constructor is in a private implementation
       * class. pmt_cpp::ahp::make is the public interface for
       * creating new instances.
       */
      static sptr make();
    };

  } // namespace pmt_cpp
} // namespace gr

#endif /* INCLUDED_PMT_CPP_AHP_H */

