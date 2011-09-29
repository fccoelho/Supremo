import glob
from pymongo import Connection
import gridfs

ims = glob.glob("*.jpg")
db = Connection('127.0.0.1').Supremo
fs = gridfs.GridFS(db)

for fn in ims:
    with open(fn,'rb') as f:
        fs.put(f,filename=fn)
        

