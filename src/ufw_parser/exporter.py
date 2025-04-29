import logging
import os
import pandas as pd
import yaml
from datetime import datetime

logger = logging.getLogger("ufw_parser_log")

class RuleExporter:
    def __init__(self, dest_folder="~/.ufw_parser/"):
        self.dest_folder = os.path.expanduser(dest_folder)
        os.makedirs(self.dest_folder, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def export_to_screen(self, dataframe):
        df = pd.DataFrame(dataframe)
        print(df)

    def export_to_csv(self, dataframe):
        filepath = f'{self.dest_folder}/ufw_rules_{self.timestamp}.csv'
        df = pd.DataFrame(dataframe)
        try:
            df.to_csv(filepath, index=False)
            logger.info(f"Data exported to {filepath} successfully.")
        except Exception as e:
            logger.error(f"Failed to export data to CSV: {e}")

    def export_to_excel(self, dataframe):
        filepath = f'{self.dest_folder}/ufw_rules_{self.timestamp}.xlsx'
        df = pd.DataFrame(dataframe)
        try:
            df.to_excel(filepath, index=False)
            logger.info(f"Data exported to {filepath} successfully.")
        except Exception as e:
            logger.error(f"Failed to export data to Excel: {e}")

    def export_to_ansible_yaml(self, dataframe):
        df = pd.DataFrame(dataframe)
        grouped = df.groupby('Hostname')

        for hostname, group in grouped:
            ansible_rules = []
            for _, row in group.iterrows():
                rule_entry = {
                    'port': int(row['Port']) if row['Port'] != 'any' else None,
                    'proto': row['Protocol'] if row['Protocol'] != 'any' else 'tcp',
                }
                if row['Source'] != '0.0.0.0/0':
                    rule_entry['src'] = row['Source']
                if row['Comment']:
                    rule_entry['comment'] = row['Comment']

                action = row['Action'].upper()
                if action == 'ACCEPT':
                    rule_entry['rule'] = 'allow'
                elif action == 'REJECT':
                    rule_entry['rule'] = 'deny'
                elif action == 'LIMIT':
                    rule_entry['rule'] = 'limit'
                else:
                    rule_entry['rule'] = 'allow'

                ansible_rules.append(rule_entry)

            host_folder = os.path.join(self.dest_folder, hostname)
            os.makedirs(host_folder, exist_ok=True)

            output = {
                'ufw_rules': ansible_rules
            }

            filepath = os.path.join(host_folder, "ufw_rules.yml")
            try:
                with open(filepath, 'w') as file:
                    yaml.safe_dump(output, file, default_flow_style=False, sort_keys=False)
                logger.info(f"Exported Ansible host_vars YAML for {hostname} to {filepath}")
            except Exception as e:
                logger.error(f"Failed to export Ansible YAML for {hostname}: {e}")

    def export(self, rules, dest="screen"):
        if dest == "screen":
            self.export_to_screen(rules)
        elif dest == "csv":
            self.export_to_csv(rules)
        elif dest == "excel":
            self.export_to_excel(rules)
        elif dest == "ansible_yaml":
            self.export_to_ansible_yaml(rules)
        else:
            logger.error(f"Unknown export format: {dest}")
