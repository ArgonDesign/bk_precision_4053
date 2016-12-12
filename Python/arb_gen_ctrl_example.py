import visa
import time
import math
from bk_precision_4053 import BkPrecision4053

def replace_non_printable(text, replacement = "."):
  return "".join([i if ((ord(i) >= 32) and (ord(i) < 128)) else replacement for i in text])

def dump_ascii_hex(data, step = 16):
  for i in range(0, len(data), step):
    hex_str = ""
    ascii_str = ""
    for j in range(step):
      try:
        hex_val_str = "{:02X}".format(ord(data[i+j]))
        hex_str += hex_val_str + " "
        ascii_str += replace_non_printable(data[i+j])
      except (IndexError):
        break
    
    print("{:s} {:s}".format(hex_str, ascii_str))

    
if __name__ == "__main__":
  rm = visa.ResourceManager()
  
  with BkPrecision4053(rm, u"USB0::0xF4ED::0xEE3A::389D15114::INSTR") as my_awg:
    my_awg.identify()
    
    # define bipolar 1kHz 2Vpp amplitude square wave in memory no.0
    waveform_data = [-1.0] * 8192
    waveform_data += [1.0] * 8192
    my_awg.define_arbitrary_waveform(mem_index = 0, data = waveform_data, freq_hz = 1000.0, amp_vpp = 2.0)
    
    # define bipolar 2kHz 3Vpp amplitude triangle wave in memory no.1
    waveform_data = []
    for i in range(8192):
      waveform_data.append(((2.0/8192.0) * i) - 1.0)
    for i in range(8192):
      waveform_data.append(((-2.0/8192.0) * i) + 1.0)
    my_awg.define_arbitrary_waveform(mem_index = 1, data = waveform_data, freq_hz = 2000.0, amp_vpp = 3.0)

    # define bipolar 5kHz 0.5Vpp amplitude sawtooth wave in memory no.2
    waveform_data = []
    for i in range(16384):
      waveform_data.append(((2.0/16384.0) * i) - 1.0)
    my_awg.define_arbitrary_waveform(mem_index = 2, data = waveform_data, freq_hz = 5000.0, amp_vpp = 0.5)
    
    #define sinewave 10kHz 1Vpp amplitude in memory no.3
    waveform_data = []
    for i in range(16384):
      waveform_data.append(math.sin(2.0*math.pi*(i/16384.0)))
    my_awg.define_arbitrary_waveform(mem_index = 3, data = waveform_data, freq_hz = 10000.0, amp_vpp = 1.0)
    
    # assign the waveform from memory no.3 to AWG output channel no.1
    my_awg.assign_arbitrary_waveform_to_channel(channel_no = 1, mem_index = 3, load_50_ohm = False)
    
    # assign the waveform from memory no.2 to AWG output channel no.2
    my_awg.assign_arbitrary_waveform_to_channel(channel_no = 2, mem_index = 2, load_50_ohm = False)
    
    # enable output channel 1 for high impedance load
    my_awg.channel_command(channel_no = 1, enable = True)
    
    # enable output channel 2 for high impedance load
    my_awg.channel_command(channel_no = 2, enable = True)

    # beep with the buzzer
    my_awg.beep_once()
    
    # wait for 5 second
    time.sleep(5.0)
    
    # disable both AWG outputs
    my_awg.channel_command(channel_no = 1, enable = False)
    my_awg.channel_command(channel_no = 2, enable = False)
    
    # beep with the buzzer
    my_awg.beep_once()
