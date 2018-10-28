import json

file_name = 'data.json'

data = {}


def add_user(userID):
        data[userID] = []


def add_dict_data(userID, data_dict):
        data[userID].append(data_dict)


def add_list_data(userID, data_list):
        # Data list should be like this [{'id': '2', 'title': 'title', 'summary': 'summ', 'rating': 1}, ...]
        data[userID] = data[userID] + data_list


def get_data():
        return json.dumps(data)


def write_to_disk():
        with open(file=file_name, mode='w') as outfile:
            json.dump(data, outfile)


def get_user_data(userID):
        with open(file=file_name, mode='r') as infile:
            file_data = json.load(infile)
            return file_data[userID]


def read_from_file():
    try:
        with open(file=file_name) as infile:
            try:
                stuff = json.load(infile)
            except ValueError:
                print('file is empty')
                stuff = []
            return stuff
    except FileNotFoundError:
        with open(file=file_name, mode="w+") as outfile:
            json.dump([], outfile)


def user_in_dict_yet(userID):
    read_from_file()
    if userID in data:
        print('yes')
        return True



