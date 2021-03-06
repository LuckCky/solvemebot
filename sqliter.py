# -*- coding: utf-8 -*-
import os
import psycopg2
import urllib.parse
import datetime

import conf

urllib.parse.uses_netloc.append("postgres")
url = urllib.parse.urlparse(os.environ["DATABASE_URL"])


class SQLighter:

    def __init__(self):
        self.connection = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        self.cursor = self.connection.cursor()

    def select_current(self, client_id):
        date = datetime.datetime.now().strftime('%Y-%m-%d')

        with self.connection:
            try:
                self.cursor.execute(conf.select_current_question, (str(client_id), date, ))
                current_question = self.cursor.fetchall()[0]
                return current_question
            except IndexError:
                return None

    def select_next(self, client_id, question_num):
        date = datetime.datetime.now().strftime('%Y-%m-%d')

        with self.connection:
            try:
                self.cursor.execute(conf.select_next_question, (str(client_id),
                                                                question_num, date, ))
                next_question = self.cursor.fetchall()[0]
                return next_question
            except IndexError:
                return False

    def rewrite(self, client_id, val, col_name=None, question_num=None):
        date = datetime.datetime.now().strftime('%Y-%m-%d')

        if question_num:
            with self.connection:
                try:
                    self.cursor.execute(conf.set_next_question, (
                        str(val), str(client_id), question_num, date, ))
                    self.connection.commit()
                    return True
                except:
                    return False
        else:
            with self.connection:
                try:
                    self.cursor.execute(conf.change_correct_answers.format(str(col_name)),
                                        (str(val), str(client_id), date, ))
                    self.connection.commit()
                    return True
                except:
                    return False

    def select_any(self, statement, user_id):
        date = datetime.datetime.now().strftime('%Y-%m-%d')

        with self.connection:
            try:
                self.cursor.execute(statement, (str(user_id), date, ))
                data = self.cursor.fetchall()
                return data
            except IndexError:
                return False
