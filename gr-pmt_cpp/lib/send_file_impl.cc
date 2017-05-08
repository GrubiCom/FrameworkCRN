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
#include "send_file_impl.h"
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <boost/lexical_cast.hpp>

/*
 * Bloco capaz de ler o conteudo gravado pelo bloco PDU_json e processar
 * todas as informacoes necessarias.
 */
namespace gr {
  namespace pmt_cpp {

    send_file::sptr
    send_file::make()
    {
      return gnuradio::get_initial_sptr
        (new send_file_impl());
    }

    /*
     * The private constructor
     */
    send_file_impl::send_file_impl()
      : gr::block("send_file",
              gr::io_signature::make(0,0,0),
              gr::io_signature::make(0,0,0))
    {
        message_port_register_out(pmt::mp("pdu"));      //Registra porta de saida pdu
    	
    	message_port_register_in(pmt::mp("file_ready"));//Registra porta de entrada file_ready
    	set_msg_handler(pmt::mp("file_ready"), boost::bind(&send_file_impl::handle_msg, this, _1));
    
    }

    /*
     * Our virtual destructor.
     */
    send_file_impl::~send_file_impl()
    {
    }
    /* handle_msg
     * \param msg booleano
     */
    void send_file_impl::handle_msg(pmt::pmt_t msg) {
        ready=pmt::to_bool(msg);
        std::cout << ready << "send_file" << std::endl;
        std::string line, freq, power, freqAnt, send;
        std::istringstream delim(":");
        double  avg = 0;
        double cont = 0;
        bool start = true;
        char*  sz;
        /*Se arquivo pronto entao podemos ler*/
        if(!ready){
            std::ifstream file; // open file
            file.open("/tmp/sense.txt");
            if (file.is_open()){
                while(!file.eof()){
                    getline(file,line);
                    int pos;
                    pos = line.find(":");
                    freq = line.substr(0,pos-2);
                    power = line.substr(pos+1);
                    if (start){
                        avg = std::strtod(power.c_str(),&sz);
                        freqAnt = freq;
                        cont++;
                        start = false;
                    }else{
                        if (!freqAnt.compare(freq)){
                            if (std::strtod(power.c_str(),&sz) > avg) {
                                avg = std::strtod(power.c_str(),&sz);
                            }                       
                        freqAnt = freq;
                        cont++;
                        }else {
                            send.append(freqAnt);
                            send.append(":");
                            send.append(boost::lexical_cast<std::string>(avg));
                            send.append(";");
                            

                            avg = 0;
                            avg += std::strtod(power.c_str(),&sz);
                            freqAnt = freq;
                            cont = 0;
                        }
                    }
                }
                //file.clear();
                file.close();
                std::remove("/tmp/sense.txt"); //remove o arquivo do disco
                
                std::string msg1 , msg2, msg3;
                int ter = send.length()/3; //divide mensagem em 3 partes
                msg1 = "<G"+send.substr(0,ter)+">";
                msg2 = "<G"+send.substr(ter, (ter))+">";// posição inicial, nro de posições à frente
                msg3 = "<G"+send.substr(ter+ter, send.length())+">";
                

                sleep(1);
                message_port_pub(pmt::mp("pdu"), pmt::intern(msg1));
                std::cout << msg1 << "msg1"<< std::endl;
                
                sleep(2);
                message_port_pub(pmt::mp("pdu"), pmt::intern(msg2));
                std::cout << msg2 << "msg2"<< std::endl;

                sleep(2);
                message_port_pub(pmt::mp("pdu"), pmt::intern(msg3));
                std::cout << msg3 << "msg3"<< std::endl;

                std::cout << send.length() << "tamanho"<< std::endl;
            }else{
                std::cerr << "file ../sense.txt don't exist" << std::endl;
                std::exit(-1);
            }
            
        }
    }

  } /* namespace pmt_cpp */
} /* namespace gr */

