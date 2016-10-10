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
from broadview_lib.bhd.bhd_parser import BHDParser
from broadview_lib.config.broadviewconfig import BroadViewBSTSwitches
import unittest

class BlackHoleDetectionEnable(AgentAPI):
    def __init__(self, host, port):
        super(BlackHoleDetectionEnable, self).__init__()
        self.setFeature("black-hole-detection")
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.__black_hole_detection_enable = False
        self.__asic_id = "1"

    def setEnable(self, val):
        self.__black_hole_detection_enable = val

    def setASIC(self, val):
        self.__asic_id = val

    def send(self, timeout=30):
        status, json = self._send(self.toDict(), timeout)
        return status


    def toDict(self):
        ret = {}
        params = {}
        params["enable"] = 1 if self.__black_hole_detection_enable else 0 
        ret["asic-id"] = self.__asic_id
        ret["params"] = params
        ret["method"] = "configure-black-hole-detection-enable"
        return ret

class ConfigureBlackHole(AgentAPI):
    def __init__(self, host, port):
        super(ConfigureBlackHole, self).__init__()
        self.setFeature("black-hole-detection")
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.__port_list = []
        self.__sampling_method = "agent"
        self.__water_mark = 200
        self.__sample_periodicity = 15
        self.__sample_count = 10
        self.__vlan_id = 1
        self.__destination_ip = None
        self.__source_udp_port = None
        self.__destination_udp_port = None
        self.__mirror_port = None
        self.__sample_pool_size = None
        self.__asic_id = "1"

    def setPortList(self, val):
        self.__port_list = val

    def setSamplingMethod(self, val):
        self.__sampling_method = val

    def setWaterMark(self, val):
        self.__water_mark = val

    def setSamplePeriodicity(self, val):
        self.__sample_periodicity = val

    def setSampleCount(self, val):
        self.__sample_count = val

    def setVLANId(self, val):
        self.__vlan_id = val

    def setDestinationIP(self, val):
        self.__destination_ip = val

    def setSourceUDPPort(self, val):
        self.__source_udp_port = val

    def setDestinationUDPPort(self, val):
        self.__destination_udp_port = val

    def setMirrorPort(self, val):
        self.__mirror_port = val

    def setSamplePoolSize(self, val):
        self.__sample_pool_size = val

    def setASIC(self, val):
        self.__asic_id = val

    def send(self, timeout=30):
        status, json = self._send(self.toDict(), timeout)
        return status

    def toDict(self):
        ret = {}
        params = {}
        params["port-list"] = self.__port_list
        params["sampling-method"] = self.__sampling_method
        params["sampling-params"] = {}
        if self.__sampling_method == "agent":
            params["sampling-params"]["water-mark"] = self.__water_mark
            params["sampling-params"]["sample-periodicity"] = self.__sample_periodicity
            params["sampling-params"]["sample-count"] = self.__sample_count
        else:
            params["sampling-params"]["encapsulation-params"] = {}
            params["sampling-params"]["encapsulation-params"]["vlan-id"] = self.__vlan_id
            params["sampling-params"]["encapsulation-params"]["destination-ip"] = self.__destination_ip
            params["sampling-params"]["encapsulation-params"]["source-udp-port"] = self.__source_udp_port
            params["sampling-params"]["encapsulation-params"]["destination-udp-port"] = self.__destination_udp_port
            params["sampling-params"]["mirror-port"] = self.__mirror_port
            params["sampling-params"]["sample-pool-size"] = self.__sample_pool_size
        ret["asic-id"] = self.__asic_id
        ret["params"] = params
        ret["method"] = "configure-black-hole"
        return ret

class CancelBlackHole(AgentAPI):
    def __init__(self, host, port):
        super(CancelBlackHole, self).__init__()
        self.setFeature("black-hole-detection")
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
        ret["method"] = "cancel-black-hole"
        return ret

'''

Status/Reporting Requests

'''

class GetBlackHoleDetectionEnable(AgentAPI):
    def __init__(self, host, port):
        super(GetBlackHoleDetectionEnable, self).__init__()
        self.setFeature("black-hole-detection")
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.__enable = False
        self.__asic_id = "1"
        self.__json = None

    def getEnable(self):
        return self.__bhd_enable

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
            self.__enable = res["enable"] == 1
        return status

    def toDict(self):
        ret = {}
        params = {}
        params["enable"] = 1 if self.__enable == True else 0 
        ret["asic-id"] = self.__asic_id
        ret["params"] = params
        ret["method"] = "get-black-hole-detection-enable"
        return ret

class GetBlackHole(AgentAPI):
    def __init__(self, host, port):
        super(GetBlackHole, self).__init__()
        self.setFeature("black-hole-detection")
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.__asic_id = "1"
        self.__json = None

    def getASIC(self):
        return self.__asic_id

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
        return status, rep

    def toDict(self):
        ret = {}
        params = {}
        
        ret["asic-id"] = self.__asic_id
        ret["params"] = params
        ret["method"] = "get-black-hole"
        return ret

class GetSFlowSamplingStatus(AgentAPI):
    def __init__(self, host, port):
        super(GetSFlowSamplingStatus, self).__init__()
        self.setFeature("black-hole-detection")
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.__port_list = []
        self.__asic_id = "1"
        self.__json = None

    def getASIC(self):
        return self.__asic_id

    def setASIC(self, val):
        self.__asic_id = val

    def setPortList(self, val):
        self.__port_list = val

    def getJSON(self):
        return self.__json

    def send(self, timeout=30):
        status, json = self._send(self.toDict(), timeout)
        rep = None
        if status == 200:
            self.__json = json["report"]
            rep = PTParser()
            rep.process(json)
        return status, rep

    def toDict(self):
        ret = {}
        params = {}
        params["port-list"] = self.__port_list
        
        ret["asic-id"] = self.__asic_id
        ret["params"] = params
        ret["method"] = "get-sflow-sampling-status"
        return ret

class TestBHDAPIParams(unittest.TestCase):

    def setUp(self):
        pass

    def test_BlackHoleDetectionEnable(self):
        sw = BroadViewBSTSwitches()
        if len(sw):
            for x in sw:
                host = x["ip"]
                port = x["port"]
                break
        else:
            host = "192.168.3.1"
            port = 8080

        x = BlackHoleDetectionEnable(host, port)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(x.getFeature() == "black-hole-detection")
        self.assertTrue(x.getHttpMethod() == "POST")
        self.assertTrue(x.getHost() == host)
        self.assertTrue(x.getPort() == port)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "black-hole-detection-enable")

        params = d["params"]
        self.assertEqual(params["enable"], False)

        x.setEnable(True)
        d = x.toDict()

        params = d["params"]
        self.assertEqual(params["enable"], True)

        x.setEnable(False)
        d = x.toDict()

        params = d["params"]
        self.assertEqual(params["enable"], False)

    def test_ConfigureBlackHole(self):
        sw = BroadViewBSTSwitches()
        if len(sw):
            for x in sw:
                host = x["ip"]
                port = x["port"]
                break
        else:
            host = "192.168.3.1"
            port = 8080

        x = ConfigureBlackHole(host, port)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(x.getFeature() == "black-hole-detection")
        self.assertTrue(x.getHttpMethod() == "POST")
        self.assertTrue(x.getHost() == host)
        self.assertTrue(x.getPort() == port)

        params = d["params"]
        samplingParams = params["sampling-params"]
        self.assertTrue(d["asic-id"] == "1")
        self.assertEqual(len(params["port-list"]), 0)
        self.assertEqual(params["sampling-method"], "agent")
        self.assertTrue(samplingParams["water-mark"] == 200)
        self.assertTrue(samplingParams["sample-periodicity"] == 15)
        self.assertTrue(samplingParams["sample-count"] == 10)

        x.setSamplingMethod("agent")
        x.setPortList(["1","5","6","10-15"])
        x.setWaterMark(500)
        x.setSamplePeriodicity(25)
        x.setSampleCount(50)
        x.setVLANId(4000)
        x.setDestinationIP("10.0.0.4")
        x.setSourceUDPPort(1234)
        x.setDestinationUDPPort(5678)
        x.setMirrorPort(8)
        x.setSamplePoolSize(5)
        d = x.toDict()
        params = d["params"]
        samplingParams = params["sampling-params"]

        self.assertEqual(params["sampling-method"], "agent")
        self.assertTrue("port-list" in params)
        self.assertTrue("water-mark" in samplingParams)
        self.assertTrue("sample-periodicity" in samplingParams)
        self.assertTrue("sample-count" in samplingParams)
        self.assertTrue(not "vlan-id" in samplingParams)
        self.assertTrue(not "destination-ip" in samplingParams)
        self.assertTrue(not "source-udp-port" in samplingParams)
        self.assertTrue(not "destination-udp-port" in samplingParams)
        self.assertTrue(not "mirror-port" in samplingParams)
        self.assertTrue(not "sample-pool-size" in samplingParams)

        self.assertTrue(samplingParams["water-mark"] == 500)
        self.assertTrue(samplingParams["sample-periodicity"] == 25)
        self.assertTrue(samplingParams["sample-count"] == 50)
        self.assertTrue(len(params["port-list"]) == 4)
        self.assertTrue("1" in params["port-list"])
        self.assertTrue("5" in params["port-list"])
        self.assertTrue("6" in params["port-list"])
        self.assertTrue("10-15" in params["port-list"])

        x.setSamplingMethod("sflow")
        d = x.toDict()
        params = d["params"]
        samplingParams = params["sampling-params"]
        encapsulationParams = samplingParams["encapsulation-params"]

        self.assertEqual(params["sampling-method"], "sflow")
        self.assertTrue("port-list" in params)
        self.assertTrue(not "water-mark" in samplingParams)
        self.assertTrue(not "sample-periodicity" in samplingParams)
        self.assertTrue(not "sample-count" in samplingParams)
        self.assertTrue("vlan-id" in encapsulationParams)
        self.assertTrue("destination-ip" in encapsulationParams)
        self.assertTrue("source-udp-port" in encapsulationParams)
        self.assertTrue("destination-udp-port" in encapsulationParams)
        self.assertTrue("mirror-port" in samplingParams)
        self.assertTrue("sample-pool-size" in samplingParams)

        self.assertTrue(encapsulationParams["vlan-id"] == 4000)
        self.assertTrue(encapsulationParams["destination-ip"] == "10.0.0.4")
        self.assertTrue(encapsulationParams["source-udp-port"] == 1234)
        self.assertTrue(encapsulationParams["destination-udp-port"] == 5678)
        self.assertTrue(samplingParams["mirror-port"] == 8)
        self.assertTrue(samplingParams["sample-pool-size"] == 5)
        self.assertTrue(len(params["port-list"]) == 4)
        self.assertTrue("1" in params["port-list"])
        self.assertTrue("5" in params["port-list"])
        self.assertTrue("6" in params["port-list"])
        self.assertTrue("10-15" in params["port-list"])

    def test_CancelBlackHole(self):
        sw = BroadViewBSTSwitches()
        if len(sw):
            for x in sw:
                host = x["ip"]
                port = x["port"]
                break
        else:
            host = "192.168.3.1"
            port = 8080

        x = CancelBlackHole(host, port)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(x.getFeature() == "black-hole-detection")
        self.assertTrue(x.getHttpMethod() == "POST")
        self.assertTrue(x.getHost() == host)
        self.assertTrue(x.getPort() == port)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "cancel-black-hole")

    def test_GetBlackHoleDetectionEnable(self):
        sw = BroadViewBSTSwitches()
        if len(sw):
            for x in sw:
                host = x["ip"]
                port = x["port"]
                break
        else:
            host = "192.168.3.1"
            port = 8080

        x = GetBlackHoleDetectionEnable(host, port)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(x.getFeature() == "black-hole-detection")
        self.assertTrue(x.getHttpMethod() == "POST")
        self.assertTrue(x.getHost() == host)
        self.assertTrue(x.getPort() == port)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "get-black-hole-detection-enable")

    def test_GetBlackHole(self):
        sw = BroadViewBSTSwitches()
        if len(sw):
            for x in sw:
                host = x["ip"]
                port = x["port"]
                break
        else:
            host = "192.168.3.1"
            port = 8080

        x = GetBlackHole(host, port)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(x.getFeature() == "black-hole-detection")
        self.assertTrue(x.getHttpMethod() == "POST")
        self.assertTrue(x.getHost() == host)
        self.assertTrue(x.getPort() == port)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "get-black-hole")

    def test_GetSFlowSamplingStatus(self):
        sw = BroadViewBSTSwitches()
        if len(sw):
            for x in sw:
                host = x["ip"]
                port = x["port"]
                break
        else:
            host = "192.168.3.1"
            port = 8080

        x = GetSFlowSamplingStatus(host, port)
        d = x.toDict()
        self.assertTrue("asic-id" in d)
        self.assertTrue("params" in d)
        self.assertTrue("method" in d)
        self.assertTrue(x.getFeature() == "black-hole-detection")
        self.assertTrue(x.getHttpMethod() == "POST")
        self.assertTrue(x.getHost() == host)
        self.assertTrue(x.getPort() == port)
        self.assertTrue(d["asic-id"] == "1")
        self.assertTrue(d["method"] == "get-sflow-sampling-status")
        params = d["params"]
        self.assertTrue("port-list" in params)
        self.assertTrue(len(params["port-list"]) == 0)

        x.setPortList(["1", "11", "3", "4-10"])
        d = x.toDict()
        params = d["params"]

        self.assertTrue("1" in params["port-list"])
        self.assertTrue("11" in params["port-list"])
        self.assertTrue("3" in params["port-list"])
        self.assertTrue("4-10" in params["port-list"])
        self.assertTrue(len(params["port-list"]) == 4)

if __name__ == "__main__":
    unittest.main()
