jschema-to-python
=================

Generate Python classes from a JSON schema.

Usage
=====
::

    python -m jschema_to_python [-h] -s SCHEMA_PATH -o OUTPUT_DIRECTORY [-m MODULE_NAME] -r ROOT_CLASS_NAME [-g HINTS_FILE_PATH] [-f] [-v]

    Generate source code for a set of Python classes from a JSON schema.

    optional arguments:
      -h, --help            show this help message and exit
      -s SCHEMA_PATH, --schema-path SCHEMA_PATH
                            path to the JSON schema file
      -o OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
                            directory in which the generated classes will be
                            created
      -m MODULE_NAME, --module-name MODULE_NAME
                            name of the module containing the object model classes
      -r ROOT_CLASS_NAME, --root-class-name ROOT_CLASS_NAME
                            the name of the class at the root of the object model
                            represented by the schema
      -g HINTS_FILE_PATH, --hints-file-path HINTS_FILE_PATH
                            path to a file containing hints that control code
                            generation
      -f, --force           overwrite the output directory if it exists
      -v, --verbose         increase output verbosity (may be specified up to two
                            times)

Contributing
============

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the `Microsoft Open Source Code of Conduct <https://opensource.microsoft.com/codeofconduct/>`_.
For more information see the `Code of Conduct FAQ <https://opensource.microsoft.com/codeofconduct/faq/>`_ or
contact `opencode@microsoft.com <mailto:opencode@microsoft.com>`_ with any additional questions or comments.
