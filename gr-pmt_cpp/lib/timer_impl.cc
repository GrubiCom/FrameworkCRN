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
#include "timer_impl.h"
//#include "time_impl.h
#include <fstream>
#include <dirent.h>
#include <cstdlib>

bool t = false;
namespace gr {
  namespace pmt_cpp {

    timer::sptr
    timer::make()
    {
      return gnuradio::get_initial_sptr
        (new timer_impl());
    }

    /*
     * The private constructor
     */
    timer_impl::timer_impl()
      : gr::block("timer",
              gr::io_signature::make(0,0,0),
              gr::io_signature::make(0,0,0))
    {
        message_port_register_in(pmt::mp("in"));
        set_msg_handler(pmt::mp("in"), boost::bind(&timer_impl::handle, this, _1));
        message_port_register_in(pmt::mp("in2"));
        set_msg_handler(pmt::mp("in2"), boost::bind(&timer_impl::handle1, this, _1));
        message_port_register_out(pmt::mp("out"));
    }

    /*
     * Our virtual destructor.
     */
    timer_impl::~timer_impl()
    {
    }
    void timer_impl::handle1(pmt::pmt_t pdu) {
        t = false;
    }

    void timer_impl::handle(pmt::pmt_t pdu) {
        if(!t){
            t = true;            
            sleep(25);
            if(t){
                DIR *dir = 0;
                struct dirent *entrada = 0;
                //unsigned char isDir = 0x4;
                unsigned char isFile = 0x8;

                dir = opendir ("/tmp/results/");

                if (dir == 0) {
                    std::cerr << "[MASTER][TIMER]: Nao foi possivel abrir diretorio." << std::endl;
                    //exit (1);
                }else{

                    //Iterar sobre o diretorio
                    while (entrada = readdir (dir)){
                        if (entrada->d_type == isFile){
                            std::cout << entrada->d_name << std::endl;

                            std::ofstream out;
                            std::string filename = "/tmp/results/" + boost::to_string(entrada->d_name);
                            std::cout << filename << std::endl;
                            std::ifstream file;
                            file.open(filename.c_str());

                           if(file.is_open()){

                                std::string line;
                                getline(file,line);
                                int pos = line.find(";");
                                std::string sub = line.substr(pos+1);
                                out.open("/tmp/res_sense.txt", std::ios::app);
                                out << sub;


                            }
                            out.close();
                            file.close();

                        }
                    }
               
                    std::cout << "[MASTER][TIMER]: Init RNA" << std::endl;
                    message_port_pub(pmt::mp("out"),pmt::from_bool(true)); 
                }
            }
        }
    }

    

  } /* namespace pmt_cpp */
} /* namespace gr */

