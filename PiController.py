from __future__ import unicode_literals

import hashlib
import socket
import sys
import protocol
import cgi
#import RPi.GPIO as GPIO
import time

class ProjectorError(Exception):
    pass

reverse_dict = lambda d: dict(zip(d.values(), d.keys()))

SET_POWER_STATES = {
    'off': '0',
    'on': '1',
    'cooling': '2',
    'warm-up': '3',
}

POWER_STATES_REV = reverse_dict(SET_POWER_STATES)

GET_POWER_STATES = '?'

POWR_BODY = 'POWR'

OFF='off'

ON='on'

class Projector(object):
    def __init__(self, f):
        self.f = f

    @classmethod
    def from_address(cls, address, port=4352):
        """build a Projector from a ip address"""
        sock = socket.socket()
        sock.connect((address, port))
        # in python 3 I need to specify newline, otherwise read hangs
        # in "PJLINK 0\r"
        # I expect socket file to return byte strings in python 2 and
        # unicode strings in python 3
        if sys.version_info.major == 2:
            f = sock.makefile()
        else:
            f = sock.makefile(mode='rw')
        return cls(f)

    def authenticate(self, cmd, password=None):
        # I'm just implementing the authentication scheme designed in the
        # protocol. Don't take this as any kind of assurance that it's secure.

        data = protocol.read(self.f, 9)
        assert data[:7] == 'PJLINK '
        security = data[7]
        if security == '0':
            return None
        data += protocol.read(self.f, 9)
        assert security == '1'
        assert data[8] == ' '
        salt = data[9:17]
        assert data[17] == '\r'

        if password is None:
            raise RuntimeError('projector needs a password')

        if callable(password):
            password = password()

        pass_data = (salt + password).encode('utf-8')
        pass_data_md5 = hashlib.md5(pass_data).hexdigest()

        # we *must* send a command to complete the procedure,
        # so we just get the power state.

        cmd_data = protocol.to_binary(POWR_BODY, cmd)
        self.f.write(pass_data_md5 + cmd_data)
        self.f.flush()

        # read the response, see if it's a failed auth
        data = protocol.read(self.f, 7)
        if data == 'PJLINK ':
            # should be a failed auth if we get that
            data += protocol.read(self.f, 5)
            assert data == 'PJLINK ERRA\r'
            # it definitely is
            return False

        # good auth, so we should get a reply to the command we sent
        body, param = protocol.parse_response(self.f, data)

        # make sure we got a sensible response back
        assert body == POWR_BODY
        if param in protocol.ERRORS:
            raise ProjectorError(protocol.ERRORS[param])

        # but we don't care about the value if we did
        return param

    # Power

    def get_power(self,password=None):
        param = self.authenticate(GET_POWER_STATES, password)
        return POWER_STATES_REV[param]

    def set_power(self, status, password=None, force=False):
        if not force:
            assert status in (SET_POWER_STATES)
        
        self.authenticate(SET_POWER_STATES[status], password)



if __name__ == "__main__":
    projector = Projector.from_address('192.168.0.100')
while true:
    try:
        GPIO.setwarnings(False) # Ignore warning for now
        GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
        GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
        GPIO.add_event_detect(10,GPIO.RISING,callback=projector.set_power(OFF, "ABCDEFG")) # Setup event on pin 10 rising edge
        GPIO.add_event_detect(10,GPIO.RISING,callback=projector.set_power(ON, "ABCDEFG")) # Setup event on pin 10 rising edge
    except:
        print("Bedienung Fehlgeschlagen")
        time.sleep(5)
