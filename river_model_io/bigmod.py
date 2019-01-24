import pandas as pd

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

    r = re.compile('\nEOC\n')
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
