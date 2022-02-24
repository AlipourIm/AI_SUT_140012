import pandas as pd
import math
import operator

def gain(data_file: pd.DataFrame, col_name, res_name):
    plural_counter = len(data_file[data_file[res_name] == 1])
    non_plural_counter = len(data_file) - plural_counter;
    entrop = calculate_B((plural_counter / (non_plural_counter + plural_counter)))
    rem = remainder(data_file, col_name, res_name)
    return calculate_B((plural_counter / (non_plural_counter + plural_counter))) - remainder(data_file, col_name, res_name), entrop, rem


def remainder(data_file: pd.DataFrame, col_name, res_name):
    plural_counter = len(data_file[data_file[res_name] == 1])
    non_plural_counter = len(data_file) - plural_counter
    all_values = data_file[col_name].unique()
    s = 0.0
    for k in all_values:
        dcol = data_file[data_file[col_name] == k]
        pk = len(dcol[dcol[res_name] == 1])
        nk = len(dcol[dcol[res_name] == 0])
        s = s + ((pk + nk) / (plural_counter + non_plural_counter) * calculate_B((pk / (pk + nk))))
    return s

def select_an_attributesibute(data_file, attributes, res_name):
    attributes_importance = {}
    entropy = {}
    remains = {}
    for tmp_attributes in attributes:
        attributes_importance[tmp_attributes], entropy[tmp_attributes], remains[tmp_attributes] = gain(data_file, tmp_attributes, res_name)
    answer = max(attributes_importance.items(), key=operator.itemgetter(1))[0]
    return answer, attributes_importance[answer], entropy[answer], remains[answer]


class decicion_tree_multi_way:
    def __init__(self, attributes, default_child=None, branches=None, entropy=None, gain_=None, remainder_=None):
        self.attributes = attributes
        self.default_child = default_child
        self.branches = branches or {}
        self.entropy = entropy
        self.gain_ = gain_
        self.remainder_ = remainder_
    def add(self, val, subtree):
        self.branches[val] = subtree
    def __call__(self, example):

        attributes_val = example[self.attributes]
        if attributes_val in self.branches:
            return self.branches[attributes_val](example)
        else:

            return self.default_child(example)
    def print_tree(self, scope=0):
        name = self.attributes
        print('Test ' + name + '?')
        for (val, subtree) in self.branches.items():
            if name == 'Patrons':
                if val == 0:
                    val = 'None'
                elif val == 1:
                    val = 'Some'
                else:
                    val = 'Full'
            elif name =='Type':
                if val == 0:
                    val = 'French'
                elif val == 1:
                    val = 'Thai'
                elif val == 2:
                    val = 'Burger'
                elif val == 3:
                    val = 'Italian'
            else:
                if val == 0:
                    val = 'No'
                else:
                    val = 'Yes'
            print(' ' * 4 * scope, 'entropy = ', str(self.entropy) + ',', name, '=', val, '--->', end=' ')
            subtree.print_tree(scope + 1)


class decicion_tree_leaf:
    def __init__(self, result, entropy=None):
        self.result = result
        self.entropy = entropy
    def __call__(self, example):
        return self.result
    def __str__(self):
        string = ' ' + str(self.result) + '\n' 
        return string
    def print_tree(self, scope=0):
        print('RESULT =', self.result)

def all_similar(data_file: pd.DataFrame):
    a = data_file.to_numpy()
    return (a[0] == a[1:]).all()

def value_node_of_plural_attributesibute(data_file: pd.DataFrame, outcome_name):
    plural_counter = len(data_file[data_file[outcome_name] == 1])
    non_plural_counter = len(data_file) - plural_counter;
    entropy = calculate_B((plural_counter / (non_plural_counter + plural_counter)))
    leaf = decicion_tree_leaf(data_file.mode()[outcome_name][0], entropy=entropy)
    return leaf

def is_plural(data_file: pd.DataFrame, outcome_name):
    return data_file.mode()[outcome_name][0]


def decicion_tree_training(examples: pd.DataFrame, attributesibutes: list, parent_examples, outcome_name, curr_depth
                         ):
    if examples.empty:
        return value_node_of_plural_attributesibute(parent_examples, outcome_name)
    if all_similar(examples[outcome_name]):
        return decicion_tree_leaf(examples[outcome_name].iloc[0], entropy=0)
    if not attributesibutes:
        return value_node_of_plural_attributesibute(examples, outcome_name)
    coloumns = list(examples.columns)
    coloumns.remove(outcome_name)
    attributes, gain_, entropy_, remains_ = select_an_attributesibute(examples, coloumns, outcome_name)
    all_values = examples[attributes].unique()
    tree = decicion_tree_multi_way(attributes, value_node_of_plural_attributesibute(examples, outcome_name), gain_=gain_, entropy=entropy_,
                        remainder_=remains_)
    for vk in all_values:
        new_coloumns = attributesibutes
        if (attributes in new_coloumns):
            new_coloumns.remove(attributes)
        subtree = decicion_tree_training(examples[examples[attributes] == vk], new_coloumns, examples, outcome_name, curr_depth + 1
                                       )
        tree.add(vk, subtree)
    return tree

def calculate_entropy(q):
    return -(q * math.log2(q))


def calculate_B(q): # according to slides
    if q == 0 or q == 1:
        return 0
    return calculate_entropy(q) + calculate_entropy(1 - q)

#############################
######## Driver Code ########
#############################
data_file = pd.read_csv('restaurants.csv')

coloumns = list(data_file.columns)
coloumns.remove('Outcome')

generated_tree = decicion_tree_training(data_file, coloumns, None, 'Outcome', 0)
generated_tree.print_tree()