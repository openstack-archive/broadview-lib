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

class ECMPMember():
    def __init__(self, id, ip, port):
        self._id = id
        self._ip = ip
        self._port = port

    def getId(self):
        return self._id

    def getIP(self):
        return self._ip

    def getPort(self):
        return self._port

class ECMPLinkResolutionEntry():
    def __init__(self):
        self.ecmp_group_id = None
        self.ecmp_members = []
        self.ecmp_dst_member = None
        self.ecmp_dst_port = None
        self.ecmp_next_hop_ip = None

    def getECMPGroupID(self):
        return self.ecmp_group_id

    def getECMPMembers(self):
        return self.ecmp_members

    def getECMPDstMember(self):
        return self.ecmp_dst_member

    def getECMPDstPort(self):
        return self.ecmp_dst_port

    def getECMPNextHopIP(self):
        return self.ecmp_next_hop_ip

    def parse(self, data):
        ret = True
        if "ecmp-group-id" in data:
            self.ecmp_group_id = data["ecmp-group-id"]
        else:
            ret = False
        if "ecmp-members" in data and type(data["ecmp-members"]) == list:
            for x in data["ecmp-members"]:
                val = ECMPMember(x[0], x[1], x[2])
                self.ecmp_members.append(val)
        else:
            ret = False
        if "ecmp-dst-member" in data:
            self.ecmp_dst_member = data["ecmp-dst-member"]
        else:
            ret = False
        if "ecmp-dst-port" in data:
            self.ecmp_dst_port = data["ecmp-dst-port"]
        else:
            ret = False
        if "ecmp-next-hop-ip" in data:
            self.ecmp_next_hop_ip = data["ecmp-next-hop-ip"]
        else:
            ret = False
        return ret

class ECMPLinkResolution():

    def __init__(self):
        self.__table = []

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

    def parse(self, data):
        #print "ECMPLinkResolution {}".format(data)
        #print type(data)
        ret = True
        for x in data:
            val = ECMPLinkResolutionEntry()
            ret = val.parse(x) 
            if not ret:
                break
            else:
                self.__table.append(val)
        return ret

    def __repr__(self):
        return "ecmp-link-resolution"

