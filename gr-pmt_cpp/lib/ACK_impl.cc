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
#include "ACK_impl.h"
#include <fstream>
#include <sys/dir.h>
#include <dirent.h>
#include <sys/stat.h>
//#include <thread>

#define DIRNAME "COG"
namespace gr {
  namespace pmt_cpp {

    ACK::sptr
    ACK::make()
    {
      return gnuradio::get_initial_sptr
        (new ACK_impl());
    }

    /*
     * The private constructor
     */
    ACK_impl::ACK_impl()
      : gr::block("ACK",
              gr::io_signature::make(0,0,0),
              gr::io_signature::make(0,0,0))
    {
        
        message_port_register_out(pmt::mp("msg"));
        message_port_register_out(pmt::mp("first"));
        message_port_register_in(pmt::mp("Ack"));
        set_msg_handler(pmt::mp("Ack"), boost::bind(&ACK_impl::handle_msg, this, _1));
        
        message_port_register_in(pmt::mp("File_Ready"));
        set_msg_handler(pmt::mp("File_Ready"), boost::bind(&ACK_impl::handle_msg_file, this, _1));
        idUsrp = '4';
    }

    /*
     * Our virtual destructor.
     */
    ACK_impl::~ACK_impl()
    {
    }
    void ACK_impl::handle_msg(pmt::pmt_t msg) {



        pmt::pmt_t ack =  pmt::dict_ref(msg, pmt::string_to_symbol("ack"), pmt::PMT_NIL);
        long number = pmt::to_long(ack);

        std::string line;
        std::ifstream file; // open file
        int acks = 0;
        
        file.open("/tmp/send.txt");
        if (file.is_open()){
            while(!file.eof()){
                        getline(file,line);
                        acks++;

                    }
        }
        file.close(); file.open("/tmp/send.txt");
        if (file.is_open()){
            bool stop = false;

                getline(file,line);
                
                int pos;
                pos = line.find(":");

                
                
                if (number == 0){
                    sleep(0.4);
                    std::cout << number << " Pacote" << " <G:"+boost::to_string(idUsrp)+":" << line << ">" << std::endl; 
                    message_port_pub(pmt::mp("msg"),pmt::intern("<G:"+boost::to_string(idUsrp)+":"+line+">"));
                    
                }
                file.seekg(0);
                for (int i = 1; i < acks && !file.eof(); i++){
                    
                    getline(file,line);

                    if(i == number){//recebo ack 1 envio mensagem 2
                        sleep(0.4);
                        std::cout << number << " Pacote" << " <G:"+boost::to_string(idUsrp)+":" << line << ">" << std::endl; 
                        message_port_pub(pmt::mp("msg"),pmt::intern("<G:"+boost::to_string(idUsrp)+":"+line+">")); 
                    }if(number == acks) {
                        stop = true;
                    }
                }
                file.close();
                if(stop){
                    std::cout <<"[SLAVE][SEND PACKET DOWN]: FINISH SEND AND ERASE FILES (SENSE AND SEND).txt" << std::endl; 
                    //usleep(100000);
                    //remove("/tmp/sense.txt");
                    //usleep(100000);
                    //remove("/tmp/send.txt");
                    
                }

            
        }
    }
    void ACK_impl::handle_msg_file(pmt::pmt_t msg) {

        pmt::pmt_t ack =  pmt::dict_ref(msg, pmt::string_to_symbol("acks_total"), pmt::PMT_NIL);
        pmt::pmt_t sense =  pmt::dict_ref(msg, pmt::string_to_symbol("sense"), pmt::PMT_NIL);
        bool is_sense = pmt::to_bool(sense);
        if(is_sense){ //is_sense
            long acks = pmt::to_long(ack);
            sleep(0.8);
            std::cout << "Pacote Controle: " << " <K:"+boost::to_string(idUsrp)+":" << boost::to_string(acks) << ">" << std::endl; 
            message_port_pub(pmt::mp("msg"),pmt::intern("<K:"+boost::to_string(idUsrp)+":"+boost::to_string(acks)+">"));
            message_port_pub(pmt::mp("first"),pmt::intern("<K:"+boost::to_string(idUsrp)+":"+boost::to_string(acks)+">"));




        }else{
            std::cerr << "[SLAVE][SEND PACKET DOWN]: file ../send.txt don't exist" << std::endl;
            std::exit(-1);   
        }
        
    }
    
    void ACK_impl::ack_wait(long acks) {
        int ack = 0;
        while(!ack){
            std::ifstream file; // open file
            file.open("/tmp/ack.txt");

            std::cout << "[SLAVE][SEND PACKET DOWN]: Sleep 3 "<<  std::endl;
            sleep(3);
            if (file.is_open()){
                std::string line;
                getline(file,line);
                ack = std::atoi(line.c_str());
                std::cout << "[SLAVE][SEND PACKET DOWN]: ack:"<< ack << std::endl; 
                
            }else{
                std::cerr << "[SLAVE][SEND PACKET DOWN]: FUCK" << std::endl;
            }
            if (ack != 1){
                    std::cout << ack <<" << (Reenvio) Pacote Controle: " << " <K:"+boost::to_string(idUsrp)+":" << boost::to_string(acks) << ">" << std::endl;
                    message_port_pub(pmt::mp("msg"),pmt::intern("<K:"+boost::to_string(idUsrp)+":"+boost::to_string(acks)+">"));
            }
        }

    }


  } /* namespace pmt_cpp */
} /* namespace gr */

