# -*- coding: utf-8 -*-

import sqlite3
import logging
import json

from common import Result
from database import RelationalDatabaseInterface

class SQLiteBase(RelationalDatabaseInterface):
    """
    sqlite3封装类，实现关系型数据库通用增删查改方法。
        实例化需要传入数据库路径，日志对象，初始化脚本或者初始化脚本文件路径。

        由于sqlite没有用户角色，也就没有权限管理，因此作为数据存储他的功能是非常单一的，我将数据表的增删查改
        作为基础功能实现，在其他模块中可以很容易使用这些功能。但是由于过于复杂，没有实现其他的SQL，这些会考虑
        之后进行添加。
    """
    name            = u"sqlite database"
    database_path   = None
    logger          = None

    def __init__(self, database_path, logger=logging, init_script=None, init_script_file=None):
        """
        确保database_path的dirname存在并且有访问权限。
        初始化脚本和初始化脚本文件可以同时存在，当两者同时存在会先执行初始化脚本再执行初始化脚本文件。
        """
        self.database_path = database_path
        self.logger        = logger
        
        if init_script is not None:
            self.initDB(init_script)
        
        if init_script_file is not None:
            try:
                f = open(init_script_file, 'r')
                init_script = f.read()
            except Exception:
                self.logger.exception(u"open script file fail.")
                raise
            self.initDB(init_script)

    def connectDB(self):
        """
        sqlite为了数据确保线程安全，因此禁止连接对象跨线程或者跨进程使用，意味着为了支持跨线程和跨进
        程，需要在每次增删查改操作前连接数据库，并在操作完成后断开数据库。
        """
        conn = sqlite3.connect(self.database_path)
        if conn is None:
            self.logger.error(u"connect to database fail.")
            self.logger.debug(u"database path: {}".format(self.database_path))
            raise Exception("disconnect to database")
        return conn

    def initDB(self, sqls):
        """
        执行初始化脚本，执行失败时抛出错误。
        """
        conn = self.connectDB()
        
        try:
            conn.executescript(sqls)
            conn.commit()
            self.logger.info(u"database initialize successfully.")
        except:
            self.logger.exception(u"Execute initialize sql script error.")
            conn.rollback()
            raise
        finally:
            conn.close()

    def _parseCol(self, columns):
        """
        把输入的columns列表变为`item1, item2, item3....`格式的字符串。原则上该方法被用来转化记录
        或者查询条件中的列名，因此columns中元素为字符串。
        """
        return json.dumps(columns).replace(u"\"", u"").strip(u'[]')

    def _parseVal(self, values):
        """
        把输入的values列表变为'item1, item2, item3...'格式的字符串。原则上
        该方法用于转化记录或者查询条件中的值。因此values必须保证为int、float、string、bool.

        调用时确保values中字符串应该为utf-8格式。
        bool会被转换成0和1。
        字符串会添加引号。
        """
        vals = []
        for v in values:
            if type(v) == type(True):
                vals.append(int(v))
            else:
                vals.append(v)
        return json.dumps(values, ensure_ascii=False).strip(u'[]')

    def _parseEquation(self, record):
        """
        把输入的record变成'k1 = v1 and k2 = v2'的格式

        当v为字符串时需要添加引号
        """
        expr = u""
        for k, v in record.items():
            if type(v) == type(u''):
                expr += u' {} = "{}" and'.format(k, v)
            else:
                expr += u' {} = {} and'.format(k, v)
        return expr[1:-4]

    def insert(self, tableName, record):
        """
        插入数据
            tableName数据库表名
            record为一条记录，dict格式，其中key作为COL名，value作为值插入

        当数据库连接失败时应该抛出错误。
        """
        conn = self.connectDB()

        # 确保tableName编码为unicode
        if type(tableName) == type(''):
            tableName = tableName.decode('utf-8')
        # 确保record的value编码为unicode
        record = json.loads(json.dumps(record))

        sql       = u"INSERT INTO {} ({}) VALUES ({});"
        colExpr   = self._parseCol(record.keys())
        valueExpr = self._parseVal(record.values())

        sql = sql.format(tableName, colExpr, valueExpr)
        self.logger.debug(u'insert sql: {}'.format(sql))

        cur = conn.cursor()
        try:
            cur.execute(sql)
            if cur.rowcount == 1:
                self.logger.debug("insert success.")
                conn.commit()
                return Result({u'success': True, u'record': record})
            else:
                self.logger.debug("insert fail.")
                conn.rollback()
                return Result({u'success': False, u'errmsg': u'insert fail'})
        except:
            self.logger.exception(u"Execute insert sql script error.")
            conn.rollback()
            return Result({u"success": False, u"errmsg": u"Execute insert sql script error"})
        finally:
            conn.close()

    def delete(self, tableName, conditions):
        """
        删除一条记录
            tableName为数据库表名
            conditions为dict结构的查询条件

        数据库连接失败时抛出异常
        """
        conn = self.connectDB()
        
        # 确保tableName编码为unicode
        if type(tableName) == type(''):
            tableName = tableName.decode('utf-8')
        # 确保key和value编码为unicode
        conditions = json.loads(json.dumps(conditions))

        # 不检查记录是否存在
        select = self.select(tableName, conditions)
        #if not select.success or len(select.record) == 0:
        #    conn.close()
        #    return Result({
        #        u"success": False,
        #        u"errmsg": u"record not found"
        #    })

        sql = u"DELETE FROM {} WHERE {};"
        conditionExpr = self._parseEquation(conditions)
        sql = sql.format(tableName, conditionExpr)
        self.logger.debug(u'delete sql: {}'.format(sql))

        cur = conn.cursor()
        try:
            cur.execute(sql)
            if cur.rowcount == 1:
                conn.commit()
                self.logger.debug("delete success.")
                return Result({u'success': True, u'record': select.record})
            else:
                conn.rollback()
                self.logger.debug("delete fail.")
                return Result({u'success': False, u'errmsg': 'delete fail'})
        except:
            self.logger.exception(u"Execute delete sql script error.")
            conn.rollback()
            return Result({u"success": False, u"errmsg": u"Execute delete sql script error"})
        finally:
            conn.close()
    
    def select(self, tableName, conditions=None, columns=None):
        """
        查询数据
            tableName为表名
            conditions为dict格式的查询条件
            columns为列表格式的查询列

        当数据库连接失败时抛出异常
        当columns为None时，从表中获取全部列名
        返回record为dict对象的列表，列名作为key，记录作为值
        """
        conn = self.connectDB()

        if columns is None:
            cur = conn.cursor()
            cur.execute(u'pragma table_info({});'.format(tableName))
            col_name = cur.fetchall()
            columns = [x[1] for x in col_name]
        # 确保tableName编码为unicode
        if type(tableName) == type(''):
            tableName = tableName.decode('utf-8')
        # 确保key和value编码为unicode
        if conditions is not None:
            conditions = json.loads(json.dumps(conditions))
        columns    = json.loads(json.dumps(columns))

        if conditions is None:
            sql = u"SELECT {} FROM {};".format(self._parseCol(columns), tableName)
        else:
            sql = u"SELECT {} FROM {} WHERE {};".format(self._parseCol(columns), tableName, self._parseEquation(conditions))
        
        self.logger.debug(u'select sql: {}'.format(sql))

        cur = conn.cursor()
        try:
            cur.execute(sql)
            records = []
            for row in cur.fetchall():
                record = {}
                for x in xrange(0, len(columns)):
                    record[columns[x]] = row[x]
                records.append(record)
            self.logger.debug("select success.")
            result = Result({u'success': True, u'record': records})
        except:
            self.logger.exception(u"Execute select sql script error.")
            result = Result({u'success': False, u'errmsg': u"Execute select sql script error"})
        finally:
            conn.close()
            return result

    def update(self, tableName, conditions, record):
        """
        更新数据
            tableName为数据库表名
            conditions为dict格式的查询条件
            record为dict格式的记录
        """
        conn = self.connectDB()
        
        if type(tableName) == type(''):
            tableName = tableName.decode('utf-8')
        # 确保key和value编码为unicode
        conditions = json.loads(json.dumps(conditions))
        record     = json.loads(json.dumps(record))

        #select = self.select(tableName, conditions)
        #if not select.success or len(select.record) == 0:
        #    conn.close()
        #    return Result({
        #        u"success": False,
        #        u"errmsg": "record not found"
        #    })
        
        conditionExpr = self._parseEquation(conditions)
        recordExpr    = self._parseEquation(record).replace(' and', ',')

        sql = u"UPDATE {} SET {} WHERE {};".format(tableName, recordExpr, conditionExpr)
        self.logger.debug(u'update sql: {}'.format(sql))
        
        cur = conn.cursor()
        try:
            cur.execute(sql)
            if cur.rowcount == 1:
                conn.commit()
                select = self.select(tableName, record)
                return Result({u'success': True, u'record': select.record[0]})
            else:
                conn.rollback()
                return Result({u'success': False, u'errmsg': u'update fail'})
        except:
            self.logger.exception(u"Execute update sql script error.")
            conn.rollback()
            return Result({u"success": False, u"errmsg": u"Execute update sql script error"})
        finally:
            conn.close()

if __name__ == "__main__":
    import json
    import os

    tmp_db = './.temp_test.xxxxxxxxx.db'
    logging.basicConfig(filename=".temp_test.xxxxxxxx.log", filemode='a', level=logging.DEBUG)

    init_script = """
    create table test (
        col1  INTEGER  NOT NULL,
        col2  TEXT     NOT NULL
    );
    insert into test
        (col1, col2)
    values
        (1, 'first');

    insert into test
        (col1, col2)
    values
        (2, 'second');

    insert into test
        (col1, col2)
    values
        (3, 'thrid');
    """
    testDB = SQLiteBase(tmp_db, init_script=init_script)

    print "Function test..."
    # insert
    ret = testDB.insert('test', {'col1': 4, 'col2': 'forth'})
    if ret.success and json.dumps(ret.record, sort_keys=True) == json.dumps({'col1': 4, 'col2': 'forth'}, sort_keys=True):
        print "\033[32mINSERT PASS\033[0m"
    else:
        print "\033[31mINSERT FAIL\033[0m"
        print "\t", ret.dump()

    # delete
    ret = testDB.delete('test', {'col1': 2})
    if ret.success and json.dumps(ret.record, sort_keys=True) == json.dumps([{'col1': 2, 'col2': 'second'}], sort_keys=True):
        print "\033[32mDELETE PASS\033[0m"
    else:
        print "\033[31mDELETE FAIL\033[0m"
        print "\t", ret.dump()
    
    ret = testDB.delete('test', {'col1': 6})
    if not ret.success and ret.errmsg == "delete fail":
        print "\033[32mDELETE PASS\033[0m"
    else:
        print "\033[31mDELETE FAIL\033[0m"
        print "\t", ret.dump()

    # select
    ret = testDB.select('test', {'col1': 1})
    if ret.success and json.dumps(ret.record, sort_keys=True) == json.dumps([{'col1': 1, 'col2': 'first'}], sort_keys=True):
        print "\033[32mSELECT PASS\033[0m"
    else:
        print "\033[31mSELECT FAIL\033[0m"
        print "\t", ret.dump()

    ret = testDB.select('test', {'col1': 6})
    if not ret.success and ret.errmsg == "select fail":
        print "\033[32mSELECT PASS\033[0m"
    else:
        print "\033[31mSELECT FAIL\033[0m"
        print "\t", ret.dump()

    # update
    ret = testDB.update('test', {'col1': 3}, {'col1': 5, 'col2': 'fifth'})
    if ret.success and json.dumps(ret.record, sort_keys=True) == json.dumps({'col1': 5, 'col2': 'fifth'}, sort_keys=True):
        print "\033[32mUPDATE PASS\033[0m"
    else:
        print "\033[31mUPDATE FAIL\033[0m"
        print "\t", ret.dump()

    ret = testDB.update('test', {'col1': 6}, {'col1': 5, 'col2': 'fifth'})
    if not ret.success and ret.errmsg == "update fail":
        print "\033[32mUPDATE PASS\033[0m"
    else:
        print "\033[31mUPDATE FAIL\033[0m"
        print "\t", ret.dump()

    # global
    conn = testDB.connectDB()
    cur = conn.cursor()
    cur.execute('SELECT * from test;')
    records = [x for x in cur]
    if json.dumps(records, sort_keys=True) == json.dumps([(1, 'first'), (5, 'fifth'), (4, 'forth')], sort_keys=True):
        print "\033[32mGLOBAL PASS\033[0m"
    else:
        print "\033[31mGLOBAL FAIL\033[0m"
        print "\t", ret.dump()
    conn.close()

    print "encode test."
    ret = testDB.insert('test', {u'col1': 8, u'col2': '第八'})
    if ret.success and json.dumps(ret.record, sort_keys=True) == json.dumps({u'col1': 8, u'col2': u'第八'}, sort_keys=True):
        print "\033[32mINSERT PASS\033[0m"
    else:
        print "\033[31mINSERT FAIL\033[0m"
        print "\t", ret.dump()

    ret = testDB.insert('test', {u'col1': 9, u'col2': u'第九'})
    if ret.success and json.dumps(ret.record, sort_keys=True) == json.dumps({u'col1': 9, u'col2': u'第九'}, sort_keys=True):
        print "\033[32mINSERT PASS\033[0m"
    else:
        print "\033[31mINSERT FAIL\033[0m"
        print "\t", ret.dump()
    
    ret = testDB.select('test', {'col2': '第九'})
    if ret.success and json.dumps(ret.record, sort_keys=True) == json.dumps([{u'col1': 9, u'col2': u'第九'}], sort_keys=True):
        print "\033[32mSELECT PASS\033[0m"
    else:
        print "\033[31mSELECT FAIL\033[0m"
        print "\t", ret.dump()
    
    ret = testDB.select('test', {u'col2': u'第八'})
    if ret.success and json.dumps(ret.record, sort_keys=True) == json.dumps([{u'col1': 8, u'col2': u'第八'}], sort_keys=True):
        print "\033[32mSELECT PASS\033[0m"
    else:
        print "\033[31mSELECT FAIL\033[0m"
        print "\t", ret.dump()

    ret = testDB.update('test', {u'col2': '第十'}, {'col1': 5, u'col2': '第八'})
    if not ret.success and ret.errmsg == "update fail":
        print "\033[32mUPDATE PASS\033[0m"
    else:
        print "\033[31mUPDATE FAIL\033[0m"
        print "\t", ret.dump()

    ret = testDB.update('test', {'col2': u'第九'}, {u'col1': 5, u'col2': u'第九'})
    if ret.success:
        print "\033[32mUPDATE PASS\033[0m"
    else:
        print "\033[31mUPDATE FAIL\033[0m"
        print "\t", ret.dump()

    ret = testDB.delete('test', {'col2': '第八'})
    if ret.success and json.dumps(ret.record, sort_keys=True) == json.dumps([{u'col1': 8, u'col2': u'第八'}], sort_keys=True):
        print "\033[32mDELETE PASS\033[0m"
    else:
        print "\033[31mDELETE FAIL\033[0m"
        print "\t", ret.dump()

    ret = testDB.delete('test', {u'col2': u'第九'})
    if ret.success and json.dumps(ret.record, sort_keys=True) == json.dumps([{u'col1': 5, u'col2': u'第九'}], sort_keys=True):
        print "\033[32mDELETE PASS\033[0m"
    else:
        print "\033[31mDELETE FAIL\033[0m"
        print "\t", ret.dump()

    os.system('rm -f {}'.format(tmp_db))
