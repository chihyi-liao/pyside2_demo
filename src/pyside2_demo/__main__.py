import os
import sys


if __package__ == "":
    path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, path)


if __name__ == "__main__":
    import pyside2_demo
    sys.exit(pyside2_demo.main())

