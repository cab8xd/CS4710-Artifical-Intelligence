##Base Negotiator Class
##Base Methods and Fields needed
##To further develop the Negotiator
import random
class BaseNegotiator:

    # Constructor - Note that you can add other fields here; the only
    # required fields are self.preferences and self.offer
    def __init__(self):
        self.preferences = {}
        self.offer = []
        self.iter_limit = 0

    # initialize(self : BaseNegotiator, preferences : list(String), iter_limit : Int)
        # Performs per-round initialization - takes in a list of items, ordered by the item's
        # preferability for this negotiator
        # You can do other work here, but still need to store the preferences 
    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        self.iter_limit = iter_limit

    # make_offer(self : BaseNegotiator, offer : list(String)) --> list(String)
        # Given the opposing negotiator's last offer (represented as an ordered list), 
        # return a new offer. If you wish to accept an offer & end negotiations, return the same offer
        # Note: Store a copy of whatever offer you make in self.offer at the end of this method.
    def make_offer(self, offer):
        pass

    # utility(self : BaseNegotiator) --> Float
        # Return the utility given by the last offer - Do not modify this method.
    def utility(self):
        total = 0
        for s in self.offer:
            total += self.preferences.get(s,0)
        return total

    # receive_utility(self : BaseNegotiator, utility : Float)
        # Store the utility the other negotiator received from their last offer
    def receive_utility(self, utility):
        pass

    # receive_results(self : BaseNegotiator, results : (Boolean, Float, Float, count))
        # Store the results of the last series of negotiation (points won, success, etc.)
    def receive_results(self, results):
        pass

    # set_diff(self: BaseNegotiator)
        ##Returns the set difference of the current offer and the total list of items
    def set_diff(self):
        diff = (self.preferences.keys())
        return [aa for aa in diff if aa not in self.offer]

    # added methods start here...
    # Accepts an offer.
    def acceptOffer(self):
        # Very important - we save the offer we're going to return as self.offer
        # print (negotiatorName +  " agrees that you can take " + str(self.offer))
        # print(self.preferences)
        self.offer = BaseNegotiator.set_diff(self)
        # print (negotiatorName + " will take: " + str(self.offer))
        return self.offer
 
    # Returns int value of given offer list or dict
    def getValue(self, input):
        if(type(input) == dict): # get sum of utility in a dict
            return BaseNegotiator.getValueD(self, input)
        elif(type(input) == list): # get sum of utility in a given list of keys (i.e. an offer)
            return BaseNegotiator.getValueL(self, input)
        else:
            return -1 # can't identify value

    # Returns total value of dict
    def getValueD(self, input):
        ret = 0
        for v in input.values():
            ret = ret + v
        return ret

    # Returns total values of inputted list of keys
    def getValueL(self, input):
        ret = 0
        for k in input:
            ret = ret + self.preferences.get(k) 
        return ret

    def printOfferValue(self, offer):
            s = ""
            for k in offer:
                s = s + str(self.preferences.get(k)) + " "
            s = s.replace(" ", " + ", s.count(" ")-1)
            s = s + "= " + str(BaseNegotiator.getValueL(self, offer))
            # print("total offer value is " + s)

    def printPrefValue(self,preferences):
            s = ""
            for v in preferences.values():
                s = s + str(v) + " "
            s = s.replace(" ", " + ", s.count(" ")-1)
            s = s + "= " + str(BaseNegotiator.getValueD(self, preferences))
            # print("total preference value is " + s)

    def randomizeKeys(self):
            # generating randomly ordered list of keys
            ordering = self.preferences
            randomKeys = list(ordering.keys())
            # print("RANDOMIZING KEYS")
            # print(str(randomKeys))
            random.shuffle(randomKeys)
            # print(str(randomKeys))
            return randomKeys
