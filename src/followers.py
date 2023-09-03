from typing import Set
import os
from loguru import logger
from dotenv import load_dotenv
from instaloader import Profile

from src.instaprofile import get_profile

load_dotenv()


def get_profile_post_likers(profile: Profile) -> Set[Profile]:
    """Return a set of profiles that have liked any post for a Profile.
    """
    posts = profile.get_posts()
    logger.info(f"Get all likes for profile: {profile.username}.")
    likers = set()
    for post in posts:
        likers = likers | set(post.get_likes())
    return likers


def get_profile_followers(profile: Profile) -> Set[Profile]:
    """Return a set of profiles that follow a Profile.
    """
    logger.info(f"Get all followers for profile: {profile.username}.")
    return set(profile.get_followers())


def get_ghost_followers(profile: Profile) -> Set[Profile]:
    """Return a set of profiles that follow a Profile but do not like any of their posts.
    """
    likers = get_profile_post_likers(profile)
    followers = get_profile_followers(profile)
    ghosts = followers - likers
    logger.info(f"""Profile: {profile.username} has {len(ghosts):,d} ghost followers.""")
    return ghosts


if __name__ == "__main__":
    profile = get_profile(os.environ["USERNAME"])
    # LIKERS = get_profile_post_likers(profile)
    GHOSTS = get_ghost_followers(profile)
