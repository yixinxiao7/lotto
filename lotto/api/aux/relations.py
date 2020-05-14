"""Util functions for model relations."""
# uncomment if there are issues
# import flask
# import lotto

# TODO: TEST THIS FUNCTIOn. MAKE TEST DIRECTORY
from itertools import combinations
from lotto.db import get_db
from lotto.api.aux.model import in_range


class RelationGenerator:

    def __init__(self, type_to_instance=None, firstnumrange_to_num=None, horizontal_relations=None, vertical_relations=None):
        self.type_to_instance = type_to_instance
        self.firstnumrange_to_num = firstnumrange_to_num
        self.horizontal_relations = horizontal_relations
        self.vertical_relations = vertical_relations

    def insert_horizontal_relation(self, val1, val2):
        """
        Each val1 maps to val2, which is either 1, 2, or 3 greater than val1.
        Each of these three possible entries for val2 has a corresponding frequency.
        """
        if val1 not in self.horizontal_relations:
            self.horizontal_relations[val1] = {val2: 1}
        else:
            if val2 not in self.horizontal_relations[val1]:
                self.horizontal_relations[val1][val2] = 1
            else:
                self.horizontal_relations[val1][val2] += 1

    def insert_vertical_relation(self, val, distance):
        """
        Each val maps to a distance val. i.e. a distance of 1 means the val occurred in
        consecutive order, so 0 entries away from a prior occurrence. a distance of 2 means 
        the val occurred 1 entry away. The distance maps to a frequency
        """
        if val not in self.vertical_relations:
            self.vertical_relations[val1] = {distance: 1}
        else:
            if distance not in self.vertical_relations[val]:
                self.vertical_relations[val][distance] = 1
            else:
                self.vertical_relations[val][distance] += 1

    def get_relations(self):
        """
        type_to_instance: dictionary of model to sequence instances.
        Key->str, val->[strings...]

        firstnumrange_to_num: dictionary of num range to num for first value.
        Key->integer, val->[integers...]

        horizontal_relations: dictionary of num to dictionary of another num to frequency.
        More info in insert_horizontal_relation.
        Key->integer, val->{integer: integer}

        vertical_relations: dictionary of num to dictionary of distance to frequency.
        More info in insert_vertical_relation.
        Key->integer, val->{integer: integer}
        """
        db = get_db()
        cursor = db.cursor()
        all_entries = cursor.execute("SELECT * FROM combinations").fetchall()
        past_nums = []

        if vertical_relations is not None:
            def find_element(num):
                distances = []
                entry_idx = -1
                for vals in reversed(num):
                    if vals.find(num) != -1:
                        distances.append(entry_idx * -1)
                    entry_idx -= 1
                return distances

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
                            self.insert_horizontal_relation(vals[j], vals[i])
            if vertical_relations is not None:
                new_entry = [entry.val1, entry.val2, entry.val3, entry.val4, entry.val5]
                if not past_nums:
                    past_nums.append(new_entry)
                else:
                    for val in new_entry:
                        # TODO: consider if val is repeated
                        distances = find_element(val)
                        for distance in distances:
                            self.insert_vertical_relation(val, distance)
                    past_num.append(new_entry)
                    if len(past_num) > 14:  # maintain maximum length of 14
                        past_num.pop(0)
