#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2016 <+YOU OR YOUR COMPANY+>.
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

import numpy as np
from gnuradio import gr
import re, pmt, os, shutil,sys
import pmt
import time
from sklearn.ensemble import RandomForestClassifier #use RandomForestRegressor for regression problem
from sklearn.externals import joblib

class RandomForest(gr.basic_block):
    """
    docstring for block RandomForest
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="RandomForest",
            in_sig=[],
            out_sig=[]);
            
        self.message_port_register_in(pmt.intern("in"))           
        self.set_msg_handler(pmt.intern("in"), self.handler) 
        self.message_port_register_out(pmt.intern("out")) 
        #self.message_port_register_out(pmt.intern("out"))

    #handler
    #funcao que armazena os dados em um arquivo
    def handler(self, pdu):
        if (pmt.is_bool(pdu) and (pmt.to_bool(pdu))):
            print "INIT RANDOM FOREST"
            self.f = open("/tmp/res_sense.txt", "r")
            self.s = self.f.readline()
            i = 0;
            hour = [];
            freq = []
            power = []
            bestPower = -0.5
            try:
                while(i < len(self.s)):#run thru the whole list
                    while(self.s[i] != ':'):#get the hour
                        hour.append(self.s[i])
                        i = i + 1
                    hour.append(' ')    
                    i = i + 1

                    while(self.s[i] != ':'):#get the frequency
                        freq.append(self.s[i])
                        i = i + 1
                    freq.append(' ')
                    i = i + 2

                    while(self.s[i] != ';'):#get the power
                        power.append(self.s[i])
                        i = i + 1
                    i = i + 1
                    power.append(' ')

                    frequency = ''.join(freq)

                    fPower = ''.join(power)

                    hours = ''.join(hour)
                arrayhour = hours.split()#put the elements into an array
                arrayFreq = frequency.split()
                arrayPower = fPower.split()
                matrix = []
                for i in range(len(arrayhour)):#create a 2d array from 2 1d array
                    matrix.append([arrayhour[i], arrayFreq[i]])

                samples = np.column_stack((matrix,arrayPower))#add one column to the 2d array

                floatSamples = samples.astype(float)#change elements to float
                for i in range(len(floatSamples)):#run normalization for samples
                    floatSamples[i][0] = floatSamples[i][0] /3600
                    floatSamples[i][2] = floatSamples[i][2] * -1
                    floatSamples[i][0] = int(floatSamples[i][0])
                    floatSamples[i][2] = int(floatSamples[i][2])

                clf = joblib.load("/home/fileconfig.forest")#get random forest configuration
                predicted = clf.predict(floatSamples)#do the predictions

                m = max(predicted)#find the best result
                arrayofIndices = [i for i, j in enumerate(predicted) if j == m]#find best result positions in the array

                result = -0.5
                for i in range(len(arrayofIndices)):#choose the highest frequency
                    if(result < floatSamples[arrayofIndices[i]][1]):
                        result = floatSamples[arrayofIndices[i]][1]
                finalMessage = ['<', '0', ':', '3', ':']
                finalMessage.append(str(result))
                finalMessage.append('>')    
                stringFinal = ''.join(finalMessage)
                retorno = pmt.to_pmt(stringFinal)
                self.f.close()
                self.message_port_pub(pmt.intern("out"), retorno);





                time.sleep(1)
                try:
                    shutil.rmtree("/tmp/Acknowledgement")
                    shutil.rmtree("/tmp/results")
                    os.remove("/tmp/res_sense.txt")
                    #os.remove("/tmp/neighbors_aux.txt")
                    #os.remove("/tmp/neighbors.txt")

                except OSError as e:
                    print e

                time.sleep(2)
                i = 0
                while (not os.path.exists("/tmp/master_channels.txt") and i < 10):
                    i = i + 1
                    print  "[MASTER][RF]: RETRANSMISSION "
                    self.message_port_pub(pmt.intern("out"), retorno)
                    time.sleep(2)
            except OSError as e:
                shutil.rmtree("/tmp/Acknowledgement")
                shutil.rmtree("/tmp/results")
                os.remove("/tmp/res_sense.txt")
                #os.remove("/tmp/neighbors_aux.txt")
                #os.remove("/tmp/neighbors.txt")