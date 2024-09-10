import logging
import re


from ufw_parser.utils import find_files

logger = logging.getLogger("ufw_parser_log")


def parse_ufw_rules_file(hostname, file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    rules = []
    comment = ''
    for line in lines:
        if line.startswith('### tuple ###'):
            comment_match = re.search(r'comment=([0-9a-f]+)', line)
            if comment_match:
                comment = comment_match.group(1)
                comment = bytes.fromhex(comment).decode('utf-8')
        elif line.startswith('-A ufw-user-input'):
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
    if processing == 'local':
        rule_path = server_data.get('rule_path')
        logger.info(f'Processing {processing} configuration for {hostname} using rule path {rule_path}')
        files = find_files(rule_path, '*.rules')
        logger.info(f'Found {len(files)} rule files for {hostname}.')
        for file in files:
            logger.info(f'Processing {file}')
            parsed_rules = parse_ufw_rules_file(hostname, file)
            server_rules.extend(parsed_rules)
    elif processing == 'remote':
        if server_data.get('use_ssh_agent'):
            logger.info(f'Processing {processing} configuration for {hostname} using ssh agent keys.')
        # Use SSH agent for authentication
        else:
            ssh_user = server_data.get('ssh_user')
            ssh_key = server_data.get('ssh_key')
            logger.info(
                f'Processing {processing} configuration for {hostname} using ssh credentials: {ssh_user} - {ssh_key}.')
    return server_rules


def process_data(config_data):
    all_rules = []
    for server, details in config_data['servers'].items():
        hostname = details['hostname']
        processing = details['processing']
        rules = get_rules(details)
        all_rules.extend(rules)
    return all_rules