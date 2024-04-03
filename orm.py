import mysql.connector


class Database:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def create_schema(self):
        self.create_collections_table()
        self.create_contracts_table()
        self.create_collection_contracts_relationship_table()

    def create_collections_table(self):
        query = """ 
        CREATE TABLE IF NOT EXISTS collections (
        id INT AUTO_INCREMENT PRIMARY KEY,
        collection VARCHAR(255),
        name VARCHAR(255),
        description TEXT,
        image_url TEXT,
        owner VARCHAR(255),
        twitter_username VARCHAR(255)
        );
        """
        self.cursor.execute(query)
        self.connection.commit()

    def create_contracts_table(self):
        query = """
        CREATE TABLE  IF NOT EXISTS contracts(
         id INT AUTO_INCREMENT PRIMARY KEY,
        address VARCHAR(255),
        chain VARCHAR(255)
        );
        """

        self.cursor.execute(query)
        self.connection.commit()

    def create_collection_contracts_relationship_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS collection_contracts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        collection_id INT,
        contract_id INT,
        FOREIGN KEY (collection_id) REFERENCES collections(id),
        FOREIGN KEY (contract_id) REFERENCES contracts(id)
        );
        """
        self.cursor.execute(query)
        self.connection.commit()

    def delete_table(self, table):
        query = f"DROP TABLE IF EXISTS {table};"
        self.cursor.execute(query)
        self.connection.commit()

    def delete_row(self, table, row_id):
        """
        since all the tables in the db have id field no need for seperate functions for each table
        :param table:
        :param row_id:
        :return:
        """
        query = f"DELETE FROM {table} WHERE id = %s;"
        self.cursor.execute(query, (row_id,))
        self.connection.commit()

    def update_row(self, table, row_id, new_data):
        """
        :param table:
        :param row_id:
        :param new_data: dictionary containing column names and new values
        """
        set_values = ', '.join([f"{key} = %s" for key in new_data.keys()])
        query = f"UPDATE {table} SET {set_values} WHERE id = %s;"
        values = list(new_data.values())
        values.append(row_id)
        self.cursor.execute(query, tuple(values))
        self.connection.commit()

    def retrieve_table_data(self, table, limit=None, order_by=None, LIKE=None, ILIKE=None):
        """
        :param LIKE:
        :param ILIKE:
        :param order_by:
        :param limit:
        :param table:
        :return: dictionary of the table rows
        """
        query = f"SELECT * FROM {table}"
        if LIKE:
            query += f" WHERE {LIKE[0]} LIKE '{LIKE[1]}'"
        elif ILIKE:
            query += f" WHERE {LIKE[0]} ILIKE '{ILIKE[1]}'"
        if order_by:
            query += f" ORDER BY {order_by}"
        if limit:
            query += f" LIMIT {limit}"
        query += ";"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def insert_into_contracts(self, address, chain):
        query = """
        INSERT INTO contracts (address, chain)
        VALUES (%s, %s);
        """
        self.cursor.execute(query, (address, chain))
        self.connection.commit()

        return self.cursor.lastrowid

    def insert_into_collection(self, data):
        query = """
        INSERT INTO collections (collection, name, description, image_url, owner, twitter_username)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        params = tuple(data.values())
        self.cursor.execute(query, params)
        self.connection.commit()

        return self.cursor.lastrowid

    def insert_into_collection_contracts(self, collection_id, contract_id):
        query = """
        INSERT INTO collection_contracts (collection_id, contract_id) VALUES (%s, %s);
        """

        params = (collection_id, contract_id)
        self.cursor.execute(query, params)
        self.connection.commit()

    def insert_data(self, data):
        """
        handles both inserting a single value and multiple values
        :param data: list of dictionary (contracts field must be a dictionary itself)
        :return:
        """
        for entry in data:
            # auto generated contract id's
            ag_ids = []
            # list of contract dictionaries
            list_of_contract_dict = entry.pop('contracts', None)
            for dic in list_of_contract_dict:
                ag_ids.append(self.insert_into_contracts(dic["address"], dic["chain"]))
            collection_id = self.insert_into_collection(entry)
            for contract_id in ag_ids:
                self.insert_into_collection_contracts(collection_id, contract_id)

    def add_column_to_table(self, table, column, column_type):
        query = f"ALTER TABLE {table} ADD COLUMN {column} {column_type};"
        self.cursor.execute(query)
        self.connection.commit()

    def remove_column_from_table(self, table, column):
        query = f"ALTER TABLE {table} DROP COLUMN {column};"
        self.cursor.execute(query)
        self.connection.commit()

    def change_column_type(self, table, column_name, new_type):
        query = f"ALTER TABLE {table} MODIFY COLUMN {column_name} {new_type};"
        self.cursor.execute(query)
        self.connection.commit()

    def close_db_connection(self):
        self.connection.close()
