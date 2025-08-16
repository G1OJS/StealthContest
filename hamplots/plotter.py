import hamplots as hp
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import time

myBands = "40m, 20m, 15m"
myModes = "FT8, FT4"

def periodic_update_plots:
    while True:

        for RxTx in ["Rx","Tx"]:
            decodes = hp.read_csv(f"{RxTx}_decodes.csv")
            for band in myBands.split(", "):
                for mode in myModes.split(", "):
                    print(f"Rx_{band}_{mode}")

                    remote_calls, homecall_reports = hp.build_connectivity_info(decodes, bands=band, modes=mode)
                #    remote_calls_needed = hp.cover_home_calls(remote_calls, homecall_reports)
                    remote_calls_needed = remote_calls
                    
                    if remote_calls_needed:
                        rowheads, colheads, rows = hp.tabulate_reports(remote_calls_needed, homecall_reports)

                        # build DataFrame
                        import pandas as pd
                        data = pd.DataFrame(rows, index=rowheads, columns=colheads)
                        
                        # sort by counts
                        row_counts = data.replace(-30, np.nan).count(axis=1)
                        col_counts = data.replace(-30, np.nan).count(axis=0)
                        data = data.loc[row_counts.sort_values(ascending=False).index,
                                        col_counts.sort_values(ascending=False).index]

                        # mask missing values
                        mask = data == -30

                        # plot seaborn heatmap
                        plt.figure(figsize=(max(6, len(colheads)*0.5), max(4, len(rowheads)*0.5)))
                        sns.heatmap(data, mask=mask, annot=True, fmt="d", cmap="hot",
                                    cbar_kws={"label":"SNR (dB)"})
                        plt.xlabel("Home stations")
                        plt.ylabel("Remote stations")
                        plt.title(f"{RxTx} {band} {mode}")
                        plt.xticks(rotation=90)
                        plt.yticks(rotation=0)
                        plt.tight_layout()
                        plt.savefig(f"../plots/{RxTx}_{band}_{mode}.png")
                        plt.close()
        
        time.sleep(5)

def run():
    periodic_update_plots()

if __name__ == "__main__":
    run()

