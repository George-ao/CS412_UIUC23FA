
def ord_prefixspan(filename, minsup):
    freq_sequences = {} # default initialization
    database = create_database(filename)
    prefixspan_helper(database, minsup, '', freq_sequences)
    # a dictionary which will have keys as frequent patterns and values as the support of thosepatterns. The dictionary may look like:{a : 4, ab : 4, ...}
    return freq_sequences

# create a database from the input file
def create_database(filename):
    sequences_dict = {}
    with open(filename, 'r') as input:
        for line in input.readlines():
            # Split the line by comma and strip whitespace or newline characters
            id, sequence = line.strip().split(', ')
            # Remove the angle brackets from the sequence
            sequence = sequence.strip('<>')
            # Add to the dictionary, with sid as the key and the sequence as the value
            sequences_dict[id] = sequence
    return sequences_dict

# helper recursive function 
def prefixspan_helper(database, minsup, prefix, freq_sequences):

    # get dictionary of frequent items
    frequent_dict, new_database = get_frequent_dict(database, minsup)   
    # check if frequent_dict is empty
    if not frequent_dict:
        return freq_sequences
    # recurse down
    for each_prefix in frequent_dict.keys():
        new_prefix = prefix + each_prefix
        freq_sequences[new_prefix] = frequent_dict[each_prefix]
        # create projection database
        projection_database = get_projection_database(new_database, each_prefix)
        prefixspan_helper(projection_database, minsup, new_prefix, freq_sequences)
    return freq_sequences

# helper function to get projection database
def get_projection_database(database, prefix):
    projection_database = {}
    for key, value in database.items():
        if prefix in value:
            index = value.index(prefix)
            projection_database[key] = value[index + 1:]
    return projection_database


# helper function to get frequent items and create new database
def get_frequent_dict(database, minsup):
    frequent_dict = {}
    infrequncy_dict = {}
    # new_database = {}
    for sequence in database.values():
        cur_frequent_dict = {}
        for item in sequence:
            if item in cur_frequent_dict:
                cur_frequent_dict[item] += 1
            else:
                cur_frequent_dict[item] = 1
        # if the letter exist in cur_frequent_dict, add 1 to frequent_dict
        for add_to_freq in cur_frequent_dict.keys():
            if add_to_freq in frequent_dict:
                frequent_dict[add_to_freq] += 1
            else:
                frequent_dict[add_to_freq] = 1
    # remove item below minsup
    for item in list(frequent_dict.keys()):
        if frequent_dict[item] < minsup:
            # add to infrequent dictionary
            infrequncy_dict[item] = frequent_dict[item]
            del frequent_dict[item]
    # create new database
    new_database = create_new_database(database, frequent_dict, minsup)
    return frequent_dict, new_database

def create_new_database(database, frequent_dict, minsup):
    new_database = {}
    # return if the database is empty or frequent_dict is empty
    if not database or not frequent_dict:
        return new_database
    for key, value in database.items():
        new_value = ''
        for char in value:
            if frequent_dict.get(char, 0) >= minsup:
                new_value += char  
            new_database[key] = new_value
    return new_database

# if __name__ == "__main__":
#     file = 'C:\\Users\\ayy13\\OneDrive - International Campus, Zhejiang University\\文档\\大学\\2023fall\\CS412\\CS412_hw5\\input.txt'
#     ord_prefixspan(file, 2)
