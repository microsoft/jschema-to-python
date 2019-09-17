import argparse

from jschema_to_python.object_model_module_generator import ObjectModelModuleGenerator

def main():
    parser = init_parser()
    args = parser.parse_args()

    display_args(args)

    generator = ObjectModelModuleGenerator(args)
    generator.generate()

def init_parser():
    parser = argparse.ArgumentParser(description='Generate source code for a set of Python classes from a JSON schema.')
    parser.add_argument('-s', '--schema-path',
                        help='path to the JSON schema file',
                        required=True)
    parser.add_argument('-o', '--output-directory',
                        help='directory in which the generated classes will be created',
                        required=True)
    parser.add_argument('-r', '--root-class-name',
                        help='the name of the class at the root of the object model represented by the schema',
                        required=True)
    parser.add_argument('-g', '--hints-file-path',
                        help='path to a file containing hints that control code generation')
    parser.add_argument('-f', '--force', action="store_true",
                        help="overwrite the output directory if it exists")
    parser.add_argument('-v', '--verbose', action="count", default=0,
                        help='increase output verbosity (may be specified up to two times)')
    return parser

def display_args(args):
    if (args.verbose > 0):
        print('Generating Python classes...')
    if (args.verbose > 1):
        print('    from JSON schema {}'.format(args.schema_path))
        print('    to root class {}'.format(args.root_class_name))
        print('    in directory {}'.format(args.output_directory))
        if not (args.hints_file_path is None):
            print('    with code generation hints from {}'.format(args.hints_file_path))

if __name__ == '__main__':
    main()