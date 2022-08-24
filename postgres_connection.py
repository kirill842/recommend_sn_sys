import pandas as pd
import sqlalchemy
import psycopg2
import config


def append_scraped_data_to_postgres_database(scraped_data: dict, database_connection_link: str):
    df_from_sql = pd.read_sql('SELECT img_url, product_url FROM ' + config.table_name, database_connection_link)

    # # print duplicates if they exist
    # grouped = df_from_sql.groupby(df_from_sql.columns.tolist(), as_index=False).size()
    # duplicates = grouped[grouped['size'] != 1]
    #
    # if len(duplicates.index) != 0:
    #     raise Exception('Remove duplicates from database!')
    # else:
    #     print('No duplicates in sql database')

    # drop duplicates and select only new img links, that are not in our database already
    scraped_data_df = pd.DataFrame({'img_url': scraped_data['image_urls'],
                                    'product_url': scraped_data['product_urls'],
                                    'brand_name': scraped_data['brand_names'],
                                    'product_name': scraped_data['product_names'],
                                    'price': scraped_data['prices']})
    scraped_data_df.drop_duplicates(subset='img_url', inplace=True)
    scraped_data_df.drop_duplicates(subset='product_url', inplace=True)
    scraped_data_df = pd.merge(scraped_data_df, df_from_sql, on=["img_url"], how='outer', indicator=True)
    scraped_data_df = scraped_data_df.loc[scraped_data_df["_merge"] == "left_only"].drop(["_merge", 'product_url_y'], axis=1)
    scraped_data_df.rename(columns={'product_url_x': 'product_url'}, inplace=True)
    scraped_data_df = pd.merge(scraped_data_df, df_from_sql, on=["product_url"], how='outer', indicator=True)
    scraped_data_df = scraped_data_df.loc[scraped_data_df["_merge"] == "left_only"].drop(["_merge", 'img_url_y'], axis=1)
    scraped_data_df.rename(columns={'img_url_x': 'img_url'}, inplace=True)
    # push img links to database
    try:
        engine = sqlalchemy.create_engine(database_connection_link)
        scraped_data_df.to_sql('scraped_imgs_with_info', con=engine, if_exists='append', index=False)
    except Exception as e:
        print('Page wasnt pushed to sql')
        print(e)


def get_pandas_df_from_sql(database_connection_link: str) -> pd.DataFrame:
    scraped_imgs_df = pd.read_sql('SELECT img_url, product_url, brand_name, product_name, price FROM ' + config.table_name,
                                  database_connection_link)
    return scraped_imgs_df


def mark_image_by_index(mark: int, img_id: int):
    # engine = sqlalchemy.create_engine(config.db_connect_link)
    try:
        connection = psycopg2.connect(user=config.user,
                                      password=config.password,
                                      host=config.host,
                                      port=config.port,
                                      database=config.database)
        cursor = connection.cursor()
        # Update single record now
        sql_update_query = 'UPDATE ' + config.table_name + ' SET target = %s WHERE img_id = %s;'
        cursor.execute(sql_update_query, (mark, img_id))
        connection.commit()
        count = cursor.rowcount
        print(count, "Record Updated successfully ")
    except (Exception, psycopg2.Error) as error:
        print("Error in update operation", error)
    finally:
        # closing database connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

