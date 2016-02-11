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
import grgsm
import osmosdr
import pmt
import sip
import sys
import time
import logging
from threading import Thread
import argparse

class airprobe_rtlsdr(gr.top_block):

    def __init__(self, fc=939.4e6, gain=30, ppm=0, samp_rate=2000000.052982, shiftoff=400e3):
        gr.top_block.__init__(self, "Airprobe Rtlsdr")

        # Logging system (to specific file)
        logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', filename='log', filemod='w', level=logging.INFO)

        ##################################################
        # Parameters
        ##################################################
        self.fc = fc
        self.gain = gain
        self.ppm = ppm
        self.samp_rate = samp_rate
        self.shiftoff = shiftoff

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

# Setup all parameters allowed to the command script
def setup_parameters():
    parser = argparse.ArgumentParser(description='Configure sniffing parameters')
    group = parser.add_argument_group("grgsm arguments")
    group.add_argument("-g", "--gain", help="Set the gain parameter", default=30, type=float)
    group.add_argument("-p", "--ppm", help="Set the ppm parameter", default=0 , type=int)
    group.add_argument("-s", "--samp_rate", help="Set the sample rate parameter", default=2000000.052982, type=float)
    group.add_argument("-o", "--shiftoff", help="Set the shiftoff (offset) parameter", default=400000, type=float)
    group.add_argument("-f", "--frequencies", help="Set all the frequencies to check", default=[937755550], type=float, nargs='+')
    return parser

if __name__ == '__main__':
    # Loading arguments parser
    parser = setup_parameters()
    args = parser.parse_args()

    #937755550

    tb = airprobe_rtlsdr(fc=args.frequencies[0], gain=args.gain, ppm=args.ppm, samp_rate=args.samp_rate, shiftoff=args.shiftoff)
    tb.start()

    # Launch gr-gsm in another thread to avoid putting the main process in "wait state"
    grgsm = Thread(target=tb.wait)
    grgsm.daemon = True # Stop the thread if the main process is stopped
    grgsm.start()

    # For all frequencies in argument, sniffing for 2 seconds then continuing to the next
    while True:
        for i,fc in enumerate(args.frequencies):
            time.sleep(2)
            print("Current frequency : " + str(fc))
            tb.set_fc(fc)

    grgsm.stop()
    tb.stop()s
