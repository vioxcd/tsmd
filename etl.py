import os
import csv
import json
from datetime import datetime

from tqdm import tqdm
from typing import List, Optional
from pydantic import BaseModel


class Tab(BaseModel):
    id: int
    index: int
    windowId: int
    pinned: bool
    lastAccessed: datetime
    url: str
    title: str


class Session(BaseModel):
    id: str
    name: str
    sessionStartTime: datetime
    date: datetime
    tag: List[str]
    tabs: List[Tab]


def timestamp_to_date(some_date, as_string=True):
    converted_date = datetime.utcfromtimestamp(some_date / 1000)
    if as_string:
        return converted_date.strftime('%d-%m-%Y %H:%M:%S')
    return converted_date


def _load_file(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data


def load_data(files):
    data = []
    for file in files:
        data.extend(_load_file(file))
    return data


def create_sessions(data):
    '''Flatten tabs & add tabs to sessions data'''
    sessions: List[Session] = []
    for i, d in enumerate(data):
        tabs = []
        for _, tabsId in d['windows'].items():
            for _, tab in tabsId.items():
                tabs.append(tab)
        assert len(tabs) == d['tabsNumber'], f"Wrong on index {i}"
        d['tabs'] = tabs  # mutates

        session = Session(**d)
        sessions.append(session)
    assert len(sessions) == len(data)
    return sessions


def dump_sessions(sessions, filename='data/dump.csv'):
    with open(filename, 'w') as f:
        session_headers = ['id', 'name', 'sessionStartTime', 'date', 'tag']
        tabs_headers = [
            'tab_id', 'index', 'windowId', 'pinned', 'lastAccessed', 'url',
            'title'
        ]

        csv_writer = csv.writer(f)
        csv_writer.writerow(session_headers + tabs_headers)

        for s in tqdm(sessions):
            d = s.dict()

            d['date'] = d['date'].strftime('%Y-%m-%d %H:%M:%S')
            d['sessionStartTime'] = d['sessionStartTime'].strftime(
                '%Y-%m-%d %H:%M:%S')

            row_session_part = [d[k] for k in session_headers]

            for tab in d['tabs']:
                tab['tab_id'] = tab['id']  # lol
                tab['lastAccessed'] = tab['lastAccessed'].strftime(
                    '%Y-%m-%d %H:%M:%S')
                row_tabs_part = [tab[k] for k in tabs_headers]

                csv_writer.writerow(row_session_part + row_tabs_part)


if __name__ == '__main__':
    session_folder_path = '/home/uchan/Documents/me/browsing-sessions'
    files = [
        os.path.join(session_folder_path, f)
        for f in os.listdir(session_folder_path)
        if os.path.isfile(os.path.join(session_folder_path, f))
    ]

    print(f"Loading data...")
    data = load_data(files)

    print(f"Creating sessions structure...")
    sessions = create_sessions(data)

    print(f"Dumping sessions...")
    dump_sessions(sessions)
