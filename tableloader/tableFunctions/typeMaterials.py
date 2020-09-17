import sys
import os
from sqlalchemy import Table
from yaml import load

try:
    from yaml import CSafeLoader as SafeLoader
    print("Using CSafeLoader")
except ImportError:
    from yaml import SafeLoader
    print("Using Python SafeLoader")


def importyaml(connection, metadata, source_path, language='en'):
    print("Importing Type Materials")
    invTypeMaterials = Table('invTypeMaterials', metadata)
    print("opening Yaml")
    trans = connection.begin()

    with open(
        os.path.join(source_path, 'fsd', 'typeMaterials.yaml'), 'r'
    ) as yamlstream:
        print("importing")
        materials = load(yamlstream, Loader=SafeLoader)
        print("Yaml Processed into memory")
        for typeid in materials:
            for material in materials[typeid]['materials']:
                connection.execute(
                    invTypeMaterials.insert(),
                    typeID=typeid,
                    materialTypeID=material['materialTypeID'],
                    quantity=material['quantity']
                )
    trans.commit()
