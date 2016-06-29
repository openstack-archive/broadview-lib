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
from broadview_lib.pt.pt_parser import PTParser
from broadview_lib.config.broadviewconfig import BroadViewBSTSwitches
import unittest

class ConfigurePacketTraceFeature(AgentAPI):
    def __init__(self, host, port):
        super(ConfigurePacketTraceFeature, self).__init__()
        self.setFeature("packettrace")
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.__packet_trace_enable = False
        self.__asic_id = "1"

    def setEnable(self, val):
        self.__packet_trace_enable = val

    def setASIC(self, val):
        self.__asic_id = val

    def send(self, timeout=30):
        status, json = self._send(self.toDict(), timeout)
        return status


    def toDict(self):
        ret = {}
        params = {}
        params["packet-trace-enable"] = 1 if self.__packet_trace_enable else 0 
        ret["asic-id"] = self.__asic_id
        ret["params"] = params
        ret["method"] = "configure-packet-trace-feature"
        return ret

class ConfigurePacketTraceDropReason(AgentAPI):
    def __init__(self, host, port):
        super(ConfigurePacketTraceDropReason, self).__init__()
        self.setFeature("packettrace")
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.__reason = []
        self.__port_list = []
        self.__send_dropped_packet = False
        self.__trace_profile = False
        self.__packet_count = 1
        self.__packet_threshold = 0
        self.__asic_id = "1"

    def setReason(self, val):
        self.__reason = val

    def setPortList(self, val):
        self.__port_list = val

    def setSendDroppedPacket(self, val):
        self.__send_dropped_packet = val

    def setTraceProfile(self, val):
        self.__trace_profile = val

    def setPacketCount(self, val):
        self.__packet_count = val

    def setPacketThreshold(self, val):
        self.__packet_threshold = val

    def setASIC(self, val):
        self.__asic_id = val

    def send(self, timeout=30):
        status, json = self._send(self.toDict(), timeout)
        return status

    def toDict(self):
        ret = {}
        params = {}
        params["reason"] = self.__reason
        params["port-list"] = self.__port_list
        params["send-dropped-packet"] = self.__send_dropped_packet
        params["trace-profile"] = self.__trace_profile
        params["packet-count"] = self.__packet_count
        params["packet-threshold"] = self.__packet_threshold
        ret["asic-id"] = self.__asic_id
        ret["params"] = params
        ret["method"] = "configure-packet-trace-drop-reason"
        return ret

class CancelPacketTraceProfile(AgentAPI):
    def __init__(self, host, port):
        super(CancelPacketTraceProfile, self).__init__()
        self.setFeature("packettrace")
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.__id = 0
        self.__asic_id = "1"

    def setId(self, val):
        self.__id = val

    def setASIC(self, val):
        self.__asic_id = val

    def send(self, timeout=30):
        status, json = self._send(self.toDict(), timeout)
        return status

    def toDict(self):
        ret = {}
        params = {}
        params["id"] = self.__id
        ret["asic-id"] = self.__asic_id
        ret["params"] = params
        ret["method"] = "cancel-packet-trace-profile"
        return ret


class CancelPacketTraceLAGResolution(AgentAPI):
    def __init__(self, host, port):
        super(CancelPacketTraceLAGResolution, self).__init__()
        self.setFeature("packettrace")
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.__id = 0
        self.__asic_id = "1"

    def setId(self, val):
        self.__id = val

    def setASIC(self, val):
        self.__asic_id = val

    def send(self, timeout=30):
        status, json = self._send(self.toDict(), timeout)
        return status

    def toDict(self):
        ret = {}
        params = {}
        params["id"] = self.__id
        ret["asic-id"] = self.__asic_id
        ret["params"] = params
        ret["method"] = "cancel-packet-trace-lag-resolution"
        return ret

class CancelPacketTraceECMPResolution(AgentAPI):
    def __init__(self, host, port):
        super(CancelPacketTraceECMPResolution, self).__init__()
        self.setFeature("packettrace")
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.__id = 0
        self.__asic_id = "1"

    def setId(self, val):
        self.__id = val

    def setASIC(self, val):
        self.__asic_id = val

    def send(self, timeout=30):
        status, json = self._send(self.toDict(), timeout)
        return status

    def toDict(self):
        ret = {}
        params = {}
        params["id"] = self.__id
        ret["asic-id"] = self.__asic_id
        ret["params"] = params
        ret["method"] = "cancel-packet-trace-ecmp-resolution"
        return ret

class CancelPacketTraceSendDropPacket(AgentAPI):
    def __init__(self, host, port):
        super(CancelPacketTraceSendDropPacket, self).__init__()
        self.setFeature("packettrace")
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.__drop_reason = []
        self.__port_list = []
        self.__asic_id = "1"

    def setDropReason(self, val):
        self.__drop_reason = val

    def setPortList(self, val):
        self.__port_list = val

    def setASIC(self, val):
        self.__asic_id = val

    def send(self, timeout=30):
        status, json = self._send(self.toDict(), timeout)
        return status

    def toDict(self):
        ret = {}
        params = {}
        params["drop-reason"] = self.__drop_reason
        params["port-list"] = self.__port_list
        ret["asic-id"] = self.__asic_id
        ret["params"] = params
        ret["method"] = "cancel-packet-trace-send-drop-packet"
        return ret

class CancelPacketTraceDropCounterReport(AgentAPI):
    def __init__(self, host, port):
        super(CancelPacketTraceDropCounterReport, self).__init__()
        self.setFeature("packettrace")
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.__drop_reason = []
        self.__port_list = []
        self.__asic_id = "1"

    def setDropReason(self, val):
        self.__drop_reason = val

    def setPortList(self, val):
        self.__port_list = val

    def setASIC(self, val):
        self.__asic_id = val

    def send(self, timeout=30):
        status, json = self._send(self.toDict(), timeout)
        return status

    def toDict(self):
        ret = {}
        params = {}
        params["drop-reason"] = self.__drop_reason
        params["port-list"] = self.__port_list
        ret["asic-id"] = self.__asic_id
        ret["params"] = params
        ret["method"] = "cancel-packet-trace-drop-counter-report"
        return ret

'''

Status/Reporting Requests

'''

class GetPacketTraceFeature(AgentAPI):
    def __init__(self, host, port):
        super(GetPacketTraceFeature, self).__init__()
        self.setFeature("packettrace")
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.__pt_enable = False
        self.__asic_id = "1"
        self.__json = None

    def getEnable(self):
        return self.__pt_enable

    def getASIC(self):
        return self.__asic_id

    def setASIC(self, val):
        self.__asic_id = val

    def getJSON(self):
        return self.__json

    def send(self, timeout=30):
        status, json = self._send(self.toDict(), timeout)
        if status == 200:
            self.__version = json["version"]
            res = json["result"]
            self.__json = res
            self.__pt_enable = res["packet-trace-enable"] == 1
        return status

    def toDict(self):
        ret = {}
        params = {}
        ret["asic-id"] = self.__asic_id
        ret["params"] = params
        ret["method"] = "get-packet-trace-feature"
        return ret

class GetPacketTraceLAGResolution(AgentAPI):
    def __init__(self, host, port):
        super(GetPacketTraceLAGResolution, self).__init__()
        self.setFeature("packettrace")
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.__packet = ""
        self.__port_list = []
        self.__collection_interval = 60
        self.__drop_packet = False
        self.__asic_id = "1"
        self.__json = None

    def getASIC(self):
        return self.__asic_id

    def setASIC(self, val):
        self.__asic_id = val

    def setPacket(self, val):
        self.__packet = val

    def setPortList(self, val):
        self.__port_list = val

    def setCollectionInterval(self, val):
        self.__collection_interval = val

    def setDropPacket(self, val):
        self.__drop_packet = val

    def getJSON(self):
        return self.__json

    def send(self, timeout=30):
        status, json = self._send(self.toDict(), timeout)
        rep = None
        if status == 200:
            self.__json = json["report"]
            rep = PTParser()
            rep.process(json)
        else:
            pass
        return status, rep

    def toDict(self):
        ret = {}
        params = {}
        params["packet"] = self.__packet
        params["port-list"] = self.__port_list
        params["collection-interval"] = self.__collection_interval
        params["drop-packet"] = 1 if self.__drop_packet else 0
        
        ret["asic-id"] = self.__asic_id
        ret["params"] = params
        ret["method"] = "get-packet-trace-lag-resolution"
        return ret

class GetPacketTraceECMPResolution(AgentAPI):
    def __init__(self, host, port):
        super(GetPacketTraceECMPResolution, self).__init__()
        self.setFeature("packettrace")
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.__packet = ""
        self.__port_list = []
        self.__collection_interval = 60
        self.__drop_packet = False
        self.__asic_id = "1"
        self.__json = None

    def getASIC(self):
        return self.__asic_id

    def setASIC(self, val):
        self.__asic_id = val

    def setPacket(self, val):
        self.__packet = val

    def setPortList(self, val):
        self.__port_list = val

    def setCollectionInterval(self, val):
        self.__collection_interval = val

    def setDropPacket(self, val):
        self.__drop_packet = val

    def getJSON(self):
        return self.__json

    def send(self, timeout=30):
        status, json = self._send(self.toDict(), timeout)
        rep = None
        if status == 200:
            self.__json = json["report"]
            rep = PTParser()
            rep.process(json)
        else:
            pass
        return status, rep

    def toDict(self):
        ret = {}
        params = {}
        params["packet"] = self.__packet
        params["port-list"] = self.__port_list
        params["collection-interval"] = self.__collection_interval
        params["drop-packet"] = 1 if self.__drop_packet else 0
        
        ret["asic-id"] = self.__asic_id
        ret["params"] = params
        ret["method"] = "get-packet-trace-ecmp-resolution"
        return ret

class GetPacketTraceProfile(AgentAPI):
    def __init__(self, host, port):
        super(GetPacketTraceProfile, self).__init__()
        self.setFeature("packettrace")
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.__packet = ""
        self.__port_list = []
        self.__collection_interval = 60
        self.__drop_packet = False
        self.__asic_id = "1"
        self.__json = None

    def getASIC(self):
        return self.__asic_id

    def setASIC(self, val):
        self.__asic_id = val

    def setPacket(self, val):
        self.__packet = val

    def setPortList(self, val):
        self.__port_list = val

    def setCollectionInterval(self, val):
        self.__collection_interval = val

    def setDropPacket(self, val):
        self.__drop_packet = val

    def getJSON(self):
        return self.__json

    def send(self, timeout=30):
        status, json = self._send(self.toDict(), timeout)
        rep = None
        if status == 200:
            self.__json = json["report"]
            rep = PTParser()
            rep.process(json)
        else:
            pass
        return status, rep

    def toDict(self):
        ret = {}
        params = {}
        params["packet"] = self.__packet
        params["port-list"] = self.__port_list
        params["collection-interval"] = self.__collection_interval
        params["drop-packet"] = 1 if self.__drop_packet else 0
        
        ret["asic-id"] = self.__asic_id
        ret["params"] = params
        ret["method"] = "get-packet-trace-profile"
        return ret

class GetPacketTraceDropReason(AgentAPI):
    def __init__(self, host, port):
        super(GetPacketTraceDropReason, self).__init__()
        self.setFeature("packettrace")
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.__asic_id = "1"
        self.__json = None

    def setASIC(self, val):
        self.__asic_id = val

    def getJSON(self):
        return self.__json

    def send(self, timeout=30):
        status, json = self._send(self.toDict(), timeout)
        rep = None
        if status == 200:
            self.__json = json["result"]
            rep = PTParser()
            rep.process(json)
        else:
            pass
        return status, rep

    def toDict(self):
        ret = {}
        params = {}
        ret["asic-id"] = self.__asic_id
        ret["params"] = params
        ret["method"] = "get-packet-trace-drop-reason"
        return ret

class GetPacketTraceDropCounterReport(AgentAPI):
    def __init__(self, host, port):
        super(GetPacketTraceDropCounterReport, self).__init__()
        self.setFeature("packettrace")
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.__drop_reason = []
        self.__port_list = []
        self.__asic_id = "1"
        self.__json = None

    def setDropReason(self, val):
        self.__drop_reason = val

    def setPortList(self, val):
        self.__port_list = val

    def setASIC(self, val):
        self.__asic_id = val

    def getJSON(self):
        return self.__json

    def send(self, timeout=30):
        status, json = self._send(self.toDict(), timeout)
        rep = None
        if status == 200:
            self.__json = json["report"]
            rep = PTParser()
            rep.process(json)
        else:
            pass
        return status, rep

    def toDict(self):
        ret = {}
        params = {}
        params["drop-reason"] = self.__drop_reason
        params["port-list"] = self.__port_list
        ret["asic-id"] = self.__asic_id
        ret["params"] = params
        ret["method"] = "get-packet-trace-drop-counter-report"
        return ret

class GetPacketTraceSupportedDropReasons(AgentAPI):
    def __init__(self, host, port):
        super(GetPacketTraceSupportedDropReasons, self).__init__()
        self.setFeature("packettrace")
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.__asic_id = "1"
        self.__json = None

    def setASIC(self, val):
        self.__asic_id = val

    def getJSON(self):
        return self.__json

    def send(self, timeout=30):
        status, json = self._send(self.toDict(), timeout)
        rep = None
        if status == 200:
            self.__json = json["report"]
            rep = PTParser()
            rep.process(json)
        else:
            pass
        return status, rep

    def toDict(self):
        ret = {}
        params = {}
        ret["asic-id"] = self.__asic_id
        ret["params"] = params
        ret["method"] = "get-packet-trace-supported-drop-reasons"
        return ret

class TestPTAPIParams(unittest.TestCase):

    def setUp(self):
        pass

    def test_ConfigurePacketTraceFeature(self):
        sw = BroadViewBSTSwitches()
        if len(sw):
            for x in sw:
                host = x["ip"]
                port = x["port"]
                break
        else:
            host = "192.168.3.1"
            port = 8080

        x = ConfigurePacketTraceFeature(host, port)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(x.getFeature() == "packettrace")
        self.assertTrue(x.getHttpMethod() == "POST")
        self.assertTrue(x.getHost() == host)
        self.assertTrue(x.getPort() == port)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "configure-packet-trace-feature")

        params = d["params"]
        self.assertEqual(params["packet-trace-enable"], False)

        x.setEnable(True)
        d = x.toDict()

        params = d["params"]
        self.assertEqual(params["packet-trace-enable"], True)

        x.setEnable(False)
        d = x.toDict()

        params = d["params"]
        self.assertEqual(params["packet-trace-enable"], False)

    def test_ConfigurePacketTraceDropReason(self):
        sw = BroadViewBSTSwitches()
        if len(sw):
            for x in sw:
                host = x["ip"]
                port = x["port"]
                break
        else:
            host = "192.168.3.1"
            port = 8080

        x = ConfigurePacketTraceDropReason(host, port)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(x.getFeature() == "packettrace")
        self.assertTrue(x.getHttpMethod() == "POST")
        self.assertTrue(x.getHost() == host)
        self.assertTrue(x.getPort() == port)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "configure-packet-trace-drop-reason")

        params = d["params"]
        self.assertEqual(len(params["reason"]), 0)
        self.assertEqual(len(params["port-list"]), 0)
        self.assertEqual(params["send-dropped-packet"], 0)
        self.assertEqual(params["trace-profile"], 0)
        self.assertEqual(params["packet-count"], 1)

        x.setReason(["vlan-xlate-miss-drop", "bpdu-drop", "trill-slowpath-drop" ])
        x.setPortList(["1","5","6","10-15"])
        x.setSendDroppedPacket(True)
        x.setTraceProfile(True)
        x.setPacketCount(9)
        x.setPacketThreshold(5)
        d = x.toDict()
        params = d["params"]

        self.assertTrue(len(params["reason"]) == 3)
        self.assertTrue("vlan-xlate-miss-drop" in params["reason"])
        self.assertTrue("bpdu-drop" in params["reason"])
        self.assertTrue("trill-slowpath-drop" in params["reason"])

        self.assertTrue(len(params["port-list"]) == 4)
        self.assertTrue("1" in params["port-list"])
        self.assertEqual(params["send-dropped-packet"], 1)
        self.assertEqual(params["trace-profile"], 1)
        self.assertEqual(params["packet-count"], 9)
        self.assertEqual(params["packet-threshold"], 5)

    def test_CancelPacketTraceProfile(self):
        sw = BroadViewBSTSwitches()
        if len(sw):
            for x in sw:
                host = x["ip"]
                port = x["port"]
                break
        else:
            host = "192.168.3.1"
            port = 8080

        x = CancelPacketTraceProfile(host, port)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(x.getFeature() == "packettrace")
        self.assertTrue(x.getHttpMethod() == "POST")
        self.assertTrue(x.getHost() == host)
        self.assertTrue(x.getPort() == port)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "cancel-packet-trace-profile")

        x.setId(2)
        d = x.toDict()
        params = d["params"]

        self.assertTrue(params["id"] == 2)

    def test_CancelPacketTraceLAGResolution(self):
        sw = BroadViewBSTSwitches()
        if len(sw):
            for x in sw:
                host = x["ip"]
                port = x["port"]
                break
        else:
            host = "192.168.3.1"
            port = 8080

        x = CancelPacketTraceLAGResolution(host, port)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(x.getFeature() == "packettrace")
        self.assertTrue(x.getHttpMethod() == "POST")
        self.assertTrue(x.getHost() == host)
        self.assertTrue(x.getPort() == port)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "cancel-packet-trace-lag-resolution")

        x.setId(5)
        d = x.toDict()
        params = d["params"]

        self.assertTrue(params["id"] == 5)

    def test_CancelPacketTraceECMPResolution(self):
        sw = BroadViewBSTSwitches()
        if len(sw):
            for x in sw:
                host = x["ip"]
                port = x["port"]
                break
        else:
            host = "192.168.3.1"
            port = 8080

        x = CancelPacketTraceECMPResolution(host, port)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(x.getFeature() == "packettrace")
        self.assertTrue(x.getHttpMethod() == "POST")
        self.assertTrue(x.getHost() == host)
        self.assertTrue(x.getPort() == port)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "cancel-packet-trace-ecmp-resolution")

        x.setId(17)
        d = x.toDict()
        params = d["params"]

        self.assertTrue(params["id"] == 17)

    def test_CancelPacketTraceSendDropPacket(self):
        sw = BroadViewBSTSwitches()
        if len(sw):
            for x in sw:
                host = x["ip"]
                port = x["port"]
                break
        else:
            host = "192.168.3.1"
            port = 8080

        x = CancelPacketTraceSendDropPacket(host, port)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(x.getFeature() == "packettrace")
        self.assertTrue(x.getHttpMethod() == "POST")
        self.assertTrue(x.getHost() == host)
        self.assertTrue(x.getPort() == port)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "cancel-packet-trace-send-drop-packet")

        x.setDropReason(["l2-lookup-failure", "l3-failure", "vlan-mismatch"])
        x.setPortList(["1", "11", "3", "4-10"])
        d = x.toDict()
        params = d["params"]

        self.assertTrue("l2-lookup-failure" in params["drop-reason"])
        self.assertTrue("l3-failure" in params["drop-reason"])
        self.assertTrue("vlan-mismatch" in params["drop-reason"])
        self.assertTrue(len(params["drop-reason"]) == 3)

        self.assertTrue("1" in params["port-list"])
        self.assertTrue("11" in params["port-list"])
        self.assertTrue("3" in params["port-list"])
        self.assertTrue("4-10" in params["port-list"])
        self.assertTrue(len(params["port-list"]) == 4)

    def test_CancelPacketTraceDropCounterReport(self):
        sw = BroadViewBSTSwitches()
        if len(sw):
            for x in sw:
                host = x["ip"]
                port = x["port"]
                break
        else:
            host = "192.168.3.1"
            port = 8080

        x = CancelPacketTraceDropCounterReport(host, port)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(x.getFeature() == "packettrace")
        self.assertTrue(x.getHttpMethod() == "POST")
        self.assertTrue(x.getHost() == host)
        self.assertTrue(x.getPort() == port)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "cancel-packet-trace-drop-counter-report")

        x.setDropReason(["l2-lookup-failure", "l3-failure", "vlan-mismatch"])
        x.setPortList(["1", "11", "3", "4-10"])
        d = x.toDict()
        params = d["params"]

        self.assertTrue("l2-lookup-failure" in params["drop-reason"])
        self.assertTrue("l3-failure" in params["drop-reason"])
        self.assertTrue("vlan-mismatch" in params["drop-reason"])
        self.assertTrue(len(params["drop-reason"]) == 3)

        self.assertTrue("1" in params["port-list"])
        self.assertTrue("11" in params["port-list"])
        self.assertTrue("3" in params["port-list"])
        self.assertTrue("4-10" in params["port-list"])
        self.assertTrue(len(params["port-list"]) == 4)

    def test_GetPacketTraceFeature(self):
        sw = BroadViewBSTSwitches()
        if len(sw):
            for x in sw:
                host = x["ip"]
                port = x["port"]
                break
        else:
            host = "192.168.3.1"
            port = 8080

        x = GetPacketTraceFeature(host, port)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(x.getFeature() == "packettrace")
        self.assertTrue(x.getHttpMethod() == "POST")
        self.assertTrue(x.getHost() == host)
        self.assertTrue(x.getPort() == port)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "get-packet-trace-feature")

        x.setASIC("2")
        d = x.toDict()

        self.assertEqual(d["asic-id"], "2")

    def test_GetPacketTraceLAGResolution(self):
        sw = BroadViewBSTSwitches()
        if len(sw):
            for x in sw:
                host = x["ip"]
                port = x["port"]
                break
        else:
            host = "192.168.3.1"
            port = 8080

        x = GetPacketTraceLAGResolution(host, port)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(x.getFeature() == "packettrace")
        self.assertTrue(x.getHttpMethod() == "POST")
        self.assertTrue(x.getHost() == host)
        self.assertTrue(x.getPort() == port)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "get-packet-trace-lag-resolution")
        params = d["params"]
        self.assertTrue("packet" in params)
        self.assertTrue(len(params["packet"]) == 0)
        self.assertTrue("port-list" in params)
        self.assertTrue(len(params["port-list"]) == 0)
        self.assertTrue("collection-interval" in params)
        self.assertTrue("drop-packet" in params)

        x.setPacket("100100330450001102003034040")
        x.setPortList(["1", "11", "3", "4-10"])
        x.setCollectionInterval(99)
        x.setDropPacket(False)
        d = x.toDict()
        params = d["params"]

        self.assertEqual(params["packet"], "100100330450001102003034040")
        self.assertEqual(params["collection-interval"], 99)
        self.assertEqual(params["drop-packet"], 0)

        self.assertTrue("1" in params["port-list"])
        self.assertTrue("11" in params["port-list"])
        self.assertTrue("3" in params["port-list"])
        self.assertTrue("4-10" in params["port-list"])
        self.assertTrue(len(params["port-list"]) == 4)


    def test_GetPacketTraceECMPResolution(self):
        sw = BroadViewBSTSwitches()
        if len(sw):
            for x in sw:
                host = x["ip"]
                port = x["port"]
                break
        else:
            host = "192.168.3.1"
            port = 8080

        x = GetPacketTraceECMPResolution(host, port)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(x.getFeature() == "packettrace")
        self.assertTrue(x.getHttpMethod() == "POST")
        self.assertTrue(x.getHost() == host)
        self.assertTrue(x.getPort() == port)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "get-packet-trace-ecmp-resolution")
        params = d["params"]
        self.assertTrue("packet" in params)
        self.assertTrue(len(params["packet"]) == 0)
        self.assertTrue("port-list" in params)
        self.assertTrue(len(params["port-list"]) == 0)
        self.assertTrue("collection-interval" in params)
        self.assertTrue("drop-packet" in params)

        x.setPacket("100100330450001102003034040")
        x.setPortList(["1", "11", "3", "4-10"])
        x.setCollectionInterval(99)
        x.setDropPacket(False)
        d = x.toDict()
        params = d["params"]

        self.assertEqual(params["packet"], "100100330450001102003034040")
        self.assertEqual(params["collection-interval"], 99)
        self.assertEqual(params["drop-packet"], 0)

        self.assertTrue("1" in params["port-list"])
        self.assertTrue("11" in params["port-list"])
        self.assertTrue("3" in params["port-list"])
        self.assertTrue("4-10" in params["port-list"])
        self.assertTrue(len(params["port-list"]) == 4)

    def test_GetPacketTraceProfile(self):
        sw = BroadViewBSTSwitches()
        if len(sw):
            for x in sw:
                host = x["ip"]
                port = x["port"]
                break
        else:
            host = "192.168.3.1"
            port = 8080

        x = GetPacketTraceProfile(host, port)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(x.getFeature() == "packettrace")
        self.assertTrue(x.getHttpMethod() == "POST")
        self.assertTrue(x.getHost() == host)
        self.assertTrue(x.getPort() == port)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "get-packet-trace-profile")
        params = d["params"]
        self.assertTrue("packet" in params)
        self.assertTrue(len(params["packet"]) == 0)
        self.assertTrue("port-list" in params)
        self.assertTrue(len(params["port-list"]) == 0)
        self.assertTrue("collection-interval" in params)
        self.assertTrue("drop-packet" in params)

        x.setPacket("100100330450001102003034040")
        x.setPortList(["1", "11", "3", "4-10"])
        x.setCollectionInterval(99)
        x.setDropPacket(False)
        d = x.toDict()
        params = d["params"]

        self.assertEqual(params["packet"], "100100330450001102003034040")
        self.assertEqual(params["collection-interval"], 99)
        self.assertEqual(params["drop-packet"], 0)

        self.assertTrue("1" in params["port-list"])
        self.assertTrue("11" in params["port-list"])
        self.assertTrue("3" in params["port-list"])
        self.assertTrue("4-10" in params["port-list"])
        self.assertTrue(len(params["port-list"]) == 4)


    def test_GetPacketTraceDropReason(self):
        sw = BroadViewBSTSwitches()
        if len(sw):
            for x in sw:
                host = x["ip"]
                port = x["port"]
                break
        else:
            host = "192.168.3.1"
            port = 8080

        x = GetPacketTraceDropReason(host, port)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(x.getFeature() == "packettrace")
        self.assertTrue(x.getHttpMethod() == "POST")
        self.assertTrue(x.getHost() == host)
        self.assertTrue(x.getPort() == port)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "get-packet-trace-drop-reason")

        x.setASIC("3")
        d = x.toDict()

        self.assertEqual(d["asic-id"], "3")

    def test_GetPacketTraceDropCounterReport(self):
        sw = BroadViewBSTSwitches()
        if len(sw):
            for x in sw:
                host = x["ip"]
                port = x["port"]
                break
        else:
            host = "192.168.3.1"
            port = 8080

        x = GetPacketTraceDropCounterReport(host, port)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(x.getFeature() == "packettrace")
        self.assertTrue(x.getHttpMethod() == "POST")
        self.assertTrue(x.getHost() == host)
        self.assertTrue(x.getPort() == port)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "get-packet-trace-drop-counter-report")
        params = d["params"]
        self.assertTrue("drop-reason" in params)
        self.assertTrue(len(params["drop-reason"]) == 0)
        self.assertTrue("port-list" in params)
        self.assertTrue(len(params["port-list"]) == 0)

        x.setPortList(["1", "11", "3", "4-10"])
        x.setDropReason(["vlan-xlate-miss-drop" , "bpdu-drop", "trill-slowpath-drop"])
        d = x.toDict()
        params = d["params"]

        self.assertTrue("1" in params["port-list"])
        self.assertTrue("11" in params["port-list"])
        self.assertTrue("3" in params["port-list"])
        self.assertTrue("4-10" in params["port-list"])
        self.assertTrue(len(params["port-list"]) == 4)

        self.assertTrue("vlan-xlate-miss-drop" in params["drop-reason"])
        self.assertTrue("bpdu-drop" in params["drop-reason"])
        self.assertTrue("trill-slowpath-drop" in params["drop-reason"])
        self.assertTrue(len(params["drop-reason"]) == 3)

    def test_GetPacketTraceSupportedDropReasons(self):
        sw = BroadViewBSTSwitches()
        if len(sw):
            for x in sw:
                host = x["ip"]
                port = x["port"]
                break
        else:
            host = "192.168.3.1"
            port = 8080

        x = GetPacketTraceSupportedDropReasons(host, port)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(x.getFeature() == "packettrace")
        self.assertTrue(x.getHttpMethod() == "POST")
        self.assertTrue(x.getHost() == host)
        self.assertTrue(x.getPort() == port)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "get-packet-trace-supported-drop-reasons")

if __name__ == "__main__":
    unittest.main()
