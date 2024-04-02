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
        image_url VARCHAR(255),
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

    def connect_to_table(self, table, limit=None):
        """
        :param limit:
        :param table:
        :return: dictionary of the table rows
        """
        query = f"SELECT * FROM {table};"
        if limit:
            query += f" LIMIT {limit}"
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


def close_db_connection(self):
    self.connection.close()