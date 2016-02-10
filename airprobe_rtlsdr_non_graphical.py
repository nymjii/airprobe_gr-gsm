#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Airprobe Rtlsdr
# Generated: Wed Fev 10 17:27:21 2016
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from math import pi
from optparse import OptionParser
import grgsm
import osmosdr
import pmt
import sip
import sys
import time
import logging

class airprobe_rtlsdr(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Airprobe Rtlsdr")

        # Logging system (to specific file)
        logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', filename='log', filemod='w', level=logging.INFO)

        ##################################################
        # Parameters
        ##################################################
        self.fc = 937755550 #939.4e6
        self.gain = 30
        self.ppm = 0
        self.samp_rate = 2000000.052982
        self.shiftoff = 400e3

        ##################################################
        # Blocks
        ##################################################

        # Initialisation of the rtlsdr module to communicate with the device
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)
        self.rtlsdr_source_0.set_center_freq(self.fc-self.shiftoff, 0)
        self.rtlsdr_source_0.set_freq_corr(self.ppm, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(2, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(2, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(self.gain, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna("", 0)
        self.rtlsdr_source_0.set_bandwidth(250e3+abs(self.shiftoff), 0)

        self.gsm_sdcch8_demapper_0 = grgsm.universal_ctrl_chans_demapper(1, ([0,4,8,12,16,20,24,28,32,36,40,44]), ([8,8,8,8,8,8,8,8,136,136,136,136]))
        self.gsm_receiver_0 = grgsm.receiver(4, ([0]), ([]))
        self.gsm_message_printer_1 = grgsm.message_printer(pmt.intern(""), False)
        self.gsm_input_0 = grgsm.gsm_input(
            ppm=self.ppm,
            osr=4,
            fc=self.fc,
            samp_rate_in=self.samp_rate,
        )

        # launch decryption of GSM packets
        self.gsm_decryption_0 = grgsm.decryption(([]), 1)
        self.gsm_control_channels_decoder_0_0 = grgsm.control_channels_decoder()
        self.gsm_control_channels_decoder_0 = grgsm.control_channels_decoder()
        self.gsm_clock_offset_control_0 = grgsm.clock_offset_control(self.fc-self.shiftoff)
        self.gsm_bcch_ccch_demapper_0 = grgsm.universal_ctrl_chans_demapper(0, ([2,6,12,16,22,26,32,36,42,46]), ([1,2,2,2,2,2,2,2,2,2]))
        self.blocks_socket_pdu_0_0 = blocks.socket_pdu("UDP_SERVER", "127.0.0.1", "4729", 10000)
        self.blocks_socket_pdu_0 = blocks.socket_pdu("UDP_CLIENT", "127.0.0.1", "4729", 10000)
        self.blocks_rotator_cc_0 = blocks.rotator_cc(-2*pi*self.shiftoff/self.samp_rate)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.gsm_bcch_ccch_demapper_0, 'bursts'), (self.gsm_control_channels_decoder_0, 'bursts'))    
        self.msg_connect((self.gsm_clock_offset_control_0, 'ppm'), (self.gsm_input_0, 'ppm_in'))    
        self.msg_connect((self.gsm_control_channels_decoder_0, 'msgs'), (self.blocks_socket_pdu_0, 'pdus'))    
        self.msg_connect((self.gsm_control_channels_decoder_0, 'msgs'), (self.gsm_message_printer_1, 'msgs'))    
        self.msg_connect((self.gsm_control_channels_decoder_0_0, 'msgs'), (self.blocks_socket_pdu_0, 'pdus'))    
        self.msg_connect((self.gsm_control_channels_decoder_0_0, 'msgs'), (self.gsm_message_printer_1, 'msgs'))    
        self.msg_connect((self.gsm_decryption_0, 'bursts'), (self.gsm_control_channels_decoder_0_0, 'bursts'))    
        self.msg_connect((self.gsm_receiver_0, 'C0'), (self.gsm_bcch_ccch_demapper_0, 'bursts'))    
        self.msg_connect((self.gsm_receiver_0, 'measurements'), (self.gsm_clock_offset_control_0, 'measurements'))    
        self.msg_connect((self.gsm_receiver_0, 'C0'), (self.gsm_sdcch8_demapper_0, 'bursts'))    
        self.msg_connect((self.gsm_sdcch8_demapper_0, 'bursts'), (self.gsm_decryption_0, 'bursts'))
        self.connect((self.blocks_rotator_cc_0, 0), (self.gsm_input_0, 0))
        self.connect((self.gsm_input_0, 0), (self.gsm_receiver_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_rotator_cc_0, 0))

    # Get the sample rate value
    def get_samp_rate(self):
        return self.samp_rate

    # Set the sample rate value
    def set_samp_rate(self, samp_rate):
        logging.info('Changing the sample rate from %s to  %s', self.samp_rate, samp_rate)
        self.samp_rate = samp_rate
        self.blocks_rotator_cc_0.set_phase_inc(-2*pi*self.shiftoff/self.samp_rate)
        self.gsm_input_0.set_samp_rate_in(self.samp_rate)
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    # Get the current shiftoff value
    def get_shiftoff(self):
        return self.shiftoff

    # Set the shiftoff value
    def set_shiftoff(self, shiftoff):
        logging.info('Changing the shiftoff from %s to  %s', self.shiftoff, shiftoff)
        self.shiftoff = shiftoff
        self.blocks_rotator_cc_0.set_phase_inc(-2*pi*self.shiftoff/self.samp_rate)
        self.rtlsdr_source_0.set_center_freq(self.fc-self.shiftoff, 0)
        self.rtlsdr_source_0.set_bandwidth(250e3+abs(self.shiftoff), 0)

    # Get the current PPM value
    def get_ppm(self):
        return self.ppm

    # Set the PPM value
    def set_ppm(self, ppm):
        logging.info('Changing the PPM from %s to  %s', self.ppm, ppm)
        self.ppm = ppm
        self.rtlsdr_source_0.set_freq_corr(self.ppm, 0)

    # Get the current gain value
    def get_gain(self):
        return self.gain

    # Set the gain value
    def set_gain(self, gain):
        logging.info('Changing gain from %s to  %s', self.gain, gain)
        self.gain = gain
        self.rtlsdr_source_0.set_gain(self.gain, 0)

    # Get the listening frequency
    def get_fc(self):
        return self.fc

    # Set the frequency to listen
    def set_fc(self, fc):
        logging.info('Changing frequency from %s to %s', self.fc, fc)
        self.fc = fc
        self.rtlsdr_source_0.set_center_freq(self.fc-self.shiftoff, 0)

if __name__ == '__main__':
    tb = airprobe_rtlsdr()
    tb.start()
    tb.wait()
    #tb = None  # to clean up Qt widgets
