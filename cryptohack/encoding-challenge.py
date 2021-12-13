import telnetlib
import json
import base64
import codecs

HOST = "socket.cryptohack.org"
PORT = 13377

tn = telnetlib.Telnet(HOST, PORT)

def readline():
    return tn.read_until(b"\n")

def json_recv():
    line = readline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    tn.write(request)

def from_hex(s):
    return bytes.fromhex(s).decode("utf-8")

def from_ascii_list(s):
    return "".join(map(str,[chr(c) for c in s]))


def show_progressbar(iteration, total, prefix = 'Progress:', suffix = '', decimals = 2, length = 25, fill = '#', print_end = "\r"):

    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))  #percent of the progress in format 0:.[decimals]f. eg. 0:.2f
    filled = int(length * iteration // total)                                           #how much of the bar is already filled
    bar = fill * filled + '-' * (length - filled)                                       #inside of the bar
    print(f'\r{prefix} [{bar}] {percent}% {suffix}', end = print_end)                   #format and print the prepared bar
    
    if iteration == total:                                                              #print a new line when the progressbar reaches 100%
        print()

for i in range(100):
    show_progressbar(i, 100, prefix="Decoding strings:")
    received = json_recv()

    if "flag" in received.keys():
        print(f"Result:\n\n{received['flag']}")
        break

    to_send = {"decoded": "changeme"}

    if "error" not in received.keys():
        output = ""

        if received["type"] == "base64":
            output += base64.b64decode(received["encoded"]).decode('utf-8')
        elif received["type"] == "hex":
            output += from_hex(received["encoded"])
        elif received["type"] == "bigint":
            output += from_hex(received["encoded"][2:])
        elif received["type"] == "rot13":
            output += codecs.decode(received["encoded"], encoding="rot13")
        else:
            output += from_ascii_list(received["encoded"])

        to_send["decoded"] = output
        
    json_send(to_send)


