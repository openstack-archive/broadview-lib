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

import ConfigParser
import json
import unittest

class BroadViewLibConfig():
    cfg = None

    def __init__(self):
        if not BroadViewLibConfig.cfg:
            try:
                BroadViewLibConfig.cfg = ConfigParser.ConfigParser()
                BroadViewLibConfig.cfg.read("/etc/broadviewlib.conf")
            except:
                BroadViewLibConfig.cfg = None
                pass

    def getRequestIDFile(self):
        ret = "/tmp/bvserial.txt"
        try:
            ret = BroadViewLibConfig.cfg.get("misc", "json_rpc_id_path")
        except:
            pass

        return ret

class BroadViewBSTSwitches():
    cfg = None
    bst_switches = None

    def __init__(self):
        if not BroadViewBSTSwitches.bst_switches:
            try:
                BroadViewBSTSwitches.cfg = ConfigParser.ConfigParser()
                BroadViewBSTSwitches.cfg.read("/etc/broadviewswitches.conf")
                BroadViewBSTSwitches.bst_switches = json.loads(BroadViewBSTSwitches.cfg.get("topology", "bst_switches"))
            except:
                pass

    def __len__(self):
        if BroadViewBSTSwitches.bst_switches:
            return len(BroadViewBSTSwitches.bst_switches)
        else:
            return 0 

    def getByIP(self, ip):
        ret = None
        for x in range(self.__len__()):
            if BroadViewBSTSwitches.bst_switches[x]["ip"] == ip:
                ret = BroadViewBSTSwitches.bst_switches[x] 
                break
        return ret

    def get(self, i):
        ret = None
        if i >= 0 and i < len(BroadViewBSTSwitches.bst_switches):
            ret = BroadViewBSTSwitches.bst_switches[i]
        return ret

    def __iter__(self):
        self.__n = 0
        return self

    def next(self):
        if BroadViewBSTSwitches.bst_switches == None:
            raise StopIteration

        if self.__n >= len(BroadViewBSTSwitches.bst_switches):
            raise StopIteration
        else:
            n = self.__n
            self.__n += 1
            return BroadViewBSTSwitches.bst_switches[n]

class TestBSTSwitches(unittest.TestCase):

    def test1(self):
        x = BroadViewBSTSwitches()

        for y in x:
            self.assertTrue("ip" in y)
            self.assertTrue("port" in y)
            self.assertTrue("description" in y)

if __name__ == "__main__":
    unittest.main()


