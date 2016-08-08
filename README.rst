Quatorze Heures
===============

A monodirectionnal `MIDI <https://en.wikipedia.org/wiki/MIDI>`_ to `OSC
<http://opensoundcontrol.org>`_ gateway that handle hot MIDI connections and
disconnections and stream MIDI bytes as OSC udp stream:

Example::


    $ quatorzeheures 192.168.1.42:1214
    2016-08-10 15:47:19,196 send OSC stream to 192.168.1.42:1214
    2016-08-10 15:47:19,198 reset ports
    2016-08-10 15:47:19,327 listen to Akai MPD18 MIDI 1
    2016-08-10 15:47:23,840 <open input u'Akai MPD18 MIDI 1' (PortMidi/ALSA)> control_change channel=0 control=7 value=60 time=0 [176, 7, 60] --> '/midi/Akai_MPD18_MIDI_1\x00,iii\x00\x00\x00\x00\x00\xb0\x00\x00\x00\x07\x00\x00\x00<'
    2016-08-10 15:47:23,842 <open input u'Akai MPD18 MIDI 1' (PortMidi/ALSA)> control_change channel=0 control=7 value=61 time=0 [176, 7, 61] --> '/midi/Akai_MPD18_MIDI_1\x00,iii\x00\x00\x00\x00\x00\xb0\x00\x00\x00\x07\x00\x00\x00='
    2016-08-10 15:47:38,587 <open input u'Akai MPD18 MIDI 1' (PortMidi/ALSA)> note_on channel=0 note=2 velocity=20 time=0 [144, 2, 20] --> '/midi/Akai_MPD18_MIDI_1\x00,iii\x00\x00\x00\x00\x00\x90\x00\x00\x00\x02\x00\x00\x00\x14'
    2016-08-10 15:47:38,689 <open input u'Akai MPD18 MIDI 1' (PortMidi/ALSA)> polytouch channel=0 note=2 value=25 time=0 [160, 2, 25] --> '/midi/Akai_MPD18_MIDI_1\x00,iii\x00\x00\x00\x00\x00\xa0\x00\x00\x00\x02\x00\x00\x00\x19'
    2016-08-10 15:47:38,690 <open input u'Akai MPD18 MIDI 1' (PortMidi/ALSA)> polytouch channel=0 note=2 value=0 time=0 [160, 2, 0] --> '/midi/Akai_MPD18_MIDI_1\x00,iii\x00\x00\x00\x00\x00\xa0\x00\x00\x00\x02\x00\x00\x00\x00'
    2016-08-10 15:47:38,690 <open input u'Akai MPD18 MIDI 1' (PortMidi/ALSA)> note_off channel=0 note=2 velocity=0 time=0 [128, 2, 0] --> '/midi/Akai_MPD18_MIDI_1\x00,iii\x00\x00\x00\x00\x00\x80\x00\x00\x00\x02\x00\x00\x00\x00'




