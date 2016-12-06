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

  # query the instrument
  print my_instrument.query('*IDN?')

  # my_instrument.write('C1:OUTP ON')
  #print my_instrument.query('ARWV?')
  # my_instrument.write('BUZZ ON')
  # my_instrument.write('ARWV INDEX,50')
  # my_instrument.encoding='latin-1'
  #data = map(ord,my_instrument.query('WVDT M50?'))
  # str=my_instrument.query('WVDT M26?')
  # data = map(ord,str)
  # #print len(data)

  # offset = str.find("WAVEDATA,")+9
  # #offset = len(data) -32768 +1

  # #print offset
  # #for i in range(16384):
  # #    v = data[(i*2)+offset] + (data[(i*2)+offset+1]*256)
  # #    if (v>8192):
  # #        v=v-16384
  # #    print "%d,%d " % (i,v)

  # wdata = []
  # for i in range(16384):
      # a = i % 1000
      # wdata.append(a %256)
      # wdata.append(a /256)
  # #for i in range(100):
  # #    print i,wdata[i]
  # #d=''
  # #for i in range(16384):
  # #    a=i % 1000
  # #    d = d + chr(a%256) + chr(a/256)
  # #str=my_instrument.write_binary_values('WVDT, M50, WVNM, MYWAVE, LENGTH, 32KB, TYPE, 5, WAVEDATA,',d,datatype='h')
  # str=my_instrument.write_ascii_values('WVDT, M50, WVNM, MYWAVE, LENGTH, 32KB, TYPE, 5, WAVEDATA,',wdata,converter='x')
  # print str   

  # my_instrument.query('WVDT M50?')

  my_instrument.write('WVDT? M50')
  data = my_instrument.read_raw()
  # dump_ascii_hex(data)
  
  # strip off actual waveform data
  waveform_str_to_find = "WAVEDATA,"
  waveform_data_index = data.find(waveform_str_to_find) + len(waveform_str_to_find)
  # make sure that the index is odd (waveform data have to be aligned in actual USB packet)
  if ((waveform_data_index % 2) == 0):
    waveform_data_index += 1
  
  waveform_data = data[waveform_data_index:]

  # now try to write command to modify the waveform
  cmmd = "C1:WVDT M50,WVNM,wave2,TYPE,5,LENGTH,32KB,FREQ,1000.000000000,AMPL,3.000000000,OFST,0.000000000,PHASE,0.000000000,WAVEDATA,"
  cmmd += "\x00"
  whole_cmmd = cmmd + waveform_data
  my_instrument.write_raw(whole_cmmd)
  
  # values = [0x1FFF] * 1024
  # values += [0x2000] * 1024
  # my_instrument.write_binary_values(cmmd, values, datatype="H", is_big_endian = True)
  
  print(waveform_data_index)
  print(type(data))
  print (len(data))

  print my_instrument.write('C1:ARWV INDEX,51')

  my_instrument.close()