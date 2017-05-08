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
#include "time_impl.h"
#include <fstream>
#include <dirent.h>
#include <cstdlib>
#include <iostream>
#include <string>

namespace gr {
  namespace pmt_cpp {

    time::sptr
    time::make()
    {
      return gnuradio::get_initial_sptr
        (new time_impl());
    }

    /*
     * The private constructor
     */
    time_impl::time_impl()
      : gr::block("time",
              gr::io_signature::make(0,0,0),
              gr::io_signature::make(0,0,0))
    {
        message_port_register_in(pmt::mp("Ack"));
        set_msg_handler(pmt::mp("Ack"), boost::bind(&time_impl::handle_msg, this, _1));
        message_port_register_out(pmt::mp("Ack_repeat"));
        message_port_register_out(pmt::mp("id_neighbor"));
        message_port_register_out(pmt::mp("Feed_back"));
    }

    /*
     * Our virtual destructor.
     */
    time_impl::~time_impl()
    {
    }
    void time_impl::handle_msg(pmt::pmt_t msg) {
        if(pmt::is_dict(msg)){

            

            pmt::pmt_t ack =  pmt::dict_ref(msg, pmt::string_to_symbol("ack"), pmt::PMT_NIL);
            pmt::pmt_t a_t =  pmt::dict_ref(msg, pmt::string_to_symbol("acks_total"), pmt::PMT_NIL);
            pmt::pmt_t id =  pmt::dict_ref(msg, pmt::string_to_symbol("id"), pmt::PMT_NIL);
            
            long number = pmt::to_long(ack);
            
            long acks_total = pmt::to_long(a_t); 

            std::string id1 = pmt::symbol_to_string(id);

            std::string line;
            std::ifstream file; // open file

            std::string filename = "/tmp/Acknowledgement/acks";
            filename.append(id1);

            filename.append(".txt");
            
            file.open(filename.c_str());
            
            bool found = false;
            while(getline(file,line)){              
                if(std::atoi(line.c_str()) == (number+1)){
                  found = true;            
                }
            }
            file.close();
            if(!found && ((number+1)<acks_total)){
                std::cout << "[MASTER][TEMPORIZE ACK]: Enviando Do Time:  "<< "<A:"<<boost::to_string(id1)<<":"<<boost::to_string(number+1)<<">" << std::endl;

                message_port_pub(pmt::mp("Ack_repeat"), pmt::intern("<A:"+boost::to_string(id1)+":"+boost::to_string(number+1)+">")); 
                usleep(200000);
                message_port_pub(pmt::mp("Feed_back"),msg);
            }else if(number +1 >= acks_total){
                std::cout << "[MASTER][TEMPORIZE ACK]: FINISH ID " << id1 << std::endl;
                sleep(1);
                //remove(filename.c_str());
                
                
                
        

                
                
                pmt::pmt_t p_dict  = pmt::make_dict();
                p_dict = pmt::dict_add(p_dict, pmt::string_to_symbol("ID"), pmt::string_to_symbol(id1));
                message_port_pub(pmt::mp("id_neighbor"),p_dict);
            }
            //std::cout << "time final" << std::endl;
            
        }
    }
    
    
    


  } /* namespace pmt_cpp */
} /* namespace gr */

