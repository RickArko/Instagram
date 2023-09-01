from datetime import datetime
from typing import Dict

import instaloader


class NoFollowersError(Exception):
    pass

def get_profile(username: str) -> instaloader.Profile:
    """Get profile from Instagram"""
    
    L = instaloader.Instaloader()
    L.load_session_from_file(username) # (load session created w/ `instaloader -l USERNAME`)  # execute scripts/login.py to create session file
    profile = instaloader.Profile.from_username(L.context, username)
    return profile


def get_followers(profile: instaloader.Profile) -> Dict:
    """Generate dictionary of follower metadata.

    Args:
        profile (instaloader.Profile): _description_

    Returns:
        Dict: follower metadata for profile.
    """
    followers = list(profile.get_followers())
    
    if len(followers) == 0:
        raise NoFollowersError("No followers found.")
    result_dict = dict()
    result_dict["timestamp"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    result_dict["nfollowers"] = len(followers)
    result_dict["followers"] = [str(f).replace("<Profile ", "").replace(">", "") for f in followers]
    return result_dict



if __name__ == "__main__":
    profile = get_profile("rickarko")
    get_followers(profile=profile)