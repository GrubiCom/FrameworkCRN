#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2017 <+YOU OR YOUR COMPANY+>.
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

from gnuradio import gr
import numpy as np
import hmms
import re
import pmt
import os
import shutil
import sys
import pmt
import time




class HMM(gr.basic_block):
    """
    docstring for block HMM
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="HMM",
            in_sig=[],
            out_sig=[]);
            
        self.message_port_register_in(pmt.intern("in"))           
        self.set_msg_handler(pmt.intern("in"), self.handler) 
        self.message_port_register_out(pmt.intern("out")) 
        #self.message_port_register_out(pmt.intern("out"))

    
    
    #funcao que armazena os dados em um arquivo
    def handler(self, pdu):
        if (pmt.is_bool(pdu) and (pmt.to_bool(pdu))):
            print "INIT HMM"
            self.f = open("/tmp/res_sense.txt", "r")
            self.s = self.f.readline()
            i = 0
            hour = []
            freq = []
            power = []
            #s = "52287:0.8:-114;52288:0.82:-92;52288:0.84:-114;52289:0.86:-115;52290:0.88:-106;52290:0.9:-115;52291:0.92:-115;52291:0.94:-116;52292:0.96:-114;52293:0.98:-117;52293:1:-117;52294:1.02:-117;52295:1.04:-117;52295:1.06:-117;52296:1.08:-117;52296:1.1:-117;52297:1.12:-116;52297:1.14:-117;52298:1.16:-116;52299:1.18:-116;52299:1.2:-116;52300:1.22:-115;52300:1.24:-115;52301:1.26:-115;52302:1.28:-114;52302:1.3:-115;52303:1.32:-115;52303:1.34:-114;52304:1.36:-113;52305:1.38:-113;52305:1.4:-114;52306:1.42:-113;52306:1.44:-112;52307:1.46:-112;52308:1.48:-113;52308:1.5:-113;52309:1.52:-113;52309:1.54:-112;52310:1.56:-113;52311:1.58:-114;52311:1.6:-114;52312:1.62:-113;52313:1.64:-110;52313:1.66:-113;52314:1.68:-91;52314:1.7:-112;52315:1.72:-113;52315:1.74:-113;52316:1.76:-114;52317:1.78:-113;52317:1.8:-110;52318:1.82:-104;52318:1.84:-108;52319:1.86:-110;52320:1.88:-105;52320:1.9:-110;52321:1.92:-110;52322:1.94:-112;52322:1.96:-113;52323:1.98:-111;52323:2:-111;52324:2.02:-112;52324:2.04:-113;52325:2.06:-114;52326:2.08:-114;52326:2.1:-114;52327:2.12:-110;52328:2.14:-113;52328:2.16:-114;52329:2.18:-115;52329:2.2:-116;52330:2.22:-115;52331:2.24:-113;52331:2.26:-111;52332:2.28:-110;52332:2.3:-109;52333:2.32:-108;52333:2.34:-106;52334:2.36:-106;52335:2.38:-106;52335:2.4:-106;52336:2.42:-105;52336:2.44:-100;52337:2.46:-80;52338:2.48:-106;52338:2.5:-104;52339:2.52:-106;52339:2.54:-106;52340:2.56:-107;52341:2.58:-109;52341:2.6:-109;52342:2.62:-109;52342:2.64:-110;52343:2.66:-110;52344:2.68:-110;52344:2.7:-110;52345:2.72:-111;52345:2.74:-109;52346:2.76:-108;"
            hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
            path = "/home/luccas/Dropbox/Mestrado Importantes/HMM DOC/HMM test/HMM_config/"
            try:
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
                except OSError as e:
                    print e
                
                matrix = []

                for i in range(len(arrayhour)):#create a 2d array from 2 1d array
                        matrix.append([arrayhour[i], arrayFreq[i]])
                samples = np.column_stack((matrix,arrayPower))#add one column to the 2d array
                floatSamples = samples.astype(float)#change elements to float
                for i in range(len(floatSamples)):#run normalization for samples
                        floatSamples[i][0] = int(floatSamples[i][0] /3600)
                        floatSamples[i][2] = int(floatSamples[i][2] * -1)
                #print floatSamples
                #0
                seq_0_08 = []
                seq_0_081 = []
                seq_0_082 = []
                seq_0_083 = []
                seq_0_084 = []
                seq_0_085 = []
                seq_0_086 = []
                seq_0_087 = []
                seq_0_088 = []
                seq_0_089 = []
                seq_0_090 = []
                seq_0_091 = []
                seq_0_240 = []
                seq_0_241 = []
                seq_0_242 = []
                seq_0_243 = []
                seq_0_244 = []
                seq_0_245 = []
                seq_0_246 = []
                seq_0_247 = []
                seq_0_248 = []
                seq_0_249 = []
                seq_0_571 = []
                seq_0_572 = []
                seq_0_573 = []
                seq_0_574 = []
                seq_0_575 = []
                seq_0_576 = []
                seq_0_577 = []
                seq_0_578 = []
                seq_0_579 = []
                seq_0_580 = []
                seq_0_581 = []
                seq_0_582 = []
                seq_0_583 = []
                seq_0_584 = []
                seq_0_585 = []
                seq_0_586 = []
                seq_0_587 = []
                #1
                seq_1_08 = []
                seq_1_081 = []
                seq_1_082 = []
                seq_1_083 = []
                seq_1_084 = []
                seq_1_085 = []
                seq_1_086 = []
                seq_1_087 = []
                seq_1_088 = []
                seq_1_089 = []
                seq_1_090 = []
                seq_1_091 = []
                seq_1_240 = []
                seq_1_241 = []
                seq_1_242 = []
                seq_1_243 = []
                seq_1_244 = []
                seq_1_245 = []
                seq_1_246 = []
                seq_1_247 = []
                seq_1_248 = []
                seq_1_249 = []
                seq_1_571 = []
                seq_1_572 = []
                seq_1_573 = []
                seq_1_574 = []
                seq_1_575 = []
                seq_1_576 = []
                seq_1_577 = []
                seq_1_578 = []
                seq_1_579 = []
                seq_1_580 = []
                seq_1_581 = []
                seq_1_582 = []
                seq_1_583 = []
                seq_1_584 = []
                seq_1_585 = []
                seq_1_586 = []
                seq_1_587 = []
                #2
                seq_2_08 = []
                seq_2_081 = []
                seq_2_082 = []
                seq_2_083 = []
                seq_2_084 = []
                seq_2_085 = []
                seq_2_086 = []
                seq_2_087 = []
                seq_2_088 = []
                seq_2_089 = []
                seq_2_090 = []
                seq_2_091 = []
                seq_2_240 = []
                seq_2_241 = []
                seq_2_242 = []
                seq_2_243 = []
                seq_2_244 = []
                seq_2_245 = []
                seq_2_246 = []
                seq_2_247 = []
                seq_2_248 = []
                seq_2_249 = []
                seq_2_571 = []
                seq_2_572 = []
                seq_2_573 = []
                seq_2_574 = []
                seq_2_575 = []
                seq_2_576 = []
                seq_2_577 = []
                seq_2_578 = []
                seq_2_579 = []
                seq_2_580 = []
                seq_2_581 = []
                seq_2_582 = []
                seq_2_583 = []
                seq_2_584 = []
                seq_2_585 = []
                seq_2_586 = []
                seq_2_587 = []
                #3
                seq_3_08 = []
                seq_3_081 = []
                seq_3_082 = []
                seq_3_083 = []
                seq_3_084 = []
                seq_3_085 = []
                seq_3_086 = []
                seq_3_087 = []
                seq_3_088 = []
                seq_3_089 = []
                seq_3_090 = []
                seq_3_091 = []
                seq_3_240 = []
                seq_3_241 = []
                seq_3_242 = []
                seq_3_243 = []
                seq_3_244 = []
                seq_3_245 = []
                seq_3_246 = []
                seq_3_247 = []
                seq_3_248 = []
                seq_3_249 = []
                seq_3_571 = []
                seq_3_572 = []
                seq_3_573 = []
                seq_3_574 = []
                seq_3_575 = []
                seq_3_576 = []
                seq_3_577 = []
                seq_3_578 = []
                seq_3_579 = []
                seq_3_580 = []
                seq_3_581 = []
                seq_3_582 = []
                seq_3_583 = []
                seq_3_584 = []
                seq_3_585 = []
                seq_3_586 = []
                seq_3_587 = []
                #4
                seq_4_08 = []
                seq_4_081 = []
                seq_4_082 = []
                seq_4_083 = []
                seq_4_084 = []
                seq_4_085 = []
                seq_4_086 = []
                seq_4_087 = []
                seq_4_088 = []
                seq_4_089 = []
                seq_4_090 = []
                seq_4_091 = []
                seq_4_240 = []
                seq_4_241 = []
                seq_4_242 = []
                seq_4_243 = []
                seq_4_244 = []
                seq_4_245 = []
                seq_4_246 = []
                seq_4_247 = []
                seq_4_248 = []
                seq_4_249 = []
                seq_4_571 = []
                seq_4_572 = []
                seq_4_573 = []
                seq_4_574 = []
                seq_4_575 = []
                seq_4_576 = []
                seq_4_577 = []
                seq_4_578 = []
                seq_4_579 = []
                seq_4_580 = []
                seq_4_581 = []
                seq_4_582 = []
                seq_4_583 = []
                seq_4_584 = []
                seq_4_585 = []
                seq_4_586 = []
                seq_4_587 = []
                #5
                seq_5_08 = []
                seq_5_081 = []
                seq_5_082 = []
                seq_5_083 = []
                seq_5_084 = []
                seq_5_085 = []
                seq_5_086 = []
                seq_5_087 = []
                seq_5_088 = []
                seq_5_089 = []
                seq_5_090 = []
                seq_5_091 = []
                seq_5_240 = []
                seq_5_241 = []
                seq_5_242 = []
                seq_5_243 = []
                seq_5_244 = []
                seq_5_245 = []
                seq_5_246 = []
                seq_5_247 = []
                seq_5_248 = []
                seq_5_249 = []
                seq_5_571 = []
                seq_5_572 = []
                seq_5_573 = []
                seq_5_574 = []
                seq_5_575 = []
                seq_5_576 = []
                seq_5_577 = []
                seq_5_578 = []
                seq_5_579 = []
                seq_5_580 = []
                seq_5_581 = []
                seq_5_582 = []
                seq_5_583 = []
                seq_5_584 = []
                seq_5_585 = []
                seq_5_586 = []
                seq_5_587 = []
                #6
                seq_6_08 = []
                seq_6_081 = []
                seq_6_082 = []
                seq_6_083 = []
                seq_6_084 = []
                seq_6_085 = []
                seq_6_086 = []
                seq_6_087 = []
                seq_6_088 = []
                seq_6_089 = []
                seq_6_090 = []
                seq_6_091 = []
                seq_6_240 = []
                seq_6_241 = []
                seq_6_242 = []
                seq_6_243 = []
                seq_6_244 = []
                seq_6_245 = []
                seq_6_246 = []
                seq_6_247 = []
                seq_6_248 = []
                seq_6_249 = []
                seq_6_571 = []
                seq_6_572 = []
                seq_6_573 = []
                seq_6_574 = []
                seq_6_575 = []
                seq_6_576 = []
                seq_6_577 = []
                seq_6_578 = []
                seq_6_579 = []
                seq_6_580 = []
                seq_6_581 = []
                seq_6_582 = []
                seq_6_583 = []
                seq_6_584 = []
                seq_6_585 = []
                seq_6_586 = []
                seq_6_587 = []
                #7
                seq_7_08 = []
                seq_7_081 = []
                seq_7_082 = []
                seq_7_083 = []
                seq_7_084 = []
                seq_7_085 = []
                seq_7_086 = []
                seq_7_087 = []
                seq_7_088 = []
                seq_7_089 = []
                seq_7_090 = []
                seq_7_091 = []
                seq_7_240 = []
                seq_7_241 = []
                seq_7_242 = []
                seq_7_243 = []
                seq_7_244 = []
                seq_7_245 = []
                seq_7_246 = []
                seq_7_247 = []
                seq_7_248 = []
                seq_7_249 = []
                seq_7_571 = []
                seq_7_572 = []
                seq_7_573 = []
                seq_7_574 = []
                seq_7_575 = []
                seq_7_576 = []
                seq_7_577 = []
                seq_7_578 = []
                seq_7_579 = []
                seq_7_580 = []
                seq_7_581 = []
                seq_7_582 = []
                seq_7_583 = []
                seq_7_584 = []
                seq_7_585 = []
                seq_7_586 = []
                seq_7_587 = []
                #8
                seq_8_08 = []
                seq_8_081 = []
                seq_8_082 = []
                seq_8_083 = []
                seq_8_084 = []
                seq_8_085 = []
                seq_8_086 = []
                seq_8_087 = []
                seq_8_088 = []
                seq_8_089 = []
                seq_8_090 = []
                seq_8_091 = []
                seq_8_240 = []
                seq_8_241 = []
                seq_8_242 = []
                seq_8_243 = []
                seq_8_244 = []
                seq_8_245 = []
                seq_8_246 = []
                seq_8_247 = []
                seq_8_248 = []
                seq_8_249 = []
                seq_8_571 = []
                seq_8_572 = []
                seq_8_573 = []
                seq_8_574 = []
                seq_8_575 = []
                seq_8_576 = []
                seq_8_577 = []
                seq_8_578 = []
                seq_8_579 = []
                seq_8_580 = []
                seq_8_581 = []
                seq_8_582 = []
                seq_8_583 = []
                seq_8_584 = []
                seq_8_585 = []
                seq_8_586 = []
                seq_8_587 = []
                #9
                seq_9_08 = []
                seq_9_081 = []
                seq_9_082 = []
                seq_9_083 = []
                seq_9_084 = []
                seq_9_085 = []
                seq_9_086 = []
                seq_9_087 = []
                seq_9_088 = []
                seq_9_089 = []
                seq_9_090 = []
                seq_9_091 = []
                seq_9_240 = []
                seq_9_241 = []
                seq_9_242 = []
                seq_9_243 = []
                seq_9_244 = []
                seq_9_245 = []
                seq_9_246 = []
                seq_9_247 = []
                seq_9_248 = []
                seq_9_249 = []
                seq_9_571 = []
                seq_9_572 = []
                seq_9_573 = []
                seq_9_574 = []
                seq_9_575 = []
                seq_9_576 = []
                seq_9_577 = []
                seq_9_578 = []
                seq_9_579 = []
                seq_9_580 = []
                seq_9_581 = []
                seq_9_582 = []
                seq_9_583 = []
                seq_9_584 = []
                seq_9_585 = []
                seq_9_586 = []
                seq_9_587 = []
                #10
                seq_10_08 = []
                seq_10_081 = []
                seq_10_082 = []
                seq_10_083 = []
                seq_10_084 = []
                seq_10_085 = []
                seq_10_086 = []
                seq_10_087 = []
                seq_10_088 = []
                seq_10_089 = []
                seq_10_090 = []
                seq_10_091 = []
                seq_10_240 = []
                seq_10_241 = []
                seq_10_242 = []
                seq_10_243 = []
                seq_10_244 = []
                seq_10_245 = []
                seq_10_246 = []
                seq_10_247 = []
                seq_10_248 = []
                seq_10_249 = []
                seq_10_571 = []
                seq_10_572 = []
                seq_10_573 = []
                seq_10_574 = []
                seq_10_575 = []
                seq_10_576 = []
                seq_10_577 = []
                seq_10_578 = []
                seq_10_579 = []
                seq_10_580 = []
                seq_10_581 = []
                seq_10_582 = []
                seq_10_583 = []
                seq_10_584 = []
                seq_10_585 = []
                seq_10_586 = []
                seq_10_587 = []
                #11
                seq_11_08 = []
                seq_11_081 = []
                seq_11_082 = []
                seq_11_083 = []
                seq_11_084 = []
                seq_11_085 = []
                seq_11_086 = []
                seq_11_087 = []
                seq_11_088 = []
                seq_11_089 = []
                seq_11_090 = []
                seq_11_091 = []
                seq_11_240 = []
                seq_11_241 = []
                seq_11_242 = []
                seq_11_243 = []
                seq_11_244 = []
                seq_11_245 = []
                seq_11_246 = []
                seq_11_247 = []
                seq_11_248 = []
                seq_11_249 = []
                seq_11_571 = []
                seq_11_572 = []
                seq_11_573 = []
                seq_11_574 = []
                seq_11_575 = []
                seq_11_576 = []
                seq_11_577 = []
                seq_11_578 = []
                seq_11_579 = []
                seq_11_580 = []
                seq_11_581 = []
                seq_11_582 = []
                seq_11_583 = []
                seq_11_584 = []
                seq_11_585 = []
                seq_11_586 = []
                seq_11_587 = []
                #1
                seq_12_08 = []
                seq_12_081 = []
                seq_12_082 = []
                seq_12_083 = []
                seq_12_084 = []
                seq_12_085 = []
                seq_12_086 = []
                seq_12_087 = []
                seq_12_088 = []
                seq_12_089 = []
                seq_12_090 = []
                seq_12_091 = []
                seq_12_240 = []
                seq_12_241 = []
                seq_12_242 = []
                seq_12_243 = []
                seq_12_244 = []
                seq_12_245 = []
                seq_12_246 = []
                seq_12_247 = []
                seq_12_248 = []
                seq_12_249 = []
                seq_12_571 = []
                seq_12_572 = []
                seq_12_573 = []
                seq_12_574 = []
                seq_12_575 = []
                seq_12_576 = []
                seq_12_577 = []
                seq_12_578 = []
                seq_12_579 = []
                seq_12_580 = []
                seq_12_581 = []
                seq_12_582 = []
                seq_12_583 = []
                seq_12_584 = []
                seq_12_585 = []
                seq_12_586 = []
                seq_12_587 = []
                #1
                seq_13_08 = []
                seq_13_081 = []
                seq_13_082 = []
                seq_13_083 = []
                seq_13_084 = []
                seq_13_085 = []
                seq_13_086 = []
                seq_13_087 = []
                seq_13_088 = []
                seq_13_089 = []
                seq_13_090 = []
                seq_13_091 = []
                seq_13_240 = []
                seq_13_241 = []
                seq_13_242 = []
                seq_13_243 = []
                seq_13_244 = []
                seq_13_245 = []
                seq_13_246 = []
                seq_13_247 = []
                seq_13_248 = []
                seq_13_249 = []
                seq_13_571 = []
                seq_13_572 = []
                seq_13_573 = []
                seq_13_574 = []
                seq_13_575 = []
                seq_13_576 = []
                seq_13_577 = []
                seq_13_578 = []
                seq_13_579 = []
                seq_13_580 = []
                seq_13_581 = []
                seq_13_582 = []
                seq_13_583 = []
                seq_13_584 = []
                seq_13_585 = []
                seq_13_586 = []
                seq_13_587 = []
                #14
                seq_14_08 = []
                seq_14_081 = []
                seq_14_082 = []
                seq_14_083 = []
                seq_14_084 = []
                seq_14_085 = []
                seq_14_086 = []
                seq_14_087 = []
                seq_14_088 = []
                seq_14_089 = []
                seq_14_090 = []
                seq_14_091 = []
                seq_14_240 = []
                seq_14_241 = []
                seq_14_242 = []
                seq_14_243 = []
                seq_14_244 = []
                seq_14_245 = []
                seq_14_246 = []
                seq_14_247 = []
                seq_14_248 = []
                seq_14_249 = []
                seq_14_571 = []
                seq_14_572 = []
                seq_14_573 = []
                seq_14_574 = []
                seq_14_575 = []
                seq_14_576 = []
                seq_14_577 = []
                seq_14_578 = []
                seq_14_579 = []
                seq_14_580 = []
                seq_14_581 = []
                seq_14_582 = []
                seq_14_583 = []
                seq_14_584 = []
                seq_14_585 = []
                seq_14_586 = []
                seq_14_587 = []
                #15
                seq_15_08 = []
                seq_15_081 = []
                seq_15_082 = []
                seq_15_083 = []
                seq_15_084 = []
                seq_15_085 = []
                seq_15_086 = []
                seq_15_087 = []
                seq_15_088 = []
                seq_15_089 = []
                seq_15_090 = []
                seq_15_091 = []
                seq_15_240 = []
                seq_15_241 = []
                seq_15_242 = []
                seq_15_243 = []
                seq_15_244 = []
                seq_15_245 = []
                seq_15_246 = []
                seq_15_247 = []
                seq_15_248 = []
                seq_15_249 = []
                seq_15_571 = []
                seq_15_572 = []
                seq_15_573 = []
                seq_15_574 = []
                seq_15_575 = []
                seq_15_576 = []
                seq_15_577 = []
                seq_15_578 = []
                seq_15_579 = []
                seq_15_580 = []
                seq_15_581 = []
                seq_15_582 = []
                seq_15_583 = []
                seq_15_584 = []
                seq_15_585 = []
                seq_15_586 = []
                seq_15_587 = []
                #16
                seq_16_08 = []
                seq_16_081 = []
                seq_16_082 = []
                seq_16_083 = []
                seq_16_084 = []
                seq_16_085 = []
                seq_16_086 = []
                seq_16_087 = []
                seq_16_088 = []
                seq_16_089 = []
                seq_16_090 = []
                seq_16_091 = []
                seq_16_240 = []
                seq_16_241 = []
                seq_16_242 = []
                seq_16_243 = []
                seq_16_244 = []
                seq_16_245 = []
                seq_16_246 = []
                seq_16_247 = []
                seq_16_248 = []
                seq_16_249 = []
                seq_16_571 = []
                seq_16_572 = []
                seq_16_573 = []
                seq_16_574 = []
                seq_16_575 = []
                seq_16_576 = []
                seq_16_577 = []
                seq_16_578 = []
                seq_16_579 = []
                seq_16_580 = []
                seq_16_581 = []
                seq_16_582 = []
                seq_16_583 = []
                seq_16_584 = []
                seq_16_585 = []
                seq_16_586 = []
                seq_16_587 = []
                #17
                seq_17_08 = []
                seq_17_081 = []
                seq_17_082 = []
                seq_17_083 = []
                seq_17_084 = []
                seq_17_085 = []
                seq_17_086 = []
                seq_17_087 = []
                seq_17_088 = []
                seq_17_089 = []
                seq_17_090 = []
                seq_17_091 = []
                seq_17_240 = []
                seq_17_241 = []
                seq_17_242 = []
                seq_17_243 = []
                seq_17_244 = []
                seq_17_245 = []
                seq_17_246 = []
                seq_17_247 = []
                seq_17_248 = []
                seq_17_249 = []
                seq_17_571 = []
                seq_17_572 = []
                seq_17_573 = []
                seq_17_574 = []
                seq_17_575 = []
                seq_17_576 = []
                seq_17_577 = []
                seq_17_578 = []
                seq_17_579 = []
                seq_17_580 = []
                seq_17_581 = []
                seq_17_582 = []
                seq_17_583 = []
                seq_17_584 = []
                seq_17_585 = []
                seq_17_586 = []
                seq_17_587 = []
                #18
                seq_18_08 = []
                seq_18_081 = []
                seq_18_082 = []
                seq_18_083 = []
                seq_18_084 = []
                seq_18_085 = []
                seq_18_086 = []
                seq_18_087 = []
                seq_18_088 = []
                seq_18_089 = []
                seq_18_090 = []
                seq_18_091 = []
                seq_18_240 = []
                seq_18_241 = []
                seq_18_242 = []
                seq_18_243 = []
                seq_18_244 = []
                seq_18_245 = []
                seq_18_246 = []
                seq_18_247 = []
                seq_18_248 = []
                seq_18_249 = []
                seq_18_571 = []
                seq_18_572 = []
                seq_18_573 = []
                seq_18_574 = []
                seq_18_575 = []
                seq_18_576 = []
                seq_18_577 = []
                seq_18_578 = []
                seq_18_579 = []
                seq_18_580 = []
                seq_18_581 = []
                seq_18_582 = []
                seq_18_583 = []
                seq_18_584 = []
                seq_18_585 = []
                seq_18_586 = []
                seq_18_587 = []
                #1
                seq_19_08 = []
                seq_19_081 = []
                seq_19_082 = []
                seq_19_083 = []
                seq_19_084 = []
                seq_19_085 = []
                seq_19_086 = []
                seq_19_087 = []
                seq_19_088 = []
                seq_19_089 = []
                seq_19_090 = []
                seq_19_091 = []
                seq_19_240 = []
                seq_19_241 = []
                seq_19_242 = []
                seq_19_243 = []
                seq_19_244 = []
                seq_19_245 = []
                seq_19_246 = []
                seq_19_247 = []
                seq_19_248 = []
                seq_19_249 = []
                seq_19_571 = []
                seq_19_572 = []
                seq_19_573 = []
                seq_19_574 = []
                seq_19_575 = []
                seq_19_576 = []
                seq_19_577 = []
                seq_19_578 = []
                seq_19_579 = []
                seq_19_580 = []
                seq_19_581 = []
                seq_19_582 = []
                seq_19_583 = []
                seq_19_584 = []
                seq_19_585 = []
                seq_19_586 = []
                seq_19_587 = []
                #20
                seq_20_08 = []
                seq_20_081 = []
                seq_20_082 = []
                seq_20_083 = []
                seq_20_084 = []
                seq_20_085 = []
                seq_20_086 = []
                seq_20_087 = []
                seq_20_088 = []
                seq_20_089 = []
                seq_20_090 = []
                seq_20_091 = []
                seq_20_240 = []
                seq_20_241 = []
                seq_20_242 = []
                seq_20_243 = []
                seq_20_244 = []
                seq_20_245 = []
                seq_20_246 = []
                seq_20_247 = []
                seq_20_248 = []
                seq_20_249 = []
                seq_20_571 = []
                seq_20_572 = []
                seq_20_573 = []
                seq_20_574 = []
                seq_20_575 = []
                seq_20_576 = []
                seq_20_577 = []
                seq_20_578 = []
                seq_20_579 = []
                seq_20_580 = []
                seq_20_581 = []
                seq_20_582 = []
                seq_20_583 = []
                seq_20_584 = []
                seq_20_585 = []
                seq_20_586 = []
                seq_20_587 = []
                #21
                seq_21_08 = []
                seq_21_081 = []
                seq_21_082 = []
                seq_21_083 = []
                seq_21_084 = []
                seq_21_085 = []
                seq_21_086 = []
                seq_21_087 = []
                seq_21_088 = []
                seq_21_089 = []
                seq_21_090 = []
                seq_21_091 = []
                seq_21_240 = []
                seq_21_241 = []
                seq_21_242 = []
                seq_21_243 = []
                seq_21_244 = []
                seq_21_245 = []
                seq_21_246 = []
                seq_21_247 = []
                seq_21_248 = []
                seq_21_249 = []
                seq_21_571 = []
                seq_21_572 = []
                seq_21_573 = []
                seq_21_574 = []
                seq_21_575 = []
                seq_21_576 = []
                seq_21_577 = []
                seq_21_578 = []
                seq_21_579 = []
                seq_21_580 = []
                seq_21_581 = []
                seq_21_582 = []
                seq_21_583 = []
                seq_21_584 = []
                seq_21_585 = []
                seq_21_586 = []
                seq_21_587 = []
                #22
                seq_22_08 = []
                seq_22_081 = []
                seq_22_082 = []
                seq_22_083 = []
                seq_22_084 = []
                seq_22_085 = []
                seq_22_086 = []
                seq_22_087 = []
                seq_22_088 = []
                seq_22_089 = []
                seq_22_090 = []
                seq_22_091 = []
                seq_22_240 = []
                seq_22_241 = []
                seq_22_242 = []
                seq_22_243 = []
                seq_22_244 = []
                seq_22_245 = []
                seq_22_246 = []
                seq_22_247 = []
                seq_22_248 = []
                seq_22_249 = []
                seq_22_571 = []
                seq_22_572 = []
                seq_22_573 = []
                seq_22_574 = []
                seq_22_575 = []
                seq_22_576 = []
                seq_22_577 = []
                seq_22_578 = []
                seq_22_579 = []
                seq_22_580 = []
                seq_22_581 = []
                seq_22_582 = []
                seq_22_583 = []
                seq_22_584 = []
                seq_22_585 = []
                seq_22_586 = []
                seq_22_587 = []
                #23
                seq_23_08 = []
                seq_23_081 = []
                seq_23_082 = []
                seq_23_083 = []
                seq_23_084 = []
                seq_23_085 = []
                seq_23_086 = []
                seq_23_087 = []
                seq_23_088 = []
                seq_23_089 = []
                seq_23_090 = []
                seq_23_091 = []
                seq_23_240 = []
                seq_23_241 = []
                seq_23_242 = []
                seq_23_243 = []
                seq_23_244 = []
                seq_23_245 = []
                seq_23_246 = []
                seq_23_247 = []
                seq_23_248 = []
                seq_23_249 = []
                seq_23_571 = []
                seq_23_572 = []
                seq_23_573 = []
                seq_23_574 = []
                seq_23_575 = []
                seq_23_576 = []
                seq_23_577 = []
                seq_23_578 = []
                seq_23_579 = []
                seq_23_580 = []
                seq_23_581 = []
                seq_23_582 = []
                seq_23_583 = []
                seq_23_584 = []
                seq_23_585 = []
                seq_23_586 = []
                seq_23_587 = []
                for i in range(len(floatSamples)):#run normalization for samples
                        if floatSamples[i][0] == 0:
                                if floatSamples[i][1] >= 0.8 and floatSamples[i][1] < 0.81:
                                        if floatSamples[i][2] > -100:
                                                seq_0_08.append(1)
                                        else:
                                                seq_0_08.append(0)
                                elif floatSamples[i][1] >= 0.81 and floatSamples[i][1] < 0.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_081.append(1)
                                        else:
                                                seq_0_081.append(0)
                                elif floatSamples[i][1] >= 0.82 and floatSamples[i][1] < 0.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_082.append(1)
                                        else:
                                                seq_0_082.append(0)
                                elif floatSamples[i][1] >= 0.83 and floatSamples[i][1] < 0.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_083.append(1)
                                        else:
                                                seq_0_083.append(0)
                                elif floatSamples[i][1] >= 0.84 and floatSamples[i][1] < 0.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_084.append(1)
                                        else:
                                                seq_0_084.append(0)
                                elif floatSamples[i][1] >= 0.85 and floatSamples[i][1] < 0.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_085.append(1)
                                        else:
                                                seq_0_085.append(0)
                                elif floatSamples[i][1] >= 0.86 and floatSamples[i][1] < 0.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_086.append(1)
                                        else:
                                                seq_0_086.append(0)
                                elif floatSamples[i][1] >= 0.87 and floatSamples[i][1] < 0.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_087.append(1)
                                        else:
                                                seq_0_087.append(0)
                                elif floatSamples[i][1] >= 0.88 and floatSamples[i][1] < 0.89:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_088.append(1)
                                        else:
                                                seq_0_088.append(0)
                                elif floatSamples[i][1] >= 0.89 and floatSamples[i][1] < 0.90:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_089.append(1)
                                        else:
                                                seq_0_089.append(0)
                                elif floatSamples[i][1] >= 0.90 and floatSamples[i][1] < 0.91:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_090.append(1)
                                        else:
                                                seq_0_090.append(0)
                                elif floatSamples[i][1] >= 0.91 and floatSamples[i][1] < 0.92:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_091.append(1)
                                        else:
                                                seq_0_091.append(0)
                                elif floatSamples[i][1] >= 2.4 and floatSamples[i][1] < 2.41: 
                                        if floatSamples[i][2]  > -100:
                                                seq_0_240.append(1)
                                        else:
                                                seq_0_240.append(0)
                                elif floatSamples[i][1] >= 2.41 and floatSamples[i][1] < 2.42:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_241.append(1)
                                        else:
                                                seq_0_241.append(0)
                                elif floatSamples[i][1] >= 2.42 and floatSamples[i][1] < 2.43:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_242.append(1)
                                        else:
                                                seq_0_242.append(0)
                                elif floatSamples[i][1] >= 2.43 and floatSamples[i][1] < 2.44:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_243.append(1)
                                        else:
                                                seq_0_243.append(0)
                                elif floatSamples[i][1] >= 2.44 and floatSamples[i][1] < 2.45:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_244.append(1)
                                        else:
                                                seq_0_244.append(0)
                                elif floatSamples[i][1] >= 2.45 and floatSamples[i][1] < 2.46:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_245.append(1)
                                        else:
                                                seq_0_245.append(0)
                                elif floatSamples[i][1] >= 2.46 and floatSamples[i][1] < 2.47:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_246.append(1)
                                        else:
                                                seq_0_246.append(0)
                                elif floatSamples[i][1] >= 2.47 and floatSamples[i][1] < 2.48:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_247.append(1)
                                        else:
                                                seq_0_247.append(0)
                                elif floatSamples[i][1] >= 2.48 and floatSamples[i][1] < 2.49:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_248.append(1)
                                        else:
                                                seq_0_248.append(0)
                                elif floatSamples[i][1] >= 2.49 and floatSamples[i][1] < 2.50:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_249.append(1)
                                        else:
                                                seq_0_249.append(0)
                                elif floatSamples[i][1] >= 5.71 and floatSamples[i][1] < 5.72:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_571.append(1)
                                        else:
                                                seq_0_571.append(0)
                                elif floatSamples[i][1] >= 5.72 and floatSamples[i][1] < 5.73:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_572.append(1)
                                        else:
                                                seq_0_572.append(0)
                                elif floatSamples[i][1] >= 5.73 and floatSamples[i][1] < 5.74:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_573.append(1)
                                        else:
                                                seq_0_573.append(0)
                                elif floatSamples[i][1] >= 5.74 and floatSamples[i][1] < 5.75:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_574.append(1)
                                        else:
                                                seq_0_574.append(0)
                                elif floatSamples[i][1] >= 5.75 and floatSamples[i][1] < 5.76:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_575.append(1)
                                        else:
                                                seq_0_575.append(0)
                                elif floatSamples[i][1] >= 5.76 and floatSamples[i][1] < 5.77:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_576.append(1)
                                        else:
                                                seq_0_576.append(0)
                                elif floatSamples[i][1] >= 5.77 and floatSamples[i][1] < 5.78:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_577.append(1)
                                        else:
                                                seq_0_577.append(0)
                                elif floatSamples[i][1] >= 5.78 and floatSamples[i][1] < 5.79:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_578.append(1)
                                        else:
                                                seq_0_578.append(0)
                                elif floatSamples[i][1] >= 5.79 and floatSamples[i][1] < 5.8:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_579.append(1)
                                        else:
                                                seq_0_579.append(0)
                                elif floatSamples[i][1] >= 5.8 and floatSamples[i][1] < 5.81:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_580.append(1)
                                        else:
                                                seq_0_580.append(0)
                                elif floatSamples[i][1] >= 5.81 and floatSamples[i][1] < 5.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_581.append(1)
                                        else:
                                                seq_0_581.append(0)
                                elif floatSamples[i][1] >= 5.82 and floatSamples[i][1] < 5.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_582.append(1)
                                        else:
                                                seq_0_582.append(0)
                                elif floatSamples[i][1] >= 5.83 and floatSamples[i][1] < 5.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_583.append(1)
                                        else:
                                                seq_0_583.append(0)
                                elif floatSamples[i][1] >= 5.84 and floatSamples[i][1] < 5.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_584.append(1)
                                        else:
                                                seq_0_584.append(0)
                                elif floatSamples[i][1] >= 5.85 and floatSamples[i][1] < 5.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_585.append(1)
                                        else:
                                                seq_0_585.append(0)
                                elif floatSamples[i][1] >= 5.86 and floatSamples[i][1] < 5.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_586.append(1)
                                        else:
                                                seq_0_586.append(0)
                                elif floatSamples[i][1] >= 5.87 and floatSamples[i][1] < 5.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_0_587.append(1)
                                        else:
                                                seq_0_587.append(0)
                        elif floatSamples[i][0] == 1:
                                if floatSamples[i][1] >= 0.8 and floatSamples[i][1] < 0.81:
                                        if floatSamples[i][2] > -100:
                                                seq_1_08.append(1)
                                        else:
                                                seq_1_08.append(0)
                                elif floatSamples[i][1] >= 0.81 and floatSamples[i][1] < 0.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_081.append(1)
                                        else:
                                                seq_1_081.append(0)
                                elif floatSamples[i][1] >= 0.82 and floatSamples[i][1] < 0.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_082.append(1)
                                        else:
                                                seq_1_082.append(0)
                                elif floatSamples[i][1] >= 0.83 and floatSamples[i][1] < 0.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_083.append(1)
                                        else:
                                                seq_1_083.append(0)
                                elif floatSamples[i][1] >= 0.84 and floatSamples[i][1] < 0.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_084.append(1)
                                        else:
                                                seq_1_084.append(0)
                                elif floatSamples[i][1] >= 0.85 and floatSamples[i][1] < 0.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_085.append(1)
                                        else:
                                                seq_1_085.append(0)
                                elif floatSamples[i][1] >= 0.86 and floatSamples[i][1] < 0.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_086.append(1)
                                        else:
                                                seq_1_086.append(0)
                                elif floatSamples[i][1] >= 0.87 and floatSamples[i][1] < 0.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_087.append(1)
                                        else:
                                                seq_1_087.append(0)
                                elif floatSamples[i][1] >= 0.88 and floatSamples[i][1] < 0.89:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_088.append(1)
                                        else:
                                                seq_1_088.append(0)
                                elif floatSamples[i][1] >= 0.89 and floatSamples[i][1] < 0.90:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_089.append(1)
                                        else:
                                                seq_1_089.append(0)
                                elif floatSamples[i][1] >= 0.90 and floatSamples[i][1] < 0.91:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_090.append(1)
                                        else:
                                                seq_1_090.append(0)
                                elif floatSamples[i][1] >= 0.91 and floatSamples[i][1] < 0.92:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_091.append(1)
                                        else:
                                                seq_1_091.append(0)
                                elif floatSamples[i][1] >= 2.4 and floatSamples[i][1] < 2.41: 
                                        if floatSamples[i][2]  > -100:
                                                seq_1_240.append(1)
                                        else:
                                                seq_1_240.append(0)
                                elif floatSamples[i][1] >= 2.41 and floatSamples[i][1] < 2.42:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_241.append(1)
                                        else:
                                                seq_1_241.append(0)
                                elif floatSamples[i][1] >= 2.42 and floatSamples[i][1] < 2.43:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_242.append(1)
                                        else:
                                                seq_1_242.append(0)
                                elif floatSamples[i][1] >= 2.43 and floatSamples[i][1] < 2.44:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_243.append(1)
                                        else:
                                                seq_1_243.append(0)
                                elif floatSamples[i][1] >= 2.44 and floatSamples[i][1] < 2.45:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_244.append(1)
                                        else:
                                                seq_1_244.append(0)
                                elif floatSamples[i][1] >= 2.45 and floatSamples[i][1] < 2.46:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_245.append(1)
                                        else:
                                                seq_1_245.append(0)
                                elif floatSamples[i][1] >= 2.46 and floatSamples[i][1] < 2.47:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_246.append(1)
                                        else:
                                                seq_1_246.append(0)
                                elif floatSamples[i][1] >= 2.47 and floatSamples[i][1] < 2.48:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_247.append(1)
                                        else:
                                                seq_1_247.append(0)
                                elif floatSamples[i][1] >= 2.48 and floatSamples[i][1] < 2.49:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_248.append(1)
                                        else:
                                                seq_1_248.append(0)
                                elif floatSamples[i][1] >= 2.49 and floatSamples[i][1] < 2.50:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_249.append(1)
                                        else:
                                                seq_1_249.append(0)
                                elif floatSamples[i][1] >= 5.71 and floatSamples[i][1] < 5.72:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_571.append(1)
                                        else:
                                                seq_1_571.append(0)
                                elif floatSamples[i][1] >= 5.72 and floatSamples[i][1] < 5.73:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_572.append(1)
                                        else:
                                                seq_1_572.append(0)
                                elif floatSamples[i][1] >= 5.73 and floatSamples[i][1] < 5.74:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_573.append(1)
                                        else:
                                                seq_1_573.append(0)
                                elif floatSamples[i][1] >= 5.74 and floatSamples[i][1] < 5.75:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_574.append(1)
                                        else:
                                                seq_1_574.append(0)
                                elif floatSamples[i][1] >= 5.75 and floatSamples[i][1] < 5.76:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_575.append(1)
                                        else:
                                                seq_1_575.append(0)
                                elif floatSamples[i][1] >= 5.76 and floatSamples[i][1] < 5.77:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_576.append(1)
                                        else:
                                                seq_1_576.append(0)
                                elif floatSamples[i][1] >= 5.77 and floatSamples[i][1] < 5.78:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_577.append(1)
                                        else:
                                                seq_1_577.append(0)
                                elif floatSamples[i][1] >= 5.78 and floatSamples[i][1] < 5.79:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_578.append(1)
                                        else:
                                                seq_1_578.append(0)
                                elif floatSamples[i][1] >= 5.79 and floatSamples[i][1] < 5.8:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_579.append(1)
                                        else:
                                                seq_1_579.append(0)
                                elif floatSamples[i][1] >= 5.8 and floatSamples[i][1] < 5.81:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_580.append(1)
                                        else:
                                                seq_1_580.append(0)
                                elif floatSamples[i][1] >= 5.81 and floatSamples[i][1] < 5.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_581.append(1)
                                        else:
                                                seq_1_581.append(0)
                                elif floatSamples[i][1] >= 5.82 and floatSamples[i][1] < 5.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_582.append(1)
                                        else:
                                                seq_1_582.append(0)
                                elif floatSamples[i][1] >= 5.83 and floatSamples[i][1] < 5.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_583.append(1)
                                        else:
                                                seq_1_583.append(0)
                                elif floatSamples[i][1] >= 5.84 and floatSamples[i][1] < 5.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_584.append(1)
                                        else:
                                                seq_1_584.append(0)
                                elif floatSamples[i][1] >= 5.85 and floatSamples[i][1] < 5.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_585.append(1)
                                        else:
                                                seq_1_585.append(0)
                                elif floatSamples[i][1] >= 5.86 and floatSamples[i][1] < 5.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_586.append(1)
                                        else:
                                                seq_1_586.append(0)
                                elif floatSamples[i][1] >= 5.87 and floatSamples[i][1] < 5.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_1_587.append(1)
                                        else:
                                                seq_1_587.append(0)
                        elif floatSamples[i][0] == 2:
                                if floatSamples[i][1] >= 0.8 and floatSamples[i][1] < 0.81:
                                        if floatSamples[i][2] > -100:
                                                seq_2_08.append(1)
                                        else:
                                                seq_2_08.append(0)
                                elif floatSamples[i][1] >= 0.81 and floatSamples[i][1] < 0.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_081.append(1)
                                        else:
                                                seq_2_081.append(0)
                                elif floatSamples[i][1] >= 0.82 and floatSamples[i][1] < 0.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_082.append(1)
                                        else:
                                                seq_2_082.append(0)
                                elif floatSamples[i][1] >= 0.83 and floatSamples[i][1] < 0.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_083.append(1)
                                        else:
                                                seq_2_083.append(0)
                                elif floatSamples[i][1] >= 0.84 and floatSamples[i][1] < 0.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_084.append(1)
                                        else:
                                                seq_2_084.append(0)
                                elif floatSamples[i][1] >= 0.85 and floatSamples[i][1] < 0.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_085.append(1)
                                        else:
                                                seq_2_085.append(0)
                                elif floatSamples[i][1] >= 0.86 and floatSamples[i][1] < 0.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_086.append(1)
                                        else:
                                                seq_2_086.append(0)
                                elif floatSamples[i][1] >= 0.87 and floatSamples[i][1] < 0.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_087.append(1)
                                        else:
                                                seq_2_087.append(0)
                                elif floatSamples[i][1] >= 0.88 and floatSamples[i][1] < 0.89:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_088.append(1)
                                        else:
                                                seq_2_088.append(0)
                                elif floatSamples[i][1] >= 0.89 and floatSamples[i][1] < 0.90:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_089.append(1)
                                        else:
                                                seq_2_089.append(0)
                                elif floatSamples[i][1] >= 0.90 and floatSamples[i][1] < 0.91:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_090.append(1)
                                        else:
                                                seq_2_090.append(0)
                                elif floatSamples[i][1] >= 0.91 and floatSamples[i][1] < 0.92:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_091.append(1)
                                        else:
                                                seq_2_091.append(0)
                                elif floatSamples[i][1] >= 2.4 and floatSamples[i][1] < 2.41: 
                                        if floatSamples[i][2]  > -100:
                                                seq_2_240.append(1)
                                        else:
                                                seq_2_240.append(0)
                                elif floatSamples[i][1] >= 2.41 and floatSamples[i][1] < 2.42:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_241.append(1)
                                        else:
                                                seq_2_241.append(0)
                                elif floatSamples[i][1] >= 2.42 and floatSamples[i][1] < 2.43:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_242.append(1)
                                        else:
                                                seq_2_242.append(0)
                                elif floatSamples[i][1] >= 2.43 and floatSamples[i][1] < 2.44:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_243.append(1)
                                        else:
                                                seq_2_243.append(0)
                                elif floatSamples[i][1] >= 2.44 and floatSamples[i][1] < 2.45:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_244.append(1)
                                        else:
                                                seq_2_244.append(0)
                                elif floatSamples[i][1] >= 2.45 and floatSamples[i][1] < 2.46:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_245.append(1)
                                        else:
                                                seq_2_245.append(0)
                                elif floatSamples[i][1] >= 2.46 and floatSamples[i][1] < 2.47:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_246.append(1)
                                        else:
                                                seq_2_246.append(0)
                                elif floatSamples[i][1] >= 2.47 and floatSamples[i][1] < 2.48:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_247.append(1)
                                        else:
                                                seq_2_247.append(0)
                                elif floatSamples[i][1] >= 2.48 and floatSamples[i][1] < 2.49:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_248.append(1)
                                        else:
                                                seq_2_248.append(0)
                                elif floatSamples[i][1] >= 2.49 and floatSamples[i][1] < 2.50:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_249.append(1)
                                        else:
                                                seq_2_249.append(0)
                                elif floatSamples[i][1] >= 5.71 and floatSamples[i][1] < 5.72:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_571.append(1)
                                        else:
                                                seq_2_571.append(0)
                                elif floatSamples[i][1] >= 5.72 and floatSamples[i][1] < 5.73:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_572.append(1)
                                        else:
                                                seq_2_572.append(0)
                                elif floatSamples[i][1] >= 5.73 and floatSamples[i][1] < 5.74:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_573.append(1)
                                        else:
                                                seq_2_573.append(0)
                                elif floatSamples[i][1] >= 5.74 and floatSamples[i][1] < 5.75:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_574.append(1)
                                        else:
                                                seq_2_574.append(0)
                                elif floatSamples[i][1] >= 5.75 and floatSamples[i][1] < 5.76:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_575.append(1)
                                        else:
                                                seq_2_575.append(0)
                                elif floatSamples[i][1] >= 5.76 and floatSamples[i][1] < 5.77:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_576.append(1)
                                        else:
                                                seq_2_576.append(0)
                                elif floatSamples[i][1] >= 5.77 and floatSamples[i][1] < 5.78:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_577.append(1)
                                        else:
                                                seq_2_577.append(0)
                                elif floatSamples[i][1] >= 5.78 and floatSamples[i][1] < 5.79:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_578.append(1)
                                        else:
                                                seq_2_578.append(0)
                                elif floatSamples[i][1] >= 5.79 and floatSamples[i][1] < 5.8:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_579.append(1)
                                        else:
                                                seq_2_579.append(0)
                                elif floatSamples[i][1] >= 5.8 and floatSamples[i][1] < 5.81:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_580.append(1)
                                        else:
                                                seq_2_580.append(0)
                                elif floatSamples[i][1] >= 5.81 and floatSamples[i][1] < 5.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_581.append(1)
                                        else:
                                                seq_2_581.append(0)
                                elif floatSamples[i][1] >= 5.82 and floatSamples[i][1] < 5.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_582.append(1)
                                        else:
                                                seq_2_582.append(0)
                                elif floatSamples[i][1] >= 5.83 and floatSamples[i][1] < 5.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_583.append(1)
                                        else:
                                                seq_2_583.append(0)
                                elif floatSamples[i][1] >= 5.84 and floatSamples[i][1] < 5.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_584.append(1)
                                        else:
                                                seq_2_584.append(0)
                                elif floatSamples[i][1] >= 5.85 and floatSamples[i][1] < 5.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_585.append(1)
                                        else:
                                                seq_2_585.append(0)
                                elif floatSamples[i][1] >= 5.86 and floatSamples[i][1] < 5.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_586.append(1)
                                        else:
                                                seq_2_586.append(0)
                                elif floatSamples[i][1] >= 5.87 and floatSamples[i][1] < 5.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_2_587.append(1)
                                        else:
                                                seq_2_587.append(0)
                        elif floatSamples[i][0] == 3:
                                if floatSamples[i][1] >= 0.8 and floatSamples[i][1] < 0.81:
                                        if floatSamples[i][2] > -100:
                                                seq_3_08.append(1)
                                        else:
                                                seq_3_08.append(0)
                                elif floatSamples[i][1] >= 0.81 and floatSamples[i][1] < 0.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_081.append(1)
                                        else:
                                                seq_3_081.append(0)
                                elif floatSamples[i][1] >= 0.82 and floatSamples[i][1] < 0.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_082.append(1)
                                        else:
                                                seq_3_082.append(0)
                                elif floatSamples[i][1] >= 0.83 and floatSamples[i][1] < 0.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_083.append(1)
                                        else:
                                                seq_3_083.append(0)
                                elif floatSamples[i][1] >= 0.84 and floatSamples[i][1] < 0.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_084.append(1)
                                        else:
                                                seq_3_084.append(0)
                                elif floatSamples[i][1] >= 0.85 and floatSamples[i][1] < 0.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_085.append(1)
                                        else:
                                                seq_3_085.append(0)
                                elif floatSamples[i][1] >= 0.86 and floatSamples[i][1] < 0.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_086.append(1)
                                        else:
                                                seq_3_086.append(0)
                                elif floatSamples[i][1] >= 0.87 and floatSamples[i][1] < 0.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_087.append(1)
                                        else:
                                                seq_3_087.append(0)
                                elif floatSamples[i][1] >= 0.88 and floatSamples[i][1] < 0.89:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_088.append(1)
                                        else:
                                                seq_3_088.append(0)
                                elif floatSamples[i][1] >= 0.89 and floatSamples[i][1] < 0.90:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_089.append(1)
                                        else:
                                                seq_3_089.append(0)
                                elif floatSamples[i][1] >= 0.90 and floatSamples[i][1] < 0.91:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_090.append(1)
                                        else:
                                                seq_3_090.append(0)
                                elif floatSamples[i][1] >= 0.91 and floatSamples[i][1] < 0.92:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_091.append(1)
                                        else:
                                                seq_3_091.append(0)
                                elif floatSamples[i][1] >= 2.4 and floatSamples[i][1] < 2.41: 
                                        if floatSamples[i][2]  > -100:
                                                seq_3_240.append(1)
                                        else:
                                                seq_3_240.append(0)
                                elif floatSamples[i][1] >= 2.41 and floatSamples[i][1] < 2.42:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_241.append(1)
                                        else:
                                                seq_3_241.append(0)
                                elif floatSamples[i][1] >= 2.42 and floatSamples[i][1] < 2.43:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_242.append(1)
                                        else:
                                                seq_3_242.append(0)
                                elif floatSamples[i][1] >= 2.43 and floatSamples[i][1] < 2.44:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_243.append(1)
                                        else:
                                                seq_3_243.append(0)
                                elif floatSamples[i][1] >= 2.44 and floatSamples[i][1] < 2.45:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_244.append(1)
                                        else:
                                                seq_3_244.append(0)
                                elif floatSamples[i][1] >= 2.45 and floatSamples[i][1] < 2.46:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_245.append(1)
                                        else:
                                                seq_3_245.append(0)
                                elif floatSamples[i][1] >= 2.46 and floatSamples[i][1] < 2.47:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_246.append(1)
                                        else:
                                                seq_3_246.append(0)
                                elif floatSamples[i][1] >= 2.47 and floatSamples[i][1] < 2.48:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_247.append(1)
                                        else:
                                                seq_3_247.append(0)
                                elif floatSamples[i][1] >= 2.48 and floatSamples[i][1] < 2.49:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_248.append(1)
                                        else:
                                                seq_3_248.append(0)
                                elif floatSamples[i][1] >= 2.49 and floatSamples[i][1] < 2.50:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_249.append(1)
                                        else:
                                                seq_3_249.append(0)
                                elif floatSamples[i][1] >= 5.71 and floatSamples[i][1] < 5.72:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_571.append(1)
                                        else:
                                                seq_3_571.append(0)
                                elif floatSamples[i][1] >= 5.72 and floatSamples[i][1] < 5.73:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_572.append(1)
                                        else:
                                                seq_3_572.append(0)
                                elif floatSamples[i][1] >= 5.73 and floatSamples[i][1] < 5.74:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_573.append(1)
                                        else:
                                                seq_3_573.append(0)
                                elif floatSamples[i][1] >= 5.74 and floatSamples[i][1] < 5.75:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_574.append(1)
                                        else:
                                                seq_3_574.append(0)
                                elif floatSamples[i][1] >= 5.75 and floatSamples[i][1] < 5.76:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_575.append(1)
                                        else:
                                                seq_3_575.append(0)
                                elif floatSamples[i][1] >= 5.76 and floatSamples[i][1] < 5.77:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_576.append(1)
                                        else:
                                                seq_3_576.append(0)
                                elif floatSamples[i][1] >= 5.77 and floatSamples[i][1] < 5.78:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_577.append(1)
                                        else:
                                                seq_3_577.append(0)
                                elif floatSamples[i][1] >= 5.78 and floatSamples[i][1] < 5.79:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_578.append(1)
                                        else:
                                                seq_3_578.append(0)
                                elif floatSamples[i][1] >= 5.79 and floatSamples[i][1] < 5.8:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_579.append(1)
                                        else:
                                                seq_3_579.append(0)
                                elif floatSamples[i][1] >= 5.8 and floatSamples[i][1] < 5.81:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_580.append(1)
                                        else:
                                                seq_3_580.append(0)
                                elif floatSamples[i][1] >= 5.81 and floatSamples[i][1] < 5.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_581.append(1)
                                        else:
                                                seq_3_581.append(0)
                                elif floatSamples[i][1] >= 5.82 and floatSamples[i][1] < 5.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_582.append(1)
                                        else:
                                                seq_3_582.append(0)
                                elif floatSamples[i][1] >= 5.83 and floatSamples[i][1] < 5.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_583.append(1)
                                        else:
                                                seq_3_583.append(0)
                                elif floatSamples[i][1] >= 5.84 and floatSamples[i][1] < 5.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_584.append(1)
                                        else:
                                                seq_3_584.append(0)
                                elif floatSamples[i][1] >= 5.85 and floatSamples[i][1] < 5.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_585.append(1)
                                        else:
                                                seq_3_585.append(0)
                                elif floatSamples[i][1] >= 5.86 and floatSamples[i][1] < 5.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_586.append(1)
                                        else:
                                                seq_3_586.append(0)
                                elif floatSamples[i][1] >= 5.87 and floatSamples[i][1] < 5.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_3_587.append(1)
                                        else:
                                                seq_3_587.append(0)
                        elif floatSamples[i][0] == 4:
                                if floatSamples[i][1] >= 0.8 and floatSamples[i][1] < 0.81:
                                        if floatSamples[i][2] > -100:
                                                seq_4_08.append(1)
                                        else:
                                                seq_4_08.append(0)
                                elif floatSamples[i][1] >= 0.81 and floatSamples[i][1] < 0.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_081.append(1)
                                        else:
                                                seq_4_081.append(0)
                                elif floatSamples[i][1] >= 0.82 and floatSamples[i][1] < 0.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_082.append(1)
                                        else:
                                                seq_4_082.append(0)
                                elif floatSamples[i][1] >= 0.83 and floatSamples[i][1] < 0.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_083.append(1)
                                        else:
                                                seq_4_083.append(0)
                                elif floatSamples[i][1] >= 0.84 and floatSamples[i][1] < 0.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_084.append(1)
                                        else:
                                                seq_4_084.append(0)
                                elif floatSamples[i][1] >= 0.85 and floatSamples[i][1] < 0.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_085.append(1)
                                        else:
                                                seq_4_085.append(0)
                                elif floatSamples[i][1] >= 0.86 and floatSamples[i][1] < 0.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_086.append(1)
                                        else:
                                                seq_4_086.append(0)
                                elif floatSamples[i][1] >= 0.87 and floatSamples[i][1] < 0.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_087.append(1)
                                        else:
                                                seq_4_087.append(0)
                                elif floatSamples[i][1] >= 0.88 and floatSamples[i][1] < 0.89:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_088.append(1)
                                        else:
                                                seq_4_088.append(0)
                                elif floatSamples[i][1] >= 0.89 and floatSamples[i][1] < 0.90:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_089.append(1)
                                        else:
                                                seq_4_089.append(0)
                                elif floatSamples[i][1] >= 0.90 and floatSamples[i][1] < 0.91:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_090.append(1)
                                        else:
                                                seq_4_090.append(0)
                                elif floatSamples[i][1] >= 0.91 and floatSamples[i][1] < 0.92:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_091.append(1)
                                        else:
                                                seq_4_091.append(0)
                                elif floatSamples[i][1] >= 2.4 and floatSamples[i][1] < 2.41: 
                                        if floatSamples[i][2]  > -100:
                                                seq_4_240.append(1)
                                        else:
                                                seq_4_240.append(0)
                                elif floatSamples[i][1] >= 2.41 and floatSamples[i][1] < 2.42:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_241.append(1)
                                        else:
                                                seq_4_241.append(0)
                                elif floatSamples[i][1] >= 2.42 and floatSamples[i][1] < 2.43:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_242.append(1)
                                        else:
                                                seq_4_242.append(0)
                                elif floatSamples[i][1] >= 2.43 and floatSamples[i][1] < 2.44:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_243.append(1)
                                        else:
                                                seq_4_243.append(0)
                                elif floatSamples[i][1] >= 2.44 and floatSamples[i][1] < 2.45:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_244.append(1)
                                        else:
                                                seq_4_244.append(0)
                                elif floatSamples[i][1] >= 2.45 and floatSamples[i][1] < 2.46:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_245.append(1)
                                        else:
                                                seq_4_245.append(0)
                                elif floatSamples[i][1] >= 2.46 and floatSamples[i][1] < 2.47:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_246.append(1)
                                        else:
                                                seq_4_246.append(0)
                                elif floatSamples[i][1] >= 2.47 and floatSamples[i][1] < 2.48:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_247.append(1)
                                        else:
                                                seq_4_247.append(0)
                                elif floatSamples[i][1] >= 2.48 and floatSamples[i][1] < 2.49:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_248.append(1)
                                        else:
                                                seq_4_248.append(0)
                                elif floatSamples[i][1] >= 2.49 and floatSamples[i][1] < 2.50:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_249.append(1)
                                        else:
                                                seq_4_249.append(0)
                                elif floatSamples[i][1] >= 5.71 and floatSamples[i][1] < 5.72:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_571.append(1)
                                        else:
                                                seq_4_571.append(0)
                                elif floatSamples[i][1] >= 5.72 and floatSamples[i][1] < 5.73:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_572.append(1)
                                        else:
                                                seq_4_572.append(0)
                                elif floatSamples[i][1] >= 5.73 and floatSamples[i][1] < 5.74:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_573.append(1)
                                        else:
                                                seq_4_573.append(0)
                                elif floatSamples[i][1] >= 5.74 and floatSamples[i][1] < 5.75:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_574.append(1)
                                        else:
                                                seq_4_574.append(0)
                                elif floatSamples[i][1] >= 5.75 and floatSamples[i][1] < 5.76:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_575.append(1)
                                        else:
                                                seq_4_575.append(0)
                                elif floatSamples[i][1] >= 5.76 and floatSamples[i][1] < 5.77:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_576.append(1)
                                        else:
                                                seq_4_576.append(0)
                                elif floatSamples[i][1] >= 5.77 and floatSamples[i][1] < 5.78:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_577.append(1)
                                        else:
                                                seq_4_577.append(0)
                                elif floatSamples[i][1] >= 5.78 and floatSamples[i][1] < 5.79:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_578.append(1)
                                        else:
                                                seq_4_578.append(0)
                                elif floatSamples[i][1] >= 5.79 and floatSamples[i][1] < 5.8:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_579.append(1)
                                        else:
                                                seq_4_579.append(0)
                                elif floatSamples[i][1] >= 5.8 and floatSamples[i][1] < 5.81:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_580.append(1)
                                        else:
                                                seq_4_580.append(0)
                                elif floatSamples[i][1] >= 5.81 and floatSamples[i][1] < 5.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_581.append(1)
                                        else:
                                                seq_4_581.append(0)
                                elif floatSamples[i][1] >= 5.82 and floatSamples[i][1] < 5.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_582.append(1)
                                        else:
                                                seq_4_582.append(0)
                                elif floatSamples[i][1] >= 5.83 and floatSamples[i][1] < 5.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_583.append(1)
                                        else:
                                                seq_4_583.append(0)
                                elif floatSamples[i][1] >= 5.84 and floatSamples[i][1] < 5.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_584.append(1)
                                        else:
                                                seq_4_584.append(0)
                                elif floatSamples[i][1] >= 5.85 and floatSamples[i][1] < 5.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_585.append(1)
                                        else:
                                                seq_4_585.append(0)
                                elif floatSamples[i][1] >= 5.86 and floatSamples[i][1] < 5.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_586.append(1)
                                        else:
                                                seq_4_586.append(0)
                                elif floatSamples[i][1] >= 5.87 and floatSamples[i][1] < 5.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_4_587.append(1)
                                        else:
                                                seq_4_587.append(0)
                        elif floatSamples[i][0] == 5:
                                if floatSamples[i][1] >= 0.8 and floatSamples[i][1] < 0.81:
                                        if floatSamples[i][2] > -100:
                                                seq_5_08.append(1)
                                        else:
                                                seq_5_08.append(0)
                                elif floatSamples[i][1] >= 0.81 and floatSamples[i][1] < 0.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_081.append(1)
                                        else:
                                                seq_5_081.append(0)
                                elif floatSamples[i][1] >= 0.82 and floatSamples[i][1] < 0.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_082.append(1)
                                        else:
                                                seq_5_082.append(0)
                                elif floatSamples[i][1] >= 0.83 and floatSamples[i][1] < 0.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_083.append(1)
                                        else:
                                                seq_5_083.append(0)
                                elif floatSamples[i][1] >= 0.84 and floatSamples[i][1] < 0.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_084.append(1)
                                        else:
                                                seq_5_084.append(0)
                                elif floatSamples[i][1] >= 0.85 and floatSamples[i][1] < 0.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_085.append(1)
                                        else:
                                                seq_5_085.append(0)
                                elif floatSamples[i][1] >= 0.86 and floatSamples[i][1] < 0.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_086.append(1)
                                        else:
                                                seq_5_086.append(0)
                                elif floatSamples[i][1] >= 0.87 and floatSamples[i][1] < 0.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_087.append(1)
                                        else:
                                                seq_5_087.append(0)
                                elif floatSamples[i][1] >= 0.88 and floatSamples[i][1] < 0.89:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_088.append(1)
                                        else:
                                                seq_5_088.append(0)
                                elif floatSamples[i][1] >= 0.89 and floatSamples[i][1] < 0.90:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_089.append(1)
                                        else:
                                                seq_5_089.append(0)
                                elif floatSamples[i][1] >= 0.90 and floatSamples[i][1] < 0.91:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_090.append(1)
                                        else:
                                                seq_5_090.append(0)
                                elif floatSamples[i][1] >= 0.91 and floatSamples[i][1] < 0.92:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_091.append(1)
                                        else:
                                                seq_5_091.append(0)
                                elif floatSamples[i][1] >= 2.4 and floatSamples[i][1] < 2.41: 
                                        if floatSamples[i][2]  > -100:
                                                seq_5_240.append(1)
                                        else:
                                                seq_5_240.append(0)
                                elif floatSamples[i][1] >= 2.41 and floatSamples[i][1] < 2.42:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_241.append(1)
                                        else:
                                                seq_5_241.append(0)
                                elif floatSamples[i][1] >= 2.42 and floatSamples[i][1] < 2.43:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_242.append(1)
                                        else:
                                                seq_5_242.append(0)
                                elif floatSamples[i][1] >= 2.43 and floatSamples[i][1] < 2.44:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_243.append(1)
                                        else:
                                                seq_5_243.append(0)
                                elif floatSamples[i][1] >= 2.44 and floatSamples[i][1] < 2.45:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_244.append(1)
                                        else:
                                                seq_5_244.append(0)
                                elif floatSamples[i][1] >= 2.45 and floatSamples[i][1] < 2.46:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_245.append(1)
                                        else:
                                                seq_5_245.append(0)
                                elif floatSamples[i][1] >= 2.46 and floatSamples[i][1] < 2.47:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_246.append(1)
                                        else:
                                                seq_5_246.append(0)
                                elif floatSamples[i][1] >= 2.47 and floatSamples[i][1] < 2.48:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_247.append(1)
                                        else:
                                                seq_5_247.append(0)
                                elif floatSamples[i][1] >= 2.48 and floatSamples[i][1] < 2.49:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_248.append(1)
                                        else:
                                                seq_5_248.append(0)
                                elif floatSamples[i][1] >= 2.49 and floatSamples[i][1] < 2.50:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_249.append(1)
                                        else:
                                                seq_5_249.append(0)
                                elif floatSamples[i][1] >= 5.71 and floatSamples[i][1] < 5.72:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_571.append(1)
                                        else:
                                                seq_5_571.append(0)
                                elif floatSamples[i][1] >= 5.72 and floatSamples[i][1] < 5.73:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_572.append(1)
                                        else:
                                                seq_5_572.append(0)
                                elif floatSamples[i][1] >= 5.73 and floatSamples[i][1] < 5.74:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_573.append(1)
                                        else:
                                                seq_5_573.append(0)
                                elif floatSamples[i][1] >= 5.74 and floatSamples[i][1] < 5.75:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_574.append(1)
                                        else:
                                                seq_5_574.append(0)
                                elif floatSamples[i][1] >= 5.75 and floatSamples[i][1] < 5.76:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_575.append(1)
                                        else:
                                                seq_5_575.append(0)
                                elif floatSamples[i][1] >= 5.76 and floatSamples[i][1] < 5.77:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_576.append(1)
                                        else:
                                                seq_5_576.append(0)
                                elif floatSamples[i][1] >= 5.77 and floatSamples[i][1] < 5.78:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_577.append(1)
                                        else:
                                                seq_5_577.append(0)
                                elif floatSamples[i][1] >= 5.78 and floatSamples[i][1] < 5.79:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_578.append(1)
                                        else:
                                                seq_5_578.append(0)
                                elif floatSamples[i][1] >= 5.79 and floatSamples[i][1] < 5.8:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_579.append(1)
                                        else:
                                                seq_5_579.append(0)
                                elif floatSamples[i][1] >= 5.8 and floatSamples[i][1] < 5.81:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_580.append(1)
                                        else:
                                                seq_5_580.append(0)
                                elif floatSamples[i][1] >= 5.81 and floatSamples[i][1] < 5.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_581.append(1)
                                        else:
                                                seq_5_581.append(0)
                                elif floatSamples[i][1] >= 5.82 and floatSamples[i][1] < 5.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_582.append(1)
                                        else:
                                                seq_5_582.append(0)
                                elif floatSamples[i][1] >= 5.83 and floatSamples[i][1] < 5.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_583.append(1)
                                        else:
                                                seq_5_583.append(0)
                                elif floatSamples[i][1] >= 5.84 and floatSamples[i][1] < 5.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_584.append(1)
                                        else:
                                                seq_5_584.append(0)
                                elif floatSamples[i][1] >= 5.85 and floatSamples[i][1] < 5.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_585.append(1)
                                        else:
                                                seq_5_585.append(0)
                                elif floatSamples[i][1] >= 5.86 and floatSamples[i][1] < 5.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_586.append(1)
                                        else:
                                                seq_5_586.append(0)
                                elif floatSamples[i][1] >= 5.87 and floatSamples[i][1] < 5.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_5_587.append(1)
                                        else:
                                                seq_5_587.append(0)
                        elif floatSamples[i][0] == 6:
                                if floatSamples[i][1] >= 0.8 and floatSamples[i][1] < 0.81:
                                        if floatSamples[i][2] > -100:
                                                seq_6_08.append(1)
                                        else:
                                                seq_6_08.append(0)
                                elif floatSamples[i][1] >= 0.81 and floatSamples[i][1] < 0.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_081.append(1)
                                        else:
                                                seq_6_081.append(0)
                                elif floatSamples[i][1] >= 0.82 and floatSamples[i][1] < 0.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_082.append(1)
                                        else:
                                                seq_6_082.append(0)
                                elif floatSamples[i][1] >= 0.83 and floatSamples[i][1] < 0.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_083.append(1)
                                        else:
                                                seq_6_083.append(0)
                                elif floatSamples[i][1] >= 0.84 and floatSamples[i][1] < 0.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_084.append(1)
                                        else:
                                                seq_6_084.append(0)
                                elif floatSamples[i][1] >= 0.85 and floatSamples[i][1] < 0.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_085.append(1)
                                        else:
                                                seq_6_085.append(0)
                                elif floatSamples[i][1] >= 0.86 and floatSamples[i][1] < 0.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_086.append(1)
                                        else:
                                                seq_6_086.append(0)
                                elif floatSamples[i][1] >= 0.87 and floatSamples[i][1] < 0.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_087.append(1)
                                        else:
                                                seq_6_087.append(0)
                                elif floatSamples[i][1] >= 0.88 and floatSamples[i][1] < 0.89:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_088.append(1)
                                        else:
                                                seq_6_088.append(0)
                                elif floatSamples[i][1] >= 0.89 and floatSamples[i][1] < 0.90:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_089.append(1)
                                        else:
                                                seq_6_089.append(0)
                                elif floatSamples[i][1] >= 0.90 and floatSamples[i][1] < 0.91:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_090.append(1)
                                        else:
                                                seq_6_090.append(0)
                                elif floatSamples[i][1] >= 0.91 and floatSamples[i][1] < 0.92:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_091.append(1)
                                        else:
                                                seq_6_091.append(0)
                                elif floatSamples[i][1] >= 2.4 and floatSamples[i][1] < 2.41: 
                                        if floatSamples[i][2]  > -100:
                                                seq_6_240.append(1)
                                        else:
                                                seq_6_240.append(0)
                                elif floatSamples[i][1] >= 2.41 and floatSamples[i][1] < 2.42:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_241.append(1)
                                        else:
                                                seq_6_241.append(0)
                                elif floatSamples[i][1] >= 2.42 and floatSamples[i][1] < 2.43:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_242.append(1)
                                        else:
                                                seq_6_242.append(0)
                                elif floatSamples[i][1] >= 2.43 and floatSamples[i][1] < 2.44:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_243.append(1)
                                        else:
                                                seq_6_243.append(0)
                                elif floatSamples[i][1] >= 2.44 and floatSamples[i][1] < 2.45:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_244.append(1)
                                        else:
                                                seq_6_244.append(0)
                                elif floatSamples[i][1] >= 2.45 and floatSamples[i][1] < 2.46:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_245.append(1)
                                        else:
                                                seq_6_245.append(0)
                                elif floatSamples[i][1] >= 2.46 and floatSamples[i][1] < 2.47:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_246.append(1)
                                        else:
                                                seq_6_246.append(0)
                                elif floatSamples[i][1] >= 2.47 and floatSamples[i][1] < 2.48:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_247.append(1)
                                        else:
                                                seq_6_247.append(0)
                                elif floatSamples[i][1] >= 2.48 and floatSamples[i][1] < 2.49:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_248.append(1)
                                        else:
                                                seq_6_248.append(0)
                                elif floatSamples[i][1] >= 2.49 and floatSamples[i][1] < 2.50:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_249.append(1)
                                        else:
                                                seq_6_249.append(0)
                                elif floatSamples[i][1] >= 5.71 and floatSamples[i][1] < 5.72:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_571.append(1)
                                        else:
                                                seq_6_571.append(0)
                                elif floatSamples[i][1] >= 5.72 and floatSamples[i][1] < 5.73:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_572.append(1)
                                        else:
                                                seq_6_572.append(0)
                                elif floatSamples[i][1] >= 5.73 and floatSamples[i][1] < 5.74:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_573.append(1)
                                        else:
                                                seq_6_573.append(0)
                                elif floatSamples[i][1] >= 5.74 and floatSamples[i][1] < 5.75:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_574.append(1)
                                        else:
                                                seq_6_574.append(0)
                                elif floatSamples[i][1] >= 5.75 and floatSamples[i][1] < 5.76:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_575.append(1)
                                        else:
                                                seq_6_575.append(0)
                                elif floatSamples[i][1] >= 5.76 and floatSamples[i][1] < 5.77:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_576.append(1)
                                        else:
                                                seq_6_576.append(0)
                                elif floatSamples[i][1] >= 5.77 and floatSamples[i][1] < 5.78:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_577.append(1)
                                        else:
                                                seq_6_577.append(0)
                                elif floatSamples[i][1] >= 5.78 and floatSamples[i][1] < 5.79:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_578.append(1)
                                        else:
                                                seq_6_578.append(0)
                                elif floatSamples[i][1] >= 5.79 and floatSamples[i][1] < 5.8:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_579.append(1)
                                        else:
                                                seq_6_579.append(0)
                                elif floatSamples[i][1] >= 5.8 and floatSamples[i][1] < 5.81:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_580.append(1)
                                        else:
                                                seq_6_580.append(0)
                                elif floatSamples[i][1] >= 5.81 and floatSamples[i][1] < 5.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_581.append(1)
                                        else:
                                                seq_6_581.append(0)
                                elif floatSamples[i][1] >= 5.82 and floatSamples[i][1] < 5.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_582.append(1)
                                        else:
                                                seq_6_582.append(0)
                                elif floatSamples[i][1] >= 5.83 and floatSamples[i][1] < 5.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_583.append(1)
                                        else:
                                                seq_6_583.append(0)
                                elif floatSamples[i][1] >= 5.84 and floatSamples[i][1] < 5.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_584.append(1)
                                        else:
                                                seq_6_584.append(0)
                                elif floatSamples[i][1] >= 5.85 and floatSamples[i][1] < 5.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_585.append(1)
                                        else:
                                                seq_6_585.append(0)
                                elif floatSamples[i][1] >= 5.86 and floatSamples[i][1] < 5.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_586.append(1)
                                        else:
                                                seq_6_586.append(0)
                                elif floatSamples[i][1] >= 5.87 and floatSamples[i][1] < 5.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_6_587.append(1)
                                        else:
                                                seq_6_587.append(0)
                        elif floatSamples[i][0] == 7:
                                if floatSamples[i][1] >= 0.8 and floatSamples[i][1] < 0.81:
                                        if floatSamples[i][2] > -100:
                                                seq_7_08.append(1)
                                        else:
                                                seq_7_08.append(0)
                                elif floatSamples[i][1] >= 0.81 and floatSamples[i][1] < 0.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_081.append(1)
                                        else:
                                                seq_7_081.append(0)
                                elif floatSamples[i][1] >= 0.82 and floatSamples[i][1] < 0.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_082.append(1)
                                        else:
                                                seq_7_082.append(0)
                                elif floatSamples[i][1] >= 0.83 and floatSamples[i][1] < 0.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_083.append(1)
                                        else:
                                                seq_7_083.append(0)
                                elif floatSamples[i][1] >= 0.84 and floatSamples[i][1] < 0.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_084.append(1)
                                        else:
                                                seq_7_084.append(0)
                                elif floatSamples[i][1] >= 0.85 and floatSamples[i][1] < 0.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_085.append(1)
                                        else:
                                                seq_7_085.append(0)
                                elif floatSamples[i][1] >= 0.86 and floatSamples[i][1] < 0.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_086.append(1)
                                        else:
                                                seq_7_086.append(0)
                                elif floatSamples[i][1] >= 0.87 and floatSamples[i][1] < 0.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_087.append(1)
                                        else:
                                                seq_7_087.append(0)
                                elif floatSamples[i][1] >= 0.88 and floatSamples[i][1] < 0.89:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_088.append(1)
                                        else:
                                                seq_7_088.append(0)
                                elif floatSamples[i][1] >= 0.89 and floatSamples[i][1] < 0.90:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_089.append(1)
                                        else:
                                                seq_7_089.append(0)
                                elif floatSamples[i][1] >= 0.90 and floatSamples[i][1] < 0.91:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_090.append(1)
                                        else:
                                                seq_7_090.append(0)
                                elif floatSamples[i][1] >= 0.91 and floatSamples[i][1] < 0.92:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_091.append(1)
                                        else:
                                                seq_7_091.append(0)
                                elif floatSamples[i][1] >= 2.4 and floatSamples[i][1] < 2.41: 
                                        if floatSamples[i][2]  > -100:
                                                seq_7_240.append(1)
                                        else:
                                                seq_7_240.append(0)
                                elif floatSamples[i][1] >= 2.41 and floatSamples[i][1] < 2.42:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_241.append(1)
                                        else:
                                                seq_7_241.append(0)
                                elif floatSamples[i][1] >= 2.42 and floatSamples[i][1] < 2.43:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_242.append(1)
                                        else:
                                                seq_7_242.append(0)
                                elif floatSamples[i][1] >= 2.43 and floatSamples[i][1] < 2.44:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_243.append(1)
                                        else:
                                                seq_7_243.append(0)
                                elif floatSamples[i][1] >= 2.44 and floatSamples[i][1] < 2.45:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_244.append(1)
                                        else:
                                                seq_7_244.append(0)
                                elif floatSamples[i][1] >= 2.45 and floatSamples[i][1] < 2.46:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_245.append(1)
                                        else:
                                                seq_7_245.append(0)
                                elif floatSamples[i][1] >= 2.46 and floatSamples[i][1] < 2.47:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_246.append(1)
                                        else:
                                                seq_7_246.append(0)
                                elif floatSamples[i][1] >= 2.47 and floatSamples[i][1] < 2.48:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_247.append(1)
                                        else:
                                                seq_7_247.append(0)
                                elif floatSamples[i][1] >= 2.48 and floatSamples[i][1] < 2.49:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_248.append(1)
                                        else:
                                                seq_7_248.append(0)
                                elif floatSamples[i][1] >= 2.49 and floatSamples[i][1] < 2.50:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_249.append(1)
                                        else:
                                                seq_7_249.append(0)
                                elif floatSamples[i][1] >= 5.71 and floatSamples[i][1] < 5.72:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_571.append(1)
                                        else:
                                                seq_7_571.append(0)
                                elif floatSamples[i][1] >= 5.72 and floatSamples[i][1] < 5.73:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_572.append(1)
                                        else:
                                                seq_7_572.append(0)
                                elif floatSamples[i][1] >= 5.73 and floatSamples[i][1] < 5.74:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_573.append(1)
                                        else:
                                                seq_7_573.append(0)
                                elif floatSamples[i][1] >= 5.74 and floatSamples[i][1] < 5.75:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_574.append(1)
                                        else:
                                                seq_7_574.append(0)
                                elif floatSamples[i][1] >= 5.75 and floatSamples[i][1] < 5.76:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_575.append(1)
                                        else:
                                                seq_7_575.append(0)
                                elif floatSamples[i][1] >= 5.76 and floatSamples[i][1] < 5.77:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_576.append(1)
                                        else:
                                                seq_7_576.append(0)
                                elif floatSamples[i][1] >= 5.77 and floatSamples[i][1] < 5.78:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_577.append(1)
                                        else:
                                                seq_7_577.append(0)
                                elif floatSamples[i][1] >= 5.78 and floatSamples[i][1] < 5.79:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_578.append(1)
                                        else:
                                                seq_7_578.append(0)
                                elif floatSamples[i][1] >= 5.79 and floatSamples[i][1] < 5.8:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_579.append(1)
                                        else:
                                                seq_7_579.append(0)
                                elif floatSamples[i][1] >= 5.8 and floatSamples[i][1] < 5.81:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_580.append(1)
                                        else:
                                                seq_7_580.append(0)
                                elif floatSamples[i][1] >= 5.81 and floatSamples[i][1] < 5.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_581.append(1)
                                        else:
                                                seq_7_581.append(0)
                                elif floatSamples[i][1] >= 5.82 and floatSamples[i][1] < 5.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_582.append(1)
                                        else:
                                                seq_7_582.append(0)
                                elif floatSamples[i][1] >= 5.83 and floatSamples[i][1] < 5.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_583.append(1)
                                        else:
                                                seq_7_583.append(0)
                                elif floatSamples[i][1] >= 5.84 and floatSamples[i][1] < 5.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_584.append(1)
                                        else:
                                                seq_7_584.append(0)
                                elif floatSamples[i][1] >= 5.85 and floatSamples[i][1] < 5.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_585.append(1)
                                        else:
                                                seq_7_585.append(0)
                                elif floatSamples[i][1] >= 5.86 and floatSamples[i][1] < 5.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_586.append(1)
                                        else:
                                                seq_7_586.append(0)
                                elif floatSamples[i][1] >= 5.87 and floatSamples[i][1] < 5.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_7_587.append(1)
                                        else:
                                                seq_7_587.append(0)
                        elif floatSamples[i][0] == 8:
                                if floatSamples[i][1] >= 0.8 and floatSamples[i][1] < 0.81:
                                        if floatSamples[i][2] > -100:
                                                seq_8_08.append(1)
                                        else:
                                                seq_8_08.append(0)
                                elif floatSamples[i][1] >= 0.81 and floatSamples[i][1] < 0.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_081.append(1)
                                        else:
                                                seq_8_081.append(0)
                                elif floatSamples[i][1] >= 0.82 and floatSamples[i][1] < 0.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_082.append(1)
                                        else:
                                                seq_8_082.append(0)
                                elif floatSamples[i][1] >= 0.83 and floatSamples[i][1] < 0.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_083.append(1)
                                        else:
                                                seq_8_083.append(0)
                                elif floatSamples[i][1] >= 0.84 and floatSamples[i][1] < 0.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_084.append(1)
                                        else:
                                                seq_8_084.append(0)
                                elif floatSamples[i][1] >= 0.85 and floatSamples[i][1] < 0.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_085.append(1)
                                        else:
                                                seq_8_085.append(0)
                                elif floatSamples[i][1] >= 0.86 and floatSamples[i][1] < 0.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_086.append(1)
                                        else:
                                                seq_8_086.append(0)
                                elif floatSamples[i][1] >= 0.87 and floatSamples[i][1] < 0.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_087.append(1)
                                        else:
                                                seq_8_087.append(0)
                                elif floatSamples[i][1] >= 0.88 and floatSamples[i][1] < 0.89:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_088.append(1)
                                        else:
                                                seq_8_088.append(0)
                                elif floatSamples[i][1] >= 0.89 and floatSamples[i][1] < 0.90:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_089.append(1)
                                        else:
                                                seq_8_089.append(0)
                                elif floatSamples[i][1] >= 0.90 and floatSamples[i][1] < 0.91:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_090.append(1)
                                        else:
                                                seq_8_090.append(0)
                                elif floatSamples[i][1] >= 0.91 and floatSamples[i][1] < 0.92:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_091.append(1)
                                        else:
                                                seq_8_091.append(0)
                                elif floatSamples[i][1] >= 2.4 and floatSamples[i][1] < 2.41: 
                                        if floatSamples[i][2]  > -100:
                                                seq_8_240.append(1)
                                        else:
                                                seq_8_240.append(0)
                                elif floatSamples[i][1] >= 2.41 and floatSamples[i][1] < 2.42:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_241.append(1)
                                        else:
                                                seq_8_241.append(0)
                                elif floatSamples[i][1] >= 2.42 and floatSamples[i][1] < 2.43:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_242.append(1)
                                        else:
                                                seq_8_242.append(0)
                                elif floatSamples[i][1] >= 2.43 and floatSamples[i][1] < 2.44:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_243.append(1)
                                        else:
                                                seq_8_243.append(0)
                                elif floatSamples[i][1] >= 2.44 and floatSamples[i][1] < 2.45:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_244.append(1)
                                        else:
                                                seq_8_244.append(0)
                                elif floatSamples[i][1] >= 2.45 and floatSamples[i][1] < 2.46:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_245.append(1)
                                        else:
                                                seq_8_245.append(0)
                                elif floatSamples[i][1] >= 2.46 and floatSamples[i][1] < 2.47:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_246.append(1)
                                        else:
                                                seq_8_246.append(0)
                                elif floatSamples[i][1] >= 2.47 and floatSamples[i][1] < 2.48:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_247.append(1)
                                        else:
                                                seq_8_247.append(0)
                                elif floatSamples[i][1] >= 2.48 and floatSamples[i][1] < 2.49:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_248.append(1)
                                        else:
                                                seq_8_248.append(0)
                                elif floatSamples[i][1] >= 2.49 and floatSamples[i][1] < 2.50:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_249.append(1)
                                        else:
                                                seq_8_249.append(0)
                                elif floatSamples[i][1] >= 5.71 and floatSamples[i][1] < 5.72:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_571.append(1)
                                        else:
                                                seq_8_571.append(0)
                                elif floatSamples[i][1] >= 5.72 and floatSamples[i][1] < 5.73:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_572.append(1)
                                        else:
                                                seq_8_572.append(0)
                                elif floatSamples[i][1] >= 5.73 and floatSamples[i][1] < 5.74:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_573.append(1)
                                        else:
                                                seq_8_573.append(0)
                                elif floatSamples[i][1] >= 5.74 and floatSamples[i][1] < 5.75:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_574.append(1)
                                        else:
                                                seq_8_574.append(0)
                                elif floatSamples[i][1] >= 5.75 and floatSamples[i][1] < 5.76:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_575.append(1)
                                        else:
                                                seq_8_575.append(0)
                                elif floatSamples[i][1] >= 5.76 and floatSamples[i][1] < 5.77:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_576.append(1)
                                        else:
                                                seq_8_576.append(0)
                                elif floatSamples[i][1] >= 5.77 and floatSamples[i][1] < 5.78:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_577.append(1)
                                        else:
                                                seq_8_577.append(0)
                                elif floatSamples[i][1] >= 5.78 and floatSamples[i][1] < 5.79:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_578.append(1)
                                        else:
                                                seq_8_578.append(0)
                                elif floatSamples[i][1] >= 5.79 and floatSamples[i][1] < 5.8:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_579.append(1)
                                        else:
                                                seq_8_579.append(0)
                                elif floatSamples[i][1] >= 5.8 and floatSamples[i][1] < 5.81:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_580.append(1)
                                        else:
                                                seq_8_580.append(0)
                                elif floatSamples[i][1] >= 5.81 and floatSamples[i][1] < 5.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_581.append(1)
                                        else:
                                                seq_8_581.append(0)
                                elif floatSamples[i][1] >= 5.82 and floatSamples[i][1] < 5.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_582.append(1)
                                        else:
                                                seq_8_582.append(0)
                                elif floatSamples[i][1] >= 5.83 and floatSamples[i][1] < 5.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_583.append(1)
                                        else:
                                                seq_8_583.append(0)
                                elif floatSamples[i][1] >= 5.84 and floatSamples[i][1] < 5.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_584.append(1)
                                        else:
                                                seq_8_584.append(0)
                                elif floatSamples[i][1] >= 5.85 and floatSamples[i][1] < 5.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_585.append(1)
                                        else:
                                                seq_8_585.append(0)
                                elif floatSamples[i][1] >= 5.86 and floatSamples[i][1] < 5.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_586.append(1)
                                        else:
                                                seq_8_586.append(0)
                                elif floatSamples[i][1] >= 5.87 and floatSamples[i][1] < 5.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_8_587.append(1)
                                        else:
                                                seq_8_587.append(0)
                        elif floatSamples[i][0] == 9:
                                if floatSamples[i][1] >= 0.8 and floatSamples[i][1] < 0.81:
                                        if floatSamples[i][2] > -100:
                                                seq_9_08.append(1)
                                        else:
                                                seq_9_08.append(0)
                                elif floatSamples[i][1] >= 0.81 and floatSamples[i][1] < 0.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_081.append(1)
                                        else:
                                                seq_9_081.append(0)
                                elif floatSamples[i][1] >= 0.82 and floatSamples[i][1] < 0.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_082.append(1)
                                        else:
                                                seq_9_082.append(0)
                                elif floatSamples[i][1] >= 0.83 and floatSamples[i][1] < 0.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_083.append(1)
                                        else:
                                                seq_9_083.append(0)
                                elif floatSamples[i][1] >= 0.84 and floatSamples[i][1] < 0.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_084.append(1)
                                        else:
                                                seq_9_084.append(0)
                                elif floatSamples[i][1] >= 0.85 and floatSamples[i][1] < 0.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_085.append(1)
                                        else:
                                                seq_9_085.append(0)
                                elif floatSamples[i][1] >= 0.86 and floatSamples[i][1] < 0.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_086.append(1)
                                        else:
                                                seq_9_086.append(0)
                                elif floatSamples[i][1] >= 0.87 and floatSamples[i][1] < 0.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_087.append(1)
                                        else:
                                                seq_9_087.append(0)
                                elif floatSamples[i][1] >= 0.88 and floatSamples[i][1] < 0.89:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_088.append(1)
                                        else:
                                                seq_9_088.append(0)
                                elif floatSamples[i][1] >= 0.89 and floatSamples[i][1] < 0.90:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_089.append(1)
                                        else:
                                                seq_9_089.append(0)
                                elif floatSamples[i][1] >= 0.90 and floatSamples[i][1] < 0.91:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_090.append(1)
                                        else:
                                                seq_9_090.append(0)
                                elif floatSamples[i][1] >= 0.91 and floatSamples[i][1] < 0.92:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_091.append(1)
                                        else:
                                                seq_9_091.append(0)
                                elif floatSamples[i][1] >= 2.4 and floatSamples[i][1] < 2.41: 
                                        if floatSamples[i][2]  > -100:
                                                seq_9_240.append(1)
                                        else:
                                                seq_9_240.append(0)
                                elif floatSamples[i][1] >= 2.41 and floatSamples[i][1] < 2.42:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_241.append(1)
                                        else:
                                                seq_9_241.append(0)
                                elif floatSamples[i][1] >= 2.42 and floatSamples[i][1] < 2.43:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_242.append(1)
                                        else:
                                                seq_9_242.append(0)
                                elif floatSamples[i][1] >= 2.43 and floatSamples[i][1] < 2.44:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_243.append(1)
                                        else:
                                                seq_9_243.append(0)
                                elif floatSamples[i][1] >= 2.44 and floatSamples[i][1] < 2.45:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_244.append(1)
                                        else:
                                                seq_9_244.append(0)
                                elif floatSamples[i][1] >= 2.45 and floatSamples[i][1] < 2.46:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_245.append(1)
                                        else:
                                                seq_9_245.append(0)
                                elif floatSamples[i][1] >= 2.46 and floatSamples[i][1] < 2.47:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_246.append(1)
                                        else:
                                                seq_9_246.append(0)
                                elif floatSamples[i][1] >= 2.47 and floatSamples[i][1] < 2.48:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_247.append(1)
                                        else:
                                                seq_9_247.append(0)
                                elif floatSamples[i][1] >= 2.48 and floatSamples[i][1] < 2.49:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_248.append(1)
                                        else:
                                                seq_9_248.append(0)
                                elif floatSamples[i][1] >= 2.49 and floatSamples[i][1] < 2.50:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_249.append(1)
                                        else:
                                                seq_9_249.append(0)
                                elif floatSamples[i][1] >= 5.71 and floatSamples[i][1] < 5.72:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_571.append(1)
                                        else:
                                                seq_9_571.append(0)
                                elif floatSamples[i][1] >= 5.72 and floatSamples[i][1] < 5.73:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_572.append(1)
                                        else:
                                                seq_9_572.append(0)
                                elif floatSamples[i][1] >= 5.73 and floatSamples[i][1] < 5.74:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_573.append(1)
                                        else:
                                                seq_9_573.append(0)
                                elif floatSamples[i][1] >= 5.74 and floatSamples[i][1] < 5.75:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_574.append(1)
                                        else:
                                                seq_9_574.append(0)
                                elif floatSamples[i][1] >= 5.75 and floatSamples[i][1] < 5.76:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_575.append(1)
                                        else:
                                                seq_9_575.append(0)
                                elif floatSamples[i][1] >= 5.76 and floatSamples[i][1] < 5.77:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_576.append(1)
                                        else:
                                                seq_9_576.append(0)
                                elif floatSamples[i][1] >= 5.77 and floatSamples[i][1] < 5.78:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_577.append(1)
                                        else:
                                                seq_9_577.append(0)
                                elif floatSamples[i][1] >= 5.78 and floatSamples[i][1] < 5.79:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_578.append(1)
                                        else:
                                                seq_9_578.append(0)
                                elif floatSamples[i][1] >= 5.79 and floatSamples[i][1] < 5.8:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_579.append(1)
                                        else:
                                                seq_9_579.append(0)
                                elif floatSamples[i][1] >= 5.8 and floatSamples[i][1] < 5.81:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_580.append(1)
                                        else:
                                                seq_9_580.append(0)
                                elif floatSamples[i][1] >= 5.81 and floatSamples[i][1] < 5.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_581.append(1)
                                        else:
                                                seq_9_581.append(0)
                                elif floatSamples[i][1] >= 5.82 and floatSamples[i][1] < 5.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_582.append(1)
                                        else:
                                                seq_9_582.append(0)
                                elif floatSamples[i][1] >= 5.83 and floatSamples[i][1] < 5.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_583.append(1)
                                        else:
                                                seq_9_583.append(0)
                                elif floatSamples[i][1] >= 5.84 and floatSamples[i][1] < 5.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_584.append(1)
                                        else:
                                                seq_9_584.append(0)
                                elif floatSamples[i][1] >= 5.85 and floatSamples[i][1] < 5.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_585.append(1)
                                        else:
                                                seq_9_585.append(0)
                                elif floatSamples[i][1] >= 5.86 and floatSamples[i][1] < 5.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_586.append(1)
                                        else:
                                                seq_9_586.append(0)
                                elif floatSamples[i][1] >= 5.87 and floatSamples[i][1] < 5.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_9_587.append(1)
                                        else:
                                                seq_9_587.append(0)
                        elif floatSamples[i][0] == 10:
                                if floatSamples[i][1] >= 0.8 and floatSamples[i][1] < 0.81:
                                        if floatSamples[i][2] > -100:
                                                seq_10_08.append(1)
                                        else:
                                                seq_10_08.append(0)
                                elif floatSamples[i][1] >= 0.81 and floatSamples[i][1] < 0.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_081.append(1)
                                        else:
                                                seq_10_081.append(0)
                                elif floatSamples[i][1] >= 0.82 and floatSamples[i][1] < 0.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_082.append(1)
                                        else:
                                                seq_10_082.append(0)
                                elif floatSamples[i][1] >= 0.83 and floatSamples[i][1] < 0.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_083.append(1)
                                        else:
                                                seq_10_083.append(0)
                                elif floatSamples[i][1] >= 0.84 and floatSamples[i][1] < 0.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_084.append(1)
                                        else:
                                                seq_10_084.append(0)
                                elif floatSamples[i][1] >= 0.85 and floatSamples[i][1] < 0.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_085.append(1)
                                        else:
                                                seq_10_085.append(0)
                                elif floatSamples[i][1] >= 0.86 and floatSamples[i][1] < 0.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_086.append(1)
                                        else:
                                                seq_10_086.append(0)
                                elif floatSamples[i][1] >= 0.87 and floatSamples[i][1] < 0.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_087.append(1)
                                        else:
                                                seq_10_087.append(0)
                                elif floatSamples[i][1] >= 0.88 and floatSamples[i][1] < 0.89:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_088.append(1)
                                        else:
                                                seq_10_088.append(0)
                                elif floatSamples[i][1] >= 0.89 and floatSamples[i][1] < 0.90:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_089.append(1)
                                        else:
                                                seq_10_089.append(0)
                                elif floatSamples[i][1] >= 0.90 and floatSamples[i][1] < 0.91:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_090.append(1)
                                        else:
                                                seq_10_090.append(0)
                                elif floatSamples[i][1] >= 0.91 and floatSamples[i][1] < 0.92:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_091.append(1)
                                        else:
                                                seq_10_091.append(0)
                                elif floatSamples[i][1] >= 2.4 and floatSamples[i][1] < 2.41: 
                                        if floatSamples[i][2]  > -100:
                                                seq_10_240.append(1)
                                        else:
                                                seq_10_240.append(0)
                                elif floatSamples[i][1] >= 2.41 and floatSamples[i][1] < 2.42:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_241.append(1)
                                        else:
                                                seq_10_241.append(0)
                                elif floatSamples[i][1] >= 2.42 and floatSamples[i][1] < 2.43:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_242.append(1)
                                        else:
                                                seq_10_242.append(0)
                                elif floatSamples[i][1] >= 2.43 and floatSamples[i][1] < 2.44:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_243.append(1)
                                        else:
                                                seq_10_243.append(0)
                                elif floatSamples[i][1] >= 2.44 and floatSamples[i][1] < 2.45:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_244.append(1)
                                        else:
                                                seq_10_244.append(0)
                                elif floatSamples[i][1] >= 2.45 and floatSamples[i][1] < 2.46:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_245.append(1)
                                        else:
                                                seq_10_245.append(0)
                                elif floatSamples[i][1] >= 2.46 and floatSamples[i][1] < 2.47:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_246.append(1)
                                        else:
                                                seq_10_246.append(0)
                                elif floatSamples[i][1] >= 2.47 and floatSamples[i][1] < 2.48:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_247.append(1)
                                        else:
                                                seq_10_247.append(0)
                                elif floatSamples[i][1] >= 2.48 and floatSamples[i][1] < 2.49:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_248.append(1)
                                        else:
                                                seq_10_248.append(0)
                                elif floatSamples[i][1] >= 2.49 and floatSamples[i][1] < 2.50:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_249.append(1)
                                        else:
                                                seq_10_249.append(0)
                                elif floatSamples[i][1] >= 5.71 and floatSamples[i][1] < 5.72:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_571.append(1)
                                        else:
                                                seq_10_571.append(0)
                                elif floatSamples[i][1] >= 5.72 and floatSamples[i][1] < 5.73:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_572.append(1)
                                        else:
                                                seq_10_572.append(0)
                                elif floatSamples[i][1] >= 5.73 and floatSamples[i][1] < 5.74:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_573.append(1)
                                        else:
                                                seq_10_573.append(0)
                                elif floatSamples[i][1] >= 5.74 and floatSamples[i][1] < 5.75:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_574.append(1)
                                        else:
                                                seq_10_574.append(0)
                                elif floatSamples[i][1] >= 5.75 and floatSamples[i][1] < 5.76:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_575.append(1)
                                        else:
                                                seq_10_575.append(0)
                                elif floatSamples[i][1] >= 5.76 and floatSamples[i][1] < 5.77:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_576.append(1)
                                        else:
                                                seq_10_576.append(0)
                                elif floatSamples[i][1] >= 5.77 and floatSamples[i][1] < 5.78:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_577.append(1)
                                        else:
                                                seq_10_577.append(0)
                                elif floatSamples[i][1] >= 5.78 and floatSamples[i][1] < 5.79:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_578.append(1)
                                        else:
                                                seq_10_578.append(0)
                                elif floatSamples[i][1] >= 5.79 and floatSamples[i][1] < 5.8:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_579.append(1)
                                        else:
                                                seq_10_579.append(0)
                                elif floatSamples[i][1] >= 5.8 and floatSamples[i][1] < 5.81:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_580.append(1)
                                        else:
                                                seq_10_580.append(0)
                                elif floatSamples[i][1] >= 5.81 and floatSamples[i][1] < 5.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_581.append(1)
                                        else:
                                                seq_10_581.append(0)
                                elif floatSamples[i][1] >= 5.82 and floatSamples[i][1] < 5.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_582.append(1)
                                        else:
                                                seq_10_582.append(0)
                                elif floatSamples[i][1] >= 5.83 and floatSamples[i][1] < 5.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_583.append(1)
                                        else:
                                                seq_10_583.append(0)
                                elif floatSamples[i][1] >= 5.84 and floatSamples[i][1] < 5.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_584.append(1)
                                        else:
                                                seq_10_584.append(0)
                                elif floatSamples[i][1] >= 5.85 and floatSamples[i][1] < 5.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_585.append(1)
                                        else:
                                                seq_10_585.append(0)
                                elif floatSamples[i][1] >= 5.86 and floatSamples[i][1] < 5.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_586.append(1)
                                        else:
                                                seq_10_586.append(0)
                                elif floatSamples[i][1] >= 5.87 and floatSamples[i][1] < 5.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_10_587.append(1)
                                        else:
                                                seq_10_587.append(0)
                        elif floatSamples[i][0] == 11:
                                if floatSamples[i][1] >= 0.8 and floatSamples[i][1] < 0.81:
                                        if floatSamples[i][2] > -100:
                                                seq_11_08.append(1)
                                        else:
                                                seq_11_08.append(0)
                                elif floatSamples[i][1] >= 0.81 and floatSamples[i][1] < 0.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_081.append(1)
                                        else:
                                                seq_11_081.append(0)
                                elif floatSamples[i][1] >= 0.82 and floatSamples[i][1] < 0.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_082.append(1)
                                        else:
                                                seq_11_082.append(0)
                                elif floatSamples[i][1] >= 0.83 and floatSamples[i][1] < 0.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_083.append(1)
                                        else:
                                                seq_11_083.append(0)
                                elif floatSamples[i][1] >= 0.84 and floatSamples[i][1] < 0.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_084.append(1)
                                        else:
                                                seq_11_084.append(0)
                                elif floatSamples[i][1] >= 0.85 and floatSamples[i][1] < 0.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_085.append(1)
                                        else:
                                                seq_11_085.append(0)
                                elif floatSamples[i][1] >= 0.86 and floatSamples[i][1] < 0.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_086.append(1)
                                        else:
                                                seq_11_086.append(0)
                                elif floatSamples[i][1] >= 0.87 and floatSamples[i][1] < 0.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_087.append(1)
                                        else:
                                                seq_11_087.append(0)
                                elif floatSamples[i][1] >= 0.88 and floatSamples[i][1] < 0.89:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_088.append(1)
                                        else:
                                                seq_11_088.append(0)
                                elif floatSamples[i][1] >= 0.89 and floatSamples[i][1] < 0.90:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_089.append(1)
                                        else:
                                                seq_11_089.append(0)
                                elif floatSamples[i][1] >= 0.90 and floatSamples[i][1] < 0.91:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_090.append(1)
                                        else:
                                                seq_11_090.append(0)
                                elif floatSamples[i][1] >= 0.91 and floatSamples[i][1] < 0.92:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_091.append(1)
                                        else:
                                                seq_11_091.append(0)
                                elif floatSamples[i][1] >= 2.4 and floatSamples[i][1] < 2.41: 
                                        if floatSamples[i][2]  > -100:
                                                seq_11_240.append(1)
                                        else:
                                                seq_11_240.append(0)
                                elif floatSamples[i][1] >= 2.41 and floatSamples[i][1] < 2.42:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_241.append(1)
                                        else:
                                                seq_11_241.append(0)
                                elif floatSamples[i][1] >= 2.42 and floatSamples[i][1] < 2.43:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_242.append(1)
                                        else:
                                                seq_11_242.append(0)
                                elif floatSamples[i][1] >= 2.43 and floatSamples[i][1] < 2.44:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_243.append(1)
                                        else:
                                                seq_11_243.append(0)
                                elif floatSamples[i][1] >= 2.44 and floatSamples[i][1] < 2.45:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_244.append(1)
                                        else:
                                                seq_11_244.append(0)
                                elif floatSamples[i][1] >= 2.45 and floatSamples[i][1] < 2.46:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_245.append(1)
                                        else:
                                                seq_11_245.append(0)
                                elif floatSamples[i][1] >= 2.46 and floatSamples[i][1] < 2.47:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_246.append(1)
                                        else:
                                                seq_11_246.append(0)
                                elif floatSamples[i][1] >= 2.47 and floatSamples[i][1] < 2.48:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_247.append(1)
                                        else:
                                                seq_11_247.append(0)
                                elif floatSamples[i][1] >= 2.48 and floatSamples[i][1] < 2.49:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_248.append(1)
                                        else:
                                                seq_11_248.append(0)
                                elif floatSamples[i][1] >= 2.49 and floatSamples[i][1] < 2.50:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_249.append(1)
                                        else:
                                                seq_11_249.append(0)
                                elif floatSamples[i][1] >= 5.71 and floatSamples[i][1] < 5.72:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_571.append(1)
                                        else:
                                                seq_11_571.append(0)
                                elif floatSamples[i][1] >= 5.72 and floatSamples[i][1] < 5.73:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_572.append(1)
                                        else:
                                                seq_11_572.append(0)
                                elif floatSamples[i][1] >= 5.73 and floatSamples[i][1] < 5.74:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_573.append(1)
                                        else:
                                                seq_11_573.append(0)
                                elif floatSamples[i][1] >= 5.74 and floatSamples[i][1] < 5.75:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_574.append(1)
                                        else:
                                                seq_11_574.append(0)
                                elif floatSamples[i][1] >= 5.75 and floatSamples[i][1] < 5.76:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_575.append(1)
                                        else:
                                                seq_11_575.append(0)
                                elif floatSamples[i][1] >= 5.76 and floatSamples[i][1] < 5.77:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_576.append(1)
                                        else:
                                                seq_11_576.append(0)
                                elif floatSamples[i][1] >= 5.77 and floatSamples[i][1] < 5.78:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_577.append(1)
                                        else:
                                                seq_11_577.append(0)
                                elif floatSamples[i][1] >= 5.78 and floatSamples[i][1] < 5.79:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_578.append(1)
                                        else:
                                                seq_11_578.append(0)
                                elif floatSamples[i][1] >= 5.79 and floatSamples[i][1] < 5.8:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_579.append(1)
                                        else:
                                                seq_11_579.append(0)
                                elif floatSamples[i][1] >= 5.8 and floatSamples[i][1] < 5.81:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_580.append(1)
                                        else:
                                                seq_11_580.append(0)
                                elif floatSamples[i][1] >= 5.81 and floatSamples[i][1] < 5.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_581.append(1)
                                        else:
                                                seq_11_581.append(0)
                                elif floatSamples[i][1] >= 5.82 and floatSamples[i][1] < 5.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_582.append(1)
                                        else:
                                                seq_11_582.append(0)
                                elif floatSamples[i][1] >= 5.83 and floatSamples[i][1] < 5.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_583.append(1)
                                        else:
                                                seq_11_583.append(0)
                                elif floatSamples[i][1] >= 5.84 and floatSamples[i][1] < 5.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_584.append(1)
                                        else:
                                                seq_11_584.append(0)
                                elif floatSamples[i][1] >= 5.85 and floatSamples[i][1] < 5.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_585.append(1)
                                        else:
                                                seq_11_585.append(0)
                                elif floatSamples[i][1] >= 5.86 and floatSamples[i][1] < 5.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_586.append(1)
                                        else:
                                                seq_11_586.append(0)
                                elif floatSamples[i][1] >= 5.87 and floatSamples[i][1] < 5.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_11_587.append(1)
                                        else:
                                                seq_11_587.append(0)
                        elif floatSamples[i][0] == 12:
                                if floatSamples[i][1] >= 0.8 and floatSamples[i][1] < 0.81:
                                        if floatSamples[i][2] > -100:
                                                seq_12_08.append(1)
                                        else:
                                                seq_12_08.append(0)
                                elif floatSamples[i][1] >= 0.81 and floatSamples[i][1] < 0.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_081.append(1)
                                        else:
                                                seq_12_081.append(0)
                                elif floatSamples[i][1] >= 0.82 and floatSamples[i][1] < 0.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_082.append(1)
                                        else:
                                                seq_12_082.append(0)
                                elif floatSamples[i][1] >= 0.83 and floatSamples[i][1] < 0.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_083.append(1)
                                        else:
                                                seq_12_083.append(0)
                                elif floatSamples[i][1] >= 0.84 and floatSamples[i][1] < 0.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_084.append(1)
                                        else:
                                                seq_12_084.append(0)
                                elif floatSamples[i][1] >= 0.85 and floatSamples[i][1] < 0.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_085.append(1)
                                        else:
                                                seq_12_085.append(0)
                                elif floatSamples[i][1] >= 0.86 and floatSamples[i][1] < 0.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_086.append(1)
                                        else:
                                                seq_12_086.append(0)
                                elif floatSamples[i][1] >= 0.87 and floatSamples[i][1] < 0.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_087.append(1)
                                        else:
                                                seq_12_087.append(0)
                                elif floatSamples[i][1] >= 0.88 and floatSamples[i][1] < 0.89:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_088.append(1)
                                        else:
                                                seq_12_088.append(0)
                                elif floatSamples[i][1] >= 0.89 and floatSamples[i][1] < 0.90:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_089.append(1)
                                        else:
                                                seq_12_089.append(0)
                                elif floatSamples[i][1] >= 0.90 and floatSamples[i][1] < 0.91:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_090.append(1)
                                        else:
                                                seq_12_090.append(0)
                                elif floatSamples[i][1] >= 0.91 and floatSamples[i][1] < 0.92:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_091.append(1)
                                        else:
                                                seq_12_091.append(0)
                                elif floatSamples[i][1] >= 2.4 and floatSamples[i][1] < 2.41: 
                                        if floatSamples[i][2]  > -100:
                                                seq_12_240.append(1)
                                        else:
                                                seq_12_240.append(0)
                                elif floatSamples[i][1] >= 2.41 and floatSamples[i][1] < 2.42:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_241.append(1)
                                        else:
                                                seq_12_241.append(0)
                                elif floatSamples[i][1] >= 2.42 and floatSamples[i][1] < 2.43:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_242.append(1)
                                        else:
                                                seq_12_242.append(0)
                                elif floatSamples[i][1] >= 2.43 and floatSamples[i][1] < 2.44:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_243.append(1)
                                        else:
                                                seq_12_243.append(0)
                                elif floatSamples[i][1] >= 2.44 and floatSamples[i][1] < 2.45:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_244.append(1)
                                        else:
                                                seq_12_244.append(0)
                                elif floatSamples[i][1] >= 2.45 and floatSamples[i][1] < 2.46:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_245.append(1)
                                        else:
                                                seq_12_245.append(0)
                                elif floatSamples[i][1] >= 2.46 and floatSamples[i][1] < 2.47:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_246.append(1)
                                        else:
                                                seq_12_246.append(0)
                                elif floatSamples[i][1] >= 2.47 and floatSamples[i][1] < 2.48:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_247.append(1)
                                        else:
                                                seq_12_247.append(0)
                                elif floatSamples[i][1] >= 2.48 and floatSamples[i][1] < 2.49:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_248.append(1)
                                        else:
                                                seq_12_248.append(0)
                                elif floatSamples[i][1] >= 2.49 and floatSamples[i][1] < 2.50:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_249.append(1)
                                        else:
                                                seq_12_249.append(0)
                                elif floatSamples[i][1] >= 5.71 and floatSamples[i][1] < 5.72:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_571.append(1)
                                        else:
                                                seq_12_571.append(0)
                                elif floatSamples[i][1] >= 5.72 and floatSamples[i][1] < 5.73:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_572.append(1)
                                        else:
                                                seq_12_572.append(0)
                                elif floatSamples[i][1] >= 5.73 and floatSamples[i][1] < 5.74:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_573.append(1)
                                        else:
                                                seq_12_573.append(0)
                                elif floatSamples[i][1] >= 5.74 and floatSamples[i][1] < 5.75:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_574.append(1)
                                        else:
                                                seq_12_574.append(0)
                                elif floatSamples[i][1] >= 5.75 and floatSamples[i][1] < 5.76:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_575.append(1)
                                        else:
                                                seq_12_575.append(0)
                                elif floatSamples[i][1] >= 5.76 and floatSamples[i][1] < 5.77:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_576.append(1)
                                        else:
                                                seq_12_576.append(0)
                                elif floatSamples[i][1] >= 5.77 and floatSamples[i][1] < 5.78:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_577.append(1)
                                        else:
                                                seq_12_577.append(0)
                                elif floatSamples[i][1] >= 5.78 and floatSamples[i][1] < 5.79:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_578.append(1)
                                        else:
                                                seq_12_578.append(0)
                                elif floatSamples[i][1] >= 5.79 and floatSamples[i][1] < 5.8:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_579.append(1)
                                        else:
                                                seq_12_579.append(0)
                                elif floatSamples[i][1] >= 5.8 and floatSamples[i][1] < 5.81:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_580.append(1)
                                        else:
                                                seq_12_580.append(0)
                                elif floatSamples[i][1] >= 5.81 and floatSamples[i][1] < 5.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_581.append(1)
                                        else:
                                                seq_12_581.append(0)
                                elif floatSamples[i][1] >= 5.82 and floatSamples[i][1] < 5.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_582.append(1)
                                        else:
                                                seq_12_582.append(0)
                                elif floatSamples[i][1] >= 5.83 and floatSamples[i][1] < 5.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_583.append(1)
                                        else:
                                                seq_12_583.append(0)
                                elif floatSamples[i][1] >= 5.84 and floatSamples[i][1] < 5.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_584.append(1)
                                        else:
                                                seq_12_584.append(0)
                                elif floatSamples[i][1] >= 5.85 and floatSamples[i][1] < 5.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_585.append(1)
                                        else:
                                                seq_12_585.append(0)
                                elif floatSamples[i][1] >= 5.86 and floatSamples[i][1] < 5.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_586.append(1)
                                        else:
                                                seq_12_586.append(0)
                                elif floatSamples[i][1] >= 5.87 and floatSamples[i][1] < 5.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_12_587.append(1)
                                        else:
                                                seq_12_587.append(0)
                        elif floatSamples[i][0] == 13:
                                if floatSamples[i][1] >= 0.8 and floatSamples[i][1] < 0.81:
                                        if floatSamples[i][2] > -100:
                                                seq_13_08.append(1)
                                        else:
                                                seq_13_08.append(0)
                                elif floatSamples[i][1] >= 0.81 and floatSamples[i][1] < 0.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_081.append(1)
                                        else:
                                                seq_13_081.append(0)
                                elif floatSamples[i][1] >= 0.82 and floatSamples[i][1] < 0.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_082.append(1)
                                        else:
                                                seq_13_082.append(0)
                                elif floatSamples[i][1] >= 0.83 and floatSamples[i][1] < 0.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_083.append(1)
                                        else:
                                                seq_13_083.append(0)
                                elif floatSamples[i][1] >= 0.84 and floatSamples[i][1] < 0.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_084.append(1)
                                        else:
                                                seq_13_084.append(0)
                                elif floatSamples[i][1] >= 0.85 and floatSamples[i][1] < 0.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_085.append(1)
                                        else:
                                                seq_13_085.append(0)
                                elif floatSamples[i][1] >= 0.86 and floatSamples[i][1] < 0.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_086.append(1)
                                        else:
                                                seq_13_086.append(0)
                                elif floatSamples[i][1] >= 0.87 and floatSamples[i][1] < 0.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_087.append(1)
                                        else:
                                                seq_13_087.append(0)
                                elif floatSamples[i][1] >= 0.88 and floatSamples[i][1] < 0.89:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_088.append(1)
                                        else:
                                                seq_13_088.append(0)
                                elif floatSamples[i][1] >= 0.89 and floatSamples[i][1] < 0.90:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_089.append(1)
                                        else:
                                                seq_13_089.append(0)
                                elif floatSamples[i][1] >= 0.90 and floatSamples[i][1] < 0.91:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_090.append(1)
                                        else:
                                                seq_13_090.append(0)
                                elif floatSamples[i][1] >= 0.91 and floatSamples[i][1] < 0.92:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_091.append(1)
                                        else:
                                                seq_13_091.append(0)
                                elif floatSamples[i][1] >= 2.4 and floatSamples[i][1] < 2.41: 
                                        if floatSamples[i][2]  > -100:
                                                seq_13_240.append(1)
                                        else:
                                                seq_13_240.append(0)
                                elif floatSamples[i][1] >= 2.41 and floatSamples[i][1] < 2.42:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_241.append(1)
                                        else:
                                                seq_13_241.append(0)
                                elif floatSamples[i][1] >= 2.42 and floatSamples[i][1] < 2.43:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_242.append(1)
                                        else:
                                                seq_13_242.append(0)
                                elif floatSamples[i][1] >= 2.43 and floatSamples[i][1] < 2.44:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_243.append(1)
                                        else:
                                                seq_13_243.append(0)
                                elif floatSamples[i][1] >= 2.44 and floatSamples[i][1] < 2.45:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_244.append(1)
                                        else:
                                                seq_13_244.append(0)
                                elif floatSamples[i][1] >= 2.45 and floatSamples[i][1] < 2.46:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_245.append(1)
                                        else:
                                                seq_13_245.append(0)
                                elif floatSamples[i][1] >= 2.46 and floatSamples[i][1] < 2.47:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_246.append(1)
                                        else:
                                                seq_13_246.append(0)
                                elif floatSamples[i][1] >= 2.47 and floatSamples[i][1] < 2.48:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_247.append(1)
                                        else:
                                                seq_13_247.append(0)
                                elif floatSamples[i][1] >= 2.48 and floatSamples[i][1] < 2.49:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_248.append(1)
                                        else:
                                                seq_13_248.append(0)
                                elif floatSamples[i][1] >= 2.49 and floatSamples[i][1] < 2.50:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_249.append(1)
                                        else:
                                                seq_13_249.append(0)
                                elif floatSamples[i][1] >= 5.71 and floatSamples[i][1] < 5.72:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_571.append(1)
                                        else:
                                                seq_13_571.append(0)
                                elif floatSamples[i][1] >= 5.72 and floatSamples[i][1] < 5.73:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_572.append(1)
                                        else:
                                                seq_13_572.append(0)
                                elif floatSamples[i][1] >= 5.73 and floatSamples[i][1] < 5.74:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_573.append(1)
                                        else:
                                                seq_13_573.append(0)
                                elif floatSamples[i][1] >= 5.74 and floatSamples[i][1] < 5.75:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_574.append(1)
                                        else:
                                                seq_13_574.append(0)
                                elif floatSamples[i][1] >= 5.75 and floatSamples[i][1] < 5.76:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_575.append(1)
                                        else:
                                                seq_13_575.append(0)
                                elif floatSamples[i][1] >= 5.76 and floatSamples[i][1] < 5.77:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_576.append(1)
                                        else:
                                                seq_13_576.append(0)
                                elif floatSamples[i][1] >= 5.77 and floatSamples[i][1] < 5.78:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_577.append(1)
                                        else:
                                                seq_13_577.append(0)
                                elif floatSamples[i][1] >= 5.78 and floatSamples[i][1] < 5.79:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_578.append(1)
                                        else:
                                                seq_13_578.append(0)
                                elif floatSamples[i][1] >= 5.79 and floatSamples[i][1] < 5.8:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_579.append(1)
                                        else:
                                                seq_13_579.append(0)
                                elif floatSamples[i][1] >= 5.8 and floatSamples[i][1] < 5.81:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_580.append(1)
                                        else:
                                                seq_13_580.append(0)
                                elif floatSamples[i][1] >= 5.81 and floatSamples[i][1] < 5.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_581.append(1)
                                        else:
                                                seq_13_581.append(0)
                                elif floatSamples[i][1] >= 5.82 and floatSamples[i][1] < 5.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_582.append(1)
                                        else:
                                                seq_13_582.append(0)
                                elif floatSamples[i][1] >= 5.83 and floatSamples[i][1] < 5.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_583.append(1)
                                        else:
                                                seq_13_583.append(0)
                                elif floatSamples[i][1] >= 5.84 and floatSamples[i][1] < 5.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_584.append(1)
                                        else:
                                                seq_13_584.append(0)
                                elif floatSamples[i][1] >= 5.85 and floatSamples[i][1] < 5.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_585.append(1)
                                        else:
                                                seq_13_585.append(0)
                                elif floatSamples[i][1] >= 5.86 and floatSamples[i][1] < 5.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_586.append(1)
                                        else:
                                                seq_13_586.append(0)
                                elif floatSamples[i][1] >= 5.87 and floatSamples[i][1] < 5.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_13_587.append(1)
                                        else:
                                                seq_13_587.append(0)
                        elif floatSamples[i][0] == 14:
                                if floatSamples[i][1] >= 0.8 and floatSamples[i][1] < 0.81:
                                        if floatSamples[i][2] > -100:
                                                seq_14_08.append(1)
                                        else:
                                                seq_14_08.append(0)
                                elif floatSamples[i][1] >= 0.81 and floatSamples[i][1] < 0.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_081.append(1)
                                        else:
                                                seq_14_081.append(0)
                                elif floatSamples[i][1] >= 0.82 and floatSamples[i][1] < 0.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_082.append(1)
                                        else:
                                                seq_14_082.append(0)
                                elif floatSamples[i][1] >= 0.83 and floatSamples[i][1] < 0.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_083.append(1)
                                        else:
                                                seq_14_083.append(0)
                                elif floatSamples[i][1] >= 0.84 and floatSamples[i][1] < 0.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_084.append(1)
                                        else:
                                                seq_14_084.append(0)
                                elif floatSamples[i][1] >= 0.85 and floatSamples[i][1] < 0.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_085.append(1)
                                        else:
                                                seq_14_085.append(0)
                                elif floatSamples[i][1] >= 0.86 and floatSamples[i][1] < 0.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_086.append(1)
                                        else:
                                                seq_14_086.append(0)
                                elif floatSamples[i][1] >= 0.87 and floatSamples[i][1] < 0.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_087.append(1)
                                        else:
                                                seq_14_087.append(0)
                                elif floatSamples[i][1] >= 0.88 and floatSamples[i][1] < 0.89:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_088.append(1)
                                        else:
                                                seq_14_088.append(0)
                                elif floatSamples[i][1] >= 0.89 and floatSamples[i][1] < 0.90:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_089.append(1)
                                        else:
                                                seq_14_089.append(0)
                                elif floatSamples[i][1] >= 0.90 and floatSamples[i][1] < 0.91:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_090.append(1)
                                        else:
                                                seq_14_090.append(0)
                                elif floatSamples[i][1] >= 0.91 and floatSamples[i][1] < 0.92:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_091.append(1)
                                        else:
                                                seq_14_091.append(0)
                                elif floatSamples[i][1] >= 2.4 and floatSamples[i][1] < 2.41: 
                                        if floatSamples[i][2]  > -100:
                                                seq_14_240.append(1)
                                        else:
                                                seq_14_240.append(0)
                                elif floatSamples[i][1] >= 2.41 and floatSamples[i][1] < 2.42:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_241.append(1)
                                        else:
                                                seq_14_241.append(0)
                                elif floatSamples[i][1] >= 2.42 and floatSamples[i][1] < 2.43:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_242.append(1)
                                        else:
                                                seq_14_242.append(0)
                                elif floatSamples[i][1] >= 2.43 and floatSamples[i][1] < 2.44:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_243.append(1)
                                        else:
                                                seq_14_243.append(0)
                                elif floatSamples[i][1] >= 2.44 and floatSamples[i][1] < 2.45:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_244.append(1)
                                        else:
                                                seq_14_244.append(0)
                                elif floatSamples[i][1] >= 2.45 and floatSamples[i][1] < 2.46:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_245.append(1)
                                        else:
                                                seq_14_245.append(0)
                                elif floatSamples[i][1] >= 2.46 and floatSamples[i][1] < 2.47:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_246.append(1)
                                        else:
                                                seq_14_246.append(0)
                                elif floatSamples[i][1] >= 2.47 and floatSamples[i][1] < 2.48:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_247.append(1)
                                        else:
                                                seq_14_247.append(0)
                                elif floatSamples[i][1] >= 2.48 and floatSamples[i][1] < 2.49:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_248.append(1)
                                        else:
                                                seq_14_248.append(0)
                                elif floatSamples[i][1] >= 2.49 and floatSamples[i][1] < 2.50:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_249.append(1)
                                        else:
                                                seq_14_249.append(0)
                                elif floatSamples[i][1] >= 5.71 and floatSamples[i][1] < 5.72:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_571.append(1)
                                        else:
                                                seq_14_571.append(0)
                                elif floatSamples[i][1] >= 5.72 and floatSamples[i][1] < 5.73:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_572.append(1)
                                        else:
                                                seq_14_572.append(0)
                                elif floatSamples[i][1] >= 5.73 and floatSamples[i][1] < 5.74:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_573.append(1)
                                        else:
                                                seq_14_573.append(0)
                                elif floatSamples[i][1] >= 5.74 and floatSamples[i][1] < 5.75:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_574.append(1)
                                        else:
                                                seq_14_574.append(0)
                                elif floatSamples[i][1] >= 5.75 and floatSamples[i][1] < 5.76:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_575.append(1)
                                        else:
                                                seq_14_575.append(0)
                                elif floatSamples[i][1] >= 5.76 and floatSamples[i][1] < 5.77:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_576.append(1)
                                        else:
                                                seq_14_576.append(0)
                                elif floatSamples[i][1] >= 5.77 and floatSamples[i][1] < 5.78:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_577.append(1)
                                        else:
                                                seq_14_577.append(0)
                                elif floatSamples[i][1] >= 5.78 and floatSamples[i][1] < 5.79:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_578.append(1)
                                        else:
                                                seq_14_578.append(0)
                                elif floatSamples[i][1] >= 5.79 and floatSamples[i][1] < 5.8:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_579.append(1)
                                        else:
                                                seq_14_579.append(0)
                                elif floatSamples[i][1] >= 5.8 and floatSamples[i][1] < 5.81:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_580.append(1)
                                        else:
                                                seq_14_580.append(0)
                                elif floatSamples[i][1] >= 5.81 and floatSamples[i][1] < 5.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_581.append(1)
                                        else:
                                                seq_14_581.append(0)
                                elif floatSamples[i][1] >= 5.82 and floatSamples[i][1] < 5.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_582.append(1)
                                        else:
                                                seq_14_582.append(0)
                                elif floatSamples[i][1] >= 5.83 and floatSamples[i][1] < 5.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_583.append(1)
                                        else:
                                                seq_14_583.append(0)
                                elif floatSamples[i][1] >= 5.84 and floatSamples[i][1] < 5.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_584.append(1)
                                        else:
                                                seq_14_584.append(0)
                                elif floatSamples[i][1] >= 5.85 and floatSamples[i][1] < 5.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_585.append(1)
                                        else:
                                                seq_14_585.append(0)
                                elif floatSamples[i][1] >= 5.86 and floatSamples[i][1] < 5.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_586.append(1)
                                        else:
                                                seq_14_586.append(0)
                                elif floatSamples[i][1] >= 5.87 and floatSamples[i][1] < 5.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_14_587.append(1)
                                        else:
                                                seq_14_587.append(0)
                        elif floatSamples[i][0] == 15:
                                if floatSamples[i][1] >= 0.8 and floatSamples[i][1] < 0.81:
                                        if floatSamples[i][2] > -100:
                                                seq_15_08.append(1)
                                        else:
                                                seq_15_08.append(0)
                                elif floatSamples[i][1] >= 0.81 and floatSamples[i][1] < 0.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_081.append(1)
                                        else:
                                                seq_15_081.append(0)
                                elif floatSamples[i][1] >= 0.82 and floatSamples[i][1] < 0.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_082.append(1)
                                        else:
                                                seq_15_082.append(0)
                                elif floatSamples[i][1] >= 0.83 and floatSamples[i][1] < 0.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_083.append(1)
                                        else:
                                                seq_15_083.append(0)
                                elif floatSamples[i][1] >= 0.84 and floatSamples[i][1] < 0.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_084.append(1)
                                        else:
                                                seq_15_084.append(0)
                                elif floatSamples[i][1] >= 0.85 and floatSamples[i][1] < 0.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_085.append(1)
                                        else:
                                                seq_15_085.append(0)
                                elif floatSamples[i][1] >= 0.86 and floatSamples[i][1] < 0.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_086.append(1)
                                        else:
                                                seq_15_086.append(0)
                                elif floatSamples[i][1] >= 0.87 and floatSamples[i][1] < 0.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_087.append(1)
                                        else:
                                                seq_15_087.append(0)
                                elif floatSamples[i][1] >= 0.88 and floatSamples[i][1] < 0.89:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_088.append(1)
                                        else:
                                                seq_15_088.append(0)
                                elif floatSamples[i][1] >= 0.89 and floatSamples[i][1] < 0.90:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_089.append(1)
                                        else:
                                                seq_15_089.append(0)
                                elif floatSamples[i][1] >= 0.90 and floatSamples[i][1] < 0.91:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_090.append(1)
                                        else:
                                                seq_15_090.append(0)
                                elif floatSamples[i][1] >= 0.91 and floatSamples[i][1] < 0.92:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_091.append(1)
                                        else:
                                                seq_15_091.append(0)
                                elif floatSamples[i][1] >= 2.4 and floatSamples[i][1] < 2.41: 
                                        if floatSamples[i][2]  > -100:
                                                seq_15_240.append(1)
                                        else:
                                                seq_15_240.append(0)
                                elif floatSamples[i][1] >= 2.41 and floatSamples[i][1] < 2.42:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_241.append(1)
                                        else:
                                                seq_15_241.append(0)
                                elif floatSamples[i][1] >= 2.42 and floatSamples[i][1] < 2.43:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_242.append(1)
                                        else:
                                                seq_15_242.append(0)
                                elif floatSamples[i][1] >= 2.43 and floatSamples[i][1] < 2.44:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_243.append(1)
                                        else:
                                                seq_15_243.append(0)
                                elif floatSamples[i][1] >= 2.44 and floatSamples[i][1] < 2.45:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_244.append(1)
                                        else:
                                                seq_15_244.append(0)
                                elif floatSamples[i][1] >= 2.45 and floatSamples[i][1] < 2.46:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_245.append(1)
                                        else:
                                                seq_15_245.append(0)
                                elif floatSamples[i][1] >= 2.46 and floatSamples[i][1] < 2.47:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_246.append(1)
                                        else:
                                                seq_15_246.append(0)
                                elif floatSamples[i][1] >= 2.47 and floatSamples[i][1] < 2.48:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_247.append(1)
                                        else:
                                                seq_15_247.append(0)
                                elif floatSamples[i][1] >= 2.48 and floatSamples[i][1] < 2.49:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_248.append(1)
                                        else:
                                                seq_15_248.append(0)
                                elif floatSamples[i][1] >= 2.49 and floatSamples[i][1] < 2.50:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_249.append(1)
                                        else:
                                                seq_15_249.append(0)
                                elif floatSamples[i][1] >= 5.71 and floatSamples[i][1] < 5.72:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_571.append(1)
                                        else:
                                                seq_15_571.append(0)
                                elif floatSamples[i][1] >= 5.72 and floatSamples[i][1] < 5.73:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_572.append(1)
                                        else:
                                                seq_15_572.append(0)
                                elif floatSamples[i][1] >= 5.73 and floatSamples[i][1] < 5.74:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_573.append(1)
                                        else:
                                                seq_15_573.append(0)
                                elif floatSamples[i][1] >= 5.74 and floatSamples[i][1] < 5.75:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_574.append(1)
                                        else:
                                                seq_15_574.append(0)
                                elif floatSamples[i][1] >= 5.75 and floatSamples[i][1] < 5.76:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_575.append(1)
                                        else:
                                                seq_15_575.append(0)
                                elif floatSamples[i][1] >= 5.76 and floatSamples[i][1] < 5.77:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_576.append(1)
                                        else:
                                                seq_15_576.append(0)
                                elif floatSamples[i][1] >= 5.77 and floatSamples[i][1] < 5.78:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_577.append(1)
                                        else:
                                                seq_15_577.append(0)
                                elif floatSamples[i][1] >= 5.78 and floatSamples[i][1] < 5.79:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_578.append(1)
                                        else:
                                                seq_15_578.append(0)
                                elif floatSamples[i][1] >= 5.79 and floatSamples[i][1] < 5.8:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_579.append(1)
                                        else:
                                                seq_15_579.append(0)
                                elif floatSamples[i][1] >= 5.8 and floatSamples[i][1] < 5.81:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_580.append(1)
                                        else:
                                                seq_15_580.append(0)
                                elif floatSamples[i][1] >= 5.81 and floatSamples[i][1] < 5.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_581.append(1)
                                        else:
                                                seq_15_581.append(0)
                                elif floatSamples[i][1] >= 5.82 and floatSamples[i][1] < 5.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_582.append(1)
                                        else:
                                                seq_15_582.append(0)
                                elif floatSamples[i][1] >= 5.83 and floatSamples[i][1] < 5.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_583.append(1)
                                        else:
                                                seq_15_583.append(0)
                                elif floatSamples[i][1] >= 5.84 and floatSamples[i][1] < 5.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_584.append(1)
                                        else:
                                                seq_15_584.append(0)
                                elif floatSamples[i][1] >= 5.85 and floatSamples[i][1] < 5.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_585.append(1)
                                        else:
                                                seq_15_585.append(0)
                                elif floatSamples[i][1] >= 5.86 and floatSamples[i][1] < 5.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_586.append(1)
                                        else:
                                                seq_15_586.append(0)
                                elif floatSamples[i][1] >= 5.87 and floatSamples[i][1] < 5.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_15_587.append(1)
                                        else:
                                                seq_15_587.append(0)
                        elif floatSamples[i][0] == 16:
                                if floatSamples[i][1] >= 0.8 and floatSamples[i][1] < 0.81:
                                        if floatSamples[i][2] > -100:
                                                seq_16_08.append(1)
                                        else:
                                                seq_16_08.append(0)
                                elif floatSamples[i][1] >= 0.81 and floatSamples[i][1] < 0.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_081.append(1)
                                        else:
                                                seq_16_081.append(0)
                                elif floatSamples[i][1] >= 0.82 and floatSamples[i][1] < 0.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_082.append(1)
                                        else:
                                                seq_16_082.append(0)
                                elif floatSamples[i][1] >= 0.83 and floatSamples[i][1] < 0.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_083.append(1)
                                        else:
                                                seq_16_083.append(0)
                                elif floatSamples[i][1] >= 0.84 and floatSamples[i][1] < 0.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_084.append(1)
                                        else:
                                                seq_16_084.append(0)
                                elif floatSamples[i][1] >= 0.85 and floatSamples[i][1] < 0.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_085.append(1)
                                        else:
                                                seq_16_085.append(0)
                                elif floatSamples[i][1] >= 0.86 and floatSamples[i][1] < 0.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_086.append(1)
                                        else:
                                                seq_16_086.append(0)
                                elif floatSamples[i][1] >= 0.87 and floatSamples[i][1] < 0.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_087.append(1)
                                        else:
                                                seq_16_087.append(0)
                                elif floatSamples[i][1] >= 0.88 and floatSamples[i][1] < 0.89:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_088.append(1)
                                        else:
                                                seq_16_088.append(0)
                                elif floatSamples[i][1] >= 0.89 and floatSamples[i][1] < 0.90:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_089.append(1)
                                        else:
                                                seq_16_089.append(0)
                                elif floatSamples[i][1] >= 0.90 and floatSamples[i][1] < 0.91:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_090.append(1)
                                        else:
                                                seq_16_090.append(0)
                                elif floatSamples[i][1] >= 0.91 and floatSamples[i][1] < 0.92:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_091.append(1)
                                        else:
                                                seq_16_091.append(0)
                                elif floatSamples[i][1] >= 2.4 and floatSamples[i][1] < 2.41: 
                                        if floatSamples[i][2]  > -100:
                                                seq_16_240.append(1)
                                        else:
                                                seq_16_240.append(0)
                                elif floatSamples[i][1] >= 2.41 and floatSamples[i][1] < 2.42:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_241.append(1)
                                        else:
                                                seq_16_241.append(0)
                                elif floatSamples[i][1] >= 2.42 and floatSamples[i][1] < 2.43:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_242.append(1)
                                        else:
                                                seq_16_242.append(0)
                                elif floatSamples[i][1] >= 2.43 and floatSamples[i][1] < 2.44:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_243.append(1)
                                        else:
                                                seq_16_243.append(0)
                                elif floatSamples[i][1] >= 2.44 and floatSamples[i][1] < 2.45:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_244.append(1)
                                        else:
                                                seq_16_244.append(0)
                                elif floatSamples[i][1] >= 2.45 and floatSamples[i][1] < 2.46:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_245.append(1)
                                        else:
                                                seq_16_245.append(0)
                                elif floatSamples[i][1] >= 2.46 and floatSamples[i][1] < 2.47:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_246.append(1)
                                        else:
                                                seq_16_246.append(0)
                                elif floatSamples[i][1] >= 2.47 and floatSamples[i][1] < 2.48:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_247.append(1)
                                        else:
                                                seq_16_247.append(0)
                                elif floatSamples[i][1] >= 2.48 and floatSamples[i][1] < 2.49:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_248.append(1)
                                        else:
                                                seq_16_248.append(0)
                                elif floatSamples[i][1] >= 2.49 and floatSamples[i][1] < 2.50:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_249.append(1)
                                        else:
                                                seq_16_249.append(0)
                                elif floatSamples[i][1] >= 5.71 and floatSamples[i][1] < 5.72:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_571.append(1)
                                        else:
                                                seq_16_571.append(0)
                                elif floatSamples[i][1] >= 5.72 and floatSamples[i][1] < 5.73:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_572.append(1)
                                        else:
                                                seq_16_572.append(0)
                                elif floatSamples[i][1] >= 5.73 and floatSamples[i][1] < 5.74:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_573.append(1)
                                        else:
                                                seq_16_573.append(0)
                                elif floatSamples[i][1] >= 5.74 and floatSamples[i][1] < 5.75:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_574.append(1)
                                        else:
                                                seq_16_574.append(0)
                                elif floatSamples[i][1] >= 5.75 and floatSamples[i][1] < 5.76:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_575.append(1)
                                        else:
                                                seq_16_575.append(0)
                                elif floatSamples[i][1] >= 5.76 and floatSamples[i][1] < 5.77:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_576.append(1)
                                        else:
                                                seq_16_576.append(0)
                                elif floatSamples[i][1] >= 5.77 and floatSamples[i][1] < 5.78:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_577.append(1)
                                        else:
                                                seq_16_577.append(0)
                                elif floatSamples[i][1] >= 5.78 and floatSamples[i][1] < 5.79:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_578.append(1)
                                        else:
                                                seq_16_578.append(0)
                                elif floatSamples[i][1] >= 5.79 and floatSamples[i][1] < 5.8:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_579.append(1)
                                        else:
                                                seq_16_579.append(0)
                                elif floatSamples[i][1] >= 5.8 and floatSamples[i][1] < 5.81:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_580.append(1)
                                        else:
                                                seq_16_580.append(0)
                                elif floatSamples[i][1] >= 5.81 and floatSamples[i][1] < 5.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_581.append(1)
                                        else:
                                                seq_16_581.append(0)
                                elif floatSamples[i][1] >= 5.82 and floatSamples[i][1] < 5.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_582.append(1)
                                        else:
                                                seq_16_582.append(0)
                                elif floatSamples[i][1] >= 5.83 and floatSamples[i][1] < 5.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_583.append(1)
                                        else:
                                                seq_16_583.append(0)
                                elif floatSamples[i][1] >= 5.84 and floatSamples[i][1] < 5.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_584.append(1)
                                        else:
                                                seq_16_584.append(0)
                                elif floatSamples[i][1] >= 5.85 and floatSamples[i][1] < 5.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_585.append(1)
                                        else:
                                                seq_16_585.append(0)
                                elif floatSamples[i][1] >= 5.86 and floatSamples[i][1] < 5.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_586.append(1)
                                        else:
                                                seq_16_586.append(0)
                                elif floatSamples[i][1] >= 5.87 and floatSamples[i][1] < 5.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_16_587.append(1)
                                        else:
                                                seq_16_587.append(0)
                        elif floatSamples[i][0] == 17:
                                if floatSamples[i][1] >= 0.8 and floatSamples[i][1] < 0.81:
                                        if floatSamples[i][2] > -100:
                                                seq_17_08.append(1)
                                        else:
                                                seq_17_08.append(0)
                                elif floatSamples[i][1] >= 0.81 and floatSamples[i][1] < 0.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_081.append(1)
                                        else:
                                                seq_17_081.append(0)
                                elif floatSamples[i][1] >= 0.82 and floatSamples[i][1] < 0.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_082.append(1)
                                        else:
                                                seq_17_082.append(0)
                                elif floatSamples[i][1] >= 0.83 and floatSamples[i][1] < 0.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_083.append(1)
                                        else:
                                                seq_17_083.append(0)
                                elif floatSamples[i][1] >= 0.84 and floatSamples[i][1] < 0.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_084.append(1)
                                        else:
                                                seq_17_084.append(0)
                                elif floatSamples[i][1] >= 0.85 and floatSamples[i][1] < 0.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_085.append(1)
                                        else:
                                                seq_17_085.append(0)
                                elif floatSamples[i][1] >= 0.86 and floatSamples[i][1] < 0.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_086.append(1)
                                        else:
                                                seq_17_086.append(0)
                                elif floatSamples[i][1] >= 0.87 and floatSamples[i][1] < 0.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_087.append(1)
                                        else:
                                                seq_17_087.append(0)
                                elif floatSamples[i][1] >= 0.88 and floatSamples[i][1] < 0.89:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_088.append(1)
                                        else:
                                                seq_17_088.append(0)
                                elif floatSamples[i][1] >= 0.89 and floatSamples[i][1] < 0.90:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_089.append(1)
                                        else:
                                                seq_17_089.append(0)
                                elif floatSamples[i][1] >= 0.90 and floatSamples[i][1] < 0.91:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_090.append(1)
                                        else:
                                                seq_17_090.append(0)
                                elif floatSamples[i][1] >= 0.91 and floatSamples[i][1] < 0.92:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_091.append(1)
                                        else:
                                                seq_17_091.append(0)
                                elif floatSamples[i][1] >= 2.4 and floatSamples[i][1] < 2.41: 
                                        if floatSamples[i][2]  > -100:
                                                seq_17_240.append(1)
                                        else:
                                                seq_17_240.append(0)
                                elif floatSamples[i][1] >= 2.41 and floatSamples[i][1] < 2.42:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_241.append(1)
                                        else:
                                                seq_17_241.append(0)
                                elif floatSamples[i][1] >= 2.42 and floatSamples[i][1] < 2.43:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_242.append(1)
                                        else:
                                                seq_17_242.append(0)
                                elif floatSamples[i][1] >= 2.43 and floatSamples[i][1] < 2.44:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_243.append(1)
                                        else:
                                                seq_17_243.append(0)
                                elif floatSamples[i][1] >= 2.44 and floatSamples[i][1] < 2.45:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_244.append(1)
                                        else:
                                                seq_17_244.append(0)
                                elif floatSamples[i][1] >= 2.45 and floatSamples[i][1] < 2.46:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_245.append(1)
                                        else:
                                                seq_17_245.append(0)
                                elif floatSamples[i][1] >= 2.46 and floatSamples[i][1] < 2.47:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_246.append(1)
                                        else:
                                                seq_17_246.append(0)
                                elif floatSamples[i][1] >= 2.47 and floatSamples[i][1] < 2.48:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_247.append(1)
                                        else:
                                                seq_17_247.append(0)
                                elif floatSamples[i][1] >= 2.48 and floatSamples[i][1] < 2.49:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_248.append(1)
                                        else:
                                                seq_17_248.append(0)
                                elif floatSamples[i][1] >= 2.49 and floatSamples[i][1] < 2.50:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_249.append(1)
                                        else:
                                                seq_17_249.append(0)
                                elif floatSamples[i][1] >= 5.71 and floatSamples[i][1] < 5.72:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_571.append(1)
                                        else:
                                                seq_17_571.append(0)
                                elif floatSamples[i][1] >= 5.72 and floatSamples[i][1] < 5.73:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_572.append(1)
                                        else:
                                                seq_17_572.append(0)
                                elif floatSamples[i][1] >= 5.73 and floatSamples[i][1] < 5.74:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_573.append(1)
                                        else:
                                                seq_17_573.append(0)
                                elif floatSamples[i][1] >= 5.74 and floatSamples[i][1] < 5.75:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_574.append(1)
                                        else:
                                                seq_17_574.append(0)
                                elif floatSamples[i][1] >= 5.75 and floatSamples[i][1] < 5.76:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_575.append(1)
                                        else:
                                                seq_17_575.append(0)
                                elif floatSamples[i][1] >= 5.76 and floatSamples[i][1] < 5.77:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_576.append(1)
                                        else:
                                                seq_17_576.append(0)
                                elif floatSamples[i][1] >= 5.77 and floatSamples[i][1] < 5.78:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_577.append(1)
                                        else:
                                                seq_17_577.append(0)
                                elif floatSamples[i][1] >= 5.78 and floatSamples[i][1] < 5.79:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_578.append(1)
                                        else:
                                                seq_17_578.append(0)
                                elif floatSamples[i][1] >= 5.79 and floatSamples[i][1] < 5.8:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_579.append(1)
                                        else:
                                                seq_17_579.append(0)
                                elif floatSamples[i][1] >= 5.8 and floatSamples[i][1] < 5.81:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_580.append(1)
                                        else:
                                                seq_17_580.append(0)
                                elif floatSamples[i][1] >= 5.81 and floatSamples[i][1] < 5.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_581.append(1)
                                        else:
                                                seq_17_581.append(0)
                                elif floatSamples[i][1] >= 5.82 and floatSamples[i][1] < 5.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_582.append(1)
                                        else:
                                                seq_17_582.append(0)
                                elif floatSamples[i][1] >= 5.83 and floatSamples[i][1] < 5.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_583.append(1)
                                        else:
                                                seq_17_583.append(0)
                                elif floatSamples[i][1] >= 5.84 and floatSamples[i][1] < 5.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_584.append(1)
                                        else:
                                                seq_17_584.append(0)
                                elif floatSamples[i][1] >= 5.85 and floatSamples[i][1] < 5.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_585.append(1)
                                        else:
                                                seq_17_585.append(0)
                                elif floatSamples[i][1] >= 5.86 and floatSamples[i][1] < 5.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_586.append(1)
                                        else:
                                                seq_17_586.append(0)
                                elif floatSamples[i][1] >= 5.87 and floatSamples[i][1] < 5.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_17_587.append(1)
                                        else:
                                                seq_17_587.append(0)
                        elif floatSamples[i][0] == 18:
                                if floatSamples[i][1] >= 0.8 and floatSamples[i][1] < 0.81:
                                        if floatSamples[i][2] > -100:
                                                seq_18_08.append(1)
                                        else:
                                                seq_18_08.append(0)
                                elif floatSamples[i][1] >= 0.81 and floatSamples[i][1] < 0.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_081.append(1)
                                        else:
                                                seq_18_081.append(0)
                                elif floatSamples[i][1] >= 0.82 and floatSamples[i][1] < 0.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_082.append(1)
                                        else:
                                                seq_18_082.append(0)
                                elif floatSamples[i][1] >= 0.83 and floatSamples[i][1] < 0.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_083.append(1)
                                        else:
                                                seq_18_083.append(0)
                                elif floatSamples[i][1] >= 0.84 and floatSamples[i][1] < 0.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_084.append(1)
                                        else:
                                                seq_18_084.append(0)
                                elif floatSamples[i][1] >= 0.85 and floatSamples[i][1] < 0.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_085.append(1)
                                        else:
                                                seq_18_085.append(0)
                                elif floatSamples[i][1] >= 0.86 and floatSamples[i][1] < 0.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_086.append(1)
                                        else:
                                                seq_18_086.append(0)
                                elif floatSamples[i][1] >= 0.87 and floatSamples[i][1] < 0.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_087.append(1)
                                        else:
                                                seq_18_087.append(0)
                                elif floatSamples[i][1] >= 0.88 and floatSamples[i][1] < 0.89:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_088.append(1)
                                        else:
                                                seq_18_088.append(0)
                                elif floatSamples[i][1] >= 0.89 and floatSamples[i][1] < 0.90:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_089.append(1)
                                        else:
                                                seq_18_089.append(0)
                                elif floatSamples[i][1] >= 0.90 and floatSamples[i][1] < 0.91:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_090.append(1)
                                        else:
                                                seq_18_090.append(0)
                                elif floatSamples[i][1] >= 0.91 and floatSamples[i][1] < 0.92:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_091.append(1)
                                        else:
                                                seq_18_091.append(0)
                                elif floatSamples[i][1] >= 2.4 and floatSamples[i][1] < 2.41: 
                                        if floatSamples[i][2]  > -100:
                                                seq_18_240.append(1)
                                        else:
                                                seq_18_240.append(0)
                                elif floatSamples[i][1] >= 2.41 and floatSamples[i][1] < 2.42:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_241.append(1)
                                        else:
                                                seq_18_241.append(0)
                                elif floatSamples[i][1] >= 2.42 and floatSamples[i][1] < 2.43:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_242.append(1)
                                        else:
                                                seq_18_242.append(0)
                                elif floatSamples[i][1] >= 2.43 and floatSamples[i][1] < 2.44:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_243.append(1)
                                        else:
                                                seq_18_243.append(0)
                                elif floatSamples[i][1] >= 2.44 and floatSamples[i][1] < 2.45:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_244.append(1)
                                        else:
                                                seq_18_244.append(0)
                                elif floatSamples[i][1] >= 2.45 and floatSamples[i][1] < 2.46:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_245.append(1)
                                        else:
                                                seq_18_245.append(0)
                                elif floatSamples[i][1] >= 2.46 and floatSamples[i][1] < 2.47:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_246.append(1)
                                        else:
                                                seq_18_246.append(0)
                                elif floatSamples[i][1] >= 2.47 and floatSamples[i][1] < 2.48:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_247.append(1)
                                        else:
                                                seq_18_247.append(0)
                                elif floatSamples[i][1] >= 2.48 and floatSamples[i][1] < 2.49:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_248.append(1)
                                        else:
                                                seq_18_248.append(0)
                                elif floatSamples[i][1] >= 2.49 and floatSamples[i][1] < 2.50:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_249.append(1)
                                        else:
                                                seq_18_249.append(0)
                                elif floatSamples[i][1] >= 5.71 and floatSamples[i][1] < 5.72:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_571.append(1)
                                        else:
                                                seq_18_571.append(0)
                                elif floatSamples[i][1] >= 5.72 and floatSamples[i][1] < 5.73:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_572.append(1)
                                        else:
                                                seq_18_572.append(0)
                                elif floatSamples[i][1] >= 5.73 and floatSamples[i][1] < 5.74:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_573.append(1)
                                        else:
                                                seq_18_573.append(0)
                                elif floatSamples[i][1] >= 5.74 and floatSamples[i][1] < 5.75:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_574.append(1)
                                        else:
                                                seq_18_574.append(0)
                                elif floatSamples[i][1] >= 5.75 and floatSamples[i][1] < 5.76:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_575.append(1)
                                        else:
                                                seq_18_575.append(0)
                                elif floatSamples[i][1] >= 5.76 and floatSamples[i][1] < 5.77:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_576.append(1)
                                        else:
                                                seq_18_576.append(0)
                                elif floatSamples[i][1] >= 5.77 and floatSamples[i][1] < 5.78:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_577.append(1)
                                        else:
                                                seq_18_577.append(0)
                                elif floatSamples[i][1] >= 5.78 and floatSamples[i][1] < 5.79:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_578.append(1)
                                        else:
                                                seq_18_578.append(0)
                                elif floatSamples[i][1] >= 5.79 and floatSamples[i][1] < 5.8:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_579.append(1)
                                        else:
                                                seq_18_579.append(0)
                                elif floatSamples[i][1] >= 5.8 and floatSamples[i][1] < 5.81:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_580.append(1)
                                        else:
                                                seq_18_580.append(0)
                                elif floatSamples[i][1] >= 5.81 and floatSamples[i][1] < 5.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_581.append(1)
                                        else:
                                                seq_18_581.append(0)
                                elif floatSamples[i][1] >= 5.82 and floatSamples[i][1] < 5.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_582.append(1)
                                        else:
                                                seq_18_582.append(0)
                                elif floatSamples[i][1] >= 5.83 and floatSamples[i][1] < 5.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_583.append(1)
                                        else:
                                                seq_18_583.append(0)
                                elif floatSamples[i][1] >= 5.84 and floatSamples[i][1] < 5.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_584.append(1)
                                        else:
                                                seq_18_584.append(0)
                                elif floatSamples[i][1] >= 5.85 and floatSamples[i][1] < 5.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_585.append(1)
                                        else:
                                                seq_18_585.append(0)
                                elif floatSamples[i][1] >= 5.86 and floatSamples[i][1] < 5.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_586.append(1)
                                        else:
                                                seq_18_586.append(0)
                                elif floatSamples[i][1] >= 5.87 and floatSamples[i][1] < 5.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_18_587.append(1)
                                        else:
                                                seq_18_587.append(0)
                        elif floatSamples[i][0] == 19:
                                if floatSamples[i][1] >= 0.8 and floatSamples[i][1] < 0.81:
                                        if floatSamples[i][2] > -100:
                                                seq_19_08.append(1)
                                        else:
                                                seq_19_08.append(0)
                                elif floatSamples[i][1] >= 0.81 and floatSamples[i][1] < 0.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_081.append(1)
                                        else:
                                                seq_19_081.append(0)
                                elif floatSamples[i][1] >= 0.82 and floatSamples[i][1] < 0.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_082.append(1)
                                        else:
                                                seq_19_082.append(0)
                                elif floatSamples[i][1] >= 0.83 and floatSamples[i][1] < 0.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_083.append(1)
                                        else:
                                                seq_19_083.append(0)
                                elif floatSamples[i][1] >= 0.84 and floatSamples[i][1] < 0.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_084.append(1)
                                        else:
                                                seq_19_084.append(0)
                                elif floatSamples[i][1] >= 0.85 and floatSamples[i][1] < 0.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_085.append(1)
                                        else:
                                                seq_19_085.append(0)
                                elif floatSamples[i][1] >= 0.86 and floatSamples[i][1] < 0.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_086.append(1)
                                        else:
                                                seq_19_086.append(0)
                                elif floatSamples[i][1] >= 0.87 and floatSamples[i][1] < 0.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_087.append(1)
                                        else:
                                                seq_19_087.append(0)
                                elif floatSamples[i][1] >= 0.88 and floatSamples[i][1] < 0.89:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_088.append(1)
                                        else:
                                                seq_19_088.append(0)
                                elif floatSamples[i][1] >= 0.89 and floatSamples[i][1] < 0.90:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_089.append(1)
                                        else:
                                                seq_19_089.append(0)
                                elif floatSamples[i][1] >= 0.90 and floatSamples[i][1] < 0.91:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_090.append(1)
                                        else:
                                                seq_19_090.append(0)
                                elif floatSamples[i][1] >= 0.91 and floatSamples[i][1] < 0.92:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_091.append(1)
                                        else:
                                                seq_19_091.append(0)
                                elif floatSamples[i][1] >= 2.4 and floatSamples[i][1] < 2.41: 
                                        if floatSamples[i][2]  > -100:
                                                seq_19_240.append(1)
                                        else:
                                                seq_19_240.append(0)
                                elif floatSamples[i][1] >= 2.41 and floatSamples[i][1] < 2.42:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_241.append(1)
                                        else:
                                                seq_19_241.append(0)
                                elif floatSamples[i][1] >= 2.42 and floatSamples[i][1] < 2.43:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_242.append(1)
                                        else:
                                                seq_19_242.append(0)
                                elif floatSamples[i][1] >= 2.43 and floatSamples[i][1] < 2.44:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_243.append(1)
                                        else:
                                                seq_19_243.append(0)
                                elif floatSamples[i][1] >= 2.44 and floatSamples[i][1] < 2.45:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_244.append(1)
                                        else:
                                                seq_19_244.append(0)
                                elif floatSamples[i][1] >= 2.45 and floatSamples[i][1] < 2.46:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_245.append(1)
                                        else:
                                                seq_19_245.append(0)
                                elif floatSamples[i][1] >= 2.46 and floatSamples[i][1] < 2.47:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_246.append(1)
                                        else:
                                                seq_19_246.append(0)
                                elif floatSamples[i][1] >= 2.47 and floatSamples[i][1] < 2.48:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_247.append(1)
                                        else:
                                                seq_19_247.append(0)
                                elif floatSamples[i][1] >= 2.48 and floatSamples[i][1] < 2.49:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_248.append(1)
                                        else:
                                                seq_19_248.append(0)
                                elif floatSamples[i][1] >= 2.49 and floatSamples[i][1] < 2.50:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_249.append(1)
                                        else:
                                                seq_19_249.append(0)
                                elif floatSamples[i][1] >= 5.71 and floatSamples[i][1] < 5.72:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_571.append(1)
                                        else:
                                                seq_19_571.append(0)
                                elif floatSamples[i][1] >= 5.72 and floatSamples[i][1] < 5.73:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_572.append(1)
                                        else:
                                                seq_19_572.append(0)
                                elif floatSamples[i][1] >= 5.73 and floatSamples[i][1] < 5.74:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_573.append(1)
                                        else:
                                                seq_19_573.append(0)
                                elif floatSamples[i][1] >= 5.74 and floatSamples[i][1] < 5.75:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_574.append(1)
                                        else:
                                                seq_19_574.append(0)
                                elif floatSamples[i][1] >= 5.75 and floatSamples[i][1] < 5.76:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_575.append(1)
                                        else:
                                                seq_19_575.append(0)
                                elif floatSamples[i][1] >= 5.76 and floatSamples[i][1] < 5.77:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_576.append(1)
                                        else:
                                                seq_19_576.append(0)
                                elif floatSamples[i][1] >= 5.77 and floatSamples[i][1] < 5.78:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_577.append(1)
                                        else:
                                                seq_19_577.append(0)
                                elif floatSamples[i][1] >= 5.78 and floatSamples[i][1] < 5.79:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_578.append(1)
                                        else:
                                                seq_19_578.append(0)
                                elif floatSamples[i][1] >= 5.79 and floatSamples[i][1] < 5.8:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_579.append(1)
                                        else:
                                                seq_19_579.append(0)
                                elif floatSamples[i][1] >= 5.8 and floatSamples[i][1] < 5.81:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_580.append(1)
                                        else:
                                                seq_19_580.append(0)
                                elif floatSamples[i][1] >= 5.81 and floatSamples[i][1] < 5.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_581.append(1)
                                        else:
                                                seq_19_581.append(0)
                                elif floatSamples[i][1] >= 5.82 and floatSamples[i][1] < 5.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_582.append(1)
                                        else:
                                                seq_19_582.append(0)
                                elif floatSamples[i][1] >= 5.83 and floatSamples[i][1] < 5.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_583.append(1)
                                        else:
                                                seq_19_583.append(0)
                                elif floatSamples[i][1] >= 5.84 and floatSamples[i][1] < 5.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_584.append(1)
                                        else:
                                                seq_19_584.append(0)
                                elif floatSamples[i][1] >= 5.85 and floatSamples[i][1] < 5.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_585.append(1)
                                        else:
                                                seq_19_585.append(0)
                                elif floatSamples[i][1] >= 5.86 and floatSamples[i][1] < 5.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_586.append(1)
                                        else:
                                                seq_19_586.append(0)
                                elif floatSamples[i][1] >= 5.87 and floatSamples[i][1] < 5.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_19_587.append(1)
                                        else:
                                                seq_19_587.append(0)
                        elif floatSamples[i][0] == 20:
                                if floatSamples[i][1] >= 0.8 and floatSamples[i][1] < 0.81:
                                        if floatSamples[i][2] > -100:
                                                seq_20_08.append(1)
                                        else:
                                                seq_20_08.append(0)
                                elif floatSamples[i][1] >= 0.81 and floatSamples[i][1] < 0.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_081.append(1)
                                        else:
                                                seq_20_081.append(0)
                                elif floatSamples[i][1] >= 0.82 and floatSamples[i][1] < 0.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_082.append(1)
                                        else:
                                                seq_20_082.append(0)
                                elif floatSamples[i][1] >= 0.83 and floatSamples[i][1] < 0.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_083.append(1)
                                        else:
                                                seq_20_083.append(0)
                                elif floatSamples[i][1] >= 0.84 and floatSamples[i][1] < 0.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_084.append(1)
                                        else:
                                                seq_20_084.append(0)
                                elif floatSamples[i][1] >= 0.85 and floatSamples[i][1] < 0.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_085.append(1)
                                        else:
                                                seq_20_085.append(0)
                                elif floatSamples[i][1] >= 0.86 and floatSamples[i][1] < 0.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_086.append(1)
                                        else:
                                                seq_20_086.append(0)
                                elif floatSamples[i][1] >= 0.87 and floatSamples[i][1] < 0.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_087.append(1)
                                        else:
                                                seq_20_087.append(0)
                                elif floatSamples[i][1] >= 0.88 and floatSamples[i][1] < 0.89:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_088.append(1)
                                        else:
                                                seq_20_088.append(0)
                                elif floatSamples[i][1] >= 0.89 and floatSamples[i][1] < 0.90:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_089.append(1)
                                        else:
                                                seq_20_089.append(0)
                                elif floatSamples[i][1] >= 0.90 and floatSamples[i][1] < 0.91:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_090.append(1)
                                        else:
                                                seq_20_090.append(0)
                                elif floatSamples[i][1] >= 0.91 and floatSamples[i][1] < 0.92:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_091.append(1)
                                        else:
                                                seq_20_091.append(0)
                                elif floatSamples[i][1] >= 2.4 and floatSamples[i][1] < 2.41: 
                                        if floatSamples[i][2]  > -100:
                                                seq_20_240.append(1)
                                        else:
                                                seq_20_240.append(0)
                                elif floatSamples[i][1] >= 2.41 and floatSamples[i][1] < 2.42:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_241.append(1)
                                        else:
                                                seq_20_241.append(0)
                                elif floatSamples[i][1] >= 2.42 and floatSamples[i][1] < 2.43:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_242.append(1)
                                        else:
                                                seq_20_242.append(0)
                                elif floatSamples[i][1] >= 2.43 and floatSamples[i][1] < 2.44:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_243.append(1)
                                        else:
                                                seq_20_243.append(0)
                                elif floatSamples[i][1] >= 2.44 and floatSamples[i][1] < 2.45:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_244.append(1)
                                        else:
                                                seq_20_244.append(0)
                                elif floatSamples[i][1] >= 2.45 and floatSamples[i][1] < 2.46:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_245.append(1)
                                        else:
                                                seq_20_245.append(0)
                                elif floatSamples[i][1] >= 2.46 and floatSamples[i][1] < 2.47:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_246.append(1)
                                        else:
                                                seq_20_246.append(0)
                                elif floatSamples[i][1] >= 2.47 and floatSamples[i][1] < 2.48:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_247.append(1)
                                        else:
                                                seq_20_247.append(0)
                                elif floatSamples[i][1] >= 2.48 and floatSamples[i][1] < 2.49:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_248.append(1)
                                        else:
                                                seq_20_248.append(0)
                                elif floatSamples[i][1] >= 2.49 and floatSamples[i][1] < 2.50:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_249.append(1)
                                        else:
                                                seq_20_249.append(0)
                                elif floatSamples[i][1] >= 5.71 and floatSamples[i][1] < 5.72:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_571.append(1)
                                        else:
                                                seq_20_571.append(0)
                                elif floatSamples[i][1] >= 5.72 and floatSamples[i][1] < 5.73:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_572.append(1)
                                        else:
                                                seq_20_572.append(0)
                                elif floatSamples[i][1] >= 5.73 and floatSamples[i][1] < 5.74:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_573.append(1)
                                        else:
                                                seq_20_573.append(0)
                                elif floatSamples[i][1] >= 5.74 and floatSamples[i][1] < 5.75:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_574.append(1)
                                        else:
                                                seq_20_574.append(0)
                                elif floatSamples[i][1] >= 5.75 and floatSamples[i][1] < 5.76:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_575.append(1)
                                        else:
                                                seq_20_575.append(0)
                                elif floatSamples[i][1] >= 5.76 and floatSamples[i][1] < 5.77:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_576.append(1)
                                        else:
                                                seq_20_576.append(0)
                                elif floatSamples[i][1] >= 5.77 and floatSamples[i][1] < 5.78:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_577.append(1)
                                        else:
                                                seq_20_577.append(0)
                                elif floatSamples[i][1] >= 5.78 and floatSamples[i][1] < 5.79:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_578.append(1)
                                        else:
                                                seq_20_578.append(0)
                                elif floatSamples[i][1] >= 5.79 and floatSamples[i][1] < 5.8:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_579.append(1)
                                        else:
                                                seq_20_579.append(0)
                                elif floatSamples[i][1] >= 5.8 and floatSamples[i][1] < 5.81:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_580.append(1)
                                        else:
                                                seq_20_580.append(0)
                                elif floatSamples[i][1] >= 5.81 and floatSamples[i][1] < 5.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_581.append(1)
                                        else:
                                                seq_20_581.append(0)
                                elif floatSamples[i][1] >= 5.82 and floatSamples[i][1] < 5.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_582.append(1)
                                        else:
                                                seq_20_582.append(0)
                                elif floatSamples[i][1] >= 5.83 and floatSamples[i][1] < 5.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_583.append(1)
                                        else:
                                                seq_20_583.append(0)
                                elif floatSamples[i][1] >= 5.84 and floatSamples[i][1] < 5.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_584.append(1)
                                        else:
                                                seq_20_584.append(0)
                                elif floatSamples[i][1] >= 5.85 and floatSamples[i][1] < 5.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_585.append(1)
                                        else:
                                                seq_20_585.append(0)
                                elif floatSamples[i][1] >= 5.86 and floatSamples[i][1] < 5.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_586.append(1)
                                        else:
                                                seq_20_586.append(0)
                                elif floatSamples[i][1] >= 5.87 and floatSamples[i][1] < 5.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_20_587.append(1)
                                        else:
                                                seq_20_587.append(0)
                        elif floatSamples[i][0] == 21:
                                if floatSamples[i][1] >= 0.8 and floatSamples[i][1] < 0.81:
                                        if floatSamples[i][2] > -100:
                                                seq_21_08.append(1)
                                        else:
                                                seq_21_08.append(0)
                                elif floatSamples[i][1] >= 0.81 and floatSamples[i][1] < 0.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_081.append(1)
                                        else:
                                                seq_21_081.append(0)
                                elif floatSamples[i][1] >= 0.82 and floatSamples[i][1] < 0.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_082.append(1)
                                        else:
                                                seq_21_082.append(0)
                                elif floatSamples[i][1] >= 0.83 and floatSamples[i][1] < 0.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_083.append(1)
                                        else:
                                                seq_21_083.append(0)
                                elif floatSamples[i][1] >= 0.84 and floatSamples[i][1] < 0.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_084.append(1)
                                        else:
                                                seq_21_084.append(0)
                                elif floatSamples[i][1] >= 0.85 and floatSamples[i][1] < 0.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_085.append(1)
                                        else:
                                                seq_21_085.append(0)
                                elif floatSamples[i][1] >= 0.86 and floatSamples[i][1] < 0.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_086.append(1)
                                        else:
                                                seq_21_086.append(0)
                                elif floatSamples[i][1] >= 0.87 and floatSamples[i][1] < 0.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_087.append(1)
                                        else:
                                                seq_21_087.append(0)
                                elif floatSamples[i][1] >= 0.88 and floatSamples[i][1] < 0.89:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_088.append(1)
                                        else:
                                                seq_21_088.append(0)
                                elif floatSamples[i][1] >= 0.89 and floatSamples[i][1] < 0.90:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_089.append(1)
                                        else:
                                                seq_21_089.append(0)
                                elif floatSamples[i][1] >= 0.90 and floatSamples[i][1] < 0.91:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_090.append(1)
                                        else:
                                                seq_21_090.append(0)
                                elif floatSamples[i][1] >= 0.91 and floatSamples[i][1] < 0.92:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_091.append(1)
                                        else:
                                                seq_21_091.append(0)
                                elif floatSamples[i][1] >= 2.4 and floatSamples[i][1] < 2.41: 
                                        if floatSamples[i][2]  > -100:
                                                seq_21_240.append(1)
                                        else:
                                                seq_21_240.append(0)
                                elif floatSamples[i][1] >= 2.41 and floatSamples[i][1] < 2.42:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_241.append(1)
                                        else:
                                                seq_21_241.append(0)
                                elif floatSamples[i][1] >= 2.42 and floatSamples[i][1] < 2.43:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_242.append(1)
                                        else:
                                                seq_21_242.append(0)
                                elif floatSamples[i][1] >= 2.43 and floatSamples[i][1] < 2.44:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_243.append(1)
                                        else:
                                                seq_21_243.append(0)
                                elif floatSamples[i][1] >= 2.44 and floatSamples[i][1] < 2.45:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_244.append(1)
                                        else:
                                                seq_21_244.append(0)
                                elif floatSamples[i][1] >= 2.45 and floatSamples[i][1] < 2.46:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_245.append(1)
                                        else:
                                                seq_21_245.append(0)
                                elif floatSamples[i][1] >= 2.46 and floatSamples[i][1] < 2.47:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_246.append(1)
                                        else:
                                                seq_21_246.append(0)
                                elif floatSamples[i][1] >= 2.47 and floatSamples[i][1] < 2.48:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_247.append(1)
                                        else:
                                                seq_21_247.append(0)
                                elif floatSamples[i][1] >= 2.48 and floatSamples[i][1] < 2.49:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_248.append(1)
                                        else:
                                                seq_21_248.append(0)
                                elif floatSamples[i][1] >= 2.49 and floatSamples[i][1] < 2.50:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_249.append(1)
                                        else:
                                                seq_21_249.append(0)
                                elif floatSamples[i][1] >= 5.71 and floatSamples[i][1] < 5.72:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_571.append(1)
                                        else:
                                                seq_21_571.append(0)
                                elif floatSamples[i][1] >= 5.72 and floatSamples[i][1] < 5.73:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_572.append(1)
                                        else:
                                                seq_21_572.append(0)
                                elif floatSamples[i][1] >= 5.73 and floatSamples[i][1] < 5.74:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_573.append(1)
                                        else:
                                                seq_21_573.append(0)
                                elif floatSamples[i][1] >= 5.74 and floatSamples[i][1] < 5.75:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_574.append(1)
                                        else:
                                                seq_21_574.append(0)
                                elif floatSamples[i][1] >= 5.75 and floatSamples[i][1] < 5.76:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_575.append(1)
                                        else:
                                                seq_21_575.append(0)
                                elif floatSamples[i][1] >= 5.76 and floatSamples[i][1] < 5.77:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_576.append(1)
                                        else:
                                                seq_21_576.append(0)
                                elif floatSamples[i][1] >= 5.77 and floatSamples[i][1] < 5.78:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_577.append(1)
                                        else:
                                                seq_21_577.append(0)
                                elif floatSamples[i][1] >= 5.78 and floatSamples[i][1] < 5.79:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_578.append(1)
                                        else:
                                                seq_21_578.append(0)
                                elif floatSamples[i][1] >= 5.79 and floatSamples[i][1] < 5.8:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_579.append(1)
                                        else:
                                                seq_21_579.append(0)
                                elif floatSamples[i][1] >= 5.8 and floatSamples[i][1] < 5.81:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_580.append(1)
                                        else:
                                                seq_21_580.append(0)
                                elif floatSamples[i][1] >= 5.81 and floatSamples[i][1] < 5.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_581.append(1)
                                        else:
                                                seq_21_581.append(0)
                                elif floatSamples[i][1] >= 5.82 and floatSamples[i][1] < 5.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_582.append(1)
                                        else:
                                                seq_21_582.append(0)
                                elif floatSamples[i][1] >= 5.83 and floatSamples[i][1] < 5.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_583.append(1)
                                        else:
                                                seq_21_583.append(0)
                                elif floatSamples[i][1] >= 5.84 and floatSamples[i][1] < 5.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_584.append(1)
                                        else:
                                                seq_21_584.append(0)
                                elif floatSamples[i][1] >= 5.85 and floatSamples[i][1] < 5.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_585.append(1)
                                        else:
                                                seq_21_585.append(0)
                                elif floatSamples[i][1] >= 5.86 and floatSamples[i][1] < 5.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_586.append(1)
                                        else:
                                                seq_21_586.append(0)
                                elif floatSamples[i][1] >= 5.87 and floatSamples[i][1] < 5.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_21_587.append(1)
                                        else:
                                                seq_21_587.append(0)
                        elif floatSamples[i][0] == 22:
                                if floatSamples[i][1] >= 0.8 and floatSamples[i][1] < 0.81:
                                        if floatSamples[i][2] > -100:
                                                seq_22_08.append(1)
                                        else:
                                                seq_22_08.append(0)
                                elif floatSamples[i][1] >= 0.81 and floatSamples[i][1] < 0.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_081.append(1)
                                        else:
                                                seq_22_081.append(0)
                                elif floatSamples[i][1] >= 0.82 and floatSamples[i][1] < 0.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_082.append(1)
                                        else:
                                                seq_22_082.append(0)
                                elif floatSamples[i][1] >= 0.83 and floatSamples[i][1] < 0.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_083.append(1)
                                        else:
                                                seq_22_083.append(0)
                                elif floatSamples[i][1] >= 0.84 and floatSamples[i][1] < 0.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_084.append(1)
                                        else:
                                                seq_22_084.append(0)
                                elif floatSamples[i][1] >= 0.85 and floatSamples[i][1] < 0.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_085.append(1)
                                        else:
                                                seq_22_085.append(0)
                                elif floatSamples[i][1] >= 0.86 and floatSamples[i][1] < 0.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_086.append(1)
                                        else:
                                                seq_22_086.append(0)
                                elif floatSamples[i][1] >= 0.87 and floatSamples[i][1] < 0.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_087.append(1)
                                        else:
                                                seq_22_087.append(0)
                                elif floatSamples[i][1] >= 0.88 and floatSamples[i][1] < 0.89:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_088.append(1)
                                        else:
                                                seq_22_088.append(0)
                                elif floatSamples[i][1] >= 0.89 and floatSamples[i][1] < 0.90:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_089.append(1)
                                        else:
                                                seq_22_089.append(0)
                                elif floatSamples[i][1] >= 0.90 and floatSamples[i][1] < 0.91:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_090.append(1)
                                        else:
                                                seq_22_090.append(0)
                                elif floatSamples[i][1] >= 0.91 and floatSamples[i][1] < 0.92:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_091.append(1)
                                        else:
                                                seq_22_091.append(0)
                                elif floatSamples[i][1] >= 2.4 and floatSamples[i][1] < 2.41: 
                                        if floatSamples[i][2]  > -100:
                                                seq_22_240.append(1)
                                        else:
                                                seq_22_240.append(0)
                                elif floatSamples[i][1] >= 2.41 and floatSamples[i][1] < 2.42:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_241.append(1)
                                        else:
                                                seq_22_241.append(0)
                                elif floatSamples[i][1] >= 2.42 and floatSamples[i][1] < 2.43:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_242.append(1)
                                        else:
                                                seq_22_242.append(0)
                                elif floatSamples[i][1] >= 2.43 and floatSamples[i][1] < 2.44:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_243.append(1)
                                        else:
                                                seq_22_243.append(0)
                                elif floatSamples[i][1] >= 2.44 and floatSamples[i][1] < 2.45:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_244.append(1)
                                        else:
                                                seq_22_244.append(0)
                                elif floatSamples[i][1] >= 2.45 and floatSamples[i][1] < 2.46:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_245.append(1)
                                        else:
                                                seq_22_245.append(0)
                                elif floatSamples[i][1] >= 2.46 and floatSamples[i][1] < 2.47:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_246.append(1)
                                        else:
                                                seq_22_246.append(0)
                                elif floatSamples[i][1] >= 2.47 and floatSamples[i][1] < 2.48:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_247.append(1)
                                        else:
                                                seq_22_247.append(0)
                                elif floatSamples[i][1] >= 2.48 and floatSamples[i][1] < 2.49:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_248.append(1)
                                        else:
                                                seq_22_248.append(0)
                                elif floatSamples[i][1] >= 2.49 and floatSamples[i][1] < 2.50:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_249.append(1)
                                        else:
                                                seq_22_249.append(0)
                                elif floatSamples[i][1] >= 5.71 and floatSamples[i][1] < 5.72:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_571.append(1)
                                        else:
                                                seq_22_571.append(0)
                                elif floatSamples[i][1] >= 5.72 and floatSamples[i][1] < 5.73:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_572.append(1)
                                        else:
                                                seq_22_572.append(0)
                                elif floatSamples[i][1] >= 5.73 and floatSamples[i][1] < 5.74:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_573.append(1)
                                        else:
                                                seq_22_573.append(0)
                                elif floatSamples[i][1] >= 5.74 and floatSamples[i][1] < 5.75:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_574.append(1)
                                        else:
                                                seq_22_574.append(0)
                                elif floatSamples[i][1] >= 5.75 and floatSamples[i][1] < 5.76:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_575.append(1)
                                        else:
                                                seq_22_575.append(0)
                                elif floatSamples[i][1] >= 5.76 and floatSamples[i][1] < 5.77:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_576.append(1)
                                        else:
                                                seq_22_576.append(0)
                                elif floatSamples[i][1] >= 5.77 and floatSamples[i][1] < 5.78:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_577.append(1)
                                        else:
                                                seq_22_577.append(0)
                                elif floatSamples[i][1] >= 5.78 and floatSamples[i][1] < 5.79:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_578.append(1)
                                        else:
                                                seq_22_578.append(0)
                                elif floatSamples[i][1] >= 5.79 and floatSamples[i][1] < 5.8:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_579.append(1)
                                        else:
                                                seq_22_579.append(0)
                                elif floatSamples[i][1] >= 5.8 and floatSamples[i][1] < 5.81:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_580.append(1)
                                        else:
                                                seq_22_580.append(0)
                                elif floatSamples[i][1] >= 5.81 and floatSamples[i][1] < 5.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_581.append(1)
                                        else:
                                                seq_22_581.append(0)
                                elif floatSamples[i][1] >= 5.82 and floatSamples[i][1] < 5.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_582.append(1)
                                        else:
                                                seq_22_582.append(0)
                                elif floatSamples[i][1] >= 5.83 and floatSamples[i][1] < 5.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_583.append(1)
                                        else:
                                                seq_22_583.append(0)
                                elif floatSamples[i][1] >= 5.84 and floatSamples[i][1] < 5.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_584.append(1)
                                        else:
                                                seq_22_584.append(0)
                                elif floatSamples[i][1] >= 5.85 and floatSamples[i][1] < 5.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_585.append(1)
                                        else:
                                                seq_22_585.append(0)
                                elif floatSamples[i][1] >= 5.86 and floatSamples[i][1] < 5.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_586.append(1)
                                        else:
                                                seq_22_586.append(0)
                                elif floatSamples[i][1] >= 5.87 and floatSamples[i][1] < 5.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_22_587.append(1)
                                        else:
                                                seq_20_587.append(0)
                        elif floatSamples[i][0] == 23:
                                if floatSamples[i][1] >= 0.8 and floatSamples[i][1] < 0.81:
                                        if floatSamples[i][2] > -100:
                                                seq_23_08.append(1)
                                        else:
                                                seq_23_08.append(0)
                                elif floatSamples[i][1] >= 0.81 and floatSamples[i][1] < 0.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_081.append(1)
                                        else:
                                                seq_23_081.append(0)
                                elif floatSamples[i][1] >= 0.82 and floatSamples[i][1] < 0.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_082.append(1)
                                        else:
                                                seq_23_082.append(0)
                                elif floatSamples[i][1] >= 0.83 and floatSamples[i][1] < 0.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_083.append(1)
                                        else:
                                                seq_23_083.append(0)
                                elif floatSamples[i][1] >= 0.84 and floatSamples[i][1] < 0.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_084.append(1)
                                        else:
                                                seq_23_084.append(0)
                                elif floatSamples[i][1] >= 0.85 and floatSamples[i][1] < 0.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_085.append(1)
                                        else:
                                                seq_23_085.append(0)
                                elif floatSamples[i][1] >= 0.86 and floatSamples[i][1] < 0.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_086.append(1)
                                        else:
                                                seq_23_086.append(0)
                                elif floatSamples[i][1] >= 0.87 and floatSamples[i][1] < 0.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_087.append(1)
                                        else:
                                                seq_23_087.append(0)
                                elif floatSamples[i][1] >= 0.88 and floatSamples[i][1] < 0.89:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_088.append(1)
                                        else:
                                                seq_23_088.append(0)
                                elif floatSamples[i][1] >= 0.89 and floatSamples[i][1] < 0.90:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_089.append(1)
                                        else:
                                                seq_23_089.append(0)
                                elif floatSamples[i][1] >= 0.90 and floatSamples[i][1] < 0.91:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_090.append(1)
                                        else:
                                                seq_23_090.append(0)
                                elif floatSamples[i][1] >= 0.91 and floatSamples[i][1] < 0.92:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_091.append(1)
                                        else:
                                                seq_23_091.append(0)
                                elif floatSamples[i][1] >= 2.4 and floatSamples[i][1] < 2.41: 
                                        if floatSamples[i][2]  > -100:
                                                seq_23_240.append(1)
                                        else:
                                                seq_23_240.append(0)
                                elif floatSamples[i][1] >= 2.41 and floatSamples[i][1] < 2.42:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_241.append(1)
                                        else:
                                                seq_23_241.append(0)
                                elif floatSamples[i][1] >= 2.42 and floatSamples[i][1] < 2.43:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_242.append(1)
                                        else:
                                                seq_23_242.append(0)
                                elif floatSamples[i][1] >= 2.43 and floatSamples[i][1] < 2.44:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_243.append(1)
                                        else:
                                                seq_23_243.append(0)
                                elif floatSamples[i][1] >= 2.44 and floatSamples[i][1] < 2.45:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_244.append(1)
                                        else:
                                                seq_23_244.append(0)
                                elif floatSamples[i][1] >= 2.45 and floatSamples[i][1] < 2.46:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_245.append(1)
                                        else:
                                                seq_23_245.append(0)
                                elif floatSamples[i][1] >= 2.46 and floatSamples[i][1] < 2.47:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_246.append(1)
                                        else:
                                                seq_23_246.append(0)
                                elif floatSamples[i][1] >= 2.47 and floatSamples[i][1] < 2.48:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_247.append(1)
                                        else:
                                                seq_23_247.append(0)
                                elif floatSamples[i][1] >= 2.48 and floatSamples[i][1] < 2.49:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_248.append(1)
                                        else:
                                                seq_23_248.append(0)
                                elif floatSamples[i][1] >= 2.49 and floatSamples[i][1] < 2.50:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_249.append(1)
                                        else:
                                                seq_23_249.append(0)
                                elif floatSamples[i][1] >= 5.71 and floatSamples[i][1] < 5.72:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_571.append(1)
                                        else:
                                                seq_23_571.append(0)
                                elif floatSamples[i][1] >= 5.72 and floatSamples[i][1] < 5.73:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_572.append(1)
                                        else:
                                                seq_23_572.append(0)
                                elif floatSamples[i][1] >= 5.73 and floatSamples[i][1] < 5.74:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_573.append(1)
                                        else:
                                                seq_23_573.append(0)
                                elif floatSamples[i][1] >= 5.74 and floatSamples[i][1] < 5.75:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_574.append(1)
                                        else:
                                                seq_23_574.append(0)
                                elif floatSamples[i][1] >= 5.75 and floatSamples[i][1] < 5.76:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_575.append(1)
                                        else:
                                                seq_23_575.append(0)
                                elif floatSamples[i][1] >= 5.76 and floatSamples[i][1] < 5.77:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_576.append(1)
                                        else:
                                                seq_23_576.append(0)
                                elif floatSamples[i][1] >= 5.77 and floatSamples[i][1] < 5.78:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_577.append(1)
                                        else:
                                                seq_23_577.append(0)
                                elif floatSamples[i][1] >= 5.78 and floatSamples[i][1] < 5.79:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_578.append(1)
                                        else:
                                                seq_23_578.append(0)
                                elif floatSamples[i][1] >= 5.79 and floatSamples[i][1] < 5.8:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_579.append(1)
                                        else:
                                                seq_23_579.append(0)
                                elif floatSamples[i][1] >= 5.8 and floatSamples[i][1] < 5.81:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_580.append(1)
                                        else:
                                                seq_23_580.append(0)
                                elif floatSamples[i][1] >= 5.81 and floatSamples[i][1] < 5.82:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_581.append(1)
                                        else:
                                                seq_23_581.append(0)
                                elif floatSamples[i][1] >= 5.82 and floatSamples[i][1] < 5.83:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_582.append(1)
                                        else:
                                                seq_23_582.append(0)
                                elif floatSamples[i][1] >= 5.83 and floatSamples[i][1] < 5.84:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_583.append(1)
                                        else:
                                                seq_23_583.append(0)
                                elif floatSamples[i][1] >= 5.84 and floatSamples[i][1] < 5.85:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_584.append(1)
                                        else:
                                                seq_23_584.append(0)
                                elif floatSamples[i][1] >= 5.85 and floatSamples[i][1] < 5.86:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_585.append(1)
                                        else:
                                                seq_23_585.append(0)
                                elif floatSamples[i][1] >= 5.86 and floatSamples[i][1] < 5.87:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_586.append(1)
                                        else:
                                                seq_23_586.append(0)
                                elif floatSamples[i][1] >= 5.87 and floatSamples[i][1] < 5.88:
                                        if floatSamples[i][2]  > -100:
                                                seq_23_587.append(1)
                                        else:
                                                seq_23_587.append(0)
                        else:
                                print 'OCORREU UM CRIAR SEQUENCIA DE OBSERVACOES DADO RUIDO BASE'

                final = []

                #seq_0_08 = []
                if seq_0_08:
                        mydata = [seq_0_08]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_08.npz" ) #load model from file
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.8])

                #seq_0_081 = []
                if seq_0_081:
                        mydata = [seq_0_081]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_081.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.81])

                #seq_0_082 = []
                if seq_0_082:
                        mydata = [seq_0_082]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_082.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.82])


                #seq_0_083 = []
                if seq_0_083:
                        mydata = [seq_0_083]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_083.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.83])

                #seq_0_084 = []
                if seq_0_084:
                        mydata = [seq_0_084]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_084.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.84])

                #seq_0_085 = []
                if seq_0_085:
                        mydata = [seq_0_085]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_085.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.85])

                #seq_0_086 = []
                if seq_0_086:
                        mydata = [seq_0_086]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_086.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.86])

                #seq_0_087 = []
                if seq_0_087:
                        mydata = [seq_0_087]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_087.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.87])

                #seq_0_088 = []
                if seq_0_088:
                        mydata = [seq_0_088]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_088.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.88])

                #seq_0_089 = []
                if seq_0_089:
                        mydata = [seq_0_089]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_089.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.89])

                #seq_0_090 = []
                if seq_0_090:
                        mydata = [seq_0_090]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm	= hmms.DtHMM.from_file( path + "seq_0_090.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.90])

                #seq_0_091 = []
                if seq_0_091:
                        mydata = [seq_0_091]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_091.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.91])

                #seq_0_240 = []
                if seq_0_240:
                        mydata = [seq_0_240]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_240.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.40])

                #seq_0_241 = []
                if seq_0_241:
                        mydata = [seq_0_241]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_241.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.41])

                #seq_0_242 = []
                if seq_0_242:
                        mydata = [seq_0_242]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_242.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.42])

                #seq_0_243 = []
                if seq_0_243:
                        mydata = [seq_0_243]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_243.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.43])

                #seq_0_244 = []
                if seq_0_244:
                        mydata = [seq_0_244]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_244.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.44])

                #seq_0_245 = []
                if seq_0_245:
                        mydata = [seq_0_245]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_245.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.45])

                #seq_0_246 = []
                if seq_0_246:
                        mydata = [seq_0_246]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_246.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.46])

                #seq_0_247 = []
                if seq_0_247:
                        mydata = [seq_0_247]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_247.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.47])

                #seq_0_248 = []
                if seq_0_248:
                        mydata = [seq_0_248]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_248.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.48])

                #seq_0_249 = []
                if seq_0_249:
                        mydata = [seq_0_249]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_249.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.49])

                #seq_0_571 = []
                if seq_0_571:
                        mydata = [seq_0_571]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_571.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.71])

                #seq_0_572 = []
                if seq_0_572:
                        mydata = [seq_0_572]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_572.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.72])

                #seq_0_573 = []
                if seq_0_573:
                        mydata = [seq_0_573]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_573.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.73])

                #seq_0_574 = []
                if seq_0_574:
                        mydata = [seq_0_574]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_574.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.74])

                #seq_0_575 = []
                if seq_0_575:
                        mydata = [seq_0_575]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_575.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.75])

                #seq_0_576 = []
                if seq_0_576:
                        mydata = [seq_0_576]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_576.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.76])

                #seq_0_577 = []
                if seq_0_577:
                        mydata = [seq_0_577]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_577.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.77])

                #seq_0_578 = []
                if seq_0_578:
                        mydata = [seq_0_578]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_578.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.78])

                #seq_0_579 = []
                if seq_0_579:
                        mydata = [seq_0_579]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_579.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.79])

                #seq_0_580 = []
                if seq_0_580:
                        mydata = [seq_0_580]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_580.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.80])

                #seq_0_581 = []
                if seq_0_581:
                        mydata = [seq_0_581]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_581.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.81])

                #seq_0_582 = []
                if seq_0_582:
                        mydata = [seq_0_582]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_582.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.82])

                #seq_0_583 = []
                if seq_0_583:
                        mydata = [seq_0_583]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_583.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.83])

                #seq_0_584 = []
                if seq_0_584:
                        mydata = [seq_0_584]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_584.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.84])

                #seq_0_585 = []
                if seq_0_585:
                        mydata = [seq_0_585]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_585.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.85])

                #seq_0_586 = []
                if seq_0_586:
                        mydata = [seq_0_586]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_586.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.86])

                #seq_0_587 = []
                if seq_0_587:
                        mydata = [seq_0_587]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_0_587.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.87])

                #seq_1_08 = []
                if seq_1_08:
                        mydata = [seq_1_08]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_08.npz" ) #load model from file
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.8])

                #seq_1_081 = []
                if seq_1_081:
                        mydata = [seq_1_081]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_081.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.81])

                #seq_1_082 = []
                if seq_1_082:
                        mydata = [seq_1_082]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_082.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.82])


                #seq_1_083 = []
                if seq_1_083:
                        mydata = [seq_1_083]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_083.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.83])

                #seq_1_084 = []
                if seq_1_084:
                        mydata = [seq_1_084]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_084.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.84])

                #seq_1_085 = []
                if seq_1_085:
                        mydata = [seq_1_085]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_085.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.85])

                #seq_1_086 = []
                if seq_1_086:
                        mydata = [seq_1_086]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_086.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.86])

                #seq_1_087 = []
                if seq_1_087:
                        mydata = [seq_1_087]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_087.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.87])

                #seq_1_088 = []
                if seq_1_088:
                        mydata = [seq_1_088]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_088.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.88])

                #seq_1_089 = []
                if seq_1_089:
                        mydata = [seq_1_089]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_089.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.89])

                #seq_1_090 = []
                if seq_1_090:
                        mydata = [seq_1_090]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm	= hmms.DtHMM.from_file( path + "seq_1_090.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.90])

                #seq_1_091 = []
                if seq_1_091:
                        mydata = [seq_1_091]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_091.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.91])

                #seq_1_240 = []
                if seq_1_240:
                        mydata = [seq_1_240]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_240.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.40])

                #seq_1_241 = []
                if seq_1_241:
                        mydata = [seq_1_241]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_241.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.41])

                #seq_1_242 = []
                if seq_1_242:
                        mydata = [seq_1_242]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_242.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.42])

                #seq_1_243 = []
                if seq_1_243:
                        mydata = [seq_1_243]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_243.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.43])

                #seq_1_244 = []
                if seq_1_244:
                        mydata = [seq_1_244]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_244.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.44])

                #seq_1_245 = []
                if seq_1_245:
                        mydata = [seq_1_245]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_245.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.45])

                #seq_1_246 = []
                if seq_1_246:
                        mydata = [seq_1_246]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_246.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.46])

                #seq_1_247 = []
                if seq_1_247:
                        mydata = [seq_1_247]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_247.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.47])

                #seq_1_248 = []
                if seq_1_248:
                        mydata = [seq_1_248]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_248.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.48])

                #seq_1_249 = []
                if seq_1_249:
                        mydata = [seq_1_249]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_249.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.49])

                #seq_1_571 = []
                if seq_1_571:
                        mydata = [seq_1_571]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_571.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.71])

                #seq_1_572 = []
                if seq_1_572:
                        mydata = [seq_1_572]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_572.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.72])

                #seq_1_573 = []
                if seq_1_573:
                        mydata = [seq_1_573]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_573.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.73])

                #seq_1_574 = []
                if seq_1_574:
                        mydata = [seq_1_574]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_574.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.74])

                #seq_1_575 = []
                if seq_1_575:
                        mydata = [seq_1_575]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_575.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.75])

                #seq_1_576 = []
                if seq_1_576:
                        mydata = [seq_1_576]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_576.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.76])

                #seq_1_577 = []
                if seq_1_577:
                        mydata = [seq_1_577]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_577.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.77])

                #seq_1_578 = []
                if seq_1_578:
                        mydata = [seq_1_578]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_578.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.78])

                #seq_1_579 = []
                if seq_1_579:
                        mydata = [seq_1_579]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_579.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.79])

                #seq_1_580 = []
                if seq_1_580:
                        mydata = [seq_1_580]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_580.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.80])

                #seq_1_581 = []
                if seq_1_581:
                        mydata = [seq_1_581]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_581.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.81])

                #seq_1_582 = []
                if seq_1_582:
                        mydata = [seq_1_582]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_582.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.82])

                #seq_1_583 = []
                if seq_1_583:
                        mydata = [seq_1_583]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_583.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.83])

                #seq_1_584 = []
                if seq_1_584:
                        mydata = [seq_1_584]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_584.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.84])

                #seq_1_585 = []
                if seq_1_585:
                        mydata = [seq_1_585]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_585.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.85])

                #seq_1_586 = []
                if seq_1_586:
                        mydata = [seq_1_586]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_586.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.86])

                #seq_1_587 = []
                if seq_1_587:
                        mydata = [seq_1_587]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_1_587.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.87])

                #seq_2_08 = []
                if seq_2_08:
                        mydata = [seq_2_08]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_08.npz" ) #load model from file
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.8])

                #seq_2_081 = []
                if seq_2_081:
                        mydata = [seq_2_081]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_081.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.81])

                #seq_2_082 = []
                if seq_2_082:
                        mydata = [seq_2_082]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_082.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.82])


                #seq_2_083 = []
                if seq_2_083:
                        mydata = [seq_2_083]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_083.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.83])

                #seq_2_084 = []
                if seq_2_084:
                        mydata = [seq_2_084]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_084.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.84])

                #seq_2_085 = []
                if seq_2_085:
                        mydata = [seq_2_085]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_085.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.85])

                #seq_2_086 = []
                if seq_2_086:
                        mydata = [seq_2_086]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_086.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.86])

                #seq_2_087 = []
                if seq_2_087:
                        mydata = [seq_2_087]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_087.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.87])

                #seq_2_088 = []
                if seq_2_088:
                        mydata = [seq_2_088]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_088.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.88])

                #seq_2_089 = []
                if seq_2_089:
                        mydata = [seq_2_089]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_089.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.89])

                #seq_2_090 = []
                if seq_2_090:
                        mydata = [seq_2_090]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm	= hmms.DtHMM.from_file( path + "seq_2_090.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.90])

                #seq_2_091 = []
                if seq_2_091:
                        mydata = [seq_2_091]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_091.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.91])

                #seq_2_240 = []
                if seq_2_240:
                        mydata = [seq_2_240]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_240.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.40])

                #seq_2_241 = []
                if seq_2_241:
                        mydata = [seq_2_241]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_241.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.41])

                #seq_2_242 = []
                if seq_2_242:
                        mydata = [seq_2_242]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_242.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.42])

                #seq_2_243 = []
                if seq_2_243:
                        mydata = [seq_2_243]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_243.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.43])

                #seq_2_244 = []
                if seq_2_244:
                        mydata = [seq_2_244]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_244.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.44])

                #seq_2_245 = []
                if seq_2_245:
                        mydata = [seq_2_245]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_245.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.45])

                #seq_2_246 = []
                if seq_2_246:
                        mydata = [seq_2_246]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_246.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.46])

                #seq_2_247 = []
                if seq_2_247:
                        mydata = [seq_2_247]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_247.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.47])

                #seq_2_248 = []
                if seq_2_248:
                        mydata = [seq_2_248]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_248.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.48])

                #seq_2_249 = []
                if seq_2_249:
                        mydata = [seq_2_249]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_249.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.49])

                #seq_2_571 = []
                if seq_2_571:
                        mydata = [seq_2_571]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_571.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.71])

                #seq_2_572 = []
                if seq_2_572:
                        mydata = [seq_2_572]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_572.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.72])

                #seq_2_573 = []
                if seq_2_573:
                        mydata = [seq_2_573]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_573.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.73])

                #seq_2_574 = []
                if seq_2_574:
                        mydata = [seq_2_574]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_574.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.74])

                #seq_2_575 = []
                if seq_2_575:
                        mydata = [seq_2_575]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_575.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.75])

                #seq_2_576 = []
                if seq_2_576:
                        mydata = [seq_2_576]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_576.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.76])

                #seq_2_577 = []
                if seq_2_577:
                        mydata = [seq_2_577]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_577.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.77])

                #seq_2_578 = []
                if seq_2_578:
                        mydata = [seq_2_578]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_578.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.78])

                #seq_2_579 = []
                if seq_2_579:
                        mydata = [seq_2_579]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_579.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.79])

                #seq_2_580 = []
                if seq_2_580:
                        mydata = [seq_2_580]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_580.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.80])

                #seq_2_581 = []
                if seq_2_581:
                        mydata = [seq_2_581]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_581.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.81])

                #seq_2_582 = []
                if seq_2_582:
                        mydata = [seq_2_582]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_582.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.82])

                #seq_2_583 = []
                if seq_2_583:
                        mydata = [seq_2_583]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_583.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.83])

                #seq_2_584 = []
                if seq_2_584:
                        mydata = [seq_2_584]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_584.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.84])

                #seq_2_585 = []
                if seq_2_585:
                        mydata = [seq_2_585]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_585.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.85])

                #seq_2_586 = []
                if seq_2_586:
                        mydata = [seq_2_586]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_586.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.86])

                #seq_2_587 = []
                if seq_2_587:
                        mydata = [seq_2_587]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_2_587.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.87])

                #seq_3_08 = []
                if seq_3_08:
                        mydata = [seq_3_08]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_08.npz" ) #load model from file
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.8])

                #seq_3_081 = []
                if seq_3_081:
                        mydata = [seq_3_081]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_081.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.81])

                #seq_3_082 = []
                if seq_3_082:
                        mydata = [seq_3_082]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_082.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.82])


                #seq_3_083 = []
                if seq_3_083:
                        mydata = [seq_3_083]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_083.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.83])

                #seq_3_084 = []
                if seq_3_084:
                        mydata = [seq_3_084]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_084.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.84])

                #seq_3_085 = []
                if seq_3_085:
                        mydata = [seq_3_085]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_085.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.85])

                #seq_3_086 = []
                if seq_3_086:
                        mydata = [seq_3_086]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_086.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.86])

                #seq_3_087 = []
                if seq_3_087:
                        mydata = [seq_3_087]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_087.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.87])

                #seq_3_088 = []
                if seq_3_088:
                        mydata = [seq_3_088]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_088.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.88])

                #seq_3_089 = []
                if seq_3_089:
                        mydata = [seq_3_089]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_089.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.89])

                #seq_3_090 = []
                if seq_3_090:
                        mydata = [seq_3_090]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm	= hmms.DtHMM.from_file( path + "seq_3_090.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.90])

                #seq_3_091 = []
                if seq_3_091:
                        mydata = [seq_3_091]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_091.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.91])

                #seq_3_240 = []
                if seq_3_240:
                        mydata = [seq_3_240]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_240.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.40])

                #seq_3_241 = []
                if seq_3_241:
                        mydata = [seq_3_241]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_241.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.41])

                #seq_3_242 = []
                if seq_3_242:
                        mydata = [seq_3_242]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_242.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.42])

                #seq_3_243 = []
                if seq_3_243:
                        mydata = [seq_3_243]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_243.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.43])

                #seq_3_244 = []
                if seq_3_244:
                        mydata = [seq_3_244]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_244.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.44])

                #seq_3_245 = []
                if seq_3_245:
                        mydata = [seq_3_245]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_245.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.45])

                #seq_3_246 = []
                if seq_3_246:
                        mydata = [seq_3_246]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_246.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.46])

                #seq_3_247 = []
                if seq_3_247:
                        mydata = [seq_3_247]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_247.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.47])

                #seq_3_248 = []
                if seq_3_248:
                        mydata = [seq_3_248]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_248.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.48])

                #seq_3_249 = []
                if seq_3_249:
                        mydata = [seq_3_249]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_249.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.49])

                #seq_3_571 = []
                if seq_3_571:
                        mydata = [seq_3_571]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_571.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.71])

                #seq_3_572 = []
                if seq_3_572:
                        mydata = [seq_3_572]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_572.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.72])

                #seq_3_573 = []
                if seq_3_573:
                        mydata = [seq_3_573]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_573.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.73])

                #seq_3_574 = []
                if seq_3_574:
                        mydata = [seq_3_574]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_574.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.74])

                #seq_3_575 = []
                if seq_3_575:
                        mydata = [seq_3_575]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_575.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.75])

                #seq_3_576 = []
                if seq_3_576:
                        mydata = [seq_3_576]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_576.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.76])

                #seq_3_577 = []
                if seq_3_577:
                        mydata = [seq_3_577]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_577.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.77])

                #seq_3_578 = []
                if seq_3_578:
                        mydata = [seq_3_578]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_578.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.78])

                #seq_3_579 = []
                if seq_3_579:
                        mydata = [seq_3_579]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_579.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.79])

                #seq_3_580 = []
                if seq_3_580:
                        mydata = [seq_3_580]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_580.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.80])

                #seq_3_581 = []
                if seq_3_581:
                        mydata = [seq_3_581]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_581.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.81])

                #seq_3_582 = []
                if seq_3_582:
                        mydata = [seq_3_582]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_582.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.82])

                #seq_3_583 = []
                if seq_3_583:
                        mydata = [seq_3_583]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_583.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.83])

                #seq_3_584 = []
                if seq_3_584:
                        mydata = [seq_3_584]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_584.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.84])

                #seq_3_585 = []
                if seq_3_585:
                        mydata = [seq_3_585]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_585.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.85])

                #seq_3_586 = []
                if seq_3_586:
                        mydata = [seq_3_586]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_586.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.86])

                #seq_3_587 = []
                if seq_3_587:
                        mydata = [seq_3_587]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_3_587.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.87])

                #seq_4_08 = []
                if seq_4_08:
                        mydata = [seq_4_08]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_08.npz" ) #load model from file
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.8])

                #seq_4_081 = []
                if seq_4_081:
                        mydata = [seq_4_081]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_081.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.81])

                #seq_4_082 = []
                if seq_4_082:
                        mydata = [seq_4_082]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_082.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.82])


                #seq_4_083 = []
                if seq_4_083:
                        mydata = [seq_4_083]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_083.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.83])

                #seq_4_084 = []
                if seq_4_084:
                        mydata = [seq_4_084]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_084.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.84])

                #seq_4_085 = []
                if seq_4_085:
                        mydata = [seq_4_085]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_085.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.85])

                #seq_4_086 = []
                if seq_4_086:
                        mydata = [seq_4_086]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_086.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.86])

                #seq_4_087 = []
                if seq_4_087:
                        mydata = [seq_4_087]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_087.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.87])

                #seq_4_088 = []
                if seq_4_088:
                        mydata = [seq_4_088]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_088.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.88])

                #seq_4_089 = []
                if seq_4_089:
                        mydata = [seq_4_089]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_089.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.89])

                #seq_4_090 = []
                if seq_4_090:
                        mydata = [seq_4_090]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm	= hmms.DtHMM.from_file( path + "seq_4_090.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.90])

                #seq_4_091 = []
                if seq_4_091:
                        mydata = [seq_4_091]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_091.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.91])

                #seq_4_240 = []
                if seq_4_240:
                        mydata = [seq_4_240]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_240.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.40])

                #seq_4_241 = []
                if seq_4_241:
                        mydata = [seq_4_241]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_241.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.41])

                #seq_4_242 = []
                if seq_4_242:
                        mydata = [seq_4_242]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_242.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.42])

                #seq_4_243 = []
                if seq_4_243:
                        mydata = [seq_4_243]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_243.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.43])

                #seq_4_244 = []
                if seq_4_244:
                        mydata = [seq_4_244]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_244.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.44])

                #seq_4_245 = []
                if seq_4_245:
                        mydata = [seq_4_245]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_245.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.45])

                #seq_4_246 = []
                if seq_4_246:
                        mydata = [seq_4_246]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_246.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.46])

                #seq_4_247 = []
                if seq_4_247:
                        mydata = [seq_4_247]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_247.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.47])

                #seq_4_248 = []
                if seq_4_248:
                        mydata = [seq_4_248]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_248.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.48])

                #seq_4_249 = []
                if seq_4_249:
                        mydata = [seq_4_249]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_249.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.49])

                #seq_4_571 = []
                if seq_4_571:
                        mydata = [seq_4_571]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_571.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.71])

                #seq_4_572 = []
                if seq_4_572:
                        mydata = [seq_4_572]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_572.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.72])

                #seq_4_573 = []
                if seq_4_573:
                        mydata = [seq_4_573]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_573.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.73])

                #seq_4_574 = []
                if seq_4_574:
                        mydata = [seq_4_574]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_574.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.74])

                #seq_4_575 = []
                if seq_4_575:
                        mydata = [seq_4_575]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_575.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.75])

                #seq_4_576 = []
                if seq_4_576:
                        mydata = [seq_4_576]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_576.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.76])

                #seq_4_577 = []
                if seq_4_577:
                        mydata = [seq_4_577]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_577.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.77])

                #seq_4_578 = []
                if seq_4_578:
                        mydata = [seq_4_578]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_578.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.78])

                #seq_4_579 = []
                if seq_4_579:
                        mydata = [seq_4_579]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_579.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.79])

                #seq_4_580 = []
                if seq_4_580:
                        mydata = [seq_4_580]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_580.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.80])

                #seq_4_581 = []
                if seq_4_581:
                        mydata = [seq_4_581]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_581.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.81])

                #seq_4_582 = []
                if seq_4_582:
                        mydata = [seq_4_582]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_582.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.82])

                #seq_4_583 = []
                if seq_4_583:
                        mydata = [seq_4_583]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_583.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.83])

                #seq_4_584 = []
                if seq_4_584:
                        mydata = [seq_4_584]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_584.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.84])

                #seq_4_585 = []
                if seq_4_585:
                        mydata = [seq_4_585]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_585.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.85])

                #seq_4_586 = []
                if seq_4_586:
                        mydata = [seq_4_586]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_586.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.86])

                #seq_4_587 = []
                if seq_4_587:
                        mydata = [seq_4_587]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_4_587.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.87])

                #seq_5_08 = []
                if seq_5_08:
                        mydata = [seq_5_08]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_08.npz" ) #load model from file
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.8])

                #seq_5_081 = []
                if seq_5_081:
                        mydata = [seq_5_081]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_081.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.81])

                #seq_5_082 = []
                if seq_5_082:
                        mydata = [seq_5_082]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_082.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.82])


                #seq_5_083 = []
                if seq_5_083:
                        mydata = [seq_5_083]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_083.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.83])

                #seq_5_084 = []
                if seq_5_084:
                        mydata = [seq_5_084]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_084.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.84])

                #seq_5_085 = []
                if seq_5_085:
                        mydata = [seq_5_085]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_085.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.85])

                #seq_5_086 = []
                if seq_5_086:
                        mydata = [seq_5_086]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_086.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.86])

                #seq_5_087 = []
                if seq_5_087:
                        mydata = [seq_5_087]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_087.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.87])

                #seq_5_088 = []
                if seq_5_088:
                        mydata = [seq_5_088]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_088.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.88])

                #seq_5_089 = []
                if seq_5_089:
                        mydata = [seq_5_089]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_089.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.89])

                #seq_5_090 = []
                if seq_5_090:
                        mydata = [seq_5_090]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm	= hmms.DtHMM.from_file( path + "seq_5_090.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.90])

                #seq_5_091 = []
                if seq_5_091:
                        mydata = [seq_5_091]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_091.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.91])

                #seq_5_240 = []
                if seq_5_240:
                        mydata = [seq_5_240]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_240.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.40])

                #seq_5_241 = []
                if seq_5_241:
                        mydata = [seq_5_241]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_241.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.41])

                #seq_5_242 = []
                if seq_5_242:
                        mydata = [seq_5_242]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_242.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.42])

                #seq_5_243 = []
                if seq_5_243:
                        mydata = [seq_5_243]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_243.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.43])

                #seq_5_244 = []
                if seq_5_244:
                        mydata = [seq_5_244]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_244.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.44])

                #seq_5_245 = []
                if seq_5_245:
                        mydata = [seq_5_245]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_245.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.45])

                #seq_5_246 = []
                if seq_5_246:
                        mydata = [seq_5_246]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_246.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.46])

                #seq_5_247 = []
                if seq_5_247:
                        mydata = [seq_5_247]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_247.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.47])

                #seq_5_248 = []
                if seq_5_248:
                        mydata = [seq_5_248]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_248.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.48])

                #seq_5_249 = []
                if seq_5_249:
                        mydata = [seq_5_249]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_249.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.49])

                #seq_5_571 = []
                if seq_5_571:
                        mydata = [seq_5_571]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_571.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.71])

                #seq_5_572 = []
                if seq_5_572:
                        mydata = [seq_5_572]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_572.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.72])

                #seq_5_573 = []
                if seq_5_573:
                        mydata = [seq_5_573]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_573.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.73])

                #seq_5_574 = []
                if seq_5_574:
                        mydata = [seq_5_574]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_574.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.74])

                #seq_5_575 = []
                if seq_5_575:
                        mydata = [seq_5_575]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_575.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.75])

                #seq_5_576 = []
                if seq_5_576:
                        mydata = [seq_5_576]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_576.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.76])

                #seq_5_577 = []
                if seq_5_577:
                        mydata = [seq_5_577]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_577.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.77])

                #seq_5_578 = []
                if seq_5_578:
                        mydata = [seq_5_578]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_578.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.78])

                #seq_5_579 = []
                if seq_5_579:
                        mydata = [seq_5_579]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_579.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.79])

                #seq_5_580 = []
                if seq_5_580:
                        mydata = [seq_5_580]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_580.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.80])

                #seq_5_581 = []
                if seq_5_581:
                        mydata = [seq_5_581]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_581.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.81])

                #seq_5_582 = []
                if seq_5_582:
                        mydata = [seq_5_582]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_582.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.82])

                #seq_5_583 = []
                if seq_5_583:
                        mydata = [seq_5_583]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_583.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.83])

                #seq_5_584 = []
                if seq_5_584:
                        mydata = [seq_5_584]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_584.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.84])

                #seq_5_585 = []
                if seq_5_585:
                        mydata = [seq_5_585]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_585.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.85])

                #seq_5_586 = []
                if seq_5_586:
                        mydata = [seq_5_586]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_586.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.86])

                #seq_5_587 = []
                if seq_5_587:
                        mydata = [seq_5_587]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_5_587.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.87])

                #seq_6_08 = []
                if seq_6_08:
                        mydata = [seq_6_08]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_08.npz" ) #load model from file
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.8])

                #seq_6_081 = []
                if seq_6_081:
                        mydata = [seq_6_081]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_081.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.81])

                #seq_6_082 = []
                if seq_6_082:
                        mydata = [seq_6_082]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_082.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.82])


                #seq_6_083 = []
                if seq_6_083:
                        mydata = [seq_6_083]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_083.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.83])

                #seq_6_084 = []
                if seq_6_084:
                        mydata = [seq_6_084]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_084.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.84])

                #seq_6_085 = []
                if seq_6_085:
                        mydata = [seq_6_085]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_085.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.85])

                #seq_6_086 = []
                if seq_6_086:
                        mydata = [seq_6_086]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_086.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.86])

                #seq_6_087 = []
                if seq_6_087:
                        mydata = [seq_6_087]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_087.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.87])

                #seq_6_088 = []
                if seq_6_088:
                        mydata = [seq_6_088]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_088.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.88])

                #seq_6_089 = []
                if seq_6_089:
                        mydata = [seq_6_089]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_089.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.89])

                #seq_6_090 = []
                if seq_6_090:
                        mydata = [seq_6_090]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm	= hmms.DtHMM.from_file( path + "seq_6_090.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.90])

                #seq_6_091 = []
                if seq_6_091:
                        mydata = [seq_6_091]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_091.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.91])

                #seq_6_240 = []
                if seq_6_240:
                        mydata = [seq_6_240]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_240.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.40])

                #seq_6_241 = []
                if seq_6_241:
                        mydata = [seq_6_241]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_241.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.41])

                #seq_6_242 = []
                if seq_6_242:
                        mydata = [seq_6_242]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_242.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.42])

                #seq_6_243 = []
                if seq_6_243:
                        mydata = [seq_6_243]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_243.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.43])

                #seq_6_244 = []
                if seq_6_244:
                        mydata = [seq_6_244]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_244.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.44])

                #seq_6_245 = []
                if seq_6_245:
                        mydata = [seq_6_245]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_245.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.45])

                #seq_6_246 = []
                if seq_6_246:
                        mydata = [seq_6_246]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_246.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.46])

                #seq_6_247 = []
                if seq_6_247:
                        mydata = [seq_6_247]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_247.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.47])

                #seq_6_248 = []
                if seq_6_248:
                        mydata = [seq_6_248]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_248.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.48])

                #seq_6_249 = []
                if seq_6_249:
                        mydata = [seq_6_249]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_249.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.49])

                #seq_6_571 = []
                if seq_6_571:
                        mydata = [seq_6_571]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_571.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.71])

                #seq_6_572 = []
                if seq_6_572:
                        mydata = [seq_6_572]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_572.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.72])

                #seq_6_573 = []
                if seq_6_573:
                        mydata = [seq_6_573]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_573.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.73])

                #seq_6_574 = []
                if seq_6_574:
                        mydata = [seq_6_574]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_574.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.74])

                #seq_6_575 = []
                if seq_6_575:
                        mydata = [seq_6_575]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_575.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.75])

                #seq_6_576 = []
                if seq_6_576:
                        mydata = [seq_6_576]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_576.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.76])

                #seq_6_577 = []
                if seq_6_577:
                        mydata = [seq_6_577]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_577.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.77])

                #seq_6_578 = []
                if seq_6_578:
                        mydata = [seq_6_578]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_578.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.78])

                #seq_6_579 = []
                if seq_6_579:
                        mydata = [seq_6_579]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_579.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.79])

                #seq_6_580 = []
                if seq_6_580:
                        mydata = [seq_6_580]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_580.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.80])

                #seq_6_581 = []
                if seq_6_581:
                        mydata = [seq_6_581]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_581.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.81])

                #seq_6_582 = []
                if seq_6_582:
                        mydata = [seq_6_582]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_582.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.82])

                #seq_6_583 = []
                if seq_6_583:
                        mydata = [seq_6_583]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_583.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.83])

                #seq_6_584 = []
                if seq_6_584:
                        mydata = [seq_6_584]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_584.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.84])

                #seq_6_585 = []
                if seq_6_585:
                        mydata = [seq_6_585]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_585.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.85])

                #seq_6_586 = []
                if seq_6_586:
                        mydata = [seq_6_586]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_586.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.86])

                #seq_6_587 = []
                if seq_6_587:
                        mydata = [seq_6_587]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_6_587.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.87])

                #seq_7_08 = []
                if seq_7_08:
                        mydata = [seq_7_08]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_08.npz" ) #load model from file
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.8])

                #seq_7_081 = []
                if seq_7_081:
                        mydata = [seq_7_081]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_081.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.81])

                #seq_7_082 = []
                if seq_7_082:
                        mydata = [seq_7_082]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_082.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.82])


                #seq_7_083 = []
                if seq_7_083:
                        mydata = [seq_7_083]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_083.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.83])

                #seq_7_084 = []
                if seq_7_084:
                        mydata = [seq_7_084]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_084.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.84])

                #seq_7_085 = []
                if seq_7_085:
                        mydata = [seq_7_085]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_085.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.85])

                #seq_7_086 = []
                if seq_7_086:
                        mydata = [seq_7_086]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_086.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.86])

                #seq_7_087 = []
                if seq_7_087:
                        mydata = [seq_7_087]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_087.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.87])

                #seq_7_088 = []
                if seq_7_088:
                        mydata = [seq_7_088]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_088.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.88])

                #seq_7_089 = []
                if seq_7_089:
                        mydata = [seq_7_089]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_089.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.89])

                #seq_7_090 = []
                if seq_7_090:
                        mydata = [seq_7_090]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm	= hmms.DtHMM.from_file( path + "seq_7_090.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.90])

                #seq_7_091 = []
                if seq_7_091:
                        mydata = [seq_7_091]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_091.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.91])

                #seq_7_240 = []
                if seq_7_240:
                        mydata = [seq_7_240]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_240.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.40])

                #seq_7_241 = []
                if seq_7_241:
                        mydata = [seq_7_241]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_241.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.41])

                #seq_7_242 = []
                if seq_7_242:
                        mydata = [seq_7_242]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_242.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.42])

                #seq_7_243 = []
                if seq_7_243:
                        mydata = [seq_7_243]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_243.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.43])

                #seq_7_244 = []
                if seq_7_244:
                        mydata = [seq_7_244]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_244.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.44])

                #seq_7_245 = []
                if seq_7_245:
                        mydata = [seq_7_245]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_245.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.45])

                #seq_7_246 = []
                if seq_7_246:
                        mydata = [seq_7_246]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_246.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.46])

                #seq_7_247 = []
                if seq_7_247:
                        mydata = [seq_7_247]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_247.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.47])

                #seq_7_248 = []
                if seq_7_248:
                        mydata = [seq_7_248]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_248.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.48])

                #seq_7_249 = []
                if seq_7_249:
                        mydata = [seq_7_249]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_249.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.49])

                #seq_7_571 = []
                if seq_7_571:
                        mydata = [seq_7_571]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_571.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.71])

                #seq_7_572 = []
                if seq_7_572:
                        mydata = [seq_7_572]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_572.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.72])

                #seq_7_573 = []
                if seq_7_573:
                        mydata = [seq_7_573]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_573.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.73])

                #seq_7_574 = []
                if seq_7_574:
                        mydata = [seq_7_574]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_574.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.74])

                #seq_7_575 = []
                if seq_7_575:
                        mydata = [seq_7_575]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_575.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.75])

                #seq_7_576 = []
                if seq_7_576:
                        mydata = [seq_7_576]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_576.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.76])

                #seq_7_577 = []
                if seq_7_577:
                        mydata = [seq_7_577]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_577.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.77])

                #seq_7_578 = []
                if seq_7_578:
                        mydata = [seq_7_578]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_578.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.78])

                #seq_7_579 = []
                if seq_7_579:
                        mydata = [seq_7_579]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_579.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.79])

                #seq_7_580 = []
                if seq_7_580:
                        mydata = [seq_7_580]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_580.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.80])

                #seq_7_581 = []
                if seq_7_581:
                        mydata = [seq_7_581]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_581.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.81])

                #seq_7_582 = []
                if seq_7_582:
                        mydata = [seq_7_582]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_582.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.82])

                #seq_7_583 = []
                if seq_7_583:
                        mydata = [seq_7_583]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_583.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.83])

                #seq_7_584 = []
                if seq_7_584:
                        mydata = [seq_7_584]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_584.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.84])

                #seq_7_585 = []
                if seq_7_585:
                        mydata = [seq_7_585]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_585.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.85])

                #seq_7_586 = []
                if seq_7_586:
                        mydata = [seq_7_586]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_586.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.86])

                #seq_7_587 = []
                if seq_7_587:
                        mydata = [seq_7_587]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_7_587.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.87])

                #seq_8_08 = []
                if seq_8_08:
                        mydata = [seq_8_08]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_08.npz" ) #load model from file
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.8])

                #seq_8_081 = []
                if seq_8_081:
                        mydata = [seq_8_081]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_081.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.81])

                #seq_8_082 = []
                if seq_8_082:
                        mydata = [seq_8_082]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_082.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.82])


                #seq_8_083 = []
                if seq_8_083:
                        mydata = [seq_8_083]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_083.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.83])

                #seq_8_084 = []
                if seq_8_084:
                        mydata = [seq_8_084]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_084.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.84])

                #seq_8_085 = []
                if seq_8_085:
                        mydata = [seq_8_085]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_085.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.85])

                #seq_8_086 = []
                if seq_8_086:
                        mydata = [seq_8_086]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_086.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.86])

                #seq_8_087 = []
                if seq_8_087:
                        mydata = [seq_8_087]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_087.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.87])

                #seq_8_088 = []
                if seq_8_088:
                        mydata = [seq_8_088]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_088.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.88])

                #seq_8_089 = []
                if seq_8_089:
                        mydata = [seq_8_089]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_089.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.89])

                #seq_8_090 = []
                if seq_8_090:
                        mydata = [seq_8_090]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm	= hmms.DtHMM.from_file( path + "seq_8_090.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.90])

                #seq_8_091 = []
                if seq_8_091:
                        mydata = [seq_8_091]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_091.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.91])

                #seq_8_240 = []
                if seq_8_240:
                        mydata = [seq_8_240]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_240.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.40])

                #seq_8_241 = []
                if seq_8_241:
                        mydata = [seq_8_241]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_241.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.41])

                #seq_8_242 = []
                if seq_8_242:
                        mydata = [seq_8_242]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_242.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.42])

                #seq_8_243 = []
                if seq_8_243:
                        mydata = [seq_8_243]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_243.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.43])

                #seq_8_244 = []
                if seq_8_244:
                        mydata = [seq_8_244]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_244.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.44])

                #seq_8_245 = []
                if seq_8_245:
                        mydata = [seq_8_245]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_245.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.45])

                #seq_8_246 = []
                if seq_8_246:
                        mydata = [seq_8_246]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_246.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.46])

                #seq_8_247 = []
                if seq_8_247:
                        mydata = [seq_8_247]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_247.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.47])

                #seq_8_248 = []
                if seq_8_248:
                        mydata = [seq_8_248]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_248.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.48])

                #seq_8_249 = []
                if seq_8_249:
                        mydata = [seq_8_249]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_249.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.49])

                #seq_8_571 = []
                if seq_8_571:
                        mydata = [seq_8_571]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_571.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.71])

                #seq_8_572 = []
                if seq_8_572:
                        mydata = [seq_8_572]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_572.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.72])

                #seq_8_573 = []
                if seq_8_573:
                        mydata = [seq_8_573]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_573.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.73])

                #seq_8_574 = []
                if seq_8_574:
                        mydata = [seq_8_574]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_574.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.74])

                #seq_8_575 = []
                if seq_8_575:
                        mydata = [seq_8_575]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_575.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.75])

                #seq_8_576 = []
                if seq_8_576:
                        mydata = [seq_8_576]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_576.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.76])

                #seq_8_577 = []
                if seq_8_577:
                        mydata = [seq_8_577]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_577.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.77])

                #seq_8_578 = []
                if seq_8_578:
                        mydata = [seq_8_578]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_578.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.78])

                #seq_8_579 = []
                if seq_8_579:
                        mydata = [seq_8_579]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_579.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.79])

                #seq_8_580 = []
                if seq_8_580:
                        mydata = [seq_8_580]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_580.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.80])

                #seq_8_581 = []
                if seq_8_581:
                        mydata = [seq_8_581]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_581.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.81])

                #seq_8_582 = []
                if seq_8_582:
                        mydata = [seq_8_582]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_582.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.82])

                #seq_8_583 = []
                if seq_8_583:
                        mydata = [seq_8_583]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_583.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.83])

                #seq_8_584 = []
                if seq_8_584:
                        mydata = [seq_8_584]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_584.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.84])

                #seq_8_585 = []
                if seq_8_585:
                        mydata = [seq_8_585]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_585.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.85])

                #seq_8_586 = []
                if seq_8_586:
                        mydata = [seq_8_586]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_586.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.86])

                #seq_8_587 = []
                if seq_8_587:
                        mydata = [seq_8_587]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_8_587.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.87])

                #seq_9_08 = []
                if seq_9_08:
                        mydata = [seq_9_08]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_08.npz" ) #load model from file
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.8])

                #seq_9_081 = []
                if seq_9_081:
                        mydata = [seq_9_081]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_081.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.81])

                #seq_9_082 = []
                if seq_9_082:
                        mydata = [seq_9_082]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_082.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.82])


                #seq_9_083 = []
                if seq_9_083:
                        mydata = [seq_9_083]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_083.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.83])

                #seq_9_084 = []
                if seq_9_084:
                        mydata = [seq_9_084]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_084.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.84])

                #seq_9_085 = []
                if seq_9_085:
                        mydata = [seq_9_085]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_085.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.85])

                #seq_9_086 = []
                if seq_9_086:
                        mydata = [seq_9_086]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_086.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.86])

                #seq_9_087 = []
                if seq_9_087:
                        mydata = [seq_9_087]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_087.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.87])

                #seq_9_088 = []
                if seq_9_088:
                        mydata = [seq_9_088]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_088.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.88])

                #seq_9_089 = []
                if seq_9_089:
                        mydata = [seq_9_089]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_089.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.89])

                #seq_9_090 = []
                if seq_9_090:
                        mydata = [seq_9_090]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm	= hmms.DtHMM.from_file( path + "seq_9_090.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.90])

                #seq_9_091 = []
                if seq_9_091:
                        mydata = [seq_9_091]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_091.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.91])

                #seq_9_240 = []
                if seq_9_240:
                        mydata = [seq_9_240]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_240.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.40])

                #seq_9_241 = []
                if seq_9_241:
                        mydata = [seq_9_241]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_241.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.41])

                #seq_9_242 = []
                if seq_9_242:
                        mydata = [seq_9_242]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_242.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.42])

                #seq_9_243 = []
                if seq_9_243:
                        mydata = [seq_9_243]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_243.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.43])

                #seq_9_244 = []
                if seq_9_244:
                        mydata = [seq_9_244]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_244.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.44])

                #seq_9_245 = []
                if seq_9_245:
                        mydata = [seq_9_245]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_245.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.45])

                #seq_9_246 = []
                if seq_9_246:
                        mydata = [seq_9_246]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_246.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.46])

                #seq_9_247 = []
                if seq_9_247:
                        mydata = [seq_9_247]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_247.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.47])

                #seq_9_248 = []
                if seq_9_248:
                        mydata = [seq_9_248]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_248.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.48])

                #seq_9_249 = []
                if seq_9_249:
                        mydata = [seq_9_249]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_249.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.49])

                #seq_9_571 = []
                if seq_9_571:
                        mydata = [seq_9_571]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_571.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.71])

                #seq_9_572 = []
                if seq_9_572:
                        mydata = [seq_9_572]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_572.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.72])

                #seq_9_573 = []
                if seq_9_573:
                        mydata = [seq_9_573]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_573.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.73])

                #seq_9_574 = []
                if seq_9_574:
                        mydata = [seq_9_574]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_574.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.74])

                #seq_9_575 = []
                if seq_9_575:
                        mydata = [seq_9_575]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_575.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.75])

                #seq_9_576 = []
                if seq_9_576:
                        mydata = [seq_9_576]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_576.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.76])

                #seq_9_577 = []
                if seq_9_577:
                        mydata = [seq_9_577]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_577.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.77])

                #seq_9_578 = []
                if seq_9_578:
                        mydata = [seq_9_578]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_578.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.78])

                #seq_9_579 = []
                if seq_9_579:
                        mydata = [seq_9_579]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_579.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.79])

                #seq_9_580 = []
                if seq_9_580:
                        mydata = [seq_9_580]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_580.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.80])

                #seq_9_581 = []
                if seq_9_581:
                        mydata = [seq_9_581]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_581.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.81])

                #seq_9_582 = []
                if seq_9_582:
                        mydata = [seq_9_582]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_582.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.82])

                #seq_9_583 = []
                if seq_9_583:
                        mydata = [seq_9_583]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_583.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.83])

                #seq_9_584 = []
                if seq_9_584:
                        mydata = [seq_9_584]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_584.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.84])

                #seq_9_585 = []
                if seq_9_585:
                        mydata = [seq_9_585]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_585.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.85])

                #seq_9_586 = []
                if seq_9_586:
                        mydata = [seq_9_586]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_586.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.86])

                #seq_9_587 = []
                if seq_9_587:
                        mydata = [seq_9_587]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_9_587.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.87])

                #seq_10_08 = []
                if seq_10_08:
                        mydata = [seq_10_08]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_08.npz" ) #load model from file
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.8])

                #seq_10_081 = []
                if seq_10_081:
                        mydata = [seq_10_081]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_081.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.81])

                #seq_10_082 = []
                if seq_10_082:
                        mydata = [seq_10_082]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_082.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.82])


                #seq_10_083 = []
                if seq_10_083:
                        mydata = [seq_10_083]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_083.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.83])

                #seq_10_084 = []
                if seq_10_084:
                        mydata = [seq_10_084]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_084.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.84])

                #seq_10_085 = []
                if seq_10_085:
                        mydata = [seq_10_085]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_085.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.85])

                #seq_10_086 = []
                if seq_10_086:
                        mydata = [seq_10_086]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_086.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.86])

                #seq_10_087 = []
                if seq_10_087:
                        mydata = [seq_10_087]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_087.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.87])

                #seq_10_088 = []
                if seq_10_088:
                        mydata = [seq_10_088]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_088.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.88])

                #seq_10_089 = []
                if seq_10_089:
                        mydata = [seq_10_089]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_089.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.89])

                #seq_10_090 = []
                if seq_10_090:
                        mydata = [seq_10_090]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm	= hmms.DtHMM.from_file( path + "seq_10_090.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.90])

                #seq_10_091 = []
                if seq_10_091:
                        mydata = [seq_10_091]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_091.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.91])

                #seq_10_240 = []
                if seq_10_240:
                        mydata = [seq_10_240]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_240.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.40])

                #seq_10_241 = []
                if seq_10_241:
                        mydata = [seq_10_241]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_241.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.41])

                #seq_10_242 = []
                if seq_10_242:
                        mydata = [seq_10_242]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_242.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.42])

                #seq_10_243 = []
                if seq_10_243:
                        mydata = [seq_10_243]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_243.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.43])

                #seq_10_244 = []
                if seq_10_244:
                        mydata = [seq_10_244]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_244.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.44])

                #seq_10_245 = []
                if seq_10_245:
                        mydata = [seq_10_245]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_245.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.45])

                #seq_10_246 = []
                if seq_10_246:
                        mydata = [seq_10_246]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_246.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.46])

                #seq_10_247 = []
                if seq_10_247:
                        mydata = [seq_10_247]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_247.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.47])

                #seq_10_248 = []
                if seq_10_248:
                        mydata = [seq_10_248]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_248.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.48])

                #seq_10_249 = []
                if seq_10_249:
                        mydata = [seq_10_249]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_249.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.49])

                #seq_10_571 = []
                if seq_10_571:
                        mydata = [seq_10_571]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_571.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.71])

                #seq_10_572 = []
                if seq_10_572:
                        mydata = [seq_10_572]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_572.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.72])

                #seq_10_573 = []
                if seq_10_573:
                        mydata = [seq_10_573]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_573.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.73])

                #seq_10_574 = []
                if seq_10_574:
                        mydata = [seq_10_574]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_574.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.74])

                #seq_10_575 = []
                if seq_10_575:
                        mydata = [seq_10_575]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_575.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.75])

                #seq_10_576 = []
                if seq_10_576:
                        mydata = [seq_10_576]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_576.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.76])

                #seq_10_577 = []
                if seq_10_577:
                        mydata = [seq_10_577]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_577.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.77])

                #seq_10_578 = []
                if seq_10_578:
                        mydata = [seq_10_578]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_578.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.78])

                #seq_10_579 = []
                if seq_10_579:
                        mydata = [seq_10_579]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_579.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.79])

                #seq_10_580 = []
                if seq_10_580:
                        mydata = [seq_10_580]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_580.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.80])

                #seq_10_581 = []
                if seq_10_581:
                        mydata = [seq_10_581]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_581.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.81])

                #seq_10_582 = []
                if seq_10_582:
                        mydata = [seq_10_582]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_582.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.82])

                #seq_10_583 = []
                if seq_10_583:
                        mydata = [seq_10_583]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_583.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.83])

                #seq_10_584 = []
                if seq_10_584:
                        mydata = [seq_10_584]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_584.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.84])

                #seq_10_585 = []
                if seq_10_585:
                        mydata = [seq_10_585]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_585.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.85])

                #seq_10_586 = []
                if seq_10_586:
                        mydata = [seq_10_586]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_586.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.86])

                #seq_10_587 = []
                if seq_10_587:
                        mydata = [seq_10_587]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_10_587.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.87])

                #seq_11_08 = []
                if seq_11_08:
                        mydata = [seq_11_08]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_08.npz" ) #load model from file
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.8])

                #seq_11_081 = []
                if seq_11_081:
                        mydata = [seq_11_081]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_081.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.81])

                #seq_11_082 = []
                if seq_11_082:
                        mydata = [seq_11_082]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_082.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.82])


                #seq_11_083 = []
                if seq_11_083:
                        mydata = [seq_11_083]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_083.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.83])

                #seq_11_084 = []
                if seq_11_084:
                        mydata = [seq_11_084]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_084.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.84])

                #seq_11_085 = []
                if seq_11_085:
                        mydata = [seq_11_085]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_085.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.85])

                #seq_11_086 = []
                if seq_11_086:
                        mydata = [seq_11_086]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_086.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.86])

                #seq_11_087 = []
                if seq_11_087:
                        mydata = [seq_11_087]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_087.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.87])

                #seq_11_088 = []
                if seq_11_088:
                        mydata = [seq_11_088]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_088.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.88])

                #seq_11_089 = []
                if seq_11_089:
                        mydata = [seq_11_089]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_089.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.89])

                #seq_11_090 = []
                if seq_11_090:
                        mydata = [seq_11_090]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm	= hmms.DtHMM.from_file( path + "seq_11_090.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.90])

                #seq_11_091 = []
                if seq_11_091:
                        mydata = [seq_11_091]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_091.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.91])

                #seq_11_240 = []
                if seq_11_240:
                        mydata = [seq_11_240]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_240.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.40])

                #seq_11_241 = []
                if seq_11_241:
                        mydata = [seq_11_241]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_241.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.41])

                #seq_11_242 = []
                if seq_11_242:
                        mydata = [seq_11_242]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_242.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.42])

                #seq_11_243 = []
                if seq_11_243:
                        mydata = [seq_11_243]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_243.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.43])

                #seq_11_244 = []
                if seq_11_244:
                        mydata = [seq_11_244]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_244.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.44])

                #seq_11_245 = []
                if seq_11_245:
                        mydata = [seq_11_245]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_245.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.45])

                #seq_11_246 = []
                if seq_11_246:
                        mydata = [seq_11_246]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_246.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.46])

                #seq_11_247 = []
                if seq_11_247:
                        mydata = [seq_11_247]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_247.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.47])

                #seq_11_248 = []
                if seq_11_248:
                        mydata = [seq_11_248]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_248.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.48])

                #seq_11_249 = []
                if seq_11_249:
                        mydata = [seq_11_249]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_249.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.49])

                #seq_11_571 = []
                if seq_11_571:
                        mydata = [seq_11_571]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_571.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.71])

                #seq_11_572 = []
                if seq_11_572:
                        mydata = [seq_11_572]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_572.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.72])

                #seq_11_573 = []
                if seq_11_573:
                        mydata = [seq_11_573]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_573.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.73])

                #seq_11_574 = []
                if seq_11_574:
                        mydata = [seq_11_574]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_574.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.74])

                #seq_11_575 = []
                if seq_11_575:
                        mydata = [seq_11_575]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_575.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.75])

                #seq_11_576 = []
                if seq_11_576:
                        mydata = [seq_11_576]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_576.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.76])

                #seq_11_577 = []
                if seq_11_577:
                        mydata = [seq_11_577]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_577.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.77])

                #seq_11_578 = []
                if seq_11_578:
                        mydata = [seq_11_578]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_578.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.78])

                #seq_11_579 = []
                if seq_11_579:
                        mydata = [seq_11_579]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_579.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.79])

                #seq_11_580 = []
                if seq_11_580:
                        mydata = [seq_11_580]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_580.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.80])

                #seq_11_581 = []
                if seq_11_581:
                        mydata = [seq_11_581]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_581.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.81])

                #seq_11_582 = []
                if seq_11_582:
                        mydata = [seq_11_582]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_582.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.82])

                #seq_11_583 = []
                if seq_11_583:
                        mydata = [seq_11_583]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_583.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.83])

                #seq_11_584 = []
                if seq_11_584:
                        mydata = [seq_11_584]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_584.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.84])

                #seq_11_585 = []
                if seq_11_585:
                        mydata = [seq_11_585]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_585.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.85])

                #seq_11_586 = []
                if seq_11_586:
                        mydata = [seq_11_586]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_586.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.86])

                #seq_11_587 = []
                if seq_11_587:
                        mydata = [seq_11_587]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_11_587.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.87])

                #seq_12_08 = []
                if seq_12_08:
                        mydata = [seq_12_08]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_08.npz" ) #load model from file
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.8])

                #seq_12_081 = []
                if seq_12_081:
                        mydata = [seq_12_081]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_081.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.81])

                #seq_12_082 = []
                if seq_12_082:
                        mydata = [seq_12_082]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_082.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.82])


                #seq_12_083 = []
                if seq_12_083:
                        mydata = [seq_12_083]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_083.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.83])

                #seq_12_084 = []
                if seq_12_084:
                        mydata = [seq_12_084]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_084.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.84])

                #seq_12_085 = []
                if seq_12_085:
                        mydata = [seq_12_085]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_085.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.85])

                #seq_12_086 = []
                if seq_12_086:
                        mydata = [seq_12_086]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_086.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.86])

                #seq_12_087 = []
                if seq_12_087:
                        mydata = [seq_12_087]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_087.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.87])

                #seq_12_088 = []
                if seq_12_088:
                        mydata = [seq_12_088]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_088.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.88])

                #seq_12_089 = []
                if seq_12_089:
                        mydata = [seq_12_089]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_089.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.89])

                #seq_12_090 = []
                if seq_12_090:
                        mydata = [seq_12_090]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm	= hmms.DtHMM.from_file( path + "seq_12_090.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.90])

                #seq_12_091 = []
                if seq_12_091:
                        mydata = [seq_12_091]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_091.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.91])

                #seq_12_240 = []
                if seq_12_240:
                        mydata = [seq_12_240]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_240.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.40])

                #seq_12_241 = []
                if seq_12_241:
                        mydata = [seq_12_241]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_241.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.41])

                #seq_12_242 = []
                if seq_12_242:
                        mydata = [seq_12_242]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_242.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.42])

                #seq_12_243 = []
                if seq_12_243:
                        mydata = [seq_12_243]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_243.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.43])

                #seq_12_244 = []
                if seq_12_244:
                        mydata = [seq_12_244]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_244.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.44])

                #seq_12_245 = []
                if seq_12_245:
                        mydata = [seq_12_245]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_245.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.45])

                #seq_12_246 = []
                if seq_12_246:
                        mydata = [seq_12_246]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_246.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.46])

                #seq_12_247 = []
                if seq_12_247:
                        mydata = [seq_12_247]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_247.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.47])

                #seq_12_248 = []
                if seq_12_248:
                        mydata = [seq_12_248]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_248.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.48])

                #seq_12_249 = []
                if seq_12_249:
                        mydata = [seq_12_249]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_249.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.49])

                #seq_12_571 = []
                if seq_12_571:
                        mydata = [seq_12_571]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_571.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.71])

                #seq_12_572 = []
                if seq_12_572:
                        mydata = [seq_12_572]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_572.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.72])

                #seq_12_573 = []
                if seq_12_573:
                        mydata = [seq_12_573]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_573.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.73])

                #seq_12_574 = []
                if seq_12_574:
                        mydata = [seq_12_574]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_574.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.74])

                #seq_12_575 = []
                if seq_12_575:
                        mydata = [seq_12_575]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_575.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.75])

                #seq_12_576 = []
                if seq_12_576:
                        mydata = [seq_12_576]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_576.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.76])

                #seq_12_577 = []
                if seq_12_577:
                        mydata = [seq_12_577]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_577.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.77])

                #seq_12_578 = []
                if seq_12_578:
                        mydata = [seq_12_578]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_578.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.78])

                #seq_12_579 = []
                if seq_12_579:
                        mydata = [seq_12_579]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_579.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.79])

                #seq_12_580 = []
                if seq_12_580:
                        mydata = [seq_12_580]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_580.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.80])

                #seq_12_581 = []
                if seq_12_581:
                        mydata = [seq_12_581]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_581.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.81])

                #seq_12_582 = []
                if seq_12_582:
                        mydata = [seq_12_582]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_582.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.82])

                #seq_12_583 = []
                if seq_12_583:
                        mydata = [seq_12_583]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_583.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.83])

                #seq_12_584 = []
                if seq_12_584:
                        mydata = [seq_12_584]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_584.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.84])

                #seq_12_585 = []
                if seq_12_585:
                        mydata = [seq_12_585]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_585.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.85])

                #seq_12_586 = []
                if seq_12_586:
                        mydata = [seq_12_586]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_586.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.86])

                #seq_12_587 = []
                if seq_12_587:
                        mydata = [seq_12_587]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_12_587.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.87])

                #seq_13_08 = []
                if seq_13_08:
                        mydata = [seq_13_08]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_08.npz" ) #load model from file
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.8])

                #seq_13_081 = []
                if seq_13_081:
                        mydata = [seq_13_081]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_081.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.81])

                #seq_13_082 = []
                if seq_13_082:
                        mydata = [seq_13_082]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_082.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.82])


                #seq_13_083 = []
                if seq_13_083:
                        mydata = [seq_13_083]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_083.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.83])

                #seq_13_084 = []
                if seq_13_084:
                        mydata = [seq_13_084]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_084.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.84])

                #seq_13_085 = []
                if seq_13_085:
                        mydata = [seq_13_085]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_085.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.85])

                #seq_13_086 = []
                if seq_13_086:
                        mydata = [seq_13_086]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_086.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.86])

                #seq_13_087 = []
                if seq_13_087:
                        mydata = [seq_13_087]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_087.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.87])

                #seq_13_088 = []
                if seq_13_088:
                        mydata = [seq_13_088]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_088.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.88])

                #seq_13_089 = []
                if seq_13_089:
                        mydata = [seq_13_089]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_089.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.89])

                #seq_13_090 = []
                if seq_13_090:
                        mydata = [seq_13_090]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm	= hmms.DtHMM.from_file( path + "seq_13_090.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.90])

                #seq_13_091 = []
                if seq_13_091:
                        mydata = [seq_13_091]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_091.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.91])

                #seq_13_240 = []
                if seq_13_240:
                        mydata = [seq_13_240]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_240.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.40])

                #seq_13_241 = []
                if seq_13_241:
                        mydata = [seq_13_241]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_241.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.41])

                #seq_13_242 = []
                if seq_13_242:
                        mydata = [seq_13_242]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_242.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.42])

                #seq_13_243 = []
                if seq_13_243:
                        mydata = [seq_13_243]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_243.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.43])

                #seq_13_244 = []
                if seq_13_244:
                        mydata = [seq_13_244]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_244.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.44])

                #seq_13_245 = []
                if seq_13_245:
                        mydata = [seq_13_245]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_245.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.45])

                #seq_13_246 = []
                if seq_13_246:
                        mydata = [seq_13_246]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_246.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.46])

                #seq_13_247 = []
                if seq_13_247:
                        mydata = [seq_13_247]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_247.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.47])

                #seq_13_248 = []
                if seq_13_248:
                        mydata = [seq_13_248]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_248.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.48])

                #seq_13_249 = []
                if seq_13_249:
                        mydata = [seq_13_249]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_249.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.49])

                #seq_13_571 = []
                if seq_13_571:
                        mydata = [seq_13_571]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_571.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.71])

                #seq_13_572 = []
                if seq_13_572:
                        mydata = [seq_13_572]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_572.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.72])

                #seq_13_573 = []
                if seq_13_573:
                        mydata = [seq_13_573]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_573.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.73])

                #seq_13_574 = []
                if seq_13_574:
                        mydata = [seq_13_574]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_574.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.74])

                #seq_13_575 = []
                if seq_13_575:
                        mydata = [seq_13_575]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_575.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.75])

                #seq_13_576 = []
                if seq_13_576:
                        mydata = [seq_13_576]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_576.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.76])

                #seq_13_577 = []
                if seq_13_577:
                        mydata = [seq_13_577]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_577.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.77])

                #seq_13_578 = []
                if seq_13_578:
                        mydata = [seq_13_578]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_578.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.78])

                #seq_13_579 = []
                if seq_13_579:
                        mydata = [seq_13_579]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_579.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.79])

                #seq_13_580 = []
                if seq_13_580:
                        mydata = [seq_13_580]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_580.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.80])

                #seq_13_581 = []
                if seq_13_581:
                        mydata = [seq_13_581]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_581.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.81])

                #seq_13_582 = []
                if seq_13_582:
                        mydata = [seq_13_582]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_582.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.82])

                #seq_13_583 = []
                if seq_13_583:
                        mydata = [seq_13_583]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_583.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.83])

                #seq_13_584 = []
                if seq_13_584:
                        mydata = [seq_13_584]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_584.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.84])

                #seq_13_585 = []
                if seq_13_585:
                        mydata = [seq_13_585]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_585.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.85])

                #seq_13_586 = []
                if seq_13_586:
                        mydata = [seq_13_586]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_586.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.86])

                #seq_13_587 = []
                if seq_13_587:
                        mydata = [seq_13_587]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_13_587.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.87])

                #seq_14_08 = []
                if seq_14_08:
                        mydata = [seq_14_08]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_08.npz" ) #load model from file
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.8])

                #seq_14_081 = []
                if seq_14_081:
                        mydata = [seq_14_081]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_081.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.81])

                #seq_14_082 = []
                if seq_14_082:
                        mydata = [seq_14_082]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_082.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.82])


                #seq_14_083 = []
                if seq_14_083:
                        mydata = [seq_14_083]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_083.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.83])

                #seq_14_084 = []
                if seq_14_084:
                        mydata = [seq_14_084]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_084.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.84])

                #seq_14_085 = []
                if seq_14_085:
                        mydata = [seq_14_085]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_085.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.85])

                #seq_14_086 = []
                if seq_14_086:
                        mydata = [seq_14_086]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_086.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.86])

                #seq_14_087 = []
                if seq_14_087:
                        mydata = [seq_14_087]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_087.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.87])

                #seq_14_088 = []
                if seq_14_088:
                        mydata = [seq_14_088]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_088.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.88])

                #seq_14_089 = []
                if seq_14_089:
                        mydata = [seq_14_089]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_089.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.89])

                #seq_14_090 = []
                if seq_14_090:
                        mydata = [seq_14_090]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm	= hmms.DtHMM.from_file( path + "seq_14_090.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.90])

                #seq_14_091 = []
                if seq_14_091:
                        mydata = [seq_14_091]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_091.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.91])

                #seq_14_240 = []
                if seq_14_240:
                        mydata = [seq_14_240]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_240.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.40])

                #seq_14_241 = []
                if seq_14_241:
                        mydata = [seq_14_241]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_241.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.41])

                #seq_14_242 = []
                if seq_14_242:
                        mydata = [seq_14_242]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_242.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.42])

                #seq_14_243 = []
                if seq_14_243:
                        mydata = [seq_14_243]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_243.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.43])

                #seq_14_244 = []
                if seq_14_244:
                        mydata = [seq_14_244]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_244.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.44])

                #seq_14_245 = []
                if seq_14_245:
                        mydata = [seq_14_245]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_245.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.45])

                #seq_14_246 = []
                if seq_14_246:
                        mydata = [seq_14_246]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_246.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.46])

                #seq_14_247 = []
                if seq_14_247:
                        mydata = [seq_14_247]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_247.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.47])

                #seq_14_248 = []
                if seq_14_248:
                        mydata = [seq_14_248]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_248.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.48])

                #seq_14_249 = []
                if seq_14_249:
                        mydata = [seq_14_249]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_249.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.49])

                #seq_14_571 = []
                if seq_14_571:
                        mydata = [seq_14_571]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_571.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.71])

                #seq_14_572 = []
                if seq_14_572:
                        mydata = [seq_14_572]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_572.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.72])

                #seq_14_573 = []
                if seq_14_573:
                        mydata = [seq_14_573]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_573.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.73])

                #seq_14_574 = []
                if seq_14_574:
                        mydata = [seq_14_574]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_574.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.74])

                #seq_14_575 = []
                if seq_14_575:
                        mydata = [seq_14_575]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_575.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.75])

                #seq_14_576 = []
                if seq_14_576:
                        mydata = [seq_14_576]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_576.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.76])

                #seq_14_577 = []
                if seq_14_577:
                        mydata = [seq_14_577]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_577.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.77])

                #seq_14_578 = []
                if seq_14_578:
                        mydata = [seq_14_578]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_578.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.78])

                #seq_14_579 = []
                if seq_14_579:
                        mydata = [seq_14_579]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_579.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.79])

                #seq_14_580 = []
                if seq_14_580:
                        mydata = [seq_14_580]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_580.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.80])

                #seq_14_581 = []
                if seq_14_581:
                        mydata = [seq_14_581]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_581.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.81])

                #seq_14_582 = []
                if seq_14_582:
                        mydata = [seq_14_582]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_582.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.82])

                #seq_14_583 = []
                if seq_14_583:
                        mydata = [seq_14_583]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_583.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.83])

                #seq_14_584 = []
                if seq_14_584:
                        mydata = [seq_14_584]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_584.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.84])

                #seq_14_585 = []
                if seq_14_585:
                        mydata = [seq_14_585]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_585.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.85])

                #seq_14_586 = []
                if seq_14_586:
                        mydata = [seq_14_586]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_586.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.86])

                #seq_14_587 = []
                if seq_14_587:
                        mydata = [seq_14_587]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_14_587.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.87])

                #seq_15_08 = []
                if seq_15_08:
                        mydata = [seq_15_08]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_08.npz" ) #load model from file
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.8])

                #seq_15_081 = []
                if seq_15_081:
                        mydata = [seq_15_081]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_081.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.81])

                #seq_15_082 = []
                if seq_15_082:
                        mydata = [seq_15_082]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_082.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.82])


                #seq_15_083 = []
                if seq_15_083:
                        mydata = [seq_15_083]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_083.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.83])

                #seq_15_084 = []
                if seq_15_084:
                        mydata = [seq_15_084]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_084.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.84])

                #seq_15_085 = []
                if seq_15_085:
                        mydata = [seq_15_085]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_085.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.85])

                #seq_15_086 = []
                if seq_15_086:
                        mydata = [seq_15_086]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_086.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.86])

                #seq_15_087 = []
                if seq_15_087:
                        mydata = [seq_15_087]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_087.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.87])

                #seq_15_088 = []
                if seq_15_088:
                        mydata = [seq_15_088]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_088.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.88])

                #seq_15_089 = []
                if seq_15_089:
                        mydata = [seq_15_089]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_089.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.89])

                #seq_15_090 = []
                if seq_15_090:
                        mydata = [seq_15_090]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm	= hmms.DtHMM.from_file( path + "seq_15_090.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.90])

                #seq_15_091 = []
                if seq_15_091:
                        mydata = [seq_15_091]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_091.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.91])

                #seq_15_240 = []
                if seq_15_240:
                        mydata = [seq_15_240]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_240.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.40])

                #seq_15_241 = []
                if seq_15_241:
                        mydata = [seq_15_241]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_241.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.41])

                #seq_15_242 = []
                if seq_15_242:
                        mydata = [seq_15_242]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_242.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.42])

                #seq_15_243 = []
                if seq_15_243:
                        mydata = [seq_15_243]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_243.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.43])

                #seq_15_244 = []
                if seq_15_244:
                        mydata = [seq_15_244]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_244.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.44])

                #seq_15_245 = []
                if seq_15_245:
                        mydata = [seq_15_245]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_245.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.45])

                #seq_15_246 = []
                if seq_15_246:
                        mydata = [seq_15_246]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_246.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.46])

                #seq_15_247 = []
                if seq_15_247:
                        mydata = [seq_15_247]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_247.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.47])

                #seq_15_248 = []
                if seq_15_248:
                        mydata = [seq_15_248]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_248.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.48])

                #seq_15_249 = []
                if seq_15_249:
                        mydata = [seq_15_249]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_249.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.49])

                #seq_15_571 = []
                if seq_15_571:
                        mydata = [seq_15_571]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_571.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.71])

                #seq_15_572 = []
                if seq_15_572:
                        mydata = [seq_15_572]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_572.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.72])

                #seq_15_573 = []
                if seq_15_573:
                        mydata = [seq_15_573]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_573.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.73])

                #seq_15_574 = []
                if seq_15_574:
                        mydata = [seq_15_574]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_574.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.74])

                #seq_15_575 = []
                if seq_15_575:
                        mydata = [seq_15_575]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_575.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.75])

                #seq_15_576 = []
                if seq_15_576:
                        mydata = [seq_15_576]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_576.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.76])

                #seq_15_577 = []
                if seq_15_577:
                        mydata = [seq_15_577]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_577.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.77])

                #seq_15_578 = []
                if seq_15_578:
                        mydata = [seq_15_578]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_578.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.78])

                #seq_15_579 = []
                if seq_15_579:
                        mydata = [seq_15_579]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_579.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.79])

                #seq_15_580 = []
                if seq_15_580:
                        mydata = [seq_15_580]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_580.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.80])

                #seq_15_581 = []
                if seq_15_581:
                        mydata = [seq_15_581]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_581.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.81])

                #seq_15_582 = []
                if seq_15_582:
                        mydata = [seq_15_582]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_582.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.82])

                #seq_15_583 = []
                if seq_15_583:
                        mydata = [seq_15_583]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_583.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.83])

                #seq_15_584 = []
                if seq_15_584:
                        mydata = [seq_15_584]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_584.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.84])

                #seq_15_585 = []
                if seq_15_585:
                        mydata = [seq_15_585]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_585.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.85])

                #seq_15_586 = []
                if seq_15_586:
                        mydata = [seq_15_586]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_586.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.86])

                #seq_15_587 = []
                if seq_15_587:
                        mydata = [seq_15_587]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_15_587.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.87])

                #seq_16_08 = []
                if seq_16_08:
                        mydata = [seq_16_08]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_08.npz" ) #load model from file
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.8])

                #seq_16_081 = []
                if seq_16_081:
                        mydata = [seq_16_081]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_081.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.81])

                #seq_16_082 = []
                if seq_16_082:
                        mydata = [seq_16_082]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_082.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.82])


                #seq_16_083 = []
                if seq_16_083:
                        mydata = [seq_16_083]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_083.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.83])

                #seq_16_084 = []
                if seq_16_084:
                        mydata = [seq_16_084]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_084.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.84])

                #seq_16_085 = []
                if seq_16_085:
                        mydata = [seq_16_085]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_085.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.85])

                #seq_16_086 = []
                if seq_16_086:
                        mydata = [seq_16_086]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_086.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.86])

                #seq_16_087 = []
                if seq_16_087:
                        mydata = [seq_16_087]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_087.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.87])

                #seq_16_088 = []
                if seq_16_088:
                        mydata = [seq_16_088]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_088.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.88])

                #seq_16_089 = []
                if seq_16_089:
                        mydata = [seq_16_089]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_089.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.89])

                #seq_16_090 = []
                if seq_16_090:
                        mydata = [seq_16_090]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm	= hmms.DtHMM.from_file( path + "seq_16_090.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.90])

                #seq_16_091 = []
                if seq_16_091:
                        mydata = [seq_16_091]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_091.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.91])

                #seq_16_240 = []
                if seq_16_240:
                        mydata = [seq_16_240]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_240.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.40])

                #seq_16_241 = []
                if seq_16_241:
                        mydata = [seq_16_241]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_241.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.41])

                #seq_16_242 = []
                if seq_16_242:
                        mydata = [seq_16_242]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_242.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.42])

                #seq_16_243 = []
                if seq_16_243:
                        mydata = [seq_16_243]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_243.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.43])

                #seq_16_244 = []
                if seq_16_244:
                        mydata = [seq_16_244]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_244.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.44])

                #seq_16_245 = []
                if seq_16_245:
                        mydata = [seq_16_245]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_245.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.45])

                #seq_16_246 = []
                if seq_16_246:
                        mydata = [seq_16_246]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_246.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.46])

                #seq_16_247 = []
                if seq_16_247:
                        mydata = [seq_16_247]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_247.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.47])

                #seq_16_248 = []
                if seq_16_248:
                        mydata = [seq_16_248]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_248.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.48])

                #seq_16_249 = []
                if seq_16_249:
                        mydata = [seq_16_249]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_249.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.49])

                #seq_16_571 = []
                if seq_16_571:
                        mydata = [seq_16_571]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_571.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.71])

                #seq_16_572 = []
                if seq_16_572:
                        mydata = [seq_16_572]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_572.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.72])

                #seq_16_573 = []
                if seq_16_573:
                        mydata = [seq_16_573]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_573.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.73])

                #seq_16_574 = []
                if seq_16_574:
                        mydata = [seq_16_574]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_574.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.74])

                #seq_16_575 = []
                if seq_16_575:
                        mydata = [seq_16_575]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_575.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.75])

                #seq_16_576 = []
                if seq_16_576:
                        mydata = [seq_16_576]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_576.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.76])

                #seq_16_577 = []
                if seq_16_577:
                        mydata = [seq_16_577]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_577.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.77])

                #seq_16_578 = []
                if seq_16_578:
                        mydata = [seq_16_578]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_578.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.78])

                #seq_16_579 = []
                if seq_16_579:
                        mydata = [seq_16_579]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_579.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.79])

                #seq_16_580 = []
                if seq_16_580:
                        mydata = [seq_16_580]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_580.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.80])

                #seq_16_581 = []
                if seq_16_581:
                        mydata = [seq_16_581]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_581.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.81])

                #seq_16_582 = []
                if seq_16_582:
                        mydata = [seq_16_582]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_582.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.82])

                #seq_16_583 = []
                if seq_16_583:
                        mydata = [seq_16_583]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_583.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.83])

                #seq_16_584 = []
                if seq_16_584:
                        mydata = [seq_16_584]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_584.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.84])

                #seq_16_585 = []
                if seq_16_585:
                        mydata = [seq_16_585]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_585.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.85])

                #seq_16_586 = []
                if seq_16_586:
                        mydata = [seq_16_586]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_586.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.86])

                #seq_16_587 = []
                if seq_16_587:
                        mydata = [seq_16_587]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_16_587.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.87])

                #seq_17_08 = []
                if seq_17_08:
                        mydata = [seq_17_08]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_08.npz" ) #load model from file
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.8])

                #seq_17_081 = []
                if seq_17_081:
                        mydata = [seq_17_081]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_081.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.81])

                #seq_17_082 = []
                if seq_17_082:
                        mydata = [seq_17_082]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_082.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.82])


                #seq_17_083 = []
                if seq_17_083:
                        mydata = [seq_17_083]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_083.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.83])

                #seq_17_084 = []
                if seq_17_084:
                        mydata = [seq_17_084]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_084.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.84])

                #seq_17_085 = []
                if seq_17_085:
                        mydata = [seq_17_085]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_085.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.85])

                #seq_17_086 = []
                if seq_17_086:
                        mydata = [seq_17_086]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_086.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.86])

                #seq_17_087 = []
                if seq_17_087:
                        mydata = [seq_17_087]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_087.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.87])

                #seq_17_088 = []
                if seq_17_088:
                        mydata = [seq_17_088]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_088.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.88])

                #seq_17_089 = []
                if seq_17_089:
                        mydata = [seq_17_089]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_089.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.89])

                #seq_17_090 = []
                if seq_17_090:
                        mydata = [seq_17_090]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm	= hmms.DtHMM.from_file( path + "seq_17_090.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.90])

                #seq_17_091 = []
                if seq_17_091:
                        mydata = [seq_17_091]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_091.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.91])

                #seq_17_240 = []
                if seq_17_240:
                        mydata = [seq_17_240]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_240.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.40])

                #seq_17_241 = []
                if seq_17_241:
                        mydata = [seq_17_241]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_241.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.41])

                #seq_17_242 = []
                if seq_17_242:
                        mydata = [seq_17_242]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_242.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.42])

                #seq_17_243 = []
                if seq_17_243:
                        mydata = [seq_17_243]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_243.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.43])

                #seq_17_244 = []
                if seq_17_244:
                        mydata = [seq_17_244]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_244.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.44])

                #seq_17_245 = []
                if seq_17_245:
                        mydata = [seq_17_245]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_245.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.45])

                #seq_17_246 = []
                if seq_17_246:
                        mydata = [seq_17_246]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_246.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.46])

                #seq_17_247 = []
                if seq_17_247:
                        mydata = [seq_17_247]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_247.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.47])

                #seq_17_248 = []
                if seq_17_248:
                        mydata = [seq_17_248]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_248.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.48])

                #seq_17_249 = []
                if seq_17_249:
                        mydata = [seq_17_249]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_249.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.49])

                #seq_17_571 = []
                if seq_17_571:
                        mydata = [seq_17_571]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_571.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.71])

                #seq_17_572 = []
                if seq_17_572:
                        mydata = [seq_17_572]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_572.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.72])

                #seq_17_573 = []
                if seq_17_573:
                        mydata = [seq_17_573]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_573.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.73])

                #seq_17_574 = []
                if seq_17_574:
                        mydata = [seq_17_574]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_574.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.74])

                #seq_17_575 = []
                if seq_17_575:
                        mydata = [seq_17_575]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_575.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.75])

                #seq_17_576 = []
                if seq_17_576:
                        mydata = [seq_17_576]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_576.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.76])

                #seq_17_577 = []
                if seq_17_577:
                        mydata = [seq_17_577]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_577.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.77])

                #seq_17_578 = []
                if seq_17_578:
                        mydata = [seq_17_578]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_578.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.78])

                #seq_17_579 = []
                if seq_17_579:
                        mydata = [seq_17_579]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_579.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.79])

                #seq_17_580 = []
                if seq_17_580:
                        mydata = [seq_17_580]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_580.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.80])

                #seq_17_581 = []
                if seq_17_581:
                        mydata = [seq_17_581]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_581.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.81])

                #seq_17_582 = []
                if seq_17_582:
                        mydata = [seq_17_582]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_582.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.82])

                #seq_17_583 = []
                if seq_17_583:
                        mydata = [seq_17_583]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_583.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.83])

                #seq_17_584 = []
                if seq_17_584:
                        mydata = [seq_17_584]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_584.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.84])

                #seq_17_585 = []
                if seq_17_585:
                        mydata = [seq_17_585]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_585.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.85])

                #seq_17_586 = []
                if seq_17_586:
                        mydata = [seq_17_586]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_586.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.86])

                #seq_17_587 = []
                if seq_17_587:
                        mydata = [seq_17_587]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_17_587.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.87])

                #seq_18_08 = []
                if seq_18_08:
                        mydata = [seq_18_08]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_08.npz" ) #load model from file
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.8])

                #seq_18_081 = []
                if seq_18_081:
                        mydata = [seq_18_081]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_081.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.81])

                #seq_18_082 = []
                if seq_18_082:
                        mydata = [seq_18_082]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_082.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.82])


                #seq_18_083 = []
                if seq_18_083:
                        mydata = [seq_18_083]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_083.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.83])

                #seq_18_084 = []
                if seq_18_084:
                        mydata = [seq_18_084]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_084.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.84])

                #seq_18_085 = []
                if seq_18_085:
                        mydata = [seq_18_085]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_085.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.85])

                #seq_18_086 = []
                if seq_18_086:
                        mydata = [seq_18_086]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_086.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.86])

                #seq_18_087 = []
                if seq_18_087:
                        mydata = [seq_18_087]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_087.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.87])

                #seq_18_088 = []
                if seq_18_088:
                        mydata = [seq_18_088]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_088.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.88])

                #seq_18_089 = []
                if seq_18_089:
                        mydata = [seq_18_089]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_089.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.89])

                #seq_18_090 = []
                if seq_18_090:
                        mydata = [seq_18_090]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm	= hmms.DtHMM.from_file( path + "seq_18_090.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.90])

                #seq_18_091 = []
                if seq_18_091:
                        mydata = [seq_18_091]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_091.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.91])

                #seq_18_240 = []
                if seq_18_240:
                        mydata = [seq_18_240]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_240.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.40])

                #seq_18_241 = []
                if seq_18_241:
                        mydata = [seq_18_241]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_241.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.41])

                #seq_18_242 = []
                if seq_18_242:
                        mydata = [seq_18_242]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_242.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.42])

                #seq_18_243 = []
                if seq_18_243:
                        mydata = [seq_18_243]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_243.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.43])

                #seq_18_244 = []
                if seq_18_244:
                        mydata = [seq_18_244]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_244.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.44])

                #seq_18_245 = []
                if seq_18_245:
                        mydata = [seq_18_245]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_245.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.45])

                #seq_18_246 = []
                if seq_18_246:
                        mydata = [seq_18_246]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_246.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.46])

                #seq_18_247 = []
                if seq_18_247:
                        mydata = [seq_18_247]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_247.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.47])

                #seq_18_248 = []
                if seq_18_248:
                        mydata = [seq_18_248]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_248.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.48])

                #seq_18_249 = []
                if seq_18_249:
                        mydata = [seq_18_249]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_249.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.49])

                #seq_18_571 = []
                if seq_18_571:
                        mydata = [seq_18_571]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_571.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.71])

                #seq_18_572 = []
                if seq_18_572:
                        mydata = [seq_18_572]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_572.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.72])

                #seq_18_573 = []
                if seq_18_573:
                        mydata = [seq_18_573]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_573.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.73])

                #seq_18_574 = []
                if seq_18_574:
                        mydata = [seq_18_574]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_574.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.74])

                #seq_18_575 = []
                if seq_18_575:
                        mydata = [seq_18_575]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_575.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.75])

                #seq_18_576 = []
                if seq_18_576:
                        mydata = [seq_18_576]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_576.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.76])

                #seq_18_577 = []
                if seq_18_577:
                        mydata = [seq_18_577]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_577.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.77])

                #seq_18_578 = []
                if seq_18_578:
                        mydata = [seq_18_578]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_578.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.78])

                #seq_18_579 = []
                if seq_18_579:
                        mydata = [seq_18_579]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_579.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.79])

                #seq_18_580 = []
                if seq_18_580:
                        mydata = [seq_18_580]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_580.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.80])

                #seq_18_581 = []
                if seq_18_581:
                        mydata = [seq_18_581]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_581.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.81])

                #seq_18_582 = []
                if seq_18_582:
                        mydata = [seq_18_582]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_582.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.82])

                #seq_18_583 = []
                if seq_18_583:
                        mydata = [seq_18_583]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_583.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.83])

                #seq_18_584 = []
                if seq_18_584:
                        mydata = [seq_18_584]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_584.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.84])

                #seq_18_585 = []
                if seq_18_585:
                        mydata = [seq_18_585]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_585.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.85])

                #seq_18_586 = []
                if seq_18_586:
                        mydata = [seq_18_586]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_586.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.86])

                #seq_18_587 = []
                if seq_18_587:
                        mydata = [seq_18_587]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_18_587.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.87])

                #seq_19_08 = []
                if seq_19_08:
                        mydata = [seq_19_08]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_08.npz" ) #load model from file
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.8])

                #seq_19_081 = []
                if seq_19_081:
                        mydata = [seq_19_081]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_081.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.81])

                #seq_19_082 = []
                if seq_19_082:
                        mydata = [seq_19_082]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_082.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.82])


                #seq_19_083 = []
                if seq_19_083:
                        mydata = [seq_19_083]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_083.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.83])

                #seq_19_084 = []
                if seq_19_084:
                        mydata = [seq_19_084]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_084.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.84])

                #seq_19_085 = []
                if seq_19_085:
                        mydata = [seq_19_085]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_085.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.85])

                #seq_19_086 = []
                if seq_19_086:
                        mydata = [seq_19_086]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_086.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.86])

                #seq_19_087 = []
                if seq_19_087:
                        mydata = [seq_19_087]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_087.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.87])

                #seq_19_088 = []
                if seq_19_088:
                        mydata = [seq_19_088]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_088.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.88])

                #seq_19_089 = []
                if seq_19_089:
                        mydata = [seq_19_089]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_089.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.89])

                #seq_19_090 = []
                if seq_19_090:
                        mydata = [seq_19_090]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm	= hmms.DtHMM.from_file( path + "seq_19_090.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.90])

                #seq_19_091 = []
                if seq_19_091:
                        mydata = [seq_19_091]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_091.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.91])

                #seq_19_240 = []
                if seq_19_240:
                        mydata = [seq_19_240]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_240.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.40])

                #seq_19_241 = []
                if seq_19_241:
                        mydata = [seq_19_241]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_241.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.41])

                #seq_19_242 = []
                if seq_19_242:
                        mydata = [seq_19_242]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_242.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.42])

                #seq_19_243 = []
                if seq_19_243:
                        mydata = [seq_19_243]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_243.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.43])

                #seq_19_244 = []
                if seq_19_244:
                        mydata = [seq_19_244]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_244.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.44])

                #seq_19_245 = []
                if seq_19_245:
                        mydata = [seq_19_245]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_245.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.45])

                #seq_19_246 = []
                if seq_19_246:
                        mydata = [seq_19_246]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_246.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.46])

                #seq_19_247 = []
                if seq_19_247:
                        mydata = [seq_19_247]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_247.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.47])

                #seq_19_248 = []
                if seq_19_248:
                        mydata = [seq_19_248]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_248.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.48])

                #seq_19_249 = []
                if seq_19_249:
                        mydata = [seq_19_249]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_249.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.49])

                #seq_19_571 = []
                if seq_19_571:
                        mydata = [seq_19_571]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_571.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.71])

                #seq_19_572 = []
                if seq_19_572:
                        mydata = [seq_19_572]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_572.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.72])

                #seq_19_573 = []
                if seq_19_573:
                        mydata = [seq_19_573]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_573.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.73])

                #seq_19_574 = []
                if seq_19_574:
                        mydata = [seq_19_574]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_574.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.74])

                #seq_19_575 = []
                if seq_19_575:
                        mydata = [seq_19_575]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_575.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.75])

                #seq_19_576 = []
                if seq_19_576:
                        mydata = [seq_19_576]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_576.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.76])

                #seq_19_577 = []
                if seq_19_577:
                        mydata = [seq_19_577]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_577.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.77])

                #seq_19_578 = []
                if seq_19_578:
                        mydata = [seq_19_578]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_578.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.78])

                #seq_19_579 = []
                if seq_19_579:
                        mydata = [seq_19_579]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_579.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.79])

                #seq_19_580 = []
                if seq_19_580:
                        mydata = [seq_19_580]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_580.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.80])

                #seq_19_581 = []
                if seq_19_581:
                        mydata = [seq_19_581]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_581.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.81])

                #seq_19_582 = []
                if seq_19_582:
                        mydata = [seq_19_582]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_582.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.82])

                #seq_19_583 = []
                if seq_19_583:
                        mydata = [seq_19_583]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_583.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.83])

                #seq_19_584 = []
                if seq_19_584:
                        mydata = [seq_19_584]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_584.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.84])

                #seq_19_585 = []
                if seq_19_585:
                        mydata = [seq_19_585]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_585.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.85])

                #seq_19_586 = []
                if seq_19_586:
                        mydata = [seq_19_586]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_586.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.86])

                #seq_19_587 = []
                if seq_19_587:
                        mydata = [seq_19_587]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_19_587.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.87])

                #seq_20_08 = []
                if seq_20_08:
                        mydata = [seq_20_08]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_08.npz" ) #load model from file
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.8])

                #seq_20_081 = []
                if seq_20_081:
                        mydata = [seq_20_081]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_081.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.81])

                #seq_20_082 = []
                if seq_20_082:
                        mydata = [seq_20_082]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_082.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.82])


                #seq_20_083 = []
                if seq_20_083:
                        mydata = [seq_20_083]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_083.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.83])

                #seq_20_084 = []
                if seq_20_084:
                        mydata = [seq_20_084]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_084.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.84])

                #seq_20_085 = []
                if seq_20_085:
                        mydata = [seq_20_085]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_085.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.85])

                #seq_20_086 = []
                if seq_20_086:
                        mydata = [seq_20_086]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_086.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.86])

                #seq_20_087 = []
                if seq_20_087:
                        mydata = [seq_20_087]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_087.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.87])

                #seq_20_088 = []
                if seq_20_088:
                        mydata = [seq_20_088]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_088.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.88])

                #seq_20_089 = []
                if seq_20_089:
                        mydata = [seq_20_089]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_089.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.89])

                #seq_20_090 = []
                if seq_20_090:
                        mydata = [seq_20_090]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm	= hmms.DtHMM.from_file( path + "seq_20_090.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.90])

                #seq_20_091 = []
                if seq_20_091:
                        mydata = [seq_20_091]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_091.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.91])

                #seq_20_240 = []
                if seq_20_240:
                        mydata = [seq_20_240]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_240.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.40])

                #seq_20_241 = []
                if seq_20_241:
                        mydata = [seq_20_241]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_241.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.41])

                #seq_20_242 = []
                if seq_20_242:
                        mydata = [seq_20_242]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_242.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.42])

                #seq_20_243 = []
                if seq_20_243:
                        mydata = [seq_20_243]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_243.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.43])

                #seq_20_244 = []
                if seq_20_244:
                        mydata = [seq_20_244]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_244.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.44])

                #seq_20_245 = []
                if seq_20_245:
                        mydata = [seq_20_245]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_245.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.45])

                #seq_20_246 = []
                if seq_20_246:
                        mydata = [seq_20_246]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_246.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.46])

                #seq_20_247 = []
                if seq_20_247:
                        mydata = [seq_20_247]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_247.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.47])

                #seq_20_248 = []
                if seq_20_248:
                        mydata = [seq_20_248]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_248.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.48])

                #seq_20_249 = []
                if seq_20_249:
                        mydata = [seq_20_249]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_249.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.49])

                #seq_20_571 = []
                if seq_20_571:
                        mydata = [seq_20_571]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_571.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.71])

                #seq_20_572 = []
                if seq_20_572:
                        mydata = [seq_20_572]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_572.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.72])

                #seq_20_573 = []
                if seq_20_573:
                        mydata = [seq_20_573]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_573.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.73])

                #seq_20_574 = []
                if seq_20_574:
                        mydata = [seq_20_574]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_574.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.74])

                #seq_20_575 = []
                if seq_20_575:
                        mydata = [seq_20_575]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_575.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.75])

                #seq_20_576 = []
                if seq_20_576:
                        mydata = [seq_20_576]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_576.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.76])

                #seq_20_577 = []
                if seq_20_577:
                        mydata = [seq_20_577]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_577.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.77])

                #seq_20_578 = []
                if seq_20_578:
                        mydata = [seq_20_578]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_578.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.78])

                #seq_20_579 = []
                if seq_20_579:
                        mydata = [seq_20_579]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_579.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.79])

                #seq_20_580 = []
                if seq_20_580:
                        mydata = [seq_20_580]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_580.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.80])

                #seq_20_581 = []
                if seq_20_581:
                        mydata = [seq_20_581]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_581.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.81])

                #seq_20_582 = []
                if seq_20_582:
                        mydata = [seq_20_582]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_582.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.82])

                #seq_20_583 = []
                if seq_20_583:
                        mydata = [seq_20_583]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_583.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.83])

                #seq_20_584 = []
                if seq_20_584:
                        mydata = [seq_20_584]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_584.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.84])

                #seq_20_585 = []
                if seq_20_585:
                        mydata = [seq_20_585]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_585.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.85])

                #seq_20_586 = []
                if seq_20_586:
                        mydata = [seq_20_586]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_586.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.86])

                #seq_20_587 = []
                if seq_20_587:
                        mydata = [seq_20_587]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_20_587.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.87])

                #seq_21_08 = []
                if seq_21_08:
                        mydata = [seq_21_08]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_08.npz" ) #load model from file
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.8])

                #seq_21_081 = []
                if seq_21_081:
                        mydata = [seq_21_081]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_081.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.81])

                #seq_21_082 = []
                if seq_21_082:
                        mydata = [seq_21_082]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_082.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.82])


                #seq_21_083 = []
                if seq_21_083:
                        mydata = [seq_21_083]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_083.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.83])

                #seq_21_084 = []
                if seq_21_084:
                        mydata = [seq_21_084]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_084.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.84])

                #seq_21_085 = []
                if seq_21_085:
                        mydata = [seq_21_085]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_085.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.85])

                #seq_21_086 = []
                if seq_21_086:
                        mydata = [seq_21_086]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_086.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.86])

                #seq_21_087 = []
                if seq_21_087:
                        mydata = [seq_21_087]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_087.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.87])

                #seq_21_088 = []
                if seq_21_088:
                        mydata = [seq_21_088]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_088.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.88])

                #seq_21_089 = []
                if seq_21_089:
                        mydata = [seq_21_089]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_089.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.89])

                #seq_21_090 = []
                if seq_21_090:
                        mydata = [seq_21_090]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm	= hmms.DtHMM.from_file( path + "seq_21_090.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.90])

                #seq_21_091 = []
                if seq_21_091:
                        mydata = [seq_21_091]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_091.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.91])

                #seq_21_240 = []
                if seq_21_240:
                        mydata = [seq_21_240]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_240.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.40])

                #seq_21_241 = []
                if seq_21_241:
                        mydata = [seq_21_241]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_241.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.41])

                #seq_21_242 = []
                if seq_21_242:
                        mydata = [seq_21_242]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_242.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.42])

                #seq_21_243 = []
                if seq_21_243:
                        mydata = [seq_21_243]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_243.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.43])

                #seq_21_244 = []
                if seq_21_244:
                        mydata = [seq_21_244]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_244.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.44])

                #seq_21_245 = []
                if seq_21_245:
                        mydata = [seq_21_245]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_245.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.45])

                #seq_21_246 = []
                if seq_21_246:
                        mydata = [seq_21_246]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_246.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.46])

                #seq_21_247 = []
                if seq_21_247:
                        mydata = [seq_21_247]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_247.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.47])

                #seq_21_248 = []
                if seq_21_248:
                        mydata = [seq_21_248]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_248.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.48])

                #seq_21_249 = []
                if seq_21_249:
                        mydata = [seq_21_249]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_249.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.49])

                #seq_21_571 = []
                if seq_21_571:
                        mydata = [seq_21_571]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_571.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.71])

                #seq_21_572 = []
                if seq_21_572:
                        mydata = [seq_21_572]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_572.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.72])

                #seq_21_573 = []
                if seq_21_573:
                        mydata = [seq_21_573]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_573.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.73])

                #seq_21_574 = []
                if seq_21_574:
                        mydata = [seq_21_574]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_574.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.74])

                #seq_21_575 = []
                if seq_21_575:
                        mydata = [seq_21_575]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_575.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.75])

                #seq_21_576 = []
                if seq_21_576:
                        mydata = [seq_21_576]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_576.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.76])

                #seq_21_577 = []
                if seq_21_577:
                        mydata = [seq_21_577]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_577.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.77])

                #seq_21_578 = []
                if seq_21_578:
                        mydata = [seq_21_578]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_578.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.78])

                #seq_21_579 = []
                if seq_21_579:
                        mydata = [seq_21_579]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_579.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.79])

                #seq_21_580 = []
                if seq_21_580:
                        mydata = [seq_21_580]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_580.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.80])

                #seq_21_581 = []
                if seq_21_581:
                        mydata = [seq_21_581]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_581.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.81])

                #seq_21_582 = []
                if seq_21_582:
                        mydata = [seq_21_582]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_582.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.82])

                #seq_21_583 = []
                if seq_21_583:
                        mydata = [seq_21_583]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_583.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.83])

                #seq_21_584 = []
                if seq_21_584:
                        mydata = [seq_21_584]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_584.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.84])

                #seq_21_585 = []
                if seq_21_585:
                        mydata = [seq_21_585]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_585.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.85])

                #seq_21_586 = []
                if seq_21_586:
                        mydata = [seq_21_586]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_586.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.86])

                #seq_21_587 = []
                if seq_21_587:
                        mydata = [seq_21_587]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_21_587.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.87])

                #seq_22_08 = []
                if seq_22_08:
                        mydata = [seq_22_08]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_08.npz" ) #load model from file
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.8])

                #seq_22_081 = []
                if seq_22_081:
                        mydata = [seq_22_081]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_081.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.81])

                #seq_22_082 = []
                if seq_22_082:
                        mydata = [seq_22_082]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_082.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.82])


                #seq_22_083 = []
                if seq_22_083:
                        mydata = [seq_22_083]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_083.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.83])

                #seq_22_084 = []
                if seq_22_084:
                        mydata = [seq_22_084]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_084.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.84])

                #seq_22_085 = []
                if seq_22_085:
                        mydata = [seq_22_085]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_085.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.85])

                #seq_22_086 = []
                if seq_22_086:
                        mydata = [seq_22_086]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_086.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.86])

                #seq_22_087 = []
                if seq_22_087:
                        mydata = [seq_22_087]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_087.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.87])

                #seq_22_088 = []
                if seq_22_088:
                        mydata = [seq_22_088]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_088.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.88])

                #seq_22_089 = []
                if seq_22_089:
                        mydata = [seq_22_089]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_089.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.89])

                #seq_22_090 = []
                if seq_22_090:
                        mydata = [seq_22_090]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm	= hmms.DtHMM.from_file( path + "seq_22_090.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.90])

                #seq_22_091 = []
                if seq_22_091:
                        mydata = [seq_22_091]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_091.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.91])

                #seq_22_240 = []
                if seq_22_240:
                        mydata = [seq_22_240]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_240.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.40])

                #seq_22_241 = []
                if seq_22_241:
                        mydata = [seq_22_241]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_241.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.41])

                #seq_22_242 = []
                if seq_22_242:
                        mydata = [seq_22_242]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_242.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.42])

                #seq_22_243 = []
                if seq_22_243:
                        mydata = [seq_22_243]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_243.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.43])

                #seq_22_244 = []
                if seq_22_244:
                        mydata = [seq_22_244]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_244.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.44])

                #seq_22_245 = []
                if seq_22_245:
                        mydata = [seq_22_245]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_245.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.45])

                #seq_22_246 = []
                if seq_22_246:
                        mydata = [seq_22_246]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_246.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.46])

                #seq_22_247 = []
                if seq_22_247:
                        mydata = [seq_22_247]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_247.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.47])

                #seq_22_248 = []
                if seq_22_248:
                        mydata = [seq_22_248]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_248.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.48])

                #seq_22_249 = []
                if seq_22_249:
                        mydata = [seq_22_249]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_249.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.49])

                #seq_22_571 = []
                if seq_22_571:
                        mydata = [seq_22_571]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_571.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.71])

                #seq_22_572 = []
                if seq_22_572:
                        mydata = [seq_22_572]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_572.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.72])

                #seq_22_573 = []
                if seq_22_573:
                        mydata = [seq_22_573]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_573.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.73])

                #seq_22_574 = []
                if seq_22_574:
                        mydata = [seq_22_574]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_574.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.74])

                #seq_22_575 = []
                if seq_22_575:
                        mydata = [seq_22_575]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_575.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.75])

                #seq_22_576 = []
                if seq_22_576:
                        mydata = [seq_22_576]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_576.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.76])

                #seq_22_577 = []
                if seq_22_577:
                        mydata = [seq_22_577]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_577.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.77])

                #seq_22_578 = []
                if seq_22_578:
                        mydata = [seq_22_578]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_578.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.78])

                #seq_22_579 = []
                if seq_22_579:
                        mydata = [seq_22_579]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_579.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.79])

                #seq_22_580 = []
                if seq_22_580:
                        mydata = [seq_22_580]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_580.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.80])

                #seq_22_581 = []
                if seq_22_581:
                        mydata = [seq_22_581]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_581.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.81])

                #seq_22_582 = []
                if seq_22_582:
                        mydata = [seq_22_582]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_582.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.82])

                #seq_22_583 = []
                if seq_22_583:
                        mydata = [seq_22_583]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_583.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.83])

                #seq_22_584 = []
                if seq_22_584:
                        mydata = [seq_22_584]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_584.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.84])

                #seq_22_585 = []
                if seq_22_585:
                        mydata = [seq_22_585]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_585.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.85])

                #seq_22_586 = []
                if seq_22_586:
                        mydata = [seq_22_586]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_586.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.86])

                #seq_22_587 = []
                if seq_22_587:
                        mydata = [seq_22_587]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_22_587.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.87])

                #seq_23_08 = []
                if seq_23_08:
                        mydata = [seq_23_08]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_08.npz" ) #load model from file
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.8])

                #seq_23_081 = []
                if seq_23_081:
                        mydata = [seq_23_081]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_081.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.81])

                #seq_23_082 = []
                if seq_23_082:
                        mydata = [seq_23_082]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_082.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.82])


                #seq_23_083 = []
                if seq_23_083:
                        mydata = [seq_23_083]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_083.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.83])

                #seq_23_084 = []
                if seq_23_084:
                        mydata = [seq_23_084]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_084.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.84])

                #seq_23_085 = []
                if seq_23_085:
                        mydata = [seq_23_085]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_085.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.85])

                #seq_23_086 = []
                if seq_23_086:
                        mydata = [seq_23_086]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_086.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.86])

                #seq_23_087 = []
                if seq_23_087:
                        mydata = [seq_23_087]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_087.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.87])

                #seq_23_088 = []
                if seq_23_088:
                        mydata = [seq_23_088]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_088.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.88])

                #seq_23_089 = []
                if seq_23_089:
                        mydata = [seq_23_089]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_089.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.89])

                #seq_23_090 = []
                if seq_23_090:
                        mydata = [seq_23_090]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm	= hmms.DtHMM.from_file( path + "seq_23_090.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.90])

                #seq_23_091 = []
                if seq_23_091:
                        mydata = [seq_23_091]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_091.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),0.91])

                #seq_23_240 = []
                if seq_23_240:
                        mydata = [seq_23_240]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_240.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.40])

                #seq_23_241 = []
                if seq_23_241:
                        mydata = [seq_23_241]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_241.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.41])

                #seq_23_242 = []
                if seq_23_242:
                        mydata = [seq_23_242]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_242.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.42])

                #seq_23_243 = []
                if seq_23_243:
                        mydata = [seq_23_243]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_243.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.43])

                #seq_23_244 = []
                if seq_23_244:
                        mydata = [seq_23_244]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_244.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.44])

                #seq_23_245 = []
                if seq_23_245:
                        mydata = [seq_23_245]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_245.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.45])

                #seq_23_246 = []
                if seq_23_246:
                        mydata = [seq_23_246]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_246.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.46])

                #seq_23_247 = []
                if seq_23_247:
                        mydata = [seq_23_247]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_247.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.47])

                #seq_23_248 = []
                if seq_23_248:
                        mydata = [seq_23_248]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_248.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.48])

                #seq_23_249 = []
                if seq_23_249:
                        mydata = [seq_23_249]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_249.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),2.49])

                #seq_23_571 = []
                if seq_23_571:
                        mydata = [seq_23_571]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_571.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.71])

                #seq_23_572 = []
                if seq_23_572:
                        mydata = [seq_23_572]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_572.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.72])

                #seq_23_573 = []
                if seq_23_573:
                        mydata = [seq_23_573]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_573.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.73])

                #seq_23_574 = []
                if seq_23_574:
                        mydata = [seq_23_574]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_574.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.74])

                #seq_23_575 = []
                if seq_23_575:
                        mydata = [seq_23_575]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_575.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.75])

                #seq_23_576 = []
                if seq_23_576:
                        mydata = [seq_23_576]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_576.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.76])

                #seq_23_577 = []
                if seq_23_577:
                        mydata = [seq_23_577]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_577.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.77])

                #seq_23_578 = []
                if seq_23_578:
                        mydata = [seq_23_578]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_578.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.78])

                #seq_23_579 = []
                if seq_23_579:
                        mydata = [seq_23_579]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_579.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.79])

                #seq_23_580 = []
                if seq_23_580:
                        mydata = [seq_23_580]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_580.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.80])

                #seq_23_581 = []
                if seq_23_581:
                        mydata = [seq_23_581]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_581.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.81])

                #seq_23_582 = []
                if seq_23_582:
                        mydata = [seq_23_582]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_582.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.82])

                #seq_23_583 = []
                if seq_23_583:
                        mydata = [seq_23_583]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_583.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.83])

                #seq_23_584 = []
                if seq_23_584:
                        mydata = [seq_23_584]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_584.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.84])

                #seq_23_585 = []
                if seq_23_585:
                        mydata = [seq_23_585]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_585.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.85])

                #seq_23_586 = []
                if seq_23_586:
                        mydata = [seq_23_586]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_586.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.86])

                #seq_23_587 = []
                if seq_23_587:
                        mydata = [seq_23_587]#used because training step requires it
                        a = np.empty_like (mydata)#used because training step requires it
                        a[:] = mydata#used because training step requires it
                        hmm  = hmms.DtHMM.random( 2,2 )#create model with random values 2 emisson values 2 transition values
                        hmm = hmms.DtHMM.from_file( path + "seq_23_587.npz" )
                        real = hmm.data_estimate(a)#goal probability
                        final.append([np.exp(real),5.87])

                arrayTemp = np.array(final)#change to numpy array

                for i in range(len(arrayTemp)):
                        max_col_in_row_i = np.argmax(arrayTemp[i,:])#get the best probability index in the array
                        #max_col_in_row_i = np.argmin(arrayTemp[i,:])#get the best probability index in the array
           
                result = arrayTemp[max_col_in_row_i,1] #the frequency of the best probability
                          
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