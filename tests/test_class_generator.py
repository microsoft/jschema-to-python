import pytest
import jschema_to_python as js2p
import jschema_to_python.class_generator as cg


def test_required_property(tmp_path):
    class_generator = cg.ClassGenerator(
        class_schema={"properties": {"req": {"type": "int"}}, "required": ["req"]},
        class_name="RequiredProperty",
        code_gen_hints=None,
        output_directory=str(tmp_path),
    )
    class_generator.generate()

    with open(class_generator.file_path, "r") as fileObj:
        actual = fileObj.read()

    with open("tests/test_files/_required_property.py", "r") as fileObj:
        expected = fileObj.read()

    expected = expected.replace("$js2p_version$", js2p.__version__)

    assert actual == expected
