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

import json
from collections import OrderedDict
from agentconnection import AgentConnection

class AgentAPI(object):
    __serial = 1
    def __init__(self):
        self.__httpMethod = "POST"
        self.__feature = None
        self.__auth = None
        self.__host = None
        self.__port = None
        self.__payload = None

    def setHost(self, host):
        self.__host = host

    def getHost(self):
        return self.__host

    def setPort(self, port):
        self.__port = port

    def getPort(self):
        return self.__port

    def setHttpMethod(self, method):
        self.__httpMethod = method

    def getHttpMethod(self):
        return self.__httpMethod

    def setFeature(self, feature):
        self.__feature = feature

    def getFeature(self):
        return self.__feature

    def getMethod(self):
        ret = None
        if self.__payload:
            ret = self.__payload["method"]
        return ret    

    def _send(self, o, timeout):
        self.__payload = {}
        self.__payload["jsonrpc"] = "2.0"
        self.__payload["asic-id"] = o["asic-id"]
        self.__payload["method"] = o["method"]
        self.__payload["params"] = o["params"]
        self.__payload["id"] = AgentAPI.__serial
        AgentAPI.__serial = AgentAPI.__serial + 1
        conn = AgentConnection(self.__host, self.__port, self.__feature, timeout)
        r = conn.makeRequest(self)
        conn.close()
        return r

    def getjson(self):
        x = json.dumps(OrderedDict(self.__payload))
        return x
