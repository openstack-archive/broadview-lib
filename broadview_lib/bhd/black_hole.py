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

import agent_sampling_params
import sflow_sampling_params

class BlackHole():

    AgentSampling = 1
    SFlowSampling = 2

    def __init__(self):
        self._portList = []
        self._samplingMethod = None
        self._samplingParams = None

    def getSamplingMethod(self):
        return self._samplingMethod

    def getPortList(self):
        return self._portList

    def getSamplingParams(self):
        return self._samplingParams

    def __repr__(self):
        return "get-black-hole"

    def parse(self, data):
        ret = True
        if "sampling-method" in data:
            if data["sampling-method"] == "sflow":
                self._samplingMethod = BlackHole.SFlowSampling
                self._samplingParams = sflow_sampling_params.SFlowSamplingParams()
            elif data["sampling-method"] == "agent":
                self._samplingMethod = BlackHole.AgentSampling
                self._samplingParams = agent_sampling_params.AgentSamplingParams()
            else:
                ret = False
        else:
            ret = False 

        if ret:
            if not "port-list" in data:
                ret = False
            else:
                self._portList = data["port-list"]

        if ret:
            ret = self._samplingParams.parse(data) 

        return ret
