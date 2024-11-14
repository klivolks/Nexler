from nexler.utils import dir_util, str_util, file_util
from daba.Mongo import collection


class Migrate:
    def __init__(self):
        self.tables = dir_util.list_files_by_type('migrations/', 'json')

    def _migrate(self):
        for table in self.tables:
            col = collection(table)
            current_path = dir_util.app_path()
            file_path = current_path + '/migrations/' + str(table) + '.json'
            docs_to_insert = str_util.parse(file_util.read_file(file_path), 'json')

            for doc in docs_to_insert:
                # Check if data already exists in the database.
                existing_doc = col.getOne(doc)
                if existing_doc is None:
                    # Data does not exist, so we can insert it.
                    response = col.put(doc)
                    print(f'Data migrated to {table} with {response.inserted_id}')
                else:
                    print(f'Data already exists in {table}. No insertion was performed.')
        print('Migration successful...')
