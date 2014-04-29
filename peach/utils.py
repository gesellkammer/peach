#!/usr/bin/env python
# encoding: utf-8
"""
utils.py

Created by edu on 2010-11-10.
"""
from _peach import *
import os

def _note_to_music21(note):
    return n2m(note)

def _open_pdf(pdf_file):
    os.system('open %s' % pdf_file)

def _show_note_in_finale(note):
    note = _note_to_music21(note)
    import music21
    out = music21.note.Note(note)
    out.show()
    return out
    
def _show_note_as_pdf(note):
    import music21
    import os
    note = _note_to_music21(note)
    out = music21.note.Note(note)
    f = out.write('musicxml')
    os.system('musicxml2ly %s' % f)
    ly = os.path.splitext(os.path.split(f)[1])[0] + '.ly'
    os.system('lilypond %s' % os.path.splitext(os.path.split(f)[1])[0] + '.ly')
    _open_pdf(os.path.splitext(ly)[0] + '.pdf')
    return out
    
def show_note(n, backend=None):
    """
    n can be a midi number or a note name

    backend: None -> use default backend
    """
    if isinstance(n, (int, float)):
        note = m2n(n)
    else:
        note = n
    DEFAULT = 'finale'
    if backend is None:
        backend = DEFAULT
    func = {
        'finale':_show_note_in_finale,
        'pdf':_show_note_as_pdf,
    }.get(backend, DEFAULT)
    return func(note)
    
def pianokey2midi(key_number):
    """
    convert the key number in a 88-key piano to its midi note
    
    A0 (the lowest in an 88-key keyboard) = 21
    so just add 21
    """
    assert 0 <= key_number <= 87
    return key_number + 21
         
def normalize_notename(n):
    """
    given a notename in the format returned by m2n, transform it to 
    note-octave format, dropping the cents if given
    
    this is useful when entering commands for software that expects a
    name for a midinote, like sample players 
    """
    n = m2n(int(n2m(n) + 0.5))
    n = n.lower()
    if n[0] in "0123456789": 
        if n[1] in "0123456789":
            digits = 2
        else:
            digits = 1
        octave = str(int(n[0:digits]))
        n = n[digits:] + octave
    elif n[0] == '-':
        octave = str(int(n[0:2]))
        n = n[2:] + octave
    return n
    
