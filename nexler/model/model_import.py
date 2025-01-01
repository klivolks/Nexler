
def import_model(args):
    from nexler.utils import file_util, str_util
    moduleName = str_util.pascal_case(args.moduleName)
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
    print(f"Added to logic {args.logic}")
