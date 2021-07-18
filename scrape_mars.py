from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    # ## NASA Mars News
    url = 'https://redplanetscience.com'
    browser = init_browser()
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find_all("div", class_="content_title")
    content_titles = []
    for result in results:
        content_titles.append(result.text)

    results = soup.find_all("div", class_="article_teaser_body")
    content_para = []
    for result in results:
        content_para.append(result.text)

    content = []
    for i in range(len(results)):
        content.append({'title': content_titles[i], 'para': content_para[i]})
    mongo_collection = {'contents': content,
                        'featured_image_url': '',
                        'hemisphere': ''
                        }

# ## JPL Mars Space Images - Featured Image

    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    links_found = browser.links.find_by_partial_text('FULL IMAGE')
    for link in links_found:
        print(link["href"])
        featured_image_url = link["href"]
    mongo_collection['featured_image_url'] = featured_image_url

    url = 'https://galaxyfacts-mars.com'
    tables = pd.read_html(url)

    df = tables[1]
    df.to_html('MarsFacts.html')

    # ## Mars Hemispheres

    url = 'https://marshemispheres.com/'
    browser.visit(url)

    links = browser.links.find_by_partial_text('Hemisphere Enhanced')
    for link in links:
        print(link['href'])

    hemisphere_image_urls = []
    for i in range(len(links)):
        browser.links.find_by_partial_text('Hemisphere Enhanced')[i].click()
        link_img = browser.links.find_by_partial_text('Original')
        soup = bs(browser.html, 'html.parser')
        title = soup.find('h2', class_='title').text.replace(" Enhanced", "")
        hemisphere_image_urls.append(
            {"title": title, "img_url": link_img["href"]})
        browser.links.find_by_partial_text('Back').click()
    mongo_collection['hemisphere'] = hemisphere_image_urls

    return mongo_collection
