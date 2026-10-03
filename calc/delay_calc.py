import argparse


SPEED_OF_SOUND = 343  # m/s in air at room temperature

# length of each note value in beats (1 beat = 1 quarter note)
NOTE_BEATS = {
    "1/1": 4,
    "1/2": 2,
    "1/4": 1,
    "1/8": 0.5,
    "1/16": 0.25,
    "1/32": 0.125,
}


def bpm_to_beat_ms(bpm):
    """length of one beat (a quarter note) in ms at the given bpm."""
    beat_ms = 60000 / bpm
    return beat_ms


def note_to_beats(note, dotted=False, triplet=False):
    """how many beats a note value lasts. dotted = x1.5, triplet = x2/3"""
    beats = NOTE_BEATS[note]

    if dotted:
        beats = beats * 1.5
    elif triplet:
        beats = beats * 2 / 3

    return beats


def delay_ms(bpm, note, dotted=False, triplet=False):
    """delay time in ms for a note value at the given bpm."""
    ms = bpm_to_beat_ms(bpm) * note_to_beats(note, dotted, triplet)
    return ms


def metres_to_ms(metres):
    """time it takes sound to travel the given distance, in ms."""
    ms = metres / SPEED_OF_SOUND * 1000
    return ms


def ms_to_samples(ms, sample_rate):
    """converts ms to samples at the given sample rate."""
    seconds = ms / 1000
    samples = seconds * sample_rate
    return samples


def show_delay(bpm, note_name, ms):
    """prints the delay result in (note, bpm, ms)"""
    print(f"{note_name} at {bpm:g} BPM = {ms:.2f} ms")


def show_distance(metres, ms, samples, sample_rate):
    """prints the distance result in (metres, ms, samples)"""
    print(f"{metres:g} m = {ms:.2f} ms = {round(samples)} samples at {sample_rate} Hz")  # rounded because delay plugins only take whole samples


def main():
    """takes --bpm (with --note) or --metres and outputs the results, or the help if neither is given"""
    parser = argparse.ArgumentParser(description="tempo synced delay times, or a distance in metres converted to ms and samples")
    parser.add_argument("--bpm", type=float, help="tempo in bpm")
    parser.add_argument("--note", default="1/4", choices=list(NOTE_BEATS.keys()), help="note value (default 1/4)")
    parser.add_argument("--dotted", action="store_true", help="dotted note (x1.5)")
    parser.add_argument("--triplet", action="store_true", help="triplet note (x2/3)")
    parser.add_argument("--metres", type=float, help="distance in metres to convert")
    parser.add_argument("--sr", type=int, default=48000, help="sample rate in Hz (default 48000)")

    args = parser.parse_args()

    if args.bpm is not None:
        bpm = args.bpm

        if bpm <= 0:
            parser.error("bpm can't be 0 or a negative value")  # 0 would divide by zero in bpm_to_beat_ms

        elif args.dotted and args.triplet:
            parser.error("a note can be dotted or triplet, not both")

        else:
            ms = delay_ms(bpm, args.note, args.dotted, args.triplet)

            note_name = args.note
            if args.dotted:
                note_name = note_name + " dotted"
            elif args.triplet:
                note_name = note_name + " triplet"

            show_delay(bpm, note_name, ms)

    elif args.metres is not None:
        metres = args.metres
        ms = metres_to_ms(metres)
        samples = ms_to_samples(ms, args.sr)

        show_distance(metres, ms, samples, args.sr)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
