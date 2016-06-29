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

from broadview_lib.config.pt import *
import sys
import json

class PTCommand():
    def __init__(self):
        self._timeout = 30
        self.__cmds = { 
                        "cfg-feature" : self.handleCfgFeature,
                        "cfg-drop-reason" : self.handleUnimplemented,
                        "cancel-profile" : self.handleCancelProfile,
                        "cancel-lag-resolution" : self.handleCancelLAGResolution,
                        "cancel-ecmp-resolution" : self.handleCancelECMPResolution,
                        "cancel-send-drop-packet" : self.handleUnimplemented,
                        "cancel-drop-counter-report" : self.handleUnimplemented,
                        "get-feature" : self.handleGetFeature,
                        "get-lag-resolution" : self.handleGetLAGResolution,
                        "get-ecmp-resolution" : self.handleGetECMPResolution,
                        "get-profile" : self.handleGetProfile,
                        "get-drop-reason" : self.handleUnimplemented,
                        "get-drop-counter-report" : self.handleUnimplemented,
                        "get-supported-drop-reasons" : self.handleUnimplemented,
                        "help": self.handleHelp,
                      }

        self.__help = { 
                        "cfg-feature" : self.helpCfgFeature,
                        "cfg-drop-reason" : self.helpUnimplemented,
                        "cancel-profile" : self.helpCancelProfile,
                        "cancel-lag-resolution" : self.helpCancelLAGResolution,
                        "cancel-ecmp-resolution" : self.helpCancelECMPResolution,
                        "cancel-send-drop-packet" : self.helpUnimplemented,
                        "cancel-drop-counter-report" : self.helpUnimplemented,
                        "get-feature" : self.helpGetFeature,
                        "get-lag-resolution" : self.helpGetLAGResolution,
                        "get-ecmp-resolution" : self.helpGetECMPResolution,
                        "get-profile" : self.helpGetProfile,
                        "get-drop-reason" : self.helpUnimplemented,
                        "get-drop-counter-report" : self.helpUnimplemented,
                        "get-supported-drop-reasons" : self.helpUnimplemented,
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

    def handleCfgFeature(self, args):
        usage = False
        usage, asic, host, port = self.getASICHostPort(args)
        usage, self._timeout = self.getTimeout(args)
        if not usage:
            x = ConfigurePacketTraceFeature(host, port)
            x.setASIC(asic) 
            x.setEnable("enable" in args)
            status = x.send(timeout=self._timeout)
            if status != 200:
                print "failure: %d" % (status)

        ret = None
        return usage, ret

    def helpCfgFeature(self, name):
        print name, "[args]"
        print
        print "args:"
        print
        print "   enable"

    def handleCfgDropReason(self, args):
        usage = False
        usage, asic, host, port = self.getASICHostPort(args)
        if not usage:
            x = ConfigurePacketTraceDropReason(host, port)
            for arg in args:
                if "reason:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        v2 = v[1].split(",")
                        reason = []
                        for y in v2:
                            reason.append(x)
                        x.setReason(reason)
                    else:
                        print "invalid reason: bad argument count"
                        usage = True
                elif "port-list:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        v2 = v[1].split(",")
                        port_list = []
                        for y in v2:
                            port_list.append(x)
                        x.setPortList(port_list)
                    else:
                        print "invalid port-list: bad argument count"
                        usage = True
                elif "send-dropped-packet:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        x.setSendDroppedPacket(v[1] == 1)
                    else:
                        print "invalid send-dropped-packet: bad argument count"
                        usage = True
                elif "trace-profile:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        x.setTraceProfile(int(v[1]) == 1)
                    else:
                        print "invalid trace-profile: bad argument count"
                        usage = True
                elif "packet-count:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        x.setPacketCount(int(v[1]))
                    else:
                        print "invalid packet-count: bad argument count"
                        usage = True
                elif "packet-threshold:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        x.setPacketThreshold(int(v[1]))
                    else:
                        print "invalid packet-threshold: bad argument count"
                        usage = True

            x.setASIC(asic)
            status = x.send(self._timeout)
            if status != 200:
                print "failure: %d" % (status)

        ret = None
        return usage, ret

    def helpCfgDropReason(self, name):
        print name, "[args]"
        print
        print "args:"
        print
        print "   reason:reason[,reason][,reason]...[,reason]"
        print "   port-list:port[,port][,port]...[,port]"
        print "   send-dropped-packet:[0|1]"
        print "   trace-profile:[0|1]"
        print "   packet-count:n"
        print "   packet-threshold:n"

    def handleCancelProfile(self, args):
        usage = False
        usage, asic, host, port = self.getASICHostPort(args)
        if not usage:
            x = CancelPacketTraceProfile(host, port)
            x.setASIC(asic)
            status = x.send(self._timeout)
            if status != 200:
                print "failure: %d" % (status)

        ret = None
        return usage, ret

    def helpCancelProfile(self, name):
        print name

    def handleCancelLAGResolution(self, args):
        usage = False
        usage, asic, host, port = self.getASICHostPort(args)
        if not usage:
            x = CancelPacketTraceLAGResolution(host, port)
            x.setASIC(asic)
            status = x.send(self._timeout)
            if status != 200:
                print "failure: %d" % (status)

        ret = None
        return usage, ret

    def helpCancelLAGResolution(self, name):
        print name

    def handleCancelECMPResolution(self, args):
        usage = False
        usage, asic, host, port = self.getASICHostPort(args)
        if not usage:
            x = CancelPacketTraceECMPResolution(host, port)
            x.setASIC(asic)
            status = x.send(self._timeout)
            if status != 200:
                print "failure: %d" % (status)

        ret = None
        return usage, ret

    def helpCancelECMPResolution(self, name):
        print name

    def handleCancelSendDropPacket(self, args):
        usage = False
        usage, asic, host, port = self.getASICHostPort(args)
        if not usage:
            x = CancelPacketTraceSendDropPacket(host, port)
            for arg in args:
                if "drop-reason:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        v2 = v[1].split(",")
                        reason = []
                        for y in v2:
                            reason.append(x)
                        x.setDropReason(reason)
                    else:
                        print "invalid drop-reason: bad argument count"
                        usage = True
                elif "port-list:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        v2 = v[1].split(",")
                        port_list = []
                        for y in v2:
                            port_list.append(x)
                        x.setPortList(port_list)
                    else:
                        print "invalid port-list: bad argument count"
                        usage = True

            x.setASIC(asic)
            status = x.send(self._timeout)
            if status != 200:
                print "failure: %d" % (status)

        ret = None
        return usage, ret

    def helpCancelSendDropPacket(self, name):
        print name, "[args]"
        print
        print "args:"
        print
        print "   drop-reason:reason[,reason][,reason]...[,reason]"
        print "   port-list:port[,port][,port]...[,port]"

    def handleCancelDropCounterReport(self, args):
        usage = False
        usage, asic, host, port = self.getASICHostPort(args)
        if not usage:
            x = CancelPacketTraceDropCounterReport(host, port)
            for arg in args:
                if "drop-reason:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        v2 = v[1].split(",")
                        reason = []
                        for y in v2:
                            reason.append(x)
                        x.setDropReason(reason)
                    else:
                        print "invalid drop-reason: bad argument count"
                        usage = True
                elif "port-list:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        v2 = v[1].split(",")
                        port_list = []
                        for y in v2:
                            port_list.append(x)
                        x.setPortList(port_list)
                    else:
                        print "invalid port-list: bad argument count"
                        usage = True

            x.setASIC(asic)
            status = x.send(self._timeout)
            if status != 200:
                print "failure: %d" % (status)

        ret = None
        return usage, ret

    def helpCancelDropCounterReport(self, name):
        print name, "[args]"
        print
        print "args:"
        print
        print "   drop-reason:reason[,reason][,reason]...[,reason]"
        print "   port-list:port[,port][,port]...[,port]"

    def handleGetFeature(self, args):
        usage = False
        usage, asic, host, port = self.getASICHostPort(args)
        if not usage:
            x = GetPacketTraceFeature(host, port)
            x.setASIC(asic)
            status = x.send(self._timeout)
            if status == 200:
                ret = json.dumps(x.getJSON())
                print ret
            else:
                print "failure: %d" % (status)

        ret = None
        return usage, ret

    def helpGetFeature(self, name):
        print name

    def handleGetLAGResolution(self, args):
        usage = False
        usage, asic, host, port = self.getASICHostPort(args)
        if not usage:
            x = GetPacketTraceLAGResolution(host, port)
            for arg in args:
                if "drop-packet:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        x.setDropPacket(int(v[1]) == 1)
                    else:
                        print "invalid drop-packet: bad argument count"
                        usage = True
                elif "packet:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        x.setPacket(v[1])
                    else:
                        print "invalid packet: bad argument count"
                        usage = True
                elif "port-list:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        v2 = v[1].split(",")
                        port_list = []
                        for y in v2:
                            port_list.append(x)
                        x.setPortList(port_list)
                    else:
                        print "invalid port-list: bad argument count"
                        usage = True
                elif "collection-interval:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        x.setCollectionInterval(int(v[1]))
                    else:
                        print "invalid collection-interval: bad argument count"
                        usage = True

            x.setASIC(asic)
            status = x.send(self._timeout)
            if status == 200:
                ret = json.dumps(x.getJSON())
                print ret
            else:
                print "failure: %d" % (status)

        ret = None
        return usage, ret

    def helpGetLAGResolution(self, name):
        print name, "[args]"
        print
        print "args:"
        print
        print "   packet: packet"
        print "   port-list:port[,port][,port]...[,port]"
        print "   collection-interval: interval"
        print "   drop-packet: [0|1]"

    def handleGetECMPResolution(self, args):
        usage = False
        usage, asic, host, port = self.getASICHostPort(args)
        if not usage:
            x = GetPacketTraceECMPResolution(host, port)
            for arg in args:
                if "drop-packet:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        x.setDropPacket(int(v[1]) == 1)
                    else:
                        print "invalid drop-packet: bad argument count"
                        usage = True
                elif "packet:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        x.setPacket(v[1])
                    else:
                        print "invalid packet: bad argument count"
                        usage = True
                elif "port-list:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        v2 = v[1].split(",")
                        port_list = []
                        for y in v2:
                            port_list.append(x)
                        x.setPortList(port_list)
                    else:
                        print "invalid port-list: bad argument count"
                        usage = True
                elif "collection-interval:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        x.setCollectionInterval(int(v[1]))
                    else:
                        print "invalid collection-interval: bad argument count"
                        usage = True

            x.setASIC(asic)
            status = x.send(self._timeout)
            if status == 200:
                ret = json.dumps(x.getJSON())
                print ret
            else:
                print "failure: %d" % (status)

        ret = None
        return usage, ret

    def helpGetECMPResolution(self, name):
        print name, "[args]"
        print
        print "args:"
        print
        print "   packet: packet"
        print "   port-list:port[,port][,port]...[,port]"
        print "   collection-interval: interval"
        print "   drop-packet: [0|1]"

    def handleGetProfile(self, args):
        usage = False
        usage, asic, host, port = self.getASICHostPort(args)
        if not usage:
            x = GetPacketTraceProfile(host, port)
            for arg in args:
                v = arg.split(":")
                if "drop-packet:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        x.setDropPacket(int(v[1]) == 1)
                    else:
                        print "invalid drop-packet: bad argument count"
                        usage = True
                elif "packet:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        x.setPacket(v[1])
                    else:
                        print "invalid packet: bad argument count"
                        usage = True
                elif "port-list:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        v2 = v[1].split(",")
                        port_list = []
                        for y in v2:
                            port_list.append(x)
                        x.setPortList(port_list)
                    else:
                        print "invalid port-list: bad argument count"
                        usage = True
                elif "collection-interval:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        x.setCollectionInterval(int(v[1]))
                    else:
                        print "invalid collection-interval: bad argument count"
                        usage = True

            x.setASIC(asic)
            status = x.send(self._timeout)
            if status == 200:
                ret = json.dumps(x.getJSON())
                print ret
            else:
                print "failure: %d" % (status)

        ret = None
        return usage, ret

    def helpGetProfile(self, name):
        print name, "[args]"
        print
        print "args:"
        print
        print "   packet: packet"
        print "   port-list:port[,port][,port]...[,port]"
        print "   collection-interval: interval"
        print "   drop-packet: [0|1]"

    def handleGetDropReason(self, args):
        usage = False
        usage, asic, host, port = self.getASICHostPort(args)
        if not usage:
            x = GetPacketTraceDropReason(host, port)
            x.setASIC(asic)
            status = x.send(self._timeout)
            if status == 200:
                ret = json.dumps(x.getJSON())
                print ret
            else:
                print "failure: %d" % (status)

        ret = None
        return usage, ret

    def helpGetDropReason(self, name):
        print name

    def handleGetDropCounterReport(self, args):
        usage = False
        usage, asic, host, port = self.getASICHostPort(args)
        if not usage:
            x = GetPacketTraceDropCounterReport(host, port)
            for arg in args:
                if "drop-reason:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        v2 = v[1].split(",")
                        reason = []
                        for y in v2:
                            reason.append(x)
                        x.setDropReason(reason)
                    else:
                        print "invalid drop-reason: bad argument count"
                        usage = True
                elif "port-list:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        v2 = v[1].split(",")
                        port_list = []
                        for y in v2:
                            port_list.append(x)
                        x.setPortList(port_list)
                    else:
                        print "invalid port-list: bad argument count"
                        usage = True
                elif "collection-interval:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        x.setCollectionInterval(int(v[1]))
                    else:
                        print "invalid collection-interval: bad argument count"

            x.setASIC(asic)
            status = x.send(self._timeout)
            if status == 200:
                ret = json.dumps(x.getJSON())
                print ret
            else:
                print "failure: %d" % (status)

        ret = None
        return usage, ret

    def helpGetDropCounterReport(self, name):
        print name, "[args]"
        print
        print "args:"
        print
        print "   drop-reason:reason[,reason][,reason]...[,reason]"
        print "   port-list:port[,port][,port]...[,port]"
        print "   collection-interval:interval"

    def handleGetSupportedDropReasons(self, args):
        usage = False
        usage, asic, host, port = self.getASICHostPort(args)
        if not usage:
            x = GetPacketTraceSupportedDropReasons(host, port)
            x.setASIC(asic)
            status = x.send(self._timeout)
            if status == 200:
                ret = json.dumps(x.getJSON())
                print ret
            else:
                print "failure: %d" % (status)

        ret = None
        return usage, ret

    def helpGetSupportedDropReasons(self, name):
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
    x = PTCommand()
    usage, ret = x.handle(argv)       
    if usage:
        x.usage()

if __name__ == "__main__":
    main(sys.argv[1:])
