import json
from unittest.mock import patch

import pytest
from pathlib import Path
from pydantic import ValidationError

from phone_directory import Record, PhoneDirectory


@pytest.mark.parametrize(
    ("person", "expected_result"),
    [
        (
            {
                "last_name": "1",
                "first_name": "Сергей",
                "middle_name": "Анатольевич",
                "organization": "СберБанк",
                "work_phone": "495-555-6666",
                "personal_phone": "916-666-7777",
            },
            (
                "1 validation error for Record\n"
                "last_name\n"
                "  Invalid data. Please enter a valid data [type=Invalid data, "
                "input_value='1', input_type=str]"
            ),
        ),
        (
            {
                "last_name": "Соколов",
                "first_name": "Сергей",
                "middle_name": "Анатольевич",
                "organization": "СберБанк",
                "work_phone": "495-555-6666",
                "personal_phone": "тест",
            },
            (
                    "1 validation error for Record\n"
                    "personal_phone\n"
                    "  Invalid phone number [type=Invalid data, "
                    "input_value='тест', input_type=str]"
            ),
        ),
    ],
)
def test_phone_directory_validation_record(person: dict, expected_result: str) -> None:
    with pytest.raises(ValidationError) as e:
        Record(**person)

    assert str(e.value) == expected_result


@pytest.mark.parametrize(
    ("person", "file_path", "expected_result"),
    [
        (
            {
                "last_name": "Соколов",
                "first_name": "Сергей",
                "middle_name": "Анатольевич",
                "organization": "СберБанк",
                "work_phone": "495-555-6666",
                "personal_phone": "916-666-7777",
            },
            "test_phone_directory.json",
            [
                Record(
                    last_name="Соколов",
                    first_name="Сергей",
                    middle_name="Анатольевич",
                    organization="СберБанк",
                    work_phone="495-555-6666",
                    personal_phone="916-666-7777",
                ),
            ],
        ),
    ],
)
def test_phone_directory(person: dict, file_path: str, expected_result: list[Record]) -> None:
    path = Path(file_path)
    record = Record(**person)
    phone_directory = PhoneDirectory(file_path=file_path)
    phone_directory.add_record(record)
    with path.open("r") as file:
        records_data = json.load(file)
        records = [Record(**data) for data in records_data]
    assert records == expected_result


@pytest.mark.parametrize(
    ("file_path", "expected_result"),
    [
        (
            "phone_directory.json",
            [
                Record(
                    last_name="Иванов",
                    first_name="Алексей",
                    middle_name="Владимирович",
                    organization="ООО РосТех",
                    work_phone="495-123-4567",
                    personal_phone="910-555-6789",
                ),
                Record(
                    last_name="Петрова",
                    first_name="Екатерина",
                    middle_name="Андреевна",
                    organization="ГазПром",
                    work_phone="499-987-6543",
                    personal_phone="916-777-8899",
                ),
                Record(
                    last_name="Смирнов",
                    first_name="Дмитрий",
                    middle_name="Сергеевич",
                    organization="СберБанк",
                    work_phone="495-111-2222",
                    personal_phone="905-333-4444",
                ),
                Record(
                    last_name="Козлов",
                    first_name="Анастасия",
                    middle_name="Павловна",
                    organization="РосНефть",
                    work_phone="499-444-5555",
                    personal_phone="916-666-7777",
                ),
                Record(
                    last_name="Ефимов",
                    first_name="Ирина",
                    middle_name="Алексеевна",
                    organization="ГазПром",
                    work_phone="495-777-8888",
                    personal_phone="910-999-0000",
                ),
                Record(
                    last_name="Васнецова",
                    first_name="Павел",
                    middle_name="Николаевич",
                    organization="ОАО РЖД",
                    work_phone="495-222-3333",
                    personal_phone="916-111-2222",
                ),
                Record(
                    last_name="Морозов",
                    first_name="Татьяна",
                    middle_name="Ивановна",
                    organization="Лукойл",
                    work_phone="499-333-4444",
                    personal_phone="905-444-5555",
                ),
                Record(
                    last_name="Соколов",
                    first_name="Сергей",
                    middle_name="Анатольевич",
                    organization="СберБанк",
                    work_phone="495-555-6666",
                    personal_phone="916-666-7777",
                ),
                Record(
                    last_name="Кузнецова",
                    first_name="Максим",
                    middle_name="Дмитриевич",
                    organization="ООО РосТех",
                    work_phone="499-888-9999",
                    personal_phone="910-000-1111",
                ),
                Record(
                    last_name="Иванова",
                    first_name="Анна",
                    middle_name="Александровна",
                    organization="РосНефть",
                    work_phone="495-999-0000",
                    personal_phone="905-111-2222",
                ),
                Record(
                    last_name="Петров",
                    first_name="Виктор",
                    middle_name="Игоревич",
                    organization="Лукойл",
                    work_phone="499-000-1111",
                    personal_phone="916-222-3333",
                ),
                Record(
                    last_name="Смирнова",
                    first_name="Александр",
                    middle_name="Артемович",
                    organization="ОАО РЖД",
                    work_phone="495-111-2222",
                    personal_phone="910-333-4444",
                ),
                Record(
                    last_name="Козлова",
                    first_name="Елена",
                    middle_name="Владимировна",
                    organization="ГазПром",
                    work_phone="495-222-3333",
                    personal_phone="916-444-5555",
                ),
                Record(
                    last_name="Ефимова",
                    first_name="Игорь",
                    middle_name="Иванович",
                    organization="СберБанк",
                    work_phone="499-333-4444",
                    personal_phone="905-555-6666",
                ),
                Record(
                    last_name="Васнецов",
                    first_name="Ольга",
                    middle_name="Алексеевна",
                    organization="ООО РосТех",
                    work_phone="495-444-5555",
                    personal_phone="916-666-7777",
                ),
            ],
        ),
    ],
)
def test_phone_directory_display(file_path: str, expected_result: list[Record]) -> None:
    path = Path(file_path)
    phone_directory = PhoneDirectory(file_path=file_path)
    phone_directory.display_records()
    with path.open("r") as file:
        records_data = json.load(file)
        records = [Record(**data) for data in records_data]
    assert records == expected_result


@pytest.mark.parametrize(
    ("file_path", "index", "side_effect", "expected_result"),
    [
        (
            "test_phone_directory.json",
            0,
            ["2", "Андрей"],
            [
                Record(
                    last_name="Соколов",
                    first_name="Андрей",
                    middle_name="Анатольевич",
                    organization="СберБанк",
                    work_phone="495-555-6666",
                    personal_phone="916-666-7777",
                ),
            ],
        ),
        (
            "test_phone_directory.json",
            5,
            ["2", "Андрей"],
            [
                Record(
                    last_name="Соколов",
                    first_name="Андрей",
                    middle_name="Анатольевич",
                    organization="СберБанк",
                    work_phone="495-555-6666",
                    personal_phone="916-666-7777",
                ),
            ],
        ),
        (
            "test_phone_directory.json",
            0,
            ["10", "Андрей"],
            [
                Record(
                    last_name="Соколов",
                    first_name="Андрей",
                    middle_name="Анатольевич",
                    organization="СберБанк",
                    work_phone="495-555-6666",
                    personal_phone="916-666-7777",
                ),
            ],
        ),
    ],
)
def test_phone_directory_edit(
    file_path: str,
    index:int,
    side_effect: list[str],
    expected_result: list[Record]
) -> None:
    path = Path(file_path)
    phone_directory = PhoneDirectory(file_path=file_path)
    with patch("builtins.input", side_effect=side_effect):
        phone_directory.edit_record(index)
    with path.open("r") as file:
        records_data = json.load(file)
        records = [Record(**data) for data in records_data]
    assert records == expected_result


@pytest.mark.parametrize(
    ("query", "file_path", "expected_result"),
    [
        (
            "first_name=андрей",
            "test_phone_directory.json",
            [
                Record(
                    last_name="Соколов",
                    first_name="Андрей",
                    middle_name="Анатольевич",
                    organization="СберБанк",
                    work_phone="495-555-6666",
                    personal_phone="916-666-7777",
                ),
            ],
        ),
        (
            "first_nam=андрей",
            "test_phone_directory.json",
            [],
        ),
        (
            "андрей",
            "test_phone_directory.json",
            [
                Record(
                    last_name="Соколов",
                    first_name="Андрей",
                    middle_name="Анатольевич",
                    organization="СберБанк",
                    work_phone="495-555-6666",
                    personal_phone="916-666-7777",
                ),
            ],
        ),
    ],
)
def test_phone_directory_search(query: str, file_path: str, expected_result: list[Record]) -> None:
    phone_directory = PhoneDirectory(file_path=file_path)
    result = phone_directory.search_records(query)
    assert result == expected_result