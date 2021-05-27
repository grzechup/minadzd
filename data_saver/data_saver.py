import json
from pymongo import MongoClient
import os
import shutil
from datetime import date

# path to directory where scrapped JSON are stored
# TO CHANGE
path = 'C:/Users/haga/Documents/ZPI/job_offers/'

#client = MongoClient("localhost", 27017)
client = MongoClient("mongodb+srv://zpi_projekt:datascience@cluster0.hzchp.mongodb.net/test")

db = client["NoFluffJobs"]
collection = db["DataScience"]

directory_name = date.today().strftime("%Y/%m/%d")

# Creating new directory for today
if not os.path.exists(path + directory_name):
    os.makedirs(path + directory_name)

with os.scandir(path) as directory_content:
    for entry in directory_content:
        if entry.name.endswith('.json'):
            # Loading or Opening the json file
            with open(path + entry.name, 'r') as file:
                file_data = json.load(file)

            # Inserting or replacing the loaded data in the Collection
            key = {'id': file_data['id']}
            result = collection.replace_one(key, file_data, upsert=True)

            # Moving inserted file to directory for today
            shutil.move(path + '/' + entry.name, path + directory_name)
