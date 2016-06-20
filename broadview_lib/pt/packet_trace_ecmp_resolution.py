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

import ecmplinkresolution

class PacketTraceECMPResolution():
    def __init__(self):
        self._port = None
        self._ecmplinkresolution = ecmplinkresolution.ECMPLinkResolution()

    def getPort(self):
        return self._port

    def getECMPLINKResolution(self):
        return self._ecmplinkresolution

    def __repr__(self):
        return "packet-trace-ecmp-resolution"

    def parse(self, data, port=None):
        ret = True

        while True:
            if "ecmp-link-resolution" not in data:
                ret = False
                break
            if port != None:
                self._port = port
            else:
                ret = False
                break
            ret = self._ecmplinkresolution.parse(data["ecmp-link-resolution"])
            break

        return ret
