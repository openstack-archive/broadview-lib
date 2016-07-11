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

class PacketTraceLAGResolution():

    def __init__(self):
        self._laglinkresolution = laglinkresolution.LAGLinkResolution()

    def getPort(self):
        return self._port

    def getLAGLinkResolution(self):
        return self._laglinkresolution

    def __repr__(self):
        return "packet-trace-lag-resolution"

    def parse(self, data, port=None):
        if port == None:
            ret = False
        else:
            self._port = port
            if "lag-link-resolution" in data:
                ret = self._laglinkresolution.parse(data["lag-link-resolution"])
            else:
                ret = False
        return ret
