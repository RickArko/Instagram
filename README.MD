# Instagram Utilities
Module to automate and track interactions and data from Instagram.


# Usage
Sign in to instagram.com using FireFox then run `python src/scripts/login.py` to generate local cache file to use for authentication.

## CLI Commands

### Download private profile you follow
```

    instaloader -l PROFILE -- profile PROFILE_TO_DOWNLOAD
```

### Login 
(need to be signed in with FireFox brower - uses a saved cookie)
```
    pipenv run src\scripts\login.py
```

### Download Posts
Download all posts for followers and serialize dataframe.
```
    pipenv run download_profile_posts.py
```

## Packages
- [instaloader](https://instaloader.github.io/troubleshooting.html)


## Installation
```
    set PIPENV_VENV_IN_PROJECT=1
    pipenv install --dev --skip-lock
```
