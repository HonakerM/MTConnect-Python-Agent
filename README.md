# MTConnect-Python-Agent
Python agent for MTConnect applications.

This library helps store, and format data for MTConnect. The 
MTConnect standard can be found at [mtconnect.org](https://www.mtconnect.org).
This package does not handle the HTTP aspect of the standard.
It is designed to be used in conjunction with a wsgi interface like
flask or django.

At the time of writting the library is not feature complete. Currently in the works is to get a minimal MTConnect instance operational. This library supports Devices, Components, DataItems, and Steams.
