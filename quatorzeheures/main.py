# coding: utf-8
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import multiprocessing
import os
import signal
import socket
import struct
import sys
import threading
import time

import mido
from mido.ports import multi_receive

logger = logging.getLogger(__name__)

DEFAULT_PORT = 'Midi Through Port-0'


def normalize_url(name):
    return name.replace(" ", "_")


def osc_string(s):
    return s + (((len(s) + 1) % 4) + 1) * b'\x00'


def pack_osc(url, *params):
    msg = osc_string(url)
    param_string = b','
    values_string = b''
    for val in params:
        if isinstance(val, float):
            param_string += b'f'
            values_string += struct.pack('>f', val)
        elif isinstance(val, int):
            param_string += b'i'
            values_string += struct.pack('>i', val)
        elif isinstance(val, basestring):
            param_string += b's'
            values_string += osc_string(val)
    return msg + osc_string(param_string) + values_string


def get_input_names():
    return set(mido.get_input_names()) - set([DEFAULT_PORT])


class MidiMonitor(multiprocessing.Process):

    def __init__(self):
        self.changed = multiprocessing.Event()
        super(MidiMonitor, self).__init__()

    @staticmethod
    def check_parent():
        pid = os.getpid()
        while True:
            if os.getppid() == 1:
                os.kill(pid, signal.SIGKILL)
            time.sleep(1)

    def run(self):
        t = threading.Thread(target=self.check_parent)
        t.daemon = True
        t.start()
        current = get_input_names()
        while True:
            time.sleep(1)
            names = get_input_names()
            if current != names:
                logger.info("input changed %s -> %s", ",".join(current), ",".join(names))
                self.changed.set()
                current = names


class QuatorzeHeures(object):

    def __init__(self, host="localhost", port=1214):
        self.monitor = MidiMonitor()
        self.ports = []
        self.names = []
        logger.info("send OSC stream to %s:%d", host, port)
        super(QuatorzeHeures, self).__init__()

    def run(self):
        self.monitor.start()
        self.reset()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            if self.monitor.changed.is_set():
                self.monitor.changed.clear()
                self.reset()

            try:
                for port, message in multi_receive(
                    self.ports, yield_ports=True, block=False
                ):
                    msg = pack_osc(
                        "/midi/{0}".format(normalize_url(port.name)),
                        *message.bytes())
                    logger.info(
                        "%s %s %s --> %s",
                        port, message, message.bytes(), repr(msg))
                    sock.sendto(msg, ("localhost", 9999))
            except IOError:
                pass

            time.sleep(.1)

    def reset(self):
        while True:
            logger.info("reset ports")
            try:
                for port in self.ports:
                    try:
                        port.close()
                    except IOError:
                        pass
                time.sleep(.1)
                self.ports = []
                for name in get_input_names():
                    self.ports.append(mido.open_input(name))
                    logger.info("listen to %s", name)
            except IOError:
                time.sleep(1)
            else:
                break


def main():
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(fmt="%(asctime)-15s %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    if len(sys.argv) > 1:
        host, port = sys.argv[1].split(":")
        port = int(port)
        QuatorzeHeures(host, port).run()
    else:
        QuatorzeHeures().run()

if __name__ == "__main__":
    main()
