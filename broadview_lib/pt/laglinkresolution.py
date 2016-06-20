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

class LAGLinkResolution():
    def __init__(self):
        self.lag_id = None
        self.lag_members = None
        self.dst_lag_member = None

    def getLAGID(self):
        return self.lag_id

    def getLAGMembers(self):
        return self.lag_members

    def getDstLAGMember(self):
        return self.dst_lag_member

    def __repr__(self):
        return "lag-link-resolution"

    def parse(self, data):
        ret = True
        if "lag-id" in data:
            self.lag_id = data["lag-id"]
        else:
            ret = False
        if "lag-members" in data and type(data["lag-members"]) == list:
            self.lag_members = data["lag-members"]
        else:
            ret = False
        if "dst-lag-member" in data:
            self.dst_lag_member = data["dst-lag-member"]
        else:
            ret = False
        return ret
