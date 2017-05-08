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
#include <fstream>
#include "wait_first_ack_impl.h"

namespace gr {
  namespace pmt_cpp {

    wait_first_ack::sptr
    wait_first_ack::make()
    {
      return gnuradio::get_initial_sptr
        (new wait_first_ack_impl());
    }

    /*
     * The private constructor Criar uma thread com loop infinito para verificar o arquico de ack
     * Entra a primeira mensagem em first e então ela é enviada para message_repeat em loop até que o 
     * escravo tenha recebido o ack 2. Posso colocar um sleep de 3 segundos +-
     */
    wait_first_ack_impl::wait_first_ack_impl()
      : gr::block("wait_first_ack",
              gr::io_signature::make(0,0,0),
              gr::io_signature::make(0,0,0))
    {
        message_port_register_out(pmt::mp("message_repeat"));      //Registra porta de saida pdu
    	
    	message_port_register_in(pmt::mp("fisrt_message"));//Registra porta de entrada file_ready
    	set_msg_handler(pmt::mp("fisrt_message"), boost::bind(&wait_first_ack_impl::handle_msg, this, _1));
    
    }

    /*
     * Our virtual destructor.
     */
    wait_first_ack_impl::~wait_first_ack_impl()
    {
    }
    void wait_first_ack_impl::handle_msg(pmt::pmt_t msg) {
        std::fstream file; // open file
        int acks = 0;
        bool read = true;
        while(read){
            std::cout << "[SLAVE][WAIT FIRST ACK]: Wait" << std::endl;
            usleep(1000000);
            std::cout << "[SLAVE][WAIT FIRST ACK]: sleep" << std::endl;
            file.open("/tmp/ack.txt", std::ios::in);
            if(file.is_open()){
                std::string line;
                getline(file,line);

                
                if(line.compare("1") == 0){
                    read = false;
                   // remove ("/tmp/ack.txt");
                }else {
                    std::cout << "[SLAVE][WAIT FIRST ACK]: Re-send Message" << std::endl;

                    pmt::print(msg);
                    message_port_pub(pmt::mp("message_repeat"),msg);
                }
            }else {
                std::cout << "[SLAVE][WAIT FIRST ACK]: Re-send Message: " << std::endl;
                pmt::print(msg);
                message_port_pub(pmt::mp("message_repeat"),msg);
            }
            
        }
    }

    


  } /* namespace pmt_cpp */
} /* namespace gr */

