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

import packet_trace_lag_resolution
import packet_trace_ecmp_resolution
import packet_trace_profile
import packet_trace_drop_reason
import packet_trace_drop_counter_report
import packet_trace_drop_reasons
import time
import unittest

class ReportTypes:
    PacketTraceProfile, PacketTraceLAGResolution, \
    PacketTraceECMPResolution, PacketTraceDropReason, \
    PacketTraceSupportedDropReasons, PacketTraceDropCounterReport = range(6)

class PTParser():
    def __init__(self):
        self.__reportType = None
        self.__packet_trace_profile = []
        self.__packet_trace_lag_resolution = []
        self.__packet_trace_ecmp_resolution = []
        self.__packet_trace_supported_drop_reasons = None
        self.__packet_trace_drop_reason = []
        self.__packet_trace_drop_counter_report = []

        self.__reportHandlers = [self._handlePacketTraceProfile,
                                 self._handlePacketTraceLAGResolution,
                                 self._handlePacketTraceECMPResolution, 
                                 self._handlePacketTraceDropReason,
                                 self._handlePacketTraceSupportedDropReasons,
                                 self._handlePacketTraceDropCounterReport]

    def getReportType(self):
        return self.__reportType

    def getASICId(self):
        return self.__asicId;

    def getTimestamp(self):
        return self.__timestamp;

    def __repr__(self):
        return "PT"

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

    def _handlePacketTraceProfile(self, data):
        ret = True
        try:
            report = data["report"]
        except:
            ret = False
            report = [] 
        for x in report:
            t = packet_trace_profile.PacketTraceProfile()
            if "port" in x:
                port = x["port"]
            else:
                ret = False
                break
            if "trace-profile" in x:
                x = x["trace-profile"]
            else:
                ret = False
                break
            ret = t.parse(x, port)
            if ret:
                self.__packet_trace_profile.append(t)
            else:
                break

        return ret

    def getPacketTraceProfile(self):
        return self.__packet_trace_profile

    def _handlePacketTraceLAGResolution(self, data):
        ret = True
        try:
            report = data["report"]
        except:
            ret = False
            report = []
        for x in report:
            t = packet_trace_lag_resolution.PacketTraceLAGResolution()
            if "port" in x:
                port = x["port"]
            else:
                ret = False
                break
            ret = t.parse(x, port)
            if ret:
                self.__packet_trace_lag_resolution.append(t)
            else:
                break

        return ret

    def getPacketTraceLAGResolution(self):
        return self.__packet_trace_lag_resolution

    def _handlePacketTraceECMPResolution(self, data):
        ret = True
        try:
            report = data["report"]
        except:
            report = []
            ret = False
        for x in report:
            t = packet_trace_ecmp_resolution.PacketTraceECMPResolution()
            if "port" in x:
                port = x["port"]
            else:
                ret = False
                break
            ret = t.parse(x, port)
            if ret:
                self.__packet_trace_ecmp_resolution.append(t)
            else:
                break

        return ret

    def getPacketTraceECMPResolution(self):
        return self.__packet_trace_ecmp_resolution

    def _handlePacketTraceDropReason(self, data):
        ret = True
        try:
            report = data["result"]
        except:
            report = []
            ret = False
        for x in report:
            t = packet_trace_drop_reason.PacketTraceDropReason()
            ret = t.parse(x)
            if ret:
                self.__packet_trace_drop_reason.append(t)
            else:
                break

        return ret

    def getPacketTraceDropReason(self):
        return self.__packet_trace_drop_reason

    def _handlePacketTraceSupportedDropReasons(self, data):
        ret = True
        result = data["result"]
        t = packet_trace_drop_reasons.PacketTraceSupportedDropReasons()
        ret = t.parse(result)
        if ret:
            self.__packet_trace_supported_drop_reasons = t
        else:
            ret = False
        return ret

    def getPacketTraceSupportedDropReasons(self):
        return self.__packet_trace_supported_drop_reasons

    def _handlePacketTraceDropCounterReport(self, data):
        ret = True
        try:
            report = data["report"]
        except:
            ret = False
            report = []
        for x in report:
            t = packet_trace_drop_counter_report.PacketTraceDropCounterReport()
            ret = t.parse(x)
            if ret:
                self.__packet_trace_drop_counter_report.append(t)
            else:
                break

        return ret

    def getPacketTraceDropCounterReport(self):
        return self.__packet_trace_drop_counter_report

    def process(self, data):
        ret = True
        if self.valid(data):
            if data["method"] == "get-packet-trace-profile":
                self.__reportType = ReportTypes.PacketTraceProfile
            elif data["method"] == "get-packet-trace-lag-resolution":
                self.__reportType = ReportTypes.PacketTraceLAGResolution
            elif data["method"] == "get-packet-trace-ecmp-resolution":
                self.__reportType = ReportTypes.PacketTraceECMPResolution
            elif data["method"] == "get-packet-trace-drop-reason":
                self.__reportType = ReportTypes.PacketTraceDropReason
            elif data["method"] == "get-packet-trace-supported-drop-reasons":
                self.__reportType = ReportTypes.PacketTraceSupportedDropReasons
            elif data["method"] == "get-packet-trace-drop-counter-report":
                self.__reportType = ReportTypes.PacketTraceDropCounterReport
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
            if data["method"] != "get-packet-trace-profile" and \
               data["method"] != "get-packet-trace-lag-resolution" and \
               data["method"] != "get-packet-trace-ecmp-resolution" and \
               data["method"] != "get-packet-trace-drop-reason" and \
               data["method"] != "get-packet-trace-supported-drop-reasons" and \
               data["method"] != "get-packet-trace-drop-counter-report":
                ret = False
        else:
            ret = False

        if ret:
            for x in keys:
                if not x in data:
                    if x == "time-stamp":
                        if data["method"] == "get-packet-trace-supported-drop-reasons":
                            continue
                        if data["method"] == "get-packet-trace-drop-reason":
                            continue
                        if data["method"] == "get-packet-trace-drop-counter-report":
                            continue
                    ret = False
                    break

        if ret:
            if "report" in data:
                if not type(data["report"]) == list:
                    ret = False
                elif len(data["report"]) == 0:
                    ret = False
            elif "result" in data:
                if not type(data["result"]) == list:
                    ret = False
                elif len(data["result"]) == 0:
                    ret = False
            else:
                ret = False # must contain a result or report

        return ret

class TestParser(unittest.TestCase):

    def setUp(self):
        self.packet_trace_profile = {
            "jsonrpc": "2.0",
            "method": "get-packet-trace-profile",
            "asic-id": "1",
            "version": "1",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "report": [
                {
                    "port": "1",
                    "trace-profile": [
                        {
                            "realm": "lag-link-resolution",
                            "data": {
                                "lag-id": "2",
                                "lag-members": ["1", "2", "3", "4"],
                                "dst-lag-member": "4"
                            }
                        },
                        {
                            "realm": "ecmp-link-resolution",
                            "data": [
                                {
                                    "ecmp-group-id": "200256",
                                    "ecmp-members": [["100004", "2.2.2.2", "28"],["100005", "6.6.6.1", "41"]],
                                    "ecmp-dst-member": "100005",
                                    "ecmp-dst-port": "41",
                                    "ecmp-next-hop-ip": "6.6.6.2"
                                },
                                {
                                    "ecmp-group-id": "200100",
                                    "ecmp-members": [["100001", "3.3.3.1", "31"],
["100002", "7.7.7.2", "21"]],
                                    "ecmp-dst-member": "100001",
                                    "ecmp-dst-port": "31",
                                    "ecmp-next-hop-ip": "3.3.3.2"
                                }
                            ]
                         }
                    ]
                },
                {
                    "port": "2",
                    "trace-profile": [
                        {
                            "realm": "lag-link-resolution",
                            "data": {
                                "lag-id": "3",
                                "lag-members": ["5","6","7","8"],
                                "dst-lag-member": "6"
                            }
                        },
                        {
                            "realm": "ecmp-link-resolution",
                            "data": [
                                {
                                    "ecmp-group-id": "200512",
                                    "ecmp-members": [["200004", "3.2.2.2", "38"],["100005", "6.6.6.1", "41"]],
                                    "ecmp-dst-member": "100010",
                                    "ecmp-dst-port": "19",
                                    "ecmp-next-hop-ip": "8.8.8.2"
                                },
                                {
                                    "ecmp-group-id": "200200",
                                    "ecmp-members": [["100002", "4.3.3.1", "76"], ["100002", "7.7.7.2", "21"]],
                                    "ecmp-dst-member": "100002",
                                    "ecmp-dst-port": "55",
                                    "ecmp-next-hop-ip": "7.3.3.2"
                                }
                            ]
                        }
                    ]
                }
            ],
            "id": 1
        }

        self.packet_trace_profile_unknown_method = {
            "jsonrpc": "2.0",
            "method": "get-packet-trace-unknown",
            "asic-id": "1",
            "version": "1",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "report": [
                {
                    "port": "1",
                    "trace-profile": [
                        {
                            "realm": "lag-link-resolution",
                            "data": {
                                "lag-id": "2",
                                "lag-members": ["1", "2", "3", "4"],
                                "dst-lag-member": "4"
                            }
                        },
                        {
                            "realm": "ecmp-link-resolution",
                            "data": [
                                {
                                    "ecmp-group-id": "200256",
                                    "ecmp-members": [["100004", "2.2.2.2", "28"],["100005", "6.6.6.1", "41"]],
                                    "ecmp-dst-member": "100005",
                                    "ecmp-dst-port": "41",
                                    "ecmp-next-hop-ip": "6.6.6.2"
                                },
                                {
                                    "ecmp-group-id": "200100",
                                    "ecmp-members": [["100001", "3.3.3.1", "31"],
["100002", "7.7.7.2", "21"]],
                                    "ecmp-dst-member": "100001",
                                    "ecmp-dst-port": "31",
                                    "ecmp-next-hop-ip": "3.3.3.2"
                                }
                            ]
                         }
                    ]
                },
                {
                    "port": "2",
                    "trace-profile": [
                        {
                            "realm": "lag-link-resolution",
                            "data": {
                                "lag-id": "2",
                                "lag-members": ["1","2","3","4"],
                                "dst-lag-member": "4"
                            }
                        },
                        {
                            "realm": "ecmp-link-resolution",
                            "data": [
                                {
                                    "ecmp-group-id": "200256",
                                    "ecmp-members": [["100004", "2.2.2.2", "28"],["100005", "6.6.6.1", "41"]],
                                    "ecmp-dst-member": "100005",
                                    "ecmp-dst-port": "41",
                                    "ecmp-next-hop-ip": "6.6.6.2"
                                },
                                {
                                    "ecmp-group-id": "200100",
                                    "ecmp-members": [["100001", "3.3.3.1", "31"], ["100002", "7.7.7.2", "21"]],
                                    "ecmp-dst-member": "100001",
                                    "ecmp-dst-port": "31",
                                    "ecmp-next-hop-ip": "3.3.3.2"
                                }
                            ]
                        }
                    ]
                }
            ],
            "id": 1
        }

        self.packet_trace_profile_unknown_realm = {
            "jsonrpc": "2.0",
            "method": "get-packet-trace-profile",
            "asic-id": "1",
            "version": "1",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "report": [
                {
                    "port": "1",
                    "trace-profile": [
                        {
                            "realm": "lag-link-unknown",
                            "data": {
                                "lag-id": "2",
                                "lag-members": ["1", "2", "3", "4"],
                                "dst-lag-member": "4"
                            }
                        },
                        {
                            "realm": "ecmp-link-unknown",
                            "data": [
                                {
                                    "ecmp-group-id": "200256",
                                    "ecmp-members": [["100004", "2.2.2.2", "28"],["100005", "6.6.6.1", "41"]],
                                    "ecmp-dst-member": "100005",
                                    "ecmp-dst-port": "41",
                                    "ecmp-next-hop-ip": "6.6.6.2"
                                },
                                {
                                    "ecmp-group-id": "200100",
                                    "ecmp-members": [["100001", "3.3.3.1", "31"],
["100002", "7.7.7.2", "21"]],
                                    "ecmp-dst-member": "100001",
                                    "ecmp-dst-port": "31",
                                    "ecmp-next-hop-ip": "3.3.3.2"
                                }
                            ]
                         }
                    ]
                },
                {
                    "port": "2",
                    "trace-profile": [
                        {
                            "realm": "lag-link-resolution",
                            "data": {
                                "lag-id": "2",
                                "lag-members": ["1","2","3","4"],
                                "dst-lag-member": "4"
                            }
                        },
                        {
                            "realm": "ecmp-link-resolution",
                            "data": [
                                {
                                    "ecmp-group-id": "200256",
                                    "ecmp-members": [["100004", "2.2.2.2", "28"],["100005", "6.6.6.1", "41"]],
                                    "ecmp-dst-member": "100005",
                                    "ecmp-dst-port": "41",
                                    "ecmp-next-hop-ip": "6.6.6.2"
                                },
                                {
                                    "ecmp-group-id": "200100",
                                    "ecmp-members": [["100001", "3.3.3.1", "31"], ["100002", "7.7.7.2", "21"]],
                                    "ecmp-dst-member": "100001",
                                    "ecmp-dst-port": "31",
                                    "ecmp-next-hop-ip": "3.3.3.2"
                                }
                            ]
                        }
                    ]
                }
            ],
            "id": 1
        }

        self.packet_trace_profile_bad_timestamp = {
            "jsonrpc": "2.0",
            "method": "get-packet-trace-profile",
            "asic-id": "1",
            "version": "1",
            "time-stamp": "XXXXXXX",
            "report": [
                {
                    "port": "1",
                    "trace-profile": [
                        {
                            "realm": "lag-link-resolution",
                            "data": {
                                "lag-id": "2",
                                "lag-members": ["1", "2", "3", "4"],
                                "dst-lag-member": "4"
                            }
                        },
                        {
                            "realm": "ecmp-link-resolution",
                            "data": [
                                {
                                    "ecmp-group-id": "200256",
                                    "ecmp-members": [["100004", "2.2.2.2", "28"],["100005", "6.6.6.1", "41"]],
                                    "ecmp-dst-member": "100005",
                                    "ecmp-dst-port": "41",
                                    "ecmp-next-hop-ip": "6.6.6.2"
                                },
                                {
                                    "ecmp-group-id": "200100",
                                    "ecmp-members": [["100001", "3.3.3.1", "31"],
["100002", "7.7.7.2", "21"]],
                                    "ecmp-dst-member": "100001",
                                    "ecmp-dst-port": "31",
                                    "ecmp-next-hop-ip": "3.3.3.2"
                                }
                            ]
                         }
                    ]
                },
                {
                    "port": "2",
                    "trace-profile": [
                        {
                            "realm": "lag-link-resolution",
                            "data": {
                                "lag-id": "2",
                                "lag-members": ["1","2","3","4"],
                                "dst-lag-member": "4"
                            }
                        },
                        {
                            "realm": "ecmp-link-resolution",
                            "data": [
                                {
                                    "ecmp-group-id": "200256",
                                    "ecmp-members": [["100004", "2.2.2.2", "28"],["100005", "6.6.6.1", "41"]],
                                    "ecmp-dst-member": "100005",
                                    "ecmp-dst-port": "41",
                                    "ecmp-next-hop-ip": "6.6.6.2"
                                },
                                {
                                    "ecmp-group-id": "200100",
                                    "ecmp-members": [["100001", "3.3.3.1", "31"], ["100002", "7.7.7.2", "21"]],
                                    "ecmp-dst-member": "100001",
                                    "ecmp-dst-port": "31",
                                    "ecmp-next-hop-ip": "3.3.3.2"
                                }
                            ]
                        }
                    ]
                }
            ],
            "id": 1
        }

        self.packet_trace_profile_report_dict = {
            "jsonrpc": "2.0",
            "method": "get-packet-trace-profile",
            "asic-id": "1",
            "version": "1",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "report": {},
            "id": 1
        }

        self.packet_trace_profile_empty_report = {
            "jsonrpc": "2.0",
            "method": "get-packet-trace-profile",
            "asic-id": "1",
            "version": "1",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "report": [],
            "id": 1
        }


        self.packet_trace_profile_missing_report = {
            "jsonrpc": "2.0",
            "method": "get-packet-trace-profile",
            "asic-id": "1",
            "version": "1",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "id": 1
        }

        self.packet_trace_lag_resolution_unknown_method = {
            "jsonrpc": "2.0",
            "method": " sdfsdfsdfsdfsdf",
            "asic-id": "1",
            "version": "1",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "report": [
                {
                    "port": "1",
                    "lag-link-resolution": {
                        "lag-id": "2",
                        "lag-members": [
                            "1",
                            "2",
                            "3",
                            "4"
                        ],
                        "dst-lag-member": "4"
                    }
                },
                {
                    "port": "2",
                    "lag-link-resolution": {
                        "lag-id": "2",
                        "lag-members": [
                            "1",
                            "2",
                            "3",
                            "4"
                        ],
                        "dst-lag-member": "4"
                    }
                }
            ],
            "id": 1
        }

        self.packet_trace_lag_resolution_unknown_realm = {
            "jsonrpc": "2.0",
            "method": " get-packet-trace-lag-resolution",
            "asic-id": "1",
            "version": "1",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "report": [
                {
                    "port": "1",
                    "lag-link-revolution": {
                        "lag-id": "2",
                        "lag-members": [
                            "1",
                            "2",
                            "3",
                            "4"
                        ],
                        "dst-lag-member": "4"
                    }
                },
                {
                    "port": "2",
                    "lag-link-restitution": {
                        "lag-id": "2",
                        "lag-members": [
                            "1",
                            "2",
                            "3",
                            "4"
                        ],
                        "dst-lag-member": "4"
                    }
                }
            ],
            "id": 1
        }

        self.packet_trace_lag_resolution_bad_timestamp = {
            "jsonrpc": "2.0",
            "method": " get-packet-trace-lag-resolution",
            "asic-id": "1",
            "version": "1",
            "time-stamp": "abcdefghijklmnopqrstuvwxyz ",
            "report": [
                {
                    "port": "1",
                    "lag-link-resolution": {
                        "lag-id": "2",
                        "lag-members": [
                            "1",
                            "2",
                            "3",
                            "4"
                        ],
                        "dst-lag-member": "4"
                    }
                },
                {
                    "port": "2",
                    "lag-link-resolution": {
                        "lag-id": "2",
                        "lag-members": [
                            "1",
                            "2",
                            "3",
                            "4"
                        ],
                        "dst-lag-member": "4"
                    }
                }
            ],
            "id": 1
        }

        self.packet_trace_lag_resolution_report_dict = {
            "jsonrpc": "2.0",
            "method": " get-packet-trace-lag-resolution",
            "asic-id": "1",
            "version": "1",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "report": {},
            "id": 1
        }

        self.packet_trace_lag_resolution_empty_report = {
            "jsonrpc": "2.0",
            "method": " get-packet-trace-lag-resolution",
            "asic-id": "1",
            "version": "1",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "report": [
            ],
            "id": 1
        }

        self.packet_trace_lag_resolution_missing_report = {
            "jsonrpc": "2.0",
            "method": " get-packet-trace-lag-resolution",
            "asic-id": "1",
            "version": "1",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "id": 1
        }

        self.packet_trace_lag_resolution = {
            "jsonrpc": "2.0",
            "method": " get-packet-trace-lag-resolution",
            "asic-id": "1",
            "version": "1",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "report": [
                {
                    "port": "1",
                    "lag-link-resolution": {
                        "lag-id": "1",
                        "lag-members": [
                            "1",
                            "2",
                            "3",
                            "4"
                        ],
                        "dst-lag-member": "4"
                    }
                },
                {
                    "port": "2",
                    "lag-link-resolution": {
                        "lag-id": "2",
                        "lag-members": [
                            "5",
                            "6",
                            "7",
                            "8"
                        ],
                        "dst-lag-member": "7"
                    }
                }
            ],
            "id": 1
        }

        self.packet_trace_ecmp_resolution_unknown_method = {
            "jsonrpc": "2.0",
            "method": " get-packet-trace-mcep-resolution",
            "asic-id": "1",
            "version": "1",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "report": [
                {
                    "port": "1",
                    "ecmp-link-resolution": [
                        {
                            "ecmp-group-id": "200256",
                            "ecmp-members": [["100004", "2.2.2.2", "28"],["100005", "6.6.6.1", "41"]],
                            "ecmp-dst-member": "100005",
                            "ecmp-dst-port": "41",
                            "ecmp-next-hop-ip": "6.6.6.2"
                        },
                        {
                            "ecmp-group-id": "200100",
                            "ecmp-members": [["100001", "3.3.3.1", "31"], ["100002", "7.7.7.2", "21"]],
                            "ecmp-dst-member": "100001",
                            "ecmp-dst-port": "31",
                            "ecmp-next-hop-ip": "3.3.3.2"
                        }
                    ]
                },
                {
                    "port": "2",
                    "ecmp-link-resolution": [
                        {
                            "ecmp-group-id": "200256",
                            "ecmp-members": [["100001", "3.3.3.1", "31"], ["100002", "7.7.7.2", "21"]],
                            "ecmp-dst-member": "100005",
                            "ecmp-dst-port": "41",
                            "ecmp-next-hop-ip": "6.6.6.2"
                        },
                        {
                            "ecmp-group-id": "200100",
                            "ecmp-members": [["100004", "2.2.2.2", "28"],["100005", "6.6.6.1", "41"]],
                            "ecmp-dst-member": "100001",
                            "ecmp-dst-port": "31",
                            "ecmp-next-hop-ip": "3.3.3.2"
                        }
                    ]
                }
            ],
            "id": 1
        }

        self.packet_trace_ecmp_resolution_unknown_realm = {
            "jsonrpc": "2.0",
            "method": " get-packet-trace-ecmp-resolution",
            "asic-id": "1",
            "version": "1",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "report": [
                {
                    "port": "1",
                    "ecmp-link-unknown": [
                        {
                            "ecmp-group-id": "200256",
                            "ecmp-members": [["100004", "2.2.2.2", "28"],["100005", "6.6.6.1", "41"]],
                            "ecmp-dst-member": "100005",
                            "ecmp-dst-port": "41",
                            "ecmp-next-hop-ip": "6.6.6.2"
                        },
                        {
                            "ecmp-group-id": "200100",
                            "ecmp-members": [["100001", "3.3.3.1", "31"], ["100002", "7.7.7.2", "21"]],
                            "ecmp-dst-member": "100001",
                            "ecmp-dst-port": "31",
                            "ecmp-next-hop-ip": "3.3.3.2"
                        }
                    ]
                },
                {
                    "port": "2",
                    "ecmp-sink-resolution": [
                        {
                            "ecmp-group-id": "200256",
                            "ecmp-members": [["100001", "3.3.3.1", "31"], ["100002", "7.7.7.2", "21"]],
                            "ecmp-dst-member": "100005",
                            "ecmp-dst-port": "41",
                            "ecmp-next-hop-ip": "6.6.6.2"
                        },
                        {
                            "ecmp-group-id": "200100",
                            "ecmp-members": [["100004", "2.2.2.2", "28"],["100005", "6.6.6.1", "41"]],
                            "ecmp-dst-member": "100001",
                            "ecmp-dst-port": "31",
                            "ecmp-next-hop-ip": "3.3.3.2"
                        }
                    ]
                }
            ],
            "id": 1
        }

        self.packet_trace_ecmp_resolution_bad_timestamp = {
            "jsonrpc": "2.0",
            "method": " get-packet-trace-ecmp-resolution",
            "asic-id": "1",
            "version": "1",
            "time-stamp": "to be or not to be, that is the question",
            "report": [
                {
                    "port": "1",
                    "ecmp-link-resolution": [
                        {
                            "ecmp-group-id": "200256",
                            "ecmp-members": [["100004", "2.2.2.2", "28"],["100005", "6.6.6.1", "41"]],
                            "ecmp-dst-member": "100005",
                            "ecmp-dst-port": "41",
                            "ecmp-next-hop-ip": "6.6.6.2"
                        },
                        {
                            "ecmp-group-id": "200100",
                            "ecmp-members": [["100001", "3.3.3.1", "31"], ["100002", "7.7.7.2", "21"]],
                            "ecmp-dst-member": "100001",
                            "ecmp-dst-port": "31",
                            "ecmp-next-hop-ip": "3.3.3.2"
                        }
                    ]
                },
                {
                    "port": "2",
                    "ecmp-link-resolution": [
                        {
                            "ecmp-group-id": "200256",
                            "ecmp-members": [["100001", "3.3.3.1", "31"], ["100002", "7.7.7.2", "21"]],
                            "ecmp-dst-member": "100005",
                            "ecmp-dst-port": "41",
                            "ecmp-next-hop-ip": "6.6.6.2"
                        },
                        {
                            "ecmp-group-id": "200100",
                            "ecmp-members": [["100004", "2.2.2.2", "28"],["100005", "6.6.6.1", "41"]],
                            "ecmp-dst-member": "100001",
                            "ecmp-dst-port": "31",
                            "ecmp-next-hop-ip": "3.3.3.2"
                        }
                    ]
                }
            ],
            "id": 1
        }

        self.packet_trace_ecmp_resolution_report_dict = {
            "jsonrpc": "2.0",
            "method": " get-packet-trace-ecmp-resolution",
            "asic-id": "1",
            "version": "1",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "report": {},
            "id": 1
        }

        self.packet_trace_ecmp_resolution_empty_report = {
            "jsonrpc": "2.0",
            "method": " get-packet-trace-ecmp-resolution",
            "asic-id": "1",
            "version": "1",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "report": [
            ],
            "id": 1
        }

        self.packet_trace_ecmp_resolution_missing_report = {
            "jsonrpc": "2.0",
            "method": " get-packet-trace-ecmp-resolution",
            "asic-id": "1",
            "version": "1",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "id": 1
        }

        self.packet_trace_ecmp_resolution = {
            "jsonrpc": "2.0",
            "method": " get-packet-trace-ecmp-resolution",
            "asic-id": "1",
            "version": "1",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "report": [
                {
                    "port": "1",
                    "ecmp-link-resolution": [
                        {
                            "ecmp-group-id": "200256",
                            "ecmp-members": [["100004", "2.2.2.2", "28"],["100005", "6.6.6.1", "41"]],
                            "ecmp-dst-member": "100005",
                            "ecmp-dst-port": "41",
                            "ecmp-next-hop-ip": "6.6.6.2"
                        },
                        {
                            "ecmp-group-id": "200100",
                            "ecmp-members": [["100001", "3.3.3.1", "31"], ["100002", "7.7.7.2", "21"]],
                            "ecmp-dst-member": "100001",
                            "ecmp-dst-port": "31",
                            "ecmp-next-hop-ip": "3.3.3.2"
                        }
                    ]
                },
                {
                    "port": "2",
                    "ecmp-link-resolution": [
                        {
                            "ecmp-group-id": "200512",
                            "ecmp-members": [["100002", "6.3.3.1", "61"], ["100004", "9.9.9.2", "41"]],
                            "ecmp-dst-member": "100010",
                            "ecmp-dst-port": "81",
                            "ecmp-next-hop-ip": "7.6.6.2"
                        },
                        {
                            "ecmp-group-id": "200200",
                            "ecmp-members": [["100008", "4.4.4.4", "56"],["100010", "8.8.8.1", "82"]],
                            "ecmp-dst-member": "100002",
                            "ecmp-dst-port": "62",
                            "ecmp-next-hop-ip": "6.5.4.3"
                        }
                    ]
                }
            ],
            "id": 1
        }

        self.packet_trace_supported_drop_reasons_unknown_method = {
            "jsonrpc": "2.0",
            "method": "get-packet-gummy-drop-reasons",
            "asic-id": "1",
            "version": "1",
            "result": [
                "l2-lookup-failure",
                "vlan-mismatch"
            ],
            "id": 1
        }


        self.packet_trace_supported_drop_reasons_report_dict = {
            "jsonrpc": "2.0",
            "method": "get-packet-trace-supported-drop-reasons",
            "asic-id": "1",
            "version": "1",
            "result": {},
            "id": 1
        }

        self.packet_trace_supported_drop_reasons_empty_report = {
            "jsonrpc": "2.0",
            "method": "get-packet-trace-supported-drop-reasons",
            "asic-id": "1",
            "version": "1",
            "result": [],
            "id": 1
        }

        self.packet_trace_supported_drop_reasons_missing_report = {
            "jsonrpc": "2.0",
            "method": "get-packet-trace-supported-drop-reasons",
            "asic-id": "1",
            "version": "1",
            "id": 1
        }

        self.packet_trace_supported_drop_reasons = {
            "jsonrpc": "2.0",
            "method": "get-packet-trace-supported-drop-reasons",
            "asic-id": "1",
            "version": "1",
            "result": [
                "l2-lookup-failure",
                "vlan-mismatch"
            ],
            "id": 1
        }

        self.packet_trace_drop_reason_unknown_method = {
            "jsonrpc": "2.0",
            "method": "get-packet-xxxxx-trace-drop-reason",
            "asic-id": "1",
            "version": "1",
            "result": [
                {
                    "reason": "l2-lookup-failure",
                    "port-list": [
                        "1",
                        "5",
                        "6",
                        "10-15"
                    ],
                    "send-dropped-packet": 1,
                    "trace-profile": 0,
                    "packet-count": 3,
                    "packet-threshold": 0
                },
                {
                    "reason": "vlan-mismatch",
                    "port-list": [
                        "1",
                        "5",
                        "6",
                        "10-15"
                    ],
                    "send-dropped-packet": 1,
                    "trace-profile": 1,
                    "packet-count": 3,
                    "packet-threshold": 10
                }
            ],
            "id": 1
        }

        self.packet_trace_drop_reason_missing_reason = {
            "jsonrpc": "2.0",
            "method": "get-packet-trace-drop-reason",
            "asic-id": "1",
            "version": "1",
            "result": [
                {
                    "port-list": [
                        "1",
                        "5",
                        "6",
                        "10-15"
                    ],
                    "send-dropped-packet": 1,
                    "trace-profile": 0,
                    "packet-count": 3,
                    "packet-threshold": 0
                },
                {
                    "reason": "vlan-mismatch",
                    "port-list": [
                        "1",
                        "5",
                        "6",
                        "10-15"
                    ],
                    "send-dropped-packet": 1,
                    "trace-profile": 1,
                    "packet-count": 3,
                    "packet-threshold": 10
                }
            ],
            "id": 1
        }

        self.packet_trace_drop_reason_missing_port_list = {
            "jsonrpc": "2.0",
            "method": "get-packet-trace-drop-reason",
            "asic-id": "1",
            "version": "1",
            "result": [
                {
                    "port-list": [
                        "1",
                        "5",
                        "6",
                        "10-15"
                    ],
                    "send-dropped-packet": 1,
                    "trace-profile": 0,
                    "packet-count": 3,
                    "packet-threshold": 0
                },
                {
                    "reason": "vlan-mismatch",
                    "port-list": [
                        "1",
                        "5",
                        "6",
                        "10-15"
                    ],
                    "send-dropped-packet": 1,
                    "trace-profile": 1,
                    "packet-count": 3,
                    "packet-threshold": 10
                }
            ],
            "id": 1
        }

        self.packet_trace_drop_reason_missing_send_dropped_packet = {
            "jsonrpc": "2.0",
            "method": "get-packet-trace-drop-reason",
            "asic-id": "1",
            "version": "1",
            "result": [
                {
                    "port-list": [
                        "1",
                        "5",
                        "6",
                        "10-15"
                    ],
                    "send-dropped-packet": 1,
                    "trace-profile": 0,
                    "packet-count": 3,
                    "packet-threshold": 0
                },
                {
                    "reason": "vlan-mismatch",
                    "port-list": [
                        "1",
                        "5",
                        "6",
                        "10-15"
                    ],
                    "send-dropped-packet": 1,
                    "trace-profile": 1,
                    "packet-count": 3,
                    "packet-threshold": 10
                }
            ],
            "id": 1
        }

        self.packet_trace_drop_reason_missing_trace_profile = {
            "jsonrpc": "2.0",
            "method": "get-packet-trace-drop-reason",
            "asic-id": "1",
            "version": "1",
            "result": [
                {
                    "port-list": [
                        "1",
                        "5",
                        "6",
                        "10-15"
                    ],
                    "send-dropped-packet": 1,
                    "trace-profile": 0,
                    "packet-count": 3,
                    "packet-threshold": 0
                },
                {
                    "reason": "vlan-mismatch",
                    "port-list": [
                        "1",
                        "5",
                        "6",
                        "10-15"
                    ],
                    "send-dropped-packet": 1,
                    "trace-profile": 1,
                    "packet-count": 3,
                    "packet-threshold": 10
                }
            ],
            "id": 1
        }

        self.packet_trace_drop_reason_missing_packet_count = {
            "jsonrpc": "2.0",
            "method": "get-packet-trace-drop-reason",
            "asic-id": "1",
            "version": "1",
            "result": [
                {
                    "port-list": [
                        "1",
                        "5",
                        "6",
                        "10-15"
                    ],
                    "send-dropped-packet": 1,
                    "trace-profile": 0,
                    "packet-count": 3,
                    "packet-threshold": 0
                },
                {
                    "reason": "vlan-mismatch",
                    "port-list": [
                        "1",
                        "5",
                        "6",
                        "10-15"
                    ],
                    "send-dropped-packet": 1,
                    "trace-profile": 1,
                    "packet-count": 3,
                    "packet-threshold": 10
                }
            ],
            "id": 1
        }

        self.packet_trace_drop_reason_missing_packet_threshold = {
            "jsonrpc": "2.0",
            "method": "get-packet-trace-drop-reason",
            "asic-id": "1",
            "version": "1",
            "result": [
                {
                    "port-list": [
                        "1",
                        "5",
                        "6",
                        "10-15"
                    ],
                    "send-dropped-packet": 1,
                    "trace-profile": 0,
                    "packet-count": 3,
                    "packet-threshold": 0
                },
                {
                    "reason": "vlan-mismatch",
                    "port-list": [
                        "1",
                        "5",
                        "6",
                        "10-15"
                    ],
                    "send-dropped-packet": 1,
                    "trace-profile": 1,
                    "packet-count": 3,
                    "packet-threshold": 10
                }
            ],
            "id": 1
        }

        self.packet_trace_drop_reason_report_dict = {
            "jsonrpc": "2.0",
            "method": "get-packet-trace-drop-reason",
            "asic-id": "1",
            "version": "1",
            "result": {}
        }

        self.packet_trace_drop_reason_empty_report = {
            "jsonrpc": "2.0",
            "method": "get-packet-trace-drop-reason",
            "asic-id": "1",
            "version": "1",
            "result": [],
            "id": 1
        }

        self.packet_trace_drop_reason_missing_report = {
            "jsonrpc": "2.0",
            "method": "get-packet-trace-drop-reason",
            "asic-id": "1",
            "version": "1",
            "id": 1
        }

        self.packet_trace_drop_reason = {
            "jsonrpc": "2.0",
            "method": "get-packet-trace-drop-reason",
            "asic-id": "1",
            "version": "1",
            "result": [
                {
                    "reason": "l2-lookup-failure",
                    "port-list": [
                        "1",
                        "5",
                        "6",
                        "10-15"
                    ],
                    "send-dropped-packet": 1,
                    "trace-profile": 0,
                    "packet-count": 3,
                    "packet-threshold": 0
                },
                {
                    "reason": "vlan-mismatch",
                    "port-list": [
                        "2",
                        "10",
                        "12",
                        "20-30"
                    ],
                    "send-dropped-packet": 1,
                    "trace-profile": 1,
                    "packet-count": 6,
                    "packet-threshold": 10
                }
            ],
            "id": 1
        }

        self.packet_trace_drop_counter_report_unknown_method = {
            "jsonrpc": "2.0",
            "method": " get-packet-unknown-drop-counter-report",
            "asic-id": "1",
            "version": "1",
            "report": [
                {
                    "realm": "vlan-xlate-miss-drop",
                    "data": [
                        {
                            "port": "1",
                            "count": 10
                        },
                        {
                            "port": "5",
                            "count": 20
                        },
                        {
                            "port": "6",
                            "count": 30
                        },
                        {
                            "port": "10",
                            "count": 40
                        },
                        {
                            "port": "11",
                            "count": 50
                        },
                        {
                            "port": "12",
                            "count": 60
                        }
                    ]
                },
                {
                    "realm": "bpdu-drop",
                    "data": [
                        {
                            "port": "1",
                            "count": 70
                        },
                        {
                            "port": "5",
                            "count": 20
                        },
                        {
                            "port": "6",
                            "count": 30
                        },
                        {
                            "port": "10",
                            "count": 40
                        },
                        {
                            "port": "11",
                            "count": 80
                        },
                        {
                            "port": "12",
                            "count": 90
                        }
                    ]
                },
                {
                    "realm": "trill-slowpath-drop",
                    "data": [
                        {
                            "port": "1",
                            "count": 10
                        },
                        {
                            "port": "5",
                            "count": 20
                        },
                        {
                            "port": "6",
                            "count": 30
                        },
                        {
                            "port": "10",
                            "count": 40
                        },
                        {
                            "port": "11",
                            "count": 50
                        },
                        {
                            "port": "12",
                            "count": 60
                        }
                    ]
                }
            ]
        }

        self.packet_trace_drop_counter_report_missing_realm = {
            "jsonrpc": "2.0",
            "method": " get-packet-trace-drop-counter-report",
            "asic-id": "1",
            "version": "1",
            "report": [
                {
                    "data": [
                        {
                            "port": "1",
                            "count": 10
                        },
                        {
                            "port": "5",
                            "count": 20
                        },
                        {
                            "port": "6",
                            "count": 30
                        },
                        {
                            "port": "10",
                            "count": 40
                        },
                        {
                            "port": "11",
                            "count": 50
                        },
                        {
                            "port": "12",
                            "count": 60
                        }
                    ]
                },
                {
                    "data": [
                        {
                            "port": "1",
                            "count": 70
                        },
                        {
                            "port": "5",
                            "count": 20
                        },
                        {
                            "port": "6",
                            "count": 30
                        },
                        {
                            "port": "10",
                            "count": 40
                        },
                        {
                            "port": "11",
                            "count": 80
                        },
                        {
                            "port": "12",
                            "count": 90
                        }
                    ]
                },
                {
                    "realm": "trill-unknown-slowpath-drop",
                    "data": [
                        {
                            "port": "1",
                            "count": 10
                        },
                        {
                            "port": "5",
                            "count": 20
                        },
                        {
                            "port": "6",
                            "count": 30
                        },
                        {
                            "port": "10",
                            "count": 40
                        },
                        {
                            "port": "11",
                            "count": 50
                        },
                        {
                            "port": "12",
                            "count": 60
                        }
                    ]
                }
            ]
        }

        self.packet_trace_drop_counter_report_report_dict = {
            "jsonrpc": "2.0",
            "method": " get-packet-trace-drop-counter-report",
            "asic-id": "1",
            "version": "1",
            "report": {}
        }

        self.packet_trace_drop_counter_report_empty_report = {
            "jsonrpc": "2.0",
            "method": " get-packet-trace-drop-counter-report",
            "asic-id": "1",
            "version": "1",
            "report": [
            ]
        }

        self.packet_trace_drop_counter_report_missing_report = {
            "jsonrpc": "2.0",
            "method": " get-packet-trace-drop-counter-report",
            "asic-id": "1",
            "version": "1"
        }

        self.packet_trace_drop_counter_report = {
            "jsonrpc": "2.0",
            "method": " get-packet-trace-drop-counter-report",
            "asic-id": "1",
            "version": "1",
            "report": [
                {
                    "realm": "vlan-xlate-miss-drop",
                    "data": [
                        {
                            "port": "1",
                            "count": 10
                        },
                        {
                            "port": "5",
                            "count": 20
                        },
                        {
                            "port": "6",
                            "count": 30
                        },
                        {
                            "port": "10",
                            "count": 40
                        },
                        {
                            "port": "11",
                            "count": 50
                        },
                        {
                            "port": "12",
                            "count": 60
                        }
                    ]
                },
                {                    
                    "realm": "bpdu-drop",
                    "data": [
                        {
                            "port": "11",
                            "count": 700
                        },
                        {
                            "port": "15",
                            "count": 200
                        },
                        {
                            "port": "16",
                            "count": 300
                        },
                        {
                            "port": "20",
                            "count": 400
                        },
                        {
                            "port": "21",
                            "count": 800
                        },
                        {
                            "port": "22",
                            "count": 900
                        }
                    ]
                },
                {
                    "realm": "trill-slowpath-drop",
                    "data": [
                        {
                            "port": "51",
                            "count": 310
                        },
                        {
                            "port": "55",
                            "count": 320
                        },
                        {
                            "port": "56",
                            "count": 330
                        },
                        {
                            "port": "60",
                            "count": 340
                        },
                        {
                            "port": "61",
                            "count": 350
                        },
                        {
                            "port": "62",
                            "count": 360
                        }
                    ]
                }

            ]
        }

    def test_packet_trace_lag_resolution_unknown_method(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_lag_resolution_unknown_method)
        self.assertEqual(ret, False)

    def test_packet_trace_lag_resolution_unknown_realm(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_lag_resolution_unknown_realm)
        self.assertEqual(ret, False)

    def test_packet_trace_lag_resolution_bad_timestamp(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_lag_resolution_bad_timestamp)
        self.assertEqual(ret, False)

    def test_packet_trace_lag_resolution_report_dict(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_lag_resolution_report_dict)
        self.assertEqual(ret, False)

    def test_packet_trace_lag_resolution_empty_report(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_lag_resolution_empty_report)
        self.assertEqual(ret, False)

    def test_packet_trace_lag_resolution_missing_report(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_lag_resolution_missing_report)
        self.assertEqual(ret, False)

    def test_packet_trace_lag_resolution(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_lag_resolution)
        self.assertEqual(ret, True)

        val = rep.getReportType()
        self.assertEqual(val, ReportTypes.PacketTraceLAGResolution)

        val = rep.getPacketTraceLAGResolution()

        for m in val:
            llr = m.getLAGLINKResolution()
            if m.getPort() == "1":
                self.assertEqual(llr.getLAGID(), "1")

                lm = llr.getLAGMembers()
                self.assertEqual(len(lm), 4)
                self.assertEqual(True, "1" in lm)
                self.assertEqual(True, "2" in lm)
                self.assertEqual(True, "3" in lm)
                self.assertEqual(True, "4" in lm)

                self.assertEqual(llr.getDstLAGMember(), "4")
            elif m.getPort() == "2":
                self.assertEqual(llr.getLAGID(), "2")

                lm = llr.getLAGMembers()
                self.assertEqual(len(lm), 4)
                self.assertEqual(True, "5" in lm)
                self.assertEqual(True, "6" in lm)
                self.assertEqual(True, "7" in lm)
                self.assertEqual(True, "8" in lm)

                self.assertEqual(llr.getDstLAGMember(), "7")
            else:
                self.assertEqual("unexpected port {}".format(llr.getPort()), True)

    def test_packet_trace_ecmp_resolution_unknown_method(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_ecmp_resolution_unknown_method)
        self.assertEqual(ret, False)

    def test_packet_trace_ecmp_resolution_unknown_realm(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_ecmp_resolution_unknown_realm)
        self.assertEqual(ret, False)

    def test_packet_trace_ecmp_resolution_bad_timestamp(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_ecmp_resolution_bad_timestamp)
        self.assertEqual(ret, False)

    def test_packet_trace_ecmp_resolution_report_dict(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_ecmp_resolution_report_dict)
        self.assertEqual(ret, False)

    def test_packet_trace_ecmp_resolution_empty_report(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_ecmp_resolution_empty_report)
        self.assertEqual(ret, False)

    def test_packet_trace_ecmp_resolution_missing_report(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_ecmp_resolution_missing_report)
        self.assertEqual(ret, False)

    def test_packet_trace_ecmp_resolution(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_ecmp_resolution)
        self.assertEqual(ret, True)

        val = rep.getReportType()
        self.assertEqual(val, ReportTypes.PacketTraceECMPResolution)

        val = rep.getPacketTraceECMPResolution()

        for m in val:
            llr = m.getECMPLINKResolution()
            if m.getPort() == "1":
                for x in llr:
                    if x.getECMPGroupID() == "200256":
                        lm = x.getECMPMembers()
                        self.assertEqual(len(lm), 2)
                        self.assertTrue(lm[0].getId() == "100004")
                        self.assertTrue(lm[0].getIP() == "2.2.2.2")
                        self.assertTrue(lm[0].getPort() == "28")
                        self.assertTrue(lm[1].getId() == "100005")
                        self.assertTrue(lm[1].getIP() == "6.6.6.1")
                        self.assertTrue(lm[1].getPort() == "41")

                        self.assertEqual(x.getECMPDstMember(), "100005")
                        self.assertEqual(x.getECMPDstPort(), "41")
                        self.assertEqual(x.getECMPNextHopIP(), "6.6.6.2")

                    elif x.getECMPGroupID() == "200100":
                        lm = x.getECMPMembers()
                        self.assertEqual(len(lm), 2)
                        self.assertTrue(lm[0].getId() == "100001")
                        self.assertTrue(lm[0].getIP() == "3.3.3.1")
                        self.assertTrue(lm[0].getPort() == "31")
                        self.assertTrue(lm[1].getId() == "100002")
                        self.assertTrue(lm[1].getIP() == "7.7.7.2")
                        self.assertTrue(lm[1].getPort() == "21")
                        self.assertEqual(x.getECMPDstMember(), "100001")
                        self.assertEqual(x.getECMPDstPort(), "31")
                        self.assertEqual(x.getECMPNextHopIP(), "3.3.3.2")
                    else:
                        self.assertEqual("unexpected group-id {}".format(x.getECMPGroupID()), True)
                
            elif m.getPort() == "2":
                for x in llr:
                    if x.getECMPGroupID() == "200512":
                        lm = x.getECMPMembers()
                        self.assertEqual(len(lm), 2)
                        self.assertTrue(lm[0].getId() == "100002")
                        self.assertTrue(lm[0].getIP() == "6.3.3.1")
                        self.assertTrue(lm[0].getPort() == "61")
                        self.assertTrue(lm[1].getId() == "100004")
                        self.assertTrue(lm[1].getIP() == "9.9.9.2")
                        self.assertTrue(lm[1].getPort() == "41")

                        self.assertEqual(x.getECMPDstMember(), "100010")
                        self.assertEqual(x.getECMPDstPort(), "81")
                        self.assertEqual(x.getECMPNextHopIP(), "7.6.6.2")
                    elif x.getECMPGroupID() == "200200":
                        lm = x.getECMPMembers()
                        self.assertEqual(len(lm), 2)
                        self.assertTrue(lm[0].getId() == "100008")
                        self.assertTrue(lm[0].getIP() == "4.4.4.4")
                        self.assertTrue(lm[0].getPort() == "56")
                        self.assertTrue(lm[1].getId() == "100010")
                        self.assertTrue(lm[1].getIP() == "8.8.8.1")
                        self.assertTrue(lm[1].getPort() == "82")

                        self.assertEqual(x.getECMPDstMember(), "100002")
                        self.assertEqual(x.getECMPDstPort(), "62")
                        self.assertEqual(x.getECMPNextHopIP(), "6.5.4.3")
                    else:
                        self.assertEqual("unexpected group-id {}".format(x.getECMPGroupID()), True)
                
            else:
                self.assertEqual("unexpected port {}".format(llr.getPort()), True)

    def test_packet_trace_supported_drop_reasons_unknown_method(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_supported_drop_reasons_unknown_method)
        self.assertEqual(ret, False)

    def test_packet_trace_supported_drop_reasons_report_dict(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_supported_drop_reasons_report_dict)
        self.assertEqual(ret, False)

    def test_packet_trace_supported_drop_reasons_empty_report(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_supported_drop_reasons_empty_report)
        self.assertEqual(ret, False)

    def test_packet_trace_supported_drop_reasons_missing_report(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_supported_drop_reasons_missing_report)
        self.assertEqual(ret, False)

    def test_packet_trace_supported_drop_reasons(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_supported_drop_reasons)
        self.assertEqual(ret, True)

        val = rep.getReportType()
        self.assertEqual(val, ReportTypes.PacketTraceSupportedDropReasons)

        val = rep.getPacketTraceSupportedDropReasons().getReasons()

        self.assertTrue("l2-lookup-failure" in val)
        self.assertTrue("vlan-mismatch" in val)

    def test_packet_trace_drop_reason_unknown_method(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_drop_reason_unknown_method)
        self.assertEqual(ret, False)

    def test_packet_trace_drop_reason_missing_reason(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_drop_reason_missing_reason)
        self.assertEqual(ret, False)

    def test_packet_trace_drop_reason_missing_port_list(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_drop_reason_missing_port_list)
        self.assertEqual(ret, False)

    def test_packet_trace_drop_reason_missing_send_dropped_packet(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_drop_reason_missing_send_dropped_packet)
        self.assertEqual(ret, False)

    def test_packet_trace_drop_reason_missing_trace_profile(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_drop_reason_missing_trace_profile)
        self.assertEqual(ret, False)

    def test_packet_trace_drop_reason_missing_packet_count(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_drop_reason_missing_packet_count)
        self.assertEqual(ret, False)

    def test_packet_trace_drop_reason_missing_packet_threshold(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_drop_reason_missing_packet_threshold)
        self.assertEqual(ret, False)

    def test_packet_trace_drop_reason_report_dict(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_drop_reason_report_dict)
        self.assertEqual(ret, False)

    def test_packet_trace_drop_reason_empty_report(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_drop_reason_empty_report)
        self.assertEqual(ret, False)

    def test_packet_trace_drop_reason_missing_report(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_drop_reason_missing_report)
        self.assertEqual(ret, False)

    def test_packet_trace_drop_reason(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_drop_reason)
        self.assertEqual(ret, True)

        val = rep.getReportType()
        self.assertEqual(val, ReportTypes.PacketTraceDropReason)

        val = rep.getPacketTraceDropReason()

        for x in val:
            if x.getReason() == "l2-lookup-failure":
                portList = x.getPortList()
                self.assertTrue("1" in portList)
                self.assertTrue("5" in portList)
                self.assertTrue("6" in portList)
                self.assertTrue("10-15" in portList)
                self.assertEqual(x.getSendDroppedPacket(), True)
                self.assertEqual(x.getTraceProfile(), False)
                self.assertEqual(x.getPacketCount(), 3)
                self.assertEqual(x.getPacketThreshold(), 0)
            elif x.getReason() == "vlan-mismatch":
                portList = x.getPortList()
                self.assertTrue("2" in portList)
                self.assertTrue("10" in portList)
                self.assertTrue("12" in portList)
                self.assertTrue("20-30" in portList)
                self.assertEqual(x.getSendDroppedPacket(), True)
                self.assertEqual(x.getTraceProfile(), True)
                self.assertEqual(x.getPacketCount(), 6)
                self.assertEqual(x.getPacketThreshold(), 10)
            else:
                self.assertEqual(True, "unrecognized reason {}".format(x.getReason()))

    # packet_trace_drop_counter_report

    def test_packet_trace_drop_counter_report_unknown_method(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_drop_counter_report_unknown_method)
        self.assertEqual(ret, False)

    def test_packet_trace_drop_counter_report_missing_realm(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_drop_counter_report_missing_realm)
        self.assertEqual(ret, False)

    def test_packet_trace_drop_counter_report_report_dict(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_drop_counter_report_report_dict)
        self.assertEqual(ret, False)

    def test_packet_trace_drop_counter_report_empty_report(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_drop_counter_report_empty_report)
        self.assertEqual(ret, False)

    def test_packet_trace_drop_counter_report_missing_report(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_drop_counter_report_missing_report)
        self.assertEqual(ret, False)

    def test_packet_trace_drop_counter_report(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_drop_counter_report)
        self.assertEqual(ret, True)

        val = rep.getReportType()
        self.assertEqual(val, ReportTypes.PacketTraceDropCounterReport)

        val = rep.getPacketTraceDropCounterReport()

        for x in val:
            for y in x:
                realm = y.getRealm()

                if realm == "vlan-xlate-miss-drop":
                    port = y.getPort()
                    count = y.getCount()
                    if port == "1":
                        self.assertEqual(count, 10)
                    elif port == "5":
                        self.assertEqual(count, 20)
                    elif port == "6":
                        self.assertEqual(count, 30)
                    elif port == "10":
                        self.assertEqual(count, 40)
                    elif port == "11":
                        self.assertEqual(count, 50)
                    elif port == "12":
                        self.assertEqual(count, 60)
                    else:
                        self.assertEqual(True, "unknown port {}".format(port))
                
                elif realm == "bpdu-drop":
                    port = y.getPort()
                    count = y.getCount()
                    if port == "11":
                        self.assertEqual(count, 700)
                    elif port == "15":
                        self.assertEqual(count, 200)
                    elif port == "16":
                        self.assertEqual(count, 300)
                    elif port == "20":
                        self.assertEqual(count, 400)
                    elif port == "21":
                        self.assertEqual(count, 800)
                    elif port == "22":
                        self.assertEqual(count, 900)
                    else:
                        self.assertEqual(True, "unknown port {}".format(port))
                elif realm == "trill-slowpath-drop":
                    port = y.getPort()
                    count = y.getCount()
                    if port == "51":
                        self.assertEqual(count, 310)
                    elif port == "55":
                        self.assertEqual(count, 320)
                    elif port == "56":
                        self.assertEqual(count, 330)
                    elif port == "60":
                        self.assertEqual(count, 340)
                    elif port == "61":
                        self.assertEqual(count, 350)
                    elif port == "62":
                        self.assertEqual(count, 360)
                    else:
                        self.assertEqual(True, "unknown port {}".format(port))
                else:
                    self.assertEqual(True, "unknown realm {}".format(realm))

    def test_packet_trace_profile_unknown_method(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_profile_unknown_method)
        self.assertEqual(ret, False)

    def test_packet_trace_profile_unknown_realm(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_profile_unknown_realm)
        self.assertEqual(ret, False)

    def test_packet_trace_profile_bad_timestamp(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_profile_bad_timestamp)
        self.assertEqual(ret, False)

    def test_packet_trace_profile_report_dict(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_profile_report_dict)
        self.assertEqual(ret, False)

    def test_packet_trace_profile_empty_report(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_profile_empty_report)
        self.assertEqual(ret, False)

    def test_packet_trace_profile_missing_report(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_profile_missing_report)
        self.assertEqual(ret, False)

    def test_packet_trace_profile(self):
        rep = PTParser()
        ret = rep.process(self.packet_trace_profile)
        self.assertEqual(ret, True)

        val = rep.getReportType()
        self.assertEqual(val, ReportTypes.PacketTraceProfile)

        val = rep.getPacketTraceProfile()

        for n in val:
            for m in n:
                realm = m.getRealm()
                if realm == "lag-link-resolution":
                    llr = m.getLAGLINKResolution()
                    if m.getPort() == "1":
                        self.assertEqual(llr.getLAGID(), "2")

                        lm = llr.getLAGMembers()
                        self.assertEqual(len(lm), 4)
                        self.assertEqual(True, "1" in lm)
                        self.assertEqual(True, "2" in lm)
                        self.assertEqual(True, "3" in lm)
                        self.assertEqual(True, "4" in lm)

                        self.assertEqual(llr.getDstLAGMember(), "4")
                    elif m.getPort() == "2":
                        self.assertEqual(llr.getLAGID(), "3")

                        lm = llr.getLAGMembers()
                        self.assertEqual(len(lm), 4)
                        self.assertEqual(True, "5" in lm)
                        self.assertEqual(True, "6" in lm)
                        self.assertEqual(True, "7" in lm)
                        self.assertEqual(True, "8" in lm)

                        self.assertEqual(llr.getDstLAGMember(), "6")
                    else:
                        self.assertEqual("unexpected port {}".format(llr.getPort()), True)
                elif realm == "ecmp-link-resolution":
                    elr = m.getECMPLINKResolution()

                    if m.getPort() == "1":
                        for x in elr:
                            if x.getECMPGroupID() == "200256":  
                                em = x.getECMPMembers()
                                self.assertEqual(len(em), 2)

                                self.assertEqual(em[0].getId(), "100004")
                                self.assertEqual(em[0].getIP(), "2.2.2.2")
                                self.assertEqual(em[0].getPort(), "28")

                                self.assertEqual(em[1].getId(), "100005")
                                self.assertEqual(em[1].getIP(), "6.6.6.1")
                                self.assertEqual(em[1].getPort(), "41")

                                self.assertEqual(x.getECMPDstMember(), "100005")
                                self.assertEqual(x.getECMPDstPort(), "41")
                                self.assertEqual(x.getECMPNextHopIP(), "6.6.6.2")
                            elif x.getECMPGroupID() == "200100":  
                                em = x.getECMPMembers()
                                self.assertEqual(len(em), 2)

                                self.assertEqual(em[0].getId(), "100001")
                                self.assertEqual(em[0].getIP(), "3.3.3.1")
                                self.assertEqual(em[0].getPort(), "31")

                                self.assertEqual(em[1].getId(), "100002")
                                self.assertEqual(em[1].getIP(), "7.7.7.2")
                                self.assertEqual(em[1].getPort(), "21")

                                self.assertEqual(x.getECMPDstMember(), "100001")
                                self.assertEqual(x.getECMPDstPort(), "31")
                                self.assertEqual(x.getECMPNextHopIP(), "3.3.3.2")
                            else:
                                self.assertEqual(False, True)
                    elif m.getPort() == "2":
                        for x in elr:
                            if x.getECMPGroupID() == "200512":
                                em = x.getECMPMembers()
                                self.assertEqual(len(em), 2)

                                self.assertEqual(em[0].getId(), "200004")
                                self.assertEqual(em[0].getIP(), "3.2.2.2")
                                self.assertEqual(em[0].getPort(), "38")

                                self.assertEqual(em[1].getId(), "100005")
                                self.assertEqual(em[1].getIP(), "6.6.6.1")
                                self.assertEqual(em[1].getPort(), "41")

                                self.assertEqual(x.getECMPDstMember(), "100010")
                                self.assertEqual(x.getECMPDstPort(), "19")
                                self.assertEqual(x.getECMPNextHopIP(), "8.8.8.2")
                            elif x.getECMPGroupID() == "200200":
                                em = x.getECMPMembers()
                                self.assertEqual(len(em), 2)

                                self.assertEqual(em[0].getId(), "100002")
                                self.assertEqual(em[0].getIP(), "4.3.3.1")
                                self.assertEqual(em[0].getPort(), "76")

                                self.assertEqual(em[1].getId(), "100002")
                                self.assertEqual(em[1].getIP(), "7.7.7.2")
                                self.assertEqual(em[1].getPort(), "21")

                                self.assertEqual(x.getECMPDstMember(), "100002")
                                self.assertEqual(x.getECMPDstPort(), "55")
                                self.assertEqual(x.getECMPNextHopIP(), "7.3.3.2")
                            else:
                                self.assertEqual(False, True)
                    else:
                        self.assertEqual("unexpected port {}".format(m.getPort()), True)

if __name__ == "__main__":
    unittest.main()
