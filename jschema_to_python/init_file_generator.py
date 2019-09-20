from jschema_to_python.python_file_generator import PythonFileGenerator
from jschema_to_python.utilities import capitalize_first_letter

class InitFileGenerator(PythonFileGenerator):
    def __init__(self, module_name, root_schema, root_class_name, output_directory):
        super(InitFileGenerator, self).__init__(output_directory)
        self.module_name = module_name
        self.root_schema = root_schema
        self.root_class_name = root_class_name

    def generate(self):
        file_path = self.make_output_file_path('__init__.py')
        with open(file_path, 'w') as self.file_obj:
            self.write_generation_comment()
            self.write_import_statements()

    def write_import_statements(self):
        self.write_import_statement(self.root_class_name)

        if 'definitions' in self.root_schema.keys():
            definition_schemas = self.root_schema['definitions']
            for definition_key in definition_schemas.keys():
                class_name = capitalize_first_letter(definition_key)
                self.write_import_statement(class_name)

    def write_import_statement(self, class_name):
        self.write_formatted_line('from {}.{} import {}', self.module_name, class_name, class_name)