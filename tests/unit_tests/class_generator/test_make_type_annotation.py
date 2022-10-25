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
        expected_property='    nested_list: List[List[int]] = dataclasses.field(default_factory=lambda: [[]], metadata={"schema_property_name": "nestedList"})',
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
        expected_property='    reference_object: Optional[_reference_object.ReferenceObject] = dataclasses.field(default=None, metadata={"schema_property_name": "referenceObject"})',
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
        expected_property='    unrecognizable_type_object: Any = dataclasses.field(default=None, metadata={"schema_property_name": "unrecognizableTypeObject"})',
    )


def _verify(class_schema, expected_property):
    class_generator = cg.DataclassesClassGenerator(
        class_schema=class_schema,
        class_name="UnusedClassName",
        code_gen_hints=None,
        output_directory="UnusedDir",
        module_name="UnusedModuleName",
    )

    schema_property_name = list(class_schema["properties"].keys())[0]
    is_required = (
        "required" in class_schema and schema_property_name in class_schema["required"]
    )
    actual_property = class_generator._generate_property(
        schema_property_name, not is_required
    )

    assert str(actual_property) == expected_property
