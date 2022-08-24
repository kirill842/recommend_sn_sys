# Intro
Once I went to a site with the purchase of things and thought, why not train a neural network that will recommend me those things that suit my taste? I chose sneakers as the main object of recommendation. My project consists of: 1) Scraping data from the site 2) Saving data via PostgreSQL 3) Data labeling 4) Training, Evaluation and Operation of the neural network 5) Interaction with the Telegram Bot API. For my project, I chose the Python language. For data scraping, I used BeautifulSoup and Selenium python libraries. To create a telegram bot, I used the Telegram Bot API. For training, evaluation and operation of my neural network, I used pytorch and timm. During the development of the project, I labeled about 1600 pictures through the telegram bot. Trained EfficientNetB0 on 300 epochs using this data. I taught the bot to take the output of the model to recommend sneakers, and as a result I got a telegram bot that really recommends only those sneakers that match my taste. I can even look at the price, brand name, model name and product link so I can immediately order the shoes I like!

# Motivation
The goal is to develop a bot that is interesting to watch. The behavior of the bot should not differ from the behavior of a person in similar situations. Our research will help raise the level of AI in games, make games more interesting, and bots in them more similar to the actions of a real person.

We assume that if people are interested in watching other gamers (professional or not) through [twitch](https://www.twitch.tv/), then they will be interested in watching our agent as well. 

# Technical stack

![image](https://user-images.githubusercontent.com/45121687/135727643-7ea3c139-fa97-47fa-801f-f48e01d524c0.png)

- offline reinforcement learning
- python3
- selenium *(agent actions execution in game environment)*
- openCV *(screenshots processing)*
- torch *(action selection)*
- mss *(do screenshots)*


# Installation guide

<details>
  <summary>Source</summary>
  
  ## Initial usage
  __1. Clone GitHub repository__
  
  ```
  git clone https://github.com/kirill842/recommend_sn_sys
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
  create table scraped_imgs_with_info(
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
  python web_crawler.py
  python img_load_and_save.py
  python bot_controller.py
  ```
  __7. Find your bot on telegram and use__
  
</details>

<details>
  <summary>Docker(Experimental)</summary>
  
  ## Initial usage
  __1. Install Docker Desktop__

  https://www.docker.com/products/docker-desktop/

  __2. Install nvidia-docker__
  
  https://github.com/NVIDIA/nvidia-docker
  
  __3. Clone GitHub repository__
  
  ```
  git clone https://github.com/kirill842/recommend_sn_sys
  ```
  
  __4. Build docker image and create docker container using my docker files__
  
  __5. Run this command to run container with gpu__
  ```
  docker run --name my_all_gpu_container --gpus all -t nvidia/cuda
  ```

</details>
