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
#include "start_share_impl.h"
#include "pmt_cpp/set_ccc.h"
#include <fstream>

namespace gr {
  namespace pmt_cpp {

    start_share::sptr
    start_share::make()
    {
      return gnuradio::get_initial_sptr
        (new start_share_impl());
    }

    
    /*
     * The private constructor
     */
    start_share_impl::start_share_impl()
      : gr::block("start_share",
              gr::io_signature::make(0,0,0),
              gr::io_signature::make(0,0,0))
    {
        message_port_register_out(pmt::mp("pmt::mp"));
        message_port_register_out(pmt::mp("bool")); 
        message_port_register_out(pmt::mp("testeRX"));
        pmt::pmt_t p_dict1 = pmt::make_dict(); /* Initiation of dictionary */

        p_dict1 = pmt::dict_add(p_dict1, pmt::string_to_symbol("share"), pmt::PMT_F);
        pmt::pmt_t sharet1 = pmt::PMT_NIL;
        sharet1 = pmt::dict_ref(p_dict1, pmt::string_to_symbol("share"), pmt::PMT_NIL);

        

        message_port_register_in(pmt::mp("pmt::dict"));
        set_msg_handler(pmt::mp("pmt::dict"), boost::bind(&start_share_impl::handle_msg, this, _1));
    }

    /*
     * Our virtual destructor.
     */
    start_share_impl::~start_share_impl()
    {
    }

    void start_share_impl::handle_msg(pmt::pmt_t msg) {
        
        std::cout <<"[SLAVE][SET NEW CONFIG] SHARE STARTED" << std::endl;
        
        srand (time(NULL));
        int time = std::rand()% 400000 + 100000;

        pmt::pmt_t nChannel = pmt::dict_ref(msg, pmt::string_to_symbol("nChannel"), pmt::PMT_NIL);
        double newChannel = pmt::to_double(nChannel);



        usleep(time);
        message_port_pub(pmt::mp("bool"), pmt::intern("<S:0:3:"+boost::to_string(newChannel/1e9)+">"));
	usleep(time);
        message_port_pub(pmt::mp("bool"), pmt::intern("<S:0:3:"+boost::to_string(newChannel/1e9)+">"));
	usleep(time);
        message_port_pub(pmt::mp("bool"), pmt::intern("<S:0:3:"+boost::to_string(newChannel/1e9)+">"));
	usleep(time);
        message_port_pub(pmt::mp("bool"), pmt::intern("<S:0:3:"+boost::to_string(newChannel/1e9)+">"));
        std::cout << "[SLAVE][SET NEW CONFIG]: MSG: " << "<S:0:3:"<<boost::to_string(newChannel/1e9)<<">"<< std::endl;
        message_port_pub(pmt::mp("testeRX"), pmt::intern("<S:0:3:"+boost::to_string(newChannel/1e9)+">"));
        std::cout << "[SLAVE][SET NEW CONFIG]:testeRX MSG: " << "<S:0:3:"<<boost::to_string(newChannel/1e9)<<">"<< std::endl;
        
        std::cout << "[SLAVE][SET NEW CONFIG]: nChannel: "<<pmt::to_double(nChannel)<< std::endl;
        //sleep(1.6);
        
        message_port_pub(pmt::mp("pmt::mp"), pmt::cons(pmt::mp("freq"), pmt::mp(pmt::to_double(nChannel))));


        usleep(1000000);



        std::fstream out; 
        out.open("/tmp/slave_channels.txt", std::ios::out | std::ios::app);
        if(out.is_open()){
            out << pmt::to_double(nChannel)<< std::endl;
            std::cout << "[SLAVE][SET NEW CONFIG]:SALVANDO "<< std::endl;
        }
        const char file_path[] = "/tmp/ack.txt";
        boost::filesystem::path file(file_path);
        boost::filesystem::remove(file);

                   
    }

  } /* namespace pmt_cpp */
} /* namespace gr */

