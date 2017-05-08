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
#include "decide_impl.h"
#include <fstream>

namespace gr {
  namespace pmt_cpp {

    decide::sptr
    decide::make()
    {
      return gnuradio::get_initial_sptr
        (new decide_impl());
    }

    /*
     * The private constructor
     */
    decide_impl::decide_impl()
      : gr::block("decide",
              gr::io_signature::make(0,0,0),
              gr::io_signature::make(0,0,0))
    {
        message_port_register_out(pmt::mp("pmt::freq"));
        
        message_port_register_in(pmt::mp("pmt::in"));
        
        set_msg_handler(pmt::mp("pmt::in"), boost::bind(&decide_impl::handle_msg, this, _1));
        
    }
    
    void decide_impl::handle_msg(pmt::pmt_t msg) {

        if(pmt::is_bool(msg) && pmt::to_bool(msg)){
            std::ifstream file; // open file
            file.open("../res_sense.txt");
            std::string messageInput;// = pmt::symbol_to_string(msg); /* Passa a mensagem chegada para um tipo String */
            getline(file,messageInput);
            
            int atualPower;
            int power = 0;
            char cursor;
            char freqVector[12];
            char powerVector[4];
            char freq[12];
            int index = 0;

            while(messageInput[index] != 0) {
                for(int i = 0; i < 12; i++) {
                    if(i < 4) { powerVector[i] = 0; }
                    freqVector[i] = 0;
                }
                for(int i = 0; i < 12; i++) {
                    cursor = messageInput[index];
                    index++;
                    if(cursor == ':') {
                        i = 12;
                    }
                    else {
                        freqVector[i] = cursor;
                    }
                }
                index ++; /* O sinal de negativo */
                for(int i = 0; i < 4; i++) {
                    cursor = messageInput[index];
                    index++;
                    if(cursor == ';') {
                        i = 4;
                    }
                    else {
                        powerVector[i] = cursor;
                    }
                }          

                atualPower = convertStringToInt(powerVector);
                
                if(atualPower > power) {
                        strcpy(freq, freqVector);
                        power = atualPower;
                }


            }
            char freqFinal[15];
            freqFinal[0] = '<';
            freqFinal[1] = '0';
            freqFinal[2] = ':';
            freqFinal[3] = '3';
            freqFinal[4] = ':';
            for(int i = 5; i < 15; i++) {
                freqFinal[i] = 0;
            }
            for(int i = 5; i < 15; i++) {
                if(freq[i-5] == 0) {
                    freqFinal[i] = '>';
                    i = 15;
                }
                freqFinal[i] = freq[i-5];
            }
            pmt::pmt_t pmt_freq = pmt::intern(freqFinal);

            //message_port_pub(pmt::mp("pmt::freq"), pmt_freq);
            ////std::cout << "freqFinal: "<<freqFinal<<std::endl; 
            //std::cout << "std::atoi(freqFinal): "<<std::atoi(freqFinal)<<std::endl;
            //std::cout << "boost::to_string(std::atoi(freqFinal)/1e9)"<<boost::to_string(std::atoi(freqFinal)/1e9)<<std::endl;
            
            message_port_pub(pmt::mp("pmt::freq"),pmt::intern(freqFinal));
                       
        }
    }
    
    long int decide_impl::convertStringWithPoinToInt(char number[]) {
	long int result = 0;
	int high = 0;
	int convertido;
	int middle = 0;
	for(int i = 0; i < 12; i++) {
		if((int)number[i] == 46) {
				middle = i;
		}
		if(number[i] < 45 || number[i] > 60) {
			i = 12;
		}
		high++;
	}
	high --;
	high --;
        if (middle == 0) {
            high++;
            middle = high;
        }
	for(int i = 0; i < middle; i++) {
		convertido = ((int)number[i] - 48); 
                std::cout << "Convertido: " << convertido << std::endl;
		result += pow(10,(9 + middle - i)) * convertido;
	}	
	for(int i = middle + 1; i <= high; i++) {
		convertido = ((int)number[i] - 48); 
		result += pow(10,(9 - i + middle + 1)) * convertido;
	}	
	return result;
    }
    
    int decide_impl::convertStringToInt(char number[]) { /* Coloquei esse decide por último */
	long int result = 0;
	int high = 0;
	int convertido;
	for(int i = 0; i < 4; i++) {
		if(number[i] < 48 || number[i] > 60) {
			i = 4;
		}
		high++;
	}
	high --;
	high --;
	for(int i = high; i >= 0; i--) {
		convertido = ((int)number[i] - 48); 
		result += pow(10,(high - i)) * convertido;
	}	
	return result;
    }

    /*
     * Our virtual destructor.
     */

  } /* namespace pmt_cpp */
} /* namespace gr */

