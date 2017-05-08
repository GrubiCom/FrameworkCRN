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
#include "time_transmission_cycle_impl.h"
#include <fstream>
bool frag = false; 

namespace gr {
  namespace pmt_cpp {

    time_transmission_cycle::sptr
    time_transmission_cycle::make()
    {
      return gnuradio::get_initial_sptr
        (new time_transmission_cycle_impl());
    }

    /*
     * The private constructor Nao precisa ser thread
     */
    time_transmission_cycle_impl::time_transmission_cycle_impl()
      : gr::block("time_transmission_cycle",
              gr::io_signature::make(0,0,0),
              gr::io_signature::make(0,0,0))
    {
        message_port_register_in(pmt::mp("in_signal"));
        message_port_register_out(pmt::mp("out_signal"));
        time(&timer);
        set_msg_handler(pmt::mp("in_signal"), boost::bind(&time_transmission_cycle_impl::handle, this, _1));

    
    }

    /*
     * Our virtual destructor.
     */
    time_transmission_cycle_impl::~time_transmission_cycle_impl()
    {
    }

    

    void time_transmission_cycle_impl::run(time_transmission_cycle_impl* instance) {
        /*while(1){
            if(frag) {
                time(&timer);
                frag = false;
                std::cout << "[MASTER][TIME TRASNMISSION CYCLE]: flag: "<< frag << std::endl;
            }
            std::cout << "[MASTER][TIME TRASNMISSION CYCLE]: while " << std::endl;
            while(!frag){
              time_t timer2;
              time(&timer2);
              double sec = difftime(timer2,timer);
              if(sec > 40){
                  message_port_pub(pmt::mp("out_signal"), pmt::intern("signal"));
                  time(&timer);
              }
              std::cout << "[MASTER][TIME TRASNMISSION CYCLE]: dif: "<< sec << std::endl;
              boost::this_thread::sleep(boost::posix_time::milliseconds(2000));
            }
        }
         */
    }


    void time_transmission_cycle_impl::handle(pmt::pmt_t pdu) {
        time(&timer);
        time_t timer2;
        time(&timer2);
        double sec = difftime(timer2,timer);
        while(sec < 60){
              time_t timer2;
              time(&timer2);
              sec = difftime(timer2,timer);
              std::cout << "[MASTER][TIME TRASNMISSION CYCLE]: dif: "<< sec << std::endl;
              sleep(1);
        }
        std::ifstream file; // open file
        file.open("/tmp/master_channels.txt");
            if (file.is_open()){
                std::string line;
                getline(file,line);
                std::stringstream ss(line);
                double channel;
                ss >> channel;
                pmt::pmt_t p_dict  = pmt::make_dict();

                p_dict = pmt::dict_add(p_dict, pmt::string_to_symbol("signal"), pmt::from_double(channel));
                message_port_pub(pmt::mp("out_signal"), p_dict);
                std::cout << "[MASTER][TIME TRASNMISSION CYCLE]: channel "<<channel<< std::endl;
            }
        std::cout << "[MASTER][TIME TRASNMISSION CYCLE]: FINISH "<< std::endl;
    }

  } /* namespace pmt_cpp */
} /* namespace gr */

