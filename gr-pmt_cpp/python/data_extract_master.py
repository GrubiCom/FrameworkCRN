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

import time,os,pmt
from gnuradio import gr

class data_extract_master(gr.basic_block):
    """
    docstring for block data_extract_master
    """
    def __init__(self,filename="/tmp/gr.msg.store.json.out"):
        gr.basic_block.__init__(self,
            name="data_extract_master",
            in_sig=[],
            out_sig=[])

        self.filename = "/tmp/"
               
        self.message_port_register_in(pmt.intern("pdus"))           #registra entrada pdus
        self.set_msg_handler(pmt.intern("pdus"), self.handler)      #seta funcao handler em pdus
        
        
        ##self.message_port_register_out(pmt.intern("file_ready"))    #registra saida file_ready
        print "WARNING: Writing JSON object trace to %s"%(self.filename)

    #work nao faz nada    
    def work(self, input_items, output_items):
        assert(False)

        
    #handler
    #funcao que armazena os dados em um arquivo
    def handler(self, pdu):
        #print "PYTHON"
        if (not os.path.exists("/tmp/results/")):
            os.mkdir("/tmp/results/")
        self.filename = "/tmp/results/res_sense";
        
        meta = pmt.to_python(pmt.car(pdu))
        #meta_pdu = pmt.car(pdu)
        if( pmt.dict_has_key(pdu,pmt.intern("res_sense"))):
            res = pmt.dict_ref(pdu,pmt.intern("res_sense"),pmt.PMT_NIL)
            #print res
            metaj = pmt.symbol_to_string(res)
            self.f = open(self.filename+metaj[3]+".txt", "a")
            print "[MASTER][FILE RECORDER MASTER]: metaj: "+ metaj
            #<G:1:1:597
            ini = metaj.find("G")
            final = metaj.find(">")
            pos1 = metaj.find(":",5)
            #print "int(metaj[5:pos1]): "+ int(metaj[5:pos1])
            #print "metaj[5:pos1]: "+ metaj[5:pos1]
            if (int(metaj[5:pos1]) >=10):
                self.f.write(metaj[ini+7:final])
            else:
                self.f.write(metaj[ini+6:final])
            #if(metaj[5:6] != "1:"):
            #    print "metaj[5] != 1: "+ metaj[5]

            #self.f.write(metaj[ini:final])
            #self.f.write("\n")
            #self.f.write(metaj)
            self.f.flush()
            self.f.close()
