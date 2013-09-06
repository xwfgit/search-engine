'''
Created on Feb 12, 2013

@author: xwf

Adapted from http://kunigami.wordpress.com/2012/09/25/skip-lists-in-python/
'''
from random import randint

class SkipNode:
    def __init__(self, height = 0, elem = None):
        self.elem = elem
        self.next = [None]*height
        
class SkipList:
    def __init__(self, height):
            self.head = SkipNode()
            self.height = height
        
    def randomHeight(self):
        return  randint(1, self.height)
    
    def updateList(self, elem):
        update = [None]*len(self.head.next)
        
        for i in reversed(range(len(self.head.next))):
            x = self.head
            while x.next[i] != None and x.next[i].elem < elem:
                x = x.next[i]
            update[i] = x
        return update
    
    def find(self, elem, update = None):
        if update == None:
            update = self.updateList(elem)
        if len(update) > 0:
            candidate = update[0].next[0]
            if candidate != None and candidate.elem == elem:
                return candidate
        return None
    
    def insert(self, elem):
        node = SkipNode(self.randomHeight(), elem)
        while len(self.head.next) < len(node.next):
            self.head.next.append(None)
        update = self.updateList(elem)            
        if self.find(elem, update) == None:
            for i in range(len(node.next)):
                node.next[i] = update[i].next[i]
                update[i].next[i] = node
                
    def remove(self, elem):
        update = self.updateList(elem)
        x = self.find(elem, update)
        if x != None:
            for i in reversed(range(len(x.next))):
                update[i].next[i] = x.next[i]
                if self.head.next[i] == None:
                    del self.head.next[i]
#                    self.head.next.pop()

if __name__ == '__main__':
    test = SkipList(4)
    test.insert(5)
    test.insert(3)
    test.insert(1)
    test.insert(10)
    test.insert(12)
#    for i in range(len(test.head.next)):
#        print test.head.next[i].elem
    test2 = SkipList(6)
    test2.insert(7)
    test2.insert(13)
    test2.insert(11)
    test2.insert(20)
    test2.insert(2)
    
    test3 = SkipList(6)
    test3.insert(2)
    test3.insert(132)
    test3.insert(11)
    test3.insert(12)
    test3.insert(22)
#    for i in range(len(test2.head.next)):
#        print test2.head.next[i].elem
    node1 = test.head.next[0]
    node2 = test2.head.next[0]
    if node1.elem < node2.elem:
        list1 = test
        list2 = test2
    else:
        list1 = test2
        list2 = test
#    for i in range(len(list1.head.next)):
#        print list1.head.next[i].elem  
#    for i in range(len(list2.head.next)):
#        print list2.head.next[i].elem      
    res = []
    index = 1
    while list1.head.next[0] != None and list2.head.next[0] != None:
#        elem1 = list1.head.next[0].elem
        elem2 = list2.head.next[0].elem
        update_list = list1.updateList(elem2)
        elem1 = update_list[0].elem
        if elem1 == elem2 - 1:
            res.append(elem2)
        update_list = list1.updateList(elem2)
        if elem1 == elem2:
            for i in range(len(update_list)):
                update_list[i] = update_list[i].next[i]
        node = update_list[0].next[0]
#       list1 = SkipList(len(update_list), update_list)
#        break
        for i in range(len(update_list)):
            list1.head.next[i] = update_list[i].next[i]
#            print list1.head.next[i].elem
#        break
        if list1.head.next[0] != None:
            elem1 = list1.head.next[0].elem
            update_list = list2.updateList(elem1)
            elem2 = update_list[0].next[0]
            if elem2 != None:
                elem2 = elem2.elem
                if elem1 == elem2:
                    for i in range(len(update_list)):
                        update_list[i] = update_list[i].next[i]
            for i in range(len(update_list)):
                if update_list[i] != None and update_list[i].next[i] != None:
                    list2.head.next[i] = update_list[i].next[i]
                else:
                    list2.head.next[i] = None
#        temp = list1
#        list1 = list2
#        list2 = temp
    print res
    
    test = SkipList(4)
    for i in res:
        test.insert(i)
    test2 = test3
    node1 = test.head.next[0]
    node2 = test2.head.next[0]
    list1 = test
    list2 = test2
    for i in range(len(list1.head.next)):
        print list1.head.next[i].elem  
    print 'asdf'
    for i in range(len(list2.head.next)):
        print list2.head.next[i].elem  
    res = []
    while list1.head.next[0] != None and list2.head.next[0] != None:
        #        elem1 = list1.head.next[0].elem
        elem2 = list2.head.next[0].elem
        update_list = list1.updateList(elem2)
        elem1 = update_list[0].elem
        if elem1 == elem2 - 1:
            res.append(elem2)
        update_list = list1.updateList(elem2)
        if elem1 == elem2:
            for i in range(len(update_list)):
                update_list[i] = update_list[i].next[i]
        node = update_list[0].next[0]
#       list1 = SkipList(len(update_list), update_list)
#        break
        for i in range(len(update_list)):
            list1.head.next[i] = update_list[i].next[i]
#            print list1.head.next[i].elem
#        break
        if list1.head.next[0] != None:
            elem1 = list1.head.next[0].elem
            update_list = list2.updateList(elem1)
            elem2 = update_list[0].next[0]
            if elem2 != None:
                elem2 = elem2.elem
                if elem1 == elem2:
                    for i in range(len(update_list)):
                        update_list[i] = update_list[i].next[i]
            for i in range(len(update_list)):
                if update_list[i] != None and update_list[i].next[i] != None:
                    list2.head.next[i] = update_list[i].next[i]
                else:
                    list2.head.next[i] = None
#        temp = list1
#        list1 = list2
#        list2 = temp
    print res

#        break
#        print res
    
#    res = sorted(res, key = int)
    print res
        
    
