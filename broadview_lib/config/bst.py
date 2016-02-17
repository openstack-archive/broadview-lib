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

from agentapi import AgentAPI
from broadview_lib.bst.bst_parser import BSTParser
from broadview_lib.config.broadviewconfig import BroadViewBSTSwitches
import unittest

class ConfigureBSTFeature(AgentAPI):
    def __init__(self, host, port):
        super(ConfigureBSTFeature, self).__init__()
        self.setFeature("bst")
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.__bst_enable = False
        self.__send_async_reports = False
        self.__collection_interval = 60
        self.__stat_in_percentage = False
        self.__stat_units_in_cells = False
        self.__trigger_rate_limit = 1
        self.__trigger_rate_limit_interval = 1
        self.__send_snapshot_on_trigger = True
        self.__async_full_reports = False
        self.__asic_id = "1"

    def setEnable(self, val):
        self.__bst_enable = val

    def setSendAsyncReports(self, val):
        self.__send_async_reports = val

    def setCollectionInterval(self, val):
        self.__collection_interval = val

    def setStatInPercentage(self, val):
        self.__stat_in_percentage = val

    def setStatUnitsInCells(self, val):
        self.__stat_units_in_cells = val

    def setTriggerRateLimit(self, val):
        self.__trigger_rate_limit = val

    def setTriggerRateLimitInterval(self, val):
        self.__trigger_rate_limit_interval = val

    def setSendSnapshotOnTrigger(self, val):
        self.__send_snapshot_on_trigger = val

    def setAsyncFullReports(self, val):
        self.__async_full_reports = val

    def setASIC(self, val):
        self.__asic_id = val

    def send(self):
        status, json = self._send(self.toDict())
        return status


    def toDict(self):
        ret = {}
        params = {}
        params["bst-enable"] = 1 if self.__bst_enable else 0 
        params["send-async-reports"] = 1 if self.__send_async_reports else 0
        params["collection-interval"] = self.__collection_interval
        params["stat-in-percentage"] = 1 if self.__stat_in_percentage else 0
        params["stat-units-in-cells"] = 1 if self.__stat_units_in_cells else 0
        params["trigger-rate-limit"] = self.__trigger_rate_limit
        params["trigger-rate-limit-interval"] = self.__trigger_rate_limit_interval 
        params["send-snapshot-on-trigger"] = 1 if self.__send_snapshot_on_trigger else 0
        params["async-full-reports"] = 1 if self.__async_full_reports else 0
        ret["asic-id"] = self.__asic_id
        ret["params"] = params
        ret["method"] = "configure-bst-feature"
        return ret

class ConfigureBSTTracking(AgentAPI):
    def __init__(self, host, port):
        super(ConfigureBSTTracking, self).__init__()
        self.setFeature("bst")
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.__track_peak_stats = False
        self.__track_ingress_port_priority_group = False
        self.__track_ingress_port_service_pool = False
        self.__track_ingress_service_pool = False
        self.__track_egress_port_service_pool = False
        self.__track_egress_service_pool = False
        self.__track_egress_uc_queue = False
        self.__track_egress_uc_queue_group = False
        self.__track_egress_mc_queue = False
        self.__track_egress_cpu_queue = False
        self.__track_egress_rqe_queue = False
        self.__track_device = False
        self.__asic_id = "1"

    def setTrackPeakStats(self, val):
        self.__track_peak_stats = val

    def setTrackIngressPortPriorityGroup(self, val):
        self.__track_ingress_port_priority_group = val

    def setTrackIngressPortServicePool(self, val):
        self.__track_ingress_port_service_pool = val

    def setTrackIngressServicePool(self, val):
        self.__track_ingress_service_pool = val

    def setTrackEgressPortServicePool(self, val):
        self.__track_egress_port_service_pool = val

    def setTrackEgressServicePool(self, val):
        self.__track_egress_service_pool = val

    def setTrackEgressUcQueue(self, val):
        self.__track_egress_uc_queue = val

    def setTrackEgressUcQueueGroup(self, val):
        self.__track_egress_uc_queue_group = val

    def setTrackEgressMcQueue(self, val):
        self.__track_egress_mc_queue = val

    def setTrackEgressCPUQueue(self, val):
        self.__track_egress_cpu_queue = val

    def setTrackEgressRQEQueue(self, val):
        self.__track_egress_rqe_queue = val

    def setTrackDevice(self, val):
        self.__track_device = val

    def setASIC(self, val):
        self.__asic_id = val

    def send(self):
        status, json = self._send(self.toDict())
        return status

    def toDict(self):
        ret = {}
        params = {}
        params["track-peak-stats"] = 1 if self.__track_peak_stats else 0
        params["track-ingress-port-priority-group"] = 1 if self.__track_ingress_port_priority_group else 0
        params["track-ingress-port-service-pool"] = 1 if self.__track_ingress_port_service_pool else 0
        params["track-ingress-service-pool"] = 1 if self.__track_ingress_service_pool else 0
        params["track-egress-port-service-pool"] = 1 if self.__track_egress_port_service_pool else 0
        params["track-egress-service-pool"] = 1 if self.__track_egress_service_pool else 0
        params["track-egress-uc-queue"] = 1 if self.__track_egress_uc_queue else 0
        params["track-egress-uc-queue-group"] = 1 if self.__track_egress_uc_queue_group else 0
        params["track-egress-mc-queue"] = 1 if self.__track_egress_mc_queue else 0
        params["track-egress-cpu-queue"] = 1 if self.__track_egress_cpu_queue else 0
        params["track-egress-rqe-queue"] = 1 if self.__track_egress_rqe_queue else 0
        params["track-device"] = 1 if self.__track_device else 0
        ret["asic-id"] = self.__asic_id
        ret["params"] = params
        ret["method"] = "configure-bst-tracking"
        return ret

class ConfigureBSTThresholds(AgentAPI):
    def __init__(self, host, port):
        super(ConfigureBSTThresholds, self).__init__()
        self.setFeature("bst")
        self.setHost(host)
        self.setPort(port)
        self.__asic_id = "1"
        self.__params = {}

    def setASIC(self, val):
        self.__asic_id = val

    def setParams(self, params):
        self.__params = params

    def send(self):
        status, json = self._send(self.toDict())
        return status 

    def toDict(self):
        ret = {}
        params = {}
        ret["asic-id"] = self.__asic_id
        ret["params"] = self.getParams()
        ret["method"] = "configure-bst-thresholds"
        return ret

class ConfigureDeviceThreshold(ConfigureBSTThresholds):
    def __init__(self, host, port, threshold):
        super(ConfigureDeviceThreshold, self).__init__(host, port)
        self.__realm = "device"
        self.__threshold = threshold

    def getParams(self):
        ret = {}
        ret["realm"] = self.__realm
        ret["threshold"] = self.__threshold 
        return ret

class ConfigureEgressCpuQueueThreshold(ConfigureBSTThresholds):
    def __init__(self, host, port, queue, threshold):
        super(ConfigureEgressCpuQueueThreshold, self).__init__(host, port)
        self.__realm = "egress-cpu-queue"
        self.__queue = queue
        self.__threshold = threshold

    def getParams(self):
        ret = {}
        ret["realm"] = self.__realm
        ret["queue"] = self.__queue 
        ret["cpu-threshold"] = self.__threshold 
        return ret

class ConfigureEgressRqeQueueThreshold(ConfigureBSTThresholds):
    def __init__(self, host, port, queue, threshold):
        super(ConfigureEgressRqeQueueThreshold, self).__init__(host, port)
        self.__realm = "egress-rqe-queue"
        self.__queue = queue
        self.__threshold = threshold

    def getParams(self):
        ret = {}
        ret["realm"] = self.__realm
        ret["queue"] = self.__queue 
        ret["rqe-threshold"] = self.__threshold 
        return ret

class ConfigureEgressPortServicePoolThreshold(ConfigureBSTThresholds):
    def __init__(self, host, port, 
                       eport,
                       servicePool, 
                       ucShareThreshold,
                       umShareThreshold,
                       mcShareThreshold,
                       mcShareQueueEntriesThreshold):
        super(ConfigureEgressPortServicePoolThreshold, self).__init__(host, port)
        self.__realm = "egress-port-service-pool"
        self.__port = eport
        self.__servicePool = servicePool
        self.__ucShareThreshold = ucShareThreshold
        self.__umShareThreshold = umShareThreshold
        self.__mcShareThreshold = mcShareThreshold
        self.__mcShareQueueEntriesThreshold = mcShareQueueEntriesThreshold

    def getParams(self):
        ret = {}
        ret["realm"] = self.__realm
        ret["port"] = self.__port
        ret["service-pool"] = self.__servicePool 
        ret["uc-share-threshold"] = self.__ucShareThreshold 
        ret["um-share-threshold"] = self.__umShareThreshold 
        ret["mc-share-threshold"] = self.__mcShareThreshold 
        ret["mc-share-queue-entries-threshold"] = self.__mcShareQueueEntriesThreshold 
        return ret

class ConfigureEgressServicePoolThreshold(ConfigureBSTThresholds):
    def __init__(self, host, port,
                       servicePool, 
                       umShareThreshold,
                       mcShareThreshold,
                       mcShareQueueEntriesThreshold):
        super(ConfigureEgressServicePoolThreshold, self).__init__(host, port)
        self.__realm = "egress-service-pool"
        self.__servicePool = servicePool
        self.__umShareThreshold = umShareThreshold
        self.__mcShareThreshold = mcShareThreshold
        self.__mcShareQueueEntriesThreshold = mcShareQueueEntriesThreshold

    def getParams(self):
        ret = {}
        ret["realm"] = self.__realm
        ret["service-pool"] = self.__servicePool 
        ret["um-share-threshold"] = self.__umShareThreshold 
        ret["mc-share-threshold"] = self.__mcShareThreshold 
        ret["mc-share-queue-entries-threshold"] = self.__mcShareQueueEntriesThreshold 
        return ret

class ConfigureEgressUcQueueThreshold(ConfigureBSTThresholds):
    def __init__(self, host, port, queue, threshold):
        super(ConfigureEgressUcQueueThreshold, self).__init__(host, port)
        self.__realm = "egress-uc-queue"
        self.__queue = queue
        self.__threshold = threshold

    def getParams(self):
        ret = {}
        ret["realm"] = self.__realm
        ret["queue"] = self.__queue 
        ret["uc-threshold"] = self.__threshold 
        return ret

class ConfigureEgressUcQueueGroupThreshold(ConfigureBSTThresholds):
    def __init__(self, host, port, queueGroup, threshold):
        super(ConfigureEgressUcQueueGroupThreshold, self).__init__(host, port)
        self.__realm = "egress-uc-queue-group"
        self.__queueGroup = queueGroup
        self.__threshold = threshold

    def getParams(self):
        ret = {}
        ret["realm"] = self.__realm
        ret["queue-group"] = self.__queueGroup 
        ret["uc-threshold"] = self.__threshold 
        return ret

class ConfigureEgressMcQueueThreshold(ConfigureBSTThresholds):
    def __init__(self, host, port,
                       queue,
                       mcQueueEntriesThreshold,
                       mcThreshold):
        super(ConfigureEgressMcQueueThreshold, self).__init__(host, port)
        self.__realm = "egress-mc-queue"
        self.__queue = queue
        self.__mcQueueEntriesThreshold = mcQueueEntriesThreshold
        self.__mcThreshold = mcThreshold

    def getParams(self):
        ret = {}
        ret["realm"] = self.__realm
        ret["queue"] = self.__queue
        ret["mc-queue-entries-threshold"] = self.__mcQueueEntriesThreshold
        ret["mc-threshold"] = self.__mcThreshold
        return ret

class ConfigureIngressPortPriorityGroupThreshold(ConfigureBSTThresholds):
    def __init__(self, host, port,
                       eport,
                       priorityGroup,
                       umShareThreshold,
                       umHeadroomThreshold):
        super(ConfigureIngressPortPriorityGroupThreshold, self).__init__(host, port)
        self.__realm = "ingress-port-priority-group"
        self.__port = eport
        self.__priorityGroup = priorityGroup
        self.__umShareThreshold = umShareThreshold
        self.__umHeadroomThreshold = umHeadroomThreshold

    def getParams(self):
        ret = {}
        ret["realm"] = self.__realm
        ret["port"] = self.__port
        ret["priority-group"] = self.__priorityGroup
        ret["um-share-threshold"] = self.__umShareThreshold
        ret["um-headroom-threshold"] = self.__umHeadroomThreshold
        return ret

class ConfigureIngressPortServicePoolThreshold(ConfigureBSTThresholds):
    def __init__(self, host, port,
                       eport,
                       servicePool,
                       threshold):
        super(ConfigureIngressPortServicePoolThreshold, self).__init__(host, port)
        self.__realm = "ingress-port-service-pool"
        self.__port = eport
        self.__servicePool = servicePool
        self.__threshold = threshold

    def getParams(self):
        ret = {}
        ret["realm"] = self.__realm
        ret["port"] = self.__port
        ret["service-pool"] = self.__servicePool
        ret["um-share-threshold"] = self.__threshold
        return ret

class ConfigureIngressServicePoolThreshold(ConfigureBSTThresholds):
    def __init__(self, host, port, servicePool, threshold):
        super(ConfigureIngressServicePoolThreshold, self).__init__(host, port)
        self.__realm = "ingress-service-pool"
        self.__servicePool = servicePool
        self.__threshold = threshold

    def getParams(self):
        ret = {}
        ret["realm"] = self.__realm
        ret["service-pool"] = self.__servicePool
        ret["um-share-threshold"] = self.__threshold
        return ret

class ClearBSTStatistics(AgentAPI):
    def __init__(self, host, port):
        super(ClearBSTStatistics, self).__init__()
        self.setFeature("bst")
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.__asic_id = "1"

    def setASIC(self, val):
        self.__asic_id = val

    def send(self):
        status, json = self._send(self.toDict())
        return status

    def toDict(self):
        ret = {}
        params = {}
        ret["asic-id"] = self.__asic_id
        ret["params"] = params
        ret["method"] = "clear-bst-statistics"
        return ret

class ClearBSTThresholds(AgentAPI):
    def __init__(self, host, port):
        super(ClearBSTThresholds, self).__init__()
        self.setFeature("bst")
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.__asic_id = "1"

    def setASIC(self, val):
        self.__asic_id = val

    def send(self):
        status, json = self._send(self.toDict())
        return status

    def toDict(self):
        ret = {}
        params = {}
        ret["asic-id"] = self.__asic_id
        ret["params"] = params
        ret["method"] = "clear-bst-thresholds"
        return ret

'''

Status/Reporting Requests

'''

class GetBSTFeature(AgentAPI):
    def __init__(self, host, port):
        super(GetBSTFeature, self).__init__()
        self.setFeature("bst")
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.__bst_enable = False
        self.__version = 1
        self.__send_async_reports = False
        self.__collection_interval = 200
        self.__stat_in_percentage = False
        self.__stat_units_in_cells = False
        self.__trigger_rate_limit = False
        self.__trigger_rate_limit_interval = 0
        self.__send_snapshot_on_trigger = False
        self.__asic_id = "1"
        self.__json = None

    def getEnable(self):
        return self.__bst_enable

    def getSendAsyncReports(self):
        return self.__send_async_reports

    def getCollectionInterval(self):
        return self.__collection_interval

    def getStatInPercentage(self):
        return self.__stat_in_percentage

    def getStatUnitsInCells(self):
        return self.__stat_units_in_cells

    def getTriggerRateLimit(self):
        return self.__trigger_rate_limit

    def getTriggerRateLimitInterval(self):
        return self.__trigger_rate_limit_interval

    def getSendSnapshotOnTrigger(self):
        return self.__send_snapshot_on_trigger

    def getAsyncFullReports(self):
        return self.__async_full_reports

    def getASIC(self):
        return self.__asic_id

    def setASIC(self, val):
        self.__asic_id = val

    def getJSON(self):
        return self.__json

    def send(self):
        status, json = self._send(self.toDict())
        if status == 200:
            self.__version = json["version"]
            res = json["result"]
            self.__json = res
            self.__bst_enable = res["bst-enable"] == 1
            self.__send_async_reports = res["send-async-reports"] == 1
            self.__collection_interval = res["collection-interval"]
            # XXX self.__stat_in_percentage = res["stat-in-percentage"] == 1
            self.__stat_units_in_cells = res["stat-units-in-cells"] == 1
            self.__trigger_rate_limit = res["trigger-rate-limit"] == 1
            self.__trigger_rate_limit_interval = res["trigger-rate-limit-interval"]
            self.__send_snapshot_on_trigger = res["send-snapshot-on-trigger"] == 1
        return status

    def toDict(self):
        ret = {}
        params = {}
        ret["asic-id"] = self.__asic_id
        ret["params"] = params
        ret["method"] = "get-bst-feature"
        return ret

class GetBSTTracking(AgentAPI):
    def __init__(self, host, port):
        super(GetBSTTracking, self).__init__()
        self.setFeature("bst")
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.__track_peak_stats = False
        self.__track_ingress_port_priority_group = False
        self.__track_ingress_port_service_pool = False
        self.__track_ingress_service_pool = False
        self.__track_egress_port_service_pool = False
        self.__track_egress_service_pool = False
        self.__track_egress_uc_queue = False
        self.__track_egress_uc_queue_group = False
        self.__track_egress_mc_queue = False
        self.__track_egress_cpu_queue = False
        self.__track_egress_rqe_queue = False
        self.__track_device = False
        self.__asic_id = "1"
        self.__json = None

    def getTrackPeakStats(self):
        return self.__track_peak_stats

    def getTrackIngressPortPriorityGroup(self):
        return self.__track_ingress_port_priority_group

    def getTrackIngressPortServicePool(self):
        return self.__track_ingress_port_service_pool

    def getTrackIngressServicePool(self):
        return self.__track_ingress_service_pool

    def getTrackEgressPortServicePool(self):
        return self.__track_egress_port_service_pool

    def getTrackEgressServicePool(self):
        return self.__track_egress_service_pool

    def getTrackEgressUcQueue(self):
        return self.__track_egress_uc_queue

    def getTrackEgressUcQueueGroup(self):
        return self.__track_egress_uc_queue_group

    def getTrackEgressMcQueue(self):
        return self.__track_egress_mc_queue

    def getTrackEgressCPUQueue(self):
        return self.__track_egress_cpu_queue

    def getTrackEgressRQEQueue(self):
        return self.__track_egress_rqe_queue

    def getTrackDevice(self):
        return self.__track_device

    def getASIC(self):
        return self.__asic_id

    def setASIC(self, val):
        self.__asic_id = val

    def getJSON(self):
        return self.__json

    def send(self):
        status, json = self._send(self.toDict())
        if status == 200:
            self.__version = json["version"]
            res = json["result"]
            self.__json = res
            self.__track_peak_stats = res["track-peak-stats"] == 1
            self.__track_ingress_port_priority_group = res["track-ingress-port-priority-group"] == 1
            self.__track_ingress_port_service_pool = res["track-ingress-port-service-pool"]  == 1
            self.__track_ingress_service_pool = res["track-ingress-service-pool"] == 1
            self.__track_egress_port_service_pool = res["track-egress-port-service-pool"] == 1
            self.__track_egress_service_pool = res["track-egress-service-pool"] == 1
            self.__track_egress_uc_queue = res["track-egress-uc-queue"] == 1
            self.__track_egress_uc_queue_group = res["track-egress-uc-queue-group"] == 1
            self.__track_egress_mc_queue = res["track-egress-mc-queue"] == 1
            self.__track_egress_cpu_queue = res["track-egress-cpu-queue"] == 1
            self.__track_egress_rqe_queue = res["track-egress-rqe-queue"] == 1
            self.__track_device = res["track-device"] == 1
        return status

    def toDict(self):
        ret = {}
        params = {}
        ret["asic-id"] = self.__asic_id
        ret["params"] = params
        ret["method"] = "get-bst-tracking"
        return ret

class GetBSTThresholds(AgentAPI):
    def __init__(self, host, port):
        super(GetBSTThresholds, self).__init__()
        self.setFeature("bst")
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.__include_ingress_port_priority_group = False
        self.__include_ingress_port_service_pool = False
        self.__include_ingress_service_pool = False
        self.__include_egress_port_service_pool = False
        self.__include_egress_service_pool = False
        self.__include_egress_uc_queue = False
        self.__include_egress_uc_queue_group = False
        self.__include_egress_mc_queue = False
        self.__include_egress_cpu_queue = False
        self.__include_egress_rqe_queue = False
        self.__include_device = False
        self.__asic_id = "1"

    def setIncludeIngressPortPriorityGroup(self, val):
        self.__include_ingress_port_priority_group = val
      
    def setIncludeIngressPortServicePool(self, val):
        self.__include_ingress_port_service_pool = val

    def setIncludeIngressServicePool(self, val):
        self.__include_ingress_service_pool = val

    def setIncludeEgressPortServicePool(self, val):
        self.__include_egress_port_service_pool = val

    def setIncludeEgressServicePool(self, val):
        self.__include_egress_service_pool = val

    def setIncludeEgressUcQueue(self, val):
        self.__include_egress_uc_queue = val

    def setIncludeEgressUcQueueGroup(self, val):
        self.__include_egress_uc_queue_group = val

    def setIncludeEgressMcQueue(self, val):
        self.__include_egress_mc_queue = val

    def setIncludeEgressCPUQueue(self, val):
        self.__include_egress_cpu_queue = val

    def setIncludeEgressRQEQueue(self, val): 
        self.__include_egress_rqe_queue = val

    def setIncludeDevice(self, val):
        self.__include_device = val

    def setASIC(self, val):
        self.__asic_id = val

    def getJSON(self):
        return self.__json

    def send(self):
        rep = None
        status, json = self._send(self.toDict())
        if status == 200:
            rep = BSTParser()
            self.__json = json["report"]
            rep.process(json)
        return status, rep

    def toDict(self):
        ret = {}
        params = {}
        params["include-ingress-port-priority-group"] = 1 if self.__include_ingress_port_priority_group else 0
        params["include-ingress-port-service-pool"] = 1 if self.__include_ingress_port_service_pool else 0
        params["include-ingress-service-pool"] = 1 if self.__include_ingress_service_pool else 0
        params["include-egress-port-service-pool"] = 1 if self.__include_egress_port_service_pool else 0
        params["include-egress-service-pool"] = 1 if self.__include_egress_service_pool else 0
        params["include-egress-uc-queue"] = 1 if self.__include_egress_uc_queue else 0
        params["include-egress-uc-queue-group"] = 1 if self.__include_egress_uc_queue_group else 0
        params["include-egress-mc-queue"] = 1 if self.__include_egress_mc_queue else 0
        params["include-egress-cpu-queue"] = 1 if self.__include_egress_cpu_queue else 0
        params["include-egress-rqe-queue"] = 1 if self.__include_egress_rqe_queue else 0
        params["include-device"] = 1 if self.__include_device else 0

        ret["asic-id"] = self.__asic_id
        ret["params"] = params
        ret["method"] = "get-bst-thresholds"
        return ret

class GetBSTReport(AgentAPI):
    def __init__(self, host, port):
        super(GetBSTReport, self).__init__()
        self.setFeature("bst")
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.__include_ingress_port_priority_group = False
        self.__include_ingress_port_service_pool = False
        self.__include_ingress_service_pool = False
        self.__include_egress_port_service_pool = False
        self.__include_egress_service_pool = False
        self.__include_egress_uc_queue = False
        self.__include_egress_uc_queue_group = False
        self.__include_egress_mc_queue = False
        self.__include_egress_cpu_queue = False
        self.__include_egress_rqe_queue = False
        self.__include_device = False
        self.__asic_id = "1"
        self.__json = None

    def setIncludeIngressPortPriorityGroup(self, val):
        self.__include_ingress_port_priority_group = val

    def setIncludeIngressPortServicePool(self, val):
        self.__include_ingress_port_service_pool = val

    def setIncludeIngressServicePool(self, val):
        self.__include_ingress_service_pool = val

    def setIncludeEgressPortServicePool(self, val):
        self.__include_egress_port_service_pool = val

    def setIncludeEgressServicePool(self, val):
        self.__include_egress_service_pool = val

    def setIncludeEgressUcQueue(self, val):
        self.__include_egress_uc_queue = val

    def setIncludeEgressUcQueueGroup(self, val):
        self.__include_egress_uc_queue_group = val

    def setIncludeEgressMcQueue(self, val):
        self.__include_egress_mc_queue = val

    def setIncludeEgressCPUQueue(self, val):
        self.__include_egress_cpu_queue = val

    def setIncludeEgressRQEQueue(self, val):
        self.__include_egress_rqe_queue = val

    def setIncludeDevice(self, val):
        self.__include_device = val

    def setASIC(self, val):
        self.__asic_id = val

    def getJSON(self):
        return self.__json

    def send(self):
        status, json = self._send(self.toDict())
        rep = None
        if status == 200:
            self.__json = json["report"]
            rep = BSTParser()
            rep.process(json)
        else:
            pass
        return status, rep

    def toDict(self):
        ret = {}
        params = {}
        params["include-ingress-port-priority-group"] = 1 if self.__include_ingress_port_priority_group else 0
        params["include-ingress-port-service-pool"] = 1 if self.__include_ingress_port_service_pool else 0
        params["include-ingress-service-pool"] = 1 if self.__include_ingress_service_pool else 0
        params["include-egress-port-service-pool"] = 1 if self.__include_egress_port_service_pool else 0
        params["include-egress-service-pool"] = 1 if self.__include_egress_service_pool else 0
        params["include-egress-uc-queue"] = 1 if self.__include_egress_uc_queue else 0
        params["include-egress-uc-queue-group"] = 1 if self.__include_egress_uc_queue_group else 0
        params["include-egress-mc-queue"] = 1 if self.__include_egress_mc_queue else 0
        params["include-egress-cpu-queue"] = 1 if self.__include_egress_cpu_queue else 0
        params["include-egress-rqe-queue"] = 1 if self.__include_egress_rqe_queue else 0
        params["include-device"] = 1 if self.__include_device else 0 
        ret["asic-id"] = self.__asic_id
        ret["params"] = params
        ret["method"] = "get-bst-report"
        return ret

class TestBSTAPIParams(unittest.TestCase):

    def setUp(self):
        pass

    def test_ConfigureBSTFeature(self):

        sw = BroadViewBSTSwitches()
        if len(sw):
            for x in sw:
                host = x["ip"]
                port = x["port"]
                break
        else:
            host = "192.168.3.1"
            port = 8080

        x = ConfigureBSTFeature(host, port)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(x.getFeature() == "bst")
        self.assertTrue(x.getHttpMethod() == "POST")
        self.assertTrue(x.getHost() == host)
        self.assertTrue(x.getPort() == port)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "configure-bst-feature")

        params = d["params"]
        self.assertEqual(params["bst-enable"], False)
        self.assertEqual(params["send-async-reports"], False)
        self.assertEqual(params["collection-interval"], 60)
        self.assertEqual(params["stat-in-percentage"], False)
        self.assertEqual(params["stat-units-in-cells"], False)
        self.assertEqual(params["trigger-rate-limit"], 1)
        self.assertEqual(params["trigger-rate-limit-interval"], 1) 
        self.assertEqual(params["send-snapshot-on-trigger"], True)
        self.assertEqual(params["async-full-reports"], False)

        x.setEnable(True)
        x.setSendAsyncReports(True)
        x.setCollectionInterval(120)
        x.setStatInPercentage(True)
        x.setStatUnitsInCells(True)
        x.setTriggerRateLimit(15)
        x.setTriggerRateLimitInterval(99)
        x.setSendSnapshotOnTrigger(False)
        x.setAsyncFullReports(True)
        d = x.toDict()
        
        params = d["params"]
        self.assertEqual(params["bst-enable"], True)
        self.assertEqual(params["send-async-reports"], True)
        self.assertEqual(params["collection-interval"], 120)
        self.assertEqual(params["stat-in-percentage"], True)
        self.assertEqual(params["stat-units-in-cells"], True)
        self.assertEqual(params["trigger-rate-limit"], 15)
        self.assertEqual(params["trigger-rate-limit-interval"], 99) 
        self.assertEqual(params["send-snapshot-on-trigger"], False)
        self.assertEqual(params["async-full-reports"], True)

    def test_ConfigureBSTTracking(self):
        host = "192.168.3.1"
        port = 8080
        x = ConfigureBSTTracking(host, port)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(x.getFeature() == "bst")
        self.assertTrue(x.getHttpMethod() == "POST")
        self.assertTrue(x.getHost() == host)
        self.assertTrue(x.getPort() == port)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "configure-bst-tracking")

        params = d["params"]

        self.assertEqual(params["track-peak-stats"], False)
        self.assertEqual(params["track-ingress-port-priority-group"], False)
        self.assertEqual(params["track-ingress-port-service-pool"], False)
        self.assertEqual(params["track-ingress-service-pool"], False)
        self.assertEqual(params["track-egress-port-service-pool"], False)
        self.assertEqual(params["track-egress-service-pool"], False)
        self.assertEqual(params["track-egress-uc-queue"], False)
        self.assertEqual(params["track-egress-uc-queue-group"], False)
        self.assertEqual(params["track-egress-mc-queue"], False)
        self.assertEqual(params["track-egress-cpu-queue"], False)
        self.assertEqual(params["track-egress-rqe-queue"], False)
        self.assertEqual(params["track-device"], False)

        x.setTrackPeakStats(True)
        x.setTrackIngressPortPriorityGroup(True)
        x.setTrackIngressPortServicePool(True)
        x.setTrackIngressServicePool(True)
        x.setTrackEgressPortServicePool(True)
        x.setTrackEgressServicePool(True)
        x.setTrackEgressUcQueue(True)
        x.setTrackEgressUcQueueGroup(True)
        x.setTrackEgressMcQueue(True)
        x.setTrackEgressCPUQueue(True)
        x.setTrackEgressRQEQueue(True)
        x.setTrackDevice(True)
        x.setASIC("3")

        d = x.toDict()
        self.assertTrue(d["asic-id"] == "3")

        params = d["params"]

        self.assertEqual(params["track-peak-stats"], True)
        self.assertEqual(params["track-ingress-port-priority-group"], True)
        self.assertEqual(params["track-ingress-port-service-pool"], True)
        self.assertEqual(params["track-ingress-service-pool"], True)
        self.assertEqual(params["track-egress-port-service-pool"], True)
        self.assertEqual(params["track-egress-service-pool"], True)
        self.assertEqual(params["track-egress-uc-queue"], True)
        self.assertEqual(params["track-egress-uc-queue-group"], True)
        self.assertEqual(params["track-egress-mc-queue"], True)
        self.assertEqual(params["track-egress-cpu-queue"], True)
        self.assertEqual(params["track-egress-rqe-queue"], True)
        self.assertEqual(params["track-device"], True)

    def test_ClearBSTStatistics(self):
        host = "192.168.3.1"
        port = 8080
        x = ClearBSTStatistics(host, port)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(x.getFeature() == "bst")
        self.assertTrue(x.getHttpMethod() == "POST")
        self.assertTrue(x.getHost() == host)
        self.assertTrue(x.getPort() == port)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "clear-bst-statistics")
        self.assertTrue(not d["params"])  # assert empty

        x.setASIC("3")

        d = x.toDict()
        self.assertTrue(d["asic-id"] == "3")
        
    def test_ClearBSTThresholds(self):
        host = "192.168.3.1"
        port = 8080
        x = ClearBSTThresholds(host, port)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(x.getFeature() == "bst")
        self.assertTrue(x.getHttpMethod() == "POST")
        self.assertTrue(x.getHost() == host)
        self.assertTrue(x.getPort() == port)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "clear-bst-thresholds")
        self.assertTrue(not d["params"])  # assert empty

        x.setASIC("3")

        d = x.toDict()
        self.assertTrue(d["asic-id"] == "3")

    def test_GetBSTThresholds(self):
        host = "192.168.3.1"
        port = 8080
        x = GetBSTThresholds(host, port)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(x.getFeature() == "bst")
        self.assertTrue(x.getHttpMethod() == "POST")
        self.assertTrue(x.getHost() == host)
        self.assertTrue(x.getPort() == port)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "get-bst-thresholds")

        x.setASIC("3")

        d = x.toDict()
        self.assertTrue(d["asic-id"] == "3")

    def test_GetBSTFeature(self):
        host = "192.168.3.1"
        port = 8080
        x = GetBSTFeature(host, port)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(x.getFeature() == "bst")
        self.assertTrue(x.getHttpMethod() == "POST")
        self.assertTrue(x.getHost() == host)
        self.assertTrue(x.getPort() == port)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "get-bst-feature")
        self.assertTrue(not d["params"])  # assert empty

        x.setASIC("3")

        d = x.toDict()
        self.assertTrue(d["asic-id"] == "3")

    def test_GetBSTReport(self):
        host = "192.168.3.1"
        port = 8080
        x = GetBSTReport(host, port)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(x.getFeature() == "bst")
        self.assertTrue(x.getHttpMethod() == "POST")
        self.assertTrue(x.getHost() == host)
        self.assertTrue(x.getPort() == port)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "get-bst-report")

        x.setASIC("3")

        d = x.toDict()
        self.assertTrue(d["asic-id"] == "3")


    def test_ConfigureDeviceThreshold(self):
        host = "192.168.3.1"
        port = 8080
        x = ConfigureDeviceThreshold(host, port, 10000)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "configure-bst-thresholds")
        parms = x.getParams()
        self.assertTrue(parms["realm"] == "device")
        self.assertTrue(parms["threshold"] == 10000)

    def test_ConfigureEgressCpuQueueThreshold(self):
        host = "192.168.3.1"
        port = 8080
        x = ConfigureEgressCpuQueueThreshold(host, port, 5, 10000)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "configure-bst-thresholds")
        parms = x.getParams()
        self.assertTrue(parms["realm"] == "egress-cpu-queue")
        self.assertTrue(parms["queue"] == 5)
        self.assertTrue(parms["cpu-threshold"] == 10000)

    def test_ConfigureEgressRqeQueueThreshold(self):
        host = "192.168.3.1"
        port = 8080
        x = ConfigureEgressRqeQueueThreshold(host, port, 5, 10000)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "configure-bst-thresholds")
        parms = x.getParams()
        self.assertTrue(parms["realm"] == "egress-rqe-queue")
        self.assertTrue(parms["queue"] == 5)
        self.assertTrue(parms["rqe-threshold"] == 10000)

    def test_ConfigureEgressPortServicePoolThreshold(self):
        host = "192.168.3.1"
        port = 8080
        x = ConfigureEgressPortServicePoolThreshold(host, port, "2", 5, 100, 200, 300, 400)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "configure-bst-thresholds")
        parms = x.getParams()
        self.assertTrue(parms["realm"] == "egress-port-service-pool")
        self.assertTrue(parms["port"] == "2")
        self.assertTrue(parms["service-pool"] == 5)
        self.assertTrue(parms["uc-share-threshold"] == 100)
        self.assertTrue(parms["um-share-threshold"] == 200)
        self.assertTrue(parms["mc-share-threshold"] == 300)
        self.assertTrue(parms["mc-share-queue-entries-threshold"] == 400)

    def test_ConfigureEgressServicePoolThreshold(self):
        host = "192.168.3.1"
        port = 8080
        x = ConfigureEgressServicePoolThreshold(host, port, 5, 100, 200, 300)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "configure-bst-thresholds")
        parms = x.getParams()
        self.assertTrue(parms["realm"] == "egress-service-pool")
        self.assertTrue(parms["service-pool"] == 5)
        self.assertTrue(parms["um-share-threshold"] == 100)
        self.assertTrue(parms["mc-share-threshold"] == 200)
        self.assertTrue(parms["mc-share-queue-entries-threshold"] == 300)

    def test_ConfigureEgressUcQueueThreshold(self):
        host = "192.168.3.1"
        port = 8080
        x = ConfigureEgressUcQueueThreshold(host, port, 5, 100)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "configure-bst-thresholds")
        parms = x.getParams()
        self.assertTrue(parms["realm"] == "egress-uc-queue")
        self.assertTrue(parms["queue"] == 5)
        self.assertTrue(parms["uc-threshold"] == 100)

    def test_ConfigureEgressUcQueueGroupThreshold(self):
        host = "192.168.3.1"
        port = 8080
        x = ConfigureEgressUcQueueGroupThreshold(host, port, 7, 200)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "configure-bst-thresholds")
        parms = x.getParams()
        self.assertTrue(parms["realm"] == "egress-uc-queue-group")
        self.assertTrue(parms["queue-group"] == 7)
        self.assertTrue(parms["uc-threshold"] == 200)

    def test_ConfigureEgressMcQueueThreshold(self):
        host = "192.168.3.1"
        port = 8080
        x = ConfigureEgressMcQueueThreshold(host, port, 7, 100, 200)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "configure-bst-thresholds")
        parms = x.getParams()
        self.assertTrue(parms["realm"] == "egress-mc-queue")
        self.assertTrue(parms["queue"] == 7)
        self.assertTrue(parms["mc-queue-entries-threshold"] == 100)
        self.assertTrue(parms["mc-threshold"] == 200)

    def test_ConfigureEgressMcQueueThreshold(self):
        host = "192.168.3.1"
        port = 8080
        x = ConfigureEgressMcQueueThreshold(host, port, 7, 100, 200)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "configure-bst-thresholds")
        parms = x.getParams()
        self.assertTrue(parms["realm"] == "egress-mc-queue")
        self.assertTrue(parms["queue"] == 7)
        self.assertTrue(parms["mc-queue-entries-threshold"] == 100)
        self.assertTrue(parms["mc-threshold"] == 200)

    def test_ConfigureIngressPortPriorityGroupThreshold(self):
        host = "192.168.3.1"
        port = 8080
        x = ConfigureIngressPortPriorityGroupThreshold(host, port, "3", 7, 100, 200)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "configure-bst-thresholds")
        parms = x.getParams()
        self.assertTrue(parms["realm"] == "ingress-port-priority-group")
        self.assertTrue(parms["port"] == "3")
        self.assertTrue(parms["priority-group"] == 7)
        self.assertTrue(parms["um-share-threshold"] == 100)
        self.assertTrue(parms["um-headroom-threshold"] == 200)

    def test_ConfigureIngressPortServicePoolThreshold(self):
        host = "192.168.3.1"
        port = 8080
        x = ConfigureIngressPortServicePoolThreshold(host, port, "3", 7, 100)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "configure-bst-thresholds")
        parms = x.getParams()
        self.assertTrue(parms["realm"] == "ingress-port-service-pool")
        self.assertTrue(parms["port"] == "3")
        self.assertTrue(parms["service-pool"] == 7)
        self.assertTrue(parms["um-share-threshold"] == 100)

    def test_ConfigureIngressServicePoolThreshold(self):
        host = "192.168.3.1"
        port = 8080
        x = ConfigureIngressServicePoolThreshold(host, port, 7, 200)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "configure-bst-thresholds")
        parms = x.getParams()
        self.assertTrue(parms["realm"] == "ingress-service-pool")
        self.assertTrue(parms["service-pool"] == 7)
        self.assertTrue(parms["um-share-threshold"] == 200)

if __name__ == "__main__":
    unittest.main()
