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

import pytest
from quatorzeheures.main import pack_osc


@pytest.mark.parametrize("url, params, expected", [
    ("/oscillator/4/frequency", (440.0,),
     b"/oscillator/4/frequency\x00\x2c\x66\x00\x00\x43\xdc\x00\x00"),
    ("/midi/Akai_MPD18_MIDI_1", (160, 6, 59), (
     b"/midi/Akai_MPD18_MIDI_1\x00,iii\x00\x00\x00\xa0\x00\x00\x00"
     b"\x06\x00\x00\x00;")),
])
def test_osc(url, params, expected):
    msg = pack_osc(url, *params)
    assert msg == expected
