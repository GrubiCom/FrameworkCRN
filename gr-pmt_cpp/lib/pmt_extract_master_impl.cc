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
#include "pmt_extract_master_impl.h"
//#include "unistd.h"
//#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <string>
#include <string.h>
#include <sys/stat.h>
#include <sys/dir.h>
#include <boost/date_time/posix_time/time_parsers.hpp>
#include <boost/date_time/posix_time/time_formatters.hpp>
int received = 0;
int sent = 0;
namespace gr {
  namespace pmt_cpp {

    pmt_extract_master::sptr
    pmt_extract_master::make()
    {
      return gnuradio::get_initial_sptr
        (new pmt_extract_master_impl());
    }

    /*
     * The private constructor
     */
    pmt_extract_master_impl::pmt_extract_master_impl()
      : gr::block("pmt_extract_master",
              gr::io_signature::make(0,0,0),
              gr::io_signature::make(0,0,0))
    {
        message_port_register_out(pmt::mp("data"));     //Registra porta de saida pmt_dict
        message_port_register_out(pmt::mp("Ack"));  
    	message_port_register_out(pmt::mp("share"));
        message_port_register_out(pmt::mp("freq")); 
    	message_port_register_out(pmt::mp("freqTeste"));
        message_port_register_in(pmt::mp("in_pdu"));        //Registra porta de entrada in_pdu
    	set_msg_handler(pmt::mp("in_pdu"), 
                boost::bind(&pmt_extract_master_impl::handle_msg, 
                this, _1));   
    
    }

    /*
     * Our virtual destructor.
     */
    pmt_extract_master_impl::~pmt_extract_master_impl()
    {
    }
    
    void pmt_extract_master_impl::handle_msg(pmt::pmt_t pdu){
        // add the field and publish
         boost::posix_time::ptime t,t2;            
        //boost::posix_time::ptime tt;
        t = boost::posix_time::microsec_clock::local_time();
        pmt::pmt_t meta = pmt::car(pdu);
        pmt::pmt_t vector = pmt::cdr(pdu);

        //Testa PDU
        if(pmt::is_null(meta)){
                meta = pmt::make_dict();
                } else if(!pmt::is_dict(meta)){
                        throw std::runtime_error("pdu_remove received non PDU input");
        }
        size_t offset(0);
        //Tamanho do PDU
        size_t len = pmt::length(vector);
        std::string lut = "0123456789:.,;-GKSTsN<>";//18 caracteres regex
        int count = 0;
        char str[50];

        const uint8_t* d = (const uint8_t*) pmt::uniform_vector_elements(vector, offset);
        for(size_t i=0; i<len; i+=16){
                for(size_t j=i; j<std::min(i+16,len); j++){
                        for (size_t x=0; x<23; x++){
                                if (lut[x] == d[j]) {
                                        str[count] = d[j];

                                        count++;
                                }
                        }
                }

        }

        
        int pos = 0;

        if (count > 3) {
            while(str[pos]!= '<' ){
                pos++;
            }
        }

        if((str[pos] =='<') && (str[pos+1] == 'G' || str[pos+1] =='K' || 
                str[pos+1] == 'N' || str[pos+1] == 's')){//to do parte do k
            
            std::fstream out; 
            bool descart = false;
            int a;
            char data,teste;
            
            const char dir_path[] = "/tmp/Acknowledgement/";
            boost::filesystem::path dir(dir_path);
            if(!boost::filesystem::exists(dir)){
               boost::filesystem::create_directories(dir); 
            }
            std::string filename = "/tmp/Acknowledgement/acks";
            filename.push_back(str[pos+3]);//ID
            int id = str[pos+3] - '0';
            filename.append(".txt");
            out.open(filename.c_str(),std::ios::in | std::ios::out ); //|std::ios::app
            if(str[pos+1] == 'G' ){
                std::string st(str);
                int ini = st.find("<");
                int end = st.find(">");
                if(end < ini){
                    end = st.find_last_of(">");
                }
                std::string sub = st.substr(ini+5,end);
                
                std::string sub2 = sub.substr(0,sub.find(":"));

                a = std::atoi(sub2.c_str());
                if (out.is_open()){

                   std::string line;
                   while(!out.eof()){
                        getline(out,line);
                        std::stringstream ss;
                        if (a>=0 && a <=9){
                            ss.width(2);
                            ss << std::setfill('0') << a;
                        }else {
                            ss << a;
                        }

                        if (ss.str().compare(line) == 0){
                            descart = true;

                        }

                    }
                }
                out.close();
                std::cout << "[MASTER][MESSAGE PARSER]: ACK: " << a << std::endl;
            }else if (str[pos+1] =='K' ){
                 
                 std::string st(str); 
                 std::size_t pos = st.find_last_of(":");
                 std::size_t terminal = st.find_last_of(">");
               
                 int bla = std::atoi(st.substr(pos+1,terminal).c_str());
                 std::cout << "[MASTER][MESSAGE PARSER]: ACK1: " << bla<< std::endl;
                 a = bla;
                
            }else if(str[pos+1] == 's'){//if novo
                
                std::fstream file1;
                std::string filename = "/tmp/acks_sense.txt";              
                std::ifstream file; // open file
                file.open(filename.c_str());
                std::string id_ack = boost::to_string(str[pos+3]);
                std::cout << "[MASTER][MESSAGE PARSER]: Ack sense: "<<str << std::endl;
                file1.open(filename.c_str(), std::ios::in | std::ios::out | std::ios::app); 
                if(file1.is_open()){
                    file1 << id_ack<< std::endl;
                    file1.close();
                }
                //received = 0;
            }else if(str[pos+1] == 'N'){
                //Descobertas dos vizinhos<N:ID_neighbor>

                
                std::fstream file1;
                std::string filename = "/tmp/neighbors.txt";
                std::string neighbor_f;
                std::ifstream file; // open file
                file.open("/tmp/neighbors.txt");
                std::string id_neighbor = boost::to_string(str[pos+3]);
                bool contained = false;
                if(file.is_open()){
                    while(getline(file,neighbor_f)){


                        if(neighbor_f.compare(id_neighbor) == 0){
                            contained = true;
                        }
                    }
                    file.close();
                    
                }
                if(!contained){
                    

                    std::cout << "[MASTER][MESSAGE PARSER]: "<<str << std::endl;
                    file1.open(filename.c_str(), std::ios::in | std::ios::out | std::ios::app); 
                    if(file1.is_open()){
                        file1 << id_neighbor<< std::endl;
                        file1.close();
                    }
                        
                }
                std::fstream out; 
                    out.open("/tmp/number_packet_received.txt", std::ios::out | std::ios::app);
                    if(out.is_open() && received > 0){
                        out << received << std::endl;
                        std::cout << "[MASTER][MESSAGE PARSER]:SALVED TOTAL PACKET RECEIVED "<< std::endl;
                        out.close();
                    }
                    received = 0;
                    sent=0;
               
                               
            }
            
            if(str[pos+1] == 'G' || str[pos+1] =='K'){
                int acks_total;

                out.open(filename.c_str(),std::ios::in | std::ios::out |std::ios::app);
                if (!descart){
                    if (a>=0 && a <=9){
                        std::stringstream ss;
                        ss.width(2);
                        ss << std::setfill('0') << a;
                        out << ss.str() << std::endl;
                    }else{
                        out << a << std::endl;
                    }

                }
            
                sleep(0.4);
                pmt::pmt_t dict1  = pmt::make_dict();
                if(str[pos+1] !='K'){

                    message_port_pub(pmt::mp("Ack"), pmt::intern("<A:"+boost::to_string(id)+":"+boost::to_string(a+1)+">"));
                    //std::cout  << " [MASTER][MESSAGE PARSER]: Ack2: "<< "<A:" << boost::to_string(id) << ":" <<boost::to_string(a+1)<<">"<< std::endl;
                    dict1 = pmt::dict_add(dict1, pmt::string_to_symbol("ack"), pmt::from_long(a));
                }else {
                    //std::cout  << " [MASTER][MESSAGE PARSER]: a: " << a << std::endl;
                    a = 1;
                    message_port_pub(pmt::mp("Ack"), pmt::intern("<A:"+boost::to_string(id)+":"+boost::to_string(1)+">"));
                    //std::cout  << " [MASTER][MESSAGE PARSER]: Ack3: " << "<A:" << boost::to_string(id) <<   ":" <<boost::to_string(1)<<">"<< std::endl;
                    dict1 = pmt::dict_add(dict1, pmt::string_to_symbol("ack"), pmt::from_long(0));
                }

                if (!descart){
                    dict1 = pmt::dict_add(dict1, pmt::string_to_symbol("res_sense"), pmt::string_to_symbol(str));

                }else {
                    std::cout << "[MASTER][MESSAGE PARSER]: Descarte da mensagem: "<< str << std::endl;
                }
                descart = false;
                std::cout << "[MASTER][MESSAGE PARSER]: Request Ack " << pmt::from_long(a) << std::endl;
                

                dict1 = pmt::dict_add(dict1,pmt::string_to_symbol("id"), pmt::string_to_symbol(boost::to_string(str[pos+3])));
                out.seekp(0);
                out >> acks_total;

                dict1 = pmt::dict_add(dict1, pmt::string_to_symbol("acks_total"), pmt::from_long(acks_total));

                sleep(0.4);
                

                
                message_port_pub(pmt::mp("data"), dict1);







                out.close();
            }
    
        } else if ((str[pos] =='<') && (str[pos+1] == 'S') && (str[pos+3] == '0')){
            std::cout << "[MASTER][MESSAGE PARSER]: SHARE " <<str[pos]<< " " << str[pos+1]<<  std::endl;
             sent=0;       
            std::string st(str); 
            std::size_t p = st.find_last_of(":");
            std::size_t terminal = st.find_last_of(">");
            
            size_t f = st.find(",");
            if (f != std::string::npos){
                st.replace(f, std::string(",").length(), ".");
            }
            char *pEnd;
            double nChannel = std::strtod(st.substr(p+1,terminal).c_str(),&pEnd);
             
            nChannel *= 1e9;
            pmt::pmt_t p_dict  = pmt::make_dict();
            p_dict = pmt::dict_add(p_dict, pmt::string_to_symbol("nChannel"), pmt::from_double(nChannel));
            p_dict = pmt::dict_add(p_dict, pmt::string_to_symbol("ID"), pmt::string_to_symbol(boost::to_string(str[pos+3])));
            message_port_pub(pmt::mp("share"), p_dict);
            
        
        }else if ((str[pos] =='<') && (str[pos+1] =='0') && str[pos+3] == '3'){
            //Implementar o change freg
            usleep(500000);
            std::string st(str); 
            std::size_t p = st.find_last_of(":");
            std::size_t terminal = st.find_last_of(">");
            
            size_t f = st.find(".");
            if (f != std::string::npos){
                st.replace(f, std::string(".").length(), ",");
            }
            char *pEnd;
            double nChannel = std::strtod(st.substr(p+1,terminal).c_str(),&pEnd);
            
            if(!boost::filesystem::exists("/tmp/master_channels.txt")){
                message_port_pub(pmt::mp("freq"),pmt::cons(pmt::mp("freq"),pmt::mp(nChannel*1e9)));
                message_port_pub(pmt::mp("freqTeste"),pmt::cons(pmt::mp("freq"),pmt::mp((nChannel*1e9)-20e6)));
                std::fstream out; 
                out.open("/tmp/master_channels.txt", std::ios::out);
                if(out.is_open()){
                    out << nChannel<< std::endl;
                    std::cout << "[MASTER][MESSAGE PARSER]:SALVANDO "<< std::endl;
                    out.close();
                }
            }
            
        }else if ((str[pos] =='<') && (str[pos+1] =='0') && str[pos+3] == '4'){
            
            std::cout << "[MASTER][MESSAGE PARSER]: DATA "<<str<< std::endl;

            std::string st(str); 
            std::size_t po = st.find(":",7);
            std::string su = st.substr(7,po-7);
            std::size_t terminal = st.find(">");
            std::size_t p = st.find_last_of(":",terminal-1);
            //std::cout << "[SLAVE][MASSAGE PARSER]: RECEIVED PACKET DATA TRANSMISSION " <<received << std::endl;
            received++;
            

            std::string filename = "/tmp/";
            
            filename.append("received_pack");
            filename.push_back(str[pos+5]);
            filename.append(".txt");

            std::fstream arq;
            
            std::string sub = st.substr(p+1,terminal-(p+1));
            
            
            
            std::string str2(str);
            str2[pos+1] = str[pos+5];
            str2[pos+5] = str[pos+1];

            std::cout << "<"<<str[pos+5]<<":5:"<<"0:"<< su<<":00011110000000000000000000000000000000000000000000000:"<<sub<<">"<<std::endl;
            
            if (sent % 53 ==0){
            message_port_pub(pmt::mp("Ack"), pmt::intern("<"+boost::to_string(str[pos+5])+":5:0:"+su+":00011110000000000000000000000000000000000000000000000:"+sub+">"));
            }
            std::string filename1 = "/tmp/";
            sent++;
            filename1.append("sent_pack");
            filename1.push_back(str[pos+5]);
            filename1.append(".txt");

            std::fstream se;
            se.open(filename1.c_str(), std::ios::out | std::ios::app);
            se << sent<< std::endl;
            se.close();
        }else{
            //std::cout << "[MASTER][MESSAGE PARSER]: NADA "<<str << std::endl;
        }
        for (int i = 0; i < 50; i++) str[i] = 0;
        
    }

  } /* namespace pmt_cpp */
} /* namespace gr */

