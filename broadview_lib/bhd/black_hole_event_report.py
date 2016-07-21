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

class BlackHoleEventReport():

    def __init__(self):
        self._ingressPort = None
        self._egressPortList = []
        self._blackHoledPacketCount = 0
        self._samplePacket = None

    def getIngressPort(self):
        return self._ingressPort

    def getEgressPortList(self):
        return self._egressPortList

    def getBlackHoledPacketCount(self):
        return self._blackHoledPacketCount

    def getSamplePacket(self):
        return self._samplePacket

    def __repr__(self):
        return "get-black-hole-event-report"

    def parse(self, data):
        ret = True
        if "ingress-port" in data:
            self._ingressPort = data["ingress-port"]
        else:
            ret = False 

        if "egress-port-list" in data:
            self._egressPortList = data["egress-port-list"]
        else:
            ret = False 

        if "black-holed-packet-count" in data:
            self._blackHoledPacketCount = data["black-holed-packet-count"]
        else:
            ret = False 

        if "sample-packet" in data:
            self._samplePacket = data["sample-packet"]
        else:
            ret = False 

        return ret
