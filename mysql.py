#-*- coding:utf-8 -*-
import MySQLdb
import os

class Mysql_hanle(object):
    def __init__(self, user= 'root', passwd = '123456', port = 3306):
       self._dbuser = user
       self._dbpasswd = passwd
       self._dbport = port
       conn=MySQLdb.connect(host='127.0.0.1',user=self._dbuser, passwd =self._dbpasswd, port=3306,charset="UTF8")
    def create_database(self):
        try:
            cur=conn.cursor()
            cur.execute('create database if not exists dht')
            conn.select_db('dht')
            cur.execute('drop table if exists hash_info')
            cur.execute('drop table if exists peerIP')
            cur.execute('create table hash_info(hash varchar(40), info varchar(300),primary key(hash)) engine=myisam charset=utf8')
            cur.execute('create table peerIP(ip varchar(40), info varchar(100),primary key(ip))')
            conn.commit()
        except MySQLdb.Error,e:
            print 'mysql error %d:%s'%(e.args[0],e.args[1])

    def insert_info(self, hash, content):
        try:
            cur=conn.cursor()
            conn.select_db('dht')
            sql="insert into hash_info(hash,info) values('%s','%s')"%(hash, content)
            cur.execute(sql)
            conn.commit()
        except MySQLdb.Error,e:
            print 'mysql error %d:%s'%(e.args[0],e.args[1])

    def select_all_table(self, table):
        try:
            cur=conn.cursor()
            conn.select_db('dht')
            sql="select * from "+table
            count=cur.execute(sql)
            print "thers are %s row in table:"% count
            result=cur.fetchall()
            
            for r in result:
                #print 'magnet:?xt=urn:btih:'+r[0].upper()+" info:"+r[1]
                if r[1]!="error" and r[1]!="":
                    print r[1]
            conn.commit()
        except MySQLdb.Error,e:
            print 'mysql error %d:%s'%(e.args[0],e.args[1])

    def executeSQL(self, sql):
        try:
            cur=conn.cursor()
            conn.select_db('dht')
            cur.execute(sql)
            conn.commit()
        except MySQLdb.Error,e:
            print 'mysql error %d:%s'%(e.args[0],e.args[1])



if(__name__ == '__main__'):
    handler = Mysql_hanle()
    handler.create_database()       
