from pathlib import Path
from src import get_profile
from src.posts import get_top_posts_df
from src.followers import get_ghost_followers
from src.analysis.followers import get_follower_updates_by_date


if __name__ == "__main__":
    
    profile = get_profile("rickarko")
    dfposts = get_top_posts_df(profile, n=25)
    dffollowers = get_follower_updates_by_date(profile, Path("cache").glob("*-followers.json"))
    ghosts = get_ghost_followers(profile)
