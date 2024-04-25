

class Label:

    def __init__(self, name, info=""):
        self.name = name
        self.info = info
        self.count = 1
        # possibly: hold a list of all the items which has the label

    def print_label(self):
        print(f"Name: {self.name}, Count: {self.count}, Info: {self.info}")

    def __str__(self):
        return f"Name: {self.name}, Count: {self.count}, Info: {self.info}"

    def __dic__(self):
        return {
                "Name": self.name,
                "Count": self.count,
                "Info": self.info
               }

    def __eq__(self, other):
        return self.name == other.name

    def get_name(self):
        return self.name



