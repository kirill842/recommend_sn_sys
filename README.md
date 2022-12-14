<div align="center">
  
[![os](https://img.shields.io/badge/Linux-passing-success)]()
[![os](https://img.shields.io/badge/MacOS-passing-success)]()
[![os](https://img.shields.io/badge/Windows-passing-success)]()

![3 1](https://user-images.githubusercontent.com/37930588/186759420-f48163c6-0a6d-4b2b-bfe7-66727b8d8e7d.PNG)
![3 2](https://user-images.githubusercontent.com/37930588/186759426-f4f6f8c1-2f75-43ec-8f29-50afc80791b6.PNG)
![3 3](https://user-images.githubusercontent.com/37930588/186759432-893f18fb-9127-48d4-bdfe-8259456acd2f.PNG)
![3 4](https://user-images.githubusercontent.com/37930588/186759441-6e1b75d8-bde2-4202-8851-9c410372ff9a.PNG)

</div>

This project uses files train.py, inference.py and timm folder from https://github.com/rwightman/pytorch-image-models

# About
Once I went to a site with the purchase of things and thought, why not train a neural network that will recommend me those things that suit my taste? I chose sneakers as the main object of recommendation. My project consists of: 1) Scraping data from the site 2) Saving data via PostgreSQL 3) Data labeling 4) Training, Evaluation and Operation of the neural network 5) Interaction with the Telegram Bot API. For my project, I chose the Python language. For data scraping, I used BeautifulSoup and Selenium python libraries. To create a telegram bot, I used Telegram Bot API. For training, evaluation and operation of my neural network, I used pytorch and timm. During the development of the project, I labeled about 1600 pictures through the telegram bot. Trained EfficientNetB0 on 300 epochs using this data. I taught the bot to take the output of the model to recommend sneakers, and as a result I got a telegram bot that really recommends only those sneakers that match my taste. I can even look at the price, brand name, model name and product link so I can immediately order the shoes I like!

# Technical stack

- image classification
- python3
- selenium
- beautifulsoup
- argparse
- sqlalchemy
- psycopg2
- pandas
- pillow
- telegramBotAPI
- pytorch
- postgresql
- timm


# Installation guide

<details>
  <summary>Source</summary>
  
  ## Initial usage
  __0. Install python, nvidia drivers and pytorch with CUDA__
  
  https://www.nvidia.com/download/index.aspx
  
  https://www.python.org/downloads/
  
  https://pytorch.org/get-started/locally/
  
  example of installation: conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia
  
  __1.1. Clone GitHub repository__
  
  ```
  git clone --recurse-submodules https://github.com/kirill842/recommend_sn_sys
  ```
  
  __1.2. Install requirements__
 
  ```
  cd <repo location>
  pip install -r requirements.txt
  ```

  __2. Install Chrome and download chromedriver__

  1. https://www.google.com/chrome/
  2. https://chromedriver.chromium.org/downloads
  
  __3. PostgreSQL__
  
  You will need PostgreSQL database to use this project
  1. Use these links to install PostgreSQL
  
  https://www.postgresql.org/download/
  
  https://www.pgadmin.org/
  
  2. Run this command in pgAdmin4 to create table
  ```
  create table <your_table_name>(
    img_id serial PRIMARY KEY,
    img_url VARCHAR(255) UNIQUE NOT NULL,
    product_url VARCHAR(255) UNIQUE NOT NULL,
    brand_name VARCHAR(255) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    price integer NOT NULL,
    target integer
  );
  ```

  __4. Get your bot telegram token from BotFather__
  
  https://core.telegram.org/bots/
  
  __5. Fill config.yaml file__
  
  __6. Run scripts__

  ```
  cd <repo location>
  python setup.py
  python bot_controller.py
  ```
  __7. Find your bot on telegram and use__
  
</details>

<details>
  <summary>Docker (Experimental but should be fine)</summary>
  
  ## Initial usage
  __1. Install Docker Desktop__

  https://www.docker.com/products/docker-desktop/

  __2. Install nvidia-docker__
  
  https://github.com/NVIDIA/nvidia-docker
  
  __3. PostgreSQL__
  
  You will need PostgreSQL database to use this project
  1. Use these links to install PostgreSQL
  
  https://www.postgresql.org/download/
  
  https://www.pgadmin.org/
  
  2. Run this command in pgAdmin4 to create table
  ```
  create table <your_table_name>(
    img_id serial PRIMARY KEY,
    img_url VARCHAR(255) UNIQUE NOT NULL,
    product_url VARCHAR(255) UNIQUE NOT NULL,
    brand_name VARCHAR(255) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    price integer NOT NULL,
    target integer
  );
  ```
  
  __4. Get your bot telegram token from BotFather__
  
  https://core.telegram.org/bots/
  
  __5. Create and fill docker_env_vars.txt. Template:__
  
  ```
  NUM_OF_PAGES_TO_SCRAP=20
  SCROLL_PAUSE_TIME=0.2
  BOT_TOKEN=<your bot telegram token>
  DB_CONNECT_LINK=postgresql://<user>:<password>@<ip>:<port>/<db_name>
  URL_TO_SCRAP=https://www.lamoda.ru/c/5971/shoes-muzhkrossovki
  TABLE_NAME=<database_table_name>
  USER=<database_user>
  PASSWORD=<database_password>
  HOST=<database_ip>
  PORT=<database_port>
  DATABASE=<db_name>
  ```
  
  __6. Use my docker image__
  
  https://hub.docker.com/repository/docker/kirprogfrog/my-repository
  
  IMPORTANT! Make sure you are in the directory where your docker_env_vars.txt file is!
  
  initial usage
  ```
  cd <where your docker_env_vars.txt file is>
  docker pull kirprogfrog/my-repository
  docker run -ti --name <container_name> --env-file docker_env_vars.txt --gpus all kirprogfrog/my-repository
  ```
  if docker container was stopped
  ```
  docker start -i <container_id>
  ```
  
  __7. Go to your telegram bot and use__

</details>

# Usage
  
https://user-images.githubusercontent.com/37930588/186913241-01f79f33-2588-4057-ab7c-d63e3ce7a3e0.mp4
