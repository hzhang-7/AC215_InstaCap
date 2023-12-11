import requests
from bs4 import BeautifulSoup
import re 

from instagrapi import Client
from instagrapi.types import Usertag
from secrets import config 

def get_influencers():

    """Gets a list of influencers from different categories (from hubspot link)

    Args
    ----------

    Returns
    -------
    top_n_usernames: list
        a list containing the usernames of the influencers from different categories 
    """
    
    # list of usernames 
    influencers = []

    # url of influencers by category 
    url = "https://blog.hubspot.com/marketing/instagram-influencers#food"

    # HTTP get request to url
    response = requests.get(url)

    # check for successful request 
    if response.status_code == 200:

        # Parse HTML content from webpage 
        soup = BeautifulSoup(response.text, 'html.parser')

        # tag for category of influencers 
        ol_elements = soup.find_all('ol')

        for ol_element in ol_elements:
            # Find all <a> elements within each <ol> element
            a_elements = ol_element.find_all('a')
            for a in a_elements:
                href = a.get('href')
                if href:
                    # extract username from instagram url 
                    match = re.search(r'https://www.instagram.com/([^/]+)/?', href)
                    if match:
                        username = match.group(1)
                        influencers.append(username)

        return influencers 
    
    else:
        print("Failed to retrieve webpage. Status code:", response.status_code)
        return None



def most_followed_username(n = 10):
    
    """Gets the most followed instagram username accounts 

    Args
    ----------
    n : int
        number of most followed instagram accounts you want 

    Returns
    -------
    top_n_usernames: list
        a list containing the usernames of the n most followed instagram accounts 
    """
    
    # The URL of the Wikipedia page containing the list of 50 most-followed Instagram accounts
    url = "https://en.wikipedia.org/wiki/List_of_most-followed_Instagram_accounts"

    # HTTP GET request to fetch url 
    response = requests.get(url)

    # Parse HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # table containing most-followed Instagram accounts
    table = soup.find("table", {"class": "wikitable"})
    
    usernames = []
    
    # Iterate through rows of the table
    # Skip header 
    for row in table.find_all("tr")[1:]:
        columns = row.find_all("td")
        username = columns[0].text.strip()
        # take out @
        username = re.sub(r'@', '', username)
        usernames.append(username)
            
    top_n_usernames = usernames[:n]
    
    # return top n usernames 
    return top_n_usernames 


def get_usernames(username, n=0):

    """Gets the usernames of the followers of an instagram account

    Args
    ----------
    username : str
        instagram username account that you want to get followers of 
    n : int
        how many followers of username you want to extract. 0 pulls all usernames 

    Returns
    -------
    follower_usernames: list
        a list containing the usernames of username's followers 
    """

    # login 
    ig_username = config.ig_username
    ig_password = config.ig_password
    ig_2fa = config.ig_2fa

    # Initialize the client 
    cl = Client()
    cl.login(ig_username, ig_password, ig_2fa)

    # get user_id that API uses to uniquely identify associated input username 
    user_id = cl.user_id_from_username(username)

    # get followers of the input username 
    followers = cl.user_followers(user_id, n)

    # store usernames of the followers in list 
    follower_usernames = [followers[k].username for k in followers.keys()]

    return follower_usernames