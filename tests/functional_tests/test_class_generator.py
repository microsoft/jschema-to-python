import pytest
import jschema_to_python as js2p
import jschema_to_python.class_generator as cg


def test_class_generation(tmp_path):
    _verify(
        class_schema={
            "description": "This is a test class.",
            "properties": {
                "requiredProperty": {"type": "int"},
                "optionalProperty": {"type": "int", "default": 42},
            },
            "required": ["requiredProperty"],
        },
        class_name="TestClass",
        expected_file_name="_test_class.py",
        tmp_path=tmp_path,
    )


def _verify(class_schema, class_name, expected_file_name, tmp_path):
    class_generator = cg.ClassGenerator(
        class_schema=class_schema,
        class_name=class_name,
        code_gen_hints=None,
        output_directory=str(tmp_path),
    )

    class_generator.generate()

    with open(class_generator.file_path, "r") as fileObj:
        actual = fileObj.read()

    with open("tests/test_files/" + expected_file_name, "r") as fileObj:
        expected = fileObj.read()

    expected = expected.replace("$js2p_version$", js2p.__version__)

    assert actual == expected
