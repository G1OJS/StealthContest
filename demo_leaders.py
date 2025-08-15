
import StealthContest as sc
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import time
import datetime
import numpy as np


#start_epoch = datetime.datetime(2025,8,15,21,50,00).timestamp()  
#decodes = sc.read_csv(start_epoch = start_epoch)

mySquares = "IO80,IO81,IO82,IO90,IO91,IO92,JO01,JO02,JO03"
listener = sc.pskr_listener(mySquares)
start_epoch = 0
fig, ax = plt.subplots()
plt.ion()

while(True):
    listener.loop(5)
    decodes = listener.get_decodes()
    home_calls, tx_calls, homecall_spots = sc.build_connectivity_info(decodes, start_epoch = start_epoch)
    tx_needed = sc.cover_home_calls(tx_calls, home_calls, homecall_spots)
    table = sc.tabulate(tx_calls, homecall_spots)
    if(len(table)>3):
        plt.cla()
        im = sc.plot_snr_heatmap(table, ax)
        #fig.colorbar(im, ax=ax, label="SNR (dB)")
        #fig.tight_layout()
    plt.pause(5)




