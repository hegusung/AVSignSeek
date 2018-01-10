import os
import time
from utils import generate_ranges, union

# RAW analysis: perform analysis on selected parts without considering the file type
def raw_analysis(file_bin, analysed_parts, sign_min_size, test_dir, subdiv, manual, sleep, replacing_value=0):
    # Each part to be analysed will be divided 'subdiv' times if each subdivision is higher than sign_min_size
    range_list, minimal_range_set = generate_ranges(analysed_parts, subdiv, sign_min_size)

    if minimal_range_set:
        # each range is equal or smaller than the minimal signature size option, abort
        return range_list

    new_range_list = []

    range_file_dict = {}

    print("[i] Creating %d test files..." % len(range_list), end="")

    for i, r in enumerate(range_list):
        filepath = os.path.join(test_dir, "test-%s.bin" % i)
        range_file_dict[filepath] = r

        f = open(filepath, "wb")
        f.write(file_bin[0:r[0]])
        f.write(bytes([replacing_value])*(r[1]+1-r[0]))
        f.write(file_bin[r[1]+1:])
        f.close()

    print("Done")

    if not manual:
        time.sleep(sleep)
    else:
        _ = input("Press any key to continue...")

    found_sign = False
    for filepath, r in range_file_dict.items():
        if os.path.exists(filepath):
            print("[i] Located signature between bytes %d and %d" % (r[0], r[1]))
            new_range_list.append(r)
            found_sign = True
        try:
            os.remove(filepath)
        except FileNotFoundError:
            pass

    if len(new_range_list) == 0:
        print("[i] Unable to get a more precise location of the signature, probable a payload containing multiple signatures")
        return new_range_list
    elif union(new_range_list) == union(analysed_parts):
        print("[i] Unable to get a more precise location of the signature")
        return new_range_list
    else:
        return raw_analysis(file_bin, new_range_list, sign_min_size, test_dir, subdiv, manual, sleep)


