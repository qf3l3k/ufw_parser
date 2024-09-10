import logging

from ufw_parser.cli import command_line_parser
from ufw_parser.config import load_config
from ufw_parser.exporter import export_rules
from ufw_parser.logger import initialize_loggers
from ufw_parser.parser import process_data


logger = logging.getLogger("ufw_parser_log")


def main():
    cmdargs = command_line_parser()
    print(cmdargs.output)
    initialize_loggers(cmdargs.log)
    logger.info("Command line arguments: %s", cmdargs)
    config = load_config(cmdargs.config)
    data_processor = process_data(config)
    export_rules(data_processor, cmdargs.output)


if __name__ == '__main__':
    main()