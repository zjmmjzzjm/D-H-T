#!/usr/bin/env python
# coding: utf-8


import os
import sys
import time
import json
import random
import traceback as tb
import tempfile

import libtorrent as lt
import MySQLdb

class DownloadParam(object):
    _time_out = 40
    def __init__(self):
       self.start_time = -1

    def is_timeout(self):
        if(time.time() - self.start_time > self._time_out):
            return True
        else:
            return False
            


class Collector(object):
    '''
    一个简单的 bt 下载工具，依赖开源库 libtorrent.
    '''
    # libtorrent下载配置
    _upload_rate_limit = 200000
    _download_rate_limit = 200000
    _active_downloads = 30
    _alert_queue_size = 4000
    _dht_announce_interval = 60
    _torrent_upload_limit = 20000
    _torrent_download_limit = 20000
    _auto_manage_startup = 30
    _auto_manage_interval = 15

    # 主循环 sleep 时间
    _sleep_time = 0.5
    _start_port = 32800
    _sessions = []
    _infohash_queue_from_getpeers = []
    _info_hash_set = {}
    _current_meta_count = 0
    _meta_list = {}
    _download_meta_params = {}

    def __init__(self,
                 session_nums=50,
                 delay_interval=20,
                 exit_time=15*60,
                 result_file=None,
                 stat_file=None):
        self._session_nums = session_nums
        self._delay_interval = delay_interval
        self._exit_time = exit_time
        self._result_file = result_file
        self._stat_file = stat_file
        self._backup_result()
        self.download_session = lt.session()
        self.download_session.add_dht_router('router.bittorrent.com', 6881)
        self.download_session.add_dht_router('router.utorrent.com', 6881)
        self.download_session.add_dht_router('router.bitcomet.com', 6881)
        self.download_session.add_dht_router('dht.transmissionbt.com', 6881)


    def _backup_result(self):
        back_file = '%s_%s' % (time.strftime('%Y%m%d'), self._result_file)
        if os.path.isfile(self._result_file) and not os.path.isfile(back_file):
            os.system('cp %s %s_%s' %
                      (self._result_file,
                       time.strftime('%Y%m%d'),
                       self._result_file))

    def _backup_all_info_hash(self):
        back_file = '%s_%s' % (time.strftime('%Y%m%d'), self._result_file)
        if not os.path.isfile(back_file):
            f = open(back_file, 'w')
            for  info_hash in self._meta_list:
                f.write(info_hash)

    def _insert_info_hash(self, info_hash):
        back_file = '%s_%s' % (time.strftime('%Y%m%d'), self._result_file)
        try :
            f = open(back_file, 'a')
            f.write(info_hash+'\n')
            f.close()
        except Exception, e:
            print "catch excepton: " + str(e)

    def _get_runtime(self, interval):
        day = interval / (60*60*24)
        interval = interval % (60*60*24)
        hour = interval / (60*60)
        interval = interval % (60*60)
        minute = interval / 60
        interval = interval % 60
        second = interval
        return 'day: %d, hour: %d, minute: %d, second: %d' % \
               (day, hour, minute, second)

    # 辅助函数
    # 事件通知处理函数
    def _handle_alerts(self, session, alerts):
        while len(alerts):
            alert = alerts.pop()
            if isinstance(alert, lt.add_torrent_alert):
                alert.handle.set_upload_limit(self._torrent_upload_limit)
                alert.handle.set_download_limit(self._torrent_download_limit)
            elif isinstance(alert, lt.dht_announce_alert):
                info_hash = alert.info_hash.to_string().encode('hex')
                if info_hash in self._meta_list:
                    self._meta_list[info_hash] += 1
                else:
                    self._meta_list[info_hash] = 1
                    self.get_torrent(self.download_session, info_hash)
                    self._current_meta_count += 1
            elif isinstance(alert, lt.dht_get_peers_alert):
                info_hash = alert.info_hash.to_string().encode('hex')
                if info_hash in self._meta_list:
                    self._meta_list[info_hash] += 1
                else:
                    self._infohash_queue_from_getpeers.append(info_hash)
                    self._meta_list[info_hash] = 1
                    self.get_torrent(self.download_session, info_hash)
                    self._current_meta_count += 1

    # 创建 session 对象
    def create_session(self, begin_port=32800):
        self._start_port = begin_port
        for port in range(begin_port, begin_port + self._session_nums):
            session = lt.session()
            session.set_alert_mask(lt.alert.category_t.all_categories)
            session.listen_on(port, port)
            session.add_dht_router('router.bittorrent.com', 6881)
            session.add_dht_router('router.utorrent.com', 6881)
            session.add_dht_router('router.bitcomet.com', 6881)
            session.add_dht_router('dht.transmissionbt.com', 6881)
            settings = session.get_settings()
            settings['upload_rate_limit'] = self._upload_rate_limit
            settings['download_rate_limit'] = self._download_rate_limit
            settings['active_downloads'] = self._active_downloads
            settings['auto_manage_startup'] = self._auto_manage_startup
            settings['auto_manage_interval'] = self._auto_manage_interval
            settings['dht_announce_interval'] = self._dht_announce_interval
            settings['alert_queue_size'] = self._alert_queue_size
            session.set_settings(settings)
            self._sessions.append(session)
        return self._sessions
    
    def get_torrent(self, ses, hash_info):
        '''
        Add hash_info to session, begin down load torrent
        '''

        return
        self._insert_info_hash(hash_info)
        if (self._download_meta_params.has_key(hash_info) is True):
            print "info hash" + hash_info + "already downloading"
            return

        download_param = DownloadParam()
        download_param.start_time = time.time()

        self._download_meta_params[hash_info] = download_param

        magnet='magnet:?xt=urn:btih:'+hash_info
        print "Add magnet ", magnet
        tempdir = tempfile.mkdtemp()
        params = {
            'save_path': tempdir,
            'duplicate_is_error': True,
            'storage_mode': lt.storage_mode_t(2),
            'paused': False,
            'auto_managed': True,
            'duplicate_is_error': True
        }

        lt.add_magnet_uri(ses, magnet, params)

    
    def check_download_torrent(self):
        handles = self.download_session.get_torrents() 
        for handle in handles:
            info_hash = handle.info_hash().to_string().encode('hex')
            if(not handle.has_metadata()):
                if(self._download_meta_params.has_key(info_hash) ):
                    p =  self._download_meta_params[info_hash]
                    if (p.is_timeout()):
                        self.download_session.remove_torrent(handle)
                        self._download_meta_params.pop(info_hash)
                        print "remove time out ",info_hash
            else:
                if(self._download_meta_params.has_key(info_hash) ):
                    self._download_meta_params.pop(info_hash)
                torinfo = handle.get_torrent_info()
                content = self.dump_torrent_info(torinfo)
                self.saveHashInfo(info_hash, content)
                self.download_session.remove_torrent(handle)
                
    def dump_torrent_info(self,info):
        content = info.name()  + "\n"
        num_file = info.num_files()
        content += str(num_file) + "\n"
        for i in range(num_file):
            f = info.file_at(i)
            content += f.path + ' ' + str(f.size) + "\n"
        print "",content 

        return content

    def start_work(self):
        # 清理屏幕
        begin_time = time.time()
        show_interval = self._delay_interval
        while True:
            for session in self._sessions:
                session.post_torrent_updates()
                self._handle_alerts(session, session.pop_alerts())
            time.sleep(self._sleep_time)
            if show_interval > 0:
                show_interval -= 1
                continue
            show_interval = self._delay_interval
            self.check_download_torrent()

            # 统计信息显示
            show_content = ['torrents:']
            interval = time.time() - begin_time
            show_content.append('  pid: %s' % os.getpid())
            show_content.append('  time: %s' %
                                time.strftime('%Y-%m-%d %H:%M:%S'))
            show_content.append('  run time: %s' % self._get_runtime(interval))
            show_content.append('  start port: %d' % self._start_port)
            show_content.append('  collect session num: %d' %
                                len(self._sessions))
            show_content.append('  info hash nums from get peers: %d' %
                                len(self._infohash_queue_from_getpeers))
            show_content.append('  torrent collection rate: %f /minute' %
                                (self._current_meta_count * 60 / interval))
            show_content.append('  current torrent count: %d' %
                                self._current_meta_count)
            show_content.append('  total torrent count: %d' %
                                len(self._meta_list))
            show_content.append('\n')



	def destroy_sessions(self):
		'''
        销毁p2p客户端
		'''
        for session in self._sessions:
            torrents = session.get_torrents()
            for torrent in torrents:
                session.remove_torrent(torrent)


    def saveHashInfo(self, info_hash, torrent_content):
        '''
		save info to database
        '''
        return
        try:
            conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='123456',port=3306,charset="UTF8")
            cur=conn.cursor()
            conn.select_db('dht')
	    hash_hex=info_hash
	    sql="insert into hash_info(hash,info) values('%s','%s')"%(hash_hex,torrent_content)
	    try:
	        cur.execute(sql)
	        conn.commit()
	    except MySQLdb.Error,e:
	        print 'mysql error %d:%s'%(e.args[0],e.args[1])
            cur.close()
            conn.close()
        except MySQLdb.Error,e:
            print 'mysql error %d:%s'%(e.args[0],e.args[1])

if __name__ == '__main__':
    #if len(sys.argv) != 3:
    #    print 'argument err:'
    #    print '\tpython collector.py result.json collector.state\n'
    #    sys.exit(-1)

    #result_file = sys.argv[1]
    #stat_file = sys.argv[2]

    result_file = 'test'

    stat_file = 'test2'
    # 创建采集对象
    sd = Collector(session_nums=20,
                   result_file=result_file,
                   stat_file=stat_file)
    # 创建p2p客户端
    sd.create_session(32900)
    sd.start_work()
