# Brewston --Find you beer in any boston bars
#### My Insight data science project, which was done within 3 weeks time at Insight Boston

##### Slides: 
https://docs.google.com/presentation/d/1Glii9f5FqkTYCsX49IthPRIASuCGOdfMqKKvAzYAx-I/edit#slide=id.g4c93729644_2_24

##### Webapp: 
http://insight-app-yanchu.herokuapp.com/

## Structure
- beeradv_crawler                     ---- a web crawler I wrote to scrape beer ratings & reviews from beeradvocate.com
  - brcrawl.py                        ---- crawler
  - brparse.py                        ---- parser 1
  - beer_brew_style_idmapping.py      ---- parser 2
- beermenus_scraper                   ---- scraping scripts for beermenus.com, using selenium
  - bmscrp.py                         ---- scraper
  - bmpars.py                         ---- parser
  - matcher_google.py                 ---- script to match beer names between beermenus and beeradvocate using google search
- EDA.ipynb                           ---- show the data
- review_nlp
  - tfidf_glda.py                     ---- beer review topic modeling using guilded LDA with TFIDF
- recommendor
  - recomdl.py                        ---- recommendation model, with modification on the surprise package
- Heroku                              ---- Dash webapp running on heroku
  - app.py                            ---- Dash main file
  - utils
    - myweb.py                        ---- webpage setup
    - beername_matcher.py             ---- match input beername with beeradvocate data, using TFIDF vector matching
