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
#include "set_ccc_master_impl.h"


bool flagx = false; 

namespace gr {
  namespace pmt_cpp {

    set_ccc_master::sptr
    set_ccc_master::make()
    {
      return gnuradio::get_initial_sptr
        (new set_ccc_master_impl());
    }

    /*
     * The private constructor
     */
    set_ccc_master_impl::set_ccc_master_impl()
      : gr::block("set_ccc_master",
              gr::io_signature::make(0,0,0),
              gr::io_signature::make(0,0,0))
    {
        message_port_register_in(pmt::mp("flag"));
        message_port_register_out(pmt::mp("ccc"));
        message_port_register_out(pmt::mp("signal"));
        time(&timer);
        set_msg_handler(pmt::mp("flag"), boost::bind(&set_ccc_master_impl::handle, this, _1));
        d_thread = new boost::thread(boost::bind(&set_ccc_master_impl::run, this, this));
        
    }

    /*
     * Our virtual destructor.
     */
    set_ccc_master_impl::~set_ccc_master_impl()
    {
        
	d_thread->interrupt();
	d_thread->join();
	delete d_thread;
    }
    void set_ccc_master_impl::run(set_ccc_master_impl* instance) {
        while(1){
            if(flagx) {
                time(&timer);
                flagx = false;
                //std::cout << "[SLAVE][SET CCC]: flag: "<< flag << std::endl;
            }
            //std::cout << "[SLAVE][SET CCC]: while " << std::endl;
            while(!flagx){
              time_t timer2;
              time(&timer2);
              double sec = difftime(timer2,timer);
              if(sec > 400){
                  message_port_pub(pmt::mp("ccc"), pmt::cons(pmt::mp("freq"),pmt::mp(6000000000)));
                  pmt::pmt_t p_dict  = pmt::make_dict();
                  p_dict = pmt::dict_add(p_dict, pmt::string_to_symbol("signal"), pmt::from_double(6));
                  message_port_pub(pmt::mp("signal"), p_dict);
                  time(&timer);
              }
              std::cout << "[SET CCC]: dif: "<< sec << std::endl;
              boost::this_thread::sleep(boost::posix_time::milliseconds(1000));
            }
        }
    }


    void set_ccc_master_impl::handle(pmt::pmt_t pdu) {
        //std::cout << "[SLAVE][SET CCC]: CHANGE FREG " << std::endl;
        flagx = true;
        //std::cout << "[SLAVE][SET CCC]: CHANGE flag: "<<flag << std::endl;
    }



  } /* namespace pmt_cpp */
} /* namespace gr */




