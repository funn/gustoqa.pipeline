# Recipes Scraper

## Using scraper
1.  Install docker-compose
2.  Clone this repo
3.  Go to the directory with the repo and run `docker-compose up -d` from command line
4.  Install scrapyd-client
5.  Run `scrapyd-deploy` from command line
6.  Schedule some spider to run with `curl http://localhost:6800/schedule.json -d project=gustoqa -d spider=copykat` executed from command line
7.  You can view the result in RabbitMQ management panel at http://localhost:15672/
8.  Images are stored in /stock directory inside the container
9.  Finally RabbitMQ and Scrapyd ports are exposed for consumption
