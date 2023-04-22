# Generate a small (single bar) motive in a given key.

import numpy as np
import random
import sys

def random_timing():
    """Generate a random list of timings in 4/4."""

    # Single 4/4 bar 16th note patterns
    patterns = [
        [0, 0, 0, 0],  # 0 - easy
        [0, 0, 0, 1],  # 1 - hard
        [0, 0, 1, 0],  # 2 - easy
        [0, 0, 1, 1],  # 3 - medium
        [0, 1, 0, 0],  # 4 - hard
        [0, 1, 0, 1],  # 5 - hard
        [0, 1, 1, 0],  # 6 - medium
        [0, 1, 1, 1],  # 7 - hard
        [1, 0, 0, 0],  # 8 - easy
        [1, 0, 0, 1],  # 9 - medium
        [1, 0, 1, 0],  # 10 - easy
        [1, 0, 1, 1],  # 11 - medium
        [1, 1, 0, 0],  # 12 - medium
        [1, 1, 0, 1],  # 13 - hard
        [1, 1, 1, 0],  # 14 - medium
        [1, 1, 1, 1]   # 15 - hard 
    ]

    easy = [0, 2, 8, 10]
    medium = [3, 6, 9, 11, 12, 14]
    hard = [1, 4, 5, 7, 13, 15]

    patterns_by_difficulty = [easy, medium, hard]

    probs = [0.7, 0.2, 0.1]
    num_bars = 4

    bars = []
    for _ in range(num_bars):
        # Select a difficulty
        idx = np.argmax(np.random.multinomial(1, probs))
        pattern_difficulty = patterns_by_difficulty[idx]

        # Select a pattern
        pattern = random.choice(pattern_difficulty)
        bars.append(patterns[pattern])

    return bars


def all_notes():
    return ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]


def notes_in_key(key):
    """Notes given the musical key."""

    notes = all_notes()
    scale = [notes.index(key)]
    steps = [2, 2, 1, 2, 2, 2]    

    for s in steps:
        scale.append(scale[-1] + s)

    return [notes[s%12] for s in scale]


def next_note(note):
    """Returns the next note on a fretboard."""

    idx = all_notes().index(note)
    if idx == len(all_notes()) - 1:
        return all_notes()[0]
    else:
        return all_notes()[idx + 1]


def fretboard(max_frets):
    """Returns a dict of string index to list of notes."""

    strings = {
        1: ['E'], # High e-string
        2: ['B'],
        3: ['G'],
        4: ['D'],
        5: ['A'],
        6: ['E']  # Low e-string
    }

    for s in strings.keys():
        for _ in range(max_frets):
            strings[s].append(next_note(strings[s][-1]))


    return strings


def random_strings(num_strings):
    """Randomly select adjacent strings."""

    assert 0 < num_strings and num_strings <= 6

    available_string_indices = [1,2,3,4,5,6]
    chosen_strings = [random.choice(available_string_indices)]

    for _ in range(num_strings - 1):

        if chosen_strings[0] == 1:
            p_below = 0
        else:
            p_below = 1

        if chosen_strings[-1] == 6:
            p_above = 0
        else:
            p_above = 1

        p_vals = [p_above / (p_above + p_below), p_below / (p_above + p_below)]
        above_or_below = np.argmax(np.random.multinomial(1, p_vals))

        if above_or_below == 0:
            chosen_strings.append(chosen_strings[-1] + 1)
        else:
            chosen_strings.insert(0, chosen_strings[0] - 1)

    # Postconditions
    assert all([chosen_strings[i] - chosen_strings[i-1] == 1 \
                for i in range(1, len(chosen_strings)) ]), f"Strings: {chosen_strings}"
    assert min(chosen_strings) >= 1, f"Strings: {chosen_strings}"
    assert max(chosen_strings) <= 6, f"Strings: {chosen_strings}"

    return chosen_strings


def fretboard_for_key(fretboard, key):
    notes = notes_in_key(key)
    return {s: [n if n in notes else "-" for n in ns] for s, ns in fretboard.items()}


def fretboard_in_span(fretboard, start, end):
    return {s:[n if start <= idx <= end else "-" for idx,n in enumerate(ns)] \
        for s, ns in fretboard.items() }


def available_nodes(fretboard):
    """Returns a list of tuples of (string, fret)."""

    available = []
    for s, ns in fretboard.items():
        for idx, n in enumerate(ns):
            if n != "-":
                available.append((s, idx))
    
    return available


def select_notes(timing, available):

    timings = []

    for _, n in enumerate(timing):
        for ni in n:
            if ni == 1:
                t = random.choice(available)
            else:
                t = None
        
            timings.append(t)

    return timings


def cell(value, width, is_string):
    if value is None:
        s = ""
    elif value == -1:
        s = ""
    else:
        s = str(value)

    pad = width - len(s)
    assert pad >= 0

    if is_string:
        s += "-" * pad
    else:
        s += " " * pad

    return s    


def display(note_timings):

    #time = '1e&a2e&a3e&a4e&a'
    time = '1.+.2.+.3.+.4.+.'
    time_line = [time[i] for i in range(len(time))]

    m = np.ones((6, 16)) * -1
    for time_idx, t in enumerate(note_timings):
        if t is None:
            continue
            
        row = t[0] - 1
        col = time_idx
        fret = t[1]
        m[row, col] = fret
    
    # Display the timing line
    width = 3
    line = "  " + "".join([cell(s, width, False) for s in time_line])
    print(line)

    # Display each string
    for row_idx in range(6):
        line = ["E", "B", "G", "D", "A", "E"][row_idx] + "|"
        line += "".join([cell(int(s), width, True) for s in m[row_idx,:]])
        print(line)



def random_sequence(timing, fretboard, num_strings, span, key):
    """Create a random sequence given the timing and number of strings."""

    assert 0 < num_strings and num_strings <= 6
    assert span > 0

    # Randomly select the strings to use
    strings = random_strings(num_strings)
    assert all([s in fretboard for s in strings])

    # Retain chosen strings
    f2 = {s:fretboard[s] for s in strings}
    assert len(f2) == len(strings)

    # Retain just the notes in the key
    f2 = fretboard_for_key(f2, key)
    
    # Randomly select a starting fret point
    max_frets = len(f2[list(f2.keys())[0]])
    start = np.random.randint(0, max_frets - span)
    end = start + span - 1
    assert start >= 0 and start <= max_frets
    assert end >= 0 and end <= max_frets    
    
    # Retain notes in span
    f2 = fretboard_in_span(f2, start, end)

    # Get a list of the available notes
    available = available_nodes(f2)
    
    s = select_notes(timing, available)
    
    display(s)


if __name__ == '__main__':

    # Get the key
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <key>")
        exit()
    key = sys.argv[1]
    key = key.upper()

    # Generate fretboard
    f = fretboard(12)

    # Generate a random timing
    bar_timing = random_timing()

    # Display the small motive
    random_sequence(bar_timing, f, 2, 4, key)
