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

import umsharebuffercount
import umheadroombuffercount

class IngressPortPriorityGroupEntry():
    def __init__(self):
        self._port = None
        self._priorityGroup = None
        self._umsharebuffercount = umsharebuffercount.UmShareBufferCount()
        self._umheadroombuffercount = umheadroombuffercount.UmHeadroomBufferCount()

    def getPort(self):
        return self._port

    def getPriorityGroup(self):
        return self._priorityGroup

    def getUmShareBufferCount(self):
        return self._umsharebuffercount.value

    def getUmHeadroomBufferCount(self):
        return self._umheadroombuffercount.value

class IngressPortPriorityGroup():
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
        return "ingress-port-priority-group"

    def parse(self, data, port=None):
        for x in data:
            val = IngressPortPriorityGroupEntry()
            if port != None:
                val._port = port
            val._priorityGroup = x[0]
            val._umsharebuffercount.parse(x)
            val._umheadroombuffercount.parse(x)
            self.__table.append(val)
