# MTConnect-Python-Agent
## Purpose
Python agent for MTConnect applications.

This library helps store, and format data for MTConnect. The MTConnect standard can be found at [mtconnect.org](https://www.mtconnect.org). This package does not handle the HTTP aspect of the standard just the data processing. It is designed to be used in conjunction with a wsgi interface like flask or django.

At the time of writting the library is not feature complete. The current implementation is to get a minimal MTConnect instance operational. This library supports Devices, Components, DataItems, and Steams. As well as the probe, current, and sample commands.

## Use
To use this library first import the `mtconnect` module.

```
import mtconnect
```

Then create an instance of the MTConnect Agent

```
instance = mtconnect.MTConnect()
```


The instance requires a xml file with the device descriptions. The default location is `./device.xml`. This can be changed by setting the loc value as shown below. This file is in the format of the `Device` element xml and will be returned by the `probe` command. Be aware that only one device is currently supported. There are plans to support multiple devices in the future.

```
instance = mtconnect.MTconnect(loc='./other_device.xml')
```


The instance creation also sets the hostname. This hostname is required by the mtconnect standard in the header of all responses. This can be set by providing the hostname variable as shown below.

```
instance = mtconnect.MTconnect(hostname='10.0.0.1:8000')
```


To push data to the buffer use the following command. The `dataId` is the same as the `id` in the `./device.xml` file. Value must be of the right type or it will error.
```
instance.push_data(dataId, value)
```

To access the commands you can run either of the following commands. The corispond to the `probe`, `sample`, `current` endpoints in the mtconnect standard. To filter by uuid/name use xpath in the format `//*[@name=<name>]` or `//*[@id=<uuid>]` though this functionality is still being worked on and is not fully functional.

```
instance.probe()
instance.sample(path=None, start=None, count=None)
instance.current(at=None, path=None)
```
## Example
Here is a working example using flask. If you would like to see a working implementaiton in a real world example take a look at [this repository](https://github.com/RPIForge/octoprint-companion)

To run this example first install flask and mtconnect using `pip3 install --upgrade mtconnect flask`. And then start the agent with `flask_app=<file_name> python3 -m flask run`. For example if the code is saved in `mttest.py` the command would be `FLASK_APP=mttest python3 -m flask run`

```
from flask import Flask, Response, request
from mtconnect import MTConnect
import json

agent = MTConnect()
app = Flask(__name__)


@app.route('/probe')
def probe():
    response = agent.probe()
    return Response(response.get_xml(),status=response.get_status(), mimetype='text/xml')

@app.route('/current', defaults={'identifier': None})
@app.route('/<identifier>/current')
def current(identifier):
    path = request.args.get('path', None)
    at = request.args.get('at', None, type=int)

    if(identifier is not None):
        path = ".//*[@id='{}'] | .//*[@name='{}']".format(identifier,identifier)

    response = agent.current(at, path)
    return Response(response.get_xml(),status=response.get_status(), mimetype='text/xml')

@app.route('/sample', defaults={'identifier': None})
@app.route('/<identifier>/sample')
def sample(identifier):
    path = request.args.get('path', None)
    start = request.args.get('from', None, type=int)
    count = request.args.get('count',None, type=int)

    if(identifier is not None):
        path = ".//*[@id='{}'] | .//*[@name='{}']".format(identifier,identifier)

    response = agent.sample(path,start,count)
    return responseResponse(response.get_xml(),status=response.get_status(), mimetype='text/xml')
    
## Push data to the agent
agent.push_data('avail','AVAILABLE')
```

## Development

There are still limitations to this library. Here is a list of features that are still needed that are being worked on. They are in no particular order

* Disk buffer. Allow the user to store data on disk using h5py instead of in memory
* Implement multiple devices. Current each instance only supports one device. This should be a relatively easy fix in the push_data function
* Implement entire MTConnect standard. Currently I do not handle assets or interfaces
