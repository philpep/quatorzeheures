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
import socket
import struct
import subprocess
import sys
import threading
import time

if sys.version_info[0] == 2:
    import Queue
    text_type = unicode  # noqa
    string_types = basestring  # noqa
else:
    import queue as Queue
    text_type = str
    string_types = (str, bytes)

# Interval in seconds to discover new midi devices
MIDI_CHECK_INTERVAL = 2

logger = logging.getLogger(__name__)


def normalize_url(name):
    return name.replace(" ", "_")


def complete_osc(s):
    return s + (len(s) % 4) * b'\x00'


def osc_string(s):
    if isinstance(s, text_type):
        s = s.encode()
    return complete_osc(s + b'\x00')


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
        elif isinstance(val, string_types):
            param_string += b's'
            values_string += osc_string(val)
    return msg + complete_osc(param_string) + values_string


class MidiReader(object):

    def __init__(self, name):
        self.name = name
        self.buf = bytes()
        self.proc = None
        self.thread = None
        super(MidiReader, self).__init__()

    def start(self, port, queue):
        self.proc = subprocess.Popen(["amidi", "--port", port, "--dump"],
                                     stdout=subprocess.PIPE)
        self.thread = threading.Thread(target=self.enqueue_stdout,
                                       args=(self.name, self.proc.stdout,
                                             queue))
        self.thread.daemon = True
        self.thread.start()

    @staticmethod
    def enqueue_stdout(name, stdout, queue):
        for line in iter(stdout.readline, b''):
            queue.put((name, line))
        queue.put((name, None))

    def stop(self):
        self.proc.communicate()
        self.thread.join()


class MultiMidiReader(object):

    def __init__(self):
        self.readers = {}
        self.queue = Queue.Queue()
        self.last_check = None
        super(MultiMidiReader, self).__init__()

    @staticmethod
    def list_devices():
        out = subprocess.check_output(["amidi", "--list-devices"])
        # Dir Device    Name
        # IO  hw:2,0,0  Akai MPD18 MIDI 1
        for line in out.splitlines()[1:]:
            _, port, name = line.split(None, 2)
            port = port.split(",", 1)[0]
            yield name, port

    def get_message(self):
        if (self.last_check is None or
           abs(self.last_check - time.time()) > MIDI_CHECK_INTERVAL):
            self.start()

        try:
            name, line = self.queue.get(True, 1)
        except Queue.Empty:
            return

        if line is None:
            # Process terminated
            logger.info("disconnect %s", name)
            self.readers[name].stop()
            del self.readers[name]
        else:
            midi_bytes = [int(b, 16) for b in line.strip().split()]
            if midi_bytes:
                return name, midi_bytes

    def start(self):
        for name, port in self.list_devices():
            if name not in self.readers:
                logger.info("connect %s on port %s", name, port)
                self.readers[name] = MidiReader(name)
                self.readers[name].start(port, self.queue)
        self.last_check = time.time()


def main():
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(fmt="%(asctime)-15s %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    if len(sys.argv) > 1:
        host, port = sys.argv[1].split(":")
        port = int(port)
    else:
        host, port = "localhost", 1214

    logger.info("stream OSC to udp://%s:%d", host, port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    reader = MultiMidiReader()
    while True:
        message = reader.get_message()
        if message is not None:
            name, midi = message
            osc_message = pack_osc("/midi/{0}".format(normalize_url(name)),
                                   *midi)
            logger.info("%s %s --> %s", name, midi, repr(osc_message))
            sock.sendto(osc_message, (host, port))

if __name__ == "__main__":
    main()
