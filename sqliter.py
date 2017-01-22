# -*- coding: utf-8 -*-
import sqlite3

import conf

connection = sqlite3.connect(conf.storage_name_params)
try:
    cursor = connection.cursor()
    cursor.execute(conf.create_table)
    connection.commit()
except sqlite3.OperationalError:
    pass
finally:
    connection.close()


class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_single(self, client_id):
        with self.connection:
            try:
                response = self.cursor.execute('SELECT * FROM params WHERE id = ?', (client_id,)).fetchall()[0]
                return response
            except IndexError:
                return None

    def write_param(self, client_id, col_name, val):
        with self.connection:
            try:
                self.cursor.execute('UPDATE params SET {}=? WHERE id = ?'.format(str(col_name)), (str(val),
                                                                                                  str(client_id),))
                self.connection.commit()
            except sqlite3.OperationalError:
                pass

    def write_first_param(self, client_id, reply_url):
        with self.connection:
            try:
                self.cursor.execute('INSERT INTO params ( id, reply ) VALUES ( ?, ? )', (client_id, str(reply_url),))
                self.connection.commit()
            except sqlite3.OperationalError:
                pass

    def clear_params(self, client_id):
        with self.connection:
            self.cursor.execute('DELETE FROM params WHERE id = ?', (client_id,))
            self.connection.commit()

    def close(self):
        self.connection.close()
