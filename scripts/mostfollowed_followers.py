import requests
from bs4 import BeautifulSoup
import instaloader as ig
import re 
import json


def most_followed(n = 10):
    
    """Gets and prints the spreadsheet's header columns

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


def main():
    top_10_usernames = most_followed()
    loader = ig.Instaloader()
    loader.login('myusername', 'mypassword')

    ig_dict = {}  # Create a dictionary to store the data

    for user in top_10_usernames:
        profile = ig.Profile.from_username(loader.context, user)
        followers = [follower.username for follower in profile.get_followers()]
        ig_dict[user] = followers

    # Save the data to a JSON file
    with open('most_followed_users_followers.json', 'w') as json_file:
        json.dump(ig_dict, json_file)


if __name__ == "__main__":
    main()