import logging
import os
import sys
import time
import argparse
from infrastructure.langtools import _


def setup_logging(args):
    peachy_logger = logging.getLogger('peachy')
    if args.devmode:
        timestr = time.strftime("%Y-%m-%d-%H%M%S")
        logfile = os.path.join(config.PEACHY_PATH, 'peachyprinter-%s.log' % timestr)
    else:
        logfile = os.path.join(config.PEACHY_PATH, 'peachyprinter.log')
    if os.path.isfile(logfile):
        os.remove(logfile)
    logging_format = '%(levelname)s: %(asctime)s %(module)s - %(message)s'
    logging_level = getattr(logging, args.loglevel.upper(), "INFO")
    if not isinstance(logging_level, int):
        raise ValueError('Invalid log level: %s' % args.loglevel)
    if True:
        peachy_logger = logging.getLogger('peachy')
        peachy_logger.propagate = False
        logFormatter = logging.Formatter(logging_format)

        fileHandler = logging.FileHandler(logfile)
        consoleHandler = logging.StreamHandler()

        fileHandler.setFormatter(logFormatter)
        consoleHandler.setFormatter(logFormatter)

        peachy_logger.addHandler(fileHandler)
        peachy_logger.addHandler(consoleHandler)

        peachy_logger.setLevel(logging_level)
    else:
        logging.basicConfig(filename=logfile, format=logging_format, level=logging_level)

def setup_env(path):
    python_64 = sys.maxsize > 2**32
    if os.name == 'nt':
        dll_base = os.path.join(path, 'win')
        if python_64:
            os.environ['PEACHY_API_DLL_PATH'] = os.path.join(dll_base, "AMD64")
        else:
            os.environ['PEACHY_API_DLL_PATH'] = os.path.join(dll_base, "x86")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Configure and print with Peachy Printer")
    parser.add_argument('-l', '--log',     dest='loglevel', action='store',      required=False, default="WARNING", help="Enter the loglevel [DEBUG|INFO|WARNING|ERROR] default: WARNING")
    parser.add_argument('-t', '--console', dest='console',  action='store_true', required=False, help="Logs to console not file")
    parser.add_argument('-d', '--development', dest='devmode',  action='store_true', required=False, help="Enable Developer Testing Mode")
    parser.add_argument('-m', '--module', dest='mod',  action='store', required=False, help='Activate a module (use "list" to get a list of available modules).')
    parser.add_argument('-y', '--language', dest='lang', action='store', required=False, default=None, help='override locale code')
    args, unknown = parser.parse_known_args()

    path = os.path.dirname(os.path.realpath(__file__))
    setup_env(path) 

    from peachyprinter import config, PrinterAPI

    if not os.path.exists(config.PEACHY_PATH):
        os.makedirs(config.PEACHY_PATH)
    if args.devmode:
        config.devmode = True
    setup_logging(args)

    api = PrinterAPI()
    sys.argv = [sys.argv[0]]
    if args.mod:
        sys.argv.append("-m")
        sys.argv.append(args.mod)

    from gui import PeachyPrinter
    PeachyPrinter(api, language=args.lang).run()
