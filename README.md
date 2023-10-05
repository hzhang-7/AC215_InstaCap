# AC215 Project: InstaCap

**Team Members**: \
Isha Vaish (ishavaish@g.harvard.edu), Danhee Kim (sharonkim@g.harvard.edu), Annabel Yim (annabelyim@g.harvard.edu), Haoran Zhang (haoran_zhang@g.harvard.edu), Mike Binkowski (mbinkowski@college.harvard.edu)

**Project**: \
The goal of this project is to develop an application for Instagram caption generation. A user can upload a post they would like to caption along with a tone (e.g. quirky, funny, serious, happy, etc) for the caption.  
  
A brief outline of our project is given below (subject to change).
1. Web-scrape Instagram posts and the corresponding captions from public accounts.
2. Preprocess the scraped data into a ready-to-use data set for modeling containing the processed posts and captions. 
3. Fine-tune the BLIP model on our dataset as a means of transfer learning. 
4. Create the modeling pipeline: given user input of a photo and tone, use the fine-tuned BLIP model to predict the caption and then feed the BLIP caption and tone as an engineered prompt into GPT-3 to return the final generated caption.
5. Create frontend and deploy the model.

## Milestone 2

The current structure of our repo is given below.

Project Organization
------------
      ├── LICENSE
      ├── README.md
      ├── notebooks
      ├── references
      └── src
            ├── persistant-folder
            ├── secrets
            ├── preprocessing
                ├── Dockerfile
                ├── docker-shell.sh
                ├── Pipfile
                ├── Pipfile.lock
                ├── Preprocess.py
                └── test_bucket_access.py
            
--------
Note: The `persistant-folder` and `secrets` are folders that are in the local directory (not pushed to GitHub). The `notebooks` folder contains code that is not part of any containers (e.g. EDA, reports, etc) and the `references` folder contains references.

For each component of our project pipeline, we will have a seperate folder (under `src`) with a similar set-up as the `preprocessing` folder (i.e. set up for its own docker container and virtual environment). For Milestone 2, we have set up the structure for our first component in the pipeline: `preprocessing`. We will set up the remaining components as we go through the project. An outline of the proposed (subject to change) components is given below.

- `preprocessing`: data collection (i.e. web scraping of instagram posts and captions) and data preprocessing (i.e. getting the data ready for modeling)
- `blip`: fine-tuning the BLIP model
- `caption-generation`: caption generation modeling pipeline (BLIP + GPT3)
- `frontend`: frontend component

A description of our `preprocessing` container is given below.

### Preprocessing

**Container Overview**:
- Web-scrapes instagram posts and captions for different users
- Preprocesses the scraped data into the desired format
- Stores the processed data to GCP
- Input to this container is source and destination is the GCS location
- Output from this container stored at the GCS location
- `secrets` folder is needed with the Google Application Credentials json stored inside
- `persistent-folder` is a temporary folder used to verify access to the GCP bucket

**Container Files**:
1. `src/preprocessing/Dockerfile` - This dockerfile sets up a Docker container for a python application. It uses the official Debian-hosted Python 3.8 image as a base, defines the python environment variables, updates the package manager, upgrades installed packages, installs neccessary dependencies, creates non-root user named "app" for running the application, sets the working directory to "/app" and switches to the "app" user, creates the pipenv virtual environment with the neccessary packages installed, copies the application source code into the container, and activates the pipenv environment.
2. `src/preprocessing/docker-shell.sh` - This shell file is used to build a docker container with the image name "web-scraper" using the dockerfile mentioned above. It sets the environment variables for GCP configuration and runs the docker container.
3. `src/preprocessing/Pipfile` - This file describes the packages we would like to install in our virtual environment.
4. `src/preprocessing/Pipfile.lock` - This is a file created by pipenv for dependency version locking and reproducibility. 
5. `src/preprocessing/test_bucket_access.py` - This is a sample python script for testing access to the GCP bucket. If it works, running `python test_bucket_access.py` should upload a  `test_bucket_access.txt` file into the `persistent-folder` stored locally. To run this script, use the command `python test_bucket_access.py`.
6. `preprocess.py` - This is the base script for data preprocessing that we will build upon in future milestones. Currently, it pulls an image from the posts of the accounts we have found, center crops it, and resizes it to 256 $\times$ 256 pixels, then uploads it to the GCP bucket along with the post's caption. To run this script, use the command `python preprocess.py`. 

**How to run the Docker Container**:
1. Clone this repo
2. `cd` into `src/preprocessing`
3. Run `sh docker-shell.sh`
