import logging
import re

from ufw_parser.utils import find_files,read_remote_files_sudo


logger = logging.getLogger("ufw_parser_log")


def parse_ufw_rules_file(hostname, file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return rule_parser(hostname, lines)


def rule_parser(hostname, input_data):
    rules = []
    comment = ''
    logger.info(f'Processing rules for {hostname}.')
    for line in input_data:
        logger.info(f'Processing line {line}')
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


def get_rules(server_data):
    server_rules = []
    hostname = server_data['hostname']
    processing = server_data['processing']
    rule_path = server_data['rule_path']
    if processing == 'local':
        #rule_path = server_data.get('rule_path')
        logger.info(f'Processing {processing} configuration for {hostname} using rule path {rule_path}')
        files = find_files(rule_path, '*.rules')
        logger.info(f'Found {len(files)} rule files for {hostname}.')
        for file in files:
            logger.info(f'Processing {file}')
            parsed_rules = parse_ufw_rules_file(hostname, file)
            server_rules.extend(parsed_rules)
    elif processing == 'remote':
        if server_data.get('use_ssh_agent') == True:
            logger.info(f'Processing {processing} configuration for {hostname} using ssh agent keys.')
        # Use SSH agent for authentication
        else:
            ssh_user = server_data.get('ssh_user')
            ssh_pass = server_data.get('ssh_pass')
            logger.info(
                f'Processing {processing} configuration for {hostname} using ssh credentials: {ssh_user} - XXXXXX.')
            retrieved_rules = read_remote_files_sudo(hostname, ssh_user, rule_path, ssh_pass)
            parsed_rules = rule_parser(hostname, retrieved_rules)
            server_rules.extend(parsed_rules)
    return server_rules


def process_data(config_data):
    all_rules = []
    for server, details in config_data['servers'].items():
        rules = get_rules(details)
        all_rules.extend(rules)
    return all_rules