#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2015 Ariel Marques.
# Universidade Federal de Lavras - UFLA
# Departamento de Ciencia da Computacao - DCC
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

import json,time,os,pmt
from gnuradio import gr

#Bloco que salvo os dados do sensoreamento em arquivo
class PDU_json(gr.sync_block):
    """
    docstring for block PDU_json
    """
    def __init__(self, filename="/tmp/gr.msg.store.json.out"):
        gr.sync_block.__init__(self,
            name="PDU_json",
            in_sig = [],
            out_sig = []);
            
        self.filename = filename
        
        
        
        self.message_port_register_in(pmt.intern("bool"))           #registra entrada bool
        self.set_msg_handler(pmt.intern("bool"), self.handler2)     #seta funcao handler2 em bool
        
        self.message_port_register_in(pmt.intern("pdus"))           #registra entrada pdus
        self.set_msg_handler(pmt.intern("pdus"), self.handler)      #seta funcao handler em pdus
        
        
        self.message_port_register_out(pmt.intern("file_ready"))    #registra saida file_ready
        #print "WARNING: Writing JSON object trace to %s"%(self.fn)

    #work nao faz nada    
    def work(self, input_items, output_items):
        assert(False)

    #handler 2
    #mensagem de controle
    def handler2(self,pdu):
        if (not(pmt.to_bool(pdu))):
            self.message_port_pub(pmt.intern("file_ready"),pdu)
            #os.system("./home/ariel/Documentos/gr-pmt_cpp/driver1/unload_gcc116")
            
        
    #handler
    #funcao que armazena os dados em um arquivo
    def handler(self, pdu):
        
        
        #meta = pmt.to_python(pmt.car(pdu))
        meta_pdu = pmt.car(pdu)
        fre = pmt.dict_ref(meta_pdu,pmt.intern("rx_freq"),pmt.PMT_NIL)
        power = pmt.dict_ref(meta_pdu,pmt.intern("power"),pmt.PMT_NIL)
        time = pmt.dict_ref(meta_pdu,pmt.intern("time"),pmt.PMT_NIL)
        
        if( -float('inf') != pmt.to_double(power) ):
            self.f = open(self.filename, "a")
            metaj = str(pmt.to_uint64(time))+":"+str(pmt.to_double(fre))+":"+str(pmt.to_double(power))
            #os.system( "echo "+metaj+"> /dev/gcc116")
            #os.system( "echo "+" "+"> /dev/gcc116")
            self.f.write(metaj)
            self.f.write("\n")
            self.f.flush()
            self.f.close()
