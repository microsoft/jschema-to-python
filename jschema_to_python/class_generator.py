import sys
from typing import Any, Dict, Optional, Sequence, Set, Tuple

import jschema_to_python.utilities as util
from jschema_to_python.python_file_generator import PythonFileGenerator


class ClassGenerator(PythonFileGenerator):
    def __init__(self, class_schema, class_name, code_gen_hints, output_directory):
        super(ClassGenerator, self).__init__(output_directory)
        self.class_schema = class_schema
        self.required_property_names = class_schema.get("required")
        if self.required_property_names:
            self.required_property_names.sort()
        self.class_name = class_name
        self.code_gen_hints = code_gen_hints
        self.file_path = self._make_class_file_path()

    def __del__(self):
        sys.stdout = sys.__stdout__

    def generate(self):
        with open(self.file_path, "w") as sys.stdout:
            self.write_generation_comment()
            self._write_class_declaration()
            self._write_class_description()
            self._write_class_body()

    def _make_class_file_path(self):
        class_module_name = util.class_name_to_private_module_name(self.class_name)
        return self.make_output_file_path(class_module_name + ".py")

    def _write_class_declaration(self):
        print("import attr")
        print("")
        print("")  # The black formatter wants two blank lines here.
        print("@attr.s")
        print("class " + self.class_name + "(object):")

    def _write_class_description(self):
        description = self.class_schema.get("description")
        if description:
            print('    """' + description + '"""')
            print("")  # The black formatter wants a blank line here.

    def _write_class_body(self):
        property_schemas = self.class_schema["properties"]
        if not property_schemas:
            print("    pass")
            return

        schema_property_names = sorted(property_schemas.keys())

        # attrs requires that mandatory attributes be declared before optional
        # attributes.
        if self.required_property_names:
            for schema_property_name in self.required_property_names:
                attrib = self._make_attrib(schema_property_name)
                print(attrib)

        for schema_property_name in schema_property_names:
            if self._is_optional(schema_property_name):
                attrib = self._make_attrib(schema_property_name)
                print(attrib)

    def _make_attrib(self, schema_property_name):
        python_property_name = (
            self._make_python_property_name_from_schema_property_name(
                schema_property_name
            )
        )
        attrib = "".join(["    ", python_property_name, " = attr.ib("])
        if self._is_optional(schema_property_name):
            property_schema = self.class_schema["properties"][schema_property_name]
            default_setter = self._make_default_setter(property_schema)
            attrib = "".join([attrib, default_setter, ", "])
        attrib = "".join(
            [attrib, 'metadata={"schema_property_name": "', schema_property_name, '"})']
        )
        return attrib

    def _is_optional(self, schema_property_name):
        return (
            not self.required_property_names
            or schema_property_name not in self.required_property_names
        )

    def _make_default_setter(self, property_schema):
        initializer = self._make_initializer(property_schema)
        return "default=" + str(initializer)

    def _make_initializer(self, property_schema):
        default = property_schema.get("default")
        if default:
            type = property_schema.get("type")
            if type:
                if type == "string":
                    default = (
                        '"' + default + '"'
                    )  # The black formatter wants double-quotes.
                elif type == "array":
                    # It isn't safe to specify a mutable object as a default value,
                    # because all new instances share the same mutable object, and
                    # one of them might mutate it, affecting all future instances!
                    # attr.Factory creates a new value for each instance.
                    default = "attr.Factory(lambda: " + str(default) + ")"
            elif property_schema.get("enum"):
                default = '"' + default + '"'
            return default

        return "None"

    def _make_python_property_name_from_schema_property_name(
        self, schema_property_name
    ):
        hint_key = self.class_name + "." + schema_property_name
        property_name_hint = self._get_hint(hint_key, "PropertyNameHint")
        if not property_name_hint:
            property_name = schema_property_name
        else:
            property_name = property_name_hint["arguments"]["pythonPropertyName"]
        return util.to_underscore_separated_name(property_name)

    def _get_hint(self, hint_key, hint_kind):
        if not self.code_gen_hints or hint_key not in self.code_gen_hints:
            return None

        hint_array = self.code_gen_hints[hint_key]
        for hint in hint_array:
            if hint["kind"] == hint_kind:
                return hint

        return None


_JSCHEMA_TO_PYTHON_TYPE_MAPPING = {
    "string": "str",
    "integer": "int",
    "number": "float",
    "boolean": "bool",
}


class DataclassesImportGenerator:
    def __init__(self, module_name: Optional[str] = None):
        self._typings: Set[str] = set()
        self._dependent_modules: Set[str] = set()
        self._typing_extensions: Set[str] = set()
        self._module_name: Optional[str] = module_name

    @property
    def _base_import(self):
        return "import dataclasses\nfrom __future__ import annotations"

    @property
    def _typing_import(self):
        if self._typings:
            return f"from typing import {', '.join(self._typings)}"
        return ""

    def add_typing(self, typing: str):
        self._typings.add(typing)

    @property
    def _typing_extension_import(self):
        if self._typing_extensions:
            return f"from typing_extensions import {', '.join(self._typing_extensions)}"
        return ""

    def add_typing_extension(self, typing: str):
        self._typing_extensions.add(typing)

    @property
    def _dependent_modules_import(self) -> Sequence[str]:
        if self._dependent_modules:
            return (
                f"from {self._module_name} import {', '.join(self._dependent_modules)}"
            )
        return ""

    def add_dependent_module(self, module_name: str):
        self._dependent_modules.add(module_name)

    def merge(self, other: "DataclassesImportGenerator"):
        self._typings.update(other._typings)
        self._typing_extensions.update(other._typing_extensions)
        self._dependent_modules.update(other._dependent_modules)

    @property
    def imports(self):
        import_lines = [
            self._base_import,
            self._typing_import,
            self._typing_extension_import,
            self._dependent_modules_import,
        ]
        return "\n".join([line for line in import_lines if line])


def make_type_annotation(
    property_schema, is_optional, module_name: Optional[str] = None
) -> Tuple[str, DataclassesImportGenerator]:
    imports = DataclassesImportGenerator(module_name)
    type_annotation = "Any"

    property_type = property_schema.get("type")
    ref_type = property_schema.get("$ref")
    enums = property_schema.get("enum")

    if property_type:
        if property_type in _JSCHEMA_TO_PYTHON_TYPE_MAPPING:
            type_annotation = _JSCHEMA_TO_PYTHON_TYPE_MAPPING[property_type]
        elif property_type == "array":
            sub_type_annotation, sub_imports = make_type_annotation(
                property_schema.get("items", {}), False, module_name
            )
            type_annotation = f"List[{sub_type_annotation}]"
            imports.merge(sub_imports)
            imports.add_typing("List")
    elif ref_type:
        ref_class_name = util.capitalize_first_letter(ref_type.split("/")[-1])
        ref_class_module_name = util.class_name_to_private_module_name(ref_class_name)
        imports.add_dependent_module(ref_class_module_name)
        type_annotation = f"{ref_class_module_name}.{ref_class_name}"
    elif enums:
        type_annotation = f"Literal[{', '.join([repr(enum) for enum in enums])}]"
        imports.add_typing_extension("Literal")

    if type_annotation == "Any":
        imports.add_typing("Any")

    if type_annotation != "Any" and is_optional:
        type_annotation = f"Optional[{type_annotation}]"
        imports.add_typing("Optional")

    return type_annotation, imports


def make_default_setter(property_schema) -> str:
    _key = "default"
    _value = property_schema.get("default")
    if _value:
        type = property_schema.get("type")
        if type:
            if type == "string":
                _value = f'"{_value}"'
            elif type == "array":
                _key = "default_factory"
                _value = f"lambda: {_value}"
        elif property_schema.get("enum"):
            _value = f'"{_value}"'
    else:
        _value = "None"
    return f"{_key}={_value}"


class DataclassesPropertyGenerator:
    def __init__(
        self,
        schema_property_name: str,
        python_property_name: str,
        is_optional: bool,
        property_schema: Dict[str, Any],
        module_name: Optional[str] = None,
    ):
        self._python_property_name = python_property_name
        self._is_optional = is_optional
        self._default_setter = (
            make_default_setter(property_schema) if is_optional else ""
        )
        self._type_annotation, self._imports = make_type_annotation(
            property_schema,
            self._default_setter.find("None") != -1,
            module_name,
        )
        self._metadata_setter = (
            f'metadata={{"schema_property_name": "{schema_property_name}"}}'
        )

    @property
    def required_imports(self) -> DataclassesImportGenerator:
        return self._imports

    def __repr__(self) -> str:
        field_kwargs = []
        if self._is_optional:
            field_kwargs.append(self._default_setter)
        field_kwargs.append(self._metadata_setter)
        return (
            f"    {self._python_property_name}: {self._type_annotation} = "
            f"dataclasses.field({', '.join(field_kwargs)})"
        )

    def __str__(self) -> str:
        return repr(self)


class DataclassesClassGenerator(ClassGenerator):
    def __init__(
        self, class_schema, class_name, code_gen_hints, output_directory, module_name
    ):
        super().__init__(class_schema, class_name, code_gen_hints, output_directory)
        self._import_generator = DataclassesImportGenerator(module_name)
        self._property_generators = []
        self._property_schemas = class_schema.get("properties", {})
        self._module_name = module_name

    def _generate_property(self, schema_property_name: str, is_optional: bool):
        python_property_name = (
            self._make_python_property_name_from_schema_property_name(
                schema_property_name
            )
        )
        property_generator = DataclassesPropertyGenerator(
            schema_property_name,
            python_property_name,
            is_optional,
            self._property_schemas.get(schema_property_name, {}),
            self._module_name,
        )
        required_imports = property_generator.required_imports
        self._import_generator.merge(required_imports)
        self._property_generators.append(property_generator)
        return property_generator

    def _generate_properties(self):
        if not self._property_schemas:
            return

        schema_property_names = sorted(self._property_schemas.keys())

        if self.required_property_names:
            for schema_property_name in self.required_property_names:
                self._generate_property(schema_property_name, False)

        for schema_property_name in schema_property_names:
            if self._is_optional(schema_property_name):
                self._generate_property(schema_property_name, True)

    def generate(self):
        self._generate_properties()
        super().generate()

    def _write_class_declaration(self):
        print(self._import_generator.imports)
        print("")
        print("")
        print("@dataclasses.dataclass")
        print(f"class {self.class_name}(object):")

    def _write_class_body(self):
        if not self._property_generators:
            print("    pass")
            return

        for property_generator in self._property_generators:
            print(str(property_generator))
