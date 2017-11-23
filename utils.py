import string

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

def union(range_list):
    res = []
    for begin, end in sorted(range_list):
        if res and res[-1][1] >= begin-1:
            res[-1][1] = max(res[-1][1], end)
        else:
            res.append([begin, end])
    return [(item[0], item[1]) for item in res]


def intersect(range_list):
    res = None
    for begin, end in sorted(range_list):
        if not res:
            res = [begin, end]
        elif res[1] >= begin:
            res[0] = begin
        else:
            res = None
    return (res[0], res[1]) if res else None

def range_size(r):
    return r[1]-r[0]+1

def generate_ranges(selected_range_list, subdiv, min_section_size):
    minimal_range_set = True

    selected_range_list = union(selected_range_list)
    res = []
    for selected_range in selected_range_list:
        if range_size(selected_range) <= min_section_size:
            res.append(selected_range)

        minimal_range_set = False

        section_size = int(range_size(selected_range)/subdiv) if int(range_size(selected_range)/subdiv) > min_section_size else min_section_size

        while range_size(selected_range) > 0:
            current_range = (selected_range[0], selected_range[0]+section_size-1)
            current_range = intersect([selected_range, current_range])
            res.append(current_range)
            selected_range = (selected_range[0]+section_size, selected_range[1])

    return [(item[0], item[1]) for item in res], minimal_range_set

def get_ranges_from_str(ranges_str, file_size):
    res = []

    for range_str in ranges_str.split(","):
        if not ":" in range_str:
            continue

        try:
            start = int(range_str.split(":")[0], 16 if range_str.split(":")[0].startswith("0x") else 10) if range_str.split(":")[0] != "" else 0
            end = int(range_str.split(":")[1], 16 if range_str.split(":")[1].startswith("0x") else 10) if range_str.split(":")[1] != "" else file_size-1

            if start < 0:
                raise Exception("Incorrect input range (example: ':0x100,0x150:0x1a0,0x1b0:')")
            if end < 0:
                raise Exception("Incorrect input range (example: ':0x100,0x150:0x1a0,0x1b0:')")
        except ValueError:
            raise Exception("Incorrect input range (example: ':0x100,0x150:0x1a0,0x1b0:')")

        if start < end:
            res.append((start, end))

    return union(res)
