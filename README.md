<center><img src="./assets/lastfm-to-mastodon.png" width=256></center>

# lastfm-to-mastodon

A simple Python script for sharing your monthly top album from LastFM to your Mastodon account.

## What does this script do?

On the first day of each month, this script fetches your most-played album from the previous month on LastFM and posts about it on Mastodon. It includes details like the album name, artist, play count, a link to the album, and some hashtags.

## Requirements

- Python 3.x
- LastFM account and application
- Mastodon account and application

## Configuration

Create a copy of the `.env.example` file and call it `.env`, then populate all of the variables with your own data.

## Usage

Run the script:


```shell
python main.py
```
For automated monthly posts, set up a cron job or a similar scheduler. There is an example github action in `./github/workflows/monthly_poster.yml`

## Contributing

Ideas, bug reports, and pull requests are welcome on GitHub at [https://github.com/wardbox/lastfm-to-mastodon].

## License

This script is available as open source under the terms of the MIT License.
