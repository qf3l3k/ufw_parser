import logging

from ufw_parser.cli import command_line_parser
from ufw_parser.config import load_config
from ufw_parser.exporter import RuleExporter
from ufw_parser.logger import initialize_loggers
from ufw_parser.parser import ServerRuleFetcher


def main():
    cmdargs = command_line_parser()
    log_level = logging.DEBUG if cmdargs.debug else logging.INFO
    initialize_loggers(cmdargs.log, log_level=log_level)
    logger = logging.getLogger("ufw_parser_log")
    logger.info("Command line arguments: %s", cmdargs)

    config = load_config(cmdargs.config)
    fetcher = ServerRuleFetcher(config)
    rules = fetcher.fetch_all_rules()
    exporter = RuleExporter(cmdargs.output_folder)
    exporter.export(rules, cmdargs.output)


if __name__ == '__main__':
    main()