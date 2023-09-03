from itertools import islice
from typing import Dict, List

import pandas as pd
from instaloader import Post, PostComment, Profile
from loguru import logger
from tqdm import tqdm

from src import get_profile


def generate_post_metadict(post: Post,
                           full_metadata: bool = False
                           ) -> Dict:
    """Generate dictionary of post metadata.

    Args:
        post (Post): instaloader.Post object.

    Returns:
        Dict: dictionary of post metadata.
    """
    post_dict = dict()
    post_dict["profile"] = post.profile
    post_dict["post_caption"] = post.pcaption
    post_dict["nposts"] = post.mediacount
    post_dict["ncomments"] = post.comments
    post_dict["post_date"] = post.date
    post_dict["code"] = post.shortcode
    post_dict["tagged"] = post.tagged_users
    post_dict["post.location"] = post.is_pinned
    post_dict["is_video"] = post.is_video
    post_dict["nlikes"] = post.likes
    post_dict["caption_hashtags"] = post.caption_hashtags
    post_dict["caption_mentions"] = post.caption_mentions
    post_dict["caption"] = post.caption
    
    # Comments
    comments = post.get_comments()
    post_dict["comments"] = comments
    post_dict["ncomments"] = comments.count
    # post.shortcode_to_mediaid(post.shortcode)
    
    # Slower metadata to query
    if full_metadata:
        post_dict["location"] = post.location
    return post_dict


def extract_comment_metadata(comment: PostComment) -> Dict:
    if comment is None:
        return
    comment_dict = dict()
    comment_dict["_id"] = comment.id
    comment_dict["dateutc"] = comment.created_at_utc
    comment_dict["name"] = comment.owner.username
    comment_dict["text"] = comment.text
    return comment_dict


def get_top_posts_df(profile: Profile, n: int = 10) -> pd.DataFrame:
    """Create a DataFrame of top n posts with metadata.

    Args:
        profile (Profile): _description_
        n (int, optional): _description_. Defaults to 10.

    Returns:
        pd.DataFrame: _description_
    """
    logger.debug(f"Getting top {n} posts from {profile.username}")

    posts = profile.get_posts()
    post_data = list()
    for post in tqdm(islice(posts, n)):
        pdict = generate_post_metadict(post)
        post_data.append(pdict)

    dfposts = pd.DataFrame(post_data)
    logger.debug(f"Returning posts dataframe with shape: {dfposts.shape}")
    return dfposts


if __name__ == "__main__":

    profile = get_profile("rickarko")
    dfposts = get_top_posts_df(profile, n=25)
