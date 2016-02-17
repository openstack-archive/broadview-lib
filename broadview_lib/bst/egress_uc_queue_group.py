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

import ucbuffercount

class EgressUcQueueGroupEntry():
    def __init__(self):
        self._queueGroup = None
        self._ucbuffercount = ucbuffercount.UcBufferCount()

    def getQueueGroup(self):
        return self._queueGroup

    def getUcBufferCount(self):
        return self._ucbuffercount.value

class EgressUcQueueGroup():
    def __init__(self):
        self.__table = []

    def __repr__(self):
        return "egress-uc-queue-group"

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

    def parse(self, data):
        for x in data:
            val = EgressUcQueueGroupEntry()
            val._queueGroup = x[0]
            val._ucbuffercount.parse(x)
            self.__table.append(val)



