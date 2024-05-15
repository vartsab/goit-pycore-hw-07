from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, phone):
        while not phone.isdigit() or len(phone) != 10:
            phone = input("Phone number must be 10 digits: ")
        self.value = phone

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if str(p) == phone:
                self.phones.remove(p)
                return

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if str(phone) == old_phone:
                phone.value = new_phone
                return

    def find_phone(self, phone):
        for p in self.phones:
            if str(p) == phone:
                return p
        return None

    def __str__(self):
        phones_str = "; ".join(str(p) for p in self.phones)
        birthday_str = str(self.birthday) if self.birthday else "Not specified"
        return f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            self.data.pop(name)

    def get_upcoming_birthdays(self, days=7):
        today = datetime.combine(datetime.today(), datetime.min.time())
        end_date = today + timedelta(days=days)
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                next_birthday = record.birthday.value.replace(year=today.year)
                if next_birthday < today:
                    next_birthday = record.birthday.value.replace(year=today.year + 1)
                if today <= next_birthday <= end_date:
                    upcoming_birthdays.append((record.name.value, next_birthday))

        return upcoming_birthdays

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"Error: {str(e)}"
    return wrapper

@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        return "Please provide both name and phone number."

    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook):
    if len(args) < 3:
        return "Please provide name, old phone, and new phone."

    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return f"Phone number updated for {name}."
    else:
        return f"Contact {name} not found."

@input_error
def show_phone(args, book: AddressBook):
    if len(args) < 1:
        return "Please provide the name of the contact."

    name = args[0]
    record = book.find(name)
    if record:
        return f"Phone numbers for {name}: {', '.join(str(p) for p in record.phones)}"
    else:
        return f"Contact {name} not found."

@input_error
def show_all(contacts):
    if not contacts:
        return "Your contact list is empty."
    else:
        return "\n".join(str(record) for record in contacts.values())

@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        return "Please provide both name and birthday in DD.MM.YYYY format."

    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday added for {name}."
    else:
        return f"Contact {name} not found."

@input_error
def show_birthday(args, book: AddressBook):
    if len(args) < 1:
        return "Please provide the name of the contact."
    
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday: {record.birthday}"
    elif record:
        return f"{name} has no birthday specified."
    else:
        return f"Contact {name} not found."

@input_error
def birthdays(args, book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return "\n".join([f"{name}: {birthday.strftime('%d.%m.%Y')}" for name, birthday in upcoming_birthdays])
    else:
        return "No upcoming birthdays found."

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book.data))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()