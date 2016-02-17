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

Code and documentation: https://github.com/Broadcom-Switch/BroadView-Instrumentation 
Product information: https://www.broadcom.com/products/ethernet-communication-and-switching/switching/broadview

## BroadView Agent and broadview-lib

A BroadView agent is software running on platforms that support BroadView. It
exposes a JSON-RPC, REST-like API for configuring the agent to report statistics
such a BST. It also report statistics to agents or collectors that are designed 
to receive these reports. These reports are also transmitted using JSON-RPC.
All connections to and from the agent are based on HTTP 1.1.

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

broadview-lib is, like BroadView itself, designed to be extensible. In this
release, the BroadView BST component is supported. Future releases will add
support for additional BroadView components as they become available.

# Tools

broadview-lib includes bv-bstctl.py, which is a command line application that 
can be used to configure BroadView BST. It also provides an example usage of 
both the configuration and BST parsing APIs in broadview-lib. For usage 
information, please type:

python bv-bstcfg.py help


bv-bstctl.py writes its output to stdout in JSON format.

The file examples.sh in the tools directory contains usage example for the
bv-bstcfg application and can be used to exercise bv-bsctl.

# Classes

The following describes the major classes in the library.

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

device - ConfigureDeviceThreshold 
egress-cpu-queue - ConfigureEgressCpuQueueThreshold
egress-rqe-queue - ConfigureEgressRqeQueueThreshold
egress-port-service-pool - ConfigureEgressPortServicePoolThreshold
egress-service-pool - ConfigureEgressServicePoolThreshold
egress-uc-queue - ConfigureEgressUcQueueThreshold
egress-uc-queue-group - ConfigureEgressUcQueueGroupThreshold
egress-mc-queue - ConfigureEgressMcQueueThreshold
ingress-port-priority-group - ConfigureIngressPortPriorityGroupThreshold
ingress-port-service-pool - ConfigureIngressPortServicePoolThreshold
ingress-service-pool - ConfigureIngressServicePoolThreshold

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

