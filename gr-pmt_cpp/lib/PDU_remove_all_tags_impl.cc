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

#include <gnuradio/io_signature.h>      // Entrada e saida do gnuradio
#include "PDU_remove_all_tags_impl.h"   // Biblioteca
#include <ctime>

/*
 * Bloco PDU_remove_all_tags.
 * Tem a funcao de retirar todas as tags indesejadas proveniente dos blocos
 * event_stream e do bloco cpdu_average_power do OOT uhdgps. 
 */
namespace gr {
  namespace pmt_cpp {

    /*
     * Funcão make do bloco PDU_remove_all_tags
     */
    PDU_remove_all_tags::sptr
    PDU_remove_all_tags::make()
    {
      return gnuradio::get_initial_sptr
        (new PDU_remove_all_tags_impl());
    }

    /*
     * The private constructor
     */
    PDU_remove_all_tags_impl::PDU_remove_all_tags_impl()
      : gr::block("PDU_remove_all_tags",
              gr::io_signature::make(0,0,0),        //anulando as entradas de fluxo
              gr::io_signature::make(0,0,0))        //anulando as saidas de fluxo
    {
        message_port_register_out(pmt::mp("pdus")); //registrando porta de saida de mensagens pdus
    	
    	message_port_register_in(pmt::mp("bool"));  //registrando porta de entrada de mensagens bool
        /*
         * Setando funcao de ativacao handle_msg2.
         * Quando uma mensagem entra na porta bool, a funcao handle_msg2
         * eh ativada. Com isso o fluxo de mensagem eh tratada na funcao handle_msg2
         */
        set_msg_handler(pmt::mp("bool"), 
                boost::bind(&PDU_remove_all_tags_impl::handle_msg2, 
                this, _1)); 
        
        
        message_port_register_in(pmt::mp("pdus"));  //registrando porta de entrada de mensagens pdus
        /*
         * Setando funcao de ativacao handle_msg.
         * Quando uma mensagem entra na porta pdus, a funcao handle_msg
         * eh ativada. Com isso o fluxo de mensagem eh tratada na funcao handle_msg
         */
        set_msg_handler(pmt::mp("pdus"), 
                boost::bind(&PDU_remove_all_tags_impl::handle_msg,
                this, _1));
    }

    /*
     * Our virtual destructor.
     */
    PDU_remove_all_tags_impl::~PDU_remove_all_tags_impl()
    {
    }
    
    /* Funcao de ativacao da porta bool
     * \param msg um PDU com uma mensagem booleana
     */
    void PDU_remove_all_tags_impl::handle_msg2(pmt::pmt_t msg) { 
        sense=pmt::to_bool(msg);
    
    }

    /* Funcao de ativacao da porta pdus
     * \param pdu PDU com todas as tags indesejadas
     */
    void PDU_remove_all_tags_impl::handle_msg(pmt::pmt_t pdu){
        
        /*Verifica se eh dicionario*/
        pmt::pmt_t meta = pmt::car(pdu);
        if(pmt::is_null(meta)){
          meta = pmt::make_dict();
          } else if(!pmt::is_dict(meta)){
          throw std::runtime_error("pdu_remove received non PDU input");
          }
        
        
        /*Remove tags do event_stream, da USRP e do uhdgps */
        meta = pmt::dict_delete(meta, pmt::intern("es::event_buffer"));
        meta = pmt::dict_delete(meta, pmt::intern("es::event_length"));
        meta = pmt::dict_delete(meta, pmt::intern("es::event_time"));
        meta = pmt::dict_delete(meta, pmt::intern("es::event_type"));
        meta = pmt::dict_delete(meta, pmt::intern("rx_rate"));
        meta = pmt::dict_delete(meta, pmt::intern("rx_time"));
        /*Verifica se a tag rx_freq estah presente. Se estiver o conteudo desta tag eh
         *padronizado para um formato legivel
         */
        time_t currentTime;
        struct tm *localTime;

        time( &currentTime );                   // Get the current time
        localTime = localtime( &currentTime );
        
        uint64_t time   = (localTime->tm_hour*3600) +(localTime->tm_min*60) + localTime->tm_sec;
        meta = pmt::dict_add(meta,pmt::intern("time"),pmt::from_uint64(time));
        if(pmt::dict_has_key(meta,pmt::intern("rx_freq"))){
           
            pmt::pmt_t f = pmt::cdr(pmt::dict_ref(meta,pmt::intern("rx_freq"),pmt::PMT_NIL));
            meta = pmt::dict_delete(meta, pmt::intern("rx_freq"));
            meta = pmt::dict_add(meta,pmt::intern("rx_freq"),f);// tirar o numero antes da frequencia
           
        }
        if (sense) {
            /*envia true para pdus*/
          message_port_pub(pmt::mp("pdus"), pmt::cons(meta, pmt::cdr(pdu)));
          
        }
    }
    

  } /* namespace pmt_cpp */
} /* namespace gr */

