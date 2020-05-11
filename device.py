#!/usr/bin/env python3
#
#   A device used at a satellite ground station
#
#   Kyle Eberhart - 7MAY20
#
#------------------------------------------------------------------------------

import math

speed_of_light = 299792458.0
boltzmann_const = 1.38064852e-23

class Device:
    '''A random device, defaults to cable'''

    def __init__(self):
        self.gain = -.5
        self.name = 'Cable'
        self.noise_figure = -.5
        self.in_dev = None
        self.in_bw = None
        self.frequency = None
        self.out_dev = None
        self.out_bw = None
        self.out_freq = None
        self.ambient_temp = 290.0
        self.T = (math.pow(10,math.fabs(self.gain)/10)-1)*self.ambient_temp

    def connect(self, dev_in, dev_out):
        self.in_dev = dev_in
        self.out_dev = dev_out


class Antenna(Device):

    def __init__(self, name='13M-1', diameter=13, effiency=52.8):
        Device.__init__(self)
        self.name = name
        self.diameter = diameter
        self.effiency = effiency
        self.sky_temp_K = 45.0
        self.beamwidth = None
        self.area = math.pi*math.pow(self.diameter,2)/4

    def set_frequency(self, frequency):
        self.frequency = frequency
        self.wavelength = freq_to_length(self.frequency)
        self.beamwidth = 70*self.wavelength/self.diameter
        self.gain = 10*math.log10(self.effiency/100*(math.pow(math.pi*self.diameter/self.wavelength,2)))
        self.calc_antenna_temp()

    def calc_antenna_temp(self):
        #self.sky_temp_K = 10.0
        #self.ambient_temp_K = 300.0
        #self.effiency = 70.0
        # With the test values above Ta_mb = 7K, Ta_gbl = 45K, Ta_hbl = 22.5K,
        # Total = 74.5K
        Ta_mb = 1/self.beamwidth*(self.sky_temp_K*(self.effiency/100)*self.beamwidth)
        Ta_gbl = 1/self.beamwidth*(self.ambient_temp_K*(1-(self.effiency/100))/2*self.beamwidth)
        Ta_hbl = 1/self.beamwidth*(self.ambient_temp_K/2*(1-(self.effiency/100))/2*self.beamwidth)
        self.T = Ta_mb + Ta_gbl + Ta_hbl
        #print(Ta_mb, Ta_gbl, Ta_hbl, self.T)

    def __str__(self):
        return (str(self.frequency)+", "+str(self.gain)+", "+str(self.T)+", "+str(self.beamwidth))


def freq_to_length(freq):
    '''Calculate the wavelength of a frequency in Hz to meters'''
    wl = speed_of_light/freq
    return wl


if __name__ == "__main__":
    #ant = Antenna('13M-1',13,52.8)
    #ant.connect(None, Device())
    #ant.set_frequency(2200000000)
    #print(ant)
    cable = Device()
    print(cable.T)


