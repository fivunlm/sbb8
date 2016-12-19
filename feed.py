import datetime
import feedparser
import time

import logging

import re

URL = 'http://dfw111vstcs1:10123/guestAuth/feed.html?buildTypeId=bt31&buildTypeId=bt24&buildTypeId=bt25&buildTypeId=bt26&buildTypeId=bt32&buildTypeId=bt9&buildTypeId=bt17&buildTypeId=bt11&buildTypeId=bt33&buildTypeId=bt13&buildTypeId=bt20&buildTypeId=bt15&buildTypeId=FusionRelease_FusionBinariesLinux&buildTypeId=FusionRelease_FusionBinariesWindows&buildTypeId=FusionRelease_FusionConsole&buildTypeId=FusionRelease_FusionWeb&buildTypeId=FusionRelease40_FusionBinariesLinux&buildTypeId=FusionRelease40_FusionBinariesWindows&buildTypeId=FusionRelease40_FusionConsole&buildTypeId=FusionRelease40_FusionWeb&buildTypeId=Systems_ForecourtController_FusionRelease41_FusionBinariesLinux&buildTypeId=Systems_ForecourtController_FusionRelease41_FusionBinariesWindows&buildTypeId=Systems_ForecourtController_FusionRelease41_FusionConsole&buildTypeId=Systems_ForecourtController_FusionRelease41_FusionWeb&buildTypeId=Systems_ForecourtController_FusionRelease42_FusionBinariesLinux&buildTypeId=Systems_ForecourtController_FusionRelease42_FusionBinariesWindows&buildTypeId=Systems_ForecourtController_FusionRelease42_FusionConsole&buildTypeId=Systems_ForecourtController_FusionRelease42_FusionWeb&buildTypeId=Systems_ForecourtController_FusionRelease43_FusionBinariesLinux&buildTypeId=Systems_ForecourtController_FusionRelease43_FusionBinariesWindows&buildTypeId=Systems_ForecourtController_FusionRelease43_FusionConsole&buildTypeId=Systems_ForecourtController_FusionRelease43_FusionWeb&buildTypeId=Systems_ForecourtController_FusionRelease44_FusionBinariesLinux&buildTypeId=Systems_ForecourtController_FusionRelease44_FusionBinariesWindows&buildTypeId=Systems_ForecourtController_FusionRelease44_FusionConsole&buildTypeId=Systems_ForecourtController_FusionRelease44_FusionWeb&buildTypeId=Systems_ForecourtController_FusionRelease45_FusionBinariesLinux&buildTypeId=Systems_ForecourtController_FusionRelease45_FusionBinariesWindows&buildTypeId=Systems_ForecourtController_FusionRelease45_FusionConsole&buildTypeId=Systems_ForecourtController_FusionRelease45_FusionWeb&buildTypeId=Systems_ForecourtController_FusionReleaseMid40_FusionBinariesLinux&buildTypeId=Systems_ForecourtController_FusionReleaseMid40_FusionBinariesWindows&buildTypeId=Systems_ForecourtController_FusionReleaseMid40_FusionConsole&buildTypeId=Systems_ForecourtController_FusionReleaseMid40_FusionWeb&buildTypeId=bt45&buildTypeId=bt46&buildTypeId=bt47&buildTypeId=bt48&buildTypeId=bt40&buildTypeId=bt41&buildTypeId=bt42&buildTypeId=bt43&buildTypeId=bt53&buildTypeId=bt55&buildTypeId=bt56&buildTypeId=bt72&buildTypeId=bt73&buildTypeId=bt74&buildTypeId=bt75&itemsType=builds&buildStatus=successful&buildStatus=failed&userKey=guest'

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
