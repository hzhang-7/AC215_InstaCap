# preprocess.py

from google.cloud import storage
from PIL import Image
import io

def initialize_storage_client():
    '''
    initialize google cloud storage client
    '''
    return storage.Client()

def download_and_preprocess_image(bucket_name, blob_name, target_size=(256, 256)):
    '''
    download and preprocess an image by doing a central crop to make an image 256x256 pixels
    '''
    try:
        client = initialize_storage_client()

        # get reference to the bucket and blob
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)

        # download image as bytes and get via pillow
        image_bytes = blob.download_as_bytes()
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
    
def upload_image_to_blob(bucket_name, blob_name, image_bytes):
    '''
    upload image to a blob
    '''
    try:
        client = initialize_storage_client()

        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)

        # upload image from bytes
        blob.upload_from_string(image_bytes, content_type='image/jpeg')  # adjust content_type as needed

        print(f"Image '{blob_name}' uploaded to '{bucket_name}'")

    except Exception as e:
        print(f"Error uploading image: {e}")

if __name__ == "__main__":
    bucket_name = 'instacap-data'

    # testing on one of mike's ig posts for now
    blob_name = 'posts/2016-10-29_13-06-27_UTC.jpg'

    preprocessed_image = download_and_preprocess_image(bucket_name, blob_name)

    if preprocessed_image:
        upload_image_to_blob(bucket_name, blob_name, preprocessed_image)
        print('uploaded test!')
