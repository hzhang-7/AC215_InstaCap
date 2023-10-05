# modeling notebook --> script for job setup, all training code for our instacap model should be here 
import argparse
import os
import requests
import zipfile
import tarfile
import time
from google.colab import auth
from google.cloud import storage
import io
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import Input, LSTM, add, Dense, Concatenate
from tensorflow.keras.models import Model
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input as preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.python.keras import backend as K
import tensorflow_hub as hub
from transformers import BertTokenizer, BertModel
from transformers import AutoTokenizer
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
import requests
from PIL import Image
from datasets import Dataset, load_dataset
import time

# W&B
import wandb
from wandb.keras import WandbCallback, WandbMetricsLogger

# Setup the arguments for the trainer task
parser = argparse.ArgumentParser()
parser.add_argument(
    "--model-dir", dest="model_dir", default="test", type=str, help="Model dir."
)
parser.add_argument("--lr", dest="lr", default=0.001, type=float, help="Learning rate.")
parser.add_argument(
    "--model_name",
    dest="model_name",
    default="baseline",
    type=str,
    help="Model name",
)

parser.add_argument(
    "--epochs", dest="epochs", default=10, type=int, help="Number of epochs."
)
parser.add_argument(
    "--batch_size", dest="batch_size", default=16, type=int, help="Size of a batch."
)
parser.add_argument(
    "--wandb_key", dest="wandb_key", default="16", type=str, help="WandB API Key"
)
args = parser.parse_args()

# TF Version
print("tensorflow version", tf.__version__)
print("Eager Execution Enabled:", tf.executing_eagerly())
# Get the number of replicas
strategy = tf.distribute.MirroredStrategy()
print("Number of replicas:", strategy.num_replicas_in_sync)

devices = tf.config.experimental.get_visible_devices()
print("Devices:", devices)
print(tf.config.experimental.list_logical_devices("GPU"))

print("GPU Available: ", tf.config.list_physical_devices("GPU"))
print("All Physical Devices", tf.config.list_physical_devices())


# Utils functions
def download_file(packet_url, base_path="", extract=False, headers=None):
    if base_path != "":
        if not os.path.exists(base_path):
            os.mkdir(base_path)
    packet_file = os.path.basename(packet_url)
    with requests.get(packet_url, stream=True, headers=headers) as r:
        r.raise_for_status()
        with open(os.path.join(base_path, packet_file), "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    if extract:
        if packet_file.endswith(".zip"):
            with zipfile.ZipFile(os.path.join(base_path, packet_file)) as zfile:
                zfile.extractall(base_path)
        else:
            packet_name = packet_file.split(".")[0]
            with tarfile.open(os.path.join(base_path, packet_file)) as tfile:
                tfile.extractall(base_path)



def get_dataset(batch_size):
  def pull_data_from_gcs(project_id, bucket_name, credentials_file_path, data_file_path):

    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(data_file_path)

    csv_data = blob.download_as_text()

    df = pd.read_csv(io.StringIO(csv_data))

    return df, bucket

  def make_data_list(df, bucket):
    data_list = []

    for index, row in df.iterrows():
      image_filename = row['image_file_name'] 
      caption = row['caption']  

      # Get image blob and download image data from bucket
      image_blob = bucket.blob('posts/' + image_filename)
      image_data = image_blob.download_as_bytes()

      # Open image using PIL
      image = Image.open(io.BytesIO(image_data))

      # Create dictionary and append to the list
      data_dict = {
          'image': image,
          'caption': caption
      }
      data_list.append(data_dict)

    return data_list

  def get_blip_transcription(data_list, blip_model_name='Salesforce/blip-image-captioning-base'):
    blip_processor = BlipProcessor.from_pretrained(blip_model_name)
    blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    blip_preds = []
    for i, example in enumerate(data_list):
        image = example["image"]
        truth = example["caption"]
        inputs = blip_processor(images=image, return_tensors="pt")
        pixel_values = inputs.pixel_values
        generated_ids = blip_model.generate(
            pixel_values=pixel_values, max_length=50)
        generated_caption = blip_processor.batch_decode(
            generated_ids, skip_special_tokens=True)[0]
        blip_preds.append([image, truth, generated_caption])
    return blip_preds

  def get_raw_data(blip_preds):
    # seperate images, captions, blip transcriptions
    image_arrs = []  # image arrays (not PIL images)
    captions = []  # true captions
    transcriptions = []  # blip transcriptions
    for entry in blip_preds:
      # convert pil image to numpy array
      image_arrs.append(np.array(entry[0].resize((224, 224))))
      captions.append(entry[1])
      transcriptions.append(entry[2])

    return image_arrs, captions, transcriptions


  def extract_image_features(img_array, weights_name='imagenet'):
    # RESNET
    resnet_model = ResNet50(weights=weights_name, include_top=False, pooling='avg')
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    features = resnet_model.predict(img_array)
    return features

  def get_bert_embeddings(blip_transcriptions, bert_model_name='bert-base-uncased'):
    bert_model = BertModel.from_pretrained(bert_model_name)
    tokenizer = AutoTokenizer.from_pretrained(bert_model_name)

    inputs = tokenizer(blip_transcriptions, return_tensors='pt',padding=True, truncation=True, max_length=128)
    outputs = bert_model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)

    return embeddings

  def create_input_output_pairs(captions, image_features, transcription_embeddings):
    # Create a tokenizer and fit on the captions
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(captions)

    # Vocabulary size is the total number of unique words in your captions
    start = len(tokenizer.word_index) + 1
    stop = start + 1
    vocab_size = stop + 1

    # Convert captions to sequences of integer indices
    captions_sequences = tokenizer.texts_to_sequences(captions)

    # Insert start and stop sequences to the encoded caption size
    captions_sequences = [([start] + c) for c in captions_sequences]
    captions_sequences = [(c + [stop]) for c in captions_sequences]

    max_caption_length = max(len(c) for c in captions_sequences)

    # create input output pairs
    input_sequences = []
    output_sequences = []
    image_sequences = []
    transcription_sequences = []

    for j in range(len(captions_sequences)):
        caption_sequence = captions_sequences[j]
        for i in range(1, len(caption_sequence)):
            # Input sequence (words before the current word)
            input_seq = caption_sequence[:i]
            input_seq = pad_sequences([input_seq], max_caption_length)[0]
            # Output word (current word)
            output_word = caption_sequence[i]
            output_word = to_categorical(output_word, num_classes = vocab_size)
            input_sequences.append(input_seq)
            output_sequences.append(output_word)
            image_sequences.append(image_features[j])
            transcription_sequences.append(transcription_embeddings[j])

    input_sequences = np.array(input_sequences)
    input_sequences = np.expand_dims(input_sequences, axis = 1)
    output_sequences = np.array(output_sequences)
    image_sequences = np.reshape(image_sequences,(np.shape(image_sequences)[0], np.shape(image_sequences)[2]))
    transcription_sequences = np.reshape(transcription_sequences,(np.shape(transcription_sequences)[0], np.shape(transcription_sequences)[2]))

    return input_sequences, output_sequences, image_sequences, transcription_sequences, vocab_size, max_caption_length

  def get_train_test_split_datasets(n_posts, input_sequences, output_sequences, image_sequences, transcription_sequences, batch_size, train_ratio=0.8):
    # train test split
    train_size = int(train_ratio * n_posts)
    test_size = n_posts - train_size

    train_dataset = tf.data.Dataset.from_tensor_slices(((image_sequences[:train_size], transcription_sequences[:train_size],input_sequences[:train_size]), output_sequences[:train_size]))
    test_dataset = tf.data.Dataset.from_tensor_slices(((image_sequences[train_size:], transcription_sequences[train_size:], input_sequences[train_size:]), output_sequences[train_size:]))

    train_dataset = train_dataset.shuffle(buffer_size=train_size).batch(batch_size)
    test_dataset = test_dataset.batch(batch_size)

    return train_dataset, test_dataset


  df, bucket = pull_data_from_gcs(project_id = 'ac215-project-398320', bucket_name='instacap-data', credentials_file_path = 'data_service_account.json', data_file_path='sample_dataset.csv')
  data_list = make_data_list(df, bucket)
  blip_preds = get_blip_transcription(data_list)
  image_arrs, captions, transcriptions = get_raw_data(blip_preds)
  image_features = [extract_image_features(img) for img in image_arrs]
  transcription_embeddings = get_bert_embeddings(transcriptions)
  transcription_embeddings = np.expand_dims(transcription_embeddings.detach().numpy(), axis=1)
  input_sequences, output_sequences, image_sequences, transcription_sequences, vocab_size, max_caption_length = create_input_output_pairs(captions, image_features, transcription_embeddings)
  
  n_posts = len(data_list)
  
  train_dataset, test_dataset = get_train_test_split_datasets(n_posts, input_sequences, output_sequences, image_sequences, transcription_sequences, batch_size)
  input_image_dim = image_features[0].shape[1]
  input_embedding_dim = transcription_embeddings.shape[-1]
  return train_dataset, test_dataset, max_caption_length, vocab_size, input_image_dim, input_embedding_dim


def build_model(model_name, input_image_dim, input_embedding_dim, max_caption_length, vocab_size, n_units=256):
  # defining input layers:
  image_input = Input(shape=(input_image_dim), name='image_input')
  image_dense = Dense(n_units, activation='relu')(image_input)
  
  trans_embedding_input = Input(shape=(input_embedding_dim), name='text_embedding_input')
  trans_dense = Dense(n_units, activation = 'relu')(trans_embedding_input)

  word_input = Input(shape=(1, max_caption_length), name='word_input')
  lstm = LSTM(units=n_units, name='lstm')(word_input)

  # add all
  combined = add([image_dense, trans_dense, lstm])

  # decoder
  decoder = Dense(n_units, activation='relu')(combined)
  outputs = Dense(vocab_size, activation='softmax')(decoder)

  model = Model(inputs=[image_input, trans_embedding_input, word_input], outputs=outputs, name=model_name)

  return model


K.clear_session()
############################
# Training Params
############################
model_name = args.model_name
learning_rate = args.lr
batch_size = args.batch_size
epochs = args.epochs

# get data:
start_time = time.time()
train_data, test_data, max_caption_length, vocab_size, input_image_dim, input_embedding_dim = get_dataset(batch_size=batch_size)
data_execution_time = (time.time() - start_time) / 60.0
print(f'Data load time (mins): {data_execution_time}')

# wandb:
wandb.login(key=args.wandb_key)

model = build_model(model_name=model_name, input_image_dim=input_image_dim, input_embedding_dim=input_embedding_dim, max_caption_length=max_caption_length, vocab_size=vocab_size)

optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
loss = tf.keras.losses.categorical_crossentropy

print('MODEL SUMMARY:')
print(model.summary())

model.compile(loss=loss, optimizer=optimizer, metrics=['accuracy'])

# Initialize a W&B run
wandb.init(
    project = 'instacap-demo',
    config = {
      "learning_rate": learning_rate,
      "epochs": epochs,
      "batch_size": batch_size,
      "model_name": model.name
    },
    name = model.name
)

start_time = time.time()
training_results = model.fit(
        train_data,
        validation_data=test_data,
        epochs=epochs,
        callbacks=[WandbCallback()],
        #callbacks = [WandbMetricsLogger(log_freq=1)],
        verbose=1)
execution_time = (time.time() - start_time)/60.0
print("Training execution time (mins)",execution_time)

# Update W&B
wandb.config.update({"execution_time": execution_time})
# Close the W&B run
wandb.run.finish()

print('training job complete')