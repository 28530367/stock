from django.test import TestCase

# Create your tests here.

def flatten_dict_to_list(data, parent_key=None):
    result = []
    for key, value in data.items():
        current_key = key if parent_key is None else f"{key}"
        if isinstance(value, dict):
            result.extend(flatten_dict_to_list(value, current_key))
        elif isinstance(value, list):
            for item in value:
                result.append([current_key, item[0], parent_key, item[1]])
    return result

data = {
    "long_short_signal": {
        "long": {
            "one_signal": {
                "bar": [["2023-09-21", 361.6]],
                "resistance": [["2023-10-09", 362.95]],
                "neckline": [["2023-09-14", 377.27], ["2023-11-06", 369.21]]
            },
            "two_signal": {
                "bar": [["2023-09-21", 361.6]],
                "resistance": [["2023-10-09", 362.95]]
            },
            "three_signal": {},
            "four_signal": {
                "bar": [["2023-09-21", 361.6]],
                "resistance": [["2023-10-09", 362.95]]
            }
        }
    }
}

result = flatten_dict_to_list(data['long_short_signal']['long'])
print(result)
