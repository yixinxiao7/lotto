"""Class for model relations."""
# TODO: TEST THIS FUNCTIOn. MAKE TEST DIRECTORY
import random
import numpy as np


from itertools import combinations
from lotto.db import get_db
from sklearn.linear_model import LinearRegression
from lotto.api.aux.model_util import in_range, convert_model_to_coordinates, convert_coordinates_to_model


class RelationModel:

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
            self.vertical_relations[val] = {distance: 1}
        else:
            if distance not in self.vertical_relations[val]:
                self.vertical_relations[val][distance] = 1
            else:
                self.vertical_relations[val][distance] += 1

    def _get_frequency(self, prefix):
        """ Returns number of model instances of all model ranges with given prefix. """
        freq = 0
        for type_, instance in self.type_to_instance.items():
            if type_.find(prefix, 0, len(type_)):
                freq += len(self.type_to_instance[type_])
        return freq

    def _get_probs(self, num):
        """ With horizontal_relations, get all related numbers and their weighted probabilties. """
        all_related_nums = []
        freqs = []
        num_range = in_range(num)
        for r_num, freq in self.horizontal_relations[num].items():
            all_related_nums.append(r_num)
            freqs.append(freq)
        sum_ = float(sum(freqs))
        weighted_probs = [(freq/sum_) for freq in freqs]
        return all_related_nums, weighted_probs
    
    def _get_common_num(self, prev_num, range_, model, model_idx):
        """ Finds num in range which is larger than prev_num. Returns list object. """
        # get num of consecutive model range excluding first
        range_reps = 0
        while model_idx < 4:  
            if model[model_idx] == model[model_idx+1]:
                range_reps += 1
            model_idx += 1
        if prev_num in self.num_to_others_freq:
            # has related nums
            related_range_nums = []
            freqs = []
            for num, freq in self.num_to_others_freq[prev_num].items():
                if in_range(num) == range_:
                    related_range_nums.append(num)
                    freqs.append(freq)
            if not freqs:
                # no related nums within specified range_. Choose random number in specified range
                if in_range(prev_num) != range_:
                    prev_num = (range_ * 10) - 1
                return [random.choice([num for num in range(prev_num+1, ((range_*10)+10)-range_reps)])]
            sum_ = float(sum(freqs))
            weighted_probs = [(freq/sum_) for freq in freqs]
            return random.choices(related_range_nums, weights=weighted_probs, k=1)
        else:
            # grab random value larger than prev_num within range.
            # if prev_num not in range, chooses random value within range vals.
            # TODO: check if this is right
            if in_range(prev_num) != range_:
                prev_num = (range_ * 10) - 1  # increases prev_num
            return [random.choice([num for num in range(prev_num+1, ((range_*10)+10)-range_reps)])]

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
                for vals in reversed(past_nums):
                    try:
                        vals.index(num)
                    except ValueError:
                        # failed to find
                        entry_idx -= 1
                        continue
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
                                        str(in_range(entry['val1'])), str(in_range(entry['val2'])),
                                        str(in_range(entry['val3'])), str(in_range(entry['val4'])),
                                        str(in_range(entry['val5']))
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
                            self._insert_horizontal_relation(new_entry[i], new_entry[j])

            if self.vertical_relations is not None:
                if not past_nums:
                    past_nums.append(new_entry)
                else:
                    for val in new_entry:
                        # TODO: consider if val is repeated
                        distances = find_element(val)
                        for distance in distances:
                            self._insert_vertical_relation(val, distance)
                    past_nums.append(new_entry)
                    if len(past_nums) > 14:  # maintain maximum length of 14
                        past_nums.pop(0)

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

    def predict_model_char(self):
        """ With current data, make a forecase of next model characterization. Returns a string. """
        all_poss = "ABCDE"
        model = "A"
        letter_idx = 0
        while len(model) != 4:
            model += all_poss[letter_idx]
            first_poss = model
            freq1 = self._get_frequency(first_poss)
            # change char in string
            tmp = list(model)
            tmp[-1] = all_poss[letter_idx+1]
            second_poss = ''.join(tmp)
            freq2 = self._get_frequency(second_poss)
            dem = freq1 + freq2  # float
            model = random.choices([first_poss, second_poss], weights=[(freq1/float(dem)), (freq2/float(dem))], k=1)
            model = model[0]  # get string
            if model == second_poss:
                letter_idx += 1
        print('Prior model: ' + model)
        # convert model to coordinate
        pred_coord = convert_model_to_coordinates(model)
        # linear regression
        X = np.asarray(self.X)  # array of tuples
        y = np.asarray(self.y)  # array of integers
        reg = LinearRegression().fit(X, y)
        # score
        print('Lin Reg Score: '  + str(reg.score(X,y)))
        num_model = reg.predict(np.array([pred_coord]))
        pred_coord.append(num_model[0])
        # TODO: choose best model
        return convert_coordinates_to_model([int(i) for i in pred_coord])

    def predict_model(self, model_char):
        """ Converts model characterization to model. """
        prev_models = self.type_to_instance[model_char]
        return random.choice(prev_models)  # already distributed, as prev_models may have duplicates

    def predict_nums(self, model_):
        """ Converts model to values. """
        # convert
        model = model_.split(' ')
        # get first val
        first_range = int(model[0])
        total_range_freq = 0.0
        range_nums = [num for num in range(first_range*10, (first_range*10)+10)]
        range_poss_freq = [0]*10
        idx = 0
        for num in range_nums:
            # TODO: test if this is correctly 
            if num in self.first_num_freq:
                total_range_freq += self.first_num_freq[num]
                range_poss_freq[idx] = self.first_num_freq[num]
            idx += 1
        weighted_freqs = [(freq/total_range_freq) for freq in range_poss_freq]
        model_nums = random.choices(range_nums, weights=weighted_freqs, k=1)
        # get remaining vals based on horizontal and vertical relations
        prev_range = first_range
        prev_num = model_nums[0]
        curr_range_idx = 1
        
        while len(model_nums) != 5:
            curr_range = int(model[curr_range_idx])
            next_num = [-1]
            if curr_range == prev_range or curr_range == prev_range + 1:  # horizontal relation possibility. TODO: consider weighted prob for hoz
                if prev_num in self.horizontal_relations:
                    vals, weighted_probs = self._get_probs(prev_num)
                    next_num = random.choices(vals, weights=weighted_probs, k=1)
                    # only accept next_num in curr_range
                    if in_range(next_num[0]) != curr_range:  # this probability changes depending on what curr_Range is.
                        next_num = self._get_common_num(prev_num, curr_range, model, curr_range_idx)
                else:
                    next_num = self._get_common_num(prev_num, curr_range, model, curr_range_idx)
            else:  # no hoz relation
                next_num = self._get_common_num(prev_num, curr_range, model, curr_range_idx)
            model_nums += next_num
            # prepare for next iter
            prev_range = curr_range
            prev_num = next_num[0]
            curr_range_idx += 1

        return model_nums