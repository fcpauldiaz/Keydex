import sys
from datetime import datetime

import eventlet

import settings
from models import ProductRecord
from helpers import make_request, log, format_url, enqueue_url, dequeue_url
from extractors import get_title, get_url, get_price, get_primary_img, get_indexing

crawl_time = datetime.now()

pool = eventlet.GreenPool(settings.max_threads)
pile = eventlet.GreenPile(pool)


def begin_crawl():

    # explode out all of our category `start_urls` into subcategories
    with open(settings.start_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # skip blank and commented out lines
            print enqueue_url(line)
            # page, html = make_request(line)

            1/0
            count = 0

            # # look for subcategory links on this page
            # image_product = page.find('img', {'class': 's-access-image cfMarker'})  # find product image
            # #find no indexing tag
            # product_indexing = soup.find('h1', {'id': 'noResultsTitle'}) 
            # print image_product['src']
            
           

            # for subcategory in subcategories:
            #     link = subcategory.find("a")
            #     if not link:
            #         continue
            #     link = link["href"]
            #     count += 1
            #     enqueue_url(link)

            log("Found {} subcategories on {}".format(count, line))


def fetch_listing():

    global crawl_time
    url = dequeue_url()
    if not url:
        log("WARNING: No URLs {} found in the queue. Retrying...".format(url))
        #pile.spawn(fetch_listing)
        return

    page, html = make_request(url)
    if not page:
        return

    item = page
    product_image = get_primary_img(item)
    if not product_image:
        log("No product image detected, skipping")
        # continue
    product_title = get_title(item)
    product_url = get_url(item)
    product_price = get_price(item)
    product_indexing = get_indexing(item)

    product = ProductRecord(
        title=product_title,
        product_url=format_url(product_url),
        listing_url=format_url(url),
        price=product_price,
        primary_img=product_image,
        product_indexing=product_indexing,
        crawl_time=crawl_time

    )
    product_id = product.save()
    #download_image(product_image, product_id)

    # add next page to queue
    # next_link = page.find("a", id="pagnNextLink")
    # if next_link:
    #     log(" Found 'Next' link on {}: {}".format(url, next_link["href"]))
    #     enqueue_url(next_link["href"])
    #     pile.spawn(fetch_listing)


if __name__ == '__main__':

    if len(sys.argv) > 1 and sys.argv[1] == "start":
        log("Seeding the URL frontier with subcategory URLs")
        begin_crawl()  # put a bunch of subcategory URLs into the queue

    log("Beginning crawl at {}".format(crawl_time))
    [pile.spawn(fetch_listing) for _ in range(settings.max_threads)]
    pool.waitall()
