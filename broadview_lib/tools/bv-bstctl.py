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

from broadview_lib.config.bst import *
from broadview_lib.config.broadviewconfig import BroadViewBSTSwitches
import sys
import unittest

class BSTConfigCommand():
    def __init__(self):
        self.__cmds = { 
                        "cfg-feature" : self.handleCfgFeature,
                        "cfg-tracking" : self.handleCfgTracking,
                        "cfg-thresholds" : self.handleCfgThresholds,
                        "clr-statistics" : self.handleClrStatistics,
                        "clr-thresholds" : self.handleClrThresholds,
                        "get-feature" : self.handleGetFeature,
                        "get-tracking" : self.handleGetTracking,
                        "get-thresholds" : self.handleGetThresholds,
                        "get-report" : self.handleGetReport,
                        "help": self.handleHelp,
                      }

        self.__help = { 
                        "cfg-feature" : self.helpCfgFeature,
                        "cfg-tracking" : self.helpCfgTracking,
                        "cfg-thresholds" : self.helpCfgThresholds,
                        "clr-statistics" : self.helpClrStatistics,
                        "clr-thresholds" : self.helpClrThresholds,
                        "get-feature" : self.helpGetFeature,
                        "get-tracking" : self.helpGetTracking,
                        "get-thresholds" : self.helpGetThresholds,
                        "get-report" : self.helpGetReport,
                      }

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
        print "usage: %s cmd host:ipv4 [port:port] [asic-id:id] [args]" % (sys.argv[0])
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

    def handleCfgFeature(self, args):
        usage = False
        usage, asic, host, port = self.getASICHostPort(args)
        if not usage:
            x = ConfigureBSTFeature(host, port)
            x.setASIC(asic) 
            x.setEnable("enable" in args)
            x.setSendAsyncReports("send_async_reports" in args)
            for arg in args:
                if "collection_interval:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        x.setCollectionInterval(int(v[1]))
                    else:
                        print "invalid set-collection-interval argument"
                        usage = True
                elif "trigger_rate_limit:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        x.setTriggerRateLimit(int(v[1]))
                    else:
                        print "invalid trigger_rate_limit argument"
                        usage = True
                elif "trigger_rate_limit_interval:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        x.setTriggerRateLimitInterval(int(v[1]))
                    else:
                        print "invalid trigger_rate_limit_interval argument"
                        usage = True

            x.setStatInPercentage("stat_in_percentage" in args)
            x.setStatUnitsInCells("stat_units_in_cells" in args)
            x.setSendSnapshotOnTrigger("send_snapshot_on_trigger" in args)
            x.setAsyncFullReports("async_full_reports" in args)
            status = x.send()
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
        print "   send_async_reports"
        print "   collection_interval:val" 
        print "   stat_in_percentage"
        print "   stat_units_in_cells"
        print "   trigger_rate_limit:val"
        print "   trigger_rate_limit_interval:val"
        print "   send_snapshot_on_trigger"
        print "   async_full_reports"

    def handleCfgTracking(self, args):
        usage = False
        usage, asic, host, port = self.getASICHostPort(args)
        if not usage:
            x = ConfigureBSTTracking(host, port)
            x.setASIC(asic)
            x.setTrackPeakStats("track_peak_stats" in args)
            x.setTrackIngressPortPriorityGroup("track_ingress_port_priority_group" in args)
            x.setTrackIngressPortServicePool("track_ingress_port_service_pool" in args)
            x.setTrackIngressServicePool("track_ingress_service_pool" in args)
            x.setTrackEgressPortServicePool("track_egress_port_service_pool" in args)
            x.setTrackEgressServicePool("track_egress_service_pool" in args)
            x.setTrackEgressUcQueue("track_egress_uc_queue" in args)
            x.setTrackEgressUcQueueGroup("track_egress_uc_queue_group" in args)
            x.setTrackEgressMcQueue("track_egress_mc_queue" in args)
            x.setTrackEgressCPUQueue("track_egress_cpu_queue" in args)
            x.setTrackEgressRQEQueue("track_egress_rqe_queue" in args)
            x.setTrackDevice("track_device" in args)
            status = x.send()
            if status != 200:
                print "failure: %d" % (status)

        ret = None
        return usage, ret

    def helpCfgTracking(self, name):
        print name, "[args]"
        print
        print "args:"
        print
        print "   track_peak_stats"
        print "   track_ingress_port_priority_group"
        print "   track_ingress_port_service_pool"
        print "   track_ingress_service_pool"
        print "   track_egress_port_service_pool"
        print "   track_egress_service_pool"
        print "   track_egress_uc_queue"
        print "   track_egress_uc_queue_group"
        print "   track_egress_mc_queue"
        print "   track_egress_cpu_queue"
        print "   track_egress_rqe_queue"
        print "   track_device"

    def handleCfgThresholds(self, args):
        usage = False
        usage, asic, host, port = self.getASICHostPort(args)
        if not usage:
            for arg in args:
                if "device:" in arg:
                    v = arg.split(":")
                    if len(v) == 2:
                        x = ConfigureDeviceThreshold(host, port, int(v[1]))
                        x.setASIC(asic)
                        status = x.send()
                        if status != 200:
                            print "failure: %d" % (status)
                    else:
                        print "invalid device: bad argument count"
                        usage = True
                elif "egress-cpu-queue:" in arg:
                    v = arg.split(":")
                    if len(v) == 3:
                        x = ConfigureEgressCpuQueueThreshold(host, port, 
                                                     int(v[1]),
                                                     int(v[2]))
                        x.setASIC(asic)
                        status = x.send()
                        if status != 200:
                            print "failure: %d" % (status)
                    else:
                        print "invalid egress-cpu-queue: bad argument count"
                        usage = True
                elif "egress-rqe-queue:" in arg:
                    v = arg.split(":")
                    if len(v) == 3:
                        x = ConfigureEgressRqeQueueThreshold(host, port, 
                                                     int(v[1]),
                                                     int(v[2]))
                        x.setASIC(asic)
                        status = x.send()
                        if status != 200:
                            print "failure: %d" % (status)
                    else:
                        print "invalid egress-rqe-queue: bad argument count"
                        usage = True
                elif "egress-port-service-pool:" in arg:
                    v = arg.split(":")
                    if len(v) == 7:
                        x = ConfigureEgressPortServicePoolThreshold(host, port, 
                                                     v[1],
                                                     int(v[2]),
                                                     int(v[3]),
                                                     int(v[4]),
                                                     int(v[5]),
                                                     int(v[6]))
                        x.setASIC(asic)
                        status = x.send()
                        if status != 200:
                            print "failure: %d" % (status)
                    else:
                        print "invalid egress-port-service-pool: bad argument count"
                        usage = True
                elif "egress-service-pool:" in arg:
                    v = arg.split(":")
                    if len(v) == 5:
                        x = ConfigureEgressServicePoolThreshold(host, port, 
                                                     int(v[1]),
                                                     int(v[2]),
                                                     int(v[3]),
                                                     int(v[4]))
                        x.setASIC(asic)
                        status = x.send()
                        if status != 200:
                            print "failure: %d" % (status)
                    else:
                        print "invalid egress-service-pool: bad argument count"
                        usage = True
                elif "egress-uc-queue:" in arg:
                    v = arg.split(":")
                    if len(v) == 3:
                        x = ConfigureEgressUcQueueThreshold(host, port, 
                                                     int(v[1]),
                                                     int(v[2]))
                        x.setASIC(asic)
                        status = x.send()
                        if status != 200:
                            print "failure: %d" % (status)
                    else:
                        print "invalid egress-uc-queue: bad argument count"
                        usage = True
                elif "egress-uc-queue-group:" in arg:
                    v = arg.split(":")
                    if len(v) == 3:
                        x = ConfigureEgressUcQueueGroupThreshold(host, port, 
                                                     int(v[1]),
                                                     int(v[2]))
                        x.setASIC(asic)
                        status = x.send()
                        if status != 200:
                            print "failure: %d" % (status)
                    else:
                        print "invalid egress-uc-queue-group: bad argument count"
                        usage = True
                elif "egress-mc-queue:" in arg:
                    v = arg.split(":")
                    if len(v) == 4:
                        x = ConfigureEgressMcQueueThreshold(host, port, 
                                                     int(v[1]),
                                                     int(v[2]),
                                                     int(v[3]))
                        x.setASIC(asic)
                        status = x.send()
                        if status != 200:
                            print "failure: %d" % (status)
                    else:
                        print "invalid egress-mc-queue-group: bad argument count"
                        usage = True
                elif "ingress-port-priority-group:" in arg:
                    v = arg.split(":")
                    if len(v) == 5:
                        x = ConfigureIngressPortPriorityGroupThreshold(host, port,
                                                     v[1],
                                                     int(v[2]),
                                                     int(v[3]),
                                                     int(v[4]))
                        x.setASIC(asic)
                        status = x.send()
                        if status != 200:
                            print "failure: %d" % (status)
                    else:
                        print "invalid ingress-port-priority-group: bad argument count"
                        usage = True
                elif "ingress-port-service-pool:" in arg:
                    v = arg.split(":")
                    if len(v) == 4:
                        x = ConfigureIngressPortServicePoolThreshold(host, port,
                                                     v[1],
                                                     int(v[2]),
                                                     int(v[3]))
                        x.setASIC(asic)
                        status = x.send()
                        if status != 200:
                            print "failure: %d" % (status)
                    else:
                        print "invalid ingress-port-service-pool: bad argument count"
                        usage = True
                elif "ingress-service-pool:" in arg:
                    v = arg.split(":")
                    if len(v) == 3:
                        x = ConfigureIngressServicePoolThreshold(host, port,
                                                     int(v[1]),
                                                     int(v[2]))
                        x.setASIC(asic)
                        status = x.send()
                        if status != 200:
                            print "failure: %d" % (status)
                    else:
                        print "invalid ingress-service-pool: bad argument count"
                        usage = True

        ret = None
        return usage, ret

    def helpCfgThresholds(self, name):
        print name, "[args]"
        print "Any number of the following args can be used in any combination."
        print
        print "Format of each argument is realm:arg1:arg2:...:argn"
        print
        print "args:"
        print
        print "   device:threshold"
        print "   egress-cpu-queue:queue:cpu-threshold"
        print "   egress-rqe-queue:queue:rqe-threshold"
        print "   egress-port-service-pool:port:service-pool:uc-share-threshold:um-share-threshold:mc-share-threshold:mc-share-queue-entries-threshold"
        print " egress-service-pool:service-pool:um-share-threshold:mc-share-threshold:mc-share-queue-entries-threshold"
        print "   egress-uc-queue:queue:uc-threshold"
        print "   egress-uc-queue-group:queue-group:uc-threshold"
        print "   egress-mc-queue:queue:mc-queue-entries-threshold"
        print "   ingress-port-priority-group:port:priority-group:um-share-threshold:um-headroom-threshold"
        print "   ingress-port-service-pool:port:service-pool:um-share-threshold"
        print "   ingress-service-pool:service-pool:um-share-threshold"

    def handleClrStatistics(self, args):
        usage = False
        usage, asic, host, port = self.getASICHostPort(args)
        if not usage:
            x = ClearBSTStatistics(host, port)
            x.setASIC(asic)
            status = x.send()
            if status != 200:
                print "failure: %d" % (status)

        ret = None
        return usage, ret

    def helpClrStatistics(self, name):
        print name

    def handleClrThresholds(self, args):
        usage = False
        usage, asic, host, port = self.getASICHostPort(args)
        if not usage:
            x = ClearBSTThresholds(host, port)
            x.setASIC(asic)
            status = x.send()
            if status != 200:
                print "failure: %d" % (status)

        ret = None
        return usage, ret

    def helpClrThresholds(self, name):
        print name

    def handleGetFeature(self, args):
        usage = False
        ret = None
        usage, asic, host, port = self.getASICHostPort(args)
        if not usage:
            x = GetBSTFeature(host, port)
            x.setASIC(asic)
            status = x.send()
            if status == 200:
                ret = x.getJSON()
                print ret
            else:
                print "failure: %d" % (status)

        return usage, ret

    def helpGetFeature(self, name):
        print name

    def handleGetTracking(self, args):
        usage = False
        ret = None
        usage, asic, host, port = self.getASICHostPort(args)
        if not usage:
            x = GetBSTTracking(host, port)
            x.setASIC(asic)
            status = x.send()
            if status == 200:
                ret = x.getJSON()
                print ret
            else:
                print "failure: %d" % (status)
        return usage, ret

    def helpGetTracking(self, name):
        print name

    def handleGetThresholds(self, args):
        usage = False
        ret = None
        usage, asic, host, port = self.getASICHostPort(args)
        if not usage:
            x = GetBSTThresholds(host, port)
            x.setASIC(asic)
            x.setIncludeIngressPortPriorityGroup("include_ingress_port_priority_group" in args)
            x.setIncludeIngressPortServicePool("include_ingress_port_service_pool" in args)
            x.setIncludeIngressServicePool("include_ingress_service_pool" in args)
            x.setIncludeEgressPortServicePool("include_egress_port_service_pool" in args)
            x.setIncludeEgressServicePool("include_egress_service_pool" in args)
            x.setIncludeEgressUcQueue("include_egress_uc_queue" in args)
            x.setIncludeEgressUcQueueGroup("include_egress_uc_queue_group" in args)
            x.setIncludeEgressMcQueue("include_egress_mc_queue" in args)
            x.setIncludeEgressCPUQueue("include_egress_cpu_queue" in args)
            x.setIncludeEgressRQEQueue("include_egress_rqe_queue" in args)
            x.setIncludeDevice("include_device" in args)

            status, rep = x.send()
            if status == 200:
                ret = x.getJSON()
                print ret
            else:
                print "failure: %d" % (status)

        return usage, ret

    def helpGetThresholds(self, name):
        print name, "[args]"
        print
        print "args:"
        print
        print "   include_ingress_port_priority_group"
        print "   include_ingress_port_service_pool"
        print "   include_ingress_service_pool"
        print "   include_egress_port_service_pool"
        print "   include_egress_service_pool"
        print "   include_egress_uc_queue"
        print "   include_egress_uc_queue_group"
        print "   include_egress_mc_queue"
        print "   include_egress_cpu_queue"
        print "   include_egress_rqe_queue"
        print "   include_device"

    def handleGetReport(self, args):
        usage = False
        ret = None
        usage, asic, host, port = self.getASICHostPort(args)
        if not usage:

            x = GetBSTReport(host, port)
            x.setASIC(asic)
            x.setIncludeIngressPortPriorityGroup("include_ingress_port_priority_group" in args)
            x.setIncludeIngressPortServicePool("include_ingress_port_service_pool" in args)
            x.setIncludeIngressServicePool("include_ingress_service_pool" in args)
            x.setIncludeEgressPortServicePool("include_egress_port_service_pool" in args)
            x.setIncludeEgressServicePool("include_egress_service_pool" in args)
            x.setIncludeEgressUcQueue("include_egress_uc_queue" in args)
            x.setIncludeEgressUcQueueGroup("include_egress_uc_queue_group" in args)
            x.setIncludeEgressMcQueue("include_egress_mc_queue" in args)
            x.setIncludeEgressCPUQueue("include_egress_cpu_queue" in args)
            x.setIncludeEgressRQEQueue("include_egress_rqe_queue" in args)
            x.setIncludeDevice("include_device" in args)

            status, rep = x.send()
            if status == 200:
                ret = x.getJSON()
                print ret
            else:
                print "failure: %d" % (status)

        return usage, ret

    def helpGetReport(self, name):
        print name, "[args]"
        print
        print "args:"
        print
        print "   include_ingress_port_priority_group"
        print "   include_ingress_port_service_pool"
        print "   include_ingress_service_pool"
        print "   include_egress_port_service_pool"
        print "   include_egress_service_pool"
        print "   include_egress_uc_queue"
        print "   include_egress_uc_queue_group"
        print "   include_egress_mc_queue"
        print "   include_egress_cpu_queue"
        print "   include_egress_rqe_queue"
        print "   include_device"

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
    x = BSTConfigCommand()
    usage, ret = x.handle(argv)       
    if usage:
        x.usage()

if __name__ == "__main__":
    main(sys.argv[1:])
