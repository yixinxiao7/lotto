"""Util functions for model relations."""
# uncomment if there are issues
# import flask
# import lotto

# TODO: TEST THIS FUNCTIOn. MAKE TEST DIRECTORY
from itertools import combinations
from lotto.db import get_db
from lotto.api.aux.model import in_range


class RelationGenerator:

    def __init__(self, type_to_instance=None, firstnumrange_to_num=None, horizontal_relations=None):
        self.type_to_instance = type_to_instance
        self.firstnumrange_to_num = firstnumrange_to_num
        self.horizontal_relations = horizontal_relations

    def insert_horizonal_relation(self, val1, val2):
        """
        Each val1 maps to val2, which is either 1, 2, or 3 greater than val1.
        Each of these three possible entries for val2 has a corresponding frequency.
        """
        if val1 not in self.horizontal_relations:
            horizontal_relations[val1] = {val2: 1}
        else:
            if val2 not in horizontal_relations[val1]:
                horizontal_relations[val1][val2] = 1
            else:
                horizontal_relations[val1][val2] += 1

    def get_relations(self):
        """
        type_to_instance: dictionary of model to sequence instances.
        Key->str, val->[strings...]

        firstnumrange_to_num: dictionary of number range to number for first value
        Key->integer, val->[integers...]

        horizontal_relations: dictionary of num to dictionary of number to frequency
        Key->integer, val->{integer: integer}
        """
        db = get_db()
        cursor = db.cursor()
        all_entries = cursor.execute("SELECT * FROM combinations").fetchall()
        
        for entry in all_entries:
            if type_to_instance is not None:
                str_sequence = ' '.join([entry.val1, entry.val2, entry.val3, entry.val4, entry.val5])
                if entry.model not in type_to_instance:
                    type_to_instance[type_to_instance] = [str_sequence]
                else:
                    type_to_instance[type_to_instance].append(str_sequence)
            if firstnumrange_to_num is not None:
                range_num = in_range(entry.val1)
                if range_num not in firstnumrange_to_num:
                    firstnumrange_to_num[range_num] = [entry.val1]
                else:
                    firstnumrange_to_num[range_num].append(entry.val1)
            if horizontal_relations is not None:
                vals = [entry.val1, entry.val2, entry.val3, entry.val4, entry.val5]
                for i in range(len(vals) - 1):
                    for j in range(i+1, len(vals)):
                        # difference  >= 0
                        if vals[j] - vals[i] <= 3:
                            self.insert_horizonal_relation(vals[j], vals[i])
            
        
