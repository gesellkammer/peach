PITCHTOOLS
==========

Functions to convert between frequency, midi-note, note-name, amplitude and decibels.

Most are efficiently implemented in cython.

Dependencies
------------

* cython >= 0.12
* python >= 2.5

You should of course have a c compiler installed.

Installation
------------

* build it in place

    python setup.py build_ext --inplace

And then add that directory to your python path

* install at site-packages

    python setup.py install

Note Names
----------

All convertion functions that take note-names accept notes in the following formats:

	C4     C in the 4th octave (central C)
	c#2    C# in the 2nd octave
	3Gb    G-flat in the 3rd octave
	4Eb+   E-flat a quarter-tone up in the 4th octave
	6G+4   G in the 6th octave, 4 cents up
       
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

Most of the pitch convertion functions have also long-name aliases
