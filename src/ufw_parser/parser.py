import logging
import re

from ufw_parser.utils import find_files, read_remote_files_sudo

logger = logging.getLogger("ufw_parser_log")


class ServerRuleFetcher:
    def __init__(self, config_data):
        self.config_data = config_data

    def parse_ufw_rules_file(self, hostname, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        return self.rule_parser(hostname, lines)

    def rule_parser(self, hostname, input_data):
        rules = []
        comment = ''
        logger.info(f'Processing rules for {hostname}.')
        for line in input_data:
            logger.debug(f'Processing line {line}')
            if line.startswith('### tuple ###'):
                comment_match = re.search(r'comment=([0-9a-f]+)', line)
                if comment_match:
                    comment = comment_match.group(1)
                    comment = bytes.fromhex(comment).decode('utf-8')
            elif (line.startswith('-A ufw-user-input') or line.startswith('-A ufw6-user-input')):
                rule = {}
                protocol_match = re.search(r'-p (\w+)', line)
                port_match = re.search(r'--dport (\d+)', line)
                source_match = re.search(r'-s ([0-9.]+)', line)
                action_match = re.search(r'-j (\w+)', line)

                rule['Hostname'] = hostname
                rule['Protocol'] = protocol_match.group(1) if protocol_match else 'any'
                rule['Port'] = port_match.group(1) if port_match else 'any'
                rule['Source'] = source_match.group(1) if source_match else '0.0.0.0/0'
                rule['Action'] = action_match.group(1) if action_match else 'ACCEPT'
                rule['Comment'] = comment
                rules.append(rule)
        return rules

    def get_rules_for_server(self, server_data):
        server_rules = []
        hostname = server_data['hostname']
        processing = server_data['processing']
        rule_path = server_data['rule_path']
        ssh_user = server_data.get('ssh_user')

        if processing == 'local':
            logger.info(f'Processing {processing} configuration for {hostname} using rule path {rule_path}')
            files = find_files(rule_path, '*.rules')
            logger.info(f'Found {len(files)} rule files for {hostname}.')
            for file in files:
                logger.info(f'Processing {file}')
                parsed_rules = self.parse_ufw_rules_file(hostname, file)
                server_rules.extend(parsed_rules)
        elif processing == 'remote':
            use_ssh_agent = server_data.get('use_ssh_agent', True)
            ssh_pass = server_data.get('ssh_pass')

            logger.info(f'Processing {processing} configuration for {hostname} using SSH {"agent" if use_ssh_agent else "credentials"}.')
            retrieved_rules = read_remote_files_sudo(hostname, ssh_user, rule_path, password=None if use_ssh_agent else ssh_pass)
            parsed_rules = self.rule_parser(hostname, retrieved_rules)
            server_rules.extend(parsed_rules)

        return server_rules

    def fetch_all_rules(self):
        all_rules = []
        for server, details in self.config_data['servers'].items():
            rules = self.get_rules_for_server(details)
            all_rules.extend(rules)
        return all_rules
