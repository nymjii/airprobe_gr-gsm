#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Airprobe Rtlsdr
# Generated: Wed Sep  2 21:46:35 2015
# Generated: Wed Fev 10 17:27:21 2016
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from math import pi
from optparse import OptionParser
import grgsm
import osmosdr
import pmt
import sip
import sys
import time
import logging

class airprobe_rtlsdr(gr.top_block, Qt.QWidget):

    def __init__(self):
        # Graphical initialisation
        gr.top_block.__init__(self, "Airprobe Rtlsdr")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Airprobe Rtlsdr")
        try:
             self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
             pass

        # Logging system (to specific file)
        logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', filename='graphical_sniffing_log', filemod='w', level=logging.INFO)

        # Windows setting
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)
        self.settings = Qt.QSettings("GNU Radio", "airprobe_rtlsdr")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Parameters
        ##################################################
        self.fc = 937755550 #937.7e6
        self.gain = 30
        self.ppm = 0
        self.samp_rate = 2000000.052982
        self.shiftoff = 400e3

        ##################################################
        # Blocks
        ##################################################
        # Order : min value, max value, step, default value and ?)
        self._ppm_slider_range = Range(-150, 150, 1, self.ppm, 100)
        self._ppm_slider_win = RangeWidget(self._ppm_slider_range, self.set_ppm, "PPM Offset", "counter", float)
        self.top_layout.addWidget(self._ppm_slider_win)
        self._g_slider_range = Range(0, 50, 0.5, self.gain, 100)
        self._g_slider_win = RangeWidget(self._g_slider_range, self.set_gain, "Gain", "counter", float)
        self.top_layout.addWidget(self._g_slider_win)
        self._fc_slider_range = Range(925e6, 1990e6, 2e5, self.fc, 100)
        self._fc_slider_win = RangeWidget(self._fc_slider_range, self.set_fc, "Frequency", "counter_slider", float)        
        self.top_layout.addWidget(self._fc_slider_win)
        
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
          
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	self.fc,
        	self.samp_rate, #bw
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        
        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.gsm_sdcch8_demapper_0 = grgsm.universal_ctrl_chans_demapper(1, ([0,4,8,12,16,20,24,28,32,36,40,44]), ([8,8,8,8,8,8,8,8,136,136,136,136]))
        self.gsm_receiver_0 = grgsm.receiver(4, ([0]), ([]))
        self.gsm_message_printer_1 = grgsm.message_printer(pmt.intern(""), False)
        self.gsm_input_0 = grgsm.gsm_input(
            ppm=self.ppm,
            osr=4,
            fc=self.fc,
            samp_rate_in=self.samp_rate,
        )
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
        self.connect((self.blocks_rotator_cc_0, 0), (self.qtgui_freq_sink_x_0, 0))    
        self.connect((self.gsm_input_0, 0), (self.gsm_receiver_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_rotator_cc_0, 0))    

#937755550

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "airprobe_rtlsdr")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    # Get the sample rate value
    def get_samp_rate(self):
        return self.samp_rate

    # Set the sample rate value
    def set_samp_rate(self, samp_rate):
        logging.info('Changing the sample rate from %s to  %s', self.samp_rate, samp_rate)
        self.samp_rate = samp_rate
        self.blocks_rotator_cc_0.set_phase_inc(-2*pi*self.shiftoff/self.samp_rate)
        self.gsm_input_0.set_samp_rate_in(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.fc, self.samp_rate)
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
        self.qtgui_freq_sink_x_0.set_frequency_range(self.fc, self.samp_rate)
        self.rtlsdr_source_0.set_center_freq(self.fc-self.shiftoff, 0)


if __name__ == '__main__':    
    Qt.QApplication.setGraphicsSystem(gr.prefs().get_string('qtgui','style','raster'))
    qapp = Qt.QApplication(sys.argv)

    # Define rtlsdr thread
    tb = airprobe_rtlsdr()
    tb.start()
    tb.show()

    # Handling rtlsdr thread in case of process father death
    def quitting():
        tb.stop()
        tb.wait()

    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    tb = None  # to clean up Qt widgets
