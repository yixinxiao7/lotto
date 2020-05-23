"""Util functions for model relations."""
# uncomment if there are issues
# import flask
# import lotto

# TODO: TEST THIS FUNCTIOn. MAKE TEST DIRECTORY
from itertools import combinations
from lotto.db import get_db
from lotto.api.aux.model import in_range, convert_model_to_coordinates


class RelationGenerator:

    def __init__(
                 self,
                 type_to_instance=None,
                 firstnumrange_to_num=None,
                 horizontal_relations=None,
                 vertical_relations=None,
                 first_num_freq=None,
                 num_to_others_freq=None
                ):
        self.type_to_instance = type_to_instance
        self.firstnumrange_to_num = firstnumrange_to_num
        self.horizontal_relations = horizontal_relations
        self.vertical_relations = vertical_relations
        self.first_num_freq = first_num_freq
        self.num_to_others_freq = num_to_others_freq
        self.X = []
        self.y = []

    def _insert_horizontal_relation(self, val1, val2):
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

    def _insert_vertical_relation(self, val, distance):
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
        More info in _insert_horizontal_relation.
        Key->integer, val->{integer: integer}

        vertical_relations: dictionary of num to dictionary of distance to frequency.
        More info in _insert_vertical_relation.
        Key->integer, val->{integer: integer}

        first_num_freq: dictionary of first num to its frequency as the first number in an entry.
        Key->integer, val-> integer

        num_to_others_freq: dictionary of num to dictionary of another num to frequency.
        More info: captures relationship of how nums appear with each other in an entry.
        Key->integer, val->{integer: integer}
        """
        db = get_db()
        cursor = db.cursor()
        all_entries = cursor.execute("SELECT * FROM combinations").fetchall()
        past_nums = []

        if self.vertical_relations is not None:
            def find_element(num):
                distances = []
                entry_idx = -1
                for vals in reversed(num):
                    if vals.find(num) != -1:
                        distances.append(entry_idx * -1)
                    entry_idx -= 1
                return distances

        for entry in all_entries:
            model = entry['model']
            coordinates = convert_model_to_coordinates(tuple(model))
            self.X.append(coordinates[:4])  # tuple
            self.y.append(coordinates[-1])  # number

            new_entry = [entry['val1'], entry['val2'], entry['val3'], entry['val4'], entry['val5']]

            if self.type_to_instance is not None:
                str_sequence = ' '.join([
                                        str(entry['val1']), str(entry['val2']),
                                        str(entry['val3']), str(entry['val4']),
                                        str(entry['val5'])
                                        ])
                if model not in self.type_to_instance:
                    self.type_to_instance[model] = [str_sequence]
                else:
                    self.type_to_instance[model].append(str_sequence)

            if self.firstnumrange_to_num is not None:
                range_num = in_range(entry['val1'])
                if range_num not in self.firstnumrange_to_num:
                    self.firstnumrange_to_num[range_num] = [entry['val1']]
                else:
                    self.firstnumrange_to_num[range_num].append(entry['val1'])

            if self.horizontal_relations is not None:
                for i in range(len(new_entry) - 1):
                    for j in range(i+1, len(new_entry)):
                        # difference  >= 0
                        if new_entry[j] - new_entry[i] <= 3:
                            self._insert_horizontal_relation(new_entry[j], new_entry[i])

            if self.vertical_relations is not None:
                if not past_nums:
                    past_nums.append(new_entry)
                else:
                    for val in new_entry:
                        # TODO: consider if val is repeated
                        distances = find_element(val)
                        for distance in distances:
                            self._insert_vertical_relation(val, distance)
                    past_num.append(new_entry)
                    if len(past_num) > 14:  # maintain maximum length of 14
                        past_num.pop(0)

            if self.first_num_freq is not None:
                first_val = entry['val1']
                if first_val not in self.first_num_freq:
                    self.first_num_freq[first_val] = 1
                else:
                    self.first_num_freq[first_val] += 1

            if self.num_to_others_freq is not None:
                for i in range(len(new_entry) - 1):
                    if new_entry[i] not in self.num_to_others_freq:
                        self.num_to_others_freq[new_entry[i]] = {}  # key -> num, val-> freq
                    for j in range(i+1, len(new_entry)):
                        if new_entry[j] not in self.num_to_others_freq[new_entry[i]]:
                            self.num_to_others_freq[new_entry[i]][new_entry[j]] = 1
                        else:
                            self.num_to_others_freq[new_entry[i]][new_entry[j]] += 1

    def get_frequency(self, prefix):
        """
        Returns number of model instances of all model ranges with given prefix.
        """
        freq = 0
        for type_, instance in self.type_to_instance.items():
            if type_.find(prefix, 0, len(type_)):
                freq += len(self.type_to_instance[type_])
        return freq
