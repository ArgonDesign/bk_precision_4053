import visa
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
      waveform_data.append(((2.0/8192) * i) - 1.0)
    for i in range(8192):
      waveform_data.append(((-2.0/8192) * i) + 1.0)
    my_awg.define_arbitrary_waveform(mem_index = 1, data = waveform_data, freq_hz = 2000.0, amp_vpp = 3.0)

    # define bipolar 5kHz 0.5Vpp amplitude sawtooth wave in memory no.2
    waveform_data = []
    for i in range(8192):
      waveform_data.append(((2.0/8192) * i) - 1.0)
    for i in range(8192):
      waveform_data.append(((2.0/8192) * i) - 1.0)
    my_awg.define_arbitrary_waveform(mem_index = 2, data = waveform_data, freq_hz = 5000.0, amp_vpp = 0.5)
    
    
    # assign the waveform from memory no.0 to AWG output channel no.1
    my_awg.select_arbitrary_waveform(channel_no = 1, mem_index = 0)
    
    # assign the waveform from memory no.1 to AWG output channel no.2
    my_awg.select_arbitrary_waveform(channel_no = 2, mem_index = 1)
    
