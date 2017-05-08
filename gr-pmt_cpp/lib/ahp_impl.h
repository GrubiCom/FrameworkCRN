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

#ifndef INCLUDED_PMT_CPP_AHP_IMPL_H
#define INCLUDED_PMT_CPP_AHP_IMPL_H

#include <pmt_cpp/ahp.h>
#include <fstream>

#define MAX_PARAMETERS 4
#define MAX_CHARSTONUMBER 9
#define AVERAGE_OWNED 0.62
#define AVERAGE_RSSI 0.24
#define AVERAGE_TIME 0.13

enum table_ids {
	table_RSSI,
	table_Time,
	table_Owned,
	table_Freq
};

typedef enum table_ids control;


namespace gr {
  namespace pmt_cpp {

    class ahp_impl : public ahp
    {
     private:
      // Nothing to declare in this block.
         int getNumberOfChannels(char[]); /* Pega a mensagem e inicial e retorna o número de canais. */
        void setDataToMatriz(char[], float[][MAX_PARAMETERS], int); /* Pega a mensagem inicial e coloca em uma matriz de parâmetros. */
        void ahp(float[][MAX_PARAMETERS], int);
        float noiseOf(float);
        float isOwned(float);
        float convertStringToFloat(char[]);
        void printMatriz(float[][MAX_PARAMETERS], int);
        int isFreqRanked(char[]); /* Checa se existe um arquivo guardado com as rankeadas, e se nesse arquivo contém alguma frequencia dentre as passadas. */
       
     public:
      ahp_impl();
      ~ahp_impl();
      void handle(pmt::pmt_t pdu); 
      
    };

  } // namespace pmt_cpp
} // namespace gr

#endif /* INCLUDED_PMT_CPP_AHP_IMPL_H */
