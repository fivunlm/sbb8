import datetime
import os

import feedparser

import re

URL = os.environ.get('FEED_URL')
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
