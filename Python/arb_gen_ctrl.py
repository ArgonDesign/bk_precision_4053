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
  
  # my_instrument = rm.open_resource(u'USB0::0xF4ED::0xEE3A::389D15114::INSTR')
  # # setup write termination characters
  # my_instrument.write_termination = "\n"

  # # perform the same queries as EasyWave does
  # print (my_instrument.query("*IDN?"))
  # print (my_instrument.query("PROD MODEL?"))
  # print (my_instrument.query("IDN-SGLT-PRI?"))
  # print (my_instrument.query("STL? RELEASE"))
  # print (my_instrument.query("PROD BAND?"))
 
  # # now write command to modify the waveform
  # cmmd = "WVDT M50,WVNM,wave2,TYPE,5,LENGTH,32KB,FREQ,1000.000000000,AMPL,5.000000000,OFST,0.000000000,PHASE,0.000000000,WAVEDATA,"
  # cmmd += "\xFF"
  
  # values = [0x1FFF] * 8192
  # values += [0x2000] * 8192
  
  # bin_values = ""
  # for i in range(len(values)):
    # bin_values += chr((values[i] >> 8) & 0xFF)
    # bin_values += chr(values[i] & 0xFF)

  # # for some reason (probably a bug in BK precision software), WVDT command data length has to be one byte less that what
  # # one expects it to be. Failing to strip one byte off results in the generator ignoring the WVDT command completely
  # bin_values = bin_values[:-1]
  
  # # write the command to the instrument
  # my_instrument.write_raw(cmmd + bin_values)

  # # use arbitrary waveform on channel 1
  # my_instrument.write('C1:ARWV INDEX,50')

  # my_instrument.close()
