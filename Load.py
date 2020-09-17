import sys, io, os
from utils import app_config
from sqlalchemy import create_engine, Table
from tableloader.tables import metadataCreator
from tableloader.tableFunctions import typeMaterials
from tableloader.tableFunctions import dogmaTypes
from tableloader.tableFunctions import dogmaEffects
from tableloader.tableFunctions import dogmaAttributes
from tableloader.tableFunctions import dogmaAttributeCategories
from tableloader.tableFunctions import blueprints
from tableloader.tableFunctions import marketGroups
from tableloader.tableFunctions import metaGroups
from tableloader.tableFunctions import controlTowerResources
from tableloader.tableFunctions import categories
from tableloader.tableFunctions import certificates
from tableloader.tableFunctions import graphics
from tableloader.tableFunctions import groups
from tableloader.tableFunctions import icons
from tableloader.tableFunctions import skins
from tableloader.tableFunctions import types
from tableloader.tableFunctions import bsdTables
from tableloader.tableFunctions import universe
from tableloader.tableFunctions import volumes

# Fire up application configuration
config = app_config.read()

# Check required parameters
if len(sys.argv) < 2:
    print("usage: Load.py destination")
    print("destination must be one of: ("+"|".join(config.options('Database'))+")")
    exit()

database = sys.argv[1]

if len(sys.argv) == 3:
    language = sys.argv[2]
else:
    language = 'en'

destination = config.get('Database', database)
source_path = config.get('Files', 'sourcePath')

print("Connecting to storage engine: " + database)

try:
    engine = create_engine(destination)
    connection = engine.connect()
except Exception as e:
    print(e)
    exit()

schema = None
if database == "postgresschema":
    schema = "evesde"

metadata = metadataCreator(schema)

print("Creating Tables")

metadata.drop_all(engine, checkfirst=True)
metadata.create_all(engine, checkfirst=True)

print("Created Tables")
print("Starting yaml imports")

typeMaterials.importyaml(connection, metadata, source_path, language)
dogmaTypes.importyaml(connection, metadata, source_path, language)
dogmaEffects.importyaml(connection, metadata, source_path, language)
dogmaAttributes.importyaml(connection, metadata, source_path, language)
dogmaAttributeCategories.importyaml(connection, metadata, source_path, language)
blueprints.importyaml(connection, metadata, source_path)
marketGroups.importyaml(connection, metadata, source_path, language)
metaGroups.importyaml(connection, metadata, source_path, language)
controlTowerResources.importyaml(connection, metadata, source_path, language)
categories.importyaml(connection, metadata, source_path, language)
certificates.importyaml(connection, metadata, source_path)
graphics.importyaml(connection, metadata, source_path)
groups.importyaml(connection, metadata, source_path, language)
icons.importyaml(connection, metadata, source_path)
skins.importyaml(connection, metadata, source_path)
types.importyaml(connection, metadata, source_path, language)
bsdTables.importyaml(connection, metadata, source_path)
universe.importyaml(connection, metadata, source_path)
universe.buildJumps(connection, database)
volumes.importVolumes(connection, metadata, source_path)
universe.fixStationNames(connection, metadata)

print("Finished")
