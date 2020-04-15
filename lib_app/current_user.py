class cuser:
    def __init__(self,id,name,uname,biladdr,shipaddr,checkout):
        self.id = id
        self.name = name
        self.uname = uname
        self.biladdr = biladdr
        self.shipaddr = shipaddr
        self.checkout = checkout

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

    def setBA(self, BA):
        self.biladdr = BA

    def setSA(self, SA):
        self.shipaddr = SA

    def getCheck(self):
        return self.checkout['books']

    def setCheckout(self, books):
        inCheck = False
        if(not books):
            self.checkout = None
        else:
            for index in enumerate(self.checkout['books']):
                try:
                    if(self.checkout['books'][books['bk_name'][0]]):
                        if(index == len(self.checkout['books'])):
                            inCheck = True
                except KeyError:
                    inCheck = True

            if(inCheck or not self.checkout['books'] ):
                #print(books['bk_name'])
                self.checkout['books'].update({books['bk_name'][0] : books['bk_price'][0]})
                print(str(books['bk_name'][0]) + " added to cart")
            else:
                print("Book is already in your cart!")

    def newUser(self,id,name,uname,biladdr,shipaddr,checkout):
        self.id = id
        self.name = name
        self.uname = uname
        self.biladdr = biladdr
        self.shipaddr = shipaddr
        self.checkout = checkout
