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

class AgentSamplingParams():

    def __init__(self):
        self._waterMark = 0
        self._samplePeriodicity = 0
        self._sampleCount = 0

    def getWaterMark(self):
        return self._waterMark

    def getSamplePeriodicity(self):
        return self._samplePeriodicity

    def getSampleCount(self):
        return self._sampleCount

    def __repr__(self):
        return "agent-sampling-params"

    def parse(self, data):
        ret = True
        
        if "sampling-params" in data:
            p = data["sampling-params"]
        else:
            ret = False 

        if ret:
            if "water-mark" in p:
                self._waterMark = p["water-mark"]
            else:
                ret = False
            if "sample-periodicity" in p:
                self._samplePeriodicity = p["sample-periodicity"]
            else:
                ret = False
            if "sample-count" in p:
                self._sampleCount = p["sample-count"]
            else:
                ret = False

        return ret
