import os
import glob
from utils import yaml_stream
from sqlalchemy import Table
import sqlalchemy

def importyaml(connection, metadata, source_path):
    print("Importing BSD Tables")

    files = glob.glob(os.path.join(source_path, 'bsd', '*.yaml'))
    for file in files:

        head, tail = os.path.split(file)
        tablename = tail.split('.')[0]
        tablevar = Table(tablename, metadata)
        print("Importing {}".format(file) + ' into ' + tablename)

        with open(file, 'r') as yamlstream:

            print("Processing of Yaml starting")
            trans = connection.begin()

            for record in yaml_stream.read_by_list(yamlstream):
                if record:
                    try:
                        connection.execute(tablevar.insert().values(record))
                    except sqlalchemy.exc.IntegrityError as err:
                        print("{} skipped {} ({})".format(tablename, record, err))
            trans.commit()
