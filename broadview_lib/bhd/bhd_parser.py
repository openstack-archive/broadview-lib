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

import black_hole_event_report
import sflow_sampling_status
import black_hole
import time
import unittest

class ReportTypes:
    BlackHole, BlackHoleEventReport, SFlowSamplingStatus = range(3) 

class BHDParser():
    def __init__(self):
        self.__reportType = None
        self.__black_hole = None
        self.__black_hole_event_report = None
        self.__sflow_sampling_status = []

        self.__reportHandlers = [self._handleBlackHole,
                                 self._handleBlackHoleEventReport,
                                 self._handleSFlowSamplingStatus]

    def getReportType(self):
        return self.__reportType

    def getASICId(self):
        return self.__asicId;

    def getTimestamp(self):
        return self.__timestamp;

    def __repr__(self):
        return "BHD"

    def dispatchReportParser(self, report):
        ret = True
        if report["realm"] in self.__handlers:
            try:
                self.__handlers[report["realm"]](report["data"])
            except:
                ret = False
        else:
            ret = False
        return ret

    def _handleBlackHoleEventReport(self, data):
        ret = True
        try:
            report = data["report"]
        except:
            ret = False
            report = None
        if ret:
            t = black_hole_event_report.BlackHoleEventReport()
            ret = t.parse(report)
            if ret:
                self.__black_hole_event_report = t

        return ret

    def getBlackHoleEventReport(self):
        return self.__black_hole_event_report

    def _handleSFlowSamplingStatus(self, data):
        ret = True
        try:
            report = data["report"]
        except:
            ret = False
        if ret:
            t = sflow_sampling_status.SFlowSamplingStatus()
            ret = t.parse(report)
            if ret:
                self.__sflow_sampling_status = t

        return ret

    def getSFlowSamplingStatus(self):
        return self.__sflow_sampling_status

    def _handleBlackHole(self, data):
        ret = True
        try:
            report = data["result"]
        except:
            report = []
            ret = False

        if ret:
            t = black_hole.BlackHole()
            ret = t.parse(report)
            if ret:
                self.__black_hole = t

        return ret

    def getBlackHole(self):
        return self.__black_hole

    def process(self, data):
        ret = True
        if self.valid(data):
            if data["method"] == "get-black-hole":
                self.__reportType = ReportTypes.BlackHole
            elif data["method"] == "get-black-hole-event-report":
                self.__reportType = ReportTypes.BlackHoleEventReport
            elif data["method"] == "get-sflow-sampling-status":
                self.__reportType = ReportTypes.SFlowSamplingStatus
            else:
                ret = False 

            if ret:
                self.__asicId = data["asic-id"]
                if "time-stamp" in data:
                    x = data["time-stamp"].strip()
                    try:
                        self.__timestamp = time.strptime(x, "%Y-%m-%d - %H:%M:%S")
                    except:
                        ret = False

                if ret:
                    if self.__reportType in range(len(self.__reportHandlers)): 
                        ret = self.__reportHandlers[self.__reportType](data)
                    else:
                        ret = False
        else:
            ret = False
        return ret

    def valid(self, data):
        ret = True
        keys  = ["jsonrpc", "method", 
                 "asic-id", "version",
                 "time-stamp"]

        if ret and "method" in data:
            data["method"] = data["method"].strip()
            if data["method"] != "get-black-hole" and \
               data["method"] != "get-black-hole-event-report" and \
               data["method"] != "get-sflow-sampling-status":
                ret = False
        else:
            ret = False

        if ret:
            for x in keys:
                if not x in data:
                    if x == "time-stamp":
                        if data["method"] == "get-black-hole":
                            continue
                    ret = False
                    break

        if ret:
            if not "report" in data and not "result" in data:
                ret = False # must contain a result or report

        return ret

class TestParser(unittest.TestCase):

    def setUp(self):

        self.get_black_hole_agent_1 = {
            "jsonrpc": "2.0",
            "asic-id": "1",
            "method": "get-black-hole",
            "version": "2",
            "result": {
                "port-list": ["1", "2", "3", "4"],
                "sampling-method": "agent",
                "sampling-params": {
                    "water-mark": 200,
                    "sample-periodicity": 15,
                    "sample-count": 10
                }
            },
            "id": 1
        }

        self.get_black_hole_agent_missing_method = {
            "jsonrpc": "2.0",
            "asic-id": "1",
            "version": "2",
            "result": {
                "port-list": ["1", "2", "3", "4"],
                "sampling-method": "agent",
                "sampling-params": {
                    "water-mark": 200,
                    "sample-periodicity": 15,
                    "sample-count": 10
                }
            },
            "id": 1
        }

        self.get_black_hole_agent_invalid_method = {
            "jsonrpc": "2.0",
            "method": "get-black-hole-in-one",
            "asic-id": "1",
            "version": "2",
            "result": {
                "port-list": ["1", "2", "3", "4"],
                "sampling-method": "agent",
                "sampling-params": {
                    "water-mark": 200,
                    "sample-periodicity": 15,
                    "sample-count": 10
                }
            },
            "id": 1
        }

        self.get_black_hole_agent_missing_asic = {
            "jsonrpc": "2.0",
            "method": "get-black-hole",
            "version": "2",
            "result": {
                "port-list": ["1", "2", "3", "4"],
                "sampling-method": "agent",
                "sampling-params": {
                    "water-mark": 200,
                    "sample-periodicity": 15,
                    "sample-count": 10
                }
            },
            "id": 1
        }

        self.get_black_hole_agent_missing_result = {
            "jsonrpc": "2.0",
            "method": "get-black-hole",
            "asic-id": "1",
            "version": "2",
            "id": 1
        }

        self.get_black_hole_agent_empty_result = {
            "jsonrpc": "2.0",
            "method": "get-black-hole",
            "asic-id": "1",
            "version": "2",
            "result": {
            },
            "id": 1
        }

        self.get_black_hole_agent_result_array = {
            "jsonrpc": "2.0",
            "method": "get-black-hole",
            "asic-id": "1",
            "version": "2",
            "result": [
            ],
            "id": 1
        }

        self.get_black_hole_agent_missing_port_list = {
            "jsonrpc": "2.0",
            "method": "get-black-hole",
            "asic-id": "1",
            "version": "2",
            "result": {
                "sampling-method": "agent",
                "sampling-params": {
                    "water-mark": 200,
                    "sample-periodicity": 15,
                    "sample-count": 10
                }
            },
            "id": 1
        }

        self.get_black_hole_agent_missing_sampling_method = {
            "jsonrpc": "2.0",
            "method": "get-black-hole",
            "asic-id": "1",
            "version": "2",
            "result": {
                "port-list": ["1", "2", "3", "4"],
                "sampling-params": {
                    "water-mark": 200,
                    "sample-periodicity": 15,
                    "sample-count": 10
                }
            },
            "id": 1
        }

        self.get_black_hole_agent_invalid_sampling_method = {
            "jsonrpc": "2.0",
            "method": "get-black-hole",
            "asic-id": "1",
            "version": "2",
            "result": {
                "port-list": ["1", "2", "3", "4"],
                "sampling-method": "ice-cream",
                "sampling-params": {
                    "water-mark": 200,
                    "sample-periodicity": 15,
                    "sample-count": 10
                }
            },
            "id": 1
        }

        self.get_black_hole_agent_missing_sampling_params = {
            "jsonrpc": "2.0",
            "method": "get-black-hole",
            "asic-id": "1",
            "version": "2",
            "result": {
                "port-list": ["1", "2", "3", "4"],
                "sampling-method": "agent"
            },
            "id": 1
        }

        self.get_black_hole_agent_missing_water_mark = {
            "jsonrpc": "2.0",
            "method": "get-black-hole",
            "asic-id": "1",
            "version": "2",
            "result": {
                "port-list": ["1", "2", "3", "4"],
                "sampling-method": "agent",
                "sampling-params": {
                    "sample-periodicity": 15,
                    "sample-count": 10
                }
            },
            "id": 1
        }

        self.get_black_hole_agent_missing_sample_periodicity = {
            "jsonrpc": "2.0",
            "method": "get-black-hole",
            "asic-id": "1",
            "version": "2",
            "result": {
                "port-list": ["1", "2", "3", "4"],
                "sampling-method": "agent",
                "sampling-params": {
                    "water-mark": 200,
                    "sample-count": 10
                }
            },
            "id": 1
        }

        self.get_black_hole_agent_missing_sample_count = {
            "jsonrpc": "2.0",
            "method": "get-black-hole",
            "asic-id": "1",
            "version": "2",
            "result": {
                "port-list": ["1", "2", "3", "4"],
                "sampling-method": "agent",
                "sampling-params": {
                    "water-mark": 200,
                    "sample-periodicity": 15,
                }
            },
            "id": 1
        }

        self.get_black_hole_sflow_1 = {
            "jsonrpc": "2.0",
            "method": "get-black-hole",
            "asic-id": "1",
            "version": "2",
            "result": {
                "port-list": ["1", "2", "3", "4"],
                "sampling-method": "sflow",
                "sampling-params": {
                    "encapsulation-params": {
                        "vlan-id": 1,
                        "destination-ip": "1.1.1.1",
                        "source-udp-port": 1234,
                        "destination-udp-port": 4321
                    },
                    "mirror-port": "10",
                    "sample-pool-size": 1
                }
            },
            "id": 1
        }

        self.get_black_hole_sflow_missing_method = {
            "jsonrpc": "2.0",
            "asic-id": "1",
            "version": "2",
            "result": {
                "port-list": ["1", "2", "3", "4"],
                "sampling-method": "sflow",
                "sampling-params": {
                    "encapsulation-params": {
                        "vlan-id": 1,
                        "destination-ip": "1.1.1.1",
                        "source-udp-port": 1234,
                        "destination-udp-port": 4321
                    },
                    "mirror-port": "10",
                    "sample-pool-size": 1
                }
            },
            "id": 1
        }

        self.get_black_hole_sflow_invalid_method = {
            "jsonrpc": "2.0",
            "method": "get-black-hole-abcd",
            "asic-id": "1",
            "version": "2",
            "result": {
                "port-list": ["1", "2", "3", "4"],
                "sampling-method": "sflow",
                "sampling-params": {
                    "encapsulation-params": {
                        "vlan-id": 1,
                        "destination-ip": "1.1.1.1",
                        "source-udp-port": 1234,
                        "destination-udp-port": 4321
                    },
                    "mirror-port": "10",
                    "sample-pool-size": 1
                }
            },
            "id": 1
        }

        self.get_black_hole_sflow_missing_asic = {
            "jsonrpc": "2.0",
            "method": "get-black-hole",
            "version": "2",
            "result": {
                "port-list": ["1", "2", "3", "4"],
                "sampling-method": "sflow",
                "sampling-params": {
                    "encapsulation-params": {
                        "vlan-id": 1,
                        "destination-ip": "1.1.1.1",
                        "source-udp-port": 1234,
                        "destination-udp-port": 4321
                    },
                    "mirror-port": "10",
                    "sample-pool-size": 1
                }
            },
            "id": 1
        }

        self.get_black_hole_sflow_missing_result = {
            "jsonrpc": "2.0",
            "method": "get-black-hole",
            "asic-id": "1",
            "version": "2",
            "id": 1
        }

        self.get_black_hole_sflow_empty_result = {
            "jsonrpc": "2.0",
            "method": "get-black-hole",
            "asic-id": "1",
            "version": "2",
            "result": {
            },
            "id": 1
        }

        self.get_black_hole_sflow_result_array = {
            "jsonrpc": "2.0",
            "method": "get-black-hole",
            "asic-id": "1",
            "version": "2",
            "result": [
            ],
            "id": 1
        }

        self.get_black_hole_sflow_missing_sampling_method = {
            "jsonrpc": "2.0",
            "method": "get-black-hole",
            "asic-id": "1",
            "version": "2",
            "result": {
                "port-list": ["1", "2", "3", "4"],
                "sampling-params": {
                    "encapsulation-params": {
                        "vlan-id": 1,
                        "destination-ip": "1.1.1.1",
                        "source-udp-port": 1234,
                        "destination-udp-port": 4321
                    },
                    "mirror-port": "10",
                    "sample-pool-size": 1
                }
            },
            "id": 1
        }

        self.get_black_hole_sflow_invalid_sampling_method = {
            "jsonrpc": "2.0",
            "method": "get-black-hole",
            "asic-id": "1",
            "version": "2",
            "result": {
                "port-list": ["1", "2", "3", "4"],
                "sampling-method": "sflow-invalid",
                "sampling-params": {
                    "encapsulation-params": {
                        "vlan-id": 1,
                        "destination-ip": "1.1.1.1",
                        "source-udp-port": 1234,
                        "destination-udp-port": 4321
                    },
                    "mirror-port": "10",
                    "sample-pool-size": 1
                }
            },
            "id": 1
        }

        self.get_black_hole_sflow_missing_sampling_params = {
            "jsonrpc": "2.0",
            "method": "get-black-hole",
            "asic-id": "1",
            "version": "2",
            "result": {
                "port-list": ["1", "2", "3", "4"],
                "sampling-method": "sflow",
                "mirror-port": "10",
                "sample-pool-size": 1
            },
            "id": 1
        }

        self.get_black_hole_sflow_invalid_sampling_method = {
            "jsonrpc": "2.0",
            "method": "get-black-hole",
            "asic-id": "1",
            "version": "2",
            "result": {
                "port-list": ["1", "2", "3", "4"],
                "sampling-method": "sflow-invalid",
                "sampling-params": {
                    "encapsulation-params": {
                        "vlan-id": 1,
                        "destination-ip": "1.1.1.1",
                        "source-udp-port": 1234,
                        "destination-udp-port": 4321
                    },
                    "mirror-port": "10",
                    "sample-pool-size": 1
                }
            },
            "id": 1
        }

        self.get_black_hole_sflow_missing_encap_params = {
            "jsonrpc": "2.0",
            "method": "get-black-hole",
            "asic-id": "1",
            "version": "2",
            "result": {
                "port-list": ["1", "2", "3", "4"],
                "sampling-method": "sflow-invalid",
                "sampling-params": {
                    "mirror-port": "10",
                    "sample-pool-size": 1
                }
            },
            "id": 1
        }

        self.get_black_hole_sflow_missing_vlan_id = {
            "jsonrpc": "2.0",
            "method": "get-black-hole",
            "asic-id": "1",
            "version": "2",
            "result": {
                "port-list": ["1", "2", "3", "4"],
                "sampling-method": "sflow-invalid",
                "sampling-params": {
                    "encapsulation-params": {
                        "destination-ip": "1.1.1.1",
                        "source-udp-port": 1234,
                        "destination-udp-port": 4321
                    },
                    "mirror-port": "10",
                    "sample-pool-size": 1
                }
            },
            "id": 1
        }

        self.get_black_hole_sflow_missing_destination_ip = {
            "jsonrpc": "2.0",
            "method": "get-black-hole",
            "asic-id": "1",
            "version": "2",
            "result": {
                "port-list": ["1", "2", "3", "4"],
                "sampling-method": "sflow-invalid",
                "sampling-params": {
                    "encapsulation-params": {
                        "vlan-id": 1,
                        "source-udp-port": 1234,
                        "destination-udp-port": 4321
                    },
                    "mirror-port": "10",
                    "sample-pool-size": 1
                }
            },
            "id": 1
        }

        self.get_black_hole_sflow_missing_src_udp = {
            "jsonrpc": "2.0",
            "method": "get-black-hole",
            "asic-id": "1",
            "version": "2",
            "result": {
                "port-list": ["1", "2", "3", "4"],
                "sampling-method": "sflow-invalid",
                "sampling-params": {
                    "encapsulation-params": {
                        "vlan-id": 1,
                        "destination-ip": "1.1.1.1",
                        "destination-udp-port": 4321
                    },
                    "mirror-port": "10",
                    "sample-pool-size": 1
                }
            },
            "id": 1
        }

        self.get_black_hole_sflow_missing_dst_udp = {
            "jsonrpc": "2.0",
            "method": "get-black-hole",
            "asic-id": "1",
            "version": "2",
            "result": {
                "port-list": ["1", "2", "3", "4"],
                "sampling-method": "sflow-invalid",
                "sampling-params": {
                    "encapsulation-params": {
                        "vlan-id": 1,
                        "destination-ip": "1.1.1.1",
                        "source-udp-port": 1234,
                    },
                    "mirror-port": "10",
                    "sample-pool-size": 1
                }
            },
            "id": 1
        }

        self.get_black_hole_sflow_missing_mirror_port = {
            "jsonrpc": "2.0",
            "method": "get-black-hole",
            "asic-id": "1",
            "version": "2",
            "result": {
                "port-list": ["1", "2", "3", "4"],
                "sampling-method": "sflow-invalid",
                "sampling-params": {
                    "encapsulation-params": {
                        "vlan-id": 1,
                        "destination-ip": "1.1.1.1",
                        "source-udp-port": 1234,
                        "destination-udp-port": 4321
                    },
                    "sample-pool-size": 1
                }
            },
            "id": 1
        }

        self.get_black_hole_sflow_missing_sample_pool_size = {
            "jsonrpc": "2.0",
            "method": "get-black-hole",
            "asic-id": "1",
            "version": "2",
            "result": {
                "port-list": ["1", "2", "3", "4"],
                "sampling-method": "sflow-invalid",
                "sampling-params": {
                    "encapsulation-params": {
                        "vlan-id": 1,
                        "destination-ip": "1.1.1.1",
                        "source-udp-port": 1234,
                        "destination-udp-port": 4321
                    },
                    "mirror-port": "10",
                }
            },
            "id": 1
        }

        self.get_black_hole_event_report_1 = {
            "jsonrpc": "2.0",
            "method": "get-black-hole-event-report",
            "asic-id": "1", 
            "version": "2",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "report": {
                "ingress-port": "1",
                "egress-port-list": ["2",  "3"],
                "black-holed-packet-count": 100,
                "sample-packet": "0010203232.."
            }
        }

        self.get_black_hole_event_report_missing_method = {
            "jsonrpc": "2.0",
            "asic-id": "1",
            "version": "2",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "report": {
                "ingress-port": "1",
                "egress-port-list": ["2",  "3"],
                "black-holed-packet-count": 100,
                "sample-packet": "0010203232.."
            }
        }

        self.get_black_hole_event_report_invalid_method = {
            "jsonrpc": "2.0",
            "method": "get-black-hole-event-report-blah",
            "asic-id": "1",
            "version": "2",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "report": {
                "ingress-port": "1",
                "egress-port-list": ["2",  "3"],
                "black-holed-packet-count": 100,
                "sample-packet": "0010203232.."
            }
        }

        self.get_black_hole_event_report_missing_asic = {
            "jsonrpc": "2.0",
            "method": "get-black-hole-event-report",
            "version": "2",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "report": {
                "ingress-port": "1",
                "egress-port-list": ["2",  "3"],
                "black-holed-packet-count": 100,
                "sample-packet": "0010203232.."
            }
        }

        self.get_black_hole_event_report_missing_result = {
            "jsonrpc": "2.0",
            "method": "get-black-hole-event-report",
            "asic-id": "1",
            "version": "2",
            "time-stamp": "2014-11-18 - 00:15:04 ",
        }

        self.get_black_hole_event_report_empty_result = {
            "jsonrpc": "2.0",
            "method": "get-black-hole-event-report",
            "asic-id": "1",
            "version": "2",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "report": {
            }
        }

        self.get_black_hole_event_report_result_array = {
            "jsonrpc": "2.0",
            "method": "get-black-hole-event-report",
            "asic-id": "1",
            "version": "2",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "report": [
            ]
        }

        self.get_black_hole_event_report_missing_timestamp = {
            "jsonrpc": "2.0",
            "method": "get-black-hole-event-report",
            "asic-id": "1",
            "version": "2",
            "report": {
                "ingress-port": "1",
                "egress-port-list": ["2",  "3"],
                "black-holed-packet-count": 100,
                "sample-packet": "0010203232.."
            }
        }

        self.get_black_hole_event_report_missing_ingress_port = {
            "jsonrpc": "2.0",
            "method": "get-black-hole-event-report",
            "asic-id": "1",
            "version": "2",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "report": {
                "egress-port-list": ["2",  "3"],
                "black-holed-packet-count": 100,
                "sample-packet": "0010203232.."
            }
        }

        self.get_black_hole_event_report_missing_egress_port_list = {
            "jsonrpc": "2.0",
            "method": "get-black-hole-event-report",
            "asic-id": "1",
            "version": "2",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "report": {
                "ingress-port": "1",
                "black-holed-packet-count": 100,
                "sample-packet": "0010203232.."
            }
        }

        self.get_black_hole_event_report_missing_bhpc = {
            "jsonrpc": "2.0",
            "method": "get-black-hole-event-report",
            "asic-id": "1", 
            "version": "2",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "report": {
                "ingress-port": "1",
                "egress-port-list": ["2",  "3"],
                "sample-packet": "0010203232.."
            }
        }

        self.get_black_hole_event_report_missing_sample_packet = {
            "jsonrpc": "2.0",
            "method": "get-black-hole-event-report",
            "asic-id": "1", 
            "version": "2",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "report": {
                "ingress-port": "1",
                "egress-port-list": ["2",  "3"],
                "black-holed-packet-count": 100,
            }
        }

        self.get_sflow_sampling_status_1 = {
            "jsonrpc": "2.0",
            "method": "get-sflow-sampling-status",
            "asic-id": "1",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "version": "2",
            "report": {
                "data": [{ "port": "2",
                           "sflow-sampling-enabled": 1,
                           "sampled-packet-count": 100,
                           "black-holed-packet-count": 1000
                         }, 
                         { "port": "3",
                           "sflow-sampling-enabled": 1,
                           "sampled-packet-count": 200,
                           "black-holed-packet-count": 2000
                         }]
            },
            "id": 1
        }

        self.get_sflow_sampling_status_missing_method = {
            "jsonrpc": "2.0",
            "asic-id": "1",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "version": "2",
            "report": {
                "data": [{ "port": "2",
                           "sflow-sampling-enabled": 1,
                           "sampled-packet-count": 100,
                           "black-holed-packet-count": 1000
                         },
                         { "port": "3",
                           "sflow-sampling-enabled": 1,
                           "sampled-packet-count": 200,
                           "black-holed-packet-count": 2000
                         }]
            },
            "id": 1
        }

        self.get_sflow_sampling_status_missing_timestamp = {
            "jsonrpc": "2.0",
            "method": "get-sflow-sampling-status-invalid",
            "asic-id": "1",
            "version": "2",
            "report": {
                "data": [{ "port": "2",
                           "sflow-sampling-enabled": 1,
                           "sampled-packet-count": 100,
                           "black-holed-packet-count": 1000
                         },
                         { "port": "3",
                           "sflow-sampling-enabled": 1,
                           "sampled-packet-count": 200,
                           "black-holed-packet-count": 2000
                         }]
            },
            "id": 1
        }

        self.get_sflow_sampling_status_invalid_timestamp = {
            "jsonrpc": "2.0",
            "method": "get-sflow-sampling-status-invalid",
            "asic-id": "1",
            "time-stamp": "invalid timestamp",
            "version": "2",
            "report": {
                "data": [{ "port": "2",
                           "sflow-sampling-enabled": 1,
                           "sampled-packet-count": 100,
                           "black-holed-packet-count": 1000
                         },
                         { "port": "3",
                           "sflow-sampling-enabled": 1,
                           "sampled-packet-count": 200,
                           "black-holed-packet-count": 2000
                         }]
            },
            "id": 1
        }

        self.get_sflow_sampling_status_invalid_method = {
            "jsonrpc": "2.0",
            "method": "get-sflow-sampling-status-invalid",
            "asic-id": "1",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "version": "2",
            "report": {
                "data": [{ "port": "2",
                           "sflow-sampling-enabled": 1,
                           "sampled-packet-count": 100,
                           "black-holed-packet-count": 1000
                         },
                         { "port": "3",
                           "sflow-sampling-enabled": 1,
                           "sampled-packet-count": 200,
                           "black-holed-packet-count": 2000
                         }]
            },
            "id": 1
        }

        self.get_sflow_sampling_status_missing_asic = {
            "jsonrpc": "2.0",
            "method": "get-sflow-sampling-status",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "version": "2",
            "report": {
                "data": [{ "port": "2",
                           "sflow-sampling-enabled": 1,
                           "sampled-packet-count": 100,
                           "black-holed-packet-count": 1000
                         },
                         { "port": "3",
                           "sflow-sampling-enabled": 1,
                           "sampled-packet-count": 200,
                           "black-holed-packet-count": 2000
                         }]
            },
            "id": 1
        }

        self.get_sflow_sampling_status_missing_data = {
            "jsonrpc": "2.0",
            "method": "get-sflow-sampling-status",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "asic-id": "1",
            "version": "2",
            "report": {
            },
            "id": 1
        }

        self.get_sflow_sampling_status_data_object = {
            "jsonrpc": "2.0",
            "method": "get-sflow-sampling-status",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "version": "2",
            "report": {
                "data": {}
            },
            "id": 1
        }

        self.get_sflow_sampling_status_data_string = {
            "jsonrpc": "2.0",
            "method": "get-sflow-sampling-status",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "version": "2",
            "report": {
                "data": "Hello World!"
            },
            "id": 1
        }

        self.get_sflow_sampling_status_missing_result = {
            "jsonrpc": "2.0",
            "method": "get-sflow-sampling-status",
            "asic-id": "1",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "version": "2",
            "id": 1
        }

        self.get_sflow_sampling_status_empty_result = {
            "jsonrpc": "2.0",
            "method": "get-sflow-sampling-status",
            "asic-id": "1",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "version": "2",
            "report": {
            },
            "id": 1
        }

        self.get_sflow_sampling_status_result_array = {
            "jsonrpc": "2.0",
            "method": "get-sflow-sampling-status",
            "asic-id": "1",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "version": "2",
            "report": [
            ],
            "id": 1
        }

        self.get_sflow_sampling_status_missing_port = {
            "jsonrpc": "2.0",
            "method": "get-sflow-sampling-status",
            "asic-id": "1",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "version": "2",
            "report": {
                "data": [{ 
                           "sflow-sampling-enabled": 1,
                           "sampled-packet-count": 100,
                           "black-holed-packet-count": 1000
                         },
                         { "port": "3",
                           "sflow-sampling-enabled": 1,
                           "sampled-packet-count": 200,
                           "black-holed-packet-count": 2000
                         }]
            },
            "id": 1
        }

        self.get_sflow_sampling_status_missing_sampling_enabled = {
            "jsonrpc": "2.0",
            "method": "get-sflow-sampling-status",
            "asic-id": "1",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "version": "2",
            "report": {
                "data": [{ "port": "2",
                           "sampled-packet-count": 100,
                           "black-holed-packet-count": 1000
                         },
                         { "port": "3",
                           "sflow-sampling-enabled": 1,
                           "sampled-packet-count": 200,
                           "black-holed-packet-count": 2000
                         }]
            },
            "id": 1
        }

        self.get_sflow_sampling_status_missing_sampled_packet_count = {
            "jsonrpc": "2.0",
            "method": "get-sflow-sampling-status",
            "asic-id": "1",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "version": "2",
            "report": {
                "data": [{ "port": "2",
                           "sflow-sampling-enabled": 1,
                           "black-holed-packet-count": 1000
                         },
                         { "port": "3",
                           "sflow-sampling-enabled": 1,
                           "sampled-packet-count": 200,
                           "black-holed-packet-count": 2000
                         }]
            },
            "id": 1
        }

        self.get_sflow_sampling_status_missing_black_holed_packet_count = {
            "jsonrpc": "2.0",
            "method": "get-sflow-sampling-status",
            "asic-id": "1",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "version": "2",
            "report": {
                "data": [{ "port": "2",
                           "sflow-sampling-enabled": 1,
                           "black-holed-packet-count": 1000
                         },
                         { "port": "3",
                           "sflow-sampling-enabled": 1,
                           "sampled-packet-count": 200,
                         }]
            },
            "id": 1
        }


        self.get_black_hole_agent_1 = {
            "jsonrpc": "2.0",
            "asic-id": "1",
            "method": "get-black-hole",
            "version": "2",
            "result": {
                "port-list": ["1", "2", "3", "4"],
                "sampling-method": "agent",
                "sampling-params": {
                    "water-mark": 200,
                    "sample-periodicity": 15,
                    "sample-count": 10
                }
            },
            "id": 1
        }

    def test_get_black_hole_agent_1(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_agent_1)
        self.assertEqual(ret, True)
        rep = rep.getBlackHole()
        self.assertTrue(rep != None)
        self.assertEqual(rep.getSamplingMethod(), rep.AgentSampling)
        portList = rep.getPortList()
        self.assertTrue(len(portList), 4)
        self.assertTrue("1" in portList)
        self.assertTrue("2" in portList)
        self.assertTrue("3" in portList)
        self.assertTrue("4" in portList)
        p = rep.getSamplingParams()
        self.assertEqual(p.getWaterMark(), 200)
        self.assertEqual(p.getSamplePeriodicity(), 15)
        self.assertEqual(p.getSampleCount(), 10)

    def test_get_black_hole_agent_missing_method(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_agent_missing_method )
        self.assertEqual(ret, False)

    def test_get_black_hole_agent_invalid_method(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_agent_invalid_method)
        self.assertEqual(ret, False)

    def test_get_black_hole_agent_missing_asic(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_agent_missing_asic)
        self.assertEqual(ret, False)

    def test_get_black_hole_agent_missing_result(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_agent_missing_result)
        self.assertEqual(ret, False)

    def test_get_black_hole_agent_empty_result(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_agent_empty_result)
        self.assertEqual(ret, False)

    def test_get_black_hole_agent_result_array(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_agent_result_array)
        self.assertEqual(ret, False)

    def test_get_black_hole_agent_missing_port_list(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_agent_missing_port_list)
        self.assertEqual(ret, False)

    def test_get_black_hole_agent_missing_sampling_method(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_agent_missing_sampling_method)
        self.assertEqual(ret, False)

    def test_get_black_hole_agent_invalid_sampling_method(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_agent_invalid_sampling_method)
        self.assertEqual(ret, False)

    def test_get_black_hole_agent_missing_sampling_params(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_agent_missing_sampling_params)
        self.assertEqual(ret, False)

    def test_get_black_hole_agent_missing_water_mark(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_agent_missing_water_mark)
        self.assertEqual(ret, False)

    def test_get_black_hole_agent_missing_sample_periodicity(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_agent_missing_sample_periodicity)
        self.assertEqual(ret, False)

    def test_get_black_hole_agent_missing_sample_count(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_agent_missing_sample_count)
        self.assertEqual(ret, False)

    def test_get_black_hole_sflow_1(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_sflow_1)
        self.assertEqual(ret, True)
        rep = rep.getBlackHole()
        self.assertTrue(rep != None)
        self.assertEqual(rep.getSamplingMethod(), rep.SFlowSampling)
        portList = rep.getPortList()
        self.assertTrue(len(portList), 4)
        self.assertTrue("1" in portList)
        self.assertTrue("2" in portList)
        self.assertTrue("3" in portList)
        self.assertTrue("4" in portList)
        p = rep.getSamplingParams()
        self.assertEqual(p.getVLANId(), 1)
        self.assertEqual(p.getDstIP(), "1.1.1.1")
        self.assertEqual(p.getSrcUDPPort(), 1234)
        self.assertEqual(p.getDstUDPPort(), 4321)
        self.assertEqual(p.getMirrorPort(), "10")
        self.assertEqual(p.getSamplePoolSize(), 1)

    def test_get_black_hole_sflow_missing_method(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_sflow_missing_method)
        self.assertEqual(ret, False)

    def test_get_black_hole_sflow_invalid_method(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_sflow_invalid_method)
        self.assertEqual(ret, False)

    def test_get_black_hole_sflow_missing_asic(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_sflow_missing_asic)
        self.assertEqual(ret, False)

    def test_get_black_hole_sflow_missing_result(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_sflow_missing_result)
        self.assertEqual(ret, False)

    def test_get_black_hole_sflow_empty_result(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_sflow_empty_result)
        self.assertEqual(ret, False)

    def test_get_black_hole_sflow_result_array(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_sflow_result_array)
        self.assertEqual(ret, False)

    def test_get_black_hole_sflow_missing_sampling_method(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_sflow_missing_sampling_method)
        self.assertEqual(ret, False)

    def test_get_black_hole_sflow_invalid_sampling_method(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_sflow_invalid_sampling_method)
        self.assertEqual(ret, False)

    def test_get_black_hole_sflow_missing_sampling_params(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_sflow_missing_sampling_params)
        self.assertEqual(ret, False)

    def test_get_black_hole_sflow_invalid_sampling_method(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_sflow_invalid_sampling_method)
        self.assertEqual(ret, False)

    def test_get_black_hole_sflow_missing_encap_params(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_sflow_missing_encap_params)
        self.assertEqual(ret, False)

    def test_get_black_hole_sflow_missing_vlan_id(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_sflow_missing_vlan_id)
        self.assertEqual(ret, False)

    def test_get_black_hole_sflow_missing_destination_ip(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_sflow_missing_destination_ip)
        self.assertEqual(ret, False)

    def test_get_black_hole_sflow_missing_src_udp(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_sflow_missing_src_udp)
        self.assertEqual(ret, False)

    def test_get_black_hole_sflow_missing_dst_udp(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_sflow_missing_dst_udp)
        self.assertEqual(ret, False)

    def test_get_black_hole_sflow_missing_mirror_port(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_sflow_missing_mirror_port)
        self.assertEqual(ret, False)

    def test_get_black_hole_sflow_missing_sample_pool_size(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_sflow_missing_sample_pool_size)
        self.assertEqual(ret, False)

    def test_get_black_hole_event_report_1(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_event_report_1)
        self.assertEqual(ret, True)
        rep = rep.getBlackHoleEventReport()
        self.assertTrue(rep != None)
        portList = rep.getEgressPortList()
        self.assertTrue(len(portList), 2)
        self.assertTrue("2" in portList)
        self.assertTrue("3" in portList)
        self.assertEqual(rep.getSamplePacket(), "0010203232..")
        self.assertEqual(rep.getBlackHoledPacketCount(), 100)
        self.assertEqual(rep.getIngressPort(), "1")

    def test_get_black_hole_event_report_missing_method(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_event_report_missing_method)
        self.assertEqual(ret, False)

    def test_get_black_hole_event_report_invalid_method(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_event_report_invalid_method)
        self.assertEqual(ret, False)

    def test_get_black_hole_event_report_missing_asic(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_event_report_missing_asic)
        self.assertEqual(ret, False)

    def test_get_black_hole_event_report_missing_result(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_event_report_missing_result)
        self.assertEqual(ret, False)

    def test_get_black_hole_event_report_empty_result(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_event_report_empty_result)
        self.assertEqual(ret, False)

    def test_get_black_hole_event_report_result_array(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_event_report_result_array)
        self.assertEqual(ret, False)

    def test_get_black_hole_event_report_missing_timestamp(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_event_report_missing_timestamp)
        self.assertEqual(ret, False)

    def test_get_black_hole_event_report_missing_ingress_port(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_event_report_missing_ingress_port)
        self.assertEqual(ret, False)

    def test_get_black_hole_event_report_missing_egress_port_list(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_event_report_missing_egress_port_list)
        self.assertEqual(ret, False)

    def test_get_black_hole_event_report_missing_bhpc(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_event_report_missing_bhpc)
        self.assertEqual(ret, False)

    def test_get_black_hole_event_report_missing_sample_packet(self):
        rep = BHDParser()
        ret = rep.process(self.get_black_hole_event_report_missing_sample_packet)
        self.assertEqual(ret, False)

    def test_get_sflow_sampling_status_1(self):
        rep = BHDParser()
        ret = rep.process(self.get_sflow_sampling_status_1)
        self.assertEqual(ret, True)
        rep = rep.getSFlowSamplingStatus()
        self.assertTrue(rep != None)
        i = 0
        for x in rep:
            comp = self.get_sflow_sampling_status_1["report"]["data"][i]
            self.assertTrue(x.getPort() == comp["port"]) 
            self.assertTrue(x.getSFlowSamplingEnabled() == comp["sflow-sampling-enabled"]) 
            self.assertTrue(x.getSampledPacketCount() == comp["sampled-packet-count"]) 
            self.assertTrue(x.getBlackHoledPacketCount() == comp["black-holed-packet-count"]) 
            i = i + 1
        self.assertEqual(i, 2)

    def test_get_sflow_sampling_status_missing_method(self):
        rep = BHDParser()
        ret = rep.process(self.get_sflow_sampling_status_missing_method)
        self.assertEqual(ret, False)

    def test_get_sflow_sampling_status_missing_timestamp(self):
        rep = BHDParser()
        ret = rep.process(self.get_sflow_sampling_status_missing_timestamp)
        self.assertEqual(ret, False)

    def test_get_sflow_sampling_status_invalid_timestamp(self):
        rep = BHDParser()
        ret = rep.process(self.get_sflow_sampling_status_invalid_timestamp)
        self.assertEqual(ret, False)

    def test_get_sflow_sampling_status_invalid_method(self):
        rep = BHDParser()
        ret = rep.process(self.get_sflow_sampling_status_invalid_method)
        self.assertEqual(ret, False)

    def test_get_sflow_sampling_status_missing_asic(self):
        rep = BHDParser()
        ret = rep.process(self.get_sflow_sampling_status_missing_asic)
        self.assertEqual(ret, False)

    def test_get_sflow_sampling_status_missing_data(self):
        rep = BHDParser()
        ret = rep.process(self.get_sflow_sampling_status_missing_data)
        self.assertEqual(ret, False)

    def test_get_sflow_sampling_status_data_object(self):
        rep = BHDParser()
        ret = rep.process(self.get_sflow_sampling_status_data_object)
        self.assertEqual(ret, False)

    def test_get_sflow_sampling_status_data_string(self):
        rep = BHDParser()
        ret = rep.process(self.get_sflow_sampling_status_data_string)
        self.assertEqual(ret, False)

    def test_get_sflow_sampling_status_missing_result(self):
        rep = BHDParser()
        ret = rep.process(self.get_sflow_sampling_status_missing_result)
        self.assertEqual(ret, False)

    def test_get_sflow_sampling_status_empty_result(self):
        rep = BHDParser()
        ret = rep.process(self.get_sflow_sampling_status_empty_result)
        self.assertEqual(ret, False)

    def test_get_sflow_sampling_status_result_array(self):
        rep = BHDParser()
        ret = rep.process(self.get_sflow_sampling_status_result_array)
        self.assertEqual(ret, False)

    def test_get_sflow_sampling_status_missing_port(self):
        rep = BHDParser()
        ret = rep.process(self.get_sflow_sampling_status_missing_port)
        self.assertEqual(ret, False)

    def test_get_sflow_sampling_status_missing_sampling_enabled(self):
        rep = BHDParser()
        ret = rep.process(self.get_sflow_sampling_status_missing_sampling_enabled)
        self.assertEqual(ret, False)

    def test_get_sflow_sampling_status_missing_sampled_packet_count(self):
        rep = BHDParser()
        ret = rep.process(self.get_sflow_sampling_status_missing_sampled_packet_count)
        self.assertEqual(ret, False)

    def test_get_sflow_sampling_status_missing_black_holed_packet_count(self):
        rep = BHDParser()
        ret = rep.process(self.get_sflow_sampling_status_missing_black_holed_packet_count)
        self.assertEqual(ret, False)

if __name__ == "__main__":
    unittest.main()
