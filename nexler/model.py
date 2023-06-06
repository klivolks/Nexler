import os
import traceback
from app.utils import file_util, str_util


def create_model(args):
    try:
        moduleName = str_util.capitalize(args.moduleName)
        variables_json_file = args.moduleName + '.json'

        # Construct the path for the JSON file
        variables_json_path = f"app/models/variables/{variables_json_file}"

        if os.path.exists(variables_json_path):
            variables_json = file_util.read_file(variables_json_path)
            variables = str_util.parse(variables_json, 'json')
        else:
            variables = [{"Variable": "_id", "Format": "str", "Required": True},
                         {"Variable": "data", "Format": "str", "Required": False}]

        # Construct the class variables and save variables
        class_variables = ""
        init_variables = ""
        save_variables = ""
        property_setter = ""
        for index, variable in enumerate(variables):
            var_name = variable['Variable']
            var_type = variable.get('Format', 'str')
            var_required = variable.get('Required', False)

            default_value = None if not var_required else f'{var_type}'
            class_variables += f", {var_name}={default_value}"
            init_variables += f"\n        self.{var_name} = {var_name}"
            if var_type == 'ObjectId':
                property_setter += f"""
    @property
    def {var_name}(self):
        return self.__id

    @{var_name}.setter
    def {var_name}(self, value):
        if value is not None:
            self._{var_name} = ObjectId(value)
        else:
            self._{var_name} = None
"""

            if var_name != '_id':
                save_variables += f"'{var_name}': self.{var_name}"
                if index < len(variables) - 1:  # add a comma only if it's not the last variable
                    save_variables += ",\n                "

        # Construct the file path for model
        model_file_path = f"app/models/{moduleName}.py"

        # Check if model already exists
        if os.path.exists(model_file_path):
            if args.logic:
                if args.main:
                    # Modify the import statement in the logic file
                    logic_file_path = f"app/logic/{args.main}/{args.logic}.py"
                else:
                    logic_file_path = f"app/logic/{args.logic}/{args.logic}.py"
                logic_file_content = file_util.read_file(logic_file_path)

                import_statement_start = "from app.models import "

                if import_statement_start in logic_file_content:
                    import_start_index = logic_file_content.index(import_statement_start) + len(import_statement_start)
                    import_end_index = logic_file_content.index("\n", import_start_index)

                    # Grab the existing imports
                    existing_imports = logic_file_content[import_start_index:import_end_index].split(", ")

                    # If module isn't already imported, add it
                    if moduleName not in existing_imports:
                        existing_imports.append(moduleName)

                    # Reconstruct the import statement
                    new_import_statement = import_statement_start + ", ".join(existing_imports) + "\n"

                    # Replace the old import statement with the new one
                    logic_file_content = logic_file_content.replace(
                        logic_file_content[import_start_index - len(import_statement_start):import_end_index],
                        new_import_statement)
                else:
                    # If there was no import statement, add one
                    logic_file_content = import_statement_start + moduleName + "\n" + logic_file_content

                # Write the updated content back to the file
                file_util.write_file(logic_file_path, logic_file_content)
            print(f"Model '{moduleName}' already exists. Added to logic {args.logic}")
            return

        # Construct the class definition with importing the collection from daba.Mongo
        class_definition = f"""from bson import ObjectId
from daba.Mongo import collection


class {moduleName}:
    {moduleName.lower()} = collection("{moduleName}")

    def __init__(self{class_variables}):
        {init_variables}

    def save(self):
        if self._id is None:  
            data = {{
                {save_variables}
            }}
            # Remove None values from data
            data = {{k: v for k, v in data.items() if v is not None}}
            result = self.{moduleName.lower()}.put(data)
            self._id = result.inserted_id  # Update the ID with the newly generated ID.
        else:  # This user already exists, so update it.
            data = {{
                {save_variables}
            }}
            # Remove None values from data
            data = {{k: v for k, v in data.items() if v is not None}}
            result = self.{moduleName.lower()}.set({{'_id': ObjectId(self._id)}},data)

    def get(self, query):
        return self.{moduleName.lower()}.get(query)

    def getOne(self, query):
        return self.{moduleName.lower()}.getOne(query)

    def update(self, query, new_data):
        return self.{moduleName.lower()}.set(query, new_data)

    def delete(self, query):
        return self.{moduleName.lower()}.deleteOne(query)

    def count(self, query):
        return self.{moduleName.lower()}.count(query)
    {property_setter}
"""

        # Create the model file and write the class definition to it
        file_util.write_file(model_file_path, class_definition)

        if args.logic:
            if args.main:
                # Modify the import statement in the logic file
                logic_file_path = f"app/logic/{args.main}/{args.logic}.py"
            else:
                logic_file_path = f"app/logic/{args.logic}/{args.logic}.py"
            logic_file_content = file_util.read_file(logic_file_path)

            import_statement_start = "from app.models import "

            if import_statement_start in logic_file_content:
                import_start_index = logic_file_content.index(import_statement_start) + len(import_statement_start)
                import_end_index = logic_file_content.index("\n", import_start_index)

                # Grab the existing imports
                existing_imports = logic_file_content[import_start_index:import_end_index].split(", ")

                # If module isn't already imported, add it
                if moduleName not in existing_imports:
                    existing_imports.append(moduleName)

                # Reconstruct the import statement
                new_import_statement = import_statement_start + ", ".join(existing_imports) + "\n"

                # Replace the old import statement with the new one
                logic_file_content = logic_file_content.replace(
                    logic_file_content[import_start_index - len(import_statement_start):import_end_index],
                    new_import_statement)
            else:
                # If there was no import statement, add one
                logic_file_content = import_statement_start + moduleName + "\n" + logic_file_content

            # Write the updated content back to the file
            file_util.write_file(logic_file_path, logic_file_content)

        # Modify __init__.py in app/models/
        init_file_path = "app/models/__init__.py"
        init_file_content = file_util.read_file(init_file_path)
        model_import = f"from .{moduleName} import {moduleName}"

        if model_import not in init_file_content:
            init_file_content += model_import + "\n"
            file_util.write_file(init_file_path, init_file_content)

        print(f"Model '{moduleName}' created.")

    except Exception as e:
        print(f"An error occurred while creating the model: {e} Trace: {traceback.format_exc()}")
