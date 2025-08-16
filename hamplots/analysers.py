
def tabulate(tx_calls, homecall_spots):
    # print out tabulated
    print("\n\n")
    colheads = [""]
    for hc in homecall_spots:
        colheads.append(hc)
    rows = [colheads]

    for tx in tx_calls:
        row = [tx]
        for hc in homecall_spots:
            hit = False
            for rp in homecall_spots[hc]:
                if(tx == rp['oc']):
                    row.append(int(rp['rp']))
                    hit = True
            if(not hit):    
                row.append('')
        rows.append(row)

    return rows

def print_table(rows):
    for r in rows:
        txt=""
        for c in r:
            if(c is None):
                c = ''
            txt+=(f"{c:<10}")
        print(txt)

def plot_snr_heatmap(table, ax, fill_value=-30, cmap='hot'):
    # Extract labels
    col_labels = table[0][1:]
    row_labels = [row[0] for row in table[1:]]

    # Fill missing entries and convert to float
    grid = [
        [float(cell) if cell != '' else fill_value for cell in row[1:]]
        for row in table[1:]
    ]
    
    # Plot onto provided Axes
    im = ax.imshow(grid, cmap=cmap)
    ax.set_xticks(range(len(col_labels)), labels=col_labels, rotation=90, size = 6)
    ax.set_yticks(range(len(row_labels)), labels=row_labels, size = 6)

    return im  # so caller can attach colorbar

def build_connectivity_info(decodes, start_epoch = 0):
    from . pskr_utils import str_to_epoch 
    #build unique list of home calls, tx calls with count of Rx reports,
    #and list of {tx call, report} for each homecall
    home_calls = {}
    tx_calls = {}
    homecall_spots = {}
    for d in decodes:
        if(str_to_epoch(d['t_str']) < start_epoch):
            continue
        homecall_spots.setdefault(d['hc'],[]).append({'oc':d['oc'],'rp':d['rp']})
        home_calls.setdefault(d['hc'],0)
        tx_calls.setdefault(d['oc'],0)
        tx_calls[d['oc']] += 1

    return home_calls, tx_calls, homecall_spots

        
def cover_home_calls(tx_calls, home_calls, homecall_spots):
    # sort tx calls according to number of rx reports
    tx_calls = dict(sorted(tx_calls.items(), key=lambda key_val: key_val[1], reverse = True))

    #go through tx calls in order of decreeasing number of home call spots
    #noting snr until all home calls have a spot
    to_cover = []
    for hc in home_calls:
        to_cover.append(hc)
    tx_needed = []
    for tx in tx_calls:
        tx_needed.append(tx)
        for hc in homecall_spots:
            for rp in homecall_spots[hc]:
                if(tx in rp['oc']):
                    if(hc in to_cover):
                        to_cover.remove(hc)
                    if (len(to_cover)==0):
                        return tx_needed
    return False




def read_csv(filepath =  "decodes.csv", start_epoch = 0):
    print(f"Reading spots from {filepath}")
    decodes = []
    with open(filepath, "r") as f:
        for l in f.readlines():
            ls=l.strip().split(", ")
            d = {'t':ls[0], 'b':ls[1], 'f':ls[2], 'md':ls[3], 'hc':ls[4], 'hl':ls[5], 'ha':ls[6], 'TxRx':ls[7], 'oc':ls[8], 'ol':ls[9], 'oa':ls[10], 'rp':ls[11]}
            if(str_to_epoch(d['t_str']) < start_epoch):
                continue
            decodes.append(d)
    return decodes








