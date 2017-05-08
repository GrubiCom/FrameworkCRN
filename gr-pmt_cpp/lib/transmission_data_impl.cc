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
#include "transmission_data_impl.h"
#include <ctime>
#include <fstream>

#include <boost/date_time/posix_time/time_formatters.hpp>
#include <boost/date_time/posix_time/time_parsers.hpp>
namespace gr {
  namespace pmt_cpp {

    transmission_data::sptr
    transmission_data::make()
    {
      return gnuradio::get_initial_sptr
        (new transmission_data_impl());
    }

    /*
     * The private constructor
     */
    transmission_data_impl::transmission_data_impl()
      : gr::block("transmission_data",
              gr::io_signature::make(0,0,0),
              gr::io_signature::make(0,0,0))
    {
      message_port_register_in(pmt::mp("signal_in"));
      set_msg_handler(pmt::mp("signal_in"),boost::bind(&transmission_data_impl::handle, this, _1));
      
      
      
      message_port_register_out(pmt::mp("packet"));
      message_port_register_out(pmt::mp("signal_out"));
      message_port_pub(pmt::mp("signal_out"),pmt::from_bool(false));
      d_power = 0;
      
      
    }

    /*
     * Our virtual destructor.
     */
    transmission_data_impl::~transmission_data_impl()
    {
    }
    

    void transmission_data_impl::handle(pmt::pmt_t pdu) {
        
        usleep(2000000);
        time_t timer1= time(0);
        time_t t2 = time(0);
        time(&timer1);
        //time(&timer2);
        time(&t2);
        double dif = difftime(t2,timer1);
        int i = 0;
        int a = 0;


        std::string data = "00011110000000000000000000000000000000000000000000";
        int time_sleep = 8000;//std::rand()%  100000 + 50000;
        char idUsrp = '4';
        while(dif < 60){
            srand (time(NULL));
            int dif_interval = std::rand()%  5 + 3;
            if((int)dif % dif_interval == 0 || ((int)dif < 3)){
                d_power = get_power();               
            }          
            if(d_power < -90){               
               
                i++;                
                std::string filename = "/tmp/neighbors_slave.txt";
                std::ifstream file;
                file.open(filename.c_str());
                std::string line;
                getline(file,line);               
                boost::posix_time::ptime t;  
                
                if(line.empty()){
                    

                    
                    usleep(time_sleep);
                    boost::posix_time::ptime t;            
                    t = boost::posix_time::microsec_clock::local_time();
                    std::string s = boost::posix_time::to_iso_string(t);
                      
                    message_port_pub(pmt::mp("packet"), pmt::intern("<"+boost::to_string('0')+":4:"+idUsrp+":"+boost::to_string(i)+":"+data+":"+boost::to_string(s)+">"));
                    std::cout <<"[SLAVE][TRANSMISSION DATA]: 1" <<std::endl;
                                             
                }else{

                    
                    usleep(time_sleep);
                    boost::posix_time::ptime t;            

                    t = boost::posix_time::microsec_clock::local_time();
                    std::string s = boost::posix_time::to_iso_string(t);

                    std::cout <<"[SLAVE][TRANSMISSION DATA]: 2" <<std::endl;
                    message_port_pub(pmt::mp("packet"), pmt::intern("<"+boost::to_string('0')+":4:"+idUsrp+":"+boost::to_string(i)+":"+data+":"+boost::to_string(s)+">"));
                }
                std::ifstream arq;
                
                std::string cu;
                
                bool achou = false;
                while(!achou && dif < 60){

                    arq.open("/tmp/time.txt");
                    while(getline(arq,cu)){

                        if(std::atoi(cu.c_str()) == i){
                            achou = true;
                        }
                    }
                    if (!achou){
                        srand (time(NULL));
                        int dif_interval = (std::rand() %  5) + 3;
                        std::cout <<"[SLAVE][TRANSMISSION DATA]: dif_inteval: "<<dif_interval <<std::endl;
                         if((int)dif % 2 == 0 ){
                            d_power = get_power();
                            std::cout <<"[SLAVE][TRANSMISSION DATA]: d_power: "<<d_power <<std::endl;
                        } 
                        if (d_power < -90){


                            usleep(time_sleep);
                            a++;
                            boost::posix_time::ptime t1;
                            t1 = boost::posix_time::microsec_clock::local_time();
                            std::string s = boost::posix_time::to_iso_string(t1);
                            std::cout <<"[SLAVE][TRANSMISSION DATA]: 3" <<std::endl;
                            message_port_pub(pmt::mp("packet"), pmt::intern("<"+boost::to_string('0')+":4:"+idUsrp+":"+boost::to_string(i)+":"+data+":"+boost::to_string(s)+">"));

                            
                        }else{
                            std::cout <<"[SLAVE][TRANSMISSION DATA]: BUSY CHANNEL>> "<<d_power <<std::endl;

                            srand (time(NULL));
                            int time_sleep_power = std::rand()%  13000 + 9000;
                            usleep(time_sleep_power);

                        }
                    } 
                    arq.close();
                    time(&t2);
                    dif = difftime(t2,timer1);    

                }
                
                file.close();
            }else{
                std::cout <<"[SLAVE][TRANSMISSION DATA]: BUSY CHANNEL:: "<<d_power <<std::endl;
                srand (time(NULL));
                int time_sleep_power = std::rand()%  13000 + 9000;
                usleep(time_sleep_power);
                
            }
            time(&t2);
            dif = difftime(t2,timer1);
            
        }
        i=i+a;
        std::cout <<"[SLAVE][TRANSMISSION DATA]: FINISH" <<std::endl;
        std::fstream out; 
        out.open("/tmp/number_transmission_for_cycle.txt", std::ios::out | std::ios::app);
        if(out.is_open()){
            out << i<< std::endl;
            //std::cout << "[MASTER][MESSAGE PARSER]:SALVANDO "<< std::endl;
        }
        out.close();
        i = 0;
        
    }

    
    double transmission_data_impl::get_power(){
        message_port_pub(pmt::mp("signal_out"),pmt::from_bool(true));
        usleep(35000);
        message_port_pub(pmt::mp("signal_out"),pmt::from_bool(false));
        std::fstream file;
        std::string line,line_p;
        file.open("/tmp/power.txt",  std::ios::in);
        while(getline(file,line)) line_p = line;
        file.close();

        int pos = line_p.find_last_of(":");
        return std::atof(line_p.substr(pos+1).c_str());
    }

  } /* namespace pmt_cpp */
} /* namespace gr */

