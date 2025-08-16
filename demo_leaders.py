
import hamplots as hp
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import time
import datetime
import numpy as np


start_epoch = datetime.datetime(2025,8,15,20,50,00).timestamp()  
decodes = hp.read_csv(start_epoch = start_epoch)

mySquares = "IO80,IO81,IO82,IO90,IO91,IO92,JO01,JO02,JO03"
#listener = hp.pskr_listener(mySquares)
#start_epoch = 0
fig, ax = plt.subplots()
plt.ion()

while(True):
   # for i in range(10):
   #     listener.loop(1)
   # decodes = listener.get_decodes()
    remote_calls, homecall_reports = hp.build_connectivity_info(decodes, start_epoch = start_epoch)
    remote_calls_needed = hp.cover_home_calls(remote_calls, homecall_reports)
    if(remote_calls_needed):
        table = hp.tabulate_reports(remote_calls_needed, homecall_reports)
       # print(tx_needed[0:5])
        plt.cla()
        im = hp.plot_snr_heatmap(table, ax)
        #fig.colorbar(im, ax=ax, label="SNR (dB)")
        #fig.tight_layout()
    plt.pause(5)




