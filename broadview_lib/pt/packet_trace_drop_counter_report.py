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


class PacketTraceDropCounterReportEntry():
    def __init__(self):
        self._realm = None
        self._port = None
        self._count = None

    def getRealm(self):
        return self._realm

    def getPort(self):
        return self._port

    def getCount(self):
        return self._count

class PacketTraceDropCounterReport():

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
        return "packet-trace-drop-counter-report"

    def parse(self, data):
        ret = True
        while True:
            if not "realm" in data:
                ret = False
                break
            else :
                realm = data["realm"] 
            if not "data" in data:
                ret = False
                break
            clean = True
            for y in data["data"]:
                val = PacketTraceDropCounterReportEntry()
                val._realm = realm
                if not "port" in y:
                    clean = False
                    break
                val._port = y["port"]
                if not "count" in y:
                    clean = False
                    break
                val._count = y["count"]
                self.__table.append(val)
            if not clean:
                ret = False
            break
                
        return ret
