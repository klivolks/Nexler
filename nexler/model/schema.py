import os
import traceback


def create_schema(args):
    from nexler.utils import file_util
    try:
        schemaName = args.moduleName
        variables_json_path = f"app/models/variables/{schemaName}.json"
        if os.path.exists(variables_json_path):
            print(f"Schema {schemaName} already exists!")
        else:
            content = """[
    {"Variable": "data", "Format": "str", "Required": false},
    {"Variable": "Status", "Format": "str", "Required": true, "Default": "active"},
    {"Variable": "CreatedAt", "Format": "datetime", "Required": false, "Default": "Field(default_factory=lambda: dt_util.get_current_time())"},
    {"Variable": "UpdatedAt", "Format": "datetime", "Required": true, "Default": "Field(default_factory=lambda: dt_util.get_current_time())"},
    {"Variable": "CreatedBy", "Format": "Union[ObjectId, str]", "Required": false, "Default": "Field(default_factory=lambda: ObjectId(user.Id) if hasattr(user, 'Id') else None)"},
    {"Variable": "isDeleted", "Format": "bool", "Required": true, "Default": false}
]"""
            file_util.write_file(variables_json_path, content)
            print(f"Empty schema {schemaName} created successfully!")
    except Exception as e:
        print(f"An error occurred while creating the schema: {e} Trace: {traceback.format_exc()}")