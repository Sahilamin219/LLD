"""
Entities
Coustomare
    - Dirver, User
Locker 
    - generateToken
    - openCompartements
Compartements
    - state occupied, empty
    - type small, medium, large

Package 
    - S,M,L
 

Config
1 to 1 ( locker vs package)

Flow/Behavour
Driver -> Small Package -> Small Compartements -> Locker -> Token vs Compartement
User -> code/token -> Locker -> Compartements -> Package -> Avaialable Compartements
Action
1.Drive-> Size
2.Locker -> compartementID 
         -> Error
        2.1 Packager <-> compartementID
"""
import random
import datetime
class Compartement:
    def __init__(self, size, occupied = False):
        self.size = size
        self.occupied = occupied
        self.__token = None
        self.expiredDate = ""
    
    def setToken(self, token):
        self.__token = token
        self.expiredDate = datetime.datetime.now(delta=7)
    def getToken(self):
        return self.__token
    
    def deleteToken(self):
        self.__token = None
        self.expiredDate = ""
        self.occupied = False
        

class Locker:
    def __init__(self, small, medium, large):
        self.small = small
        self.medium = medium
        self.large = large
        self.Compartements = {}
        self.Compartements['small'] = [ Compartement('small') for _ in small ]
        self.Compartements['medium']   = [ Compartement('medium') for _ in medium ]
        self.Compartements['large'] = [ Compartement('large') for _ in large ]
    
    def insertPackage(self, size):
        for compartement in self.Compartements[size]:
            if not compartement.occupied:
                compartement.occupied = True
                print( f"Compartement with {compartement.size} is got occupied successfully" )
                self.generateToken(compartement)
                return
        print( f"Compartement with {size} is not available" )

    def generateToken(self, compartement):
        print( f"Token for {compartement.size} is generated" )
        compartement.setToken(random.randint(1,100000))

    def openCompartements(self, token):
        allSizes = ['small', 'medium', 'large']
        for compartement in self.Compartements[allSizes]:
            if compartement.occupied and compartement.getToken() == token and compartement.expiredDate > datetime.datetime.now():
                print( f"Compartement with {compartement.size} is opened successfully" )
                compartement.deleteToken()
                return
            elif compartement.occupied and compartement.getToken() == token and compartement.expiredDate > datetime.datetime.now():
                print( f"Compartement with {compartement.size} is expired" )
        print( f"Code did not Mactched with {token}" )

    def cleanExpiredComp(self):
        allSizes = ['small', 'medium', 'large']
        for compartement in self.Compartements[allSizes]:
            if compartement.occupied and compartement.expiredDate < datetime.datetime.now():
                print( f"Compartement with {compartement.size} is cleaned successfully" )
                compartement.deleteToken()
        print('Clean up Done')
    


