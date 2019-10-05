import pytest
import jschema_to_python as js2p
import jschema_to_python.class_generator as cg


def test_required_property(tmp_path):
    verify(
        class_schema={"properties": {"requiredProperty": {"type": "int"}}, "required": ["requiredProperty"]},
        class_name="RequiredProperty",
        expected_file_name="_required_property.py",
        tmp_path=tmp_path,
    )


def test_optional_property(tmp_path):
    verify(
        class_schema={"properties": {"optionalProperty": {"type": "int", "default": 42}}},
        class_name="OptionalProperty",
        expected_file_name="_optional_property.py",
        tmp_path=tmp_path,
    )


def verify(class_schema, class_name, expected_file_name, tmp_path):
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
