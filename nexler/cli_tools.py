import argparse
from nexler import component, logic
from nexler import __version__ as nexler_version

def main():
    parser = argparse.ArgumentParser(prog='nexler', description='Nexler framework')
    parser.add_argument('--version', action='version', version=f'%(prog)s {nexler_version}')
    parser.add_argument('command', help='Command to run', choices=['create'])
    parser.add_argument('module', help='Name of the module (component/logic)', choices=['component', 'logic'])
    parser.add_argument('moduleName', help='Module Class Name or Component Class Name')
    parser.add_argument('--url', default=None, help='URL for the component')
    parser.add_argument('--variables', nargs='*', default=[], help='Variables for the module')
    parser.add_argument('--component', default=None, help='Component Class Name (for logic module only)')

    args = parser.parse_args()

    if args.command == 'create':
        if args.module == 'component':
            if not args.url:
                parser.error("The --url argument is required for creating a component.")
            component.create_component(args)
        elif args.module == 'logic':
            if not args.component:
                parser.error("The --component argument is required for creating logic.")
            logic.create_logic(args)
        else:
            parser.error(f"The module '{args.module}' is not recognized. Use 'component' or 'logic'.")

if __name__ == "__main__":
    main()
