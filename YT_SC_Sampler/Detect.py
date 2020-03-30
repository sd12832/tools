# Grabbed from https://github.com/scaperot/the-BPM-detector-python

# Implementation of a Beats Per Minute (BPM) detection algorithm, 
# as presented in the paper of G. Tzanetakis, G. Essl and P. Cook titled: 
# "Audio Analysis using the Discrete Wavelet Transform".
# Modified by Sharan Duggirala

import wave, array, math, time, argparse, sys
import numpy, pywt
from scipy import signal
import pdb

class Detect():

    def read_wav(self, filename):
    
        #open file, get metadata for audio
        try:
            wf = wave.open(filename,'rb')
        except IOError:
            print('File Error')
            sys.exit(1)

        # typ = choose_type( wf.getsampwidth() ) #TODO: implement choose_type
        nsamps = wf.getnframes()
        assert(nsamps > 0)

        fs = wf.getframerate()
        assert(fs > 0)

        # read entire file and make into an array
        samps = list(array.array('i',wf.readframes(nsamps)))
        #print 'Read', nsamps,'samples from', filename
        try:
            assert(nsamps == len(samps))
        except AssertionError:
            print(nsamps, "not equal to", len(samps))

        return samps, fs


    # print an error when no data can be found
    def no_audio_data(self):

        print("No audio data for sample, skipping...")
        return None, None


    # simple peak detection
    def peak_detect(self, data):

        max_val = numpy.amax(abs(data)) 
        peak_ndx = numpy.where(data==max_val)

        #if nothing found then the max must be negative
        if len(peak_ndx[0]) == 0:
            peak_ndx = numpy.where(data==-max_val)

        return peak_ndx


    def bpm_detector(self, data, fs):

        cA = [] 
        cD = []
        correl = []
        cD_sum = []
        levels = 4
        max_decimation = 2**(levels-1);
        min_ndx = int(60./ 220 * (fs/max_decimation))
        max_ndx = int(60./ 40 * (fs/max_decimation))

        for loop in range(0,levels):
            cD = []
            # 1) DWT
            if loop == 0:
                [cA,cD] = pywt.dwt(data,'db4')
                cD_minlen = int(len(cD)/max_decimation+1)
                cD_sum = numpy.zeros(cD_minlen)
            else:
                [cA,cD] = pywt.dwt(cA,'db4')
            # 2) Filter
            cD = signal.lfilter([0.01],[1 -0.99],cD)

            # 4) Subtractargs.filename out the mean.

            # 5) Decimate for reconstruction later.
            cD = abs(cD[::(2**(levels-loop-1))])
            cD = cD - numpy.mean(cD);
            # 6) Recombine the signal before ACF
            #    essentially, each level I concatenate 
            #    the detail coefs (i.e. the HPF values)
            #    to the beginning of the array
            cD_sum = cD[0:cD_minlen] + cD_sum

        if [b for b in cA if b != 0.0] == []:
            return self.no_audio_data()
        # adding in the approximate data as well...    
        cA = signal.lfilter([0.01],[1 -0.99],cA);
        cA = abs(cA);
        cA = cA - numpy.mean(cA);
        cD_sum = cA[0:cD_minlen] + cD_sum;

        # ACF
        correl = numpy.correlate(cD_sum,cD_sum,'full') 

        midpoint = len(correl) / 2
        correl_midpoint_tmp = correl[int(midpoint):]
        peak_ndx = self.peak_detect(correl_midpoint_tmp[min_ndx:max_ndx]);
        if len(peak_ndx) > 1:
            return self.no_audio_data()

        peak_ndx_adjusted = peak_ndx[0]+min_ndx;
        bpm = 60./ peak_ndx_adjusted * (fs/max_decimation)

        return bpm, correl


    def detect(self, filename, window = 3):

        samps,fs = self.read_wav(filename)

        data = []
        correl=[]
        bpm = 0
        n=0;
        nsamps = len(samps)
        window_samps = int(window*fs)         
        samps_ndx = 0  #first sample in window_ndx 
        max_window_ndx = int(nsamps / window_samps)
        bpms = numpy.zeros(int(max_window_ndx))

        #iterate through all windows
        for window_ndx in range(0, int(max_window_ndx)):

            #get a new set of samples
            #print n,":",len(bpms),":",max_window_ndx,":",fs,":",nsamps,":",samps_ndx
            data = samps[samps_ndx:samps_ndx+window_samps]
            if not ((len(data) % window_samps) == 0):
                raise AssertionError( str(len(data) ) ) 

            bpm, correl_temp = self.bpm_detector(data,fs)
            if bpm == None:
                continue
            bpms[window_ndx] = bpm
            correl = correl_temp

            #iterate at the end of the loop
            samps_ndx = samps_ndx+window_samps;
            n=n+1; #counter for debug...

        bpm = numpy.median(bpms)
        print('Completed. Estimated Beats Per Minute:', bpm)

        return bpm