# Yashi puzzle solver: A constraint-based approach with SAT solver

# Introduction 

Goal: **Connect all the dots** while following these **constraints** (rules):
1. Diagonal lines aren’t allowed;
2. All points must be connected;
3. Lines cannot cross each other;
4. Exactly $n-1$ lines must be used, where $n$ is the number of points;
5. No closed loops.

A thorough explanation about the game and my approach can be found in the project [Presentation](Presentation.pdf).\
If you would like to play Yashi and explore more examples, visit [Yashi Puzzle](http://www.sumsumpuzzle.com/yashi.htm).


The game can be divided up in two sub-games:
* Version 1: If there is a solution, return one solution.

![Example of a Version 1 Yashi game](/game_results/original_yashi_8x8_game1_solution.png "Example of a Version 1 Yashi game")
* Version 2: If there is a solution, return a minimum-length solution.

![Example of a Version 2 Yashi game](/game_results/original_yashi_8x8_game2_solution.png "Example of a Version 2 Yashi game")

***To find a solution to the game, I employed a combination of graph theory and SAT-solving. First, a graph theory-based approach is used to check whether the initial graph is connected, and if it is, the next step is to discover all possible cycles. Then, after generating all the necessary constraints (no cycles, no crossing lines, and exactly $n-1$ lines), they are passed to a SAT solver.***

# Requirements

Before running the application be sure to have installed all the required libraries:
   
    $ pip install -r requirements.txt

# Usage

The application can be executed by simply running main.py, where you can modify several constants:

* game_version: Enter 1 or 2, depending on the game version you want to play.
* path_to_file: The path to the CSV file containing the game configuration you wish to use.
* show_plot: A flag indicating whether to display the plot.
* count_sol: A flag indicating whether to count how many solutions there are in Version 1.

Alternatively, you can run all possible game versions and configurations by using run_all_game_configurations(True) instead of main().

The format of the CVS file is the following:
   
    point,x,y
    ---,---,---

and some examples are located in the game_data folder.

The results will be saved in the game_results folder.

# References

- [Yashi Puzzle](http://www.sumsumpuzzle.com/yashi.htm)
- [Formal Modeling with Propositional Logic](https://www.cs.bu.edu/faculty/kfoury/UNI-Teaching/CS512/AK_Documents/Modeling-with-PL/main.pdf)
- [Enumerating All Cycles in an Undirected Graph](https://www.codeproject.com/Articles/1158232/Enumerating-All-Cycles-in-an-Undirected-Graph)
- [PySAT Documentation](https://pysathq.github.io/)
