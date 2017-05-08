#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2015 Libério.
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

class cogmac(gr.basic_block):
    """
    docstring for block annp
    """
    def __init__(self):
        gr.basic_block.__init__(self, 
            name="cogmac", 
            in_sig=[], 
            out_sig=[]);
        
         
        self.message_port_register_in(pmt.intern("in"))           
        self.set_msg_handler(pmt.intern("in"), self.handler) 
        self.message_port_register_out(pmt.intern("out")) 
        
    def handler(self, pdu):
        if (pmt.is_bool(pdu) and (pmt.to_bool(pdu))):
            #self.s = pmt.to_python(pdu);
            self.f = open("/tmp/res_sense.txt", "r")
            self.s = self.f.readline()
            #print "s: "+self.s
            self.pos = self.s.find(";")
            self.sub = self.s[self.pos+1:]
            print self.sub
            #print "sub: "+self.sub
            pattern = re.compile(r'(:)') # caractere - e numeros 0 a 9
            i = 0;
            tag = 1;
            hour = [];
            freq = []
            power = []
            bestPower = [-0.5,-0.5,-0.5,-0.5,-0.5]
            freqFinal = ["Not", "Not", "Not", "Not", "Not"]
            rankedFreq = ["Not", "Not", "Not", "Not"] 
            rankedPower = ["Not", "Not", "Not", "Not"]
            finalMessage = ['<', '0', ':', '3', ':']
            try:
                rankExist = os.path.exists("/tmp/rankCogMac.txt")
                rankExist = False
		if(rankExist):
			j = 0
			k = 0
			l = 0
			f = open("/tmp/rankCogMac.txt", "r")
			sRank = f.readline()
                        print "sRank: "
                        print (sRank)
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
                                print "Rank"
                                print  (rankFrequency, rankPower)
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
				
				print "Result"
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
						f = open("/tmp/rankCogMac.txt", "w")
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
                                                                print "tag"
                                                                print (tag)
                                                                print "sRankp"
                                                                print (sRank)
								f.write(sRank)
								f.write(":")
								sRank = str(rankedFreq[k])
                                                                print "sRankf"
                                                                print (sRank)
								f.write(sRank)
								f.write(";")
						f.close()
                                                j = 4
                                                l = len(self.sub)
                                                
                                        
		if(tag):
                    print "entrou"
                    while(i < len(self.sub)): 
                        
                        while(self.sub[i] != ':'):
                            hour.append(self.sub[i])
                            i = i + 1
                        i = i + 1
                        hours = ''.join(hour)
                        floatHour = float(hours)
                        #print(floatHour)
                        floatHour = floatHour / 3600
                        floatHour = floatHour / 24
                        floatHour = floatHour - 0.5
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
                        print "AKI"
                        print(frequency, fPower)

                        floatFreq = float(frequency)
                        floatPower = float(fPower)
                        freq = []
                        power = []
                        hour = []
                        if(tag):
                            if(floatPower > bestPower[0]):
                                    bestPower[4] = bestPower[3]
                                    freqFinal[4] = freqFinal[3]
                                    bestPower[3] = bestPower[2]
                                    freqFinal[3] = freqFinal[2]
                                    bestPower[2] = bestPower[1]
                                    freqFinal[2] = freqFinal[1]
                                    bestPower[1] = bestPower[0]
                                    freqFinal[1] = freqFinal[0]
                                    bestPower[0] = floatPower
                                    freqFinal[0] = frequency
                            else:
                                    if((floatPower > bestPower[1]) | (floatPower == bestPower[0])):
                                            bestPower[4] = bestPower[3]
                                            freqFinal[4] = freqFinal[3]
                                            bestPower[3] = bestPower[2]
                                            freqFinal[3] = freqFinal[2]
                                            bestPower[2] = bestPower[1]
                                            freqFinal[2] = freqFinal[1]
                                            bestPower[1] = floatPower
                                            freqFinal[1] = frequency
                                    else:
                                            if((floatPower > bestPower[2]) | (floatPower == bestPower[1])):
                                                    bestPower[4] = bestPower[3]
                                                    freqFinal[4] = freqFinal[3]
                                                    bestPower[3] = bestPower[2]
                                                    freqFinal[3] = freqFinal[2]
                                                    bestPower[2] = floatPower
                                                    freqFinal[2] = frequency
                                            else:
                                                    if((floatPower > bestPower[3]) | (floatPower == bestPower[2])):
                                                            bestPower[4] = bestPower[3]
                                                            freqFinal[4] = freqFinal[3]
                                                            bestPower[3] = floatPower
                                                            freqFinal[3] = frequency
                                                    else:
                                                            if(floatPower > bestPower[4]):
                                                                    bestPower[4] = floatPower
                                                                    freqFinal[4] = frequency
                            print "bestTudo"
                            print (freqFinal,bestPower)
                    i = 0
                    #while(i < len(frequency)):
                    finalMessage.append(freqFinal[0])
                    #        i = i + 1

                    finalMessage.append('>')
                    stringFinal = ''.join(finalMessage)
                    print "[MASTERT][COGMAC]:  FINISH"
                    retorno = pmt.to_pmt(stringFinal)

                    f = open("/tmp/rankCogMac.txt", "w")
                    for i in range(1, 5):
                        print "bestPower[i]"
                        print (bestPower[i])
                        s = str(bestPower[i])
                        f.write(s)
                        f.write(":")
                        print "freqFinal[i]"
                        print (freqFinal[i])
                        f.write(freqFinal[i])
                        f.write(";")
                    f.close()

                print retorno
                
                self.message_port_pub(pmt.intern("out"), retorno);
            except:
                print  "[MASTER][COGMAC]: EXCEPTION"
                #print e
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
            #time.sleep(0.4)
            time.sleep(1)
            os.remove("/tmp/res_sense.txt")
            os.remove("/tmp/neighbors_aux.txt")
            os.remove("/tmp/neighbors.txt")
            shutil.rmtree("/tmp/Acknowledgement")
            shutil.rmtree("/tmp/results")
            time.sleep(2)
            i = 0
            while (not os.path.exists("/tmp/master_channels.txt") and i < 10):
                i = i + 1
                print  "[MASTER][COGMAC]: RETRANSMISSION "
                self.message_port_pub(pmt.intern("out"), retorno)
                time.sleep(2)
