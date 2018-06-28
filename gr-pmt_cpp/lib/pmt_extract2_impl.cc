/* -*- c++ -*- */
/* 
 * Copyright 2015 Ariel Marques.
 * Universidade Federal de Lavras - UFLA
 * Departamento de Ciencia da Computacao - DCC
 *
 * 2017 - Modified by <Luccas Rafael Martins Pinto>.
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
#include "pmt_extract2_impl.h"
#include "unistd.h"
#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <boost/date_time/posix_time/time_parsers.hpp>
#include <boost/date_time/posix_time/time_formatters.hpp>
/*Bloco pmt_extract2
 *Bloco capaz de extrair mensagens de dentro do PDU gerado pelo OOT 802.15.4 
 */

int packet_received = 0;
int sent1 = 0;
bool sense = false;
bool share = false;

namespace gr {
	
	namespace pmt_cpp {
	
		/* Funcao make do pmt_extract2 */
		pmt_extract2::sptr
		
		pmt_extract2::make(){
			
			return gnuradio::get_initial_sptr (new pmt_extract2_impl());
		}
		
		pmt_extract2_impl::pmt_extract2_impl() : gr::block("pmt_extract",
								gr::io_signature::make(0,0,0),
								gr::io_signature::make(0,0,0)){
			
			message_port_register_out(pmt::mp("sense"));     //Registra porta de saida pmt_dict
			message_port_register_out(pmt::mp("share")); 
			message_port_register_out(pmt::mp("Ack"));  
			message_port_register_out(pmt::mp("info_neighbor"));
			
			message_port_register_in(pmt::mp("in_pdu"));        //Registra porta de entrada in_pdu
			set_msg_handler(pmt::mp("in_pdu"), 
					
			boost::bind(&pmt_extract2_impl::handle_msg, this, _1)); //Seta handle_msg em in_pdu
			packet_received = 0;
		}
		
		pmt_extract2_impl::~pmt_extract2_impl(){}
		
		/* Funcao capaz de retirar todo o conteudo desejavel do PDU do 802.15.4 */
		void pmt_extract2_impl::handle_msg(pmt::pmt_t pdu){
			
			//exemplo sense <1:2:2.4:3.9>
			
			boost::posix_time::ptime x;           
			//boost::posix_time::ptime tt;
			x = boost::posix_time::microsec_clock::local_time();
			
			// add the field and publish
			pmt::pmt_t meta = pmt::car(pdu);
			pmt::pmt_t vector = pmt::cdr(pdu);
			
			//Testa PDU
			if(pmt::is_null(meta)){
				
				meta = pmt::make_dict();
				
			} else if (!pmt::is_dict(meta)){
				
				throw std::runtime_error("pdu_remove received non PDU input");
				
			}
			
			size_t offset(0);
			
			//Tamanho do PDU
			size_t len = pmt::length(vector);
			std::string lut = "0123456789:.,;-ANT<>B"; //17 caracteres regex
			int count = 0;
			char str[50];
			
			const uint8_t* d = (const uint8_t*) pmt::uniform_vector_elements(vector, offset);
			
			for(size_t i=0; i<len; i+=16){
				
				for(size_t j = i; j < std::min(i+16, len); j++){
					
					for (size_t x = 0; x < 21; x++){
						
						if (lut[x] == d[j]) {
							
							str[count] = d[j];
							count++;
						}
					}
				}
			}
			
			char idUsrp = '4';
			size_t idMaster = -1;
			char* pEnd;
			double fMax, fMim, nChannel;
			char value[3];
			int pos = 0;
			
			while(str[pos] != '<'){
				
				pos++;
			}

			if (str[pos] =='<' && (str[pos+1] == idUsrp || str[pos+1] == '0' ) ){ //1
				
				if (str[pos+1] == '0') {
					
					//std::cout <<"[SLAVE][MESSAGE PARSER]:Info: "<<str<< std::endl;
					// std::cout << "[SLAVE][MESSAGE PARSER]:Broadcast Message" << std::endl;
				}
				
				//std::cout <<"Info: "<<str<< std::endl;
				if(str[pos+3] == '0'){ //step <0:0> Broadcast:ID_MSG
					
					std::cout<< "[SLAVE][MESSAGE PARSER]:Discovery of neighbors " << "<0:N:"<<boost::to_string(idUsrp)<<":"<<boost::to_string(idUsrp)<<":1>"<< std::endl;
					std::fstream out; 
					out.open("/tmp/number_packet_received.txt", std::ios::out | std::ios::app);
                    
					if (out.is_open() && packet_received > 0){
						
						out << packet_received << std::endl;
						std::cout << "[SLAVE][MESSAGE PARSER]:SALVED TOTAL PACKET RECEIVED "<< std::endl;
						out.close();
					}
					std::ofstream out_file_table;
                                        std::fstream in_file_table;
                                        std::string filename_table = "/tmp/routing_table.txt";
                                        std::string mensagem_para_tabela;
                                        std::string mensagem_para_tabela_com_master;
                                        std::string separador = " ";
                                        std::string master_id = "0";
                                        
                                        int sourceID = 0;
                                        int hop_msg = 1; 
                                        
                                        if(!boost::filesystem::exists("/tmp/routing_table.txt")){
                                            out_file_table.open(filename_table.c_str(), std::ios::out | std::ios::in | std::ios::app);
                                            mensagem_para_tabela = "0 0 1";//Cria msg pra salvar na tabela
                                            out_file_table << mensagem_para_tabela << std::endl;//salva na tabela
                                            out_file_table.close();
                                        }else {
                                        std::cout << "TABELA JA EXISTE" << std::endl;
                                        
                                        in_file_table.open(filename_table.c_str(), std::ios::out | std::ios::in | std::ios::app);
                                        int dest,next,hop;
                                        bool atualizar_tabela = false;
                                        bool no_encontrado = false;                          

                                        //std::cout << sourceID << myID << hop_msg <<  std::endl;

                                        while (in_file_table >> dest >> next >> hop ){//verificar se a informacao do no ja esta na tabela

                                            if(sourceID == dest){//se o no se encontra na tabela

                                                if(hop_msg < hop){//verifica se o hop ja e o menor

                                                    atualizar_tabela = true;
                                                    no_encontrado = true;

                                                } else{

                                                    no_encontrado = true;
                                                    break;
                                                }
                                            }

                                        }//end while

                                        in_file_table.close();

                                        if(atualizar_tabela){

                                            std::cout << "Atualizar a tabela" << std::endl;
                                            std::string filename_table_temp = "/tmp/routing_table_temp.txt";
                                            in_file_table.open(filename_table.c_str(), std::ios::out | std::ios::in | std::ios::app);
                                            std::ofstream temp_out_file_table;
                                            temp_out_file_table.open(filename_table_temp.c_str(), std::ios::out | std::ios::in | std::ios::app);
                                            std::fstream temp_in_file_table;


                                            while(in_file_table >> dest >> next >> hop){//copia as informacoes para a tabela temporaria

                                                mensagem_para_tabela = boost::to_string(dest)+separador+boost::to_string(next)+separador+boost::to_string(hop);//monta a mensagem

                                                temp_out_file_table << mensagem_para_tabela << std::endl;//salva linha na tabela

                                            }
                                            temp_out_file_table.close();
                                            in_file_table.close();
                                            out_file_table.open(filename_table.c_str(), std::ofstream::out | std::ofstream::trunc);//limpar tabela
                                            out_file_table.close();//fechar tabela depois de limpar

                                            in_file_table.open(filename_table_temp.c_str(), std::ios::out | std::ios::in | std::ios::app);//abre tabela temporaria para leitura
                                            out_file_table.open(filename_table.c_str(), std::ios::out | std::ios::in | std::ios::app);//abre tabela para escrita

                                            while(in_file_table >> dest >> next >> hop){//copia as informacoes para a tabela

                                                if(sourceID == dest){

                                                    if(hop_msg < hop){

                                                        mensagem_para_tabela = boost::to_string(dest)+separador+boost::to_string(next)+separador+boost::to_string(hop_msg);//monta a mensagem com o menor hop

                                                    } else {
                                                        mensagem_para_tabela = boost::to_string(dest)+separador+boost::to_string(next)+separador+boost::to_string(hop);//monta a mensagem com o menor hop
                                                    }
                                                } else {
                                                    mensagem_para_tabela = boost::to_string(dest)+separador+boost::to_string(next)+separador+boost::to_string(hop);//copia a mensagem na integra
                                                }

                                                out_file_table << mensagem_para_tabela << std::endl;//salva linha na tabela

                                            }

                                            remove("/tmp/routing_table_temp.txt");//remove tabela temporaria

                                            out_file_table.close();
                                            in_file_table.close();

                                        }
                                        if(!no_encontrado){
                                            //std::cout << "colocar na tabela" << std::endl;
                                            out_file_table.open(filename_table.c_str(), std::ios::out | std::ios::in | std::ios::app);

                                            mensagem_para_tabela = "0 0 1";//Cria msg pra salvar na tabela

                                            out_file_table << mensagem_para_tabela << std::endl;//salva na tabela
                                        }
                                    
                                    }//end else

                                    out_file_table.close();
                                    
                                    packet_received = 0;
                                    srand (time(NULL));

                                    int time = std::rand()% 500000 + 200000;
                                    usleep(time);
                                    //Primeiro hop <0:B:srcID:1>
                                    message_port_pub(pmt::mp("info_neighbor"), pmt::intern("<0:B:"+boost::to_string(idUsrp)+":1>"));//broadcast vizinhos
                                    
                                    int time_2 = std::rand()% 500000 + 200000;
                                    usleep(time_2);
                                    //Primeira resposta <0 : N : myID : srcID : hop>
                                    message_port_pub(pmt::mp("info_neighbor"), pmt::intern("<0:N:"+boost::to_string(idUsrp)+":"+boost::to_string(idUsrp)+":1>"));//resposta para o master

                                    
                                   
                                    
				} else if (str[pos+3] == '1'){		// Comunicação de quem é o master //3
					
					std::cout << "[SLAVE][MESSAGE PARSER]:MASTER" << std::endl; //TALVEZ COMENTAR ESSE BLOCO
					idMaster = str[pos+5]; //5
					
				} else if (str[pos+3] =='2' && !sense){	// Comunicação para realizar sense
					
					//<1:2:2:3,0>
					sense = true;
					share = false;
					std::cout << "[SLAVE][MESSAGE PARSER]:SENSE" << std::endl;
					
					message_port_pub(pmt::mp("info_neighbor"), pmt::intern("<s:"+boost::to_string(idUsrp)+">"));//linha nova
					usleep(2000000);
					message_port_pub(pmt::mp("info_neighbor"), pmt::intern("<s:"+boost::to_string(idUsrp)+">"));//linha nova
					// remove("/tmp/ack");
					// remove("/tmp/sense.txt");
					// remove("/tmp/send.txt");
					// remove("/tmp/power.txt");
					// remove("/tmp/time.txt");
					
					std::string new_str (str);//<1:2:2:3,0>
					std::size_t p = new_str.find_last_of(":");//<1:2:2(:)3,0>
					std::string sub_str (new_str.substr(0,p));//<1:2:2
					std::size_t p1 = sub_str.find_last_of(":");//<1:2(:)2
					size_t f1 = sub_str.find(",");
					
					if (f1 != std::string::npos){
						
						sub_str.replace(f1, std::string(",").length(), ".");
					}
					
					std::stringstream sss(sub_str.substr(sub_str.find_last_of(":")+1,p1+1));
                    
					fMim = std::atof(sss.str().c_str());
					std::cout << "FMIm: " << fMim << std::endl;
					fMim *= (double)1.0e9;

					pmt::pmt_t p_dict  = pmt::make_dict();
					p_dict = pmt::dict_add(p_dict, pmt::string_to_symbol("mim"), pmt::from_double(fMim));
                    
					std::string st(str); //<1:2:2:3,0>
					
					std::size_t pos = st.find_last_of(":");//<1:2:2(:)3,0>
					std::size_t terminal = st.find_last_of(">");//<1:2:2:3,0(>)
					
					std::string su = st.substr(pos+1,((terminal)-(pos+1)));
					//std::string::size_type sz;
					size_t f = su.find(",");
					
					if (f != std::string::npos){
						
						su.replace(f, std::string(",").length(), ".");
					}
					
					std::cout << "SubString:su = "<< su << std::endl;
					std::stringstream ss(su);
					
					fMax = std::atof(ss.str().c_str());
					
					std::cout <<"[SLAVE][MESSAGE PARSER]:value: " << ss.str()<<std::endl;
					
					fMax *= 1e9;     
					std::cout << "[SLAVE][MESSAGE PARSER]: FMax: " << fMax << std::endl;
					p_dict = pmt::dict_add(p_dict, pmt::string_to_symbol("max"), pmt::from_double(fMax));
					p_dict = pmt::dict_add(p_dict, pmt::string_to_symbol("sense"), pmt::PMT_T);
					
					message_port_pub(pmt::mp("sense"), p_dict);
					
				} else if (str[pos+3] =='3' && !share){// Comunicação de novo canal
					
					//<1:3:2,4>
					sense = false;
					
					std::cout << "[SLAVE][MESSAGE PARSER]:SHARE" << std::endl;
					
					std::string st(str); 
					std::size_t pos = st.find_last_of(":");
					std::size_t terminal = st.find_last_of(">");
					
					size_t f = st.find(",");
					
					if (f != std::string::npos){
						
						st.replace(f, std::string(",").length(), ".");
					}
					
					nChannel = std::strtod(st.substr(pos+1,terminal).c_str(),&pEnd);
					std::cout << "[SLAVE][MESSAGE PARSER]:nChannel: " << nChannel<< std::endl;
					message_port_pub(pmt::mp("info_neighbor"), pmt::intern("<0:3:"+boost::to_string(nChannel)+">"));
					nChannel *= 1e9;
					
					pmt::pmt_t p_dict  = pmt::make_dict();
					p_dict = pmt::dict_add(p_dict, pmt::string_to_symbol("nChannel"), pmt::from_double(nChannel));
					share = true;
					message_port_pub(pmt::mp("share"), p_dict);
					
				} else if (str[pos+1] == idUsrp && str[pos+3] == '5' ){//confirmacao da mensagem do tipo 4(dados)
					
					sense = false;
					share = false;
					boost::posix_time::ptime t,t2;            
					
					t = boost::posix_time::microsec_clock::local_time();
					std::cout << "[SLAVE][MASSAGE PARSER]: RECEIVED PACKET DATA TRANSMISSION " <<packet_received << std::endl;
					std::string st(str);
					std::size_t po = st.find(":",7);
					
					std::string cu = st.substr(7,po-7);
					std::ofstream arq;
					arq.open("/tmp/time.txt",  std::ios::app);
					arq << cu<< std::endl;
					arq.close();
					std::size_t p = st.find_last_of(":");
					std::size_t terminal = st.find(">");
					std::string sub = st.substr(p+1,terminal-(p+1));
					
					try {
						t2 = boost::posix_time::from_iso_string(sub);
						boost::posix_time::time_duration t1 = t - t2;
						std::ofstream micro;
						micro.open("/tmp/total_microseconds.txt",  std::ios::app);
						micro << t1.total_microseconds()<< std::endl;
						micro.close(); 
						
					} catch (...) {
						
						//std::cout << "Date error" << std::endl;
					}
					
					//packet_received++;
				} else if (str[pos+1] == idUsrp && str[pos+3] == '4' ) {//Comunicacao do tipo dados
					
					//std::cout << "[SLAVE][MESSAGE PARSER]: DATA "<< std::endl;
					
					std::string st(str); 
					std::size_t po = st.find(":",7);
					std::string su = st.substr(7,po-7);
					std::size_t terminal = st.find(">");
					std::size_t p = st.find_last_of(":",terminal-1);
					//std::cout << "[SLAVE][MASSAGE PARSER]: RECEIVED PACKET DATA TRANSMISSION " <<packet_received << std::endl;
					packet_received++;
					std::string filename = "/tmp/";
					filename.append("received_pack");
					filename.push_back(str[pos+5]);
					filename.append(".txt");
					std::fstream arq;
					std::string sub = st.substr(p+1,terminal-(p+1));
					std::string str2(str);
					str2[pos+1] = str[pos+5];
					str2[pos+5] = str[pos+1];
					std::cout << "<"<<str[pos+5]<<":4:"<<"0:"<< su<<":00011110000000000000000000000000000000000000000000000:"<<sub<<">"<<std::endl;
					
					if((int)packet_received % 53 == 0){
						
						message_port_pub(pmt::mp("info_neighbor"), pmt::intern("<"+boost::to_string(str[pos+5])+":5:"+idUsrp+":"+su+":00011110000000000000000000000000000000000000000000000:"+sub+">"));
					}
					
					std::string filename1 = "/tmp/";
					sent1++;
					filename1.append("sent_pack");
					filename1.push_back(str[pos+5]);
					filename1.append(".txt");
					
					std::fstream se;
					se.open(filename1.c_str(), std::ios::out | std::ios::app);
					se << sent1<< std::endl;
					se.close();
                                        
				} else if(str[pos+3] == 'B' && str[pos+5] != idUsrp){//SLAVE BROADCAST <0:B:srcID:hop>
                                    
                                    //inicio da criacao da tabela de roteamento
                                    std::ofstream out_file_table;
                                    std::fstream in_file_table;
                                    std::string filename_table = "/tmp/routing_table.txt";
                                    std::string mensagem_para_tabela;
                                    std::string mensagem_para_tabela_com_master;
                                    std::string separador = " ";
                                    std::string master_id = "0";
                                    
                                    int sourceID = str[pos+5] - '0';//the integer value for any digit is the digit less '0' (or 48).
                                    int hop_msg = str[pos+7] - '0';
                                    bool hop_incrementado = false;
                                    

                                    if(!boost::filesystem::exists("/tmp/routing_table.txt")){

                                        std::cout << "CRIANDO TABELA DE ROTEAMENTO" << std::endl;
                                        out_file_table.open(filename_table.c_str(), std::ios::out | std::ios::in | std::ios::app);
                                        
                                        hop_msg++;
                                        hop_incrementado = true;
                                        
                                        char hop_char = hop_msg + '0';//hop no tipo char para colocar na tabela
                                        
                                        mensagem_para_tabela_com_master = master_id+separador+str[pos+5]+separador+hop_char;
                                                
                                        mensagem_para_tabela = str[pos+5]+separador+str[pos+5]+separador+"1";//Cria msg pra salvar na tabela o no vizinho

                                        out_file_table << mensagem_para_tabela_com_master << std::endl;//salva na tabela
                                        
                                        out_file_table << mensagem_para_tabela << std::endl;//salva na tabela
                                        

                                    } else {
                                        std::cout << "TABELA JA EXISTE" << std::endl;
                                        
                                        in_file_table.open(filename_table.c_str(), std::ios::out | std::ios::in | std::ios::app);
                                        int dest,next,hop;
                                        bool atualizar_tabela = false;
                                        bool no_encontrado = false;                          

                                        //std::cout << sourceID << myID << hop_msg <<  std::endl;

                                        while (in_file_table >> dest >> next >> hop ){//verifica se a informacao do no ja esta na tabela
                                            
                                            //TODO verificar se o master possui menor hop

                                            if(sourceID == dest){//se o no se encontra na tabela

                                                if(hop_msg < hop){//verifica se o hop ja' e' o menor

                                                    atualizar_tabela = true;
                                                    no_encontrado = true;
                                                    break;

                                                } else{

                                                    no_encontrado = true;
                                                    break;
                                                }
                                            }

                                        }//end while

                                        in_file_table.close();

                                        if(atualizar_tabela){

                                            std::cout << "Atualizar a tabela" << std::endl;
                                            std::string filename_table_temp = "/tmp/routing_table_temp.txt";
                                            in_file_table.open(filename_table.c_str(), std::ios::out | std::ios::in | std::ios::app);
                                            std::ofstream temp_out_file_table;
                                            temp_out_file_table.open(filename_table_temp.c_str(), std::ios::out | std::ios::in | std::ios::app);
                                            std::fstream temp_in_file_table;


                                            while(in_file_table >> dest >> next >> hop){//copia as informacoes para a tabela temporaria

                                                mensagem_para_tabela = boost::to_string(dest)+separador+boost::to_string(next)+separador+boost::to_string(hop);//monta a mensagem

                                                temp_out_file_table << mensagem_para_tabela << std::endl;//salva linha na tabela

                                            }
                                            temp_out_file_table.close();
                                            in_file_table.close();
                                            out_file_table.open(filename_table.c_str(), std::ofstream::out | std::ofstream::trunc);//limpar tabela
                                            out_file_table.close();//fechar tabela depois de limpar

                                            in_file_table.open(filename_table_temp.c_str(), std::ios::out | std::ios::in | std::ios::app);//abre tabela temporaria para leitura
                                            out_file_table.open(filename_table.c_str(), std::ios::out | std::ios::in | std::ios::app);//abre tabela para escrita

                                            while(in_file_table >> dest >> next >> hop){//copia as informacoes para a tabela

                                                if(sourceID == dest){

                                                    if(hop_msg < hop){

                                                        mensagem_para_tabela = boost::to_string(dest)+separador+boost::to_string(next)+separador+boost::to_string(hop_msg);//monta a mensagem com o menor hop

                                                    } else {
                                                        mensagem_para_tabela = boost::to_string(dest)+separador+boost::to_string(next)+separador+boost::to_string(hop);//monta a mensagem com o menor hop
                                                    }
                                                } else {
                                                    mensagem_para_tabela = boost::to_string(dest)+separador+boost::to_string(next)+separador+boost::to_string(hop);//copia a mensagem na integra
                                                }

                                                out_file_table << mensagem_para_tabela << std::endl;//salva linha na tabela

                                            }

                                            remove("/tmp/routing_table_temp.txt");//remove tabela temporaria

                                            out_file_table.close();
                                            in_file_table.close();

                                        }
                                        if(!no_encontrado){
                                            //std::cout << "colocar na tabela" << std::endl;
                                            out_file_table.open(filename_table.c_str(), std::ios::out | std::ios::in | std::ios::app);
                                            
                                            //hop_msg++;
                                            //hop_incrementado = true;
                                            
                                            char hop_char = hop_msg + '0';//hop no tipo char para colocar na tabela

                                            mensagem_para_tabela = str[pos+5]+separador+str[pos+5]+separador+"1";//Cria msg pra salvar na tabela

                                            out_file_table << mensagem_para_tabela << std::endl;//salva na tabela
                                        }
                                    
                                    }//end else

                                    out_file_table.close();
                                    
                                    //fim da criacao da tabela de roteamento
                                    
                                    //inicio da resposta
                                    
                                    int dest,next,hop;
                                    bool transmite = true;
                                    
                                    if(!hop_incrementado){
                                        hop_msg++;
                                    }
                                    char hop_char = hop_msg + '0';//hop no tipo char para colocar na tabela
                                    
                                    while(in_file_table >> dest >> next >> hop){
                                                
                                        if(dest == 0){
                                            
                                            if(hop < hop_msg){
                                                transmite = false;
                                                
                                            }
                                        }
                                                
                                    }//end while
                                    
                                    //for (int i = 0; i < 5; i++){
                                        //usleep(200000);
                                    
                                    if(transmite){
                                        message_port_pub(pmt::mp("info_neighbor"), pmt::intern("<0:N:"+boost::to_string(idUsrp)+":"+boost::to_string(idUsrp)+":"+hop_char+">"));//resposta broadcast vizinhos
                                    }
                                        
                                    //}
                                    //fim da resposta
                                    std::cout << "[SLAVE][MESSAGE PARSER]: RESPONSE SLAVE BROADCAST DA MENSAGEM "<< str << std::endl;
                                    //std::cout << "[SLAVE][MESSAGE PARSER]: DEU CERTO "<< std::endl;
                                    //exit(1);
                                } else if(str[pos+3] == 'N' && str[pos+5] != idUsrp){//RESPOSTA SLAVE BROADCAST<0:N:srcID:myID:hop>
                                    
                                    
                                    if(!boost::filesystem::exists("/tmp/routing_table.txt")){
                                        
                                        std::cout << "[SLAVE][MESSAGE PARSER]: MENSAGEM DE N ANTES DA MENSAGEM DE B "<< str << std::endl;
                                    
                                    } else {
                                        
                                        std::ofstream out_file_table;
                                        std::fstream in_file_table;
                                        std::string filename_table = "/tmp/routing_table.txt";
                                        std::string mensagem_para_tabela; 
                                        std::string separador = " ";

                                        in_file_table.open(filename_table.c_str(), std::ios::out | std::ios::in | std::ios::app);
                                        int dest,next,hop;
                                        bool atualizar_tabela = false;
                                        bool no_encontrado = false;


                                        int sourceID = str[pos+7] - '0';//the integer value for any digit is the digit less '0' (or 48).
                                        int myID = str[pos+5] - '0';
                                        int hop_msg = str[pos+9] - '0';

                                        //std::cout << myID << sourceID << hop_msg <<  std::endl;

                                        while (in_file_table >> dest >> next >> hop ){//verificar se a informacao do no ja esta na tabela

                                            if(sourceID == dest){

                                                if(hop_msg < hop){

                                                    atualizar_tabela = true;
                                                    no_encontrado = true;

                                                } else{

                                                    no_encontrado = true;
                                                    break;
                                                }
                                            }

                                        }//end while

                                        in_file_table.close();

                                        if(atualizar_tabela){

                                            std::cout << "Atualizar a tabela" << std::endl;
                                            std::string filename_table_temp = "/tmp/routing_table_temp.txt";
                                            in_file_table.open(filename_table.c_str(), std::ios::out | std::ios::in | std::ios::app);
                                            std::ofstream temp_out_file_table;
                                            temp_out_file_table.open(filename_table_temp.c_str(), std::ios::out | std::ios::in | std::ios::app);
                                            std::fstream temp_in_file_table;


                                            while(in_file_table >> dest >> next >> hop){//copia as informacoes para a tabela temporaria

                                                mensagem_para_tabela = boost::to_string(dest)+separador+boost::to_string(next)+separador+boost::to_string(hop);//monta a mensagem

                                                temp_out_file_table << mensagem_para_tabela << std::endl;//salva linha na tabela

                                            }
                                            temp_out_file_table.close();
                                            in_file_table.close();
                                            out_file_table.open(filename_table.c_str(), std::ofstream::out | std::ofstream::trunc);//limpar tabela
                                            out_file_table.close();//fechar tabela depois de limpar

                                            in_file_table.open(filename_table_temp.c_str(), std::ios::out | std::ios::in | std::ios::app);//abre tabela temporaria para leitura
                                            out_file_table.open(filename_table.c_str(), std::ios::out | std::ios::in | std::ios::app);//abre tabela para escrita

                                            while(in_file_table >> dest >> next >> hop){//copia as informacoes para a tabela

                                                if(sourceID == dest){

                                                    if(hop_msg < hop){

                                                        mensagem_para_tabela = boost::to_string(dest)+separador+boost::to_string(next)+separador+boost::to_string(hop_msg);//monta a mensagem com o menor hop

                                                    } else {
                                                        mensagem_para_tabela = boost::to_string(dest)+separador+boost::to_string(next)+separador+boost::to_string(hop);//monta a mensagem com o menor hop
                                                    }
                                                } else {
                                                    mensagem_para_tabela = boost::to_string(dest)+separador+boost::to_string(next)+separador+boost::to_string(hop);//copia a mensagem na integra
                                                }

                                                out_file_table << mensagem_para_tabela << std::endl;//salva linha na tabela

                                            }

                                            remove("/tmp/routing_table_temp.txt");//remove tabela temporaria

                                            out_file_table.close();
                                            in_file_table.close();

                                        }
                                        if(!no_encontrado && str[pos+7] != idUsrp){
                                            //std::cout << "colocar na tabela" << std::endl;
                                            out_file_table.open(filename_table.c_str(), std::ios::out | std::ios::in | std::ios::app);
                                            in_file_table.open(filename_table.c_str(), std::ios::out | std::ios::in | std::ios::app);//abre tabela temporaria para leitura
                                            
                                            int hop_para_node_vizinho;
                                            while(in_file_table >> dest >> next >> hop){
                                                
                                                if(dest == 0){
                                                    hop_para_node_vizinho = hop_msg - hop;//calcula os hops para o node que mandou a msg baseado no master
                                                }
                                                
                                            }//end while

                                            mensagem_para_tabela = str[pos+7]+separador+str[pos+5]+separador+boost::to_string(hop_para_node_vizinho);//Cria msg pra salvar na tabela

                                            out_file_table << mensagem_para_tabela << std::endl;//salva na tabela
                                            
                                        }//end if
                                        
                                        out_file_table.close();
                                        in_file_table.close();
                                        
                                        bool transmite = true;
                                        
                                        if(str[pos+7] == idUsrp){
                                            transmite =  false;
                                        }
                                        
                                        //for (int i = 0; i < 5; i++){
                                            //usleep(100000);
                                            if(transmite){
                                                message_port_pub(pmt::mp("info_neighbor"), pmt::intern("<0:N:"+boost::to_string(idUsrp)+":"+str[pos+7]+":"+str[pos+9]+">"));//resposta para o no proximo do master
                                                std::cout << "[SLAVE][MESSAGE PARSER]: ENCAMINHEI A MENSAGEM "<< str << std::endl;
                                            }
                                            
                                        //}
                                        
                                        std::fstream file1;
                                        std::string filename = "/tmp/neighbors_slave.txt";
                                        std::string neighbor_f;
                                        std::ifstream file; // open file
                                        file.open(filename.c_str());
                                        std::string id_neighbor = boost::to_string(str[pos+5]);
                                        bool contained = false;

                                        if (file.is_open()){

                                                while (getline(file,neighbor_f)){

                                                        if(neighbor_f.compare(id_neighbor) == 0 ){//verifica existencia de vizinho no arquivo
                                                                contained = true;
                                                        }
                                                }

                                                file.close();
                                        }

                                        if (!contained  && (id_neighbor.compare(boost::to_string(idUsrp))!= 0)){

                                                //std::cout << "[SLAVE][MESSAGE PARSER]: Saved "<<str << std::endl;
                                                file1.open(filename.c_str(), std::ios::in | std::ios::out | std::ios::app); 

                                                if(file1.is_open()){

                                                        file1 << id_neighbor<< std::endl;//coloca o vizinho na lista
                                                        file1.close();
                                                }
                                        }
                                        //exit(1); 

                                    }//end else

                                    
                                }//end else if
				
			} else if (str[pos] =='<' && str[pos+1] == 'A' && str[pos+3] == idUsrp){
               
				std::string st(str); 
				std::size_t pos = st.find_last_of(":");
				std::size_t terminal = st.find_last_of(">");
				std::string::size_type sz;//TALVEZ COMENTAR;
				int bla = std::atoi(st.substr(pos+1,terminal).c_str());
				
				int a = bla;
				
				if (a == 1){// Salva a primeira mensagem recebida
					
					std::fstream out;
					out.open("/tmp/ack.txt", std::ios::out);
					
					if(out.is_open()){
						
						out << a;
						std::cout << "[SLAVE][MESSAGE PARSER]:SALVANDO ACK = 1"<< a <<std::endl;
						
					} else {
						
						std::cerr << "file ~/ack.txt don't exist" << std::endl;
						std::exit(-1);
					}
					
					out.close();
				}
				
				pmt::pmt_t dict  = pmt::make_dict();
				dict = pmt::dict_add(dict, pmt::string_to_symbol("ack"), pmt::from_long(a));
				std::cout << "[SLAVE][MESSAGE PARSER]: ACK" << std::endl;
				
				message_port_pub(pmt::mp("Ack"), dict);
				sense = false;
				share = false;
				
			} else if(str[pos+3] == 'N'){
				
				//Descobertas dos vizinhos<N:ID_neighbor>

				std::fstream file1;
				std::string filename = "/tmp/neighbors_slave.txt";
				std::string neighbor_f;
				std::ifstream file; // open file
				file.open(filename.c_str());
				std::string id_neighbor = boost::to_string(str[pos+5]);
				bool contained = false;
				
				if (file.is_open()){
					
					while (getline(file,neighbor_f)){
						
						if(neighbor_f.compare(id_neighbor) == 0 ){//verifica existencia de vizinho no arquivo
							contained = true;
						}
					}
					
					file.close();
				}
				
				if (!contained  && (id_neighbor.compare(boost::to_string(idUsrp))!= 0)){

					//std::cout << "[SLAVE][MESSAGE PARSER]: Saved "<<str << std::endl;
					file1.open(filename.c_str(), std::ios::in | std::ios::out | std::ios::app); 
					
					if(file1.is_open()){
						
						file1 << id_neighbor<< std::endl;//coloca o vizinho na lista
						file1.close();
					}
				}       
				
			} else {
				
				//str = NULL; std::free(str);
				std::cout << "[SLAVE][MESSAGE PARSER]: Ultimo else provavel Lixo" << std::endl;
			}
				
			for (int i = 0; i < 50; i++) str[i] = 0;
			//sense=false;
		}
	} /* namespace pmt_cpp */
} /* namespace gr */

