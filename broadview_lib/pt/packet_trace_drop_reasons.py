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


class PacketTraceSupportedDropReasons():

    def __init__(self):
        self._reasons = []

    def getReasons(self):
        return self._reasons

    def __repr__(self):
        return "packet-trace-supported-drop-reasons"

    def parse(self, data):
        ret = True
        self._reasons = data
        return ret
