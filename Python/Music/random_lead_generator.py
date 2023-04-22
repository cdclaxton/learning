# Random lead riff generator
#
# --------========--------========
# 1 e & a 2 e & a 3 e & a 4 e & a
# 0 1 2 3 4 5 6 7 8 9 1 1 1 1 1 1
#                     0 1 2 3 4 5

import numpy as np
import random
import sys


def random_bar_timings():

    times = []

    patterns = [
        [0, 0, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 1, 0, 0],
        [0, 1, 0, 1],
        [0, 1, 1, 0],
        [0, 1, 1, 1],
        [1, 0, 0, 0],
        [1, 0, 0, 1],
        [1, 0, 1, 0],
        [1, 0, 1, 1],
        [1, 1, 0, 0],
        [1, 1, 0, 1],
        [1, 1, 1, 0],
        [1, 1, 1, 1],        
    ]

    def p_pattern(x):
        space = sum([xi == 0 for xi in x])
        ease = x[1] == 0 and x[3] == 0
        return 1 + space + 0.5*ease

    # Probability of each pattern is dependent on its complexity
    pattern_prob = [p_pattern(x) for x in patterns]
    pattern_prob = np.array(pattern_prob) / sum(pattern_prob)

    for i in range(4):
        # Randomly select a pattern
        pattern_idx = np.argmax(np.random.multinomial(1, pattern_prob))

        for j,t in enumerate(patterns[pattern_idx]):
            if t == 1:
                times.append(i*4 + j)

    # Postconditions
    assert len(times) > 0
    assert all(times[i+1] - times[i] > 0 for i in range(len(times)-1))
    assert min(times) >= 0
    assert max(times) <= 15

    return times

def build_bar2(timings, notes):

    assert len(timings) == len(notes)

    bar1 = "1e&a2e&a3e&a4e&a"
    bar1 = [b for b in bar1]

    bar2 = []
    note_idx = 0
    for i in range(16):
        if i in timings:
            bar2.append(notes[note_idx])
            note_idx += 1
        else:
            bar2.append("")
    
    assert len(bar1) == len(bar2)
    bars = [bar1, bar2]

    s = ""
    width = 3
    for bar in bars:
        s += "  | "
        for i in range(16):
            s += bar[i] + " "*(width - len(bar[i]))

            if (i+1)%4 == 0:
                s += "| "

        s += "\n"

    return s


def build_bar(timings, notes):

    bar =  "|            |            |            |            |\n"
    bar += "| 1  e  &  a | 2  e  &  a | 3  e  &  a | 4  e  &  a |\n"
    bar += "| "
    
    j = 0
    for i in range(16):
        if i in timings:
            bar += notes[j] + " "
            j += 1
        else: 
            bar += "  "
        
        if i in [3,7,11, 15]:
            bar += "| "
        else:
            bar += " "

    return bar


def random_notes(notes, num):

    # Preconditions
    assert num > 0
    assert len(notes) == 7

    sequence = []

    initial = [1, 0, 1, 0, 1, 0, 0]
    initial = np.array(initial) / sum(initial)

    transition = [
        [4, 2, 4, 2, 4, 2, 1],
        [4, 3, 4, 0, 4, 0, 0],
        [4, 2, 4, 2, 4, 2, 1],
        [4, 0, 4, 3, 4, 0, 0],
        [4, 2, 4, 2, 4, 2, 1],
        [4, 0, 4, 0, 4, 1, 0],
        [4, 0, 4, 0, 4, 0, 1]
    ]

    transition = [np.array(row) / sum(row) for row in transition]

    idx = np.argmax(np.random.multinomial(1, initial))
    sequence.append(notes[idx])

    for _ in range(1, num):
        idx = np.argmax(np.random.multinomial(1, transition[idx]))
        sequence.append(notes[idx])

    # Postconditions
    assert len(sequence) == num

    return sequence


def notes_in_key(key):
    """Notes given the musical key."""

    notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]

    scale = [notes.index(key)]
    steps = [2, 2, 1, 2, 2, 2]    

    for s in steps:
        scale.append(scale[-1] + s)

    return [notes[s%12] for s in scale]


def chords_in_key(scale):

    tpe = ["", "m", "m", "", "", "m", "dim"]
    return [s + tpe[idx] for idx, s in enumerate(scale)]


def random_chord_progression(chords_in_key):
    """Create a random chord progression."""

    patterns = [
        [1, 4, 5, 5],
        [1, 5, 6, 4],
        [1, 4, 5, 4],
        [1, 4, 2, 5],
        [1, 6, 4, 5],
        [6, 5, 4, 5],
    ]

    chosen = random.choice(patterns)

    return [chords_in_key[i-1] for i in chosen]


def random_arpeggio():
    """Build a random 8th note apeggio."""

    p_num_strings = [0, 5, 4, 3, 2, 1, 1]
    p_num_strings = np.array(p_num_strings) / sum(p_num_strings)
    number_strings = np.argmax(np.random.multinomial(1, p_num_strings))

    strings = [1,2,3,4,5,6]
    random.shuffle(strings)

    potentials = [0]  # means no note is played
    potentials.extend(strings[:number_strings])

    selection = [random.choice(potentials) for _ in range(8)]

    bar = "  | 1  &  2  &  3  &  4  &   |\n"
    
    for string_idx, string in enumerate(["e", "B", "G", "D", "A", "E"]):
        bar += string + " | "
        for i in range(8):
            if selection[i] == string_idx + 1:
                bar += "#--"
            else:
                bar += "---"
        bar += " |\n"

    return bar


def random_syncopated_rhythm():
    """Build a two-bar random syncopated rhythm."""

    patterns = [
        (0, 0),
        (0, 1),
        (1, 0),
        (1, 1)
    ]

    p_initial = np.array([1, 1, 0.1, 0.1])
    p_initial = p_initial / np.sum(p_initial)

    p_others = np.array([1, 1, 1, 1])
    p_others = p_others / np.sum(p_others)

    sequence = [patterns[np.argmax(np.random.multinomial(1, p_initial))]]

    for _ in range(7):
        p = patterns[np.argmax(np.random.multinomial(1, p_others))]
        sequence.append(p)

    bar = "  | 1  &  2  &  3  &  4  &  | 1  &  2  &  3  &  4  &  |\n"
    bar += "  | "

    for i in range(8):
        for k in sequence[i]:
            if k == 0:
                bar += "   " 
            else:
                bar += "#  "

        if i == 3 or i == 7:
            bar += "| "

    return bar


if __name__ == '__main__':

    # Get the key
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <key>")
        exit()
    key = sys.argv[1]

    # Scale given the key
    scale = notes_in_key(key)
    print(scale)

    chords = chords_in_key(scale)
    progression = random_chord_progression(chords)

    timings = random_bar_timings()

    for chord in progression:

        start_idx = [i for i in range(len(scale)) if chord[0] == scale[i][0]][0]
        scale_for_chord = [scale[(start_idx+i)%7] for i in range(len(scale))]

        notes = random_notes(scale_for_chord, len(timings))
        print(f"  {chord}")
        bar = build_bar2(timings, notes)
        print(bar)
        print()
    
    print(random_arpeggio())
    print(random_syncopated_rhythm())
    print()
    