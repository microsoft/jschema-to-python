from jschema_to_python.python_file_generator import PythonFileGenerator

class ClassGenerator(PythonFileGenerator):
    def __init__(self, class_schema, class_name, code_gen_hints, output_directory):
        super(ClassGenerator, self).__init__(output_directory)
        self.class_schema = class_schema
        self.class_name = class_name
        self.code_gen_hints = code_gen_hints

    def generate(self):
        file_path = self.make_class_file_path()
        with open(file_path, 'w') as self.file_obj:
            self.write_generation_comment()
            self.write_class_declaration()
            self.write_class_description()
            self.write_constructor()

    def make_class_file_path(self):
        return self.make_output_file_path(self.class_name + '.py')

    def write_class_declaration(self):
        self.write_formatted_line('class {}(object):', self.class_name)

    def write_class_description(self):
        if 'description' in self.class_schema.keys():
            self.write_formatted_line('    """{}"""', self.class_schema['description'])

    def write_constructor(self):
        self.write_constructor_parameters()
        self.write_required_property_checks()
        self.write_attribute_assignments()

    def write_constructor_parameters(self):
        self.file_obj.write('    def __init__(self')

        for schema_property_name in self.class_schema['properties'].keys():
            self.file_obj.write(',\n')
            python_property_name = self.make_python_property_name_from_schema_property_name(schema_property_name)
            property_schema = self.class_schema['properties'][schema_property_name]
            initializer = self.make_initializer(property_schema)
            self.file_obj.write('        {}={}'.format(python_property_name, initializer))

        self.file_obj.write('):\n')

    def write_required_property_checks(self):
        if 'required' in self.class_schema.keys():
            self.file_obj.write('\n')
            self.write_formatted_line('        missing_properties = []')
            for schema_property_name in self.class_schema['required']:
                python_property_name = self.make_python_property_name_from_schema_property_name(schema_property_name)
                self.write_formatted_line('        if {} is None:', python_property_name)
                self.write_formatted_line('            missing_properties.append(\'{}\')', python_property_name)

            self.write_formatted_line('        if len(missing_properties) > 0:')
            self.write_formatted_line('            raise Exception(\'required properties of class {} were not provided: {{}}\'.format(\', \'.join(missing_properties)))', self.class_name)

    def write_attribute_assignments(self):
        self.file_obj.write('\n')
        for schema_property_name in self.class_schema['properties'].keys():
            python_property_name = self.make_python_property_name_from_schema_property_name(schema_property_name)
            self.write_formatted_line('        self.{}={}', python_property_name, python_property_name)

    def make_initializer(self, property_schema):
        if 'default' in property_schema.keys():
            default = property_schema['default']
            keys = property_schema.keys()
            if 'type' in keys:
                type = property_schema['type']
                if type == 'string':
                    default = '\'{}\''.format(default)
            elif 'enum' in keys:
                default = '\'{}\''.format(default)
            return default

        return 'None'

    def make_python_property_name_from_schema_property_name(self, schema_property_name):
        hint_key = '{}.{}'.format(self.class_name, schema_property_name)
        property_name_hint = self.get_hint(hint_key, 'PropertyNameHint')
        if property_name_hint is None:
            return schema_property_name
        else:
            return property_name_hint['arguments']['pythonPropertyName']

    def get_hint(self, hint_key, hint_kind):
        if self.code_gen_hints is None or hint_key not in self.code_gen_hints.keys():
            return None

        hint_array = self.code_gen_hints[hint_key]
        for hint in hint_array:
            if hint['kind'] == hint_kind:
                return hint

        return None