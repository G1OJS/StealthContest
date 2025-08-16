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
        t = datetime.datetime.fromtimestamp(d['t'])
        d.update({'t_str':str(t).replace(' ','_')})
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
                dtbfm = f"{d['t_str']}, d['t']}, {d['b']}, {d['f']}, {d['md']}, "
                spot = f"{d['hc']}, {d['hl']}, {d['ha']}, {d['TxRx']}, {d['oc']}, {d['ol']}, {d['oa']}, {d['rp']}\n"
                f.write(dtbfm+spot)

def str_to_epoch(t_str):
    import datetime
    yy = int(t_str[0:4])
    m = int(t_str[5:7])
    dd = int(t_str[8:10])
    hh = int(t_str[11:13])
    mm = int(t_str[14:16])
    ss = int(t_str[17:19])
    return datetime.datetime(yy,m,dd,hh,mm,ss).timestamp()

def read_csv(filepath =  "decodes.csv", start_epoch = 0):
    print(f"Reading spots from {filepath}")
    decodes = []
    with open(filepath, "r") as f:
        for l in f.readlines():
            ls=l.strip().split(", ")
            d = {'t_str':ls[0], 'b':ls[1], 'f':ls[2], 'md':ls[3], 'hc':ls[4], 'hl':ls[5], 'ha':ls[6], 'TxRx':ls[7], 'oc':ls[8], 'ol':ls[9], 'oa':ls[10], 'rp':ls[11]}
            if(str_to_epoch(d['t_str']) < start_epoch):
                continue
            decodes.append(d)
    return decodes



