import gviz_api as GV 
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from lebanco import *
import datetime

env = Environment(loader=FileSystemLoader( 'templates'))

def gera_javascript_date(d):
    """
    Receives a datetime.date object and returns a string
    to generate an equivalent javascript date instance
    """
    assert isinstance(d, datetime.date)
    return "new Date(%s,%s,%s)"%(d.year, d.month, d.day)

## Google datasource generators
def create_ts_data_source(cnames,data,types):
    '''
    Creates a JSON datasource compatible with google visualization API
    Annotated time series.
    First column type must be date.
    cnames: tuple of strings. column names
    data: list of data tuples of the same size as cnames. each tuple is a line in a table
    types: tuple of types for each column using the standard of visualization API
    '''
    description = dict([(n,(t,n.title())) for n,t in zip(cnames,types)])
    dados =[]
    for d in data:
        dados.append(dict(zip(cnames,d)))
    data_table = GV.DataTable(description)
    data_table.LoadData(dados)
    return data_table
    
def create_motion_chart_data_source(data, cnames, tipos):
    """
    Creates a JSON datasource compatible with google visualization API
    Motion chart.
    First column type must be Strings with entity names.
    Second column must be date (Javascript date instances) or numeric year values.
    Other columns may be numeric or strings
    cnames: tuple of strings. column names
    data: list of data tuples of the same size as cnames. each tuple is a line in a table
    tipos: tuple of types for each column using the standard of visualization API
    """
    description = dict([(n,(t,n.title())) for n,t in zip(cnames,tipos)])
    dados =[]
    for d in data:
        assert isinstance(d[0], str)
        assert isinstance(d[1], (datetime.date, int))
        d[1] = gera_javascript_date(d[1]) if isinstance(d[1], datetime.date) else d[1]
        dados.append(dict(zip(cnames,d)))
    data_table = GV.DataTable(description)
    data_table.LoadData(dados)
    return data_table
    

def create_map_data_source(data, vname):
    '''
    Creates a JSON datasource compatible with ''geomap'' from google visualization API
    data: list of data tuples (lat,long,number,'hoverstring')
    '''
    description = {"LATITUDE":('number','Latitude'),
                   "LONGITUDE":('number','Longitude'),
                   "VALUE":('number',vname),
                   "HOVER":('string','HoverText')
                }
    dados =[]
    for d in data:
        try:
            dados.append({"LATITUDE":d[0],
                    "LONGITUDE":d[1],
                    "VALUE":d[2],
                    "HOVER":d[3]
            })
        except:
            pass
    data_table = GV.DataTable(description)
    data_table.LoadData(dados)
    return data_table
    
def motion_chart(title, data,  vnames, tipos):
    data_table = create_map_data_source(data, vname, tipos)
    json = data_table.ToJSon(columns_order=vnames, order_by=vnames[1])
    template = env.get_template('motion_chart.html')
    data = {'json' : json,
                'title':title
            }
    return template.render(**data)
    
def blob_map(title,country, data,  vname):
    """
    generate a google visualization blob map.
    country: country code e.g. BR
    """
    data_table = create_map_data_source(data, vname)
    json = data_table.ToJSon(columns_order=("LATITUDE", "LONGITUDE","VALUE","HOVER"), order_by="VALUE")
    template = env.get_template('map.html')
    data = {'json' : json,
                'country':country.upper(),
                'title':title
            }
    return template.render(**data)
    
def annot_TS(title, dates, values, snames, anot=[], anot_text=[]):
    '''
    Generates an annotated times series

    :Parameters:
        - `title`: String with chart title
        - `dates`: list of dates.
        - `values`: list of lists of values for each variable series.
        - `snames`: List of names for each series
        - `anot`: positions of annotations
        - `anot`: text of annotations
    '''
    if isinstance(dates[0], int): #checking date format
        dt = ['number']
    else: 
        dt = ['date']
        
    cnames = ['Time']
    if anot:
        for n, s in enumerate(snames):
            cnames += [s, 'label%s'%n, 'text%s'%n]
        data = [dates]
        types = dt+(['number', 'string','string']*len(snames))
        data += values +[anot]+[anot_text]

        data = zip(*data)
    else:
        cnames += snames
        data = [dates]+ values
        data = zip(*data)
        types = dt +(['number']*len(values))
    data_table = create_ts_data_source(cnames, data, types)
    json = data_table.ToJSon(columns_order=cnames, order_by=cnames[1])
    template = env.get_template('series.html')
    data = {'json' : json,'title':title}
    return template.render(**data)
     
## Formatadores de dados para visualizacoes Protoviz 
