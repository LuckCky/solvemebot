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

    def select_next(self, client_id, question_num):
        with self.connection:
            try:
                next_question = self.cursor.execute(conf.select_next_question,
                                                    (client_id, question_num,)).fetchall()[0]
                return next_question
            except IndexError:
                return False

    def rewrite(self, client_id, val, col_name=None, question_num=None):
        if question_num:
            with self.connection:
                try:
                    self.cursor.execute(conf.set_next_question, (
                        str(val), str(client_id), str(question_num)))
                    self.connection.commit()
                    return True
                except sqlite3.OperationalError:
                    return False
        else:
            with self.connection:
                try:
                    self.cursor.execute(conf.change_correct_answers.format(str(col_name)),
                                        (str(val), str(client_id),))
                    self.connection.commit()
                    return True
                except sqlite3.OperationalError as e:
                    print(e)
                    return False

    def select_any(self, statement, user_id):
        with self.connection:
            try:
                data = self.cursor.execute(statement, (user_id,)).fetchall()
                return data
            except IndexError:
                return False
