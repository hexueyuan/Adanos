# -*- coding: utf-8 -*-

import json

class Datapool:
    def __init__(self):
        self._pool = {}

    def _include(self, target, conditions):
        for key in conditions.keys():
            if not target.has_key(key) or target[key] != conditions[key]:
                return False
        return True

    def insert(self, namespace, record):
        if type(record) != dict:
            raise TypeError("invalid record type: {}".format(str(type(record))))

        if not self._pool.has_key(namespace):
            self._pool[namespace] = []

        self._pool[namespace].append(record)
        return record

    def delete(self, namespace, conditions):
        if type(conditions) != dict:
            raise TypeError("invalid conditions type: {}".format(str(type(conditions))))

        if not self._pool.has_key(namespace):
            return None
        
        _targetsIndex = []
        _targets = []
        for x in xrange(0, len(self._pool[namespace])):
            if self._include(self._pool[namespace][x], conditions):
                _targets.append(self._pool[namespace][x])
                _targetsIndex.append(x)

        for i in _targetsIndex:
            del self._pool[namespace][i]
        
        return _targets

    def select(self, namespace, conditions):
        if type(conditions) != dict:
            raise TypeError("invalid conditions type: {}".format(str(type(conditions))))

        if not self._pool.has_key(namespace):
            return None
        
        _targets = []
        for x in xrange(0, len(self._pool[namespace])):
            if self._include(self._pool[namespace][x], conditions):
                _targets.append(self._pool[namespace][x])

        return _targets

    def update(self, namespace, conditions, record):
        if type(conditions) != dict:
            raise TypeError("invalid conditions type: {}".format(str(type(conditions))))

        if not self._pool.has_key(namespace):
            return None

        _targets = []
        for x in xrange(0, len(self._pool[namespace])):
            if self._include(self._pool[namespace][x], conditions):
                _targets.append(self._pool[namespace][x])
                self._pool[namespace][x] = record
        
        return _targets

    def writeTo(self, path):
        with open(path, 'w') as f:
            f.write(json.dumps(self._pool, indent=2))

    def readFrom(self, path):
        with open(path, 'r') as f:
            self._pool.update(json.load(f))


if __name__ == "__main__":
    """Test"""
    db = Datapool()
    # readFrom
    initData = {
        'test_namespace1': [
            {
                "name": "vic",
                "age": 22
            },
            {
                "name": "kk",
                "age": 22
            },
            {
                "name": "lei",
                "age": 22
            },
            {
                "name": "ss",
                "age": 24
            },
            {
                "name": "jok",
                "age": 23
            }
        ],
        "test_namespace2": [
            {
                "name": "tom",
                "age": 22
            }
        ]
    }
    with open('.test.db', 'w') as f:
        f.write(json.dumps(initData, indent=2))
    
    db.readFrom('.test.db')
    import os
    os.system('rm -f ./.test.db')
    print db._pool

    # insert
    print "insert"
    print db.insert('test_namespace3', {'name': "li", "age": 21})
    print db.insert('test_namespace3', {'name': "zhang", "age": 21})
    print db.insert('test_namespace2', {'name': 'jack', "age": 23})

    # delete
    print "delete"
    print db.delete('test_namespace1', {'name': 'vic'})
    print db.delete('test_namespace4', {'test': 'test'})
    print db.delete('test_namespace1', {'name': 'hu'})

    # select
    print "select"
    print db.select('test_namespace1', {'age': 22})
    print db.select('test_namespace4', {'test': 'test'})
    print db.select('test_namespace1', {'name': 'hu'})

    # update
    print "update"
    print db.update('test_namespace2', {'name': 'tom'}, {'name': 'tom', 'age': 24})
    print db.update('test_namespace4', {'test': 'test'}, {'test': 'new_test'})
    print db.update('test_namespace1', {'name': 'liu'}, {'name': 'liu', 'age': 28})

    # writeTo
    db.writeTo('.test2.db')