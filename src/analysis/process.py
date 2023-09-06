import json
import os
from pathlib import Path
from typing import List
import pandas as pd
from dotenv import load_dotenv
from loguru import logger
from tqdm import tqdm


def read_post_json(file):
    with open(file, encoding="utf-8") as f:
        data = json.load(f)
    return data


def convert_post_json_to_dict(data):
    d = dict()
    d["type"] = data["__typename"]
    d["viewer_has_liked"] = data.get("viewer_has_liked", False)
    
    location = data["location"]
    
    if location is not None:
        d["location_id"] = location.get("id")
        d["location_name"] = location.get("name")
    elif location is None:
        d["location_id"] = None
        d["location_name"] = None

    d["is_video"] = data["is_video"]
    d["owner_id"] = data["owner"]["id"]
    d["owner_username"] = data["owner"]["username"]

    d["taken_at_time_unix"] = data["taken_at_timestamp"]
    d["taken_at_timestamp"] = pd.to_datetime(data["taken_at_timestamp"], unit="s")

    # Fact check
    d["fact_check_overall_rating"] = data.get("fact_check_overall_rating")
    d["fact_check_information"] = data.get("fact_check_information")
    
    # # Edge Media    
    # edges = data["edge_media_preview_like"]["edges"]
    # if len(edges) > 1:
    #     logger.warning(f"More than one edge: {edges}")
    # for node in edges:
    #     d["likecount"] = data["edge_media_preview_like"].get("count", 0)
    #     d["profile_pic_url"] = node.get("profile_pic_url")
    #     d["username"] = node.get("username")
    
    # data["viewer_in_photo_of_you"]
    # data['viewer_can_reshare']
    # data["accessibility_caption"]
    # data["comments_disabled"]
    # data["dimensions"]
    # 'accessibility_caption', 'comments_disabled', 'display_url', 'fact_check_information', 'fact_check_overall_rating',
    # 'gating_info', 'id', 'is_video', 'location', 'media_overlay_info', 'media_preview', 'sensitivity_friction_info', 'shortcode',
    # 'taken_at_timestamp', 'thumbnail_src', 'tracking_token', 'viewer_can_reshare', 'viewer_has_liked', 'viewer_has_saved', 'viewer_has_saved_to_collection', 'viewer_in_photo_of_you']
    
    keys_to_copy_if_present = ["display_url", "video_view_count", "video_url", "video_duration"]
    
    str_keys = ['display_url', 'id', 'media_preview', 'shortcode', 'thumbnail_src', 'tracking_token']
    
    keys_to_copy_if_present = ['display_url', 'id', 'media_preview', 'shortcode', 'thumbnail_src', 'tracking_token', 'comments_disabled', 'gating_info', 'id', 'is_video',
                               'viewer_can_reshare', 'viewer_has_liked', 'viewer_has_saved', 'viewer_has_saved_to_collection', 'viewer_in_photo_of_you',
                               'media_overlay_info', 'media_preview', 'sensitivity_friction_info', 'thumbnail_src',
                               ]

    for key in keys_to_copy_if_present:
        d[key] = data.get(key)

    return d


def process_downloaded_posts(local_directories: List[Path]) -> pd.DataFrame:
    """Process local posts json data and combine into a single DataFrame.

    Args:
        local_directories (List[Path]): directories generated from download_profile_posts.py

    Returns:
        pd.DataFrame: DataFrame of post metadata.
    """
    logger.info(f"Begin to process {len(local_directories):,d} local directories of downloaded posts.")
    results = []

    for user in tqdm(local_directories):

        for json_file in user.glob("*.json"):
            data = read_post_json(json_file)
            post_dict = convert_post_json_to_dict(data)
            post_dict["local_path"] = user
            results.append(post_dict)

    dfr = pd.DataFrame(results)
    dfr["local_path"] = dfr["local_path"].astype(str)
    return dfr


if __name__ == "__main__":

    load_dotenv()
    from download_profile_posts import get_downloaded_profiles
    SAVE_DIR = Path("cache").joinpath("follower-posts")
    downloaded_users = get_downloaded_profiles(SAVE_DIR)
    dfresults = process_downloaded_posts(downloaded_users)
    dfresults.to_parquet(SAVE_DIR.joinpath("dfposts.snap.parquet"))
