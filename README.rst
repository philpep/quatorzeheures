Quatorze Heures
===============

.. image:: https://travis-ci.org/philpep/quatorzeheures.svg?branch=master
   :target: https://travis-ci.org/philpep/quatorzeheures
   :alt: Build status


A mono-directional `MIDI <https://en.wikipedia.org/wiki/MIDI>`_ to `OSC
<http://opensoundcontrol.org>`_ gateway.

Dump all midi sources using `amidi <http://alsa.opensrc.org/Amidi>`_ (require
the ``alsa-utils`` package) send MIDI bytes as an OSC udp stream
``/midi/<device> <midi bytes>``.

Handle live connections and disconnections of midi sources.

Example::


    $ quatorzeheures 192.168.1.42:1214
    2016-08-12 02:47:44,653 stream OSC to udp://192.168.1.42:1214
    2016-08-12 02:47:44,662 connect Akai MPD18 MIDI 1 on port hw:2
    2016-08-12 02:47:49,223 Akai MPD18 MIDI 1 [176, 7, 37] --> '/midi/Akai_MPD18_MIDI_1\x00,iii\x00\x00\x00\x00\x00\xb0\x00\x00\x00\x07\x00\x00\x00%'
    2016-08-12 02:47:49,223 Akai MPD18 MIDI 1 [144, 10, 32] --> '/midi/Akai_MPD18_MIDI_1\x00,iii\x00\x00\x00\x00\x00\x90\x00\x00\x00\n\x00\x00\x00 '




