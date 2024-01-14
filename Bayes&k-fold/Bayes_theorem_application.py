import math
import numpy as np

def my_Bayes_candy(pi_list, p_list, c_list):
    posterior_probabilities = [[0] * 5 for _ in range(10)]  # Default initialization with 0s

    #draw one candy each loop
    for candy_index in range(1, len(c_list)+1):
        candy_sequence = c_list[0:candy_index]
        joint_probabilities = []
        for i in range(5):
            joint_probabilities.append(pi_list[i])
        for candy in candy_sequence:
            for i in range(5):
                if candy == 0:
                    joint_probabilities[i] = p_list[i] * joint_probabilities[i]
                if candy == 1:
                    joint_probabilities[i] = (1-p_list[i]) * joint_probabilities[i]
        total = sum(joint_probabilities)
        #update
        for i in range(5):
            posterior_probabilities[candy_index-1][i] = joint_probabilities[i] / total
    return posterior_probabilities

