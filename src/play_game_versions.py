import pandas as pd
import os
import multiprocessing

from pysat.solvers import Minisat22
from pysat.examples.fm import FM
from pysat.formula import WCNF
from src.init_yashi_game import connect_points_to_lines
from src.plotting import plot_yashi
from src.sat.minimum_cost_length_constraints import calculate_minimum_length_solution_constraints
from src.sat.no_cycles_constraint import init_graph
from src.sat.basic_constraints import generate_yashi_basic_constraints
from src.graph.graph_connectivity import is_graph_connected


def play_game_version(path_to_file, save_game_path, version, to_show=True, count_sol=False):
    try:
        if version == 1:
            play_game_version1_findSolution(path_to_file, save_game_path, to_show, count_sol)
        elif version == 2:
            play_game_version2_findMinimumLengthSolution(path_to_file, save_game_path, to_show)
        else:
            print("Invalid version specified. Please use 1 or 2.")
    except FileNotFoundError:
        print("File not found. Please check the path_to_file.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def load_yashi_data(input_file):
    # Load Yashi game data from CSV
    yashi_points_csv = pd.read_csv(input_file)
    # This deals with "no diagonal lines" constraint.
    lines, points, pointsToLines = connect_points_to_lines(yashi_points_csv)
    # plot_yashi(lines, points, "No diagonal lines", "", to_show=True)
    # This deals with "all points connected" constraint
    graph = init_graph(lines)
    return lines, points, pointsToLines, graph


def play_game_version1_findSolution(input_file_path, output_path="", to_show=True, count_sol=False):
    lines, points, pointsToLines, graph = load_yashi_data(input_file_path)

    if not is_graph_connected(graph):
        print("No solution (graph is not connected).")
        plot_yashi({}, points, "Yashi Version 1 - No solution", output_path, to_show)
        return

    yashi_constraints = generate_yashi_basic_constraints(graph, lines, points, pointsToLines)

    solver = Minisat22()
    solver.append_formula(yashi_constraints.hard)
    solution_found = solver.solve()

    if solution_found:
        print("Solution exists.")
        save_figure_path = output_path + "_game1_solution"
        fig_title = "Version 1 - Solution"
        model = solver.get_model()
        model_lines = {x: lines[x] for x in model if x > 0}
        if count_sol:
            n_solutions = sum(1 for _ in solver.enum_models())
            print("Number of solutions:", n_solutions)
            fig_title = "Version 1 solution. #Solutions = " + str(n_solutions)
            save_figure_path = save_figure_path + "_#" + str(n_solutions)
        plot_yashi(model_lines, points, fig_title, save_figure_path, to_show)
    else:
        print("No solution.")
        plot_yashi({}, points, "Yashi Version 1 - No solution", output_path, to_show)


def play_game_version2_findMinimumLengthSolution(input_file_path, output_path="", to_show=True, show_length=True):
    lines, points, pointsToLines, graph = load_yashi_data(input_file_path)

    if not is_graph_connected(graph):
        plot_yashi({}, points, "Yashi Version 2 - No solution", output_path, to_show)
        print("No solution (graph is not connected).")
        return

    # Combine hard and soft constraints
    yashi_hard_constraints = generate_yashi_basic_constraints(graph, lines, points, pointsToLines)
    yashi_soft_constraints = calculate_minimum_length_solution_constraints(lines, points, pointsToLines)
    phi = WCNF()
    phi.extend(yashi_hard_constraints.hard)
    phi.extend(yashi_soft_constraints.soft, weights=yashi_soft_constraints.wght)

    solver = FM(phi)
    solution_found = solver.compute()

    if solution_found:
        print("Solution found.")
        model = solver.model
        # Calculate and display the cost of the solution
        cost = -sum(yashi_soft_constraints.wght) + solver.cost
        print(f"Cost of the solution: {cost}.")

        model_lines = {x: lines[x] for x in model if x > 0}
        save_figure_path = output_path + "_game2_solution"
        plot_yashi(model_lines, points, "Version 2 (Minimum length) - Solution: " + str(cost),
                   save_figure_path, to_show, show_length)
    else:
        print("No solution")
        plot_yashi({}, points, "Yashi Version 2 - No solution", output_path, to_show)


def run_all_game_configurations(to_show=True):
    input_folder_path = "game_data/"
    save_folder_path = 'game_results/'
    count_sol = False
    game_versions = [1, 2]

    # Loop through all files in the folder
    for filename in os.listdir(input_folder_path):
        if filename.endswith(".csv"):
            save_game_path = save_folder_path + filename[:-4]
            for game_version in game_versions:
                print(f"Playing version {game_version}, configuration: {filename}.")

                process = multiprocessing.Process(target=play_game_version,
                                                  args=(input_folder_path + filename, save_game_path, game_version,
                                                        to_show, count_sol))
                process.start()
                process.join(timeout=300)  # Wait for 5 minutes

                if process.is_alive():
                    print("Terminating game due to timeout.")
                    process.terminate()
                    process.join()  # Ensure the terminated process is cleaned up

                print('-' * 100)
