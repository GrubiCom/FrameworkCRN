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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include <gnuradio/block_detail.h>
#include <string.h>
#include "message_type_impl.h"

namespace gr {
  namespace pmt_cpp {

    message_type::sptr
    message_type::make()
    {
      return gnuradio::get_initial_sptr
        (new message_type_impl());
    }

    /*
     * The private constructor
     */
    message_type_impl::message_type_impl()
      : gr::block("message_type",
              gr::io_signature::make(0,0,0),
              gr::io_signature::make(0,0,0))
    {
        message_port_register_out(pmt::mp("out"));

	d_thread = new boost::thread(boost::bind(&message_type_impl::run, this, this));
    }

    message_type_impl::~message_type_impl(){
        
    }
    
    void
    message_type_impl::run(message_type_impl *instance) {

	try {

	// flow graph startup delay
	boost::this_thread::sleep(boost::posix_time::milliseconds(500));
        int i = 0;
        bool master = false, sense = false, share = false;
        
	while(1) {
		
		{
			gr::thread::scoped_lock(d_mutex);
			if (!master){
                            message_port_pub( pmt::mp("out"), pmt::intern("master"));
                            master = true;
                        }
                        
			std::cout << "PMS: number of messages left: " <<i<< std::endl;
                        i++;
			message_port_pub( pmt::mp("out"), pmt::intern("Hello World!"));
                        
			
		}
		boost::this_thread::sleep(boost::posix_time::milliseconds(500));
	} 

	} catch(boost::thread_interrupted) {
		gr::thread::scoped_lock(d_mutex);
		std::cout << "PMS: thread interrupted" << std::endl;
		
			boost::this_thread::sleep(boost::posix_time::milliseconds(500));
			post(pmt::mp("system"), pmt::cons(pmt::mp("done"), pmt::from_long(1)));
		
	}
    }
    
    
    
    
    void message_type_impl::set_nmsg(int nmsg){
          
    }
    int message_type_impl::get_nmsg(){
            
    }

    void message_type_impl::set_delay(float delay){
            
    }
    float message_type_impl::get_delay(){
        
    }
    void
    message_type_impl::start_tx() {
	gr::thread::scoped_lock(d_mutex);

	if(is_running()) return;

	
	d_thread->join();
	delete d_thread;

	d_thread = new boost::thread(boost::bind(&message_type_impl::run, this, this));
    }

    void
    message_type_impl::stop_tx() {
	d_thread->interrupt();
    }

    bool
    message_type_impl::is_running() {
	return true;
    }


  } /* namespace pmt_cpp */
} /* namespace gr */

