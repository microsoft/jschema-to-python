from jschema_to_python import class_generator as cg


def test_make_type_annotation_for_nested_list():
    _verify(
        class_schema={
            "properties": {
                "nestedList": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "integer",
                        },
                    },
                    "default": [[]],
                },
            },
        },
        expected_imports="""import dataclasses
from __future__ import annotations
from typing import List""",
    )


def test_make_type_annotation_for_optional_reference_object():
    _verify(
        class_schema={
            "properties": {
                "referenceObject": {
                    "$ref": "#/definitions/ReferenceObject",
                },
            },
        },
        expected_imports="""import dataclasses
from __future__ import annotations
from typing import Optional
from module_name import _reference_object""",
    )


def test_make_type_annotation_for_fallback_any():
    _verify(
        class_schema={
            "properties": {
                "unrecognizableTypeObject": {
                    "type": "object",
                },
            },
        },
        expected_imports="""import dataclasses
from __future__ import annotations
from typing import Any""",
    )


def _verify(class_schema, expected_imports):
    class_generator = cg.DataclassesClassGenerator(
        class_schema=class_schema,
        class_name="ClassName",
        code_gen_hints=None,
        output_directory="UnusedDir",
        module_name="module_name",
    )

    schema_property_name = list(class_schema["properties"].keys())[0]
    is_required = (
        "required" in class_schema and schema_property_name in class_schema["required"]
    )
    actual_property = class_generator._generate_property(
        schema_property_name, not is_required
    )

    assert actual_property.required_imports.imports == expected_imports
