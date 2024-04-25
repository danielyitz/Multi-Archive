from Item import Item
import pickle
import json
import numpy as np
import pandas as pd
from Label import Label
import typing
from global_var import *
from external_functions import *


class Archive:
    def __init__(self):
        self.items: list[Item] = []
        self.next_free_id = 1
        self.labels = {}  # can be a dictionary with the label.name as the key and the label object as the value
        self.archive_thumbnails_path = ARCHIVE_THUMBNAILS_PATH
        self.num_of_backups = NUM_OF_BACKUPS
        self.last_back_up_index = 1

    def add_new_item(self, name, date, dest_path, name_of_charge, labels, free_text, thumbnail_path, palga,
                     operation, pikud):
        """

        :param thumbnail_path:
        :param pikud:
        :param operation:
        :param palga:
        :param name:
        :param date:
        :param dest_path:
        :param name_of_charge:
        :param labels: list of names of labels, the function will create the label object for each non-existing label
        :param free_text:
        :return:
        """
        self.archive_thumbnails_path = ARCHIVE_THUMBNAILS_PATH
        item_thumbnail_path = make_and_save_thumbnail(thumbnail_path, self.archive_thumbnails_path, THUMBNAILS_SIZE,
                                                      self.next_free_id)
        item = Item(self.next_free_id, name, date, dest_path, name_of_charge, labels, free_text, item_thumbnail_path,
                    palga, operation, pikud)
        self.items.append(item)
        self.update_labels_count(labels)
        self.next_free_id += 1
        print(item)
        # self.save_archive()

    # def load_archive(self):
    #     try:
    #         with open(self.data_file, 'r') as file:
    #             data = pickle.load(file)
    #             self.items = data['items']
    #             self.next_free_id = data['next_free_id']
    #             self.labels = data['labels']
    #     except FileNotFoundError:
    #         self.save_archive()
    #
    # def save_archive(self):
    #     with open(self.data_file, 'w') as file:
    #         pickle.dump(data, file)

    def add_label(self, name):  # todo: add info
        if not name:
            raise ValueError("Name cannot be empty")
        if self.labels.get(name):
            raise ValueError("Label already exists")
        self.labels[name] = Label(name)
        return self.labels[name]

    def remove_label(self, name):
        self.labels.pop(name)

    def print_archive(self):
        for item in self.items:
            item.print_item()
        print("The next free id is: ", self.next_free_id)
        print("The labels are: ", self.labels)

    def __str__(self):
        return f"Items: {self.get_items_str()}, Next Free ID: {self.next_free_id}, Labels: {self.labels}"

    def _json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def get_items_str(self):
        return [[item.__str__()] for item in self.items]

    def get_items_dic(self):
        return {item.id: item.__dic__() for item in self.items}

    def make_data(self):
        data = pd.DataFrame([item.__dic__() for item in self.items])
        data.to_csv(ARCHIVE_CSV_DATA_PATH, encoding='utf-8-sig', index=False)
        print(data)

    def update_labels_count(self, labels, increase=True):
        for label_name in labels.keys():
            self.labels[label_name].count += (-1 + increase * 2)

    def Items_filtered_by(self, name, date_from, date_to, name_of_charge, labels, pikud, operation, palga, free_text):
        filtered_items = self.items
        if name:
            filtered_items = [item for item in filtered_items if name in item.name]
        if date_from:
            filtered_items = [item for item in filtered_items if item.date >= date_from]
        if date_to:
            filtered_items = [item for item in filtered_items if item.date <= date_to]
        if name_of_charge:
            filtered_items = [item for item in filtered_items if item.name_of_charge == name_of_charge]
        if labels:
            labels_name = [label.name for label in labels]
            filtered_items = [item for item in filtered_items if set(labels_name).issubset(set(item.labels.keys()))]
        if pikud:
            filtered_items = [item for item in filtered_items if item.pikud == pikud]
        if operation:
            filtered_items = [item for item in filtered_items if item.operation == operation]
        if palga:
            filtered_items = [item for item in filtered_items if item.palga == palga]
        if free_text:
            filtered_items = [item for item in filtered_items if free_text in item.free_text]
        return filtered_items

    def remove_item(self, item):
        self.update_labels_count(item.labels, False)
        self.items.remove(item)

    def get_favorite_labels(self, start=0, n=5):
        labels = sorted(self.labels.values(), key=lambda x: x.count, reverse=True)
        return labels[start:start + n]

    def get_labels_contains(self, name):
        return [label for label in self.labels.values() if name in label.name]

    # def change_label(self, label, new_name):
    #     for l in self.labels:
    #         if l.name == label:
    #             l.name = new_name
    #             break
    def get_palgot(self):
        return PALGOT

    def get_operations(self):
        return OPERATIONS

    def get_pikuds(self):
        return PIKUDS

    def get_next_free_id(self):
        return self.next_free_id
    def backup_update(self):
        self.archive_thumbnails_path = ARCHIVE_THUMBNAILS_PATH
        self.num_of_backups = NUM_OF_BACKUPS
        self.last_back_up_index += 1
        if self.last_back_up_index > self.num_of_backups:
            self.last_back_up_index = 1

        return "data_file_" + str(self.last_back_up_index) + ".json"
