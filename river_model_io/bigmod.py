import pandas as pd
import numpy as np
from datetime import datetime
import os

def load_bigmod(fn:str) -> (pd.DataFrame,pd.DataFrame):
  '''
  Read a bigmod CSV file

  Returns
    * attributes - Pandas Dataframe of the various metadata attributes in the file
    * data - Pandas dataframe of the time series
  '''
  import pandas as pd
  import re
  import io
  text = open(fn, 'r').read()

  r = re.compile('\nEOC,*\n')
  first_header, remaining = r.split(text)
  attribute_names = first_header.splitlines()[-1]

  lines = remaining.splitlines()
  n_cols = int(lines[0])
  attribute_vals = lines[1:n_cols+1]

  attributes = pd.read_csv(io.StringIO('\n'.join([attribute_names]+attribute_vals)))

  regular_csv = '\n'.join([lines[n_cols+1]] + lines[n_cols+3:])
  data = pd.read_csv(io.StringIO(regular_csv))
  data['Date'] = pd.to_datetime(data.Year*10000+data.Mn*100+data.Dy,format='%Y%m%d')
  data = data.set_index('Date')
  return attributes, data

def save_bigmod(fn:str, meta:pd.DataFrame, data:pd.DataFrame):
  raise Exception('Writing bigmod files not supported')

def replace_values(src_fn:str, dest_fn:str, values:np.array, column:int, start:datetime):
  assert not os.path.exists(dest_fn) or not os.path.samefile(src_fn,dest_fn)

  src = open(src_fn, 'r')
  dest = open(dest_fn,'w')

  while True:
    line = src.readline()
    dest.write(line)
    if line.startswith('EOH'):
      if len(line)<=4:
        # Main data header on next line
        header = src.readline()
        dest.write(header)
      break

  while True:
    line = src.readline()
    dd,mm,yyyy = [int(txt) for txt in line.split(',')[:3]]
    if yyyy==start.year and mm==start.month and dd==start.day:
      break
    dest.write(line)
  
  for val in values:
    components = line.split(',')
    components[column] = str(val)
    dest.write(','.join(components)+'\n')

    line = src.readline()

  dest.write(line)

  while line:
    line = src.readline()
    dest.write(line)

  src.close()
  dest.close()
