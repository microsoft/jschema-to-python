import sys
from jschema_to_python.python_file_generator import PythonFileGenerator
import jschema_to_python.utilities as util

class ClassGenerator(PythonFileGenerator):
    def __init__(self, class_schema, class_name, code_gen_hints, output_directory):
        super(ClassGenerator, self).__init__(output_directory)
        self.class_schema = class_schema
        self.required_property_names = class_schema.get('required')
        self.class_name = class_name
        self.code_gen_hints = code_gen_hints

    def __del__(self):
        sys.stdout = sys.__stdout__

    def generate(self):
        file_path = self.make_class_file_path()
        with open(file_path, 'w', encoding='utf-8') as sys.stdout:
            self.write_generation_comment()
            self.write_class_declaration()
            self.write_class_description()
            self.write_class_body()

    def make_class_file_path(self):
        class_module_name = util.class_name_to_private_module_name(self.class_name)
        return self.make_output_file_path(class_module_name + '.py')

    def write_class_declaration(self):
        print('import attr')
        print()
        print('@attr.s')
        print('class ' + self.class_name + '(object):')

    def write_class_description(self):
        description = self.class_schema.get('description')
        if description:
            print('    """' + description + '"""')

    def write_class_body(self):
        property_schemas = self.class_schema['properties']

        # attrs requires that mandatory attributes be declared before optional
        # attributes.
        if self.required_property_names:
            for schema_property_name in self.required_property_names:
                python_property_name = self.make_python_property_name_from_schema_property_name(schema_property_name)
                print('    ' + python_property_name + ' = attr.ib()')

        for schema_property_name in property_schemas:
            if self.is_optional(schema_property_name):
                python_property_name = self.make_python_property_name_from_schema_property_name(schema_property_name)
                property_schema = property_schemas[schema_property_name]
                default_setter = self.make_default_setter(property_schema)
                print('    ' + python_property_name + ' = attr.ib(' + default_setter + ')')

    def is_optional(self, schema_property_name):
        return not self.required_property_names or schema_property_name not in self.required_property_names

    def make_default_setter(self, property_schema):
        initializer = self.make_initializer(property_schema)
        return 'default=' + str(initializer)

    def make_initializer(self, property_schema):
        default = property_schema.get('default')
        if default:
            type = property_schema.get('type')
            if type:
                if type == 'string':
                    default = repr(default)
            elif property_schema.get('enum'):
                default = repr(default)
            return default

        return 'None'

    def make_python_property_name_from_schema_property_name(self, schema_property_name):
        hint_key = self.class_name + '.' + schema_property_name
        property_name_hint = self.get_hint(hint_key, 'PropertyNameHint')
        if not property_name_hint:
            return schema_property_name
        else:
            return property_name_hint['arguments']['pythonPropertyName']

    def get_hint(self, hint_key, hint_kind):
        if not self.code_gen_hints or hint_key not in self.code_gen_hints:
            return None

        hint_array = self.code_gen_hints[hint_key]
        for hint in hint_array:
            if hint['kind'] == hint_kind:
                return hint

        return None