import os
import sys
import json
import argparse
from datetime import datetime

import pandas as pd


def load_data(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data


if __name__ == "__main__":
    """Argparse"""
    ap = argparse.ArgumentParser(
        prog='tsmdam',
        usage='%(prog)s [options] path_to_session_file',
        description=
        'Deduplicate and merge exported session data from Tab Session Manager plugin'
    )
    ap.add_argument('session_file',
                    metavar='path_to_session_file',
                    type=str,
                    help='path to session file')
    args = ap.parse_args()
    session_file = args.session_file

    if not os.path.isfile(session_file):
        print('The path specified does not exist')
        sys.exit()

    """tsmdam"""
    print('Loading data...')
    data = load_data(session_file)

    print('Processing data...')
    encountered = set()
    for d in data:
        for tabs in d['windows'].values():
            duplicated = []
            for tabId, tab in tabs.items():
                if tab['url'] in encountered:
                    duplicated.append(tabId)
                else:
                    encountered.add(tab['url'])
            for tabId in duplicated:
                del tabs[tabId]
    """dump data"""
    print('Dumping data...')
    now = (datetime.now().strftime("%Y-%m-%d"))
    with open(f'data/deduplicated-session-{now}.json', 'w') as f:
        json.dump(data, f, indent=2)

    print('Done!')
