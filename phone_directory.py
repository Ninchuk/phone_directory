import argparse
import dataclasses
import json
import logging
import math
import re
import textwrap
from pathlib import Path

from pydantic import ValidationError, field_validator
from pydantic.dataclasses import dataclass
from pydantic_core import PydanticCustomError


logging.basicConfig(filename="phone_directory.log",
                    filemode="a",
                    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
                    datefmt="%H:%M:%S",
                    level=logging.DEBUG)

log = logging.getLogger(__name__)


@dataclass
class Record:
    """
    Create Record object.
    """
    last_name: str
    first_name: str
    middle_name: str
    organization: str
    work_phone: str
    personal_phone: str

    @field_validator("last_name", "first_name", "middle_name", "organization")
    @classmethod
    def validate_string_fields(cls, value):
        pattern = r'^[a-zA-Zа-яА-Я\s]+(?:-[a-zA-Zа-яА-Я\s]+)?$'
        if not re.match(pattern, value):
            raise PydanticCustomError("Invalid data", "Invalid data. Please enter a valid data")
        return value

    @field_validator("personal_phone", "work_phone")
    @classmethod
    def validate_phone(cls, value):
        pattern = r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'
        if not re.match(pattern, value):
            raise PydanticCustomError("Invalid data", "Invalid phone number")
        return value

class DataclassJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


class PhoneDirectory:
    """
    Initializes the PhoneDirectory object.

    :param file_path: Path to the file where phone directory records are stored.
    """
    def __init__(self, file_path: str = "phone_directory.json") -> None:
        self.file_path = Path(file_path)
        self.records = self.load_records()

    def load_records(self) -> list[Record]:
        """
        Loads records from the file.

        :return: List of Record objects.
        """
        try:
            with self.file_path.open("r") as file:
                records_data = json.load(file)
                records = [Record(**data) for data in records_data]
                return records
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            log.error("Error decoding JSON in the file. Please check the file format.")
            return []
        except ValidationError as e:
            log.error(f"Validation error in the data: {e}")
            return []

    def save_records(self) -> None:
        """
        Saves records to the file.

        :return: None
        """
        records_data = [dataclasses.asdict(record) for record in self.records]
        with self.file_path.open("w") as file:
            json.dump(records_data, file, indent=2, cls=DataclassJSONEncoder)

    def display_records(self, records: list[Record] = None, entries_per_page: int = 5, page_number: int = 1) -> None:
        """
        Displays records on the screen with pagination.

        :param records: List of records to display (default first page).
        :param entries_per_page: Number of entries to display per page.
        :param page_number: Page number to display.
        :return: None
        """
        records_to_display = records or self.records
        start_index = (page_number - 1) * entries_per_page
        end_index = start_index + entries_per_page
        current_page_records = records_to_display[start_index:end_index]

        for index, record in enumerate(current_page_records, start=start_index + 1):
            formatted_text = f"""
            ID {index}
            Last name: {record.last_name}
            First name: {record.first_name}
            Middle name: {record.middle_name}
            Organization: {record.organization}
            Work phone: {record.work_phone}
            Personal phone: {record.personal_phone}
            """

            formatted_text = textwrap.dedent(formatted_text).strip()
            print(formatted_text)

        print(f"Page {page_number}/{math.ceil(len(records_to_display) / entries_per_page)}")

    def add_record(self, record: Record) -> None:
        """
        Adds a new record to the phone directory.

        :param record: Record object representing the new record.
        :return: None
        """
        try:
            self.records.append(record)
            self.save_records()
            print("Entry added successfully.")
        except ValidationError as e:
            log.error(f"Failed to add entry: {e}")

    def edit_record(self, index: int) -> None:
        """
        Edits an existing record in the phone directory.

        :param index: Index of the record to edit.
        :return: None
        """
        if 0 <= index < len(self.records):
            record = self.records[index]

            print("Current values:")
            for key, value in dataclasses.asdict(record).items():
                formatted_key = key.replace('_', ' ').capitalize()
                print(f"{formatted_key}: {value}")

            print("Choose a field to edit:")
            for i, field in enumerate(dataclasses.asdict(record).keys(), start=1):
                formatted_field = field.replace('_', ' ')
                print(f"{i}. {formatted_field.capitalize()}")

            try:
                selected_field_index = int(input("Enter the number of the field to edit: ")) - 1
                selected_field = list(dataclasses.asdict(record).keys())[selected_field_index]

                new_value = input(f"Enter the new value for {selected_field.capitalize()}: ")
                setattr(record, selected_field, new_value)

                self.save_records()
                print("Entry edited successfully.")
            except (ValidationError, IndexError):
                log.exception("Invalid input. Please enter a valid field number.")
                print("Invalid input. Please enter a valid field number.")
        else:
            log.error("Invalid index.")
            print("Invalid index.")

    def search_records(self, query: str) -> list[Record]:
        """
        Searches for records in the phone directory based on the given query.

        :param query: Search query string.
        :return: List of records matching the query.
        """
        results = []
        if "=" in query.lower():
            field, value = query.split("=")
            for record in self.records:
                if not hasattr(record, field):
                    print(f"Field '{field}' does not exist.")
                    log.error(f"Field '{field}' does not exist.")
                    return results
                if getattr(record, field).lower() == value.lower():
                    results.append(record)

        else:
            for record in self.records:
                if any(query.lower() in value.lower() for value in dataclasses.asdict(record).values()):
                    results.append(record)
        return results


def parse_arguments():
    parser = argparse.ArgumentParser(description="Phone Directory Management")
    sub_parser = parser.add_subparsers(dest="command")
    display = sub_parser.add_parser("display", help="Display all records")
    display.add_argument("--page", "-p", type=int, default=1, help="Page number for display")
    display.add_argument("--records_per_page", "-r", type=int, default=5, help="Number records for display")

    sub_parser.add_parser("add", help="Add a new record")

    edit = sub_parser.add_parser("edit", help="Edit an record by index")
    edit.add_argument("index", type=int, help="Record index")

    search = sub_parser.add_parser("search", help="Search records by query")
    search.add_argument("query", type=str, help="Query for display")
    search.add_argument("--page", "-p", type=int, default=1, help="Page number for display")
    search.add_argument("--records_per_page", "-r", type=int, default=5, help="Number records for display")

    return parser.parse_args()


def main():
    phone_directory = PhoneDirectory()

    args = parse_arguments()

    match args.command:
        case "display":
            phone_directory.display_records(page_number=args.page, entries_per_page=args.entries_per_page)
        case "add":
            try:
                new_record = Record(
                        input("Last Name: "),
                        input("First Name: "),
                        input("Middle Name: "),
                        input("Organization: "),
                        input("Work Phone: "),
                        input("Personal Phone: "),
                    )
                phone_directory.add_record(new_record)
            except ValidationError as e:
                log.exception(f"Failed to create record: {e}")
                print(f"Failed to create record: {e}")
        case "edit":
            phone_directory.edit_record(args.index - 1)
        case "search":
            search_query = args.query
            search_results = phone_directory.search_records(search_query)
            phone_directory.display_records(search_results) if search_results else print("No results found.")


if __name__ == "__main__":
    main()
