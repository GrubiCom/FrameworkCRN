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
#include "Noise_impl.h"

namespace gr {
  namespace pmt_cpp {

    Noise::sptr
    Noise::make()
    {
      return gnuradio::get_initial_sptr
        (new Noise_impl());
    }

    /*
     * The private constructor
     */
    Noise_impl::Noise_impl()
      : gr::block("Noise",
              gr::io_signature::make(0,0,0),
              gr::io_signature::make(0,0,0))
    {
        
        message_port_register_out(pmt::mp("mp"));

	d_thread = new boost::thread(boost::bind(&Noise_impl::run, this, this));
    }
    /*
     * Our virtual destructor.
     */
    Noise_impl::~Noise_impl()
    {
        gr::thread::scoped_lock(d_mutex);

	
	d_thread->interrupt();
	d_thread->join();
	delete d_thread;
    }

    void Noise_impl::run(Noise_impl* instance) {
	try {

	// flow graph startup delay
	boost::this_thread::sleep(boost::posix_time::milliseconds(500));

	while(1) {
		float delay = 500;
		{
			gr::thread::scoped_lock(d_mutex);
			
                    for (int i = 80; i <= 300; i+=2){ //pula de 10MHz
                    
                        message_port_pub(pmt::mp("mp"), pmt::cons(pmt::mp("freq"),pmt::mp(i*1e7)));    //envia a nova frequencia para a placa USRP
                        usleep(2000000);//Sleep de 1 segundo
                }
                        
		}
		boost::this_thread::sleep(boost::posix_time::milliseconds(delay));
	} 

	} catch(boost::thread_interrupted) {
		gr::thread::scoped_lock(d_mutex);
		std::cout << "PMS: thread interrupted" << std::endl;
		
		
	}
        std::cout << "FINAL" << std::endl;
    }
    


    


    

  } /* namespace pmt_cpp */
} /* namespace gr */

