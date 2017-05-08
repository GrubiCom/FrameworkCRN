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
#include "start_sense_impl.h"
#include <sys/time.h>
#include <sys/stat.h>



/* Bloco Start Sense. Bloco capaz de dar inicio ao sensoreamento do espectro.
 * Bloco que recebe um dicionario pmt. Este dicionario eh composto de tres valores. 
 * Frequencia minima, frequencia maxima e uma variavel bool indicando que o modo sense
 * esta ativo. 
 * Este bloco tem duas saidas de mensagens que sao as saidas bool e pmt::mp. A saida
 * bool eh para controle do modo sense, jah a saida pmt::mp eh para setar a nova frequencia
 * o bloco UHD: USRP Source/Sink 
 */
int acabooo = 0;
namespace gr {
    namespace pmt_cpp {

        /*Funcao make do start_sense*/
        start_sense::sptr
        start_sense::make() {
            return gnuradio::get_initial_sptr
                    (new start_sense_impl());
        }

        /*
         * The private constructor
         */
        start_sense_impl::start_sense_impl()
        : gr::block("start_sense",
        gr::io_signature::make(0, 0, 0),            //Anulo as entradas de fluxo de dados
        gr::io_signature::make(0, 0, 0))            //Anulo as saidas de fluxo de dados
        { 
        message_port_register_out(pmt::mp("pmt::mp"));  //Registra porta de saida pmt::mp. Fluxo de mensagens
        message_port_register_out(pmt::mp("bool"));     //Registra porta de saida bool. Fluxo de mensagens
    	
        pmt::pmt_t p_dict1  = pmt::make_dict();         //Cria um dicionario pmt de nome p_dict1
                
        p_dict1 = pmt::dict_add(p_dict1, pmt::string_to_symbol("sense"), pmt::PMT_F);       //Adiciona uma (chave=sense,valor=false)
        pmt::pmt_t senset1 = pmt::PMT_NIL;                                                  //Cria um pmt senset1 nulo
        senset1 = pmt::dict_ref(p_dict1, pmt::string_to_symbol("sense"), pmt::PMT_NIL);     //Retira valor do dicionario p_dict com a chave sense
                    
        message_port_pub(pmt::mp("bool"), senset1);         //Envia o senset1 para a saida bool
                
    	message_port_register_in(pmt::mp("pmt::dict"));     //Registra entrada pmt::dict
    	set_msg_handler(pmt::mp("pmt::dict"), 
                boost::bind(&start_sense_impl::handle_msg, 
                this, _1));                                 //Seta handlw_msg em pmt::dict
        sense = false;
        
        }
       

        /* handle_msg
         * \param msg Dicionario contendo uma mensagem
         */
        void start_sense_impl::handle_msg(pmt::pmt_t msg) {
            

            if(pmt::is_dict(msg)){// se vier um dicionário
                acabooo++;
                if (acabooo > 1){
                    exit(1);
                }
                std::cout << "[START SENSE]: STARTED"<< std::endl;
                
                pmt::pmt_t mim =  pmt::dict_ref(msg, pmt::string_to_symbol("mim"), pmt::PMT_NIL);     //Pega a frenquencia minima 
                pmt::pmt_t max =  pmt::dict_ref(msg, pmt::string_to_symbol("max"), pmt::PMT_NIL);       //Pega a frequencia maxima
                pmt::pmt_t senset = pmt::dict_ref(msg, pmt::string_to_symbol("sense"), pmt::PMT_NIL);   //Pega a flag sense
                
                double i = 0;
                
                
                time_t timer1, timer2;
                time(&timer1);
                
                //std::cout << "[SLAVE][START SENSE]: FMIm: " << pmt::to_double(mim) << std::endl; 
                //std::cout << "[SLAVE][START SENSE]: FMam: " << pmt::to_double(max) << std::endl; 
                for (i = pmt::to_double(mim); i <= pmt::to_double(max); i+=20e6){ //pula de 10MHz

                    
                    message_port_pub(pmt::mp("bool"), senset);  //Envia flag sense para bool


                    message_port_pub(pmt::mp("pmt::mp"), pmt::cons(pmt::mp("freq"),pmt::mp(i)));    //envia a nova frequencia para a placa USRP
                    //sleep(1);  
                    usleep(1000000);//Sleep de 1 segundo
                }
                
                time(&timer2);
                double sec = difftime(timer2,timer1);
                
                
                std::cout << "TIMER: "<< sec<<" s" << std::endl;
                pmt::pmt_t p_dict1  = pmt::make_dict();                                         //Cria dicionario vazio
                p_dict1 = pmt::dict_add(p_dict1, pmt::string_to_symbol("sense"), pmt::PMT_F);   //Cria (chave=sense,valor=false)
                pmt::pmt_t senset1 = pmt::PMT_NIL;                                              //Cria pmt nulo
                senset1 = pmt::dict_ref(p_dict1, pmt::string_to_symbol("sense"), pmt::PMT_NIL); //Senset1 recebe a flag sense

                    
                message_port_pub(pmt::mp("bool"), senset1);                                     //envia senset1 para bool
                sleep(1);
                std::cout << "[SLAVE]: tuned fo CCC 6.0G" << std::endl;
                message_port_pub(pmt::mp("pmt::mp"), pmt::cons(pmt::mp("freq"),pmt::mp(6000000000)));   //Seta frequencia da usrp em 2.48GHz
               

            }
        }
        
        
        bool start_sense_impl::is_sense() {
            return sense;
        }


    } /* namespace pmt_cpp */
} /* namespace gr */

