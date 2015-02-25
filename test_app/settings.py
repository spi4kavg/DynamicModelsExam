import os, sys

APP_PATH = os.path.abspath(os.path.dirname(__file__))

if sys.argv[1:2] == ['test']:
    CONFIG_FILE = os.path.join(APP_PATH, 'test_models.yaml')
else:
    CONFIG_FILE = os.path.join(APP_PATH, 'models.yaml')
DEFAULT_CHAR_LEN = 50
DEFAULT_INT_VAL = 0