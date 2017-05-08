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
#include <gnuradio/blocks/bin_statistics_f.h>
#include "pmt_extract_impl.h"
#include "unistd.h"
//I'm trying to run two executables consecutively using this c code:
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <gnuradio/block_gateway.h>

namespace gr {
  namespace pmt_cpp {

    pmt_extract::sptr
    pmt_extract::make()
    {
      return gnuradio::get_initial_sptr
        (new pmt_extract_impl());
    }

    /*
     * The private constructor
     */
    pmt_extract_impl::pmt_extract_impl()
      : gr::block("pmt_extract",
              gr::io_signature::make(0,0,0),
              gr::io_signature::make(0,0,0))
    {
        message_port_register_out(pmt::mp("content"));
    	
    	message_port_register_in(pmt::mp("in_pdu"));
    	set_msg_handler(pmt::mp("in_pdu"), boost::bind(&pmt_extract_impl::handle_msg, this, _1));
    }

       void
    	pmt_extract_impl::handle_msg(pmt::pmt_t pdu)
        {
    	//gr::thread::scoped_lock guard(d_mutex);
           
           
          // add the field and publish
		pmt::pmt_t meta = pmt::car(pdu);
		pmt::pmt_t vector = pmt::cdr(pdu);
		
		if(pmt::is_null(meta)){
			meta = pmt::make_dict();
			} else if(!pmt::is_dict(meta)){
				throw std::runtime_error("pdu_remove received non PDU input");
		}
          //meta = pmt::dict_delete(meta, d_k);
		size_t offset(0);
		//Tamanho do PDU
		size_t len = pmt::length(vector);
		std::string lut = "0123456789:.,ABCDEFGHIJKLMNOPQRSTUVXZWYabcdefghijklmnopqrstuvxzwy<>";//66 caracteres
		int count = 0;
                char str[50];
		const uint8_t* d = (const uint8_t*) pmt::uniform_vector_elements(vector, offset);
		for(size_t i=0; i<len; i+=16){
			//printf("%04x: ", ((unsigned int)i));
			for(size_t j=i; j<std::min(i+16,len); j++){
				//printf("%02x ",d[j] );
				for (size_t x=0; x<66; x++){
					if (lut[x] == d[j]) {
						//std::cout <<d[j];
                                                str[count] = d[j];
                                                count++;
                                        
                                        }
				}
					
				//str[count] = (char) d[j];
				//count++;
				
				
			}
		}
                
                //
                size_t pos = 0;
                for(size_t i=0; i< 20; i++){
                    if(str[i] == ':'){
                        pos = i-4; //ex freq:2.4G
                    }
                }
                char command[4];
                char value[12];
                if (pos != 0){
                    
                    command[0] = str[pos];
                    command[1] = str[pos+1];
                    command[2] = str[pos+2];
                    command[3] = str[pos+3];
                    
                    size_t v = 0;
                    for(size_t i=pos+5; i< 50; i++){
                        if(str[i] != 'G' || str[i] != 'M'){
                            value[v] = str[i];
                            v++;
                        }
                    }
                }
                
                //std::string::size_type sz;     // alias of size_t
                
                //std::string orbits(values);
                char* pEnd;
                
                double valor = std::strtod (value,&pEnd);
                
                message_port_pub(pmt::mp("content"), pmt::cons(pmt::mp(command),pmt::mp(valor)));

        }
       
       
       
      
    

  } /* namespace pmt_cpp */
} /* namespace gr */

