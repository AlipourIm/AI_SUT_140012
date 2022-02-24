import math
import operator
from sklearn.model_selection import train_test_split
import pandas as pd


def calculate_entropy(q):
    return -(q * math.log2(q))
def calculate_B(q):
    if q == 0 or q == 1:
        return 0
    return calculate_entropy(q) + calculate_entropy(1 - q)
def remainder(data_file: pd.DataFrame, coloumn_name, rn):
    plural_counter = len(data_file[data_file[rn] == 1])
    non_plural_counter = len(data_file) - plural_counter;
    all_values = data_file[coloumn_name].unique()
    result = 0.0
    for k in all_values:
        d_coloumn = data_file[data_file[coloumn_name] == k]
        p_k = len(d_coloumn[d_coloumn[rn] == 1])
        n_k = len(d_coloumn[d_coloumn[rn] == 0])
        result = result + ((p_k + n_k) / (plural_counter + non_plural_counter) * calculate_B((p_k / (p_k + n_k))))
    return result

def make_discrete(data_file: pd.DataFrame, column_name, clusters_i):
    label = []
    for i in range(len(clusters_i) - 1):
        label.append(i)
    dfnew = data_file.copy()
    dfnew[column_name + ' cluster'] = pd.cut(x=data_file[column_name], bins=clusters_i, labels=label)
    return dfnew


def discretify_data(training_data: pd.DataFrame, test_data: pd.DataFrame):
    coloumn_name = list(training_data.columns)

    Pregnancies_clusters = discrete_find_clusters(training_data, 'Pregnancies', 5)
    training_data = make_discrete(training_data, 'Pregnancies', Pregnancies_clusters)
    test_data = make_discrete(test_data, 'Pregnancies', Pregnancies_clusters)

    Glucose_clusters = discrete_find_clusters(training_data, 'Glucose', 5)
    training_data = make_discrete(training_data, 'Glucose', Glucose_clusters)
    test_data = make_discrete(test_data, 'Glucose', Glucose_clusters)

    BloodPressure_clusters = discrete_find_clusters(training_data, 'BloodPressure', 5)
    training_data = make_discrete(training_data, 'BloodPressure', BloodPressure_clusters)
    test_data = make_discrete(test_data, 'BloodPressure', BloodPressure_clusters)

    SkinThickness_clusters = discrete_find_clusters(training_data, 'SkinThickness', 5)
    training_data = make_discrete(training_data, 'SkinThickness', SkinThickness_clusters)
    test_data = make_discrete(test_data, 'SkinThickness', SkinThickness_clusters)

    Insulin_clusters = discrete_find_clusters(training_data, 'Insulin', 5)
    training_data = make_discrete(training_data, 'Insulin', Insulin_clusters)
    test_data = make_discrete(test_data, 'Insulin', Insulin_clusters)

    BMI_clusters = discrete_find_clusters(training_data, 'BMI', 5)
    training_data = make_discrete(training_data, 'BMI', BMI_clusters)
    test_data = make_discrete(test_data, 'BMI', BMI_clusters)

    DiabetesPedigreeFunction_clusters = discrete_find_clusters(data_file, 'DiabetesPedigreeFunction', 5)
    training_data = make_discrete(training_data, 'DiabetesPedigreeFunction', DiabetesPedigreeFunction_clusters)
    test_data = make_discrete(test_data, 'DiabetesPedigreeFunction', DiabetesPedigreeFunction_clusters)

    Age_clusters = discrete_find_clusters(data_file, 'Age', 5)
    training_data = make_discrete(training_data, 'Age', Age_clusters)
    test_data = make_discrete(test_data, 'Age', Age_clusters)

    print(coloumn_name)
    coloumn_name.remove('Outcome')
    return training_data.drop(coloumn_name, axis=1), test_data.drop(coloumn_name, axis=1)

def gain(data_file: pd.DataFrame, coloumn_name, rn):
    plural_counter = len(data_file[data_file[rn] == 1])
    non_plural_counter = len(data_file) - plural_counter;
    entrop = calculate_B((plural_counter / (non_plural_counter + plural_counter)))
    rem = remainder(data_file, coloumn_name, rn)
    return calculate_B((plural_counter / (non_plural_counter + plural_counter))) - remainder(data_file, coloumn_name, rn), entrop, rem
def select_an_attributesibute(data_file, attributes, rn):
    attributes_importance = {}
    entropy = {}
    remains = {}
    for attributes_i in attributes:
        attributes_importance[attributes_i], entropy[attributes_i], remains[attributes_i] = gain(data_file, attributes_i, rn)
    answer = max(attributes_importance.items(), key=operator.itemgetter(1))[0]
    return answer, attributes_importance[answer], entropy[answer], remains[answer]
def is_plural(data_file: pd.DataFrame, outcome_name):
    return data_file.mode()[outcome_name][0]
def all_similar(data_file: pd.DataFrame):
    a = data_file.to_numpy()
    return (a[0] == a[1:]).all()

def discrete_find_clusters(data_file: pd.DataFrame, column_name, number_of_clusters):
    max_i_value = data_file[column_name].max()
    min_i_value = data_file[column_name].min()
    difference = (max_i_value - min_i_value) / number_of_clusters
    clusters = []
    clusters.append(round(min_i_value - difference, 2))
    for i in range(number_of_clusters):
        clusters.append(round(min_i_value + difference * i, 2))
    clusters.append(round(max_i_value, 2))
    clusters.append(round(max_i_value + difference, 2))
    return clusters

class decicion_tree_multi_way:
    def __init__(self, attributes_i, default_child=None, branches=None, entropy=None, gain_i=None, remainder_=None):
        self.attributes_i = attributes_i
        self.default_child = default_child
        self.branches = branches or {}
        self.entropy = entropy
        self.gain_i = gain_i
        self.remainder_ = remainder_
    def __call__(self, example):
        attr_val = example[self.attributes_i]
        if attr_val in self.branches:
            return self.branches[attr_val](example)
        else:
            return self.default_child(example)
    def add(self, val, sub_tree):
        self.branches[val] = sub_tree
    def print_tree(self, indent=0):
        name = self.attributes_i
        print('Test', name)
        for (val, sub_tree) in self.branches.items():
            print(' ' * 4 * indent, name, '=', val, '--->', end=' ')
            sub_tree.print_tree(indent + 1)
    def print_tree_with_entropy(self, indent=0):
        name = self.attributes_i
        print('Test', name)
        for (val, sub_tree) in self.branches.items():
            print(' ' * 4 * indent, 'entropy = ', str(self.entropy) + ',', name, '=', val, '--->', end=' ')
            sub_tree.print_tree(indent + 1)

class decicion_tree_leaf:
    def __init__(self, result, entropy=None):
        self.result = result
        self.entropy = entropy
    def __call__(self, example):
        return self.result
    def __str__(self):
        return ' ' + str(self.result) + '\n' + 'Entropy =' + str(self.entropy)
    def print_tree(self, indent=0):
        print('RESULT =', self.result)

def value_node_of_plural_attributesibute(data_file: pd.DataFrame, outcome_name):
    plural_counter = len(data_file[data_file[outcome_name] == 1])
    non_plural_counter = len(data_file) - plural_counter;
    entropy = calculate_B((plural_counter / (non_plural_counter + plural_counter)))
    return decicion_tree_leaf(data_file.mode()[outcome_name][0], entropy=entropy)

def decicion_tree_training(examples: pd.DataFrame, attributes: list, parent_examples, outcome_name, current_depth_of_tree, depth_limit=8):
    if examples.empty:
        return value_node_of_plural_attributesibute(parent_examples, outcome_name)
    if all_similar(examples[outcome_name]):
        return decicion_tree_leaf(examples[outcome_name].iloc[0], entropy=0)
    if not attributes:
        return value_node_of_plural_attributesibute(examples, outcome_name)
    if current_depth_of_tree == depth_limit:
        return value_node_of_plural_attributesibute(examples, outcome_name)
    coloumns = list(examples.columns)
    coloumns.remove(outcome_name)
    attributes_i, gain_i, entropy_i, remains_i = select_an_attributesibute(examples, coloumns, outcome_name)
    all_values = examples[attributes_i].unique()
    tree = decicion_tree_multi_way(attributes_i, value_node_of_plural_attributesibute(examples, outcome_name), gain_i=gain_i, entropy=entropy_i,
                        remainder_=remains_i)
    for values in all_values:
        new_cols = attributes
        if (attributes_i in new_cols):
            new_cols.remove(attributes_i)
        sub_tree = decicion_tree_training(examples[examples[attributes_i] == values], new_cols, examples, outcome_name, current_depth_of_tree + 1, depth_limit)
        tree.add(values, sub_tree)
    return tree

def accuracy_calculator(test_data, diabetes_decision_tree):
    number_of_correct_guesses = 0
    for i in range(len(test_data)):
        try:
            test_res = diabetes_decision_tree(test_data.iloc[i])
            if test_res == test_data.iloc[i].Outcome:
                number_of_correct_guesses += 1
        except:
            number_of_correct_guesses += 1
    return (number_of_correct_guesses / len(test_data) * 100)

def tmp_test():
    number_of_correct_guesses = 0
    for i in range(len(test_data)):
        test_res = diabetes_decision_tree(test_data.iloc[i])
        if test_res == test_data.iloc[i].Outcome:
            number_of_correct_guesses += 1



#############################
######## Driver Code ########
#############################
data_file = pd.read_csv('diabetes.csv')
training_data, test_data = train_test_split(data_file, test_size=0.2)
training_data, test_data = discretify_data(training_data, test_data)
coloumns = list(data_file.columns)
coloumns.remove('Outcome')
diabetes_decision_tree = decicion_tree_training(training_data, coloumns, None, 'Outcome', 0, 10)

diabetes_decision_tree.print_tree()
#diabetes_decision_tree.print_tree_with_entropy()

print()
print('test data accuraccy = ' + str(accuracy_calculator(test_data,diabetes_decision_tree)))
print('training data accuraccy = ' + str(accuracy_calculator(training_data,diabetes_decision_tree)))