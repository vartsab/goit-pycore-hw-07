from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        self.value = value


class Phone(Field):
    def __init__(self, phone):
        while not phone.isdigit() or len(phone) != 10:
            phone = input("Phone number must be 10 digits.>")
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
        if len(phone) != 10 or not phone.isdigit():
            raise ValueError("Phone number must be 10 digits.")
        phone_obj = Phone(phone)
        self.phones.append(phone_obj)

    def remove_phone(self, phone):
        for p in self.phones:
            if str(p) == phone:
                self.phones.remove(p)
                return

    def edit_phone(self, old_phone, new_phone):
        if len(new_phone) != 10 or not new_phone.isdigit():
            raise ValueError("Phone number must be 10 digits.")
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


book = AddressBook()

john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
john_record.add_birthday("01.05.1990")  # Adding birthday
book.add_record(john_record)

jane_record = Record("Jane")
jane_record.add_phone("9876543210")
jane_record.add_birthday("15.05.1985")  # Adding birthday
book.add_record(jane_record)

for name, record in book.data.items():
    print(record)

john = book.find("John")
if john:
    john.edit_phone("1234567890", "1112223333")
    print(john)

found_phone = john.find_phone("5555555555")
if found_phone:
    print(f"{john.name.value}: {found_phone}")

upcoming_birthdays = book.get_upcoming_birthdays()
print("\nUpcoming birthdays:")
for name, birthday in upcoming_birthdays:
    print(f"{name}: {birthday.strftime('%d.%m')}")

book.delete("Jane")