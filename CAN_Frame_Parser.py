import csv
def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False


class CANFrame:
    def __init__(self, timestamp, interface, can_id, data_hex):
        self.timestamp = timestamp
        self.interface = interface
        self.can_id = can_id
        self.data_hex = data_hex

    def is_valid(self):
        if not is_hex(self.can_id):
            return False, "ID is not a valid hexadecimal"

        if len(self.can_id) <= 3:
            if int(self.can_id, 16) > 0x7FF:
                return False, "INVALID: standard ID out of range"
        elif len(self.can_id) <= 8:
            if int(self.can_id, 16) > 0x1FFFFFFF:
                return False, "INVALID: extended ID out of range"
        else:
            return False, "INVALID: ID too long"

        if not is_hex(self.data_hex):
            return False, "The data is not a hexadecimal"

        if len(self.data_hex) % 2 != 0:
            return False, "INVALID: the data has an uneven number of hexadecimal characters."

        num_bytes = len(self.data_hex) // 2
        if num_bytes > 8:
            return False, "INVALID: too many bytes, the max is 8 bytes."

        return True, "VALID"


def parse_line(line):
    parts = line.split()

    raw_timestamp = parts[0]
    interface = parts[1]
    id_and_data = parts[2]

    clean_timestamp = raw_timestamp.strip("()")
    timestamp = float(clean_timestamp)
    split_result = id_and_data.split("#")

    can_id_hex = split_result[0]
    data_hex = split_result[1]

    return CANFrame(timestamp, interface, can_id_hex, data_hex)

valid_count=0
invalid_count=0
id_counts={}
results=[]

with open("sample_log.txt") as f:
    for line in f:
        line=line.strip()
        if line== "":
            continue
        try:
            frame=parse_line(line)
            valid, reason=frame.is_valid()
        except (IndexError,ValueError) as e:
            print(f"INVALID:malformed line ({e})")
            invalid_count+=1
            continue
        if frame.can_id in id_counts:
            id_counts[frame.can_id]+=1
        else:
            id_counts[frame.can_id]=1
        if valid:
            print(f"ID={frame.can_id}| DATA={frame.data_hex}| VALID")
            valid_count+=1
            results.append({"can_id":frame.can_id,"data_hex":frame.data_hex,"status": "VALID", "reason": reason})
        else:
            print(f"ID={frame.can_id}| DATA={frame.data_hex}| INVALID:{reason}")
            invalid_count+=1
            results.append({"can_id": frame.can_id, "data_hex": frame.data_hex, "status": "INVALID", "reason": reason})
print(f"\nSummary:{valid_count} valid, {invalid_count} invalid")
print("\n Statistics for each ID:")
for can_id, count in id_counts.items():
    print(f"ID={can_id}:{count} mesaje")
with open("results.csv","w",newline="") as csv_file:
    writer=csv.DictWriter(csv_file,fieldnames=["can_id", "data_hex", "status", "reason"])
    writer.writeheader()
    writer.writerows(results)