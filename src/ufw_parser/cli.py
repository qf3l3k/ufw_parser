import argparse


def command_line_parser():
    parser = argparse.ArgumentParser(prog='ufw_parser',
                                     prefix_chars='-',
                                     description='UFW Rule Parser Tool consolidates and presents firewall rules in tabular format.',
                                     epilog='...and SysAdmin is happy!')
    parser.add_argument('-c', '--config',
                        type=str,
                        required=True,
                        action='store',
                        dest='config',
                        default='~/.ufw_parser/hosts.yml',
                        help='Path to the configuration file.')
    parser.add_argument('-l', '--log',
                        action='store',
                        dest='logs',
                        default='~/.ufw_parser/logs/',
                        help='Directory to store log files. Default: ~/.ufw_parser/logs/')
    parser.add_argument('-o', '--output',
                        choices=['screen', 'csv', 'excel'],
                        action='store',
                        dest='output',
                        default='screen',
                        help='Output format')
    parser.add_argument('-of', '--output_folder',
                        choices=['screen', 'csv', 'excel'],
                        action='store',
                        dest='output_folder',
                        default='~/.ufw_parser/logs/',
                        help='Output file destination.')
    parser.add_argument('-v', '--version',
                        action='version',
                        version='1.0')
    return parser.parse_args()


