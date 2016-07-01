# Authentication

broadview-lib uses python "requests" module for issuing HTTP 1.1 POST
requests to the agent. In some cases, authentication is required by the
device. The requests module methods (e.g., post(), get()) support an
auth keyword argument which can be used to specify an instance of an
object that derives from requests.auth.AuthBase, and handle the tasks
related to authentication. More information can
be found here: http://docs.python-requests.org/en/master/user/authentication/

In broadview_lib/agentconnection.py we've included support for three such
objects:

* requests.HTTPBasicAuth
* requests.HTTPDigestAuth
* SIDAuth

HTTPBasicAuth and HTTPDigestAuth are documented on the Requests page linked
to above, and are provided by the requests module. SIDAuth is supplied as a 
class by broadview-lib in config/siduath.py to provide authentication to 
switches which are running the ICOS NOS.

## Specifying Authentication Settings

To use one of the above authentication methods, you must identify the 
method, and supply a username and password for the device that you are
trying to connect to. There are two methods for doing this supported by
broadview-lib:

* environment variables
* configuration in /etc/broadviewswitches.conf

Note: if a HTTP 401 error is returned by the agent and WWW-Authenticate header 
is supplied by the server (as required by RFC 2616) then the authentation 
method specified in the WWW-Authenticate header is used. Otherwise, the method 
is determined by looking at either the environment variable or the setting in 
/etc/broadviewswitches.conf. 

The settings file has priority over environment variables. In other words,
if both specify a value, the settings file value is used, and the environment
variable value will be ignored.

The following sections detail each method.

### Authentication Environment Variables

Three environment variables can be used to specify authentication settings:

* BV_AUTH - a string that specifies the authentication method. Supported 
values include "basic", for HTTPBasicAuth, "digest", for HTTPDigestAuth,
and "sidauth", for SIDAuth authentication. Use this variable only against
devices that are not providing a WWW-Authenticate header.
* BV_USERNAME - a string that contains the username used for authentication 
* BV_PASSWORD - a string that contains the password used for authentication 

BV_AUTH is ignored if WWW-Authenticate header is present in the HTTP 401
response.

Each environment variable will be ignored if a corresponding value is present
in /etc/broadviewswitches.conf.

### Authentication settings in /etc/broadviewswitches.conf

The broadviewswitches.conf was originally designed to provide topology 
information for the BroadView horizon dashboard in OpenStack. It was extended
to support 3 additional settings per switch:

* auth - a string that specifies the authentication method. Supported
values include "basic", for HTTPBasicAuth, "digest", for HTTPDigestAuth,
and "sidauth", for SIDAuth authentication. Use this variable only against
devices that are not providing a WWW-Authenticate header.
* username - a string that contains the username used for authentication
* password - a string that contains the password used for authentication

These settings will override the corresponding environment variables, as
defined in the previous section. auth is overridden on a per-response
basis if WWW-Authenticate is present in the HTTP 401 response headers.

The following is an example /etc/broadviewswitches.conf file.

    [topology]

    bst_switches = [ { "ip": "10.14.244.119", "port": 80, \
    "description" : "switch 1", "auth": "sidauth", \
    "username": "admin", "password": ""}, \
    { "ip": "10.27.31.1", "port": 80, "description" : "switch 2", \
    "auth": "sidauth", "username": "admin", "password": "" } ] 

