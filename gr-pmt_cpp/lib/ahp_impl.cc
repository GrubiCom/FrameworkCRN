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
#include "ahp_impl.h"
#include <sstream> 
#include <dirent.h>
#include <iostream>
namespace gr {
  namespace pmt_cpp {

    ahp::sptr
    ahp::make()
    {
      return gnuradio::get_initial_sptr
        (new ahp_impl());
    }

    /*
     * The private constructor
     */
    ahp_impl::ahp_impl()
      : gr::block("ahp",
              gr::io_signature::make(0,0,0),
              gr::io_signature::make(0,0,0))
    {
        
        message_port_register_out(pmt::mp("out"));
    	
    	message_port_register_in(pmt::mp("in"));        //Registra porta de entrada in_pdu
    	set_msg_handler(pmt::mp("in"), 
                boost::bind(&ahp_impl::handle, 
                this, _1));                                 //Seta handle_msg em in_pdu
       
    }

    /*
     * Our virtual destructor.
     */
    ahp_impl::~ahp_impl()
    {
    }

    void ahp_impl::handle(pmt::pmt_t pdu) {
        if (pmt::is_bool(pdu) and (pmt::to_bool(pdu))){
            std::fstream file;
            file.open("/tmp/res_sense.txt",std::ios::in);
            std::string str;
            getline(file,str);
            std::system("rm -rf /tmp/results/");
            
            char *message = new char[str.length() +1];
            strcpy(message,str.c_str());
            std::cout << "[AHP]: " << message << std::endl;
            int tag = 0;//isFreqRanked(message);
            if(tag == 0){
                int channels = getNumberOfChannels(message);
                float parameters[channels][MAX_PARAMETERS];
                setDataToMatriz(message, parameters, channels);
                ahp(parameters,channels);
                printMatriz(parameters,channels);
            }
            
            remove("/tmp/res_sense.txt");
            
            
        }
            
 
    }

    void ahp_impl::ahp(float parameters[][MAX_PARAMETERS], int channels) {
        float best[5] = {0,0,0,0,0};
	float frequencys[5] = {0,0,0,0,0};
	float result;
	for(int i = 0; i < channels; i++) {
		result = parameters[i][table_RSSI] * AVERAGE_RSSI;
		result += parameters[i][table_Time] * AVERAGE_TIME;
		result += parameters[i][table_Owned] * AVERAGE_OWNED;

		if(result > best[0]) {
			best[4] = best[3];
			frequencys[4] = frequencys[3];
			best[3] = best[2];
			frequencys[3] = frequencys[2];
			best[2] = best[1];
			frequencys[2] = frequencys[1];
			best[1] = best[0];
			frequencys[1] = frequencys[0];
			best[0] = result;
			frequencys[0] = parameters[i][table_Freq];
		}
		else {
			if((result > best[1]) || (result == best[0])) {
				best[4] = best[3];
				frequencys[4] = frequencys[3];
				best[3] = best[2];
				frequencys[3] = frequencys[2];
				best[2] = best[1];
				frequencys[2] = frequencys[1];
				best[1] = result;
				frequencys[1] = parameters[i][table_Freq];
			}
			else {
				if((result > best[2]) || (result == best[1])) {
					best[4] = best[3];
					frequencys[4] = frequencys[3];
					best[3] = best[2];
					frequencys[3] = frequencys[2];
					best[2] = result;
					frequencys[2] = parameters[i][table_Freq];
				}
				else {
					if((result > best[3]) || (result == best[2])) {
						best[4] = best[3];
						frequencys[4] = frequencys[3];
						best[3] = result;
						frequencys[3] = parameters[i][table_Freq];
					}
					else {
						if(result > best[4]) {
							best[4] = result;
							frequencys[4] = parameters[i][table_Freq];
						}
					}
				}
			}
		}	
	}
	std::ofstream writer;
	writer.open("/tmp/rankedAHP.txt");
        message_port_pub(pmt::mp("out"),pmt::intern("<0:3:"+boost::to_string(frequencys[0])+">"));
	for(int i = 1; i < 5; i++) {
		writer << frequencys[i] << ":" << best[i] << ";"<< std::endl;
	}
	writer.close();
	/*FILE *writer;
	fopen("rankedAHP.txt", "w"); */
    }
    int ahp_impl::isFreqRanked(char message[]) {
        char line[20];
            char aux[10];
            char aux1[10];
            int count = 0;
            float frequency;
            float rankedFreq[5] = {0,0,0,0,0};
            float rankedAHP[5] = {0,0,0,0,0};
            std::ifstream reader;
            reader.open("/tmp/rankedAHP.txt");
            if (reader.is_open()) {
                while(reader.getline(line, 20)) {
                    int i = 0;
                    while(line[i] != ':') {
                            aux[i] = line[i];
                            i++;
                    }
                    i++;
                    std::stringstream strd(aux);
                    strd >> rankedFreq[count];
                    //rankedFreq[count] = std::atof(aux);	
                    std::cout << "AHP: rankedFreq"<< rankedAHP[count] << " aux: "<< aux << std::endl;
                    while(line[i] != ';') {
                            aux1[i] = line[i];
                            i++;
                    }
                    //rankedAHP[count] = std::atof(aux);
                    std::stringstream strdo(aux1);
                    strdo >> rankedAHP[count];
                    std::cout << "AHP: rankedAHP"<< rankedAHP[count] << " aux: "<< aux1 << std::endl;
                    count ++;
                }
                reader.close();
                int counter = 0;
                int counter2 = 0;
                char number[MAX_CHARSTONUMBER];
                while(message[counter] != 0 && message[counter] != 32 && message[counter] != 10) {
                    for(int k = 0; k < MAX_CHARSTONUMBER; k++) {
                            number[k] = 0;
                    }
                    while(message[counter] != ':' && message[counter] != ';') {
                            number[counter2] = message[counter];
                            counter ++;
                            counter2 ++;
                    }
                    counter ++;
                    counter2 = 0;
                    for(int k = 0; k < MAX_CHARSTONUMBER; k++) {
                            number[k] = 0;
                    }
                    while(message[counter] != ':' && message[counter] != ';') {
                            number[counter2] = message[counter];
                            counter ++;
                            counter2 ++;
                    }
                    counter ++;
                    counter ++;
                    counter2 = 0;
                    frequency = atof(number);
                    for(int i = 0; i < 5; i++) {
                        if(frequency == rankedFreq[i]) {
                            std::ofstream writer;
                            writer.open("/tmp/rankedAHP.txt");
                            message_port_pub(pmt::mp("out"),pmt::intern("<0:3:"+boost::to_string(number)+">"));
                            for(int j = 0; j < 5; j++) {
                                if(i != j && rankedFreq != 0) {
                                    writer << rankedFreq[j] << ":" << rankedAHP[j] << ";" << std::endl;
                                }
                            }
                            writer.close();
                            return 1;
                        }
                    }

                    for(int k = 0; k < MAX_CHARSTONUMBER; k++) {
                        number[k] = 0;
                    }
                    while(message[counter] != ':' && message[counter] != ';') {
                        number[counter2] = message[counter];
                        counter ++;
                        counter2 ++;
                    }
                    counter ++;
                    counter2 = 0;
                }
            }
            return 0;
        }


    void ahp_impl::setDataToMatriz(char message[], float parameters[][MAX_PARAMETERS], int channels) {
        int counter = 0;
	int counter2 = 0;
	float aux;
	char number[MAX_CHARSTONUMBER];
	for(int i = 0; i < channels; i++) {
		for(int k = 0; k < MAX_CHARSTONUMBER; k++) {
			number[k] = 0;
		}
		while(message[counter] != ':' && message[counter] != ';') {
			number[counter2] = message[counter];
			counter ++;
			counter2 ++;
		}
		counter ++;
		counter2 = 0;
		aux = convertStringToFloat(number);
		aux = aux / 1440;
		aux = aux / 60;
		parameters[i][table_Time] = aux;
		
		for(int k = 0; k < MAX_CHARSTONUMBER; k++) {
			number[k] = 0;
		}
		while(message[counter] != ':' && message[counter] != ';') {
			number[counter2] = message[counter];
			counter ++;
			counter2 ++;
		}
		counter ++;
		counter ++;
		counter2 = 0;


                std::stringstream ss(number);

                ss >> aux;



		parameters[i][table_Freq] = aux;
		aux = aux / 6.0;
		aux = aux * 2.0;
		aux = aux - 1.0;
		parameters[i][table_Owned] = isOwned(aux); // Here
		
		for(int k = 0; k < MAX_CHARSTONUMBER; k++) {
			number[k] = 0;
		}
		while(message[counter] != ':' && message[counter] != ';') {
			number[counter2] = message[counter];
			counter ++;
			counter2 ++;
		}
		counter ++;
		counter2 = 0;
		aux = convertStringToFloat(number);
		aux /= 130;	
		parameters[i][table_RSSI] = aux;	
	}
    }

    int ahp_impl::getNumberOfChannels(char message[]) {
        int result = 0;
	int i = 0;
	while(message[i] != 0 && message[i] != 32 && message[i] != 10) {
		if(message[i] == ';') {
			result ++;
		}
		i ++;
	}
	return result;
    }
    
    void ahp_impl::printMatriz(float matriz[][MAX_PARAMETERS], int channels) {
        for(int i = 0; i < channels; i++) {
		for(int j = 0; j < MAX_PARAMETERS; j++) {
			std::cout << matriz[i][j] << "\t";
		}
		std::cout << "\n";
	}
    }

    float ahp_impl::convertStringToFloat(char number[]) {
        float result = 0;
	int j = 0;
	for(int i = MAX_CHARSTONUMBER-1; i >= 0; i--) {
		if(number[i] != 0 && number[i] != '.') {
			result += (int(number[i]) - 48) * pow(10,j);
			j++;
		}
	}
	return result;
    }
    
    float ahp_impl::isOwned(float frequency) {
        float number = frequency;
	if((number > 0.46 && number < 0.47) || (number < -0.13 && number >= -0.4) || (number < -0.53 && number > -0.54) || (number < -0.66 && number > -0.74)) {
		return 0.5;
	}
	return 1;
    }
    float ahp_impl::noiseOf(float frequency) {
        float result = 0;
	return result;
    }



  } /* namespace pmt_cpp */
} /* namespace gr */

