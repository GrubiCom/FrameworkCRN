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
#include "send_file_ACK_impl.h"
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <boost/lexical_cast.hpp>
#include <sys/wait.h>
#include <stdlib.h>

/*
 * Bloco capaz de ler o conteudo gravado pelo bloco PDU_json e processar
 * todas as informacoes necessarias.
 */
namespace gr {
  namespace pmt_cpp {

    send_file_ACK::sptr
    send_file_ACK::make()
    {
      return gnuradio::get_initial_sptr
        (new send_file_ACK_impl());
    }

    /*
     * The private constructor
     */
    send_file_ACK_impl::send_file_ACK_impl()
      : gr::block("send_file",
              gr::io_signature::make(0,0,0),
              gr::io_signature::make(0,0,0))
    {
        message_port_register_out(pmt::mp("pdu"));      //Registra porta de saida pdu
    	
    	message_port_register_in(pmt::mp("file_ready"));//Registra porta de entrada file_ready
    	set_msg_handler(pmt::mp("file_ready"), boost::bind(&send_file_ACK_impl::trigger, this, _1));
        d_nmsg_left = 3;
        d_interval = 1000;
        d_finished = false;
    
    }

    /*
     * Our virtual destructor.
     */
    send_file_ACK_impl::~send_file_ACK_impl()
    {
    }
    void send_file_ACK_impl::trigger(pmt::pmt_t msg) {
        ready=pmt::to_bool(msg);
        
        
        std::cout <<"[SLAVE][FILE PREPROCESSOR]: STARTED"<< std::endl;
        //sleep(3); 05/10/15 20 horas
        
        double  avg = 0;
        double cont = 0;
        bool start = true;
        char*  sz;
        if(!ready){
            std::ifstream file; // open file
            file.open("/tmp/sense.txt");
            if (file.is_open()){
                std::string line, freq, power, freqAnt, send,time, time2;

                while(!file.eof()){
                    getline(file,line);
                    int pos0,pos1;
                    pos0 = line.find(":");
                    pos1 = line.find(":", pos0+2);                 
                    time = line.substr(0,pos0);
                    freq = line.substr(pos0+1,(pos1-pos0-2));
                    power = line.substr(pos1+1);
                    
                  if (freq.compare("6000000000.0")!= 0){
   
			  if (start){
		                time2=time;                       
		                freqAnt = freq;
		                avg = std::strtod(power.c_str(),&sz);


		                if(avg < -130 ){
		                    avg = -50;

		                }
		                cont++;
		                start = false;
		            }else{

		                if (freqAnt.compare(freq) == 0){

		                    double tod = std::strtod(power.c_str(),&sz);

		                    if (tod > avg ) {

		                        avg = tod;

		                        time2=time;                           
		                    }                       
		                    freqAnt = freq;
		                    cont++;
		                }else {

		                    double t = std::atof(freqAnt.c_str())/(double)1.0e9;

		                    std::ostringstream ss;
		                    ss << time2;
		                    send.append(ss.str());
		                    send.append(":");
		                    std::ostringstream sstream;
		                    sstream << t;
		                    send.append(sstream.str());

		                    send.append(":");
		                    send.append(boost::lexical_cast<std::string>(avg));
		                    send.append(";");


		                    avg = 0;
		                    avg += std::strtod(power.c_str(),&sz);


		                    freqAnt = freq;
		                    time2 = time;
		                    cont = 0;
		                }
		            }
			}
                }

                file.close();
                std::remove("/tmp/ack.txt"); //remove o arquivo do disco


                
                std::ofstream out;
                out.open("/tmp/send.txt");
                if(out.is_open()){
                    out <<"1:"<< send.length() <<";"<< std::endl;
                   
                    int offset = 45;
                    int msg = 2;
                    for(int i = 0; i <= send.length();i+=45){
                        
                        std::string swap = boost::lexical_cast<std::string>( msg );
                        out <<swap<< ":"+send.substr(i,offset) << std::endl;
                        msg++;
                    }
                    out.close();
                    pmt::pmt_t p_dict1  = pmt::make_dict();                                         //Cria dicionario vazio
                    p_dict1 = pmt::dict_add(p_dict1, pmt::string_to_symbol("sense"), pmt::PMT_T);   //Cria (chave=sense,valor=false)
                    p_dict1 = pmt::dict_add(p_dict1, pmt::string_to_symbol("acks_total"), pmt::from_long(msg));



                    sleep(0.2);
                    message_port_pub(pmt::mp("pdu"), p_dict1); 
                   
                }else{
                std::cerr << "[SLAVE][FILE PREPROCESSOR]:file /tmp/send.txt don't exist" << std::endl;
                std::exit(-1);
            }

            }else{
                std::cerr << "[SLAVE][FILE PREPROCESSOR]: file /tmp/sense.txt don't exist" << std::endl;
                std::exit(-1);
            }
        }
    }

    void send_file_ACK_impl::send() {
        pmt::pmt_t p_dict1  = pmt::make_dict();                                         //Cria dicionario vazio
        p_dict1 = pmt::dict_add(p_dict1, pmt::string_to_symbol("file"), pmt::PMT_T);   //Cria (chave=sense,valor=false)
        pmt::pmt_t senset1 = pmt::PMT_NIL;                                              //Cria pmt nulo
        senset1 = pmt::dict_ref(p_dict1, pmt::string_to_symbol("file"), pmt::PMT_NIL); //Senset1 recebe a flag sense


        message_port_pub(pmt::mp("pdu"), senset1); 
        }

    
    
    /* handle_msg
     * \param msg booleano
     */
    void send_file_ACK_impl::handle_msg() {
        
        
            
        
    }

  } /* namespace pmt_cpp */
} /* namespace gr */

