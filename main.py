import os

from src.play_game_versions import play_game_version, run_all_game_configurations


def main():
    # Modify these
    game_version = 2
    path_to_file = "game_data/original_yashi_7x7.csv"
    show_plot = True
    count_sol = False

    # Save path
    base_path = 'game_results/'
    save_game_path = base_path + os.path.splitext(os.path.basename(path_to_file))[0]

    print(f"Playing game: {os.path.splitext(os.path.basename(path_to_file))[0]}, Version: {game_version}.")

    play_game_version(path_to_file, save_game_path, game_version, show_plot, count_sol)


if __name__ == "__main__":
    main()
    # run_all_game_configurations(True)
