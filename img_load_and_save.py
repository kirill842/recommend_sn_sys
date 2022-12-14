import pandas as pd
import argparse
from PIL import Image
import requests
import config
from torchvision import transforms
import pickle
import shutil
from sklearn.model_selection import train_test_split


def load_images_from_url_and_save(database_connection_link: str, save_path: str):
    scraped_imgs_df = pd.read_sql('SELECT img_id, img_url FROM ' + config.TABLE_NAME, database_connection_link)
    for index, row in scraped_imgs_df.iterrows():
        img_id = int(row['img_id'])
        url = row.img_url
        img = Image.open(requests.get('http:' + url, stream=True).raw)
        img.crop((20, 170, 215, 310)).save(save_path + '/' + str(img_id) + '.jpg')


def convert_images_to_training_format_and_save(database_connection_link: str):
    scraped_data_df = pd.read_sql('SELECT img_id, target FROM ' + config.TABLE_NAME, database_connection_link)
    scraped_data_df_filtered = scraped_data_df.sort_values(by=['img_id'])
    scraped_data_df_filtered = scraped_data_df_filtered.sample(frac=1).reset_index(drop=True)
    train, test = train_test_split(scraped_data_df_filtered, test_size=0.2)
    for i, row in train.iterrows():
        target = row['target']
        img_id = int(row['img_id'])
        img = Image.open("./img_data_scraped_from_urls/all/" + str(img_id) + ".jpg")
        resize_img = transforms.Resize((224, 224))
        img_resized = resize_img(img)
        if target == 1:
            img_resized.save('./resized_imgs/train/good/' + str(img_id) + '.jpg')
        elif target == 0:
            img_resized.save('./resized_imgs/train/bad/' + str(img_id) + '.jpg')
        else:
            img_resized.save('./resized_imgs/not_labeled/' + str(img_id) + '.jpg')
    for i, row in test.iterrows():
        target = row['target']
        img_id = int(row['img_id'])
        img = Image.open("./img_data_scraped_from_urls/all/" + str(img_id) + ".jpg")
        resize_img = transforms.Resize((224, 224))
        img_resized = resize_img(img)
        if target == 1:
            img_resized.save('./resized_imgs/val/good/' + str(img_id) + '.jpg')
        elif target == 0:
            img_resized.save('./resized_imgs/val/bad/' + str(img_id) + '.jpg')
        else:
            img_resized.save('./resized_imgs/not_labeled/' + str(img_id) + '.jpg')


def move_new_labeled_imgs_to_proper_dirs(last_labeled_img_id: int, not_efficient_but_safe: bool):
    if not_efficient_but_safe:
        convert_images_to_training_format_and_save(config.DB_CONNECT_LINK)
    else:
        with open('./last_moved_img_id.pkl', 'rb') as file:
            last_moved_img_id = pickle.load(file)

        print('Moving images from', last_moved_img_id + 1, 'to', last_labeled_img_id)

        scraped_data_df = pd.read_sql('SELECT img_id, target FROM ' + config.TABLE_NAME, config.DB_CONNECT_LINK)

        i = 0
        for img_id in range(last_moved_img_id + 1, last_labeled_img_id + 1):
            # print(scraped_data_df[scraped_data_df['img_id'] == img_id])
            target = int(scraped_data_df[scraped_data_df['img_id'] == img_id]['target'])
            # print(target)
            assert (target == 0 or target == 1)
            if target == 1:
                if i == 4:
                    shutil.move('./resized_imgs/not_labeled/' + str(img_id) + '.jpg',
                                './resized_imgs/val/good/' + str(img_id) + '.jpg')
                    i = 0
                else:
                    shutil.move('./resized_imgs/not_labeled/' + str(img_id) + '.jpg',
                                './resized_imgs/train/good/' + str(img_id) + '.jpg')
            elif target == 0:
                if i == 4:
                    shutil.move('./resized_imgs/not_labeled/' + str(img_id) + '.jpg',
                                './resized_imgs/val/bad/' + str(img_id) + '.jpg')
                    i = 0
                else:
                    shutil.move('./resized_imgs/not_labeled/' + str(img_id) + '.jpg',
                                './resized_imgs/train/bad/' + str(img_id) + '.jpg')
            i += 1

        last_moved_img_id = last_labeled_img_id
        with open('./last_moved_img_id.pkl', 'wb') as file:
            # A new file will be created
            pickle.dump(last_moved_img_id, file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='write after .py -h for more info')

    parser.add_argument('--db_connect_link', type=str,
                        default=config.DB_CONNECT_LINK,
                        help='Connection link to database. Example: postgresql://login:password@ip:port/db_name')
    parser.add_argument('--save_path', type=str,
                        default='./img_data_scraped_from_urls/all',
                        help='Connection link to database. Example: postgresql://login:password@ip:port/db_name')

    args = parser.parse_args()

    load_images_from_url_and_save(config.DB_CONNECT_LINK, './img_data_scraped_from_urls/all')

    convert_images_to_training_format_and_save(config.DB_CONNECT_LINK)
