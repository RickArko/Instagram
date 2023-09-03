from loguru import logger
from datetime import datetime
from src.utils import save_dict
from src.instaprofile import get_profile, get_followers


if __name__ == "__main__":
    logger.info("Starting Instagram Tracker...")
    PROFILE = get_profile("rickarko")
    follower_dict = get_followers(PROFILE)
    fname_followers = f"""cache/{datetime.today().strftime("%Y-%m-%d")}-followers.json"""
    save_dict(follower_dict, fname_followers)
    logger.info(f"""Saved {follower_dict["nfollowers"]} followers to {fname_followers}""")