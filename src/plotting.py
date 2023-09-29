import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np


def plot_yashi(lines, points, title="", output_path="", to_show=True, show_length=False):

    if not output_path and not to_show:
        return

    fig, ax = plt.subplots()
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])  # ax.margins(x=0.1, y=0.1)

    # Plot the points with markers inside
    for point_ID in points:
        r, c = points[point_ID]
        ax.plot(r, c, "bo", markersize=16)
        ax.annotate(point_ID, (r, c), fontsize=10, ha='center', va='center', color='yellow')

    # Plot the lines
    for line_ID, (point1_ID, point2_ID) in lines.items():
        (x1, y1), (x2, y2) = points[point1_ID], points[point2_ID]
        ax.plot([x1, x2], [y1, y2], "k-", linewidth=2.0)
        line_length = int(np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
        if show_length:
            if x1 - x2 == 0:  # Check if the line is vertical
                ax.annotate(line_length, (x1 + 0.04, (y1 + y2) / 2),
                            fontsize=12, ha='left', va='center', color='red')
            else:
                ax.annotate(line_length, ((x1 + x2) / 2, (y1 + y2) / 2 + 0.02),
                            fontsize=12, ha='center', va='bottom', color='red')

    # Set major ticks to integers on both x and y axes
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    title_font = {'family': 'serif', 'color': 'blue', 'size': 16}
    ax.set_title(title, fontdict=title_font)

    ax.set_xlabel("x")
    ax.set_ylabel("y")

    ax.grid(True)

    if output_path:
        plt.savefig(output_path)

    if to_show:
        plt.show()
    else:
        plt.close()
