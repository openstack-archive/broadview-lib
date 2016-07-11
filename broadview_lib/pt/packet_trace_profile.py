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

import laglinkresolution
import ecmplinkresolution

class PacketTraceProfileEntry():
    def __init__(self):
        self._port = None
        self._realm = None
        self._laglinkresolution = None
        self._ecmplinkresolution = None

    def getRealm(self):
        return self._realm

    def getPort(self):
        return self._port

    def getLAGLinkResolution(self):
        return self._laglinkresolution

    def getECMPLinkResolution(self):
        return self._ecmplinkresolution

class PacketTraceProfile():
    def __init__(self):
        self.__table = []

    def __init__(self):
        self.__table = []

    def __iter__(self):
        self.__n = 0
        return self

    def next(self):
        if self.__n >= len(self.__table):
            raise StopIteration
        else:
            n = self.__n
            self.__n += 1
            return self.__table[n]

    def __repr__(self):
        return "packet-trace-profile"

    def parse(self, data, port=None):
        ret = True
        for x in data:
            val = PacketTraceProfileEntry()
            if port != None:
                val._port = port
            else:
                ret = False
                break
            if not "realm" in x:
                ret = False
                break
            else:
                val._realm = x["realm"]
            if not "data" in x:
                ret = False
                break
            if x["realm"] == "lag-link-resolution":
                val._laglinkresolution = laglinkresolution.LAGLinkResolution()
                if val._laglinkresolution.parse(x["data"]):
                    self.__table.append(val)
                else:
                    ret = False
                    break
            elif x["realm"] == "ecmp-link-resolution":
                val._ecmplinkresolution = ecmplinkresolution.ECMPLinkResolution()
                if val._ecmplinkresolution.parse(x["data"]):
                    self.__table.append(val)
                else:
                    ret = False
                    break
            else:
                ret = False
                break
        return ret
