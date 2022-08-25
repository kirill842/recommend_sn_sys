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

# # use it to create yaml file
# next_marking_img_id = 1
# with open('next_marking_img_id.pkl', 'wb') as file:
#     # A new file will be created
#     pickle.dump(next_marking_img_id, file)
#
# exit()


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
    print('Уже зарекомендованные кроссовки:', already_recommended_img_ids)


with open('./is_model_up_to_date.pkl', 'rb') as file:
    is_model_up_to_date = pickle.load(file)
    print('Модель обучена на новых данных?', is_model_up_to_date)

with open('./first_launch.pkl', 'rb') as file:
    first_launch = pickle.load(file)

if first_launch is True:
    web_crawler.scrap_site_and_update_database()
    img_load_and_save.load_images_from_url_and_save(config.DB_CONNECT_LINK, './img_data_scraped_from_urls/all')
    img_load_and_save.convert_images_to_training_format_and_save(config.DB_CONNECT_LINK)
    with open('./first_launch.pkl', 'wb') as file:
        # A new file will be created
        pickle.dump(False, file)

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    global is_model_up_to_date
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Режим разметки данных')
    item2 = types.KeyboardButton('Новый подбор кроссовок')
    item3 = types.KeyboardButton('Обучить модель на новых данных')
    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id, 'У бота есть 2 функции: Режим разметки данных и Подбор' +
                     ' кроссовок основываясь на вкусе пользователя', parse_mode='html',
                     reply_markup=markup)

    if not is_model_up_to_date:
        bot.send_message(message.chat.id, 'Возможно модель устарела, нажмите "Обучить модель на новых данных", если хотите обучить модель на новых данных', parse_mode='html',
                         reply_markup=markup)


@bot.message_handler(content_types=['text'])
def text(message):
    global marking_stage
    global next_marking_img_id
    global is_model_up_to_date
    global already_recommended_img_ids
    if message.chat.type == 'private' and message.chat.username == 'kirill_lekanov':
        if message.text == 'Режим разметки данных' and marking_stage is False:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('I like it')
            item2 = types.KeyboardButton('Naah')
            item3 = types.KeyboardButton('Back')
            markup.add(item1, item2, item3)

            bot.send_message(message.chat.id, 'Бот перешёл в режим разметки: Нажимайте "I like it", ' +
                                              'если вам нравятся кроссовки и "Naah", если кроссовки не нравятся',
                             parse_mode='html', reply_markup=markup)

            send_next_image(message)
            marking_stage = True
        elif message.text == 'Новый подбор кроссовок' and marking_stage is False:
            column_names = ['img_id_jpg', 'target']
            try:
                output = pd.read_csv('topk_ids.csv', names=column_names)
            except Exception as error:
                print(error)
                exit()
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
                caption += 'Цена: ' + str(single_product['price'].values[0]) + '\n'
                caption += 'Ссылка на продукт: ' + str(single_product['product_url'].values[0])
                time.sleep(1)
                bot.send_photo(message.chat.id, image, caption=caption)
                i += 1
            with open('./already_recommended_img_ids.pkl', 'wb') as file:
                pickle.dump(already_recommended_img_ids, file)
        elif message.text == 'I like it' and marking_stage is True:
            postgres_connection.mark_image_by_index(1, next_marking_img_id)
            increment_next_marking_img_id()
            send_next_image(message)
        elif message.text == 'Обучить модель на новых данных' and marking_stage is False and (not is_model_up_to_date):
            print('Обучаем')
            os.system('python train.py ./resized_imgs --train-split train --val-split val --model efficientnet_b0 --pretrained --num-classes 2 --input-size 3 224 224 -b 32 --epochs 100 --no-aug --output ./trained_models')
            # todo implement loading newer trained model and using percentage as an output

            def find_all(name, path):
                result = []
                for root, dirs, files in os.walk(path):
                    if name in files:
                        result.append(os.path.join(root, name))
                return result

            all_matches = find_all('model_best.pth.tar', './trained_models')
            path_to_best_model = all_matches[len(all_matches) - 1]
            os.system('python inference.py ./resized_imgs/not_labeled --model efficientnet_b0 --num-classes 2 --topk 1 --checkpoint ' + path_to_best_model + ' --input-size 3 224 224 -b 32 --interpolation bicubic')
            with open('./is_model_up_to_date.pkl', 'wb') as file:
                pickle.dump(True, file)
            is_model_up_to_date = True
        elif message.text == 'Обучить модель на новых данных' and marking_stage is False and is_model_up_to_date:
            bot.send_message(message.chat.id, 'Модель уже обучена на новых данных',
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
            bot.send_message(message.chat.id, 'Бот сохраняет новые данные, в зависимости от количества данных это может занять разное время', parse_mode='html')
            img_load_and_save.move_new_labeled_imgs_to_proper_dirs(last_labeled_img_id, not_efficient_but_safe=True)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Режим разметки данных')
            item2 = types.KeyboardButton('Новый подбор кроссовок')
            item3 = types.KeyboardButton('Обучить модель на новых данных')
            markup.add(item1, item2, item3)
            bot.send_message(message.chat.id, 'У бота есть 2 главных функции: Режим разметки данных и Подбор' +
                             ' кроссовок основываясь на вкусе пользователя', parse_mode='html',
                             reply_markup=markup)
            if not is_model_up_to_date:
                bot.send_message(message.chat.id,
                                 'Возможно модель устарела, нажмите "Обучить модель на новых данных", если хотите обучить модель на новых данных',
                                 parse_mode='html',
                                 reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Бот на время закрыт для неприватных чатов и для недоверенных лиц')


bot.polling(none_stop=True)
