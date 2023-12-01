import datetime
import os
import pylast
import logging
from dotenv import load_dotenv
from mastodon import Mastodon
from dateutil.relativedelta import relativedelta

load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

LASTFM_API_KEY = os.environ.get("LASTFM_API_KEY")
LASTFM_API_SECRET = os.environ.get("LASTFM_API_SECRET")
LASTFM_USERNAME = os.environ.get("LASTFM_USERNAME")
LASTFM_PASSWORD = os.environ.get("LASTFM_PASSWORD")
MASTODON_ACCESS_TOKEN = os.environ.get("MASTODON_ACCESS_TOKEN")
MASTODON_BASE_URL = os.environ.get("MASTODON_BASE_URL")

# Validate required environment variables
required_env_vars = [
    LASTFM_API_KEY,
    LASTFM_API_SECRET,
    LASTFM_USERNAME,
    LASTFM_PASSWORD,
    MASTODON_ACCESS_TOKEN,
    MASTODON_BASE_URL,
]
if not all(required_env_vars):
    logging.error(
        "One or more environment variables are missing. Please check the README for more information."
    )
    exit(1)


def get_last_month():
    """
    Calculate the last month's date.
    Returns:
        month (int): The month number of the previous month.
        month_word (str): The name of the previous month.
    """
    last_month_date = datetime.date.today() - relativedelta(months=1)
    month = last_month_date.month
    month_word = last_month_date.strftime("%B")
    return month, month_word


def fetch_top_album(network, month):
    """
    Fetches the top album from LastFM for the given month.
    Args:
        network (pylast.LastFMNetwork): The LastFM network object.
        month (int): Month number for which to fetch the top album.
    Returns:
        top_album (pylast.Album): The top album object.
    """
    top_albums = network.get_authenticated_user().get_top_albums(
        period=pylast.PERIOD_1MONTH, limit=1
    )
    if top_albums:
        return top_albums[0].item
    else:
        logging.warning(f"No top album found for month {month}.")
        return None


def create_message(album, month_word):
    """
    Creates a message for posting, including album details and hashtags.
    Args:
        album (pylast.Album): The top album object.
        month_word (str): The name of the previous month.
    Returns:
        message (str): The crafted message for posting.
    """
    album_url = album.get_url()
    artist = album.artist.name
    playcount = album.get_userplaycount()
    tags = album.get_top_tags()

    message = f"In {month_word}, I thought the album {album.title} by {artist} was 🔥 I've scrobbled songs from it {playcount} times. {album_url}\n"

    for tag in tags[1:5]:  # Limit to 4 tags
        message += f"#{tag.item.name.strip().lower().replace(' ', '')} "

    return message


def post_to_mastodon(mastodon, message):
    """
    Posts the message to Mastodon.
    Args:
        mastodon (Mastodon): Mastodon instance.
        message (str): The message to post.
    """
    mastodon.status_post(message, visibility="public")


def main():
    try:
        if datetime.date.today().day != 1:
            logging.info("Not the first day of the month. Exiting.")
            return

        network = pylast.LastFMNetwork(
            api_key=LASTFM_API_KEY,
            api_secret=LASTFM_API_SECRET,
            username=LASTFM_USERNAME,
            password_hash=pylast.md5(LASTFM_PASSWORD),
        )

        month, month_word = get_last_month()
        top_album = fetch_top_album(network, month)

        if top_album:
            message = create_message(top_album, month_word)
            mastodon = Mastodon(
                access_token=MASTODON_ACCESS_TOKEN, api_base_url=MASTODON_BASE_URL
            )
            post_to_mastodon(mastodon, message)
            logging.info("Message posted to Mastodon.")
        else:
            logging.info("No top album to post.")
    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    main()
