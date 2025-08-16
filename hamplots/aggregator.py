
import hamplots as hp
import time


def periodic_mqtt_update():
    mySquares = "IO80,IO81,IO82,IO90,IO91,IO92,JO01,JO02,JO03"
    myBands = "40m, 20m, 15m, 10m, 2m"
    myModes = "FT8, FT4"

    rx_listener = hp.pskr_listener(mySquares, modes = myModes, bands = myBands, TxRx = "Rx")
    tx_listener = hp.pskr_listener(mySquares, modes = myModes, bands = myBands, TxRx = "Tx")

    lifetime = 15*60

    while(True):
        epoch = time.time()

        rx_listener.purge_decodes(epoch - lifetime)
        tx_listener.purge_decodes(epoch - lifetime)
        
        for i in range(50):
            rx_listener.loop(1)
        rx_listener.write_csv(filepath =  "Rx_decodes.csv")
            
        for i in range(50):
            tx_listener.loop(1)
        tx_listener.write_csv(filepath =  "Tx_decodes.csv")

        time.sleep(10)

def run():
    periodic_mqtt_update()

if __name__ == "__main__":
    run()
