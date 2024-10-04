class Item:
    def __init__(self, id, name, date, dest_path, name_of_charge, labels, free_text, thumbnail_path, palga,
                 operation, pikud):
        self.id = id
        self.name = name
        self.date = date
        self.dest_path = dest_path
        self.name_of_charge = name_of_charge
        self.labels = labels
        self.thumbnail = thumbnail_path
        self.palga = palga
        self.operation = operation
        self.pikud = pikud
        self.free_text = free_text
        self.was_opened = 0

    def __str__(self):
        if not hasattr(Item, 'was_opened'):
            self.was_opened = 0


        return f"ID: {self.id}, Name: {self.name}, Date: {self.date}, Dest Path: {self.dest_path}," \
               f" Name of Charge: {self.name_of_charge}, Labels: {self.labels}, Thumbnail: {self.thumbnail}," \
               f" Palga: {self.palga}, Operation: {self.operation}, Pikud: {self.pikud}, Free Text: {self.free_text}," \
               f" Was Opened: {self.was_opened} times"

    def __dic__(self):
        if not hasattr(Item, 'was_opened'):
            self.was_opened = 0

        return {
            "ID": self.id,
            "Name": self.name,
            "Date": self.date,
            "Dest Path": self.dest_path,
            "Name of Charge": self.name_of_charge,
            "Labels": str(self.labels),
            "Thumbnail": self.thumbnail,
            "Palga": self.palga,
            "Operation": self.operation,
            "Pikud": self.pikud,
            "Free Text": self.free_text,
            "Was Opened": self.was_opened
        }

    def print_item(self):
        if not hasattr(Item, 'was_opened'):
            self.was_opened = 0
        print(
            f"ID: {self.id}, Name: {self.name}, Date: {self.date}, Dest Path: {self.dest_path}, Name of Charge: {self.name_of_charge},"
            f" Labels: {self.labels}, Free Text: {self.free_text}, Thumbnail: {self.thumbnail}, Palga: {self.palga}, Operation: {self.operation}, Pikud: {self.pikud},"
            f" Was Opened: {self.was_opened} times")

    def open_item(self):
        # checks if self.was_opened initialized
        if not hasattr(Item, 'was_opened'):
            self.was_opened = 0
        self.was_opened += 1
        print(f"Item {self.id} was opened {self.was_opened} times")
