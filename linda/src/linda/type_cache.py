#    Copyright 2004-2006 Andrew Wilkinson <aw@cs.york.ac.uk>
#
#    This file is part of PyLinda (http://www-users.cs.york.ac.uk/~aw/pylinda)
#
#    PyLinda is free software; you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation; either version 2.1 of the License, or
#    (at your option) any later version.
#
#    PyLinda is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with PyLinda; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from utils import Counter

from threading import Semaphore

cache_lock = Semaphore()

__cache = {}
getTypeId = Counter(start=1)

def registerType(type, pid):
    assert type.isType()

    cache_lock.acquire()
    try:
        id = getTypeId()
        __cache[id] = [type, pid, getTypeReferences(type), {}]
        return id
    finally:
        cache_lock.release()

def updateType(type_id, type):
    assert type.isType()

    cache_lock.acquire()
    try:
        __cache[type_id][0] = type
        __cache[type_id][2] = getTypeReferences(type)
    finally:
        cache_lock.release()

def emptyTypeCache():
    __cache = None

def lookupType(id):
    return __cache[id][0]

def getTypeReferences(type):
    return []

def unregisterTypesFromProcess(pid):
    garbage = []
    cache_lock.acquire()
    try:
        for tid in __cache.keys():
            if pid == __cache[tid][1]:
                clearIsos(__cache[tid][0])
                del __cache[tid]
    finally:
        cache_lock.release()

    for tid in garbage:
        doTypeGarbageCollection(tid)

#def doTypeGarbageCollection(tid):
    #cache_lock.acquire()
    #try:
        #if len(__cache[tid][1]) != 0:
            #return

        #memo = [tid]
        #pending = typeReferencedBy(tid)

    #finally:
        #cache_lock.release()

#def typeReferencedBy(tid):
    #l = []
    #for t in __cache.keys():
        #if tid in __cache[t][2]:
            #l.append(t)
    #return l

from iso_cache import clearIsos
