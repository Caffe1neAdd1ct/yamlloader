import os
from utils import yaml_stream
from sqlalchemy import Table


def importyaml(connection, metadata, source_path):
    eveIcons = Table('eveIcons', metadata)
    print("Importing Icons")

    trans = connection.begin()

    with open(
        os.path.join(source_path, 'fsd', 'groupIDs.yaml'), 'r'
    ) as yamlstream:
        for icon in yaml_stream.read_by_any(yamlstream):
            for icon_id, icon_details in icon.items():
                connection.execute(
                    eveIcons.insert(),
                    iconID=icon_id,
                    iconFile=icon_details.get('iconFile', ''),
                    description=icon_details.get('description', '')
                )
    trans.commit()
