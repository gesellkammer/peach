#cython: embedsignature=True
cdef extern from "math.h":
    cdef double log(double n)
    cdef double log10(double n)
    cdef double fmod(double a, double b)
    cdef double modf(double x, double *integer)
    cdef double pow(double x, double y)

cdef dict _notes2 = {
    "C":0,
    "c":0,
    "D":2,
    "d":2,
    "E":4,
    "e":4,
    "F":5,
    "f":5,
    "G":7,
    "g":7,
    "A":9,
    "a":9,
    "B":11,
    "b":11}

cdef list _notes3      = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C"]
cdef list _enharmonics = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B", "C"]

cdef double _a4 = 442.0
cdef int _central_octave = 4

DEF OCTAVE_NOT_FOUND = -99
DEF loge_2 = 0.6931471805599453094172321214581766

cpdef inline double m2f(double midi):
    """
    convert midi value to frequency (A4 = 69.0 = 442.0)
    
    by default A4 = 69 = 442 Hz. 
    You can change the reference frequency (A4) by calling set_reference_freq

    A4 * 2.0 ** ((midi - 69.0) / 12.0)   # where A4 is 440 or 442 depending on the desired intonation
    """
    global _a4
    if 0.0 <= midi:
        return _a4 * 2.0 ** ((midi - 69.0) / 12.0)
    return 0.

cpdef inline double f2m(double freq):
    """
    convert frequency to midinote (C4 is central C)
    
    by default A4 = 69 = 442 Hz. 
    You can change the reference frequency (A4) by calling set_reference_freq

    12 * (log(freq / A4) / loge_2) + 69.0   # where A4 corresponds to the intonation of A4 in Hz (440-442)
    """
    global _a4
    if freq <= 0:
        return 0
    cdef double res
    if freq < 8.2129616379875419:   # this is the corresponding freq to midi 0
        return 0
    return 12 * (log(freq / _a4) / loge_2) + 69.0

def set_reference_freq(double a4=442.0):
    """
    set the value for A4
    """
    global _a4
    _a4 = a4
    
def set_central_octave(int octave=4):
    """
    define which is the central octave taken as reference
    
    if oct = 4 then C4 = 60
    if oct = 3 then C3 = 60
    """
    global _central_octave
    _central_octave = octave
    
cpdef m2n(double midi):
    """
    convert midi value to note string (69.0 = 'A4')

    format: 4C#+07

    """
    cdef double entero
    cdef double micro = modf(midi, &entero)
    cdef int octave = <int>(midi / 12.0) - 1
    cdef int ps = <int>fmod(midi, 12.0)
    cdef int cents = <int>(micro * 100 + 0.5)
    if cents == 0:
        return str(octave) + _notes3[ps]
    elif cents == 50:
        if ps == 1 or ps == 3 or ps == 6 or ps == 8 or ps == 10:
            return str(octave) + _notes3[ps+1] + '-'
        return str(octave) + _notes3[ps] + '+'
    elif cents > 50:  # convert it to negative
        cents = 100 - cents
        ps += 1
        if ps > 11:
            octave += 1
        if cents > 9:
            return "%d%s-%d" % (octave, _enharmonics[ps], cents)
        else:
            return "%d%s-0%d" % (octave, _enharmonics[ps], cents)
    else:
        if cents > 9:
            return "%d%s+%d" % (octave, _notes3[ps], cents)
        else:
            return "%d%s+0%d" % (octave, _notes3[ps], cents)

cpdef f2n (double freq):
    """
    convert frequency to note string
    """
    return m2n(f2m(freq))

cpdef n2f(note):
    """
    convert note string to frequency ('A4' = 442.0)
    """
    return m2f(n2m(note))

cdef int get_octave(note):
    cdef int octave
    try:
        octave = int(note[0])
    except ValueError:
        try:
            octave = int(note[-1])
        except ValueError:
            octave = OCTAVE_NOT_FOUND
    return octave

def complete_octaves(notes):
    cdef int current_octave = 4 # default octave: 
    cdef int octave
    cdef list new_notes = []
    for note in notes:
        octave = get_octave(note)
        if octave != OCTAVE_NOT_FOUND:
            current_octave = octave
            new_notes.append(note)
        else:
            new_notes.append(str(current_octave) + note)
    return new_notes

cpdef double n2m(note):
    """
    note can be:
        "4A" or "A4" 
        "4a" or "a4" 
        "c4 e g" or "4C E G" --> [60, 64, 67]
        "C#", "Db"
        "C4+" or "4C+" (C a 1/4 tone up)
        "E4-" or "4E-" (E a 1/4 tone down)
        "4C#+" -> C 3/4 tone up 
        "4E-31" -> E 31 cents down
        etc...

    
    """
    cdef int octave
    cdef double micro
    cdef int pc
    cdef int alteration

    out = note.split('+')
    try:
        micro = int(out[1]) / 100.
    except ValueError:
        micro = 0.5
    except IndexError, TypeError:
        # no +, negative?
        out = note.split('-')
        try:
            micro = -int(out[1]) / 100.
        except ValueError:
            micro = -0.5
        except IndexError, TypeError:
            micro = 0.0
    out0 = out[0]
    try:
        octave = int(out0[0])
        pc = _notes2[out0[1]]
        alteration = ord(out0[-1])
    except ValueError:
        octave = int(out0[-1])
        pc = _notes2[out0[0]]
        alteration = ord(out0[1])
    if alteration == 35:   # the # character
        pc += 1
    elif alteration == 98 or alteration == 115: # 'b' or 's'
        pc -= 1
    if pc > 11:
        pc = 0
        octave += 1
    elif pc < 0:
        pc = 0
        octave -= 1
    return (octave + 1) * 12 + pc + micro

cpdef double db2amp(double dBvalue):
    """ 
    convert dB to amplitude (0, 1) 

    pow(10.0, (0.05 * dBvalue))
    """
    return pow(10.0, (0.05 * dBvalue))

cpdef double amp2db(double amplitude):
    """ 
    convert amp (0, 1) to dB 

    20.0 * log10(amplitude)
    """
    return 20.0 * log10(amplitude)
