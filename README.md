# Recipes Scraper

## Using scraper
1.  Install system packages, command for Debian-based systems: `sudo apt-get install python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev`
2.  Clone this repo
3.  Go to the directory with the repo and run `pip install -r requirements.txt` from command line
4.  Adjust the gustoqa/settings.py as needed.
5.  Run the spider with `scrapy crawl <spider>`, you can view available spiders with `scrapy list`



on mac
1. install docker compose
2. once done run init_docker.sh to set-env
