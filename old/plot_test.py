
import matplotlib.pyplot as plt
import pickle
import operator
import matplotlib.colors as mcolors

def get_color_for_tx(tx):
    if tx not in tx_colors:
        # pick a color from matplotlib's tab20 palette, cycling if needed
        all_colors = list(mcolors.TABLEAU_COLORS.values())
        tx_colors[tx] = all_colors[len(tx_colors) % len(all_colors)]
    return tx_colors[tx]



with open("decodes.pkl",'rb') as f:
    decodes = pickle.load(f)

plt.ion()
fig, ax = plt.subplots()
ax.set_xlabel("Callsign")
ax.set_ylabel("SNR (dB)")
art = False


f_all = 14074000
txCalls = set()
for d in decodes:
    if(abs(float(d['f'])-f_all)>10000):
        continue
    txCalls.add(d['sc'])

default_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
tx_colors = {}


rx_reports = {}
for i, d in enumerate(decodes):
    tx=d['sc']
    rx=d['rc']
    report = {'tx':tx,'rp':int(d['rp'])}
    rx_reports.setdefault(rx, []).append(report)

sorted_rx = sorted(rx_reports.keys(), key=lambda rx: max(report['rp'] for report in rx_reports[rx]), reverse=True)
x_vals = []
y_vals = []
cols = []
for i, rx in enumerate(sorted_rx):
    for report in rx_reports[rx]:
        x_vals.append(rx)
        y_vals.append(report['rp'])
        cols.append(get_color_for_tx(report['tx']))
plt.cla()
ax.scatter(x_vals, y_vals, c = cols, alpha=0.7)

ax.tick_params("x", rotation=90, labelsize=6)





