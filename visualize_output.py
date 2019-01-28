import numpy as np
import matplotlib.pyplot as plt


def draw_scatter(comparison_objects, intersections_dict, precisions_dict, recalls_dict, f1_dict):

    labels = []
    intersections_counter = []#3, 0, 0, 1, 2, 0, 0, 0, 1, 2, 0, 3, 0, 0, 1, 0, 4, 0, 4, 0, 3, 0, 1, 0, 2, 1, 2, 0, 0]
    precisions = []#0.21428571428571427, 0, 0, 0.03125, 0.11764705882352941, 0, 0, 0, 0.25, 0.2, 0.0, 0.12, 0, 0, 0.043478260869565216,0, 0.13333333333333333, 0, 0.2, 0, 0.04838709677419355, 0, 0.045454545454545456, 0, 0.11764705882352941, 0.02564102564102564, 0.25, 0, 0]
    recalls = []#0.15, 0.0, 0.0, 0.05, 0.1, 0.0, 0.0, 0.0, 0.05, 0.1, 0.0, 0.15, 0.0, 0.0, 0.05, 0.0, 0.2, 0.0, 0.2, 0.0, 0.15, 0.0,0.05, 0.0, 0.1, 0.06666666666666667, 0.1, 0.0, 0.0]
    f1scores =[]#0.044117647058823525, 0, 0, 0.009615384615384616, 0.02702702702702703, 0, 0, 0, 0.020833333333333332, 0.03333333333333333, 0, 0.03333333333333333, 0, 0, 0.011627906976744186, 0, 0.04, 0, 0.05, 0, 0.018292682926829267, 0, 0.011904761904761904, 0, 0.02702702702702703, 0.009259259259259259, 0.03571428571428571, 0, 0]

    x_axis = []
    i = -0.5
    for co in comparison_objects:
        labels.append(co)
        intersections_counter.append(intersections_dict[co])
        precisions.append(precisions_dict[co])
        recalls.append(recalls_dict[co])
        f1scores.append(f1_dict[co])
        x_axis.append(i + 1)
        i += 1


    fig, ax1 = plt.subplots()

    color = 'tab:red'
    #plt.xticks(x, labels, rotation='vertical')
    plt.xticks(x_axis, labels, rotation='vertical')
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('size of intersection of ggl- and ccr-suggestions: i', color=color)
    ax1.scatter(x_axis, intersections_counter, color=color, marker=r"$i$")
    ax1.tick_params(axis='y', labelcolor=color)

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
