import datetime
import os

import feedparser
import time

import logging

import re

URL = os.environ.get('FEED_URL')

last_checked = datetime.datetime.utcnow() - datetime.timedelta(days=10)

#
# while True:
#     entries = feedparser.parse(URL)
#
#     for entry in [e for e in entries['entries']]:
#         if 'failed' in entry['title']:
#             raw_data = entry['title'].split('::')
#             entry_date = datetime.datetime.strptime(entry['updated'], '%Y-%m-%dT%H:%M:%SZ')
#             if entry_date > last_checked:
#                 print(entry['date'] + ' ' + raw_data[3])
#
#     last_checked = datetime.datetime.utcnow()
#     time.sleep(10)

BUILD_REGEX = re.compile(r'^(?P<artifact>[\w\s]*)#(?P<version>\w*-[\d\w.]*)\s(?P<status>[\w\s]*)$')


def get_builds():
    entries = feedparser.parse(URL)
    builds = []
    for entry in [e for e in entries['entries']]:
        title = entry['title'].split('::')[-1]
        match = BUILD_REGEX.match(title)

        if not match:
            continue

        builds.append({
            'artifact': match.group('artifact'),
            'version': match.group('version'),
            'status': match.group('status'),
            'timestamp': entry['updated_parsed']
        })

    return builds
