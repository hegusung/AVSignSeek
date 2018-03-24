import string
from utils import strings

def print_results(file_bin, signature_range_list, output_file):
    out = open(output_file, "w")

    out.write("=== AVSignSeek ===\n")

    for signature_range in signature_range_list:
        start = signature_range[0]
        end = signature_range[1]

        print("[+] Signature between bytes %d and %d" % (start, end))
        out.write("[+] Signature between bytes %d and %d\n" % (start, end))
        print("[+] Bytes:")
        out.write("[+] Bytes:\n")
        b = file_bin[start:end]
        while len(b) > 0:
            row = b[:16]
            output_line =  "".join(["{:02x} ".format(c) for c in row]).ljust(60)
            output_line += "".join([chr(c) if chr(c) in string.printable[:-5] else "." for c in row])
            print(output_line)
            out.write(output_line + "\n")
            b = b[16:]

        b = file_bin[start:end]
        print("[+] Strings:")
        out.write("[+] Strings:\n")
        for s in strings(b):
            print("> %s" % s)
            out.write("> %s\n" % s)

    out.close()


