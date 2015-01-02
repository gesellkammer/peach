PEACH
=====

Functions to convert between frequency, midi-note, note-name, amplitude and decibels.

Most are efficiently implemented in cython.

Dependencies
------------

* cython >= 0.12
* python >= 2.5 (python3 >= 3.3)
* six

You should of course have a c compiler installed.

Installation
------------

    python setup.py install
    
    or
    
    python3 setup.py install

Note Names
----------

All convertion functions that take note-names accept notes in the following formats:

	C4     C in the 4th octave (central C)
	c#2    C# in the 2nd octave
	3Gb    G-flat in the 3rd octave
	Eb4+   E-flat a quarter-tone up in the 4th octave
	G6+4   G in the 6th octave, 4 cents up
       
Functions
---------

	f2m      frequency to midi-note
	m2f      midi-note to frequency
	f2n      frequency to note-name
	n2f      note-name to frequency
	n2m      note-name to midinote
	m2n      midi-note to note-name
	amp2db   amptlitude to dB (0dB = 1 amp, 0 = -inf dB)
	db2amp   dB to amplitude
