import argparse
from blaze_cicd.commands import init_command, build_command

def main():
    parser = argparse.ArgumentParser(description="Blaze CI/CD CLI Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize a new configuration file")
    init_parser.add_argument("--file", default="config.yaml", help="Path to the configuration file")

    # Build command
    build_parser = subparsers.add_parser("build", help="Build the project using the configuration file")
    build_parser.add_argument("--file", default="config.yaml", help="Path to the configuration file")

    args = parser.parse_args()

    if args.command == "init":
        init_command(args.file)
    elif args.command == "build":
        build_command(args.file)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()