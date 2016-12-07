
class BkPrecision4053:
  """
  Class implementing methods allowing to use py-visa to work with
  BK Precision 4053 Arbitrary Waveform Generator
  """
  
  def __init__(self, rm, rm_open_string):
    """
    Initialization of the instrument. The function
    requires two arguments:
    rm - py-visa Resource Manager instance
    rm_open_string - the string required to open communication with 4053 in Resource Manager
    """
    self.instrument = rm.open_resource(rm_open_string)
    self.instrument_open = True
    
    self.instrument.write_termination = "\n"  # by default the commands should be ended with single Line Feed character
    self.instrument.read_termination = "\n"  # by default the commands replies should be ended with single Line Feed character
    
  # check if correct instrument is connected
    idn_string = self.instrument.query("*IDN?")
    if (idn_string.find("BK Precision,4053") == -1):
      raise ValueError("BK Precision 4053 AWG is not detected")
    
  def __enter__(self):
    """
    Object method called when entering the block surrounded by Python "with" statement
    """
    return self
    
  def __exit__(self, exc_type, exc_value, traceback):
    """
    Method called when exiting the block surrounded by Python "with" statement.
    Please note that it will also be called if Python exception has been thrown.
    This fact allow us to clean up after ourselves
    """
    if (self.instrument_open == True):
      self.instrument.close()
      self.instrument_open = False
    
  def __del__(self):
    """
    Method called when the object is deleted. Allows for cleaning up after ourselves
    """
    if (self.instrument_open == True):
      self.instrument.close()
      self.instrument_open = False

  def is_connected(self):
    """
    Method checks if correct instrument is connected
    """
    if (idn_string.find("BK Precision,4053") != -1):
      return True
    else:
      return False
      
  def identify(self):
    """
    Method queries the instrument to find out details about what instrument is connected
    """
    print (self.instrument.query("PROD MODEL?"))
    print (self.instrument.query("IDN-SGLT-PRI?"))
    print (self.instrument.query("PROD BAND?"))

  def define_arbitrary_waveform(self, mem_index, data, name = None, freq_hz = 1000.0, amp_vpp = 1.0, offset_v = 0.0, phase_deg = 0.0):
    """
    Method defines and stores arbitrary waveform in one of memories in BK Precision 4053.
    Arguments:
      mem_index - index specifying which memory should be used for storage. 4053 has 10 memories indexed from 0 to 9
      data -  indexable object (list, numpy array) containing floating point samples defining arbitrary waveform. For 4053 it has to containing
              exactly 16384 samples. These samples define only the shape of the waveform, amplitude and repetitions frequency is defined by other arguments
      name -  waveform name. If not provided, standard name is assigned. If provided, it has to be no more than 5 characters long
      freq_hz - waveform repetition frequency given in Hz
      amp_vpp - waveform peak-to-peak amplitude given in V
      offset_v  - waveform DC offset given in V
      phase_deg - waveform phase shift given in degrees
    """

  # check if given arguments values are correct
    if ((mem_index < 0) or (mem_index > 9)):
      raise ValueError("Arbitrary waveform index {0:d} is outside <0,9> range".format(mem_index))
    
    if (len(data) != 16384):
      raise ValueError("Arbitrary waveform data lenght = {0:d} bytes has to be equal to 16384".format(len(data)))
    
    if (name != None):
      if not (type(name) is str):
        raise ValueError("Arbitrary waveform name has to be a string")
      elif (len(name) > 5):
        raise ValueError("Arbitrary waveform name can be up to 5 characters long")

    if ((name != None) and (len(name) > 5)):
      raise ValueError("Arbitrary waveform name can be up to 5 characters long")
    
    if (freq_hz < 0.0):
      raise ValueError("Arbitrary waveform frequency can't be negative")
    elif (freq_hz > 10000000.0):
      raise ValueError("Arbitrary waveform frequency can't be more than 10MHz")
    
    if (amp_vpp <= 0.0):
      raise ValueError("Arbitrary waveform amplitude has to be positive")
    elif (amp_vpp > 10.0):
      raise ValueError("Arbitrary waveform amplitude can't be more than 10V")
    
    if ((offset_v < -5.0) or (offset_v > 5.0)):
      raise ValueError("Arbitrary waveform offset has to be within (-5V, +5V) range")
    
    if ((phase_deg < -360.0) or (phase_deg > 360.0)):
      raise ValueError("Arbitrary waveform phase has to be withing <-360, 360> degrees range")
      
  # arguments are fine, so prepare their string version in the right format
    mem_index_str = "M{0:2d}".format(mem_index + 50)
    if (name == None):
    # create default name if necessary
      name_str = "wave{0:1d}".format(mem_index)
    else:
    # name was provided, so make sure that it is 5 characters long
      name_str = name
      if (len(name_str) < 5):
        added_spaces = 5-len(name_str)
        for i in range(added_spaces):
          name_str.join(" ")

    freq_str = "{0:.9f}".format(freq_hz)
    amp_str = "{0:.9f}".format(amp_vpp)
    offset_str = "{0:.9f}".format(offset_v)
    phase_str =  "{0:.9f}".format(phase_deg)
    
  # prepare the command for the generator
    cmmd = "WVDT " + mem_index_str + ","
    cmmd += "WVNM," + name_str + ","
    cmmd += "TYPE,5,LENGTH,32KB,"
    cmmd += "FREQ," + freq_str + ","
    cmmd += "AMPL," + amp_str + ","
    cmmd += "OFST," + offset_str + ","
    cmmd += "PHASE," + phase_str + ","
    cmmd += "WAVEDATA,"
  
  # and the waveform data
  # first find the minimum and maximum data value and scale the whole set accordingly
    min_val = min(data)
    max_val = max(data)
    scale = max(abs(min_val), abs(max_val))

  # the instrument requires the waveform values to be provides as 14 bit signed integer values
  # for example minimum negative voltage is represented as 0x2000 and maximum positive voltage is represented as 0x1FFF

    bin_data_str = ""
    for i in range(len(data)):
      sample_float = data[i]
      sample_float_scaled_int14 = (sample_float * 8191.0) / scale  # multiplying by 0x1FFF = 8191 rather than 0x2000 = 8192 will prevent overflow
      sample_int_scaled_int14 = (int)(sample_float_scaled_int14)
      u2_int14_val = sample_int_scaled_int14 & 0x3FFF
      bin_data_str += chr((u2_int14_val >> 8) & 0xFF)
      bin_data_str += chr(u2_int14_val & 0xFF)

  # for some reason (probably a bug in BK precision software), WVDT command data length has to be one byte less that what
  # one expects it to be. Failing to strip one byte off results in the generator ignoring the WVDT command completely
    bin_data_str = bin_data_str[:-1]

  # finally we are ready to send the command to the instrument
    self.instrument.write_raw(cmmd + bin_data_str)

  def assign_arbitrary_waveform_to_channel(self, channel_no, mem_index):
    """
    Method assigns arbitrary waveform to specific 4053 output channel
    Arguments:
      channel_no - 4053 output channel number. Can either take value 1 or 2
      mem_index - index specifying which memory should be used for storage. 4053 has 10 memories indexed from 0 to 9
    """
  
  # check if given arguments values are correct
    if ((channel_no < 1) or (channel_no > 2)):
      raise ValueError("Arbitrary waveform generator channel number can either be set to 1 or 2")
  
    if ((mem_index < 0) or (mem_index > 9)):
      raise ValueError("Arbitrary waveform index {0:d} is outside <0,9> range".format(mem_index))
    
  # arguments are fine, so prepare their string version in the right format
    channel_no_str = "C{0:1d}".format(channel_no)
    mem_index_str = "M{0:2d}".format(mem_index + 50)
    
    cmmd = channel_no_str + ":ARWV INDEX," + mem_index_str
    self.instrument.write(cmmd)

  def channel_command(self, channel_no, enable = True, load_50_ohm = False):
    """
    Method controls specific 4053 output channel
    Arguments:
      channel_no - 4053 output channel number. Can either take value 1 or 2
      enable - if True, the channel gets enabled. Channel gets disabled otherwise
      load_50_ohm - if True 4053 expects to drive 50R load. Otherwise 4053 expects to drive high impedance load
    """
  
  # check if given arguments values are correct
    if ((channel_no < 1) or (channel_no > 2)):
      raise ValueError("Arbitrary waveform generator channel number can either be set to 1 or 2")
    
    cmmd = "C{0:1d}:".format(channel_no)

    cmmd += "OUTP "
    if (enable == True):
      cmmd += "ON,"
    else:
      cmmd += "OFF,"

    cmmd += "LOAD,"
    if (load_50_ohm == True):
      cmmd += "50"
    else:
      cmmd += "HZ"

    self.instrument.write(cmmd)
      
    