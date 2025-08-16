def str_to_epoch(t_str):
    import datetime
    yy = int(t_str[0:4])
    m = int(t_str[5:7])
    dd = int(t_str[8:10])
    hh = int(t_str[11:13])
    mm = int(t_str[14:16])
    ss = int(t_str[17:19])
    return datetime.datetime(yy,m,dd,hh,mm,ss).timestamp()
