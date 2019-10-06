import pytest
import jschema_to_python.class_generator as cg


def test_make_attrib_for_required_property():
    _verify(
        class_schema={
            "properties": {
                "requiredProperty": {"type": "int"},
            },
            "required": ["requiredProperty"],
        },
        expected_attrib="    required_property = attr.ib(metadata={\"schema_property_name\": \"requiredProperty\"})"
    )


def test_make_attrib_for_optional_property():
    _verify(
        class_schema={
            "properties": {
                "optionalProperty": {"type": "int", "default": 42},
            }
        },
        expected_attrib="    optional_property = attr.ib(default=42, metadata={\"schema_property_name\": \"optionalProperty\"})"
    )


def _verify(class_schema, expected_attrib):
    class_generator = cg.ClassGenerator(
        class_schema=class_schema,
        class_name="Unused",
        code_gen_hints=None,
        output_directory="Unused",
    )

    schema_property_name = list(class_schema["properties"].keys())[0]
    actual_attrib = class_generator._make_attrib(schema_property_name)

    assert actual_attrib == expected_attrib