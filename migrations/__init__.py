from app.utils import dir_util, file_util, str_util
from daba.Mongo import collection


class Migrate:
    def __init__(self):
        self.tables = dir_util.list_files_by_type('migrations/', 'json')

    def _migrate(self):
        for table in self.tables:
            col = collection(table)
            current_path = dir_util.app_path()
            file_path = current_path + '/migrations/' + str(table) + '.json'
            doc = str_util.parse(file_util.read_file(file_path), 'json')
            response = col.putMany(doc)
            print(f'Data migrated to {table} with {response.insertedIds}')
        print('Migration successful...')

