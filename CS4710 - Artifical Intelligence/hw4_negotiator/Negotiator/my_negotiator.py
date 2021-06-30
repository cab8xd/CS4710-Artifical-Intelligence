from negotiator_base import BaseNegotiator
from random import random
import math

# Example negotiator implementation, which randomly chooses to accept
# an offer or return with a randomized counteroffer.
# Important things to note: We always set self.offer to be equal to whatever
# we eventually pick as our offer. This is necessary for utility computation.
# Second, note that we ensure that we never accept an offer of "None".
class MyNegotiator(BaseNegotiator):

   round_count = 0
   sortedPrefs = []
   totalUtil = 0

    # Override the make_offer method from BaseNegotiator to accept a given offer 20%
    # of the time, and return a random subset the rest of the time.
   def make_offer(self, offer):

        # Nested functions
        # Returns a target utility value that the negotiator later uses
        # to assess and create offers. 
        # The target value decreases towards 50% of the total possible utility as more rounds pass. 
        def get_target():
            # print("GETTING TARGET...")

            ordering = dict(MyNegotiator.sortedPrefs)
            rounds_remaining = self.iter_limit - MyNegotiator.round_count

            # Calculates no. of iterations. TODO
            count = rounds_remaining

            # Conditional to prevent out of indexing--though this shouldn't happen anyway. I am caütious.
            if count > len(ordering):
                count = len(ordering)

            values = list(ordering.values())

            # print("count is " + str(rounds_remaining) + " - " + "(" + str(rounds_remaining) + "-" + str(len(ordering)) + ") = " + str(count))

            # I guess this could also be floored, but I decided to keep the bot a -little- ambitious.
            ret = math.ceil(MyNegotiator.totalUtil * .5)

             # Calculating target as 
             # fifty percent + the utility of lowest items; 
             #  the number of lowest items is deduced by how many rounds are left.
             # ex. if there are 0 rounds left, the target will be 50% of the max util. 
             #  Similarly, if there are n rounds left, the target will be 50% + the total util of about
             #  n of the lowest util items with some exception.
            for n in range(count):
                i = len(values) - (n + 1)

                # To prevent the target value of going over the total possible util 
                # (plus some cushioning for more flexible negotiating)
                if(ret + values[i] >= math.floor(MyNegotiator.totalUtil * .75)):
                   # print("too much!.")
                    break

                else:
                    ret = ret + values[i]
                   # print("value is " + str(values[i]))
                   # print("new ret is " + str(ret + values[i]))


            # print("TARGET IS " + str(ret) + ", and the max util is " + str(MyNegotiator.totalUtil))

            return ret

        # Returns value of the offer. 
        def get_value_of_offer(offer):
            ret = 0
            for item in offer:
                ret = ret + self.preferences[item]
            return ret

        # Creates an offer.
        def compile_offer(ordering, target, offer):
            ourOffer = []
            for item in ordering.keys():
                if get_value_of_offer(ourOffer) >= target:
                    break
                # Has randomness in case the other negotiator has the similar preferences and is stubborn.
                if random() > .5: 
                   ourOffer = ourOffer + [item]

            return ourOffer

        # Iterates what round the negotiator is currently at
        MyNegotiator.round_count = MyNegotiator.round_count + 1

        # print()
        # print("--Turn: " + str(MyNegotiator.round_count) + " / " + str(self.iter_limit) + "--")

        # Setting up some field variables if this our first turn.
        if(MyNegotiator.round_count == 1):

            # set an ordered dict of valued items.
            MyNegotiator.sortedPrefs = dict(sorted(self.preferences.items(),key=lambda x: -x[1]))

            # calc. total util. score
            for item in dict(MyNegotiator.sortedPrefs).keys(): # ...not sure why i need to convert again but it is what is working. 
               # print(str(item) + " : " + str(MyNegotiator.sortedPrefs[item]))
               MyNegotiator.totalUtil = MyNegotiator.totalUtil + MyNegotiator.sortedPrefs[item]


        # Assessing the offer...
        self.offer = offer
        target = get_target()

        # if(offer is not None):
            # print("Their OFFER GIVES us " + str(MyNegotiator.totalUtil - get_value_of_offer(self.offer)) + " and them " + str(get_value_of_offer(self.offer)))

        # Accepts offer if it exists and either...
        #   1) It's the final round.
        #   2) The utility we receive in the offer is greater or equal to our current target.
        if offer is not None and (MyNegotiator.totalUtil - get_value_of_offer(self.offer) >= target or MyNegotiator.round_count == self.iter_limit):
            # Very important - we save the offer we're going to return as self.offer
            print ("I agree that you can take " + str(self.offer))
            self.offer = BaseNegotiator.set_diff(self)
            print ("I will take: " + str(self.offer))
            return self.offer

        else: # Create an offer
            ourOffer = compile_offer(MyNegotiator.sortedPrefs, target, offer)

            # Reassures that our offer will always be >= to the target. 
            while get_value_of_offer(ourOffer) < target:
                ourOffer = compile_offer(MyNegotiator.sortedPrefs, target, offer)
            self.offer = ourOffer

            # print("We OFFER " + str(get_value_of_offer(self.offer)))

            return self.offer

       
