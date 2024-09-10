import logging
import pandas as pd


logger = logging.getLogger("ufw_parser_log")


def export_to_excel(dataframe):
    try:
        df = pd.DataFrame(dataframe)
        columns = list(df.columns)
        df = df[columns]
        df.to_excel('ufw_rules.xlsx', index=False)
        logger.info("Data exported to ufw_rules.xlsx successfully.")
    except Exception as e:
        logger.error("Failed to export data to Excel: " + str(e))


def export_to_csv(dataframe):
    try:
        df = pd.DataFrame(dataframe)
        columns = list(df.columns)
        df = df[columns]
        df.to_csv('ufw_rules.csv', index=False)
        logger.info("Data exported to ufw_rules.csv successfully.")
    except Exception as e:
        logger.error("Failed to export data to CSV: " + str(e))


def export_to_screen(dataframe):
    df = pd.DataFrame(dataframe)
    columns = list(df.columns)
    df = df[columns]
    print(df)


def export_rules(rules, dest="screen"):
    if dest == "screen":
        export_to_screen(rules)
    elif dest == "excel":
        export_to_excel(rules)
    elif dest == "csv":
        export_to_csv(rules)