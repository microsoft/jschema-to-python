from __future__ import absolute_import

import os
import sys

if not __package__:
    path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, path)

from jschema_to_python.driver import main as _main  # noqa

if __name__ == "__main__":
    sys.exit(_main())
