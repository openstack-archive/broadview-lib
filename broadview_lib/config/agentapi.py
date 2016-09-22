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

import json
from collections import OrderedDict
from agentconnection import AgentConnection
from broadviewconfig import BroadViewLibConfig
import fcntl

class AgentAPI(object):
    __serial = None
    __cfg = BroadViewLibConfig()
    def __init__(self):
        self.__httpMethod = "POST"
        self.__feature = None
        self.__auth = None
        self.__host = None
        self.__port = None
        self.__payload = None

    def setHost(self, host):
        self.__host = host

    def getHost(self):
        return self.__host

    def setPort(self, port):
        self.__port = port

    def getPort(self):
        return self.__port

    def setHttpMethod(self, method):
        self.__httpMethod = method

    def getHttpMethod(self):
        return self.__httpMethod

    def setFeature(self, feature):
        self.__feature = feature

    def getFeature(self):
        return self.__feature

    def getMethod(self):
        ret = None
        if self.__payload:
            ret = self.__payload["method"]
        return ret    
    
    def getLastUsedSerial(self):
        '''
        Some requests to the agent, like PT's get lag resolution with a
        non-zero collection interval, require knowlege of the JSON RPC 
        serial number because it is used as a key/index for later 
        cancelling the collection. While this violates layering, this is 
        no big deal if only one client (or client instance) ever connects 
        to an agent in the data center, and the client never generates
        (within reason) a request with a duplicate ID that maps to an ID
        used by the agent as an index.
         
        When multiple clients, or even clients that are restarted enter 
        the picture, requiring clients to generate IDs that are
        unique across applications and hosts is obviously more difficult. 
        Such difficulties are communication among clients within
        the datacenter to ensure that no client uses the same IDs as any
        other, and requiring each client to persist the last used ID in
        case of crash or restart. 

        The strategy we take here to deal with this is to use a file to 
        store the last used ID, and protect that file with a SYSV file 
        lock. If a client wants to make a request, the lock is acquired, 
        the last used ID is read from the file, the ID is incremented by 
        1 and the file rewritten, followed by release of the lock. Sharing 
        across nodes in the datacenter can be acheived by all hosts using 
        a lock file that is located in shared filesystem location, such 
        as NFS. 

        Obviously all apps on a host or within the datacenter that access
        a given agent must use the same ID file. If there are multiple agents
        in the datacenter (which is going to be the case, as no interesting
        datacenter is going to have one switch), there must be one (and only
        one) id file per switch/agent.

        We can eliminate this need for request ID management once the
        agent adopts a method where it allocates and returns handles for 
        objects and tasks that it is managing to be used by clients to 
        refer to those same objects and tasks in subsequent requests. 

        This function exposes the last used ID so that the client can use
        it in a subsequent (cancellation) request. 

        
        '''

        return AgentAPI.__serial

    def getIDFileLocation(self):
        return AgentAPI.__cfg.getRequestIDFile()

    def getNextSerial(self):

        '''
        Get the next request ID, updating the shared ID file. The name
        of the ID file comes from a configuration file named 
        /etc/broadviewlib.conf via a setting named json_rpc_id_path. Here 
        is an example conf file that sets the ID file path to /tmp/foo.txt:

        [misc]

        json_rpc_id_path = /tmp/foo.txt

        '''

        filename = self.getIDFileLocation()

        f = open(filename, "a").close()  # create if needed
        f = open(filename, "r+")
        fd = f.fileno()
        fcntl.lockf(fd, fcntl.LOCK_EX)
        serial = f.read()
        if len(serial) == 0:
            serial = 1        # new file, read zero bytes, so initialize
        else:
            serial = int(serial)
        f.seek(0)
        f.write("{}".format(serial + 1))
        fcntl.lockf(fd, fcntl.LOCK_UN)
        f.close()
        AgentAPI.__serial = serial # XXX not thread safe
        return serial

    def _send(self, o, timeout):
        self.__payload = {}
        self.__payload["jsonrpc"] = "2.0"
        self.__payload["asic-id"] = o["asic-id"]
        self.__payload["method"] = o["method"]
        self.__payload["params"] = o["params"]
        self.__payload["id"] = self.getNextSerial()
        conn = AgentConnection(self.__host, self.__port, self.__feature, timeout)
        r = conn.makeRequest(self)
        conn.close()
        return r

    def getjson(self):
        x = json.dumps(OrderedDict(self.__payload))
        return x
