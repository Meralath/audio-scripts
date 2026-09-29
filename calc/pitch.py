import math
import argparse


def cents_to_ratio(cents):
    """converts cents to a ratio. 1 octave = 12 semitones = 1200 cents = ratio 2."""
    ratio = 2 ** (cents / 1200)
    return ratio


def ratio_to_percent(ratio):
    """conversion of ratio to a percentage change. ratio 1 = no change"""
    percent = (ratio - 1) * 100
    return percent


def ratio_to_cents(ratio):
    """convert a ratio back to cents. ratio can't be 0 or a negative value."""
    cents = 1200 * math.log2(ratio)
    return cents


def show_result(cents, ratio, percent):
    """prints the final result in (cents, ratio, percent)"""
    print(f"{cents:+.2f} cents = ratio {ratio:.4f} = {percent:+.2f}%") # ratio gets 4 decimals for finer resolution


def main():
    """takes the arguments --cents or --ratio and a value, then outputs the results, or the help if neither is given"""
    parser = argparse.ArgumentParser(description="convert pitch (cents) to ratio and percentage or a ratio back to cents")
    parser.add_argument("--cents", type=float, help="number of cents to convert")
    parser.add_argument("--ratio", type=float, help="pitch ratio to convert")

    args = parser.parse_args()

    if args.cents is not None:
        cents = args.cents
        ratio = cents_to_ratio(cents)
        percent = ratio_to_percent(ratio)

        show_result(cents, ratio, percent)

    elif args.ratio is not None:
        ratio = args.ratio

        if ratio <= 0:
            parser.error("ratio can't be 0 or a negative value")  # values of 0 and below crash math.log2

        else:
            cents = ratio_to_cents(ratio)
            percent = ratio_to_percent(ratio)

            show_result(cents, ratio, percent)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
