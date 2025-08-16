
def tabulate_reports(remote_calls, homecall_reports):
    colheads = [""]
    for hc in homecall_reports:
        colheads.append(hc)
    rows = [colheads]

    for rc in remote_calls:
        row = [rc]
        for hc in homecall_reports:
            row.append(max(int(rp) for rp in homecall_reports[hc][rc])  if rc in homecall_reports[hc] else -30)
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
    col_labels = table[0][1:]
    row_labels = [row[0] for row in table[1:]]

    grid = [ [float(cell) if cell != '' else fill_value for cell in row[1:]]
        for row in table[1:] ]
    
    im = ax.imshow(grid, cmap=cmap)
    ax.set_xticks(range(len(col_labels)), labels=col_labels, rotation=90, size = 6)
    ax.set_yticks(range(len(row_labels)), labels=row_labels, size = 6)

    return im

def build_connectivity_info(decodes, start_epoch = 0):
    # return
    # calls[callsign] = nSpots
    # spots[homecall] = [reports]
    remote_calls = {}
    homecall_reports = {}
    for d in decodes:
        if(int(d['t']) < start_epoch):
            continue
        homecall_reports.setdefault(d['hc'],{})
        homecall_reports[d['hc']].setdefault(d['oc'],[]).append(d['rp'])
        remote_calls.setdefault(d['oc'],0)
        remote_calls[d['oc']] += 1
    return remote_calls, homecall_reports

        
def cover_home_calls(calls,  spots):
    # sort calls according to number of reports
    calls = dict(sorted(calls.items(), key=lambda key_val: key_val[1], reverse = True))
    #go through calls in order of decreeasing number of home call spots
    #noting snr until all home calls have a spot
    to_cover = []
    for hc in spots:
        to_cover.append(hc)
    needed = []
    for c in calls:
        needed.append(c)
        for hc in spots:
            if(c in spots[hc]):
                if(hc in to_cover):
                    to_cover.remove(hc)
                if (len(to_cover)==0):
                    return needed
    return False

def read_csv(filepath =  "decodes.csv", start_epoch = 0):
    print(f"Reading spots from {filepath}")
    decodes = []
    with open(filepath, "r") as f:
        for l in f.readlines():
            ls=l.strip().split(", ")
            d = {'t':ls[0], 'b':ls[1], 'f':ls[2], 'md':ls[3], 'hc':ls[4], 'hl':ls[5], 'ha':ls[6], 'TxRx':ls[7], 'oc':ls[8], 'ol':ls[9], 'oa':ls[10], 'rp':ls[11]}
            if(int(d['t']) < start_epoch):
                continue
            decodes.append(d)
    return decodes








