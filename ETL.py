#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import json
from datetime import datetime

import pandas as pd


# #### Initial Load

# In[ ]:


SESSION_FOLDER_PATH = '/home/uchan/Documents/me/browsing-sessions'
FILES = list(map(lambda p: os.path.join(SESSION_FOLDER_PATH, p), os.listdir(SESSION_FOLDER_PATH)))


# In[3]:


def timestamp_to_date(some_date, as_string=True):
    converted_date = datetime.utcfromtimestamp(some_date/1000)
    if as_string:
        return converted_date.strftime('%d-%m-%Y %H:%M:%S')
    return converted_date


def _load_file(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data


def check_browsing_periods(file):
    print(f'loading {file}')
    data = _load_file(file)
    
    total_record = len(data)
    earliest_record = timestamp_to_date(data[0]['date'])
    latest_record   = timestamp_to_date(data[-1]['date'])
    
    print(f'Total record   : {total_record}')
    print(f'Earliest record: {earliest_record}')
    print(f'Latest record  : {latest_record}')
    print('=' * 15)


# #### Extraction

# In[192]:


def extract_data_from_window(data):
    records = []
    for session in data:
        for window_id in session['windows']:
            for tab in session['windows'][window_id].values():
                record = {
                    'session_id': session['id'],
                    'session_tabsNumber': session['tabsNumber'],
                    'session_name': session['name'],
                    'session_date': session['date'],
                    'session_tag': session['tag'],
                    'session_sessionStartTime': session['sessionStartTime'],
                    'tab_name': tab['title'],
                    'tab_url': tab['url'],
                    'tab_lastAccessed': tab['lastAccessed']
                }
                records.append(record)

    return records


# In[183]:


"""Join all the data for easier analysis"""
data = []

for file in FILES:
    print(f'processing {file}')
    json_data = _load_file(file)
    records = extract_data_from_window(json_data)
    data.extend(records)
    
print(f'Amount of data: {len(data)}')


# In[ ]:


df = pd.DataFrame(data)


# In[197]:


"""Dumping files"""
CSV_PATH = 'merged_sessions.csv'
df.to_csv(CSV_PATH, index=False)

JSON_PATH = 'merged_sessions.json'
df.to_json(JSON_PATH, indent=4)

