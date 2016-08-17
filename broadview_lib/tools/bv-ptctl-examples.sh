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

host=10.18.20.217
port=8080

BV_USERNAME=admin
BV_PASSWORD=
BV_AUTH=sidauth

export BV_USERNAME
export BV_PASSWORD
export BV_AUTH

echo "********** get-system-feature **********"
python bv-ctl.py get-system-feature timeout:30 host:$host port:$port 
echo "********** get-switch-properties **********"
python bv-ctl.py get-switch-properties timeout:30 host:$host port:$port 

echo "********** pt cfg-feature **********"
python bv-ptctl.py cfg-feature timeout:30 host:$host port:$port enable 
echo "********** pt get-feature **********"
python bv-ptctl.py get-feature timeout:30 host:$host port:$port 
echo "********** pt cfg-feature **********"
python bv-ptctl.py cfg-feature timeout:30 host:$host port:$port disable 
echo "********** pt get-feature **********"
python bv-ptctl.py get-feature timeout:30 host:$host port:$port 
echo "********** pt cancel-profile **********"
python bv-ptctl.py cancel-profile timeout:30 host:$host port:$port 
echo "********** pt cancel-lag-resolution **********"
python bv-ptctl.py cancel-lag-resolution timeout:30 host:$host port:$port 
echo "********** pt cancel-ecmp-resolution **********"
python bv-ptctl.py cancel-ecmp-resolution timeout:30 host:$host port:$port 
echo "********** pt get-profile **********"
python bv-ptctl.py get-lag-resolution packet:"1MOyoQIABAAAAAAAAAAAAP//AAABAAAANlMKVgAAAABDAAAAQwAAAAAAAAAGAAAO7DIeCoEAAAoAAQIDBAUGBwgJCgsMDQ4PEBESExQVFhcYGRobHB0eHyAhIiMkJSYnKCkqKywtLi8V5EQ=" port-list:"0/4" drop-packet:1 collection-interval:10 timeout:30 host:$host port:$port 

