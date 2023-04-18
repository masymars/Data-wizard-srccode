from itertools import combinations
import math
from collections import defaultdict

import numpy as np
import threading
from queue import Queue
candidates_queue = Queue()
class Apriori_reduse(object):
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
        print(dataset)
        print("/**/*/*/*//*/*/*//")
        for transaction in dataset:
            print(transaction)
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
            print(support)
            print(itemset)
            if support >= (min_support)/10:
                frequent_items.append((itemset, support))

        return frequent_items

    def calsup(self, candidate, dataset):

        item_counts = 0
        for transaction in dataset:
            if candidate.issubset(transaction):
                if item_counts == 0:
                    item_counts = 1
                else:
                    item_counts += 1

        sup = item_counts / len(dataset)

        return sup

    #########appriori##############
    def generate_candidates(self, frequent_items, k):

        candidates = set()
        num_frequent_items = len(frequent_items)
        for i in range(num_frequent_items):
            for j in range(i + 1, num_frequent_items):

                itemset1 = frequent_items[i][0]
                itemset2 = frequent_items[j][0]
                union = itemset1.union(itemset2)

                if len(union) == k + 1:
                    print("------", union)
                    candidates.add(union)
        return candidates

    def worker(self, subset, min_support,lendat):
        candidates = self.create_candidates(subset)
        itemset_counts = defaultdict(int)
        for transaction in subset:
            for candidate in candidates:
                if candidate.issubset(transaction):
                    itemset_counts[candidate] += 1
        frequent_itemsets = []
        for itemset, count in itemset_counts.items():
            support = count / len(subset)
            if support >= min_support:
                frequent_itemsets.append((itemset, support))
        candidates_queue.put(frequent_itemsets)

    def worker2(self, subset, min_support,k,lendat,dataset):
            candidates = self.generate_candidates(subset,k)
            print(candidates)
            print("////////////////////////")
            frequent_itemsets = self.support_prune(dataset,candidates,min_support)
            print(frequent_itemsets)
            candidates_queue.put(frequent_itemsets)

    def apriori_reduse(self, dataset,min_support):

        frequent_itemsets = []
        frequent_itemsets2 = []
        k = 1
        subsets = np.array_split(dataset, 10)

        threads = []
        for subset in subsets:
            t = threading.Thread(target=self.worker, args=(subset,min_support,len(dataset)))
            threads.append(t)
            t.start()

        # Wait for all threads to complete
        for t in threads:
            t.join()

        # Collect frequent itemsets from the queue
        candidates = defaultdict(int)
        while not candidates_queue.empty():
                frequent_itemsets2 += candidates_queue.get()
        for itemset, support in frequent_itemsets2:
                candidates[itemset] += support



        while candidates:
            for itemset, support in candidates.items():
                if (support/10) >= min_support :
                    frequent_itemsets.append((itemset, support/10))
            subsets1 = np.array_split(frequent_itemsets, 10)

            print(subsets1)
            for i in range(len(subsets1)):
                t = threading.Thread(target=self.worker2, args=(subsets1[i], min_support,k,len(dataset),subsets[i]))
                threads.append(t)
                t.start()

            # Wait for all threads to complete
            for t in threads:
                t.join()

            # Collect frequent itemsets from the queue
            candidates = defaultdict(int)
            frequent_itemsets2 = []
            while not candidates_queue.empty():
                frequent_itemsets2 += candidates_queue.get()
            for itemset, support in frequent_itemsets2:
                candidates[itemset] += support


            k += 1

        return frequent_itemsets


