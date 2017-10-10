from HTMLParser import HTMLParser

htmlparser = HTMLParser()

def get_indexing(item):
    count_true = 0
    count_false = 0
    max_count = 100
    result = 'Information Not Available'
    while (True):
        product_indexing = item.find_all('h1', {'id': 'noResultsTitle'})
        if len(product_indexing) == 1:
            count_false += 1 # product is not indexing
        else:
            count_true += 1 # product is indexing
        if ((count_true - count_false) > max_count):
            result = True
            break
        if ((count_false - count_true) > max_count):
            result = False
            break  
    return result

def get_title(item):
    title = item.find("h2", "s-access-title")
    if title:
        return htmlparser.unescape(title.text.encode("utf-8"))
    else:
        return "<missing product title>"


def get_url(item):
    link = item.find("a", "s-access-detail-page")
    if link:
        return link["href"]
    else:
        return "<missing product url>"


def get_price(item):
    price = item.find("span", "sx-price")
    if price:
        return parse_price(price.text)
    price = item.find("span", "s-price")
    if price:
        return parse_price(price.text)
    price = item.select(".a-size-base.a-color-base")
    if price:
        return price[0].text.strip()
    return ""


def get_primary_img(item):
    thumb = item.find("img", "s-access-image")
    if thumb:
        src = thumb["src"]

        p1 = src.split("/")
        p2 = p1[-1].split(".")

        base = p2[0]
        ext = p2[-1]

        return "/".join(p1[:-1]) + "/" + base + "." + ext

    return None
def parse_price(price):
    parsed_price = "".join((price).split())
    formatted_price = parsed_price[:len(parsed_price)-2] + '.' + parsed_price[len(parsed_price)-2:]
    return formatted_price