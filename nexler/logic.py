from app.utils import dir_util, file_util, response_util
import os
import re


def create_logic(args):
    try:
        # Construct the directory path
        directory_path = f"app/logic/{args.component}"

        # Create the directory
        dir_util.create_directory(directory_path)

        # Construct the file path
        file_path = os.path.join(directory_path, '__init__.py')

        # Construct the class definition
        class_definition = f"""
class {args.moduleName}:
    def __init__(self):
        pass
"""
        # Create the file and write the class definition to it
        file_util.write_file(file_path, class_definition)

        # Append the import line to the logic __init__.py
        logic_init_path = 'app/logic/__init__.py'
        import_line = f"from .{args.component} import {args.moduleName}\n"
        file_util.append_file(logic_init_path, import_line)

        # Update the component __init__.py file
        component_init_path = f'app/components/{args.component}/__init__.py'
        content = file_util.read_file(component_init_path)

        # Split the content by lines
        lines = content.split('\n')

        # Find the last import line
        last_import_index = -1
        for i, line in enumerate(lines):
            if re.match(r"from .+ import .+", line):
                last_import_index = i

        # Insert the new import line after the last import line
        if last_import_index != -1:
            lines.insert(last_import_index + 1, f"from app.logic import {args.moduleName}")
        else:
            lines.insert(0, f"from app.logic import {args.moduleName}")

        # Join the lines back together and write the updated content back to the file
        updated_content = '\n'.join(lines)
        file_util.write_file(component_init_path, updated_content)

        print(f"Logic '{args.moduleName}' created for component: {args.component}")

    except Exception as e:
        print(f"An error occurred while creating the logic: {e}")
