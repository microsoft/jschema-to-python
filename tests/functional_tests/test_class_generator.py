import jschema_to_python as js2p
import jschema_to_python.class_generator as cg

_TEST_CLASS_SCHEMA = {
    "description": "This is a test class.",
    "properties": {
        "requiredProperty": {"type": "integer"},
        "optionalProperty": {"type": "integer", "default": 42},
    },
    "required": ["requiredProperty"],
}


def test_class_generation(tmp_path):
    _verify(
        class_schema=_TEST_CLASS_SCHEMA,
        class_name="TestClass",
        expected_file_name="_test_class.py",
        tmp_path=tmp_path,
    )


def test_class_generation_using_dataclasses(tmp_path):
    _verify(
        class_schema=_TEST_CLASS_SCHEMA,
        class_name="TestClass",
        expected_file_name="_test_class_dataclasses.py",
        tmp_path=tmp_path,
        library="dataclasses",
    )


def _verify(class_schema, class_name, expected_file_name, tmp_path, library="attrs"):
    if library == "attrs":
        class_generator = cg.ClassGenerator(
            class_schema=class_schema,
            class_name=class_name,
            code_gen_hints=None,
            output_directory=str(tmp_path),
        )
    else:
        class_generator = cg.DataclassesClassGenerator(
            class_schema=class_schema,
            class_name=class_name,
            code_gen_hints=None,
            output_directory=str(tmp_path),
            module_name="",
        )

    class_generator.generate()

    with open(class_generator.file_path, "r") as fileObj:
        actual = fileObj.read()

    with open("tests/test_files/" + expected_file_name, "r") as fileObj:
        expected = fileObj.read()

    expected = expected.replace("$js2p_version$", js2p.__version__)

    assert actual == expected
