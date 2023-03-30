from itertools import combinations
import math
from collections import defaultdict



class Apriori(object):
    def __init__(self):
        """ Parameters setting
        """
          # min support (used for mining frequent sets)




    def create_candidates(self,dataset):

        k=1
        candidates = set()
        for transaction in dataset:
            for item in transaction:
                candidates.add(frozenset([item]))
        return candidates

    def support_prune(self,dataset, candidates, min_support):

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
                frequent_items.append((itemset,support))

        return frequent_items

    def generate_candidates( self, frequent_items, k):

        candidates = set()
        num_frequent_items = len(frequent_items)
        for i in range(num_frequent_items):
            for j in range(i + 1, num_frequent_items):
                itemset1 = frequent_items[i][0]
                itemset2 = frequent_items[j][0]
                union = itemset1.union(itemset2)
                if len(union) == k + 1:
                    candidates.add(union)
        return candidates

    def apriori(self , dataset, min_support):

        frequent_itemsets = []
        k = 1


        candidates = self.create_candidates(dataset)

        while candidates:

            frequent_items = self.support_prune(dataset, candidates, min_support)
            print(frequent_items)
            frequent_itemsets.extend(frequent_items)


            candidates = self.generate_candidates(frequent_items, k)
            k += 1

        return frequent_itemsets



        
    def adaptive_support_threshold(self ,dataset,priority):
     item_counts = defaultdict(int)
     candidates = []

     for transaction in dataset:
      i=0
      for index, item in enumerate(transaction):
        candidate = frozenset([item])
        
        # Update candidates list only if the candidate is not already in it
        if candidate not in candidates:
            candidates.append([candidate,i])

        # Update item_counts
        if candidate.issubset(transaction):
            item_counts[candidate] += 1
        i=i+1     
     n = len(dataset)
     Sum = 0
     print(n)
     for d in candidates:
        S = item_counts[d[0]]
        value = priority[d[1]].replace(',', '')
        priority
        if value:
             p = S * (int(value) / math.factorial(len(priority)))
        else:
            print("Error: Empty value encountered.")
        Sum += p
     Avesup = Sum / n
     Min_threshold = Avesup / n
     print(Min_threshold)
     return Min_threshold


    def generate_rules(self , frequent_itemsets, min_confidence):
        rules = []
        num_transactions = sum([itemset[1] for itemset in frequent_itemsets])

        for itemset in frequent_itemsets:
            size = len(itemset[0])
            if size > 1:
                for i in range(1, size):
                    for antecedent in combinations(itemset[0], i):
                        antecedent = frozenset(antecedent)
                        consequent = itemset[0].difference(antecedent)
                        consequent = frozenset(consequent)

                        support_antecedent = 0
                        support_consequent = 0
                        for row in frequent_itemsets:
                            if antecedent == row[0]:
                                support_antecedent = row[1]
                            if consequent == row[0]:
                                support_consequent = row[1]

                        confidence = itemset[1] / support_antecedent
                        if confidence >= min_confidence:
                            lift = (confidence * num_transactions) / support_consequent
                            leverage = itemset[1] - (support_antecedent * support_consequent / num_transactions)

                            if confidence == 1:
                                conviction = float('inf')
                            else:
                                conviction = (1 - support_consequent / num_transactions) / (1 - confidence)

                            rules.append((antecedent, consequent, itemset[1], confidence, lift, leverage, conviction))

        return rules