
from negotiator_base import BaseNegotiator
from random import random
import math
import random

class GreaterThanHalfNegotiator(BaseNegotiator):
    # Override the make_offer method from BaseNegotiator to accept a given offer 20%
    # of the time, and return a random subset the rest of the time.
   def make_offer(self, offer):
        self.offer = offer

        # printing the given offer and thsi negotiator's preferenceds
        if offer is not None: 
            BaseNegotiator.printOfferValue(self, offer)

        BaseNegotiator.printPrefValue(self, self.preferences)

        prefVal  = BaseNegotiator.getValue(self, self.preferences)
        theirOfferVal = BaseNegotiator.getValue(self, self.offer)
        print(type(self.offer))
        # accepting offer if offer is...
        #   * not none
        #   * greater than or equal to our total pref utility value / 2
        if theirOfferVal >= prefVal/2 and offer is not None:
            # print("*ACCEPTING OFFER*")
            return BaseNegotiator.acceptOffer(self, "MyNegotiator") 
        
        # making new offer that...
        #   * proposes a RANDOM set of items with values 
        #       summing to greater than our total pref utility value / 2.
        #       alternative: summing to greater than the util val of the other negotiator
        else:
            # print("*PROPOSING NEW OFFER*")
            ourOffer = []

            # randomizing a keys list
            randomKeys = BaseNegotiator.randomizeKeys(self)

            # looping through items in dict
            for item in randomKeys:
                ourOffer = ourOffer + [item]
                if(BaseNegotiator.getValue(self, ourOffer) > prefVal / 2): 
                    break 
            self.offer = ourOffer
            BaseNegotiator.printOfferValue(self,self.offer)
            return self.offer



class GreaterThanHalfNegotiatorV2(BaseNegotiator):
    # Override the make_offer method from BaseNegotiator to accept a given offer 20%
    # of the time, and return a random subset the rest of the time.
   def make_offer(self, offer):
        self.offer = offer

        # printing the given offer and thsi negotiator's preferenceds
        if offer is not None: 
            BaseNegotiator.printOfferValue(self, offer)

        BaseNegotiator.printPrefValue(self, self.preferences)

        prefVal  = BaseNegotiator.getValue(self, self.preferences)
        theirOfferVal = BaseNegotiator.getValue(self, self.offer)

        # accepting offer if offer is...
        #   * not none
        #   * greater than or equal to our total pref utility value / 2
        if theirOfferVal >= prefVal/2 and offer is not None:
            # print("*ACCEPTING OFFER*")
            return BaseNegotiator.acceptOffer(self, "MyNegotiator") 
        
        # making new offer that...
        #   * proposes a RANDOM set of items with values 
        #       summing to greater than or equal to our total pref utility value / 2.
        else:
            # print("*PROPOSING NEW OFFER*")
            ourOffer = []

            # randomizing a keys list
            randomKeys = BaseNegotiator.randomizeKeys(self)

            # looping through items in dict
            for item in randomKeys:
                ourOffer = ourOffer + [item]
                if(BaseNegotiator.getValue(self, ourOffer) >= prefVal / 2): 
                    break 
            self.offer = ourOffer
            return self.offer