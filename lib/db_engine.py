import json
import os
from uuid import uuid4

tables = ["receipts"]


class DbEngine:
    """Database engine class: this will use json files to read and write data"""

    def __init__(self) -> None:
        self.db_path = "db/data"

    def initialize_db(self) -> None:
        """Check if the database exists"""
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path)
        # Check if the tables exist
        for table in tables:
            if not os.path.exists(f"{self.db_path}/{table}.json"):
                self.create_table(table)

    def create_table(self, table) -> None:
        """Create a table"""
        with open(f"{self.db_path}/{table}.json", "w") as file:
            json.dump([], file)

    def generate_id(self) -> str:
        return str(uuid4())

    def read(self, table) -> list[dict]:
        """Read data from a table"""
        with open(f"{self.db_path}/{table}.json") as file:
            return json.load(file)

    def insert_one(self, table: str, data: dict) -> str:
        """Insert one record into a table"""
        records = self.read(table)
        data["id"] = self.generate_id()
        records.append(data)
        print(records)
        with open(f"{self.db_path}/{table}.json", "w") as file:
            json.dump(records, file)
        return data["id"]

    def select_one(self, table, query) -> dict | None:
        """Select one record from a table"""
        records = self.read(table)
        for record in records:
            if record == query:
                return record
        return None

    def select_all(self, table) -> list[dict]:
        """Select all records from a table"""
        return self.read(table)

    def update_one(self, table, query, data) -> dict | None:
        """Update one record in a table"""
        records = self.read(table)
        for record in records:
            if record == query:
                record.update(data)
                with open(f"{self.db_path}/{table}.json", "w") as file:
                    json.dump(records, file)
                return record
        return None

    def delete_database(self) -> None:
        """Delete the database on close"""
        for table in tables:
            os.remove(f"{self.db_path}/{table}.json")
