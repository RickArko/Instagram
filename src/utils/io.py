import json
from typing import Dict, Union
from pathlib import Path


def read_json(fname: Union[str, Path]) -> Dict:
    """Read local json to dictionary.

    Args:
        fname (str): _description_

    Returns:
        Dict: _description_
    """
    with open(fname, "r") as f:
        return json.load(f)


def save_dict(dict: Dict, fname: Union[str, Path]) -> None:
    """Save dictionary to json file.

    Args:
        dict (Dict): dictionary to save
        fname (str): relative path to save file
    """
    # fname.mkdir(exist_ok=True, parents=True)
    with open(fname, "w") as f:
        json.dump(dict, f, indent=4)
