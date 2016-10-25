Note
====

This repo supports versions of BroadView up to, but not including, version
3 of the agent protocol. For all later versions of BroadView, please visit
https://github.com/Broadcom-Switch/broadview-lib.

# Overview

`broadview-lib` is a library that provides an interface to Broadcom's
BroadView instrumentation functionality.

## What is BroadView?

BroadView is an open source software suite that enables advanced analytics in 
next-generation networks. Troubleshooting network problems and ensuring 
application SLAs are very complex tasks. In cloud networks, overlay 
technologies reduce visibility into packet flows, thereby making it even more 
difficult to analyze issues and ensure SLAs. OpenStack projects such as 
Monasca provide monitoring-as-a-service to deliver usage metrics from 
applications and tenant networks; however, underlay monitoring is not 
supported. Ensuring application SLAs requires overlay mapping to the underlay, 
and optimal performance of underlay infrastructure is essential. 

BroadView-based solutions enable programmable access to underlay monitoring, 
facilitating applications to gather advanced analytics in a highly scalable 
manner. 

Buffer Statistics Tracking (BST) is one of the most important features for 
enabling rich congestion analytics. Network Traffic is bursty by nature and 
microbursts occur when there is transient congestion. Microbursts are difficult 
to detect using traditional port drop counts. Broadcom silicon provides the 
ability to monitor MMU buffer utilization counts as part of the BST feature.
It provides network administrators and applications improved telemetry on
the usage of various ingress and egress buffers, without disrupting regular 
packet forwarding operations. There are thousands of counters available across 
various ports, port groups, and service pools that can be utilized by the 
applications for instantaneous monitoring in a scalable way. BST tracks 
ingress-, egress-, and device-based use-counts for both unicast and multicast 
flows. The actual use-counts vary depending on the chip set. 

More information on BroadView, BST, and what they provide can be found at:

* Code and documentation: https://github.com/Broadcom-Switch/BroadView-Instrumentation 
* Product information: https://www.broadcom.com/products/ethernet-communication-and-switching/switching/broadview

## BroadView Agent and broadview-lib

A BroadView agent is software running on platforms that support BroadView. It
exposes a JSON-RPC, REST-like API for configuring the agent to report statistics
such as BST. It also report statistics to agents or collectors that are 
designed to receive these reports. These reports are also transmitted using 
JSON-RPC.  All connections to and from the agent are based on HTTP 1.1.

broadview-lib is designed to provide the underlying infrastructure that is
needed for the development of Python applications that interact with a 
BroadView agent. Using broadview-lib, a Python application can configure a 
BroadView agent and make calls on the agent to perform various tasks. 
broadview-lib also provides classes that can parse notifications and data sent 
to an application by a BroadView agent. broadview-lib can be thought of as 
presenting an object-model above the JSON-RPC protocol of the BroadView agent.

As such, broadview-lib forms the basis of other contributions that integrate
BroadView functionality into OpenStack, and represents an OpenStack-neutral
view of BroadView's API. The library can be used by other projects outside of
OpenStack, if desired.

broadview-lib consists of two components. One is a set of classes that can
be used to configure BroadView. The other is an API that parses content
sent by BroadView agents and presents it as Python objects. 

broadview-lib is, like BroadView itself, designed to be extensible. Currently 
the BroadView BST and PacketTrace components are supported. Future releases 
will add support for additional BroadView components as they become available.

# Tools

broadview-lib includes command line tools that make use of broadview-lib to
to issue supported commands for querying and configuring BroadView. Each 
command line tool is paired to a specific component of BroadView (BST, 
PacketTrace, etc).

Each of these commands supports a "help" argument that will print usage
information. For commands that retrieve a JSON response from the agent, 
the JSON response will be written to stdout.

The file examples.sh in the tools directory contains example invocations
of the supported commands.

Each of the commands provides example usage of broadview-lib APIs and thus
can be used as inspiration for your own broadview-lib applications.

### bv-bstctl.py

A command line application that can be used to configure BroadView BST. 

### bv-ptctl.py

A command line application that can be used to configure BroadView PacketTrace. 

### bv-bhdctl.py

A command line application that can be used to configure BroadView's Black
Hole Detection feature. 

### bv-ctl.py

A command line application that can be used to issue general BroadView
commands for querying the supported features of BroadView, cancelling
requests, etc.

# Classes

The following describes the major classes in the library. 

## General 

The broadview.py file in config contains general configuration classes for
BroadView.

The following briefly summarizes these classes. For example usage, see the
unit test code in broadview.py, or the bv-ctl.py application.

### GetSwitchProperties

This command is used to retrieve the switch properties.

### GetSystemFeature

This command is used to retrieve the current configuration of the System 
module on the Agent. 

### ConfigureSystemFeature

This command can be used to enable or disable heartbeat messages from the
agent, as well as specify a heartbeat interval.

### CancelRequest

All JSON RPC requests to the agent must be identified by a unique integer ID.
The reference implementation of the agent does not provide any support for
managing the ID space, ad it is left to client to ensure that IDs are unique.
broadview-lib supports this by maintaining an ID file that is shared across all
broadview-lib instances on the host and possibly the datacenter should the
ID file be placed in a shared file system. See commit
a72b75082ee961abcdc7da542da6767ee484560e for details on the implementation.

The CancelRequest command takes the ID of a previous request as an argument
and cancels that command on the agent. To obtain this ID, refer to the JSON
output of the corresponding command for the cancellation-id field. Alternately,
Python code using configuration objects can get at this ID for a request by
calling getLastUsedSerial() member function of the object before making another
request with that object (the configuration objects record the last used ID
number within the object, so as long as the object itself is being used in a 
thread safe manner, this ID will be correct).

## BST Configuration and Data Gathering

The bst.py file in config contains various configuration and data gathering 
classes. 

The following briefly summarizes these classes. For example usage, see the
unit test code in bst.py, or the bv-bstctl.py application.

### ConfigureBSTFeature

This class can be used to provide general configuration of the BroadView BST
component.

### ConfigureBSTTracking

This class is used to enable or disable the tracking of various BST statistics.

### ConfigureBSTThresholds

This base class is inherited by the several subclasses, each which allow for
the configuration of thresholds for the various statistics (realms) that
are supported by BST. The following is a list of these subclasses, one for
each supported BST realm:

* device - ConfigureDeviceThreshold 
* egress-cpu-queue - ConfigureEgressCpuQueueThreshold
* egress-rqe-queue - ConfigureEgressRqeQueueThreshold
* egress-port-service-pool - ConfigureEgressPortServicePoolThreshold
* egress-service-pool - ConfigureEgressServicePoolThreshold
* egress-uc-queue - ConfigureEgressUcQueueThreshold
* egress-uc-queue-group - ConfigureEgressUcQueueGroupThreshold
* egress-mc-queue - ConfigureEgressMcQueueThreshold
* ingress-port-priority-group - ConfigureIngressPortPriorityGroupThreshold
* ingress-port-service-pool - ConfigureIngressPortServicePoolThreshold
* ingress-service-pool - ConfigureIngressServicePoolThreshold

### ClearBSTStatistics

This class supports the resetting of all BST statistics in the agent.

### ClearBSTThresholds

This class supports the resetting of all BST thresholds in the agent.

### GetBSTFeature

This class reports the various settings of the BroadView BST component. 

### GetBSTTracking

This class reports the tracking settings for the BroadView BST component. 
The tracking status of each supported realm is reported.

### GetBSTThresholds

This class reports the threshold settings for the various BST realms.

### GetBSTReport

This class reports the current buffer statistics for the specified realms.

## BST Object

The class BSTParser (found in bst/bst_parser.py) accepts the JSON payload
that is sent by a BroadView agent for BST notifications and responses that
contain BST threshold reports.

## Packet Trace Configuration 

The pt.py file in config contains various classes that wrap the BroadView
packet trace protocol.

The following briefly summarizes these classes. For example usage, see the
unit test code in pt.py, or the bv-ptctl.py application.

### ConfigurePacketTraceFeature

This class can be used to provide general configuration of the BroadView
packet trace component.

### ConfigurePacketTraceDropReason

This command configures the agent to send a copy of dropped packets and/or 
trace-profile to requestor asynchronously.

### CancelPacketTraceProfile

This command is used to cancel the trace-profile request previously initiated 
by GetPacketTraceProfile.

### CancelPacketTraceLAGResolution

This command is used to cancel the lag-resolution request previously 
initiated by GetPacketTraceLAGResolution.

### CancelPacketTraceECMPResolution

This command is used to cancel the ecmp-resolution request previously 
initiated by GetPacketTraceECMPResolution.

### CancelPacketTraceSendDropPacket

This command is used to cancel the send-dropped-packet request for a given 
list of ports. This command allows canceling of send-dropped-packet request 
for multiple drop reasons at a time.

### CancelPacketTraceDropCounterReport

This command is used to cancel the drop-counter-report request for a given 
list of ports. This command allows canceling of drop-counter-report request 
for multiple drop reasons at a time.

### GetPacketTraceFeature

This command is used to retrieve the current configuration of the Packet Trace
functionality on the Agent

### GetPacketTraceLAGResolution

This command is used to retrieve the LAG resolution for the given packet.

### GetPacketTraceECMPResolution

This command is used to retrieve the ECMP resolution for the given packet.

### GetPacketTraceProfile

This command is used to retrieve the trace-profile for the given packet.

### GetPacketTraceDropReason

This command is used to retrieve the current configured drop reasons on the
Broadcom ASIC.

### GetPacketTraceDropCounterReport

This command is used to retrieve the drop counter-report. 

### GetPacketTraceSupportedDropReasons

This command is used to retrieve the supported drop reasons on the Broadcom
ASIC.

## PTParser Object

The class PTParser (found in pt/pt_parser.py) accepts the JSON payload
that is sent by a BroadView agent for PacketTrace, and converts this 
payload into Python objects. It provides an API for accessing these objects.

## Black Hole Detection Configuration and Reports

The bhd.py file in config contains various configuration and data gathering 
classes. 

The following briefly summarizes these classes. For example usage, see the
unit test code in bhd.py, or the bv-bhdctl.py application.

### BlackHoleDetectionEnable

This class can be used to enable (or disable) black hole detection.

### ConfigureBlackHole

This class configures the Black Hole Detection functionality on the switch.

### CancelBlackHole

This class nullifies the configuration made by the ConfigureBlackHole class.

### GetBlackHoleDetectionEnable

This class can be used to determine of black hole detection is enabled or not.

### GetBlackHole

This class is used to get the current configuration of black hole detection 
on the agent.

### GetBlackHoleEventReport

This class is used to get a black hole event report. It is only valid if the
agent sampling mode is configured on the agent.

### GetSFlowSamplingStatus

This class is used to get current sFlow sampling status of Black Holed
traffic.

## BHDParser Object

The class BHDParser (found in bhd/bhd_parser.py) accepts the JSON payload
that is sent by a BroadView agent for Black Hole Detection, and converts this 
payload into Python objects. It provides an API for accessing the data that
is contained in these objects.

## Unit tests

To ensure that broadview-lib is decoupled from any (and all) OpenStack 
dependencies, unit tests are implemented by each of the individual Python 
modules using the Python unittest framework. 

# License

(C) Copyright Broadcom Corporation 2016

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.

You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

