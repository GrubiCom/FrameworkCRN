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


#ifndef INCLUDED_PMT_CPP_TRANSMISSION_DATA_H
#define INCLUDED_PMT_CPP_TRANSMISSION_DATA_H

#include <pmt_cpp/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace pmt_cpp {

    /*!
     * \brief <+description of block+>
     * \ingroup pmt_cpp
     *
     */
    class PMT_CPP_API transmission_data : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<transmission_data> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of pmt_cpp::transmission_data.
       *
       * To avoid accidental use of raw pointers, pmt_cpp::transmission_data's
       * constructor is in a private implementation
       * class. pmt_cpp::transmission_data::make is the public interface for
       * creating new instances.
       */
      static sptr make();
    };

  } // namespace pmt_cpp
} // namespace gr

#endif /* INCLUDED_PMT_CPP_TRANSMISSION_DATA_H */

