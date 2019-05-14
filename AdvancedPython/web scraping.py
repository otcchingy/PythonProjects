import re
import requests
from bs4 import BeautifulSoup

HTML = """<!DOCTYPE html>
<html itemscope="" itemtype="http://schema.org/QAPage" class="html__responsive"><head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">

        <title>Implementing the LZ78 compression algorithm in python - Stack Overflow</title>


<header class="top-bar js-top-bar top-bar__network _fixed">
    <div class="-container">
        <div class="-main">
                <a href="#" class="left-sidebar-toggle p0 ai-center jc-center js-left-sidebar-toggle"><span class="ps-relative"></span></a>
                                <a href="https://stackoverflow.com/" class="-logo js-gps-track" data-gps-track="top_nav.click({is_current:false, location:2, destination:8})">
                        <span class="-img _glyph">Stack Overflow</span>
                    </a>



        </div>

            <form id="search" action="/search" method="get" class="searchbar js-searchbar " autocomplete="off" role="search">
                    <div class="ps-relative">
                        <input name="q" type="text" placeholder="Search…" autocomplete="off" maxlength="240" class="s-input js-search-field ">
                        <button type="submit" aria-label="Search…" class="s-btn s-btn__primary s-btn__icon btn-topbar-primary js-search-submit"><svg aria-hidden="true" class="svg-icon iconSearch" width="18" height="18" viewBox="0 0 18 18"><path d="M12.86 11.32L18 16.5 16.5 18l-5.18-5.14v-.35a7 7 0 1 1 1.19-1.19h.35zM7 12A5 5 0 1 0 7 2a5 5 0 0 0 0 10z"></path></svg></button>
                    </div>
            </form>

        






    <div class="site-footer--col site-footer--category js-footer-col" data-name="Other">
        <ul class="-list">
                <li class="-item"><a href="https://meta.stackexchange.com/" class="-link js-gps-track" data-gps-track="footer.click({ location: 1, link: 25 })" title="meta-discussion of the Stack Exchange family of Q&amp;A websites">Meta Stack Exchange</a></li>
                <li class="-item"><a href="https://stackapps.com/" class="-link js-gps-track" data-gps-track="footer.click({ location: 1, link: 25 })" title="apps, scripts, and development with the Stack Exchange API">Stack Apps</a></li>
                <li class="-item"><a href="https://api.stackexchange.com/" class="-link js-gps-track" data-gps-track="footer.click({ location: 1, link: 25 })" title="programmatic interaction with Stack Exchange sites">API</a></li>
                <li class="-item"><a href="https://data.stackexchange.com/" class="-link js-gps-track" data-gps-track="footer.click({ location: 1, link: 25 })" title="querying Stack Exchange data using SQL">Data</a></li>
                <li class="-item"><a href="https://area51.stackexchange.com/" class="-link js-gps-track" data-gps-track="footer.click({ location: 1, link: 25 })" title="proposing new sites in the Stack Exchange network">Area 51</a></li>
                    </ul>
    </div>
                </div>
            </nav>
            <div class="site-footer--copyright fs-fine">
                <ul class="-list">
                    <li class="-item"><a class="js-gps-track -link" data-gps-track="footer.click({ location: 2, link:4 })" href="https://stackoverflow.blog/?blb=1">Blog</a></li>
                    <li class="-item"><a href="https://www.facebook.com/officialstackoverflow/" class="-link">Facebook</a></li>
                    <li class="-item"><a href="https://twitter.com/stackoverflow" class="-link">Twitter</a></li>
                    <li class="-item"><a href="https://linkedin.com/company/stack-overflow" class="-link">LinkedIn</a></li>
                </ul>

                <p class="mt-auto mb24">
site design / logo © 2019 Stack Exchange Inc; user contributions licensed under <a href="https://creativecommons.org/licenses/by-sa/3.0/" rel="license">cc by-sa 3.0</a>
                            with <a href="https://stackoverflow.blog/2009/06/25/attribution-required/" rel="license">attribution required</a>.
                    <span id="svnrev">rev&nbsp;2019.1.18.32694</span>
                </p>
            </div>
        </div>

            </footer>
            <script>StackExchange.ready(function () { StackExchange.responsiveness.addSwitcher(); })</script>
    <noscript>
        <div id="noscript-warning">Stack Overflow works best with JavaScript enabled
            <img src="https://pixel.quantserve.com/pixel/p-c1rF4kxgLUzNc.gif" alt="" class="dno">
        </div>
    </noscript>

    
<div class="adsbox" id="clc-abd" style="position: absolute; pointer-events: none;">&nbsp;</div><iframe id="google_osd_static_frame_8881606525790" name="google_osd_static_frame" style="display: none; width: 0px; height: 0px;" __idm_frm__="8589934631"></iframe><script src="Implementing%20the%20LZ78%20compression%20algorithm%20in%20python%20-%20Stack%20Overflow_files/markup.js"></script></body></html>

"""
"""
#####    Tips     #####

soup = BeautifulSoup(HTML, "html.parser")

# print(soup.prettify())
print(soup.find('title').text)
print(soup.find('title').string)
print(type(soup.find('title').text))
print(type(soup.find('title').string))

print(soup.find('div',{'class':'adsbox', 'id':'clc-abd'}))

divs = soup.find_all('div')
for div in divs:
    print(div.string)
    print(div.attrs) # return a list of attribute of objects with that tag
    print(div.attrs.get('class')) # get an atrribute from a list of a tributes 
    print(div.attrs.get('class', "return this if false")) # sets default return value if atrribute not found


locator = "arcticle.classname_optional div a" # a hirarchy of tags make locating easier
item = soup.select_one(locator)
print(item.attrs['attribute_name']) #return value for that attribute
## use regular expression to get certain items eg ..prices with symbols
"""

class HTMLPageLocators:
    """
    This class contains the locators that will be need
    to scrap your webpage
    """

    TITLE_LOCATOR = "title"
    SUBTITLE_LOCATOR = ""
    LINK_LOCATOR = ""
    PARENT_OBJECT_LOCATOR = "div ul li a"
    CHILD_NAME_LOCATOR = ""
    CHILD_SOMEPROPERTY_LOCATOR = ""
    # ADD OTHER PAGE PROPERTIES YOU NEED AND
    # DEFINE THIER FUNTIONS IN HTMLPAGEPARSER


class HTMLPageParser:
    """
    This class takes an HTML data or an Html link and or a list of Html Links
    or a generator that return an html link usually when it has pagination 
    return the part of html you want to scrap
    Uses The PARENT_OBJECT_LOCATOR defined in the HTMLPageLocator Class
    It also gets The page Title
    """

    def __init__(self, PageSource):
        self.soup = None

        if self.is_link(PageSource):
            HtmlPageSource = requests.get(PageSource)
            self.soup = BeautifulSoup(HtmlPageSource, "html.parser")
        elif isinstance(PageSource, (list, tuple)):
            for PageSource in PageSource:
                self.soup += BeautifulSoup(PageSource, "html.parser")
        elif "generator" in str(type(PageSource)):
            while True:
                try:
                    self.soup += BeautifulSoup(next(PageSource), "html.parser")
                except StopIteration:
                    break
        else:
            self.soup = BeautifulSoup(PageSource, "html.parser")

    def __repr__(self):
        return f"<HTMLPageParser {self.getTitle}>"

    @classmethod
    def is_link(self, line):
        p = re.compile("((http|https)://.*\.\w+)")
        if p.match(line):
            return True

    @property
    def getTitle(self):
        locator = HTMLPageLocators.TITLE_LOCATOR
        # title = self.soup.find(locator)
        title = self.soup.select_one(locator).string
        return title

    @property
    def getSubTitle(self):
        locator = HTMLPageLocators.SUBTITLE_LOCATOR
        subtitle = self.soup.select_one(locator).string
        return subtitle

    @property
    def getContent(self):
        return self.soup.prettify()

    @property
    def getItemsToScrap(self):
        locator = HTMLPageLocators.PARENT_OBJECT_LOCATOR
        subtitle = self.soup.select(locator)
        return subtitle


class HtmlScraper:
    """
    This class takes the Part of the Html to be scraped, scrapes it and
    return a list of the scraped items..also can be used like an iterator (generator)
    Scrapping methods must be defined in ScrapedObject class
    """

    SCRAPED_ITEMS = []
    NEXT_ITEM = 0

    def __init__(self, ItemsToScrap):
        for Item in ItemsToScrap:
            scrapeditem = self.ScrapedObject(Item)
            self.SCRAPED_ITEMS.append(scrapeditem)

    def __next__(self):
        if self.NEXT_ITEM < len(self.SCRAPED_ITEMS):
            scraped_item = self.SCRAPED_ITEMS[self.NEXT_ITEM]
            self.NEXT_ITEM += 1
            return scraped_item
        else:
            raise StopIteration()

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.SCRAPED_ITEMS)

    def __getitem__(self, index):
        if index < len(self.SCRAPED_ITEMS):
            return self.SCRAPED_ITEMS[index]
        else:
            raise IndexError()
    
    @classmethod
    def sort(self, function, reverse=False):
        return sorted(self.SCRAPED_ITEMS, key=function, reverse=reverse)

    class ScrapedObject:

        def __init__(self, Item):
            self.item = Item

        def __repr__(self):
            return f"ScrapedObject(name:{self.name})"

        @property
        def name(self):
            name = self.item.string
            return name

        @property
        def link(self):
            link = self.item.attrs.get('href')
            return link

        @property
        def someproperty(self):
            someproperty = "someproperty"
            return someproperty





page = HTMLPageParser(HTML)

print(page)

items = page.getItemsToScrap

scrapeditems = HtmlScraper(items)

for item in scrapeditems:
    print(item, item.link)