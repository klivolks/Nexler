import os
import traceback

from .model_import import import_model
from .schema import create_schema


def create_model(args):
    from nexler.utils import str_util, file_util
    try:
        moduleName = str_util.pascal_case(args.moduleName)
        model_file_path = f"app/models/{moduleName}.py"
        if os.path.exists(model_file_path):
            print(f"Model {moduleName} already exists.")
            import_model(args)
            return
        class_variables = ""
        if not args.blank:
            variables_json_file = args.moduleName + '.json'

            # Construct the path for the JSON file
            variables_json_path = f"app/models/variables/{variables_json_file}"

            if os.path.exists(variables_json_path):
                variables_json = file_util.read_file(variables_json_path)
                variables = str_util.parse(variables_json, 'json')
            else:
                variables = [
                    {"Variable": "data", "Format": "str", "Required": False},
                    {"Variable": "Status", "Format": "str", "Required": True, "Default": "active"},
                    {"Variable": "CreatedAt", "Format": "datetime", "Required": False,
                     "Default": "dt_util.get_current_time()"},
                    {"Variable": "UpdatedAt", "Format": "datetime", "Required": True,
                     "Default": "dt_util.get_current_time()"},
                    {"Variable": "CreatedBy", "Format": "ObjectId", "Required": False, "Default": "Field(default_factory=lambda: ObjectId(user.Id) if hasattr(user, 'Id') else None)"},
                    {"Variable": "isDeleted", "Format": "bool", "Required": True, "Default": False}
                ]

            for index, variable in enumerate(variables):
                var_name = variable['Variable']
                var_type = variable.get('Format', 'str')
                var_required = variable.get('Required', False)

                var_type = var_type if var_required else f'Optional[{var_type}]'
                if index == 0:
                    class_variables += f"""{var_name}: {var_type}"""
                else:
                    class_variables += f"""
    {var_name}: {var_type}"""
                if variable.get('Default', None) or var_type == "bool":
                    class_variables += f" = '{variable.get('Default', None)}'" if var_type == "str" else f" = {variable.get('Default', None)}"

            class_definition = f"""from nexler.model.base_model import MongoBaseModel
from nexler.model.base_class import BaseClass
from datetime import datetime
from bson import ObjectId
from daba.Mongo import collection
from typing import Optional
from pydantic import Field
from nexler.utils import dt_util
from nexler.services.AuthService import user


class Model(MongoBaseModel):
    {class_variables}


data_collection = collection("{moduleName}")

handler = BaseClass(Model, data_collection)
"""
        else:
            class_definition = f"""from daba.Mongo import collection


data_collection = collection("{moduleName}")
"""

        # Create the model file and write the class definition to it
        file_util.write_file(model_file_path, class_definition)

        print(f"Model '{moduleName}' created.")
        import_model(args)
    except Exception as e:
        print(f"An error occurred while creating the model: {e} Trace: {traceback.format_exc()}")
