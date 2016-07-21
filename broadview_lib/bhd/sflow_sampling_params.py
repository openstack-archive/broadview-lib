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

class SFlowSamplingParams():

    def __init__(self):
        self._vlanId = 0
        self._dstIP = None
        self._srcUDPPort = 0
        self._dstUDPPort = 0
        self._mirrorPort = None
        self._samplePoolSize = 0

    def getVLANId(self):
        return self._vlanId

    def getDstIP(self):
        return self._dstIP

    def getSrcUDPPort(self):
        return self._srcUDPPort

    def getDstUDPPort(self):
        return self._dstUDPPort

    def getMirrorPort(self):
        return self._mirrorPort

    def getSamplePoolSize(self):
        return self._samplePoolSize

    def __repr__(self):
        return "sflow-sampling-params"

    def parse(self, data):
        ret = True
        
        if "sampling-params" in data:
            p = data["sampling-params"]
        else:
            ret = False 

        if ret:
            if "mirror-port" in p:
                self._mirrorPort = p["mirror-port"]
            else:
                ret = False
            if "sample-pool-size" in p:
                self._samplePoolSize = p["sample-pool-size"]
            else:
                ret = False
            if "encapsulation-params" in p:
                # embedded object, note we are changing p here
                p = p["encapsulation-params"]
            else:
                ret = False
            if "vlan-id" in p:
                self._vlanId = p["vlan-id"]
            else:
                ret = False

            if "destination-ip" in p:
                self._dstIP = p["destination-ip"]
            else:
                ret = False

            if "source-udp-port" in p:
                self._srcUDPPort = p["source-udp-port"]
            else:
                ret = False

            if "destination-udp-port" in p:
                self._dstUDPPort = p["destination-udp-port"]
            else:
                ret = False

        return ret
