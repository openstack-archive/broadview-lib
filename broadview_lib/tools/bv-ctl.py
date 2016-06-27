#!/usr/bin/python

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

from broadview_lib.config.broadview import *
from broadview_lib.config.broadviewconfig import BroadViewBSTSwitches
import sys
import json

class BroadViewCommand():
    def __init__(self):
        self._timeout = 30
        self.__cmds = { 
                        "get-switch-properties" : self.handleGetSwitchProperties,
                        "get-system-feature" : self.handleGetSystemFeature,
                        "help": self.handleHelp,
                      }

        self.__help = { 
                        "get-switch-properties" : self.helpGetSwitchProperties,
                        "get-system-feature" : self.helpGetSystemFeature,
                      }

    def getTimeout(self, args):
        timeout = 30
        usage = False
        for x in args:
            if "timeout:" in x:
                v = x.split(":")
                if len(v) == 2:
                    timeout = int(v[1])
                else:
                    print "invalid timeout"
                    usage = True
        return usage, timeout

    def getASICHostPort(self, args):
        usage = False
        asic = "1"
        port = 8080
        host = None

        for x in args:
            if "asic-id:" in x:
                v = x.split(":")
                if len(v) == 2:
                    asic = v[1]
                else:
                    print "invalid asic-id"
                    usage = True
            if "host:" in x:
                v = x.split(":")
                if len(v) == 2:
                    host = v[1]
                else:
                    print "invalid host"
                    usage = True
            if "port:" in x:
                v = x.split(":")
                if len(v) == 2:
                    port = int(v[1])
                else:
                    print "invalid port"
                    usage = True

        if host == None:
            # host is required
            print "missing host"
            usage = True

        return  usage, asic, host, port 

    def usage(self):
        print "usage: %s cmd host:ipv4 [timeout:seconds] [port:port] [asic-id:id] [args]" % (sys.argv[0])
        print
        print "Commands:"
        print
        for key, val in self.__help.iteritems():
            print
            val(key)

    def handleHelp(self, args):
        usage = True

        if len(args):
            cmd = args[0]
            if cmd in self.__help:
                self.__help[cmd](cmd)
                usage = None

        return usage, None

    def handleGetSwitchProperties(self, args):
        usage = False
        ret = None
        usage, asic, host, port = self.getASICHostPort(args)
        if not usage:
            x = GetSwitchProperties(host, port)
            x.setASIC(asic)
            status = x.send(self._timeout)
            if status == 200:
                ret = json.dumps(x.getJSON())
                print ret
            else:
                print "failure: %d" % (status)

        return usage, ret

    def helpGetSwitchProperties(self, name):
        print name

    def handleGetSystemFeature(self, args):
        usage = False
        ret = None
        usage, asic, host, port = self.getASICHostPort(args)
        if not usage:
            x = GetSystemFeature(host, port)
            x.setASIC(asic)
            status = x.send(self._timeout)
            if status == 200:
                ret = json.dumps(x.getJSON())
                print ret
            else:
                print "failure: %d" % (status)

        return usage, ret

    def helpGetSystemFeature(self, name):
        print name

    def isCmd(self, cmd):
        return cmd in self.__cmds

    def handle(self, args):
        usage = True
        ret = {}
        status = False
        if len(args):
            cmd = args.pop(0)
            if self.isCmd(cmd):
                usage, ret = self.__cmds[cmd](args)
        return usage, ret 

def main(argv):
    x = BroadViewCommand()
    usage, ret = x.handle(argv)       
    if usage:
        x.usage()

if __name__ == "__main__":
    main(sys.argv[1:])
