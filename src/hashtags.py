from itertools import islice
from typing import Generator, Iterable, List

import pandas as pd
from instaloader import Hashtag, Instaloader, Post, Profile

from src.instaprofile import get_profile
from src.posts import generate_post_metadict


def get_hashtag_posts(hashtag: str) -> Iterable[Post]:
    """Return a List of Posts associated with a hashtag.

    Args:
        hashtag (str): hashtag to search

    Returns:
        List[Post]: List of Post objects.
    """
    L = Instaloader()
    posts = Hashtag.from_name(L.context, HASHTAG).get_posts()
    return posts


def get_post_metadata_df(posts = List[Post],
                         num_posts: int = 10) -> pd.DataFrame:
    post_list = []
    for post in islice(posts, num_posts):
        try:
            pdict = generate_post_metadict(post)
            post_list.append(pdict)
        except Exception as e:
            print(e)
            continue

    return pd.DataFrame(post_list)


if __name__ == "__main__":
    HASHTAG = "urbanphotography"
    POSTS = get_hashtag_posts(HASHTAG)
    dfposts = get_post_metadata_df(POSTS)
