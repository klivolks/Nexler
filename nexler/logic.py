import traceback
from app.utils import dir_util, file_util, response_util
import os
import re


def create_logic(args):
    try:
        # Construct the directory path
        directory_path = f"app/logic/{args.component}"

        # Check if directory exists
        if not os.path.exists(directory_path):
            # Create the directory
            dir_util.create_directory(directory_path)

            # Create __init__.py in the directory
            init_file_path = os.path.join(directory_path, '__init__.py')
            file_util.write_file(init_file_path, '')

        # Construct the file path for module
        module_file_path = os.path.join(directory_path, f"{args.moduleName}.py")

        # Construct the class definition
        class_definition = f"""
class {args.moduleName}:
    def __init__(self):
        pass
"""
        # Create the module file and write the class definition to it
        file_util.write_file(module_file_path, class_definition)

        # Update the __init__.py to include the new module
        init_file_content = file_util.read_file(os.path.join(directory_path, '__init__.py'))
        import_line = f"from .{args.moduleName} import {args.moduleName}"
        if import_line not in init_file_content:
            init_file_content = import_line + '\n' + init_file_content
            file_util.write_file(os.path.join(directory_path, '__init__.py'), init_file_content)

        # Update the component __init__.py file to import the new logic module
        component_init_path = f'app/components/{args.component}/__init__.py'
        component_init_content = file_util.read_file(component_init_path)
        component_import_line = f"from app.logic.{args.component} import {args.moduleName}"
        if component_import_line not in component_init_content:
            # Check if there is already an import from the same logic directory
            existing_import = re.search(rf"from app\.logic\.{args.component} import (.+)", component_init_content)
            if existing_import:
                # Append the new module to the existing import
                new_import = existing_import.group(1) + ', ' + args.moduleName
                component_init_content = component_init_content.replace(existing_import.group(0),
                                                                        f"from app.logic.{args.component} import {new_import}")
            else:
                # Add a new import line
                component_init_content = component_import_line + '\n' + component_init_content

            file_util.write_file(component_init_path, component_init_content)

        print(f"Logic '{args.moduleName}' created for component: {args.component}")

    except Exception as e:
        print(f"An error occurred while creating the logic: {e} Trace: {traceback.format_exc()}")
