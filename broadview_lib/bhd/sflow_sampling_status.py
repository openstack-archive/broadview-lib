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


class SFlowSamplingStatusEntry():
    def __init__(self):
        self._port = None
        self._sflowSamplingEnabled = False 
        self._sampledPacketCount = 0
        self._blackHoledPacketCount = 0

    def getSFlowSamplingEnabled(self):
        return self._sflowSamplingEnabled

    def getPort(self):
        return self._port

    def getSampledPacketCount(self):
        return self._sampledPacketCount

    def getBlackHoledPacketCount(self):
        return self._blackHoledPacketCount

class SFlowSamplingStatus():

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
        return "sflow-sampling-status"

    def parse(self, data):
        ret = True
        if not "data" in data:
            ret = False
        else: 
            for y in data["data"]:
                val = SFlowSamplingStatusEntry()
                if not "port" in y:
                    ret = False
                    break
                val._port = y["port"]
                if not "sflow-sampling-enabled" in y:
                    ret = False
                    break
                val._sflowSamplingEnabled = y["sflow-sampling-enabled"] == 1
                if not "sampled-packet-count" in y:
                    ret = False
                    break
                val._sampledPacketCount = y["sampled-packet-count"]
                if not "black-holed-packet-count" in y:
                    ret = False
                    break
                val._blackHoledPacketCount = y["black-holed-packet-count"]
                self.__table.append(val)
                
        return ret
