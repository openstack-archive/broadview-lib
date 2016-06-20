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


class PacketTraceDropReason():

    def __init__(self):
        self._reason = None
        self._portList = None
        self._sendDroppedPacket = None
        self._traceProfile = None
        self._packetCount = None
        self._packetThreshold = None

    def getReason(self):
        return self._reason

    def getPortList(self):
        return self._portList

    def getSendDroppedPacket(self):
        return self._sendDroppedPacket

    def getTraceProfile(self):
        return self._traceProfile

    def getPacketCount(self):
        return self._packetCount

    def getPacketThreshold(self):
        return self._packetThreshold

    def __repr__(self):
        return "packet-trace-drop-reason"

    def parse(self, data):

        ret = True

        while True:
            if not "reason" in data:
                ret = False
                break
            self._reason = data["reason"]
            if not "port-list" in data:
                ret = False
                break
            self._portList = data["port-list"]
            if not "send-dropped-packet" in data:
                ret = False
                break
            self._sendDroppedPacket = data["send-dropped-packet"] == 1 
            if not "trace-profile" in data:
                ret = False
                break
            self._traceProfile = data["trace-profile"] == 1 
            if not "packet-count" in data:
                ret = False
                break
            self._packetCount = int(data["packet-count"])
            if not "packet-threshold" in data:
                ret = False
                break
            self._packetThreshold = int(data["packet-threshold"])
            break

        return ret
