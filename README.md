# PiControl

PiControl is a python Code to interoperate with
projectors through PJLink protocol (http://pjlink.jbmia.or.jp/english/)

It is a fork of the work of Peter Ward Library (https://bitbucket.org/flowblok/pjlink).

You can use the python library of him, when you don’t have a PJLink password on your projectors. I have modified it because I had difficulties setting a command when my projector was protected.

## Installation

Latest release can be found on GitHub and installed with:
```bash
git clone https://github.com/goer1011/PiControl.git
```

## Usage

### ~~Command line~~

To keep it simple I didn’t implement it.

### Python library

The library supports the following python versions:
* python2.7

for it to work on Python 3.4/3.5, you should put in newline where it is commented you to.
__I didn’t try it out by myself, so it may not work. __ 
* python3.4
* python3.5

```python
import Projector
projector = Projector.from_address('10.1.1.1')
# authenticate is required even if there is no password
print(projector.get_power())
# off
projector.set_power(ON, "ABCDEFG"))
```
## Problems I had
---
To get the IP address of the projector Epson provides a Tool where you can control it (https://www.epson.de/epson-projector-software#easymp-multi). If you don’t want to run it on a raspberry or similar I highly recommend using it instead.

### Troubleshooting
If you don’t know if you are connected to the projector then download on this page https://pjlink.jbmia.or.jp/english/dl_class2.html the test software.
