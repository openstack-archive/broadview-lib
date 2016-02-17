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

import mcbuffercount
import mcqueueentries

class EgressMcQueueEntry():
    def __init__(self):
        self._queue = None
        self._port = None
        self._mcbuffercount = mcbuffercount.McBufferCount()
        self._mcqueueentries = mcqueueentries.McQueueEntries()

    def getQueue(self):
        return self._queue

    def getPort(self):
        return self._port

    def getMCBufferCount(self):
        return self._mcbuffercount.value

    def getMCQueueEntries(self):
        return self._mcqueueentries.value

class EgressMcQueue():
    def __init__(self):
        self.__table = []

    def __repr__(self):
        return "egress-mc-queue"

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
            val = EgressMcQueueEntry()
            val._queue = x[0]
            val._port = x[1]
            val._mcbuffercount.parse(x)
            val._mcqueueentries.parse(x)
            self.__table.append(val)


