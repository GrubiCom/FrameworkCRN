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
#include "message_generation_impl.h"
#include <dirent.h>
#include <fstream>

#define dout true && std::cout

namespace gr {
  namespace pmt_cpp {

    message_generation::sptr
    message_generation::make()
    {
      return gnuradio::get_initial_sptr
        (new message_generation_impl());
    }

    /*
     * The private constructor Arrumar o ciclo
     */
    message_generation_impl::message_generation_impl()
      : gr::block("message_generation",
              gr::io_signature::make(0,0,0),
              gr::io_signature::make(0,0,0))
    {
        d_finished = true;
        new_freq = 6;
        old_freq = 6;
        cycle = 0;
        init = 0;
        count = 0;
        neighbors_msg = false;
        d_interval = 120000;//30000; // 100 minutos 642026 10 minutos   240000 s
        d_nmsg_left = (int)4e9;//Virtualmente infinito
        //d_msg = pmt::intern("<0:2:0,8:2,8>");
	message_port_register_out(pmt::mp("msg"));
        message_port_register_out(pmt::mp("mp"));
        message_port_register_in(pmt::mp("signal"));
        gain = 50;
        
	d_thread = new boost::thread(boost::bind(&message_generation_impl::run, this, this));
        set_msg_handler(pmt::mp("signal"), 
                boost::bind(&message_generation_impl::set_de_finished, 
                this, _1));    
    }

    /*
     * Our virtual destructor.
     */
    message_generation_impl::~message_generation_impl(){
        gr::thread::scoped_lock(d_mutex);

	d_finished = true;
	d_thread->interrupt();
	d_thread->join();
	delete d_thread;
    }

    void message_generation_impl::set_de_finished(pmt::pmt_t pdu) {
        
        pmt::pmt_t key = pmt::dict_ref(pdu, pmt::string_to_symbol("signal"), pmt::PMT_NIL);
        old_freq = new_freq;
        if(cycle >= 5){
            //new_freq = 0;
            cycle = 0;
        }
        new_freq = pmt::to_double(key);
        
        if(old_freq == 0){
            old_freq = new_freq;
        }
        d_finished = true;
        //std::cout << "[MASTER][MESSAGE GENERATION]: new freq: "<<new_freq << " Old freq: "<<old_freq<< std::endl;
    }
    void message_generation_impl::send_sense() {
        std::string filename = "/tmp/neighbors.txt";
        std::string line;
        std::ifstream file;
        double variation = 0.3;
        file.open(filename.c_str());
        //std::cout << "[MASTER][MESSAGE GENERATION]: new freq-: "<<boost::to_string(new_freq-variation) << " freq: "<<new_freq<< std::endl;
        //std::cout << "[MASTER][MESSAGE GENERATION]: new freq+: "<<boost::to_string(new_freq+variation)<< std::endl;
        //std::cout << "[MASTER][MESSAGE GENERATION]: new freq: "<<boost::to_string(new_freq)<< std::endl;
        dif = 0;
        min = 0;
        max = 0;
        if (file.is_open()){
            while(getline(file,line)){
                if(true){//cycle == 0){
                    d_msg = pmt::intern("<"+line+":2:0.8:5.8>");
                    std::cout << pmt::symbol_to_string(d_msg);
                    message_port_pub( pmt::mp("msg"), d_msg );
                    usleep(200000);

                }else{
                    
                    min = new_freq-variation;
                    max = new_freq+variation;
                    if ( min < 0.8){
                        dif = 0.8 - min;
                        min = 0.8;
                        max = max + dif;
                    }
                    if(max > 5.8){
                        dif = max - 5.8;
                        max = 5.8;
                        min = std::abs(min - dif);
                    }
                    d_msg = pmt::intern("<"+line+":2:"+boost::to_string(min)+":"+boost::to_string(max)+">");
                    std::cout << "<"+line+":2:"+boost::to_string(min)+":"+boost::to_string(max)+">" << std::endl;
                    message_port_pub( pmt::mp("msg"), d_msg );
                    usleep(200000);
                }
            }
        }
        
        
        file.close();
    }

    void message_generation_impl::run(message_generation_impl* instance) {
	try {

	// flow graph startup delay
	boost::this_thread::sleep(boost::posix_time::milliseconds(500));

	while(1) {
		float delay = 500;
		
		{
                        if(count> 10){
                            exit(1);
                        }
                        
			gr::thread::scoped_lock(d_mutex);
			
			//if(d_finished || !d_nmsg_left) {
				//d_finished = true;				
				//break;
			//}
                        
                        if(!neighbors_msg && d_finished){
                            
                            std::cout<< "[MASTER][MESSAGE GENERATION]: Send neighbors discovery" << std::endl;
                            //rmdir("/tmp/Acknowledgement");      
                            int b ;//= std::system("rm -rf /tmp/results/" );
                            b = std::system("rm -rf /tmp/Acknowledgement/" );
                            remove("/tmp/neighbors.txt");
                            remove("/tmp/neighbors_aux.txt");
                            //remove("/tmp/master_channels.txt");
                            remove("/tmp/acks_sense.txt");
                            
                            for (int i = 0; i < 10; i++){
                                usleep(200000);
                                message_port_pub(pmt::mp("msg"), pmt::intern("<0:0>"));//<Broadcast:ID_MSG>
                            }
                            
                            
                            //std::fstream file;
                            //sleep(2);
                            std::string filename = "/tmp/neighbors.txt";
                            
                            if(boost::filesystem::exists(filename)){
				    
                                neighbors_msg = true;  
				
                            }else {
				    
                                std::cout << "[MASTER][MESSAGE GENERATION]: Repeat Send Neighbors Discovery with gain: "<<gain << std::endl;
                                if (gain < 58){
                                    gain+=1;
                                }
                                //message_port_pub(pmt::mp("mp"), pmt::cons(pmt::mp("gain"),pmt::mp(gain)));
                                std::cout << "[MASTER][MESSAGE GENERATION]: tuned CCC 6GHz" << std::endl;
                                message_port_pub(pmt::mp("mp"), pmt::cons(pmt::mp("freq"),pmt::mp(6000000000)));
				
                                for (int i = 0; i < 5; i++){
                                    usleep(200000);
                                    message_port_pub(pmt::mp("msg"), pmt::intern("<0:0>"));//<Broadcast:ID_MSG>
                                }
                                
                                if(init != 0){
                                    std::cout << "[MASTER][MESSAGE GENERATION]: tuned old freq "<<new_freq*1e9<< std::endl;
                                    message_port_pub(pmt::mp("mp"), pmt::cons(pmt::mp("freq"),pmt::mp(new_freq*1e9)));
                                }
                                
                                if(boost::filesystem::exists(filename)){
                                    
                                    neighbors_msg = true;
                                }
                               
                            }
                            
                            
                        }else if (d_finished){
                           
                            
                            init = 1;
                            int j = 0;
                            do{ 
                                if(init != 0){
                                    std::cout << "[MASTER][MESSAGE GENERATION]: tuned old freq "<<new_freq*1e9<< std::endl;
                                    message_port_pub(pmt::mp("mp"), pmt::cons(pmt::mp("freq"),pmt::mp(new_freq*1e9)));
                                    usleep(200000);
                                }
                                send_sense();

                                //gain = 58;

                                std::cout << "[MASTER][MESSAGE GENERATION]: tuned CCC 6GHz" << std::endl;
                                message_port_pub(pmt::mp("mp"), pmt::cons(pmt::mp("freq"),pmt::mp(6000000000)));
                                //message_port_pub(pmt::mp("mp"), pmt::cons(pmt::mp("gain"),pmt::mp(gain)));
                                for (int i = 0; i < 5; i++){
                                    usleep(200000);
                                    message_port_pub(pmt::mp("msg"), pmt::intern("<0:0>"));//<Broadcast:ID_MSG>
                                }

                                send_sense();
                                //usleep(2000000);
                                j++;
                            }while(!boost::filesystem::exists("/tmp/acks_sense.txt") && j<5);
                            if(j > 4) {
                                d_finished = true; 
                            }
                            //d_nmsg_left--;
                            neighbors_msg = false;
                            d_finished = false;
                            //}
                            cycle++;
                            count++;
                        }        
                        
		}
		boost::this_thread::sleep(boost::posix_time::milliseconds(delay));
	} 

	} catch(boost::thread_interrupted) {
		gr::thread::scoped_lock(d_mutex);
		dout << "PMS: thread interrupted" << std::endl;
		//d_finished = true;
		
	}
        
    }
    


    void message_generation_impl::set_delay(float delay) {
	gr::thread::scoped_lock(d_mutex);
	d_interval = delay;
    }

    float message_generation_impl::get_delay() {
	gr::thread::scoped_lock(d_mutex);
	return d_interval;
    }


    void message_generation_impl::start_tx() {
	gr::thread::scoped_lock(d_mutex);

	if(is_running()) return;

	
	d_finished = false;
	d_thread->join();
	delete d_thread;

	d_thread = new boost::thread(boost::bind(&message_generation_impl::run, this, this));
    }

    void message_generation_impl::stop_tx() {
	d_thread->interrupt();
    }

    bool message_generation_impl::is_running() {
	return !d_finished;
    }

  } /* namespace pmt_cpp */
} /* namespace gr */


