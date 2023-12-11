# preprocess.py

from google.cloud import storage
from PIL import Image
import io
import requests
import instaloader
import os

def get_profile_list(files):
    profiles = []
    for file in files:
        try:
            with open(file, 'r') as file:
                profiles.extend([line.strip() for line in file.readlines()])
        except FileNotFoundError:
            print(f"The file '{file}' was not found.")
        except Exception as e:
            print(f"An error occurred while processing '{file}': {str(e)}")
    return profiles


def initialize_storage_client():
    '''
    initialize google cloud storage client
    '''
    return storage.Client()

def download_and_preprocess_image(bucket_name, blob_name, image_bytes, target_size=(256, 256)):
    '''
    download and preprocess an image by doing a central crop to make an image 256x256 pixels
    '''
    try:
        client = initialize_storage_client()

        # get reference to the bucket and blob
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)

        # download image as bytes and get via pillow
        #image_bytes = blob.download_as_bytes()
        image = Image.open(io.BytesIO(image_bytes))

        width, height = image.size

        # determine crop dimensions
        if width > height:
            left = (width - height) / 2
            top = 0
            right = left + height
            bottom = height
        else:
            left = 0
            top = (height - width) / 2
            right = width
            bottom = top + width

        # cropping + resizing
        image = image.crop((left, top, right, bottom))
        image = image.resize(target_size)

        # convert image back to bytes
        image_byte_array = io.BytesIO()
        image.save(image_byte_array, format='JPEG')  # saving as jpegs for now

        return image_byte_array.getvalue()

    except Exception as e:
        print(f"Error downloading and preprocessing image: {e}")
        return None
    
def upload_image_to_blob(bucket_name, blob_name, image_bytes, caption):
    '''
    upload image to a blob
    '''
    try:
        client = initialize_storage_client()

        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(f'posts/{blob_name}')

        # upload image from bytes
        blob.upload_from_string(image_bytes, content_type='image/jpeg') 

        blob = bucket.blob(f'captions/{blob_name}') # adjust content_type as needed
        blob.upload_from_string(caption, content_type='text/plain')

        print(f"Image '{blob_name}' uploaded to '{bucket_name}'")

    except Exception as e:
        print(f"Error uploading image: {e}")

def get_post_data_from_profiles(profile_list = ["mbinkowski56"]):
    
    """Gets the data for every post

    Args:
        profile_list (list, optional): _description_. Defaults to ["mbinkowski56"].

    Returns:
        processed_posts: a list of dictionaries containing the owner_username, mediaid, caption, post url, and photo
    """
    L = instaloader.Instaloader()

    # List of posts and post data
    processed_posts = []
    print(type(profile_list[0]))
    
    # Iterate through profiles in profile_list
    for profile_name in profile_list[:180]:
        
        # Get profile information
        profile = instaloader.Profile.from_username(L.context, profile_name)
        
        if not profile.is_private:
            print(profile_name)
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
                    if(i>10):
                        break
                else:  
                    print('Failed to retrieve the image data.')
        #else:
            #print('PRIVATE PROFILE')        
        # Return post data
    return processed_posts

if __name__ == "__main__":

    profiles = get_profile_list(['usernames_0.txt', 'usernames_1.txt', 'usernames_2.txt'])
    print("got profiles")
    posts = get_post_data_from_profiles(profiles)

    bucket_name = 'instacap-data'

    for post in posts:
        # testing on one of mike's ig posts for now
        blob_name = f'{post["owner_username"]}_{post["mediaid"]}'
        print(f'BLOOOB: {blob_name}')


        preprocessed_image = download_and_preprocess_image(bucket_name, blob_name, post['photo'])

        if preprocessed_image:
            upload_image_to_blob(bucket_name, blob_name, preprocessed_image, post['caption'])
            print('uploaded test!')
