import json
import os
import time
from datetime import datetime
from pathlib import Path

import instaloader
import pandas as pd
from dotenv import load_dotenv
from loguru import logger
from tqdm import tqdm

from src.instaprofile import get_followers, get_profile
from src.utils import read_json

load_dotenv()

def get_downloaded_profiles(dir: Path):
    return [d for d in list(dir.iterdir()) if d.is_dir()]


def get_empty_dirs(dir: Path):
    return [d for d in list(dir.iterdir()) if d.is_dir() & d.stat().st_size == 0]


def get_profile_posts(username: str, save_path: Path):
    """Create a Directory {save_path/username} and Download all posts for a given user.

    
    Args:
        username (str): instagram username
        save_path (Path): local directory to save results to.
    """
    save_path = save_path.joinpath(username)
    save_path.mkdir(exist_ok=True, parents=True)

    L = instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_video_thumbnails=False,
        compress_json=False,
        download_geotags=False,
        post_metadata_txt_pattern=None,
        max_connection_attempts=0,
        download_comments=False,
        )

    L.load_session_from_file(os.environ.get("USERNAME", "rickarko"))
    profile = instaloader.Profile.from_username(L.context, username)
    posts = profile.get_posts()

    for post in tqdm(posts):

        post_sleep = 1 # Sleep 1 seconds between posts
        # print("sleeping for: " + str(post_sleep) + " seconds")
        time.sleep(post_sleep)

        data = post.__dict__
        data_node = data["_node"]
        captured_on = time.strftime("%Y-%m-%d")
        file_name = captured_on+"_"+post.shortcode
        with open(os.path.join(save_path, file_name+".json"), "w", encoding='utf-8') as write_file:
            json.dump(data_node, write_file, sort_keys=True, indent=4, ensure_ascii=False)
            # print(write_file)


if __name__ == "__main__":

    SECONDS = 300 # Sleep Time between users. 5 minutes recommended.
    SAVE_DIR = Path("cache").joinpath("follower-posts")
    SAVE_DIR.mkdir(exist_ok=True, parents=True)
    
    downloaded_users = get_downloaded_profiles(SAVE_DIR)
    followers = get_followers(get_profile(os.environ.get("USERNAME", "rickarko")))["followers"]

    names = [f.split(" ")[0] for f in followers]
    names = [n for n in names if n not in [n.name for n in downloaded_users]]

    logger.info(f"Begin Downloading Posts Data for: {len(names):,d} users")

    for name in tqdm(names):
        logger.info(f"Downloading Data for: {name}")
        get_profile_posts(name, SAVE_DIR)
        logger.info(f"Finished: {name} sleeping for {SECONDS / 60 :,.1f} minutes")
        time.sleep(SECONDS)
    
    SAVED_USERS = get_downloaded_profiles(SAVE_DIR)
