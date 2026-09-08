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

        return True, "VALID" #returneaza un tuple, nu e musai sa aiba paranteze de tipul (True/False|Mesaj)


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

with open("sample_log.txt") as f: # deschide fisierul si il inchide automat
    for line in f: #parcurge fiecare linie din fisier
        line=line.strip() #elimina spatiile si \n
        if line== "": #asta e o verificare extra, in caz de exista un rand gol care avea un newline
            continue
        try: # e mai bun try daca codul functioneaza in mare parte a timpului fat de if si daca se pot intampla crashuri random
            frame=parse_line(line)
            valid, reason=frame.is_valid() #face legatura cu tupleul (TRUE/FALSE,Mesaj) din functia is_valid()
        except (IndexError,ValueError) as e: #salveaza obiectul erorii in variabila e
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