import requests
from bs4 import BeautifulSoup 

# def make_soup(url: str) -> BeautifulSoup:
#     res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'})
#     res.raise_for_status()
#     return BeautifulSoup(res.text, 'lxml')

# def parse_product_page(soup: BeautifulSoup) -> dict:
#     # title = soup.select_one('#productTitle').text.strip()
#     title = soup.find(id='productTitle').text.strip()
#     price = soup.find(id='priceblock_ourprice').text.strip()
#     return {
#         'title': title,
#         'price': price
#     }

# if __name__ == "__main__":
#     url = 'https://www.amazon.com/Lenovo-130S-11IGM-Laptop-Celeron-Windows/dp/B07RHMBGCF/ref=sr_1_1?keywords=lenovo+130s&qid=1562548099&s=gateway&sr=8-1'
#     soup = make_soup(url)
#     info = parse_product_page(soup)
#     print(info) 



class Product:
    def __init__(self, name: str, price: str):
        self.name = name
        self.price = price




class Category:
    def __init__(self, name: str, productsList: list):
        self.name = name
        self.productsList = productsList
        # self.productNames = productNames
        # self.productPrices = productPrices

    def printInfo(self):
        print('-----------------------------------------------------------------------------------------------------------------------')
        print('-----------------------------------------------------------------------------------------------------------------------')
        print('-----------------------------------------------------------------------------------------------------------------------')
        print('-----------------------------------------------------------------------------------------------------------------------')
        print('-----------------------------------------------------------------------------------------------------------------------')
        print('************' + self.name.upper() + ' ***************')
        for product in self.productsList:
            print('product: ', product.name)
            print('price: ', product.price)
            print('\n')

        print('-----------------------------------------------------------------------------------------------------------------------')
        print('-----------------------------------------------------------------------------------------------------------------------')
        print('-----------------------------------------------------------------------------------------------------------------------')
        print('-----------------------------------------------------------------------------------------------------------------------')
        print('-----------------------------------------------------------------------------------------------------------------------')
        

def make_soup(headers: dict) -> BeautifulSoup:
    url = 'https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_b_0_b_1'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'lxml')

def find_category_urls(soup: BeautifulSoup) -> list:
    links = []
    categoryUrls = []
    for tag in soup.find_all('a', href=True):
        links.append(tag['href'])

    for link in links:
        if 'Best-Sellers' in link and 'home' not in link:
            categoryUrls.append(link)
            
    return categoryUrls

def find_best_sellers(categoryUrls: list, headers: dict):
    del categoryUrls[-1]

    fullCategoryList = []

    for url in categoryUrls:
        productsList = []
        names = []
        prices = []
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        categoryName = soup.find('span', {'class': 'category'})
        categoryProductsByName = soup.select('.p13n-sc-truncate')
        categoryProductsByPrice = soup.select('.p13n-sc-price')
        if type(categoryName) != type(None):
            for item in categoryProductsByName:
                names.append(item.text.strip())

            for item in categoryProductsByPrice:
                prices.append(item.text.strip())

            if len(prices) != 0:
                for i in range(len(prices)):
                    productsList.append(Product(names[i-1], prices[i-1]))

            fullCategoryList.append(Category(categoryName.text, productsList))

    for cat in fullCategoryList:
        cat.printInfo()
        

if __name__ == "__main__":
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'}
    soup = make_soup(headers)
    categoryUrls = find_category_urls(soup)
    find_best_sellers(categoryUrls, headers)
    