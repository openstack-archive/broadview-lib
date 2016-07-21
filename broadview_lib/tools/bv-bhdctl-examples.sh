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
port=8082

echo "********** get-system-feature **********"
python bv-ctl.py get-system-feature timeout:30 host:$host port:$port 
echo "********** get-switch-properties **********"
python bv-ctl.py get-switch-properties timeout:30 host:$host port:$port 

python bv-bhdctl.py configure sampling-method:agent sample-count:100 sample-periodicity:45 port-list:1,2,3,4 water-mark:45 timeout:30 host:$host port:$port 
python bv-bhdctl.py configure sampling-method:sflow vlan-id:1 dst-ip:10.0.0.4 src-udp-port:4567 dst-udp-port:1234 mirror-port:3 sample-pool-size:100 timeout:30 host:$host port:$port 
python bv-bhdctl.py get-detection-enable timeout:30 host:$host port:$port 
python bv-bhdctl.py get timeout:30 host:$host port:$port 
python bv-bhdctl.py get-sflow-sampling-status port-list:1,2,3,4 timeout:30 host:$host port:$port 
python bv-bhdctl.py cancel timeout:30 host:$host port:$port 
python bv-bhdctl.py detection-enable enable:true timeout:30 host:$host port:$port 
