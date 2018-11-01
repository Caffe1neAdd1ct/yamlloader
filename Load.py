from sqlalchemy import create_engine,Table
import warnings
import sys





warnings.filterwarnings('ignore', '^Unicode type received non-unicode bind param value')


if len(sys.argv)<2:
    print("Load.py destination")
    exit()


database=sys.argv[1]


import configparser, os
fileLocation = os.path.dirname(os.path.realpath(__file__))
inifile=fileLocation+'/sdeloader.cfg'
config = configparser.ConfigParser()
config.read(inifile)
destination=config.get('Database',database)
sourcePath=config.get('Files','sourcePath')






from tableloader.tableFunctions import *



print("connecting to DB")


engine = create_engine(destination)
connection = engine.connect()



from tableloader.tables import metadataCreator

schema=None
if database=="postgresschema":
    schema="evesde"

metadata=metadataCreator(schema)



print("Creating Tables")

metadata.drop_all(engine,checkfirst=True)
metadata.create_all(engine,checkfirst=True)

print("created")

import tableloader.tableFunctions

blueprints.importyaml(connection,metadata,sourcePath)
categories.importyaml(connection,metadata,sourcePath)
certificates.importyaml(connection,metadata,sourcePath)
graphics.importyaml(connection,metadata,sourcePath)
groups.importyaml(connection,metadata,sourcePath)
icons.importyaml(connection,metadata,sourcePath)
skins.importyaml(connection,metadata,sourcePath)
types.importyaml(connection,metadata,sourcePath)
bsdTables.importyaml(connection,metadata,sourcePath)
universe.importyaml(connection,metadata,sourcePath)
universe.buildJumps(connection,database)
universe.fixStationNames(connection,metadata)
volumes.importVolumes(connection,metadata,sourcePath)

print("Finished")