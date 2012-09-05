##
##
##
import time
import uuid
import socket

class Ynode:
    def __init__(self, **kw):
        self.dirty = True
        self.Create(kw)
    def isStored(self, dirty=True):
        if self.dirty != dirty:
            self.dirty = dirty
        return self.dirty
    def __setif(self,kw,key,default):
        if kw.has_key(key):
            setattr(self,key,kw[key])
        else:
            setattr(self,key,default)
    def __getif(self, kw, key, mndt_set=None,default=None):
        if mndt_set:
            kw[key] = mndt_set
            return
        try:
            kw[key] = getattr(self, key)
        except:
            kw[key] = default
    def Create(self, kw):
        self.__setif(kw,"_id", "%s@%s"%(str(uuid.uuid4()),socket.gethostname()))
        self.__setif(kw,"name",self._id)
        self.__setif(kw,"type","object/generic")
        self.__setif(kw,"ftix",[])
        self.__setif(kw,"data",None)
        self.__setif(kw,"links",{})
        self.__setif(kw,"created",time.time())
        self.__setif(kw,"updated",time.time())
        self.__setif(kw,"owner","nobody")
        self.__setif(kw,"acl",{"access":["*"],"modify":["*"],"delete":["*"]})
    def Export(self):
        kw = {}
        self.__getif(kw,"_id")
        self.__getif(kw,"name")
        self.__getif(kw,"type")
        self.__getif(kw,"ftix")
        self.__getif(kw,"data")
        self.__getif(kw,"links")
        self.__getif(kw,"created")
        self.__getif(kw,"updated")
        self.__getif(kw,"owner")
        self.__getif(kw,"acl")
        return kw
    def Link(self, obj, lname="link", probability=100):
        k = "%s:%d"%(lname, probability)
        if not self.links.has_key(k):
            self.links[k] = {}
        if obj._id not in self.links[k]:
            self.links[k][obj.name]=obj._id
        self.isStored(True)
    def __add__(self, obj):
        self.Link(obj, "link", 100)
        return self
    def Unlink(self, obj, lname, probability):
        k = "%s:%d"%(lname, probability)
        if self.links.has_key(k):
            try:
                del self.linksp[k][obj.name]
            except:
                pass
            self.isStored(True)
    def __sub__(self, obj):
        self.Unlink(obj, "link", 100)
        return self
    def Links(self, lname="link", probability=100):
        k = "%s:%d"%(lname, probability)
        if self.links.has_key(k):
            return self.links[k].values()


if __name__ == "__main__":
    n = Ynode()
    print n.Export()
    n2 = Ynode()
    n3 = Ynode()
    n = n + n2
    n = n + n3
    print n.Links("link")
    
    
        
