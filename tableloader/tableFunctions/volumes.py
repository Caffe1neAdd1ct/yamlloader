import os
import csv
from sqlalchemy import Table,literal_column,select


def importVolumes(connection, metadata, source_path):
    invVolumes = Table('invVolumes', metadata)
    invTypes = Table('invTypes', metadata)

    with open(
        os.path.join(source_path, 'invVolumes1.csv'), 'r'
    ) as groupVolumes:
        volumereader = csv.reader(groupVolumes, delimiter=',')
        for group in volumereader:
            connection.execute(
                invVolumes.insert().from_select(['typeID','volume'], select([invTypes.c.typeID,literal_column(group[0])]).where(invTypes.c.groupID == literal_column(group[1])))
            )

    with open(os.path.join(source_path, 'invVolumes2.csv'), 'r') as groupVolumes:
        volumereader = csv.reader(groupVolumes, delimiter=',')
        for group in volumereader:
            connection.execute(
                invVolumes.insert(),
                typeID=group[1],
                volume=group[0]
            )
