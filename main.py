import flow





ip_lst = flow.get_ip_lst_1()
flow.check_ip(ip_lst, song_id=157014)

ip_lst = flow.get_ip_lst_2()
flow.check_ip(ip_lst, song_id=157014)

ip_lst = flow.get_ip_lst_3()
flow.check_ip(ip_lst, song_id=157014)

ip_lst = flow.get_ip_lst_4(3)
flow.check_ip(ip_lst, song_id=157014)
