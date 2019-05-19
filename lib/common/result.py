# -*- coding: utf-8 -*-

class Result:
    success = True # default
    errmsg = u''
    record = None

    def __init__(self, r):
        self.load(r)

    def dump(self):
        return {
            u'result': self.success,
            u'errmsg': self.errmsg,
            u'record': self.record
        }

    def load(self, r):
        self.success = r.get('success', True)
        self.errmsg  = r.get('errmsg', u'')
        self.record  = r.get('record', None)