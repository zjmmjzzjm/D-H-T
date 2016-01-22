#-*- coding:utf-8 -*-
import MySQLdb
import os
import time

class Mysql_hanle(object):
	def __init__(self, user= 'root', passwd = '123456', port = 3306):
	   self._dbuser = user
	   self._dbpasswd = passwd
	   self._dbport = port
	   self.conn=MySQLdb.connect(host='127.0.0.1',user=self._dbuser, passwd =self._dbpasswd, port=3306,charset="UTF8")
	   self.cur = self.conn.cursor()
	   
	def reconnect(self):
		try:
			self.conn.cping()
		except:
			try:
				self.conn.close()
			except:
				print "Cannot close mysql conn"
			try:
			   self.conn=MySQLdb.connect(host='127.0.0.1',user=self._dbuser, passwd =self._dbpasswd, port=3306,charset="UTF8")
			   self.cur = self.conn.cursor()
			except:
				print "Cannot connect mysql"


	def create_database(self):
		try:
			self.cur=self.conn.cursor()
			self.cur.execute('create database if not exists dht ')
			self.conn.select_db('dht')
			self.cur.execute('drop table if exists hash_info')
			self.cur.execute('drop table if exists keywords')
			self.cur.execute('''CREATE TABLE `hash_info` (
					  `id`  int(11) UNSIGNED NOT NULL AUTO_INCREMENT,
					  `hash` char(40) NOT NULL DEFAULT '' UNIQUE,
					  `info` mediumtext DEFAULT NULL,
					  `size`  bigint UNSIGNED NOT NULL,
					  `time` int UNSIGNED NOT NULL,
					PRIMARY KEY (`id`) 
					) ENGINE=MyISAM  DEFAULT CHARSET=utf8 ''')
			self.cur.execute('''CREATE TABLE `keywords` (
					`id` int UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
					`ip` char(20),
					`keyword` varchar(100)
					)ENGINE=MyISAM  DEFAULT CHARSET=utf8 ''')
			self.cur.execute('''CREATE TABLE `hash_set` (
					`id` int UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
					`hash` char(40) DEFAULT '' UNIQUE,
					`hit` int UNSIGNED NOT NULL, 
					`last_hit_time` int UNSIGNED NOT NULL 
					)ENGINE=MyISAM  DEFAULT CHARSET=utf8 ''')
			self.conn.commit()
		except MySQLdb.Error,e:
			print 'mysql error %d:%s'%(e.args[0],e.args[1])
		finally:
			self.cur.close()


	def insert_info(self, hash, content, size, t ):
		try:
			self.cur=self.conn.cursor()
			self.conn.select_db('dht')
			sql="insert into hash_info(hash,info, size, time) values('%s','%s', '%s' , '%s')"% ( hash, MySQLdb.escape_string(content),size, t)
			self.cur.execute(sql)
			self.conn.commit()
		except MySQLdb.Error,e:
			print 'mysql error %d:%s'%(e.args[0],e.args[1])
			self.reconnect()
		finally:
			self.cur.close()

	def select_all_table(self, table):
		try:
			self.cur=self.conn.cursor()
			self.conn.select_db('dht')
			sql="select * from "+table
			count=self.cur.execute(sql)
			print "thers are %s row in table:"% count
			result=self.cur.fetchall()
			
			for r in result:
				#print 'magnet:?xt=urn:btih:'+r[0].upper()+" info:"+r[1]
				if r[1]!="error" and r[1]!="":
					print r[1]
			self.conn.commit()
		except MySQLdb.Error,e:
			print 'mysql error %d:%s'%(e.args[0],e.args[1])
		finally:
			self.cur.close()

	def executeSQL(self, sql):
		try:
			self.cur=self.conn.cursor()
			self.conn.select_db('dht')
			self.cur.execute(sql)
			self.conn.commit()
		except MySQLdb.Error,e:
			print 'mysql error %d:%s'%(e.args[0],e.args[1])
		finally:
			self.cur.close()

	def query_info_hash_set(self, info_hash):
		try:
			self.cur=self.conn.cursor()
			self.conn.select_db('dht')
			sql="select * from hash_set where hash='%s'"%MySQLdb.escape_string(info_hash.upper())
			#print sql
			self.cur.execute(sql)
			result = self.cur.fetchall()
			self.conn.commit()
			if result == None:
				return False
			if len(result) == 0:
				return False
			return True
		except MySQLdb.Error,e:
			print 'mysql error %d:%s'%(e.args[0],e.args[1])
			self.reconnect()
		finally:
			self.cur.close()
		return False

	
	def insert_info_hash_set(self, info_hash):
		try:
			self.cur=self.conn.cursor()
			self.conn.select_db('dht')
			sql="insert into hash_set(hash, hit, last_hit_time) values('%s','%s', '%s' )"% ( MySQLdb.escape_string(info_hash.upper()),1, int(time.time()))
			self.cur.execute(sql)
			result = self.cur.fetchall()
			self.conn.commit()
		except MySQLdb.Error,e:
			print 'mysql error %d:%s'%(e.args[0],e.args[1])
			self.reconnect()
		finally:
			self.cur.close()

	def close(self):
		try:
			self.conn.close()
		except Exception,e:
			print "close error", str(e)


if(__name__ == '__main__'):
	handler = Mysql_hanle()
	#handler.create_database()	   
	#handler.close()
	handler.insert_info_hash_set("aaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
	ret = handler.query_info_hash_set("aaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
	if ret == False:
		print "not find result"
	else:
		print "find result"
