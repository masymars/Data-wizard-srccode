from itertools import combinations
import math
from collections import defaultdict


class Close(object):
    def __init__(self):
        """ Parameters setting
        """
        # min support (used for mining frequent sets)

    def create_candidates(self, dataset):

        k = 1
        candidates = set()
        for transaction in dataset:
            for item in transaction:
                candidates.add(frozenset([item]))
        return candidates

    def support_prune(self, dataset, candidates, min_support):

        item_counts = {}
        for transaction in dataset:
            for candidate in candidates:
                if candidate.issubset(transaction):

                    if candidate not in item_counts:
                        item_counts[candidate] = 1
                    else:
                        item_counts[candidate] += 1

        num_transactions = len(dataset)
        frequent_items = []
        for itemset, count in item_counts.items():
            support = count / num_transactions
            if support >= min_support:
                frequent_items.append((itemset, support))

        return frequent_items

    def support_prune2(self, dataset, candidates, min_support):

        item_counts = {}
        for transaction in dataset:
            for candidate in candidates:
                if candidate.issubset(transaction):
                    candidate_frozen = frozenset(candidate)
                    if candidate_frozen not in item_counts:
                        item_counts[candidate_frozen] = 1
                    else:
                        item_counts[candidate_frozen] += 1

        num_transactions = len(dataset)
        frequent_items = []
        for itemset, count in item_counts.items():
            support = count / num_transactions
            if support >= min_support:
                frequent_items.append((itemset, support))

        return frequent_items


    def get_items_in_all_rows(self,list):
        first_row_set = set(list[0])

        for row in list[1:]:
            for item in first_row_set:
                if item not in row:
                    first_row_set.remove(item)
                    break

        return first_row_set
    def calculate_closure(self, itemset, dataset):

        rows = []

        for row in dataset:


            if itemset.issubset(set(row)):

                    rows.append(row)

        closers = self.get_items_in_all_rows(rows)
        return  closers
    #######closed########
    def generate_candidates2(self, frequent_items, k):

        candidates = set()

        num_frequent_items = len(frequent_items)
        for i in range(num_frequent_items):
            for j in range(i + 1, num_frequent_items):
                itemset1 = frequent_items[i][0]
                itemset2 = frequent_items[j][0]
                union = itemset1.union(itemset2)
                if len(union) == k + 1 :
                    candidates.add(union)

        return candidates

    def check_if_frozensets_have_same_items(self,frozenset1, frozenset2):


        if len(frozenset1) != len(frozenset2):
            return False


        for item in frozenset1:
            if item not in frozenset2:
                return False

        return True

    def Close(self, dataset, min_support):

        frequent_itemsets = []
        k = 1
        
        Closers = []
        candidates = self.create_candidates(dataset)

        rulsgen = []
        while candidates:
            frequent_candidates = self.support_prune(dataset, candidates, min_support)
            frequent_candidatess = []
            for S in frequent_candidates:
                cls= self.calculate_closure(S[0], dataset)
                Closers.append(cls)
                S = (S[0],S[1],cls)
                frequent_candidatess.append(S)
            frequent_itemsets.extend(frequent_candidatess)

            candidates_t = self.generate_candidates2(frequent_candidates, k)
            k += 1
            candidates = set()
            for cand in candidates_t:
                for close in Closers:

                   if not self.check_if_frozensets_have_same_items(cand, frozenset(close)):

                       candidates.add(cand)
                   else:
                       print(close)
                       print(cand)
        t = self.support_prune2(dataset, Closers, 0)               
        closerss=[]
        closerss.extend(t)

        return frequent_itemsets,closerss
