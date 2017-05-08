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
#include "file_connect_impl.h"
/*
 * Bloco file_connect
 * Este bloco faz o chaveamento entre o consumo do fluxo de dados pelo bloco json_File
 * e pelo bloco Null_Sink. Quando o fluxo precisa ser consumido este bloco reenvia o fluxo para
 * o json_File. Quando o fluxo não precisa ser consumido ele eh reenviado para o Null_Sink.
 */
namespace gr {
  namespace pmt_cpp {

    /*Funcao make do bloco file_connect 
     */
    file_connect::sptr
    file_connect::make()
    {
      return gnuradio::get_initial_sptr
        (new file_connect_impl());
    }

    /*
     * The private constructor
     */
    file_connect_impl::file_connect_impl()
      : gr::block("file_connect",
              gr::io_signature::make(1, 1, sizeof(gr_complex)),     //Registra uma entrada de fluxo do tipo gr_complex
              gr::io_signature::make(2, 2, sizeof(gr_complex)))     //Registra duas saidas de fluxo do tipo gr_complex
    {
        message_port_register_in(pmt::mp("in_pdu"));                //Registra entrada de mensagens in_pdu

        set_msg_handler(pmt::mp("in_pdu"), 
                boost::bind(&file_connect_impl::handle_msg, 
                this, _1));                                         //Registra a funcao handle_msg na entrada de mensagens in_pdu
        sense = false;                                              //Inicializa sense como falso
        
        message_port_register_out(pmt::mp("bool"));                 //Registra porta mensagem de saida bool
    }

    /*
     * Our virtual destructor.
     */
    file_connect_impl::~file_connect_impl()
    {
    }
    
    /*handle_msg
     * \param msg PDU contendo um booleano
     */
    void file_connect_impl::handle_msg(pmt::pmt_t msg) {

        sense=pmt::to_bool(msg);
    }

    /*
     * Funcao criada pelo gnuradio
     */
    void
    file_connect_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
        unsigned ninputs = ninput_items_required.size ();// relação 1:1
        for(unsigned i = 0; i < ninputs; i++)
            ninput_items_required[i] = noutput_items;
    }

    /*
     * Funcao criada pelo gnuradio.
     * general_work eh uma funcao para tratar o fluxo de dados     
     */
    int
    file_connect_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
        const gr_complex *in = (const gr_complex *) input_items[0]; //Entrada de fluxo in
        gr_complex *out1 = (gr_complex *) output_items[0];          //Saida de fluxo out1
        gr_complex *out2 = (gr_complex *) output_items[1];          //Saida de fluxo out2
        /*
         * Se estiver no modo sense o fluxo é repassado para a saida de fluxo out1
         */
        if(sense){
            for(int i = 0; i< noutput_items ;i++){
                out1[i] = in[i]; // repassa fluxo para out1. Não altera o conteudo do fluxo
            }
            
            /*
             * Cria um pmt com a tag sense no valor true
             */
            pmt::pmt_t p_dict1  = pmt::make_dict();
            p_dict1 = pmt::dict_add(p_dict1, pmt::string_to_symbol("sense"), pmt::PMT_T);
            pmt::pmt_t senset1 = pmt::PMT_NIL;
            senset1 = pmt::dict_ref(p_dict1, pmt::string_to_symbol("sense"), pmt::PMT_NIL);
           
                    
            message_port_pub(pmt::mp("bool"), senset1);     //Envia pmt senset1 para bool
            consume_each (noutput_items);                   //Consome fluxo. Funcao do gnuradio que permite coletar informacoes do fluxo de dados proveniente da USRP
        } else {
            /*
             * Se modo sense estiver desligado. O fluxo de dados coletados pela USRP eh desconsiderado com o bloco Null_SInk              
             */
            for(int i = 0; i< noutput_items ;i++){
                out2[i] = in[i];  // repassa fluxo para out2. Não altera o conteudo do fluxo
                
            }
            /*
             * Cria um pmt com a tag sense no valor true
             */
            pmt::pmt_t p_dict1  = pmt::make_dict();
            p_dict1 = pmt::dict_add(p_dict1, pmt::string_to_symbol("sense"), pmt::PMT_F);
            pmt::pmt_t senset1 = pmt::PMT_NIL;
            senset1 = pmt::dict_ref(p_dict1, pmt::string_to_symbol("sense"), pmt::PMT_NIL);
                
            message_port_pub(pmt::mp("bool"), senset1);     //Envia pmt senset1 para bool.
            consume_each (noutput_items);                   //Consome fluxo.
            //return 
        }
        // Tell runtime system how many input items we consumed on
        // each input stream.
        

        // Tell runtime system how many output items we produced.
        return noutput_items;;
    }

  } /* namespace pmt_cpp */
} /* namespace gr */

