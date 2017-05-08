#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2015 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 
import numpy, re, pmt, os, shutil,sys
import time
from gnuradio import gr
from fann2 import libfann

class annp(gr.basic_block):
    """
    docstring for block annp
    """
    def __init__(self):
        gr.basic_block.__init__(self, 
            name="annp", 
            in_sig=[], 
            out_sig=[]);
        
         
        self.message_port_register_in(pmt.intern("in"))           
        self.set_msg_handler(pmt.intern("in"), self.handler) 
        self.message_port_register_out(pmt.intern("out")) 

        
        
    def handler(self, pdu):
         if (pmt.is_bool(pdu) and (pmt.to_bool(pdu))):

            self.f = open("/tmp/res_sense.txt", "r")
            self.s = self.f.readline()
            
            
            self.sub = self.s
            print "[ANNP]: res_sense: "+self.sub

            pattern = re.compile(r'(:)') # caractere - e numeros 0 a 9
            tag = 1
            i = 0;
            hour = [];
            freq = []
            power = []
            bestPower = [-0.5,-0.5,-0.5,-0.5,-0.5]
            freqFinal = ["Not", "Not", "Not", "Not", "Not"]
            rankedFreq = ["Not", "Not", "Not", "Not"] 
            rankedPower = ["Not", "Not", "Not", "Not"]
            finalMessage = ['<', '0', ':', '3', ':']
            try:
		rankExist = os.path.exists("/tmp/rankANN.txt")
                rankExist = False
		if(rankExist):
			j = 0
			k = 0
			l = 0
			f = open("/tmp/rankANN.txt", "r")
			sRank = f.readline()
                        #print "sRank: "+ sRank
			f.close()
			while(j < len(sRank)):
				while(sRank[j] != ":"):
					power.append(sRank[j])
					j = j + 1
				j = j + 1
				while(sRank[j] != ";"):
					freq.append(sRank[j])
					j = j + 1
				j = j + 1
				
				rankFrequency = ''.join(freq)
				rankPower = ''.join(power)
				rankedFreq[k] = float(rankFrequency)
				rankedPower[k] = float(rankPower)
				k = k + 1
				freq = []
				power = []
			while(l < len(self.sub)): 
				while(self.sub[l] != ':'):
					hour.append(self.sub[l])
					l = l + 1
				l = l + 1
				
				while(self.sub[l] != ':'):
					freq.append(self.sub[l])
					l = l + 1

				l = l + 2

				while(self.sub[l] != ';'):
					power.append(self.sub[l])
					l = l + 1
				l = l + 1
				frequency = ''.join(freq)

				fPower = ''.join(power)
				
				hours = ''.join(hour)
				
				
				print  (frequency, fPower)

				floatFreq = float(frequency)
				floatPower = float(fPower)
				floatHour = float(hours)
				
                                
                                freq = []
				power = []
                                j = 0
				for j in range(0, 4):
                                        #print (j)
                                        #print (floatFreq, rankedFreq)
					if((floatFreq == rankedFreq[j])& (rankedFreq[j] !="Not")):
                                                print (j)
                                                print (floatFreq, rankedFreq[j])
						i = len(self.sub)
						tag = 0
						f = open("/tmp/rankANN.txt", "w")
						k = 0
						#while(k < len(frequency)):
                                                finalMessage.append(str(floatFreq))
                                                
						#	k = k + 1

						finalMessage.append('>')
						stringFinal = ''.join(finalMessage)
						#print "ANN FINISH"
						retorno = pmt.to_pmt(stringFinal)
						for k in range(0, 4):
                                                        print(k,j)
							if((k != j) &  (rankedFreq[k] !=0) & (rankedFreq[k] !="Not")):
								sRank = str(rankedPower[k])
								f.write(sRank)
								f.write(":")
								sRank = str(rankedFreq[k])
								f.write(sRank)
								f.write(";")
						f.close()
                                                j = 4
                                                l = len(self.sub)
		if(tag):
			while(i < len(self.sub)): 
			    while(self.sub[i] != ':'):
				hour.append(self.sub[i])
				i = i + 1
			    i = i + 1
			    
			    while(self.sub[i] != ':'):
				    freq.append(self.sub[i])
				    i = i + 1

			    i = i + 2

			    while(self.sub[i] != ';'):
				    power.append(self.sub[i])
				    i = i + 1
			    i = i + 1
			    frequency = ''.join(freq)

			    fPower = ''.join(power)
			    
			    hours = ''.join(hour)
			    
			    
			    print  (frequency, fPower)

			    floatFreq = float(frequency)
			    floatPower = float(fPower)
			    floatHour = float(hours)
			    if(tag):
				    if((floatFreq < 0.8) | (0.85 < floatFreq < 2.4) | (floatFreq > 2.43)):

					    floatFreq = floatFreq / 3
					    floatFreq = floatFreq - 1

					    floatPower = floatPower - 90
					    floatPower = floatPower / 100
					    floatPower = floatPower * -1


					    freq = []
					    power = []
					    hour = []
					    ann = libfann.neural_net()
					    ann.create_from_file("/opt/FrameworkCRN/final_data_config.net")
					    result = ann.run([floatFreq, floatPower])
					    floatResult = float(result[0])
				    else:
					    if(floatFreq < 1):
						    floatFreq = floatFreq - 1
					    else:
						    floatFreq = floatFreq - 2.4
						    floatFreq = floatFreq / 2
						    floatFreq = floatFreq * 10
						    floatFreq = floatFreq - 0.1

					    floatPower = floatPower - 90
					    floatPower = floatPower / 100
					    floatPower = floatPower * -1
					    
					    floatHour = floatHour / 3600
					    floatHour = floatHour / 24
					    floatHour = floatHour - 0.5
					    
                                            
					    #print("[MASTER][ANNP]: Mark 0")
					    #print"[MASTER][ANNP]: Hour1: %d" % (floatHour)
					    freq = []
					    power = []
					    hour = []
					    ann = libfann.neural_net()

					    ann.create_from_file("/opt/FrameworkCRN/final_data_config.net")
					    result = ann.run([floatHour,floatFreq, floatPower])
					    floatResult = float(result[0])
					    if (floatResult > 0.2):                              
						floatResult = floatResult - 0.3
                                    #print "RESULT"
				    #print (result)
				    if(floatResult > bestPower[0]):
								bestPower[4] = bestPower[3]
								freqFinal[4] = freqFinal[3]
								bestPower[3] = bestPower[2]
								freqFinal[3] = freqFinal[2]
								bestPower[2] = bestPower[1]
								freqFinal[2] = freqFinal[1]
								bestPower[1] = bestPower[0]
								freqFinal[1] = freqFinal[0]
								bestPower[0] = floatResult
								freqFinal[0] = frequency
				    else:
					    if((floatResult > bestPower[1]) | (floatResult == bestPower[0])):
						    bestPower[4] = bestPower[3]
						    freqFinal[4] = freqFinal[3]
						    bestPower[3] = bestPower[2]
						    freqFinal[3] = freqFinal[2]
						    bestPower[2] = bestPower[1]
						    freqFinal[2] = freqFinal[1]
						    bestPower[1] = floatResult
						    freqFinal[1] = frequency
					    else:
						    if((floatResult > bestPower[2]) | (floatResult == bestPower[1])):
							    bestPower[4] = bestPower[3]
							    freqFinal[4] = freqFinal[3]
							    bestPower[3] = bestPower[2]
							    freqFinal[3] = freqFinal[2]
							    bestPower[2] = floatResult
							    freqFinal[2] = frequency
						    else:
							    if((floatResult > bestPower[3]) | (floatResult == bestPower[2])):
								    bestPower[4] = bestPower[3]
								    freqFinal[4] = freqFinal[3]
								    bestPower[3] = floatResult
								    freqFinal[3] = frequency
							    else:
								    if(floatResult > bestPower[4]):
									    bestPower[4] = floatResult
									    freqFinal[4] = frequency
			    #print "[MASTER][ANNP]: Result " + floatResult+ " Power: "+bestPower+ " Final: "+ freqFinal
			i = 0

                        finalMessage.append(freqFinal[0]) #Qualquer coisa vou trocar pra freqFinal[0][i]


			finalMessage.append('>')
			stringFinal = ''.join(finalMessage)
			print "[MASTER][ANNP]: RNA FINISH"

			retorno = pmt.to_pmt(stringFinal)
			
			f = open("/tmp/rankANN.txt", "w")
			for i in range(1, 5):
                            s = str(bestPower[i])
                            f.write(s)
                            f.write(":")
                            f.write(freqFinal[i])
                            f.write(";")
						


			
			f.close()
                print retorno
                self.message_port_pub(pmt.intern("out"), retorno);
                
                #self.message_port_pub(pmt.intern("out"), pmt.intern("<0:3:6.0>"));
            except Exception as e:
                print  "[MASTER][ANNP]: EXCEPTION"
                print e
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                i = 0
                #while(i < len(freqFinal)):
                finalMessage.append(freqFinal[0])
                
                #        i = i + 1

                finalMessage.append('>')
                stringFinal = ''.join(finalMessage)
                print "[MASTER][ANNP]: RNA FINISH EXCEPTION"

                retorno = pmt.to_pmt(stringFinal)
                print retorno
                self.message_port_pub(pmt.intern("out"), retorno);
                
                #self.message_port_pub(pmt.intern("out"), pmt.intern("<0:3:6.0>"));
            print  "[MASTER][ANNP]: ERASE FILES (res_sense,neightbors_aux,neigtbor) AND DIRECTORY (Acknowledgement AND results)"
            
            time.sleep(1)
            #try:
                #shutil.rmtree("/tmp/Acknowledgement")
                #shutil.rmtree("/tmp/results")
                #os.remove("/tmp/res_sense.txt")
                #os.remove("/tmp/neighbors_aux.txt")
                #os.remove("/tmp/neighbors.txt")
                
            #except OSError as e:
            #    print e
                
            time.sleep(2)
            i = 0
            while (not os.path.exists("/tmp/master_channels.txt") and i < 10):
                i = i + 1
                print  "[MASTER][ANNP]: RETRANSMISSION "
                self.message_port_pub(pmt.intern("out"), retorno)
                time.sleep(2)
                

