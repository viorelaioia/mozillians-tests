#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import time
import requests


def get_login_link(username, message_count=1, timeout=60):
    username = username.partition('@restmail.net')[0]
    end_time = time.time() + timeout
    while (True):
        response = requests.get(
            'http://restmail.net/mail/%s' % username,
            verify=False)
        restmail = json.loads(response.content)
        requests.delete(
            'http://restmail.net/mail/%s' % username,
            verify=False)
        if len(restmail) == message_count:
            mail_content = restmail[0]['text'].replace('\n', ' ').replace('amp;', '').split(" ")
            for link in mail_content:
                if link.startswith("http"):
                    return link
        time.sleep(0.5)
        if (time.time() > end_time):
            break
    raise Exception('Timeout after %(TIMEOUT)s seconds getting restmail for '
                    '%(USERNAME)s. Expected %(EXPECTED_MESSAGE_COUNT)s '
                    'messages but there were %(ACTUAL_MESSAGE_COUNT)s.' % {
                        'TIMEOUT': timeout,
                        'USERNAME': username,
                        'EXPECTED_MESSAGE_COUNT': message_count,
                        'ACTUAL_MESSAGE_COUNT': len(restmail)})
