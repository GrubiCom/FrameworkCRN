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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "set_new_config_master_impl.h"
#include <fstream>

namespace gr {
  namespace pmt_cpp {

    set_new_config_master::sptr
    set_new_config_master::make()
    {
      return gnuradio::get_initial_sptr
        (new set_new_config_master_impl());
    }

    /*
     * The private constructor
     */
    set_new_config_master_impl::set_new_config_master_impl()
      : gr::block("set_new_config_master",
              gr::io_signature::make(0, 0, 0),            //Anulo as entradas de fluxo de dados
        gr::io_signature::make(0, 0, 0))            //Anulo as saidas de fluxo de dados
    { 
        message_port_register_out(pmt::mp("pmt::mp"));
        message_port_register_out(pmt::mp("bool")); 

        pmt::pmt_t p_dict1 = pmt::make_dict(); /* Initiation of dictionary */

        p_dict1 = pmt::dict_add(p_dict1, pmt::string_to_symbol("share"), pmt::PMT_F);
        pmt::pmt_t sharet1 = pmt::PMT_NIL;
        sharet1 = pmt::dict_ref(p_dict1, pmt::string_to_symbol("share"), pmt::PMT_NIL);

        

        message_port_register_in(pmt::mp("pmt::dict"));
        set_msg_handler(pmt::mp("pmt::dict"), boost::bind(&set_new_config_master_impl::handle_msg, this, _1));
    }

    /*
     * Our virtual destructor.
     */
    set_new_config_master_impl::~set_new_config_master_impl()
    {
    }
    
    void set_new_config_master_impl::handle_msg(pmt::pmt_t msg) {
        std::cout <<"[MASTER][SET NEW CONFIG MASTER]: SHARE" << std::endl;
        pmt::pmt_t nChannel = pmt::dict_ref(msg, pmt::string_to_symbol("nChannel"), pmt::PMT_NIL);
        pmt::pmt_t str = pmt::dict_ref(msg, pmt::string_to_symbol("ID"), pmt::PMT_NIL);
        double newChannel = pmt::to_double(nChannel);


        message_port_pub(pmt::mp("bool"), pmt::intern("<S:"+pmt::symbol_to_string(str)+":"+boost::to_string(newChannel/1e9)+">"));
        
        std::fstream out; 
        out.open("/tmp/master_channels.txt", std::ios::out);
        if(out.is_open()){
            out << (pmt::to_double(nChannel)/1e9)<< std::endl;

            out.close();
        }
        message_port_pub(pmt::mp("pmt::mp"), pmt::cons(pmt::mp("freq"), pmt::mp(pmt::to_double(nChannel))));

        
                   
    }
    

  } /* namespace pmt_cpp */
} /* namespace gr */

