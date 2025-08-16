import paho.mqtt.client as mqtt
import ast
import datetime

class pskr_listener:
    def __init__(self, squares, bands="20m", modes="FT8", direction = "Rx", csv_file = "Rx_decodes.csv"):
        self.decodes = []
        self.squares = squares.split(",")
        self.bands = bands.split(",")
        self.modes = modes.split(",")
        self.direction = direction
        self.mqtt_cl = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqtt_cl.on_connect = self.subscribe
        self.mqtt_cl.on_message = self.add_decode
        self.mqtt_cl.connect("mqtt.pskreporter.info", 1883, 60)
        self.csvfilepath = csv_file

    def loop(self, timeout):
        self.mqtt_cl.loop(timeout)

    def loop_forever(self, timeout):
        self.mqtt_cl.loop_forever()

    def get_decodes(self):
        return self.decodes
        
    def subscribe(self, client, userdata, flags, reason_code, properties):
        # pskr/filter/v2/{band}/{mode}/{sendercall}/{receivercall}/{senderlocator}/{receiverlocator}/{sendercountry}/{receivercountry}
        print(f"Connected: {reason_code}")
        for sq in self.squares:
            for b in self.bands:
                for md in self.modes:
                    print(f"Subscribe to {self.direction} in {sq} on {b} {md}")
                    tailstr = f"+/+/{sq}/+/+/#" if self.direction == "Tx" else f"+/+/+/{sq}/+/#"
                    client.subscribe(f"pskr/filter/v2/{b}/{md}/{tailstr}")

    def add_decode(self, client, userdata, msg):
        d = ast.literal_eval(msg.payload.decode())
        d['sl'] = d['sl'].upper()
        d['rl'] = d['rl'].upper()
        d.update({'TxRx':self.direction})
        d.update({'hc':  d['rc'] if self.direction =="Rx" else d['sc']})
        d.update({'hl':  d['rl'] if self.direction =="Rx" else d['sl']})
        d.update({'ha':  d['ra'] if self.direction =="Rx" else d['sa']})
        d.update({'oc':  d['sc'] if self.direction =="Rx" else d['rc']})
        d.update({'ol':  d['sl'] if self.direction =="Rx" else d['rl']})
        d.update({'oa':  d['sa'] if self.direction =="Rx" else d['ra']})
        self.decodes.append(d)

    def write_csv(self, decodes = None, filepath =  "decodes.csv"):
        if(decodes == None):
            decodes = self.decodes
        print(f"Writing spots to {filepath}")
        with open(filepath, "w") as f:
            for d in decodes:
                ebfm = f"{d['t']}, {d['b']}, {d['f']}, {d['md']}, "
                spot = f"{d['hc']}, {d['hl']}, {d['ha']}, {d['TxRx']}, {d['oc']}, {d['ol']}, {d['oa']}, {d['rp']}\n"
                f.write(ebfm+spot)



class wsjt:
    
    def parse_line_datetime(line):
        ## includes kludge to convert to BST
         return datetime.datetime(2000+int(line[0:2]),int(line[2:4]),int(line[4:6]),
                                 (int(line[7:9])+1) % 24, int(line[9:11]), int(line[11:13]) ).timestamp()

    def parse_line(line):
        import re
        dt = parse_line_datetime(line)
        ls = line.split()
        if len(ls) == 10:
            sq = ls[9]
            if(re.search("[A-R][A-R][0-9][0-9]",sq) and sq != "RR73"):            
                return {
                    "dt": dt,
                    "f": float(ls[1])*1e6,
                    "sc": ls[8],
                    "rc": "G1OJS",
                    "rp": float(ls[4]),
                    "sl": ls[9],
                    "rl": "IO90",
                    "km": None,
                    "deg":None
                }
            
    def read_ALLTXT(fpath, dt_first, home_square):
       # print(f"{fpath}")
        with open(fpath) as f:
            lines = f.readlines()
        decodes_all = []

        km = {}
        deg = {}
        nrecs = 0
        for l in lines:
            if(len(l)>100):
                continue
            dt = parse_line_datetime(l)
            if(dt < dt_first):
                continue
            decode = parse_line(l)
            if decode:
                sc = decode["sc"]
                if(sc not in km):
                    kmdeg = sq_km_deg(decode["sl"], home_square)
                    if(kmdeg):
                        km[sc], deg[sc] = kmdeg
                decodes_all.append(decode)
                nrecs += 1
      #    print(f"Read {len(lines)} lines with {nrecs} decodes in session time window\n")
        return decodes_all



