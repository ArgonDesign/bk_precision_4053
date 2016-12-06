import visa

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
  my_instrument = rm.open_resource(u'USB0::0xF4ED::0xEE3A::389D15114::INSTR')
  # setup write termination characters
  my_instrument.write_termination = "\n"

  # perform the same queries as EasyWave does
  print (my_instrument.query("PROD MODEL?"))
  print (my_instrument.query("IDN-SGLT-PRI?"))
  print (my_instrument.query("STL? RELEASE"))
  print (my_instrument.query("PROD BAND?"))
 
  # my_instrument.query('WVDT M50?')

  # my_instrument.write('WVDT? M50')
  # data = my_instrument.read_raw()
  # dump_ascii_hex(data)
  
  # strip off actual waveform data
  # waveform_str_to_find = "WAVEDATA,"
  # waveform_data_index = data.find(waveform_str_to_find) + len(waveform_str_to_find)
  # # make sure that the index is odd (waveform data have to be aligned in actual USB packet)
  # if ((waveform_data_index % 2) == 0):
    # waveform_data_index += 1
  
  # waveform_data = data[waveform_data_index:]

  # now try to write command to modify the waveform
  cmmd = "C1:WVDT M50,WVNM,wave2,TYPE,5,LENGTH,32KB,FREQ,1000.000000000,AMPL,4.000000000,OFST,0.000000000,PHASE,0.000000000,WAVEDATA,"
  cmmd += "\xFF"
  
  values = [0x1FFF] * 8192
  values += [0x2000] * 8192
  
  bin_values = ""
  for i in range(len(values)):
    bin_values += chr((values[i] >> 8) & 0xFF)
    bin_values += chr(values[i] & 0xFF)

  my_instrument.write_raw(cmmd + bin_values)

  print my_instrument.write('C1:ARWV INDEX,50')

  my_instrument.close()