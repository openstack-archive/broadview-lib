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

host=10.14.244.128

echo "********** cfg-feature **********"
python bv-bstctl.py cfg-feature timeout:30 host:$host enable send_async_reports
echo "********** get-feature **********"
python bv-bstctl.py get-feature host:$host 
echo "********** cfg-tracking **********"
python bv-bstctl.py cfg-tracking host:$host track_ingress_port_priority_group
echo "********** get-tracking **********"
python bv-bstctl.py get-tracking host:$host 
echo "********** clr-statistics **********"
python bv-bstctl.py clr-statistics host:$host 
echo "********** clr-thresholds **********"
python bv-bstctl.py clr-thresholds host:$host 
echo "********** cfg-thresholds **********"
python bv-bstctl.py get-thresholds host:$host include_ingress_port_priority_group include_ingress_port_service_pool include_ingress_service_pool include_egress_port_service_pool include_egress_service_pool
echo "********** get-report **********"
python bv-bstctl.py get-report host:$host include_ingress_port_priority_group include_ingress_port_service_pool include_ingress_service_pool include_egress_port_service_pool include_egress_service_pool
echo "********** cfg-thresholds device **********"
python bv-bstctl.py cfg-thresholds host:$host device:10100 
echo "********** cfg-thresholds egress-cpu-queue **********"
python bv-bstctl.py cfg-thresholds host:$host egress-cpu-queue:5:20202
echo "********** cfg-thresholds egress-rqe-queue **********"
python bv-bstctl.py cfg-thresholds host:$host egress-rqe-queue:6:30130 
echo "********** cfg-thresholds egress-port-service-pool **********"
python bv-bstctl.py cfg-thresholds host:$host egress-port-service-pool:"2":2:204556:30000:40000:5000 
echo "********** cfg-thresholds egress-service-pool **********"
python bv-bstctl.py cfg-thresholds host:$host egress-service-pool:2:30:40:50
echo "********** cfg-thresholds egress-uc-queue **********"
python bv-bstctl.py cfg-thresholds host:$host egress-uc-queue:5:20200 
echo "********** cfg-thresholds egress-uc-queue-group **********"
python bv-bstctl.py cfg-thresholds host:$host egress-uc-queue-group:5:204
echo "********** cfg-thresholds egress-mc-queue **********"
python bv-bstctl.py cfg-thresholds host:$host egress-mc-queue:5:204:10500
echo "********** cfg-thresholds ingress-port-priority-group **********"
python bv-bstctl.py cfg-thresholds host:$host ingress-port-priority-group:"5":2:20456:40404 
echo "********** cfg-thresholds ingress-port-service-pool **********"
python bv-bstctl.py cfg-thresholds host:$host ingress-port-service-pool:"4":2:50505
echo "********** cfg-thresholds ingress-service-pool **********"
python bv-bstctl.py cfg-thresholds host:$host ingress-service-pool:2:56783 
#
