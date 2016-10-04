# Pairs class is to create set of two pairs to be used in the preferances learning algorithm
from random import randint

class Pairs:
    
    def __init__(self):
        self.index_a = []
        self.index_b = []
        self.index_not = []             # index of pairs not to use 
        self.index_train = []
        self.index_sub = []
        self.BASE_SIZE = 53                             # amount of items that will be compared
        self.TOTAL_COM = self.BASE_SIZE*self.BASE_SIZE            # total amount of comparisions possible, including with each other, is pizza_index square
        # if pizza_index is 53 the max is 2809
        self.LIMIT = 2756                               # amount of maxium pairs possible, not including with each other pizza_index square - pizza_index
        self.USER_COM = 55                              # total amount of comparisons users will make
        # if pizza_index is 53 the max is 2756
        self.TRAING_SET = 30            # set the size of pizza training set for the ML training
        self.train_start = 0            # start point of training set
        self.train_end = 0              # end point of training set
        self.TRAIN_SUB = 10             # set the size of a sub set that will be used for more consitancy
        self.train_sub_start = 0        # start point of sub training set
        self.train_sub_end = 0          # end point of sub training set
        self.rounds = 0                 # set the number of rounds to be compared
        self.rounds_coms = []           # number of comparisions per round
        
    def set_num_rounds(self, i):
        # cap the size of the comparisions
        if i > self.LIMIT:
            i == self.LIMIT
        self.rounds = i
    
    def set_com_rounds(self, comparisions):
        i = 0
        for rnd in comparisions:
            # cap the size of rounds
            if rnd > self.LIMIT/self.rounds:
                self.rounds_coms.append(self.LIMIT/self.rounds)
            else: self.rounds_coms.append(rnd)
            i = i +1
            
    def set_start(self, i, start, limit_end):
        # sets start points
        if i < start:
            i = start
            
        if i > limit_end:
            end = i/limit_end
            if end < start: return start
            else: return end
        else: return i
    
    def set_end(self,start, limit, curr_end):
        # make sub sets are within the index set
        if curr_end > limit:
            if start > self.train_start:
                extra = curr_end - limit
                return self.train_start + extra
            return curr_end - limit
        else:
            return curr_end

    def set_train(self, i):
        # choose training set by splitting the index at point a point
        self.train_start = self.set_start(i, 0, self.BASE_SIZE)
        self.train_end = self.set_end(self.train_start,self.BASE_SIZE, self.train_start + self.TRAING_SET)
        return self.train_start

    def set_sub(self,i):
        # choose sub set from training set

        # find good start
        if self.train_start > self.train_end:
            self.train_sub_start = self.set_start(i, self.train_start, self.BASE_SIZE)
            self.train_sub_end = self.set_end(self.train_sub_start, self.BASE_SIZE, self.train_sub_start + self.TRAIN_SUB)
        else:
            self.train_sub_start = self.set_start(i, self.train_start, self.train_end)
            self.train_sub_end = self.set_end(self.train_sub_start, self.train_end, self.train_sub_start + self.TRAIN_SUB)

        
        return self.train_sub_start
    
        
    def contains_item(self, item, index, start):
        if len(index) < start: return False
        else:
            for i in range(start, len(index)):
                if item == i: return True
        return False
        
    def random_start(self, start, end):
        # creates a random starting point for making pairs
        return randint(start, end)
        
    
    def add_to_index(self, start, end, size, limit, comparisions, boo):
        # populate the global index with items
        index_start = self.random_start(0, size) # finds an index in the size of the training/sub set
        
        items_mixed =[]
        items_com = []
        
        for i in range(size):
            # checking everythin is in range
            if self.train_start > self.train_end:
                if start > end:
                    if start + i + index_start > self.BASE_SIZE:
                        # the middle tricky bit
                        excess = (i + index_start+start)
                        if excess - self.BASE_SIZE -1 > end:
                            excess = ((i + index_start+start)- self.BASE_SIZE -1)-end
                            items_mixed.append(start + excess)
                        else:
                            items_mixed.append(((i + index_start+start)- self.BASE_SIZE)+ start - 1)
                    else:
                        items_mixed.append(start + i + index_start)
                else:
                    if start + i + index_start > self.BASE_SIZE:
                        # the middle tricky bit
                        if (i + index_start+start)- self.BASE_SIZE -1 > end:
                            excess = ((i + index_start+start)- self.BASE_SIZE -1)-end
                            items_mixed.append(start + excess)
                        else:
                            items_mixed.append(((i + index_start+start)- self.BASE_SIZE)+ end - 1)
                    elif start + i + index_start > end:
                        items_mixed.append(((i + index_start+start)-limit)+ end)
                    else:
                        items_mixed.append(start + i + index_start)
            else:
                if start > end:
                    if start + i + index_start > self.BASE_SIZE:
                        items_mixed.append(((i + index_start+start)- self.BASE_SIZE)+ end)
                    elif start + i + index_start > limit:
                        # the middle tricky bit
                        excess = ((i + index_start + start)- limit)
                        if excess + self.train_start >= end:
                            excess = (excess + self.train_start) - end
                            items_mixed.append(start + excess -1)
                        else: items_mixed.append(excess + self.train_start)
                    else:
                        items_mixed.append(start + i + index_start)
                else:
                    if start + i + index_start > self.BASE_SIZE:
                        items_mixed.append(((i + index_start+start)- self.BASE_SIZE)+ end)
                    elif start + i + index_start > end:
                        items_mixed.append(((i + index_start+start-1)-end)+ start)
                    else:
                        items_mixed.append(start + i + index_start)
        
        # create a list the size of the comparisions needed from mixed list                
        for i in range(0,comparisions):
            if len(items_mixed) > i: items_com.append(items_mixed[i])
            else:
                num = randint(0, len(items_mixed)-1)
                items_com.append(items_mixed[num])
                
        # check if a or b
        if boo == True:
            for item in items_com:
                self.index_a.append(item)
        else:
            for item in items_com:
            
                # make sure they don't match

                if self.index_a[len(self.index_b)] and self.index_a[len(self.index_b)] == item:
                    # add new value if they match
                    new = item + 1
                    if new > limit: self.index_b.append(new - 2)
                    elif new > self.BASE_SIZE: self.index_b.append(new - 2)
                    else: self.index_b.append(new)
                else:
                    self.index_b.append(item)
                        

    def set_pairs(self, r, list_of_com_per_rnd):
        # create pairings for sub set with each other
        self.set_num_rounds(r)
        self.set_com_rounds(list_of_com_per_rnd)
        rnd = 0
        for comparisions in self.rounds_coms:
            # for all rounds with less than 10 use the sub set
            if rnd < 1:
                # set a random range
                # add sub to index a
                self.add_to_index(self.train_sub_start, self.train_sub_end, self.TRAIN_SUB, self.train_end, comparisions, True)
                # add train to index b
                self.add_to_index(self.train_sub_start, self.train_sub_end, self.TRAIN_SUB, self.train_end, comparisions, False)
                

            elif rnd < 3:
                # add train to index a
                self.add_to_index(self.train_start, self.train_end, self.TRAING_SET, self.BASE_SIZE, comparisions, True)
                
                if rnd == 1:
                    # add train to index b
                    self.add_to_index(self.train_start, self.train_end, self.TRAING_SET, self.BASE_SIZE, comparisions, False)
                else:
                    # add sub to index b
                    self.add_to_index(self.train_sub_start, self.train_sub_end, self.TRAIN_SUB, self.train_end, comparisions, False)
            else:
                # add train to index a
                self.add_to_index(self.train_start, self.train_end, self.TRAING_SET, self.BASE_SIZE, comparisions, True)
                # add train to index b
                self.add_to_index(self.train_start, self.train_end, self.TRAING_SET, self.BASE_SIZE, comparisions, False)
            rnd = rnd+1
    
    def get_index_of_pair(self, left_pair, right_pair):
        # calculating the position a pair is in an index of pairs
        no_of_items_in_index = self.BASE_SIZE
        return (((left_pair * no_of_items_in_index) - no_of_items_in_index)) + right_pair
        
    def get_pairs(self, index_of_pair):
        # returns a pair from the index of all possible pairs in the set
        no_of_items_in_index = self.BASE_SIZE

        # roughly where the pair are in the index
        print 'index_of_pair: ', index_of_pair, ' / no_of_items_in_index: ', no_of_items_in_index, ' = '
        starting_point_of_pair_set_in_index = index_of_pair / no_of_items_in_index
        print 'starting_point_of_pair_set_in_index: ', starting_point_of_pair_set_in_index
        
        right_pair = index_of_pair - starting_point_of_pair_set_in_index * no_of_items_in_index
        print  'no_of_items_in_index: ', no_of_items_in_index, ' * starting_point_of_pair_set_in_index: ', starting_point_of_pair_set_in_index, '- index_of_pair', index_of_pair, '= right_pair ', right_pair
        
        if right_pair == no_of_items_in_index: left_pair = starting_point_of_pair_set_in_index
        else: left_pair = starting_point_of_pair_set_in_index + 1
        
        return left_pair, right_pair
        
    def contains_pair(self, poss_index_of_pair):
        index_size= self.TOTAL_COM
        if poss_index_of_pair > index_size: return False
        else:        return True

    
        
        

pair = Pairs()
print pair.set_train(50), ' Train to ', pair.train_end
print pair.set_sub(28), ' Sub to ', pair.train_sub_end
comparisions = []
comparisions.append(10)
comparisions.append(15)
comparisions.append(15)
comparisions.append(20)
pair.set_pairs(4,comparisions)
print pair.index_a, len(pair.index_a)
print pair.index_b, len(pair.index_b)

dict_comparisions = { }

print '-------------- Find index of pairs --------------------------'
for i in range(len(pair.index_a)):
    pairs = pair.get_index_of_pair(pair.index_a[i], pair.index_b[i])
if pa
        print pairs, 'this set of pairs are the same: ', ' index_a[i] is ', pair.index_a[i], ' index_b[i] is ', pair.index_b[i]
        dict_comparisions[pairs] = -1
    else:t
        if not dict_comparisions[pairs]:
            print 'these pairs already exist ', pairs
        else:
            dict_comparisions[pairs] = 0
            print pairs, 'good pairs: ', ' index_a[i] is ', pair.index_a[i], ' index_b[i] is ', pair.index_b[i]
            
            print '-------------- Validate index of pairs --------------------------'
            print pair.get_pairs(pairs), ' do these match these ', 'index_a[i] is ', pair.index_a[i], ' index_b[i] is ', pair.index_b[i]


print '----------------------------------------'