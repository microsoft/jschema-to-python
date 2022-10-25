import argparse

from jschema_to_python import __version__
from jschema_to_python.object_model_module_generator import \
    ObjectModelModuleGenerator


def main():
    parser = _init_parser()
    args = parser.parse_args()

    _display_args(args)

    generator = ObjectModelModuleGenerator(args)
    generator.generate()

    if args.verbose:
        print("Done.")


def _init_parser():
    parser = argparse.ArgumentParser(
        description="Generate source code for a set of Python classes from a JSON schema."
    )
    parser.add_argument(
        "-s", "--schema-path", help="path to the JSON schema file", required=True
    )
    parser.add_argument(
        "-o",
        "--output-directory",
        help="directory in which the generated classes will be created",
        required=True,
    )
    parser.add_argument(
        "-m",
        "--module-name",
        help="name of the module containing the object model classes",
    )
    parser.add_argument(
        "-r",
        "--root-class-name",
        help="the name of the class at the root of the object model represented by the schema",
        required=True,
    )
    parser.add_argument(
        "-g",
        "--hints-file-path",
        help="path to a file containing hints that control code generation",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="overwrite the output directory if it exists",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="increase output verbosity (may be specified up to two times)",
    )
    parser.add_argument(
        "-l",
        "--library",
        help="the library to use for code generation (default: attr)",
        default="attr",
        choices=["attr", "dataclasses"],
    )
    return parser


def _display_args(args):
    if args.verbose:
        print(
            __package__
            + ": JSON schema to Python object model generator, version "
            + __version__
        )
        print("Generating Python classes...")
    if args.verbose > 1:
        print("    from JSON schema " + args.schema_path)
        print("    to module " + args.module_name)
        print("    in directory " + args.output_directory)
        print("    with root class " + args.root_class_name)
        print("    using " + args.library)
        if args.hints_file_path:
            print("    with code generation hints from " + args.hints_file_path)


if __name__ == "__main__":
    main()
