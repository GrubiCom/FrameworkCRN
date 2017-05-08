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
#include "preprocessor_master_impl.h"
#include "pmt_cpp/timer.h"
#include <dirent.h>
#include <cstdlib>

namespace gr {
  namespace pmt_cpp {

    preprocessor_master::sptr
    preprocessor_master::make()
    {
      return gnuradio::get_initial_sptr
        (new preprocessor_master_impl());
    }

    /*
     * The private constructor
     */
    preprocessor_master_impl::preprocessor_master_impl()
      : gr::block("preprocessor_master",
              gr::io_signature::make(0,0,0),
              gr::io_signature::make(0,0,0))
    {
        message_port_register_out(pmt::mp("rna_file"));
        message_port_register_out(pmt::mp("tuned"));
        message_port_register_in(pmt::mp("id_neighbor"));
        set_msg_handler(pmt::mp("id_neighbor"), boost::bind(&preprocessor_master_impl::handle, this, _1));
 
    }


    preprocessor_master_impl::~preprocessor_master_impl()
    {
    }


    void preprocessor_master_impl::handle(pmt::pmt_t p) {
        if(pmt::dict_has_key(p,pmt::intern("ID"))){
            
            pmt::pmt_t key = pmt::dict_ref(p, pmt::string_to_symbol("ID"), pmt::PMT_NIL);
            std::string id_neighbor = pmt::symbol_to_string(key);
            
            std::fstream file,aux;
            std::string filename = "/tmp/neighbors.txt";
            std::string auxname = "/tmp/neighbors_aux.txt";
            
            std::string neighbor_f, neighbor_aux,lines;
            file.open(filename.c_str(), std::ios::in | std::ios::out);
            file.seekp(file.beg);
            
           

            int id,f;
            id = std::atoi(id_neighbor.c_str());

            
            if(file.is_open()){
                while(getline(file,neighbor_f)){
                    lines.append(neighbor_f);
                    lines.append(";");
                }
                std::cout << lines << std::endl;
                for (int i =0 ; i < lines.length(); i++){
                    if(lines[i] != ';'){
                        f = lines[i] - '0';
                        if(id == f ){
                            aux.open(auxname.c_str(), std::ios::in | std::ios::out| std::ios::app );
                            aux << id << ";" ;


                            aux.close();
                        }
                    }
                }
                
                file.close();
            }
            file.open(filename.c_str(), std::ios::in | std::ios::out);
            aux.open(auxname.c_str(), std::ios::in | std::ios::out);

            
            getline(aux,neighbor_aux); 
            
            file.close();
            aux.close();
           
            
            if(neighbor_aux.length() == lines.length()){
                DIR *dir = 0;
                struct dirent *entrada = 0;

                unsigned char isFile = 0x8;

                dir = opendir ("/tmp/results/");

                if (dir == 0) {
                    std::cerr << "[MASTER][PREPROCESSOR MASTER]: Nao foi possivel abrir diretorio." << std::endl;
                    //exit (1);
                }

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
               
                std::cout << "[MASTER][PREPROCESSOR MASTER]: Init RNA" << std::endl;
                message_port_pub(pmt::mp("rna_file"),pmt::from_bool(true)); 
                
                
                
                closedir (dir);
                
            }
        }
    }

    

  } /* namespace pmt_cpp */
} /* namespace gr */

