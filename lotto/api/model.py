"""Util functions."""


def conv_to_nums(str_list):
    """Convert list of strs to list of ints."""
    num_list = []
    for str_ in str_list:
        num_list.append(int(str_))
    return num_list


def in_range(num):
    """Helper function for convert_to_model."""
    if num in range(0, 10):
        return 0
    elif num in range(10, 20):
        return 1
    elif num in range(20, 30):
        return 2
    elif num in range(30, 40):
        return 3
    elif num in range(40, 50):
        return 4
    elif num in range(50, 60):
        return 5
    elif num in range(60, 70):
        return 6
    else:
        raise Exception

def convert_to_ranges(num_list):
    """Return a string of the ranges."""
    output = ''
    for num in num_list:
        print(num)
        output += str(in_range(num))
    return output


def convert_to_model(num_list):
    """Converts input to model."""
    model_vals = ['A','B','C','D','E','F']
    val_ptr = 0
    model_output = ''
    range_ = [0, 10]

    first_val = True
    for num in num_list:
        if first_val:
            model_output += model_vals[0]
            first_val = False
            prev_val = num
        else:
            if num in range(range_[0], range_[1]) or in_range(num) == in_range(prev_val):
                model_output += model_vals[val_ptr]
                prev_val = num
            else:  # make updates
                try:
                    curr_range_idx = in_range(range_[0])
                    new_range_idx = in_range(num)
                except Exception:
                    print("Error: value out of range")
                    return
                diff_range = (new_range_idx - curr_range_idx) * 10
                range_[0] += diff_range
                range_[1] += diff_range
                val_ptr += 1
                prev_val = num
                model_output += model_vals[val_ptr]
    return model_output
