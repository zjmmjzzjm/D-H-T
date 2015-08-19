import libtorrent as lt
import time

import sys

ses = lt.session()
ses.listen_on(6881, 6891)

e = lt.bdecode(open(sys.argv[1], 'rb').read())
info = lt.torrent_info(e)

print "info_hash " + info.info_hash().to_string().encode("HEX")
print "torrent info name " + info.name()

num_file = info.num_files()
print "num_files ", num_file
for i in range(num_file):
    f = info.file_at(i)
    print "path",f.path, " size ", str(f.size) 
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
