#!/usr/bin/env python3
#
# Onetab to HTML bookmark converter
# Brian Landers <brian@packetslave.com>
#
# See http://one-tab.com for more information about OneTab. This tool
# is not affiliated with them in any way.
#
# usage: onetab_to_bookmarks.py [-h] [--input_file [INPUT_FILE]]
#                               [--output_file [OUTPUT_FILE]]
#
# Convert OneTab export to HTML bookmarks
#
# optional arguments:
#   -h, --help            show this help message and exit
#   --input_file [INPUT_FILE]
#                         Path to OneTab file. STDIN if omitted.
#   --output_file [OUTPUT_FILE]
#                         Path to bookmarks file. STDOUT if omitted
#

import argparse
import sys
import time


HEADER = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
    <!--This is an automatically generated file.
    It will be read and overwritten.
    Do Not Edit! -->
    <Title>Bookmarks</Title>
    <H1>Bookmarks</H1>
    <DL>"""

FOOTER = "<DL>\n"


def main(args):
    if args.output_file:
        out = open(args.output_file, "w")
    else:
        out = sys.stdout

    if args.input_file:
        with open(args.input_file) as f:
            onetabs = f.readlines()
    else:
        onetabs = sys.stdin.readlines()

    # Pinboard (for example) doesn't like it when you have a ton of bookmarks
    # all with the same timestamp. Hack around that by setting each entry to
    # be N seconds in the past.
    now = int(time.time() - (len(onetabs) * 65))

    out.write(HEADER)

    for onetab in onetabs:
        if not onetab.startswith("http"):
            continue
        fields = onetab.strip().split(" | ", 1)
        site = fields[0]
        name = fields[1] if len(fields) > 1 else site

        out.write(
            f'<DT><A HREF="{site}" LAST_VISIT="{now}" LAST_MODIFIED="{now}">'
            f'{name}</A></DT>\n'
        )
        now += 65

    out.write(FOOTER)

    if args.output_file:
        out.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Convert OneTab export to HTML bookmarks",
        epilog="(c) Brian Landers <brian@packetslave.com>")
    parser.add_argument(
        "--input_file", nargs="?",
        help="Path to OneTab file. STDIN if omitted.")
    parser.add_argument(
        "--output_file", nargs="?",
        help="Path to bookmarks file. STDOUT if omitted")

    args = parser.parse_args()
    main(args)
