import time
import telebot
from telebot import types
import pickle
import pandas as pd
import os

import config
import img_load_and_save
import postgres_connection
import web_crawler

TOKEN = config.BOT_TOKEN
marking_stage = False


def increment_next_marking_img_id():
    global next_marking_img_id
    next_marking_img_id += 1
    # Open a file and use dump()
    with open('./next_marking_img_id.pkl', 'wb') as file:
        # A new file will be created
        pickle.dump(next_marking_img_id, file)


def send_next_image(message):
    img_index_to_mark = next_marking_img_id
    image = open('./img_data_scraped_from_urls/all' + '/' + str(img_index_to_mark) + '.jpg', 'rb')
    bot.send_photo(message.chat.id, image)


# Loading last index to mark
with open('./next_marking_img_id.pkl', 'rb') as file:
    next_marking_img_id = pickle.load(file)
    print('Last saved next marking index:', next_marking_img_id)


with open('./already_recommended_img_ids.pkl', 'rb') as file:
    already_recommended_img_ids = pickle.load(file)
    print('Already recommended sneakers:', already_recommended_img_ids)


with open('./is_model_up_to_date.pkl', 'rb') as file:
    is_model_up_to_date = pickle.load(file)
    print('Is the model trained on new data?', is_model_up_to_date)

with open('./first_launch.pkl', 'rb') as file:
    first_launch = pickle.load(file)

if first_launch is True:
    print('It is first launch, we will scrape', config.NUM_OF_PAGES_TO_SCRAP, 'pag. and fill directories for train and inference scripts')
    web_crawler.scrap_site_and_update_database()
    img_load_and_save.load_images_from_url_and_save(config.DB_CONNECT_LINK, './img_data_scraped_from_urls/all')
    print('All images were loaded')
    img_load_and_save.convert_images_to_training_format_and_save(config.DB_CONNECT_LINK)
    print('All images were transformed ')
    with open('./first_launch.pkl', 'wb') as file:
        # A new file will be created
        pickle.dump(False, file)
else:
    print('It is not first launch')

bot = telebot.TeleBot(TOKEN)

print('Bot is ready, go to telegram')


@bot.message_handler(commands=['start'])
def welcome(message):
    global is_model_up_to_date
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Data tagging mode')
    item2 = types.KeyboardButton('New selection of sneakers')
    item3 = types.KeyboardButton('Train the model on new data')
    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id, 'The bot has 2 functions: data markup mode and selection of sneakers based on the users taste', parse_mode='html',
                     reply_markup=markup)

    if not is_model_up_to_date:
        bot.send_message(message.chat.id, 'Perhaps the model is outdated, click "Train the model on new data" if you want to train the model on new data', parse_mode='html',
                         reply_markup=markup)


@bot.message_handler(content_types=['text'])
def text(message):
    global marking_stage
    global next_marking_img_id
    global is_model_up_to_date
    global already_recommended_img_ids
    if message.chat.type == 'private':  # and message.chat.username == 'kirill_lekanov':
        if message.text == 'Data tagging mode' and marking_stage is False:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('I like it')
            item2 = types.KeyboardButton('Naah')
            item3 = types.KeyboardButton('Back')
            markup.add(item1, item2, item3)

            bot.send_message(message.chat.id, 'The bot has switched to markup mode: Click "I like it" if you like the sneakers and "Naah" if you dont like the sneakers',
                             parse_mode='html', reply_markup=markup)

            send_next_image(message)
            marking_stage = True
        elif message.text == 'New selection of sneakers' and marking_stage is False:
            column_names = ['img_id_jpg', 'target']
            predictions_loaded = False
            try:
                output = pd.read_csv('topk_ids.csv', names=column_names)
                predictions_loaded = True
            except Exception as error:
                print(error)
                bot.send_message(message.chat.id, 'The bot did not find the output of the model, first label the data and train the model', parse_mode='html')
                exit()
            if predictions_loaded:
                good_output = output[output['target'] == 1]
                img_ids_jpg = good_output['img_id_jpg'].tolist()
                good_output['img_id'] = [img_id_jpg[:-4] for img_id_jpg in img_ids_jpg]
                mask = []
                for i, row in good_output.iterrows():
                    if int(row['img_id']) not in already_recommended_img_ids:
                        mask.append(True)
                    else:
                        mask.append(False)
                good_output = good_output[mask]
                scraped_imgs_df = pd.read_sql(
                    'SELECT img_id, img_url, product_url, brand_name, product_name, price FROM ' + config.TABLE_NAME,
                    config.DB_CONNECT_LINK
                )
                i = 0
                for index, row in good_output.iterrows():
                    if i == 5:
                        break
                    img_id = int(row['img_id'])
                    already_recommended_img_ids.append(img_id)
                    image = open('./img_data_scraped_from_urls/all' + '/' + str(img_id) + '.jpg', 'rb')
                    caption = ''
                    single_product = scraped_imgs_df[scraped_imgs_df['img_id'] == img_id]
                    caption += str(single_product['brand_name'].values[0]) + ' ' + str(single_product['product_name'].values[0]) + '\n'
                    caption += 'Price: ' + str(single_product['price'].values[0]) + '\n'
                    caption += 'Product Link: ' + str(single_product['product_url'].values[0])
                    time.sleep(1)
                    bot.send_photo(message.chat.id, image, caption=caption)
                    i += 1
                with open('./already_recommended_img_ids.pkl', 'wb') as file:
                    pickle.dump(already_recommended_img_ids, file)
        elif message.text == 'I like it' and marking_stage is True:
            postgres_connection.mark_image_by_index(1, next_marking_img_id)
            increment_next_marking_img_id()
            send_next_image(message)
        elif message.text == 'Train the model on new data' and marking_stage is False and (not is_model_up_to_date):
            print('Training stage')
            bot.send_message(message.chat.id, 'Wait for the bot to finish training',
                             parse_mode='html')
            return_code = os.system('python pytorch-image-models/train.py ./resized_imgs --train-split train --val-split val --model efficientnet_b0 --pretrained --num-classes 2 --input-size 3 224 224 -b 16 --epochs 40 --no-aug --output ./trained_models')
            if return_code == 0:
                print('Model was trained successfully')
                bot.send_message(message.chat.id, 'Training completed successfully! Now wait for the model to predict recommendations',
                                 parse_mode='html')
                with open('./is_model_up_to_date.pkl', 'wb') as file:
                    pickle.dump(True, file)
                is_model_up_to_date = True
            else:
                print('Model wasnt trained, check error above. Possible solution might be to label more data')
                bot.send_message(message.chat.id,
                                 'Training was not completed successfully, check the error log',
                                 parse_mode='html')

            def find_all(name, path):
                result = []
                for root, dirs, files in os.walk(path):
                    if name in files:
                        result.append(os.path.join(root, name))
                return result

            all_matches = find_all('model_best.pth.tar', './trained_models')
            if len(all_matches) == 1:
                print('Bot didnt find any new trained models. Loading trained model by me')
            path_to_best_model = all_matches[len(all_matches) - 1]
            return_code = os.system('python pytorch-image-models/inference.py ./resized_imgs/not_labeled --model efficientnet_b0 --num-classes 2 --topk 1 --checkpoint ' + path_to_best_model + ' --input-size 3 224 224 -b 32 --interpolation bicubic')
            if return_code == 0:
                bot.send_message(message.chat.id,
                                 'The model predicted recommendations',
                                 parse_mode='html')
                print('Model output was saved')
            else:
                bot.send_message(message.chat.id,
                                 'The model did not predict recommendations, look at the error log',
                                 parse_mode='html')
                print('Model didnt send output, check error above')
        elif message.text == 'Train the model on new data' and marking_stage is False and is_model_up_to_date:
            bot.send_message(message.chat.id, 'The model is already trained on the new data',
                             parse_mode='html')
        elif message.text == 'Naah' and marking_stage is True:
            postgres_connection.mark_image_by_index(0, next_marking_img_id)
            increment_next_marking_img_id()
            send_next_image(message)
        elif message.text == 'I like it' and marking_stage is False:
            print('Error! Please try later')
        elif message.text == 'Naah' and marking_stage is False:
            print('Error! Please try later')
        elif message.text == 'Back' and marking_stage is True:
            with open('./is_model_up_to_date.pkl', 'wb') as file:
                pickle.dump(False, file)
            is_model_up_to_date = False
            marking_stage = False
            last_labeled_img_id = next_marking_img_id - 1
            bot.send_message(message.chat.id, 'The bot saves new data, depending on the amount of data it may take different time, wait for "Done" from the bot', parse_mode='html')
            img_load_and_save.move_new_labeled_imgs_to_proper_dirs(last_labeled_img_id, not_efficient_but_safe=False)
            bot.send_message(message.chat.id,
                             'Done',
                             parse_mode='html')
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Data tagging mode')
            item2 = types.KeyboardButton('New selection of sneakers')
            item3 = types.KeyboardButton('Train the model on new data')
            markup.add(item1, item2, item3)
            bot.send_message(message.chat.id, 'The bot has 2 functions: data markup mode and selection of sneakers based on the users taste', parse_mode='html',
                             reply_markup=markup)
            if not is_model_up_to_date:
                bot.send_message(message.chat.id,
                                 'Perhaps the model is outdated, click "Train the model on new data" if you want to train the model on new data',
                                 parse_mode='html',
                                 reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Error! Try later')


bot.polling(none_stop=True)
