from phone_book import AddressBook, Record, Birthday
from datetime import datetime
import pickle

FILE_NAME = "addressbook.pkl"


def save_data(book, filename=FILE_NAME):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename=FILE_NAME):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, NameError) as e:
            return f"Error: {e}"

    return wrapper


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args


@input_error
def add_contact(args, contacts):
    name, phone = args
    record = contacts.find(name)
    if record is None:
        record = Record(name)
        contacts.add_record(record)
    record.add_phone(phone)
    return f"Contact {name} added with the phone number {phone}."


@input_error
def change_contact(args, contacts):
    name, old_phone, new_phone = args
    record = contacts.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact updated."
    else:
        raise NameError(f"Contact {name} not found.")


@input_error
def get_phone(args, contacts):
    name = args[0]
    record = contacts.find(name)
    if record:
        phones = "; ".join(phone.value for phone in record.phones)
        return f"{name}'s phone numbers: {phones}"
    else:
        raise NameError(f"Contact {name} not found.")


@input_error
def get_all_contacts(contacts):
    if contacts.data:
        return "\n".join([str(record) for record in contacts.data.values()])
    else:
        return "No contacts found."


@input_error
def add_birthday(args, contacts):
    name, birthday = args
    record = contacts.find(name)
    if record:
        record.birthday = Birthday(birthday)
        return f"{name}'s birthday added as {birthday}."
    else:
        raise NameError(f"Contact {name} not found.")


@input_error
def show_birthday(args, contacts):
    name = args[0]
    record = contacts.find(name)
    if record and record.birthday:
        return f"{name}'s birthday is on {record.birthday}."
    return f"Contact {name} does not have a birthday recorded."


@input_error
def birthdays(_, contacts):
    upcoming_birthdays = contacts.get_upcoming_birthdays()
    if upcoming_birthdays:
        return "\n".join(upcoming_birthdays)
    return "No birthdays in the next week."


def main():
    contacts = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(contacts)
            print("Goodbye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(get_phone(args, contacts))
        elif command == "all":
            print(get_all_contacts(contacts))
        elif command == "add-birthday":
            print(add_birthday(args, contacts))
        elif command == "show-birthday":
            print(show_birthday(args, contacts))
        elif command == "birthdays":
            print(birthdays(args, contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
