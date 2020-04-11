class cuser:
    def __init__(self,id,name,uname,biladdr,shipaddr,cart):
        self.id = id
        self.name = name
        self.uname = uname
        self.biladdr = biladdr
        self.shipaddr = shipaddr
        self.cart = cart

    def getID(self):
        return self.id

    def getName(self):
        return self.name

    def getUname(self):
        return self.uname

    def getBA(self):
        return self.biladdr

    def getSA(self):
        return self.shipaddr

    def getCart(self):
        return self.cart
