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


The instance requires a xml file with the device descriptions. The default location is `./device.xml`. This can be changed by setting the loc value as shown below. This file is in the format of the `Device` element xml and will be returned by the `probe` command.

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

To access the commands you can run either of the following commands. The corispond to the `probe`, `sample`, `current` endpoints in the mtconnect standard.

```
instance.probe()
instance.sample(path=None, start=None, count=None)
instance.current(at=None, path=None)
```


