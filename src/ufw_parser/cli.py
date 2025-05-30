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
                        default='~/.config/ufw_parser/hosts.yml',
                        help='Path to the configuration file.')
    parser.add_argument('-l', '--log',
                        action='store',
                        dest='log',
                        default='~/.config/ufw_parser/',
                        help='Directory to store log files. Default: ~/.config/ufw_parser/')
    parser.add_argument('-o', '--output',
                        choices=['screen', 'csv', 'excel', 'ansible_yaml'],
                        action='store',
                        dest='output',
                        default='screen',
                        help='Output format')
    parser.add_argument('-of', '--output_folder',
                        action='store',
                        dest='output_folder',
                        default='~/.config/ufw_parser/',
                        help='Output file destination.')
    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='Enable debug output (set log level to DEBUG)')
    parser.add_argument('-v', '--version',
                        action='version',
                        version='1.0')
    return parser.parse_args()


