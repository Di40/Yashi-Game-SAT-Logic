import os
import yaml
import numpy as np
from itertools import chain, combinations


def load_config(config_name, config_path):
    config_file = os.path.join(config_path, config_name)

    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Configuration file '{config_file}' not found")

    try:
        with open(config_file) as file:
            config = yaml.safe_load(file)
        return config
    except yaml.YAMLError as e:
        raise ValueError(f"Error loading YAML from '{config_file}': {e}")


def powerset(iterable):
    return chain.from_iterable(combinations(iterable, r) for r in range(len(iterable) + 1))


def euclidean_distance(point1, point2):
    point1, point2 = np.array(point1), np.array(point2)
    return np.linalg.norm(point1 - point2)
