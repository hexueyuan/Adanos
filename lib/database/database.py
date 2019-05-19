# -*- coding: utf-8 -*-
#!/usr/bin/env python2

class RelationalDatabaseInterface:
    name    = u"RelationalDatabaseInterface"

    def __init__(self):
        """
        """
        pass

    def connectDB(self):
        """
        """
        raise Exception("This method was not implemented")

    def closeDB(self):
        """
        """
        raise Exception("This method was not implemented")

    def initDB(self, script):
        """
        """ 
        raise Exception("This method was not implemented")

    def clearDB(self, script):
        """
        """
        raise Exception("This method was not implemented")

    def insert(self, tableName, record):
        """
        """
        raise Exception("This method was not implemented")

    def delete(self, tableName, conditions):
        """
        """
        raise Exception("This method was not implemented")

    def select(self, tableName, conditions, columns):
        """
        """
        raise Exception("This method was not implemented")

    def update(self, tableName, conditions, record):
        """
        """
        raise Exception("This method was not implemented")
