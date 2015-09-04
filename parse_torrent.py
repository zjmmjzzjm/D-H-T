import libtorrent as lt
import time
import os

import sys
import mysql

if __name__ == "__main__":
    dirname = "torrents/"

    mysql_handle = mysql.Mysql_hanle()
    for root,dirs, files in os.walk(dirname):
        if len(files) == 0:
            continue
        for f in files:
            torrent_name = root + '/' + f;
            try:
                #ses = lt.session()
                #ses.listen_on(6881, 6891)

                e = lt.bdecode(open(torrent_name, 'rb').read())
                info = lt.torrent_info(e)

                print "info_hash " + info.info_hash().to_string().encode("HEX")
                content = info.name() + "\n"
                print info.name()
                num_file = info.num_files()
                print "num_files ", num_file
                for i in range(num_file):
                    f = info.file_at(i)
                    content += f.path + " " + str(f.size) + "\n"
                print content
                mysql_handle.insert_info(info.info_hash().to_string().encode("HEX"),content)
                    
            except Exception , e:
                print "cannot parse torrent " +  torrent_name , e
                pass

#pass
#params = { save_path: '.', \
#        storage_mode: lt.storage_mode_t.storage_mode_sparse, \
#        ti: info }
#h = ses.add_torrent(params)
#
#s = h.status()
#while (not s.is_seeding):
#    s = h.status()
#    state_str = ['queued', 'checking', 'downloading metadata', \
#    'downloading', 'finished', 'seeding', 'allocating']
#    print '%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
#    (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
#    s.num_peers, state_str[s.state])
#    time.sleep(1)
