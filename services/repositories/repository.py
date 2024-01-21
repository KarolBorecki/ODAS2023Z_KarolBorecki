from services.repositories.db_manager import DbManager


class Repository:
    def __init__(self, table_name, columns, columns_ref):
        self.table_name = table_name
        self.columns = columns
        self.columns_ref = columns_ref
        self.db = DbManager()
        self.db.clear_table_if_should(self.table_name)

    def create_table(self):
        cols = ""
        for key in self.columns:
            cols += f"{key} {self.columns[key]}, "
        if len(self.columns_ref) == 0:
            cols = cols[:-2]

        ref = ""
        for key in self.columns_ref:
            ref += f"FOREIGN KEY({key}) REFERENCES {self.columns_ref[key]}, "
        ref = ref[:-2]

        self.db.connect()
        self.db.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} ({cols} {ref})")
        self.db.commit()
        self.db.close()

    def get(self, by, param):
        if by not in self.columns.keys():
            raise Exception(f"[GET] Column {by} not found in {self.table_name}")
        raw_data = self.db.fast_exec(
            f"SELECT * FROM {self.table_name} WHERE {by}=?", (param,)
        )
        data = []
        for row in raw_data:
            data_row = {}
            i = 0
            for key in self.columns:
                data_row[key] = row[i]
                i += 1
            data.append(data_row)
        return data

    def insert(self, data):
        cols_names = ""
        cols_values = tuple([str(data[key]) for key in data])
        for key in data:
            if key not in self.columns.keys():
                raise Exception(f"[INSERT] Column {key} not found in {self.table_name}")
            cols_names += f"{key}, "
        cols_names = cols_names[:-2]

        val_format = f"{'?, ' * len(data)}"
        val_format = val_format[:-2]

        self.db.connect()
        inserted_id = self.db.execute(
            f"INSERT INTO {self.table_name} ({cols_names}) VALUES ({val_format})",
            cols_values,
        )
        self.db.commit()
        self.db.close()
        return inserted_id

    def update(self, data, by, param):
        cols_names = ""
        for key in data:
            if key not in self.columns.keys():
                raise Exception(f"[UPDATE] Column {key} not found in {self.table_name}")
            cols_names += f"{key}=?, "
        cols_names = cols_names[:-2]

        param_values = tuple([str(data[key]) for key in data] + [param])

        self.db.connect()
        inserted_id = self.db.execute(
            f"UPDATE {self.table_name} SET {cols_names} WHERE {by}=?", param_values
        )
        self.db.commit()
        self.db.close()
        return inserted_id
