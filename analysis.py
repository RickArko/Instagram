from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Set, Union

import pandas as pd
from tqdm import tqdm

from src import get_followers, get_profile
from src.utils import read_json

today = datetime.today().date()
yesterday = today - timedelta(days=1)


def _get_date(fname: Path) -> str:
    """Extract date from filename."""
    dt = str(fname).split("\\")[1].split("-followers.json")[0]
    return dt


def get_new_followers(prev_followers: set, current_followers: set) -> List[str]:
    """Get a list of new followers.

    Args:
        prev_followers (set): _description_
        current_followers (set): _description_

    Returns:
        List[str]: _description_
    """
    new = [f for f in current_followers if f not in prev_followers]
    if len(new) > 0:
        return new
    else:
        return


def get_new_unfollowers(prev_followers: set, current_followers: set) -> List[str]:
    """Get a list of new unfollowers.

    Args:
        prev_followers (set): _description_
        current_followers (set): _description_

    Returns:
        List[str]: _description_
    """
    new = [f for f in prev_followers if f not in current_followers]
    if len(new) > 0:
        return new
    else:
        return


def get_saved_followers(date_to_check: Union[str, datetime, pd.Timestamp]) -> Set[str]:
    """Get saved followers from a given date.

    Args:
        date_to_check (Union[str, datetime, pd.Timestamp]): _description_

    Returns:
        Set[str]: _description_
    """
    if hasattr(date_to_check, "strftime"):
        date_to_check = date_to_check.strftime("%Y-%m-%d")

    json_data = read_json(f"cache/{date_to_check}-followers.json")
    return set(json_data["followers"])
    
    
if __name__ == "__main__":
    saved_followers = list(Path("cache").glob("*-followers.json"))
    profile = get_profile("rickarko")
    current = get_followers(profile=profile)
    current_followers = set(current["followers"])
    
    dates = [_get_date(f) for f in saved_followers]
    
    results = []

    for d in tqdm(dates):
        historic_followers = get_saved_followers(d)
        
        new_followers = get_new_followers(historic_followers, current_followers)
        new_unfollowers = get_new_unfollowers(historic_followers, current_followers)
        
        day_result = {}
        day_result["date"] = d
        day_result["new_followers"] = new_followers
        day_result["new_unfollowers"] = new_unfollowers
        results.append(day_result)
        
    df = pd.DataFrame(results)