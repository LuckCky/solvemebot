# -*- coding: utf-8 -*-
import sqlite3

import conf


class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_current(self, client_id):
        with self.connection:
            try:
                current_question = self.cursor.execute(conf.select_current_question,
                                                       (client_id,)).fetchall()[0]
                return current_question
            except IndexError:
                return None

    def select_next(self, client_id):
        with self.connection:
            try:
                next_question = self.cursor.execute(conf.select_next_question,
                                                       (client_id,)).fetchall()[0]
                return next_question
            except IndexError:
                return None

    def rewrite(self, client_id, col_name, val):
        with self.connection:
            try:
                self.cursor.execute(conf.change_correct_answers.format(str(col_name)),
                                    (str(val), str(client_id),))
                self.connection.commit()
                return True
            except sqlite3.OperationalError:
                return False

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
