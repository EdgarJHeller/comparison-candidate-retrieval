import numpy as np
import matplotlib.pyplot as plt
import operator

labels = []#'motorcycle', 'cuda', 'php', 'android', 'milk', 'toyota', 'perl', 'gamecube', 'pepsi', 'potato', 'steak', 'beer', 'microsoft', 'bmw', 'golf', 'bluetooth', 'truck', 'ps2', 'python', 'coca-cola', 'apple', 'opencl', 'java', 'ios', 'tennis', 'michigan', 'ethernet', 'oregon', 'javascript']
intersections_counter = []#3, 0, 0, 1, 2, 0, 0, 0, 1, 2, 0, 3, 0, 0, 1, 0, 4, 0, 4, 0, 3, 0, 1, 0, 2, 1, 2, 0, 0]
precisions = []#0.21428571428571427, 0, 0, 0.03125, 0.11764705882352941, 0, 0, 0, 0.25, 0.2, 0.0, 0.12, 0, 0, 0.043478260869565216, 0, 0.13333333333333333, 0, 0.2, 0, 0.04838709677419355, 0, 0.045454545454545456, 0, 0.11764705882352941, 0.02564102564102564, 0.25, 0, 0]
recalls = []#0.15, 0.0, 0.0, 0.05, 0.1, 0.0, 0.0, 0.0, 0.05, 0.1, 0.0, 0.15, 0.0, 0.0, 0.05, 0.0, 0.2, 0.0, 0.2, 0.0, 0.15, 0.0, 0.05, 0.0, 0.1, 0.06666666666666667, 0.1, 0.0, 0.0]
f1scores = []#0.044117647058823525, 0, 0, 0.009615384615384616, 0.02702702702702703, 0, 0, 0, 0.020833333333333332, 0.03333333333333333, 0, 0.03333333333333333, 0, 0, 0.011627906976744186, 0, 0.04, 0, 0.05, 0, 0.018292682926829267, 0, 0.011904761904761904, 0, 0.02702702702702703, 0.009259259259259259, 0.03571428571428571, 0, 0]

#aaa = ['motorcycle', 'cuda', 'php', 'android', 'milk', 'toyota', 'perl', 'gamecube', 'pepsi', 'potato', 'steak', 'beer', 'microsoft', 'bmw', 'golf', 'bluetooth', 'truck', 'ps2', 'python', 'coca-cola', 'apple', 'opencl', 'java', 'ios', 'tennis', 'michigan', 'ethernet', 'oregon', 'javascript']
#bbb = {'motorcycle': 3, 'cuda': 0, 'php': 0, 'android': 1, 'milk': 2, 'toyota': 0, 'perl': 0, 'gamecube': 0, 'pepsi': 1, 'potato': 2, 'steak': 0, 'beer': 3, 'microsoft': 0,'bmw': 0, 'golf': 1, 'bluetooth': 0, 'truck': 4, 'ps2': 0, 'python': 4, 'coca-cola': 0, 'apple': 3, 'opencl': 0, 'java': 1, 'ios': 0, 'tennis': 2, 'michigan': 1, 'ethernet': 2, 'oregon': 0, 'javascript': 0}
#ccc = {'motorcycle': 0.21428571428571427, 'cuda': 0, 'php': 0, 'android': 0.03125, 'milk': 0.11764705882352941, 'toyota': 0, 'perl': 0, 'gamecube': 0, 'pepsi': 0.25, 'potato': 0.2, 'steak': 0.0, 'beer': 0.12, 'microsoft': 0, 'bmw': 0, 'golf': 0.043478260869565216, 'bluetooth': 0, 'truck': 0.13333333333333333, 'ps2': 0, 'python': 0.2, 'coca-cola': 0, 'apple': 0.04838709677419355, 'opencl': 0, 'java': 0.045454545454545456, 'ios': 0, 'tennis': 0.11764705882352941, 'michigan': 0.02564102564102564, 'ethernet': 0.25, 'oregon': 0, 'javascript': 0}
#ddd = {'motorcycle': 0.15, 'cuda': 0.0, 'php': 0.0, 'android': 0.05, 'milk': 0.1, 'toyota': 0.0, 'perl': 0.0, 'gamecube': 0.0, 'pepsi': 0.05, 'potato': 0.1, 'steak': 0.0, 'beer': 0.15, 'microsoft': 0.0, 'bmw': 0.0, 'golf': 0.05, 'bluetooth': 0.0, 'truck': 0.2, 'ps2': 0.0, 'python': 0.2, 'coca-cola': 0.0, 'apple': 0.15, 'opencl': 0.0, 'java': 0.05, 'ios': 0.0, 'tennis': 0.1, 'michigan': 0.06666666666666667, 'ethernet': 0.1, 'oregon': 0.0, 'javascript': 0.0}
#eee = {'motorcycle': 0.044117647058823525, 'cuda': 0, 'php': 0, 'android': 0.009615384615384616, 'milk': 0.02702702702702703, 'toyota': 0, 'perl': 0, 'gamecube': 0, 'pepsi': 0.020833333333333332, 'potato': 0.03333333333333333, 'steak': 0, 'beer': 0.03333333333333333, 'microsoft': 0, 'bmw': 0, 'golf': 0.011627906976744186, 'bluetooth': 0,'truck': 0.04, 'ps2': 0, 'python': 0.05, 'coca-cola': 0, 'apple': 0.018292682926829267, 'opencl': 0, 'java': 0.011904761904761904, 'ios': 0, 'tennis': 0.02702702702702703, 'michigan': 0.009259259259259259, 'ethernet': 0.03571428571428571, 'oregon': 0, 'javascript': 0}



def draw_scatter(comparison_objects, intersections_dict, precisions_dict, recalls_dict, f1_dict):

    intersections_counter = []
    precisions = []
    recalls = []
    f1scores = []
    x_axis = []
    i = -0.5

    # sort intersections_dict by value
    sorted_intersections_dict = dict(sorted(intersections_dict.items(), key=operator.itemgetter(1)))
    # get labels in same order as sorted_intersections_dict
    for key in sorted_intersections_dict.keys():
        labels.append(key)

    for co in labels:
        intersections_counter.append(intersections_dict[co])
        precisions.append(precisions_dict[co])
        recalls.append(recalls_dict[co])
        f1scores.append(f1_dict[co])
        x_axis.append(i + 1)
        i += 1

    fig, ax1 = plt.subplots()

    color = 'tab:red'
    plt.xticks(x_axis, labels, rotation='vertical')
    ax1.set_xlabel('comparison objects')
    ax1.set_ylabel('size of intersection of ggl- and ccr-suggestions: i', color=color)
    ax1.scatter(x_axis, intersections_counter, color=color, marker=r"$i$") 
    ax1.tick_params(axis='y', labelcolor=color)
    plt.yticks([1, 2, 3, 4])

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('precisions: p; recalls: r; f1scores: f', color=color)  # we already handled the x-label with ax1
    ax2.scatter(x_axis, precisions, color=color, marker=r"$p$")
    ax2.tick_params(axis='y', labelcolor=color)

    color = 'tab:cyan'
    ax2.scatter(x_axis, recalls, color=color, marker=r"$r$")

    color = 'tab:green'
    ax2.scatter(x_axis, f1scores, color=color, marker=r"$f$")

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()


#draw_scatter(aaa,bbb,ccc,ddd,eee)

