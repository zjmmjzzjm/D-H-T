#-*- coding:utf-8 -*-
import MySQLdb
import os

class Mysql_hanle(object):
    def __init__(self, user= 'root', passwd = '123456', port = 3306):
       self._dbuser = user
       self._dbpasswd = passwd
       self._dbport = port
       self.conn=MySQLdb.connect(host='127.0.0.1',user=self._dbuser, passwd =self._dbpasswd, port=3306,charset="UTF8")
       self.cur = self.conn.cursor()
       
    def create_database(self):
        try:
            self.cur=self.conn.cursor()
            self.cur.execute('create database if not exists dht')
            self.conn.select_db('dht')
            self.cur.execute('drop table if exists hash_info')
            self.cur.execute('drop table if exists peerIP')
            self.cur.execute('create table hash_info(hash varchar(40), info varchar(1024),primary key(hash)) engine=myisam charset=utf8')
            self.cur.execute('create table peerIP(ip varchar(40), info varchar(100),primary key(ip))')
            self.conn.commit()
        except MySQLdb.Error,e:
            print 'mysql error %d:%s'%(e.args[0],e.args[1])
        finally:
            self.cur.close()


    def insert_info(self, hash, content):
        try:
            self.cur=self.conn.cursor()
            self.conn.select_db('dht')
            sql="insert into hash_info(hash,info) values('%s','%s')"%(hash, content)
            self.cur.execute(sql)
            self.conn.commit()
        except MySQLdb.Error,e:
            print 'mysql error %d:%s'%(e.args[0],e.args[1])
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

    def close(self):
        try:
            self.conn.close()
        except Exception,e:
            print "close error", str(e)


if(__name__ == '__main__'):
    handler = Mysql_hanle()
    handler.create_database()       
    handler.close()
