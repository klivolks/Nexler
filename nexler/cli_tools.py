import argparse
from nexler import component, logic, upgrade, migrate  # import the upgrade module
from nexler import __version__ as nexler_version


def main():
    parser = argparse.ArgumentParser(prog='nexler', description='Nexler framework')
    parser.add_argument('--version', action='version', version=f'%(prog)s {nexler_version}')
    subparsers = parser.add_subparsers(dest='command', help='Sub-commands')

    # create sub-command
    create_parser = subparsers.add_parser('create', help='Create a new component or logic module')
    create_parser.add_argument('module', help='Name of the module (component/logic)', choices=['component', 'logic'])
    create_parser.add_argument('moduleName', help='Module Class Name or Component Class Name')
    create_parser.add_argument('--url', default=None, help='URL for the component')
    create_parser.add_argument('--variables', default=None, help='Variables for the module')
    create_parser.add_argument('--component', default=None, help='Component Class Name (for logic module only)')
    create_parser.add_argument('--protected', action='store_true', help='Create a protected component')
    create_parser.add_argument('--methods', default=None, help='Methods for the module')
    create_parser.add_argument('--main', default=None, help='Name of the main logic directory.')
    create_parser.add_argument('--independent', action='store_true', help='generate independent logic that can be imported to any component')

    # upgrade sub-command
    upgrade_parser = subparsers.add_parser('upgrade', help='Upgrade Nexler to the latest version')

    # migrate sub-command
    migrate_parser = subparsers.add_parser('migrate', help='Run migration for the Nexler framework')

    args = parser.parse_args()

    if args.command == 'create':
        if args.module == 'component':
            if not args.url:
                create_parser.error("The --url argument is required for creating a component.")
            component.create_component(args)
        elif args.module == 'logic':
            if not args.component:
                create_parser.error("The --component argument is required for creating logic.")
            logic.create_logic(args)
        else:
            create_parser.error(f"The module '{args.module}' is not recognized. Use 'component' or 'logic'.")
    elif args.command == 'upgrade':
        upgrade.upgrade()  # call the upgrade function from the upgrade module
    elif args.command == 'migrate':
        migrate.migrate()  # call the migrate function from the migrate module


if __name__ == "__main__":
    main()
