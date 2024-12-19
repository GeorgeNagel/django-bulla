def max_length_from_choices(choices_dict):
    """
    Return the max length needed in the databse to store the given choices
    """
    max_length = 0
    for choice in choices_dict.keys():
        max_length = max(max_length, len(choice))
    return max_length
