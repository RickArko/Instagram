import pandas as pd
import time
from typing import Union
from pathlib import Path
import requests
from PIL import Image
from loguru import logger
from tqdm import tqdm
tqdm.pandas()


def download_image(url: str,
                   filepath: Path,
                   sleep_seconds: int = 1,
                   overwrite: bool = False
                   ) -> None:
    
    if isinstance(filepath, str):
        filepath = Path(filepath)

    if filepath.exists() and not overwrite:
        logger.info(f"File already exists at {filepath}. Skipping download.")
        return
    response = requests.get(url)
    if response.status_code == 200:  # HTTP status code for success
        with open(filepath, 'wb') as f:
            f.write(response.content)
            time.sleep(sleep_seconds)
    else:
        logger.warning(f"Failed to download image at {url}. HTTP Status Code: {response.status_code}")


def display_image(filepath: Union[str, Path]):
    # Open an image file
    with Image.open(filepath) as img:
        # Display the image
        img.show()


if __name__ == "__main__":

    filepath = Path("cache/test.jpg")  # Replace with your image's filepath
    url = "https://scontent-ord5-2.cdninstagram.com/v/t51.2885-15/358172263_981524823090698_8015635719662731785_n.jpg?stp=c180.0.1080.1080a_dst-jpg_e35_s640x640_sh0.08&_nc_ht=scontent-ord5-2.cdninstagram.com&_nc_cat=102&_nc_ohc=bFOMpTJM7qsAX-8Xoye&edm=AOQ1c0wBAAAA&ccb=7-5&ig_cache_key=MzE0MjQyNTI5NzAxNDA5NzYzMQ%3D%3D.2.c-ccb7-5&oh=00_AfBywkn8PuBkwYAg24X1MUn56IE6JHFDHCtEQKqJVQt8Gg&oe=64FD2BDD&_nc_sid=8b3546"
    
    SAVE_DIR = Path("cache").joinpath("follower-posts")
    dfposts = pd.read_parquet(SAVE_DIR.joinpath("dfposts.snap.parquet"))
    
    url = dfposts[dfposts["owner_username"] == "rickarko"].sort_values("taken_at_timestamp", ascending=False)["thumbnail_src"].iloc[0]
    download_image(url, filepath, overwrite=True)
    display_image(filepath)
    
    user = "rickarko"
    dfuser = dfposts[dfposts["owner_username"] == user]
    dfuser.progress_apply(lambda x: download_image(x["display_url"], f"cache/{x['shortcode']}_{x['owner_username']}.jpg"), axis=1)
