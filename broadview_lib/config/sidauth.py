#
# (C) Copyright Broadcom Corporation 2016
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import requests

class SIDAuth(requests.auth.AuthBase):
    def __init__(self, host, port, username, password):
        super(SIDAuth, self).__init__()
        self._SID = None
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._login()

    def _getCookie(self):
        cookie = {}
        if self._SID:
            x = self._SID.split("=")
            cookie[x[0]] = x[1]
        return cookie

    def _login(self):
        url = "http://{}:{}/broadview/login?username={}&password={}".format(self._host, self._port, self._username, self._password) 
        r = requests.put(url)
        code = r.status_code
        if code == 200:
            try:
                self._SID = r.headers["Set-Cookie"]
            except:
                self._SID = None
    
    def logout(self):
        url = "http://{}:{}/broadview/logout".format(self._host, self._port) 
        r = requests.put(url, cookies=self._getCookie())
        self._SID = None

    def __call__(self, r):
        if self._SID:
            r.headers['Cookie'] = self._SID
        return r
