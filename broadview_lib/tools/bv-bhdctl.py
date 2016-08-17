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

from broadview_lib.config.bhd import *
import sys
import json

class BHDCommand():
    def __init__(self):
        self._timeout = 30
        self.__cmds = { 
                        "detection-enable" : self.handleDetectionEnable,
                        "configure" : self.handleConfigure,
                        "cancel" : self.handleCancel,
                        "get-detection-enable" : self.handleGetDetectionEnable,
                        "get" : self.handleGet,
                        "get-sflow-sampling-status" : self.handleGetSFlowSamplingStatus,
                        "help": self.handleHelp,
                      }

        self.__help = { 
                        "detection-enable" : self.helpDetectionEnable,
                        "configure" : self.helpConfigure,
                        "cancel" : self.helpCancel,
                        "get-detection-enable" : self.helpGetDetectionEnable,
                        "get" : self.helpGet,
                        "get-sflow-sampling-status" : self.helpGetSFlowSamplingStatus,
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

    def handleUnimplemented(self, args):
        usage = True
        ret = None
        return usage, ret

    def helpUnimplemented(self, name):
        print name
        print 
        print "The {} command is currently not supported and may become deprecated".format(name) 

    def helpDetectionEnable(self, name):
        print name, "[args]"
        print
        print "args:"
        print
        print "   enable:[true|false]"

    def handleDetectionEnable(self, args):
        usage = False
        usage, asic, host, port = self.getASICHostPort(args)
        usage, self._timeout = self.getTimeout(args)
        if not usage:
            x = BlackHoleDetectionEnable(host, port)
            x.setASIC(asic) 
            for arg in args:
                if "enable:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        if v[1] == "true":
                            x.setEnable(True)
                        elif v[1] == "false":
                            x.setEnable(False)
                        else:
                            print "invalid enable argument"
                            self.helpDetectionEnable("detection-enable")
                    else:
                        print "invalid enable: bad argument count"
            status = x.send(timeout=self._timeout)
            if status != 200:
                print "failure: {}".format(status)

        ret = None
        return usage, ret

    def handleConfigure(self, args):
        usage = False
        usage, asic, host, port = self.getASICHostPort(args)
        if not usage:
            x = ConfigurePacketTraceDropReason(host, port)
            for arg in args:
                if "sampling-method:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        x.setSamplingMethod(v[1])
                    else:
                        print "invalid sampling-method: bad argument count"
                        usage = True
                elif "port-list:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        v2 = v[1].split(",")
                        port_list = []
                        for y in v2:
                            port_list.append(y)
                        x.setPortList(port_list)
                    else:
                        print "invalid port-list: bad argument count"
                        usage = True
                elif "water-mark:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        x.setWaterMark(int(v[1]))
                    else:
                        print "invalid water-mark: bad argument count"
                        usage = True
                elif "sample-periodicity:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        x.setSamplePeriodicity(int(v[1]))
                    else:
                        print "invalid sample-periodicity: bad argument count"
                        usage = True
                elif "sample-count:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        x.setSampleCount(int(v[1]))
                    else:
                        print "invalid sample-count: bad argument count"
                        usage = True
                elif "dst-ip:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        x.setDestinationIP(v[1])
                    else:
                        print "invalid dst-ip: bad argument count"
                        usage = True
                elif "src-udp-port:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        x.setSourceUDPPort(int(v[1]))
                    else:
                        print "invalid src-udp-port: bad argument count"
                        usage = True
                elif "dst-udp-port:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        x.setDestinationUDPPort(int(v[1]))
                    else:
                        print "invalid dst-udp-port: bad argument count"
                        usage = True
                elif "mirror-port:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        x.setMirrorPort(int(v[1]))
                    else:
                        print "invalid mirror-port: bad argument count"
                        usage = True
                elif "sample-pool-size:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        x.setSamplePoolSize(int(v[1]))
                    else:
                        print "invalid sample-pool-size: bad argument count"
                        usage = True
                elif "vlan-id:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        x.setVLANId(int(v[1]))
                    else:
                        print "invalid vlan-id: bad argument count"
                        usage = True

            x.setASIC(asic)
            status = x.send(self._timeout)
            if status != 200:
                print "failure: {}".format(status)

        ret = None
        return usage, ret

    def helpConfigure(self, name):
        print name, "[args]"
        print
        print "args:"
        print
        print "   sampling-method:[agent|sflow]"
        print "   water-mark:integer"
        print "   port-list:port[,port][,port]...[,port]"
        print "   sample-periodicity:[integer]"
        print "   sample-count:n"
        print "   vlan-id:id"
        print "   dst-ip:ipv4"
        print "   src-udp-port:integer"
        print "   dst-udp-port:integer"
        print "   mirror-port:integer"
        print "   sample-pool-size:integer"

    def handleCancel(self, args):
        usage = False
        usage, asic, host, port = self.getASICHostPort(args)
        if not usage:
            x = CancelPacketTraceProfile(host, port)
            x.setASIC(asic)
            status = x.send(self._timeout)
            if status != 200:
                print "failure: {}".format(status)

        ret = None
        return usage, ret

    def helpCancel(self, name):
        print name

    def handleGetDetectionEnable(self, args):
        usage = False
        usage, asic, host, port = self.getASICHostPort(args)
        if not usage:
            x = GetBlackHoleDetectionEnable(host, port)
            x.setASIC(asic)
            status = x.send(self._timeout)
            if status == 200:
                ret = json.dumps(x.getJSON())
                print ret
            else:
                print "failure: {}".format(status)

        ret = None
        return usage, ret

    def helpGetDetectionEnable(self, name):
        print name

    def handleGet(self, args):
        usage = False
        usage, asic, host, port = self.getASICHostPort(args)
        if not usage:
            x = GetBlackHole(host, port)
            x.setASIC(asic)
            status = x.send(self._timeout)
            if status == 200:
                ret = json.dumps(x.getJSON())
                print ret
            else:
                print "failure: {}".format(status)

        ret = None
        return usage, ret

    def helpGet(self, name):
        print name

    def handleGetSFlowSamplingStatus(self, args):
        usage = False
        usage, asic, host, port = self.getASICHostPort(args)
        if not usage:
            x = GetSFlowSamplingStatus(host, port)
            for arg in args:
                if "port-list:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        v2 = v[1].split(",")
                        port_list = []
                        for y in v2:
                            port_list.append(y)
                        x.setPortList(port_list)
                    else:
                        print "invalid port-list: bad argument count"
                        usage = True

            x.setASIC(asic)
            status = x.send(self._timeout)
            if status == 200:
                ret = json.dumps(x.getJSON())
                print ret
            else:
                print "failure: {}".format(status)

        ret = None
        return usage, ret

    def helpGetSFlowSamplingStatus(self, name):
        print name, "[args]"
        print
        print "args:"
        print
        print "   port-list:port[,port][,port]...[,port]"

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
    x = BHDCommand()
    usage, ret = x.handle(argv)       
    if usage:
        x.usage()

if __name__ == "__main__":
    main(sys.argv[1:])
