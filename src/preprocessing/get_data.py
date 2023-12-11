import requests
import instaloader

L = instaloader.Instaloader()

def get_post_data_from_profiles(profile_list = ["mbinkowski56"]):
    
    """Gets the data for every post

    Args:
        profile_list (list, optional): _description_. Defaults to ["mbinkowski56"].

    Returns:
        processed_posts: a list of dictionaries containing the owner_username, mediaid, caption, post url, and photo
    """

    # List of posts and post data
    processed_posts = []
    
    # Iterate through profiles in profile_list
    for profile_name in profile_list:

        # Get profile information
        profile = instaloader.Profile.from_username(L.context, profile_name)
        
        if not profile.is_private:
            # Iterate though the first 100 posts of a profile
            i = 0
            for post in profile.get_posts():

                # Check if post url is good
                response = requests.get(post.url)
                if response.status_code == 200:
                    
                    # Get the image data as bytes
                    image_data = response.content
                    
                    # Create and add dictionary of post data
                    processed_posts.append({
                        'owner_username': post.owner_username,
                        'mediaid': post.mediaid,
                        'caption': post.caption,
                        'url': post.url,
                        'photo': image_data,
                    })
                    i+=1
                    if(i>100):
                        break
                else:  
                    print('Failed to retrieve the image data.')
        else:
            print('PRIVATE PROFILE')        
        # Return post data
        return processed_posts
