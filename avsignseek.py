#!/usr/bin/python3
import argparse
import base64
import os
import re
import string
import time
from zipfile import ZipFile

SUBDIV = 10
SIGN_LIMIT = 64

def strings(binary, min=4):
    result = ""
    for c in binary:
        c = chr(c)
        if c in string.printable[:-5]:
            result += c
            continue
        if len(result) >= min:
            yield result
        result = ""
    if len(result) >= min:  # catch result at EOF
        yield result

def print_res(infected_file, start, end, output_file):
    out = open(output_file, "w")

    out.write("=== AVSignSeek ===")

    print("[+] Signature between bytes %d and %d" % (start, end))
    out.write("[+] Signature between bytes %d and %d\n" % (start, end))
    print("[+] Bytes:")
    out.write("[+] Bytes:\n")
    b = infected_file[start:end]
    while len(b) > 0:
        row = b[:16]
        output_line =  b"".join([b"%.2x " % c for c in row]).decode()
        output_line += "\t"
        output_line += "".join([chr(c) if chr(c) in string.printable[:-5] else "." for c in row])
        print(output_line)
        out.write(output_line + "\n")
        b = b[16:]

    b = infected_file[start:end]
    print("[+] Strings:")
    out.write("[+] Strings:\n")
    for s in strings(b):
        print("> %s" % s)
        out.write("> %s\n" % s)

    out.close()

def detect_sign(infected_file, sign_loc_list, sleep_time, limit_sign, subdiv, output_file):

    new_sign_loc_list = []

    for sign_loc in sign_loc_list:
        start = sign_loc[0]
        end = sign_loc[1]

        if end-start <= limit_sign:
            print_res(infected_file, start, end, output_file)
            continue

        test_files = []
        section_size = int((end-start)/subdiv)
        nb_range = range(0, subdiv)
        if section_size < limit_sign:
            section_size = limit_sign
            nb_range = range(0, int((end-start)/section_size)+1)

        print("[i] Processing bytes %d through %d, creating %d test files, section size:%d bytes" % (start, end, len(nb_range), section_size))

        for i in nb_range:
            filepath = os.path.join(".", "test-%s.bin" % i)
            test_files.append(filepath)

            f = open(filepath, "wb")
            f.write(infected_file[0:start+i*section_size])
            f.write(b"\x00"*section_size)
            f.write(infected_file[start+(i+1)*section_size:])
            f.close()

        time.sleep(sleep_time)

        print("[i] Removing test files")

        found = False
        for filepath in test_files:
            if os.path.exists(filepath):
                i = int(re.findall(r'\d+', filepath)[-1])
                sign_start = start + i*section_size
                sign_end = start + (i+1)*section_size

                new_sign_loc_list.append((sign_start, sign_end))
                found = True

            try:
                os.remove(filepath)
            except FileNotFoundError:
                pass

    if len(new_sign_loc_list) != 0:
        detect_sign(infected_file, new_sign_loc_list, sleep_time, limit_sign, subdiv, output_file)

def main(infected_file_path, start, end, sleep_time, filename, password, limit_sign, subdiv, output_file):

    print("=== AVSignSeek ===")

    with ZipFile(infected_file_path) as myzip:
        with myzip.open(filename, pwd=password.encode()) as myfile:
            file_bin = myfile.read()

    if end < 0:
        end = len(file_bin)

    sign_loc = [(start, end)]

    detect_sign(file_bin, sign_loc, sleep_time, limit_sign, subdiv, output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automatically detects AV Signatures")
    parser.add_argument("zip_file")
    parser.add_argument('-w', help='waiting time between 2 tests (default: 20)', dest='sleep', default=20, type=int)
    parser.add_argument('-p', help='zip password (default: infected)', dest='zip_password', default="infected")
    parser.add_argument('-f', help='file name contained in the zip (default: infected.bin)', dest='filename', default="infected.bin")
    parser.add_argument('-l', help='signature limit (default: 64)', dest='limit_sign', default=64, type=int)
    parser.add_argument('-d', help='subdiv per step (default: 4)', dest='subdiv', default=4, type=int)
    parser.add_argument('-o', help='output_file (default: output.txt)', dest='output_file', default="output.txt")
    parser.add_argument('-s', help='start byte (default: 0)', dest='start', default=0, type=int)
    parser.add_argument('-e', help='end byte', dest='end', default=-1, type=int)

    args = parser.parse_args()

    main(args.zip_file, args.start, args.end, args.sleep, args.filename, args.zip_password, args.limit_sign, args.subdiv, args.output_file)
