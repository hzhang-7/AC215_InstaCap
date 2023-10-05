# script reads in images and captions uploaded to gcs and creates a dataset csv file to use for finetuning our model

from google.cloud import storage
import pandas as pd

def initialize_storage_client():
    '''
    initialize gcs client
    '''
    return storage.Client()

def get_image_caption_mapping(client, bucket_name, posts_folder, captions_folder):
    '''
    get image and caption mapping from gcs
    '''
    images_blobs = list(client.bucket(bucket_name).list_blobs(prefix=posts_folder))
    captions_blobs = list(client.bucket(bucket_name).list_blobs(prefix=captions_folder))

    # key: image filename, value: associated caption
    image_caption_mapping = {}

    for image_blob in images_blobs:
        image_file_name = image_blob.name.split('/')[-1]
        for caption_blob in captions_blobs:
            caption_blob_name = caption_blob.name.split('/')[-1]


            # the way that the image and caption data is in gcp is if the filenames are the
            # same, they correspond to the same post

            # here we are matching the two (filename and caption) to create a dictionary
            # of images and captions to later create a dataframe
            if caption_blob_name == image_file_name:
                caption_text = caption_blob.download_as_text()

                # making sure we're not putting in nothing into our dataset
                if image_file_name != '':
                    image_caption_mapping[image_file_name] = caption_text

    return image_caption_mapping

def upload_dataframe_to_gcs(client, bucket_name, dataframe, path_name):
    '''
    upload a pandas dataframe to gcs as a csv file
    '''
    csv_data = dataframe.to_csv(index=False)
    df_blob = client.bucket(bucket_name).blob(path_name)
    df_blob.upload_from_string(csv_data, content_type='text/csv')

if __name__ == "__main__":
    client = initialize_storage_client()
    bucket_name = 'instacap-data'
    posts_folder = 'posts/'
    captions_folder = 'captions/'

    image_caption_mapping = get_image_caption_mapping(client, bucket_name, posts_folder, captions_folder)
    dataset = pd.DataFrame.from_dict(image_caption_mapping, orient='index', columns=['caption'])
    dataset.index.name = 'image_file_name'
    dataset.reset_index(inplace=True)
    print(dataset.head())
    path_name = 'sample_dataset.csv'
    upload_dataframe_to_gcs(client, bucket_name, dataset, path_name)