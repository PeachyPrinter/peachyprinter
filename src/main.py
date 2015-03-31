import logging
import os
import sys
import time
from peachyprinter import config, PrinterAPI
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


if __name__ == "__main__":
    if not os.path.exists(config.PEACHY_PATH):
        os.makedirs(config.PEACHY_PATH)

    parser = argparse.ArgumentParser("Configure and print with Peachy Printer")
    parser.add_argument('-l', '--log',     dest='loglevel', action='store',      required=False, default="WARNING", help="Enter the loglevel [DEBUG|INFO|WARNING|ERROR] default: WARNING")
    parser.add_argument('-t', '--console', dest='console',  action='store_true', required=False, help="Logs to console not file")
    parser.add_argument('-d', '--development', dest='devmode',  action='store_true', required=False, help="Enable Developer Testing Mode")
    args, unknown = parser.parse_known_args()

    setup_logging(args)
    if args.devmode:
        config.devmode = True

    if getattr(sys, 'frozen', False):
        path = os.path.dirname(sys.executable)
    else:
        path = os.path.dirname(os.path.realpath(__file__))

    api = PrinterAPI()
    sys.argv = [sys.argv[0]]
    from gui import PeachyPrinter
    PeachyPrinter(api).run()
