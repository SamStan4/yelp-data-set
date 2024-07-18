import json
from private.data_base_details import data_base_info
from private.data_base_details import file_paths
from data_base_interface import execute_insert
from data_base_interface import sql_clean_string

def get_attributes(attributes : dict) -> list:
    attribute_list = []
    for attribute, value in list(attributes.items()):
        if isinstance(value, dict):
            attribute_list += get_attributes(value)
        else:
            attribute_list.append((attribute, value))
    return attribute_list

def parse_yelp_business_file(file_path : str) -> None:
    try:
        input_stream = open(file_path, "r")
    except:
        print("ERROR -- parse_yelp_business_file --")
        return
    for input_item in input_stream:
        json_data = json.loads(input_item)
        business_id = sql_clean_string(str(json_data["business_id"]))
        business_name = sql_clean_string(str(json_data["name"]))
        business_city = sql_clean_string(str(json_data["city"]))
        business_zipcode = sql_clean_string(str(json_data["postal_code"]))
        business_address = sql_clean_string(str(json_data["address"]))
        business_stars = sql_clean_string(str(json_data["stars"]))
        business_state = sql_clean_string(str(json_data["state"]))
        business_attributes = get_attributes(json_data["attributes"])
        business_categories = json_data["categories"]
        sql_str = "INSERT INTO {} VALUES ('{}', '{}', '{}', '{}', '{}', '{}', {}, {}, {});".format(
            data_base_info.business_table_schema,
            business_id,
            business_name,
            business_city,
            business_state,
            business_zipcode,
            business_address,
            "0",
            "0",
            business_stars
        )
        execute_insert(sql_str)
        for attribute_value in business_attributes:
            attribute = sql_clean_string(str(attribute_value[0]))
            value = sql_clean_string(str(attribute_value[1]))
            sql_str = "INSERT INTO {} VALUES('{}', '{}', '{}')".format(
                data_base_info.attributes_table_schema,
                attribute,
                value,
                business_id
            )
            execute_insert(sql_str)
        for category in business_categories:
            category_clean = sql_clean_string(str(category))
            sql_str = "INSERT INTO {} VALUES ('{}', '{}');".format(
                data_base_info.categories_table_schema,
                category_clean,
                business_id
            )
            execute_insert(sql_str)
    input_stream.close()

def parse_reviews_file(file_path : str) -> None:
    try:
        input_stream = open(file_path, "r")
    except:
        print("ERROR -- parse_reviews_file() --")
        return
    for input_item in input_stream:
        json_data = json.loads(input_item)
        review_id = sql_clean_string(str(json_data["review_id"]))
        review_stars = sql_clean_string(str(json_data["stars"]))
        review_date = sql_clean_string(str(json_data["date"]))
        review_text = sql_clean_string(str(json_data["text"]))
        review_useful_vote = sql_clean_string(str(json_data["useful"]))
        review_funny_vote = sql_clean_string(str(json_data["funny"]))
        review_cool_vote = sql_clean_string(str(json_data["cool"]))
        business_id = sql_clean_string(str(json_data["business_id"]))
        sql_str = "INSERT INTO {} VALUES ('{}', {}, '{}', '{}', {}, {}, {}, '{}');".format(
            data_base_info.review_table_schema,
            review_id,
            review_stars,
            review_date,
            review_text,
            review_useful_vote,
            review_funny_vote,
            review_cool_vote,
            business_id
        )
        execute_insert(sql_str)
    input_stream.close()

def parse_check_in(file_path : str) -> None:
    try:
        input_stream = open(file_path, "r")
    except:
        print("ERROR -- parse_check_in() --")
        return
    for input_item in input_stream:
        json_data = json.loads(input_item)
        business_id = sql_clean_string(str(json_data["business_id"]))
        for check_in_day, check_in_time in json_data["time"].items():
            for hour, count in check_in_time.items():
                check_in_day_clean = sql_clean_string(str(check_in_day))
                check_in_time_clean = sql_clean_string(str(hour))
                sql_str = "INSERT INTO {} VALUES ('{}', '{}', {}, '{}')".format(
                    data_base_info.checkins_table_schema,
                    check_in_day_clean,
                    check_in_time_clean,
                    count,
                    business_id
                )
                execute_insert(sql_str)

def main() -> int:
    parse_yelp_business_file(file_path=file_paths.business_json_path)
    parse_reviews_file(file_path=file_paths.business_json_path)
    parse_check_in(file_path=file_paths.checkin_json_path)
    return 0

if __name__ == '__main__':
    main()