import argparse
import json
import os
import sys
from datetime import datetime


def load_data(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data


if __name__ == "__main__":
    """Argparse"""
    ap = argparse.ArgumentParser(
        prog='tsmd',
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

    """tsmd"""
    print('Loading data...')
    data = load_data(session_file)

    print(f"Total data pre-processing: ", len(data))
    print('Processing data...')
    encountered = set()
    # Mutates the data
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

    """update the broken metadata"""
    print("Printing windows to delete...")
    to_remove = []
    for i, d in enumerate(data):
        windows_to_delete = []
        tabs_length = 0
        for windowId, tabs in d['windows'].items():
            # check whether windows are still filled (also check for multiple windows)
            if len(tabs) == 0:
                windowsNumber = int(d['windowsNumber']) - 1
                d['windowsNumber'] = windowsNumber
                if windowsNumber == 0:
                    # pop or delete operations decrease the index count
                    # so use i - len(to_remove)
                    to_remove.append(i - len(to_remove))
                windows_to_delete.append(windowId)
                print(f"\tgot {windowsNumber} on {d['name']}")
            else:
                tabs_length += len(tabs)

        # update metadata
        for windowId in windows_to_delete:
            del d['windows'][windowId]
            del d['windowsInfo'][windowId]
        assert d['windowsNumber'] == len(d['windows'].keys()), f"{d['name']}"
        assert d['windowsNumber'] == len(d['windowsInfo'].keys()), f"{d['name']}"
        d["tabsNumber"] = tabs_length

    print(f"Number of windows to be removed: {len(to_remove)}")
    for index in to_remove:
        d = data.pop(index)
        assert d['windowsNumber'] == 0, "Windows number should be zero"
    print(f"Total data post-processing: ", len(data))

    """dump data"""
    print('Dumping data...')
    now = (datetime.now().strftime("%Y-%m-%d"))
    with open(f'data/deduplicated-session-{now}.json', 'w') as f:
        json.dump(data, f, indent=2)

    print('Done!')
