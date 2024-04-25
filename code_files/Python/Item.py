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

    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, Date: {self.date}, Dest Path: {self.dest_path}," \
               f" Name of Charge: {self.name_of_charge}, Labels: {self.labels}, Thumbnail: {self.thumbnail}," \
               f" Palga: {self.palga}, Operation: {self.operation}, Pikud: {self.pikud}, Free Text: {self.free_text}"

    def __dic__(self):
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
            "Free Text": self.free_text
        }

    def print_item(self):
        print(
            f"ID: {self.id}, Name: {self.name}, Date: {self.date}, Dest Path: {self.dest_path}, Name of Charge: {self.name_of_charge},"
            f" Labels: {self.labels}, Free Text: {self.free_text}, Thumbnail: {self.thumbnail}, Palga: {self.palga}, Operation: {self.operation}, Pikud: {self.pikud}")
