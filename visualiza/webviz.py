import gviz_api as GV 
import jinja2
from lebanco import *


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
    
def blob_map(title,country, data,  vname):
    """
    generate a google visualization blob map.
    country: country code e.g. BR
    """
    data_table = create_map_data_source(data, vname)
    json = data_table.ToJSon(columns_order=("LATITUDE", "LONGITUDE","VALUE","HOVER"), order_by="VALUE")
    return render_to_string("map.html", {'json' : json,'country':country.upper(),'title':title})
    
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
    cnames = ['Time']
    if anot:
        for n, s in enumerate(snames):
            cnames += [s, 'label%s'%n, 'text%s'%n]
        data = [dates]
        types = ['date']+(['number', 'string','string']*len(snames))
        data += values +[anot]+[anot_text]
#        for n, s in enumerate(values):
#            data.extend([s, anot[n], anot_text[n]])
        data = zip(*data)
    else:
        cnames += snames
        data = [dates]+ values
        data = zip(*data)
        types = ['date'] +(['number']*len(values))
    data_table = create_ts_data_source(cnames, data, types)
    json = data_table.ToJSon(columns_order=cnames, order_by=cnames[1])
    return render_to_string("series.html", {'json' : json,'title':title})
