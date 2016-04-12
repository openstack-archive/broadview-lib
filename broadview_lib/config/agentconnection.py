#/*****************************************************************************
#*
#* (C) Copyright Broadcom Corporation 2015
#*
#* Licensed under the Apache License, Version 2.0 (the "License");
#* you may not use this file except in compliance with the License.
#*
#* You may obtain a copy of the License at
#* http://www.apache.org/licenses/LICENSE-2.0
#*
#* Unless required by applicable law or agreed to in writing, software
#* distributed under the License is distributed on an "AS IS" BASIS,
#* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#* See the License for the specific language governing permissions and
#* limitations under the License.
#*
#***************************************************************************/

import requests
import sys
import urllib
from xml.etree import ElementTree
import json

class RequestObj():
  pass

class RequestFailed(Exception):
  '''
  class to represent a failed RESTful call
  '''
  def __init__(self, url, http_code, open_code, open_msg):
    self._url = url
    self._http_code = int(http_code)
    self._open_code = int(open_code)
    self._open_msg = open_msg

  def __str__(self):
    return repr((self._url, self._http_code, self._open_code, self._open_msg))

class AgentConnection():
  def __init__(self, host, port, feature, timeout):
    self.host = host
    self.port = port
    self.feature = feature  # e.g., "bst"
    self._timeout = timeout

  def _is_ok(self, r):
    return r.status_code == 200

  def _raise_fail_if(self, url, r, timeout):
    if not self._is_ok(r):
      if timeout:
        j = {"response_code": r.status_code,
             "error_code": 0,
             "msg": "Connection timeout"}
      else:
        try:
          j = r.json()["status"]
        except:
          try:
            t = ElementTree.fromstring(r)
            j = {"response_code": r.status_code,
                 "error_code": 0,
                 "msg": "XML failure response from web server"}

          except:
            j = {"response_code": r.status_code,
                 "error_code": 0,
                 "msg": "Unparsable response from web server"}

      raise RequestFailed(url, j["response_code"], j["error_code"], j["msg"])

  def makeRequest(self, request):

    headers = {"Content-Type": "application/json"}
    timeout = False

    isGet = False
    if request.getHttpMethod() == "GET":
      isGet = True

    if False and isGet:
      payload = request.getjson().encode("utf-8")
      if self.feature:
        url = "http://%s:%d/broadview/%s/%s%s%s" % (self.host, self.port, self.feature, request.getMethod(), "?req=", payload)
      else:
        url = "http://%s:%d/broadview/%s%s%s" % (self.host, self.port, request.getMethod(), "?req=", payload)
      try:
        r = requests.get(url, timeout=self._timeout, headers=headers)
      except requests.exceptions.Timeout:
        timeout = True
    else:
      payload = request.getjson().encode("utf-8")
      if self.feature:
        url = "http://%s:%d/broadview/%s/%s" % (self.host, self.port, self.feature, request.getMethod())
      else:
        url = "http://%s:%d/broadview/%s" % (self.host, self.port, request.getMethod())
      if isGet:
        try:
          r = requests.get(url, timeout=self._timeout, data=payload, headers=headers)
        except requests.exceptions.Timeout:
          timeout = True
      else:
        try:
          r = requests.post(url, timeout=self._timeout, data=payload, headers=headers)
        except requests.exceptions.Timeout:
          timeout = True

    json_data = {}
    if timeout:
        r = RequestObj() 
        r.status_code = 500

    if r.status_code == 200:
        try:
            # Data can come back with leading.trailing spaces, which trips 
            # up requests' json parser. So get as test, string, and let
            # Python json do the parsing

            json_data = json.loads(r.text.strip())
        except:
            pass

    self._raise_fail_if(url, r, timeout)
    return (r.status_code, json_data)

