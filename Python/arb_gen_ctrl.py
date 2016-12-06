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
  # print my_instrument.query('*IDN?')

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
  dump_ascii_hex(data)
  print(type(data))
  print (len(data))

  my_instrument.close()