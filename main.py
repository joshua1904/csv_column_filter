import csv
import copy
import logging

from keys import KEYS, REIHENFOLGE

logger = logging.getLogger(__name__)

CSV_PATH = "beispiel.csv"
NEW_CSV_PATH = "xxxx.csv"


def get_csv_as_dict(filepath: str) -> dict:
    csv_dict = dict()
    keys = list()
    with open(filepath, "r") as f:
        for row in csv.reader(f, delimiter=";"):
            if not csv_dict:
                keys = copy.copy(row)
                for i in row:
                    csv_dict[i] = []
                continue
            for counter, i in enumerate(row):
                csv_dict[keys[counter]].append(i)
    return csv_dict


def get_dict_with_right_keys(current_dict: dict) -> dict:
    new_dict = dict()
    for current_key, current_value in current_dict.items():
        found = False
        for key, value in KEYS.items():
            if current_key in value:
                new_dict[key] = current_value
                found = True
        if not found:
            logger.warning(f"{current_key} not in given keys")

    return new_dict


def get_safe_string(current_dict: dict, keys: list) -> str:
    safe_csv_str = ";".join(keys) + "\n"
    for i in range(1, len(current_dict[list(current_dict.keys())[0]])):
        row_str = ""
        for key in keys:
            row_str += current_dict[key][i] + ";"
        safe_csv_str += row_str + "\n"
    return safe_csv_str


def validate_if_all_keys_were_given(current_keys: list):
    complete = True
    for key in KEYS:
        if key not in current_keys:
            logger.warning(f"{key} not found")
            complete = False
    return complete


def safe(filepath: str, safe_str):
    with open(filepath, "w") as f:
        f.write(safe_str)


if __name__ == "__main__":
    csv_dict = get_csv_as_dict(CSV_PATH)
    dict_with_right_keys = get_dict_with_right_keys(csv_dict)
    if validate_if_all_keys_were_given(list(dict_with_right_keys.keys())):
        safe_string = get_safe_string(dict_with_right_keys, REIHENFOLGE)
        safe(NEW_CSV_PATH, safe_string)
    else:
        logger.warning("Mach die KEys vollständig dann bekommst du auch deine Datei (CSV FILE NICHT KREIRT)")
