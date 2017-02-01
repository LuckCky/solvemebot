import telebot
import cherrypy

from utils import working_hours, insert_questions, read_current_question
from utils import create_table, change_correct_answers, read_next_question
from utils import set_next_question
import conf

# WEBHOOK_PORT = conf.webhook_port
# WEBHOOK_LISTEN = conf.webhook_listen
#
# WEBHOOK_SSL_CERT = conf.webhook_ssl_cert
# WEBHOOK_SSL_PRIV = conf.webhook_ssl_priv
#
# WEBHOOK_URL_BASE = conf.post_url
# WEBHOOK_URL_PATH = "/{}/".format(conf.token)

bot = telebot.TeleBot(conf.token)


@bot.message_handler(commands=["start"])
def command_start(message):
    # if working_hours():
    if True:
        message_text = conf.greeting
        create_table()
        insert_questions(message.chat.id)
    else:
        message_text = conf.not_welcome
    bot.send_message(message.chat.id, message_text)


@bot.message_handler(commands=["game"])
def command_start_game(message):
    question = read_current_question(message.chat.id)[3]
    if question.startswith('http'):
        bot.send_photo(message.chat.id, question, 'Тут вопрос???')
    else:
        bot.send_message(message.chat.id, question)


@bot.message_handler(commands=["next"])
def command_next_question(message):
    current_question_num = read_current_question(message.chat.id)[2]
    next_question = read_next_question(message.chat.id, current_question_num)
    if next_question:
        solved = set_next_question(message.chat.id, current_question_num, 'Next', 'status')
        set_next = set_next_question(message.chat.id, next_question[2], 'Active', 'status')
        if solved and set_next:
            message_text = conf.next_question
        else:
            message_text = conf.gone_wrong
    else:
        message_text = conf.finished
    bot.send_message(message.chat.id, message_text)


@bot.message_handler(content_types=['text', 'audio', 'document', 'photo', 'sticker', 'video',
                                    'voice', 'location', 'contact'])
def answer_reaction(message):
    answer = message.text.lower()
    correct_answers = read_current_question(message.chat.id)[4].lower()
    correct_answers = correct_answers.split('\n')
    if answer in correct_answers:
        correct_answers.remove(answer)
        len_correct_answers = len(correct_answers)
        if len_correct_answers > 0:
            correct_answers = "\n".join(correct_answers)
            answers_changed = change_correct_answers(message.chat.id, correct_answers)
            if answers_changed:
                message_text = conf.right_answer.format(len_correct_answers)
            else:
                message_text = conf.gone_wrong
        else:
            current_question_num = read_current_question(message.chat.id)[2]
            next_question = read_next_question(message.chat.id, current_question_num)
            if next_question:
                solved = set_next_question(message.chat.id, current_question_num, 'Solved', 'status')
                set_next = set_next_question(message.chat.id, next_question[2], 'Active', 'status')
                if solved and set_next:
                    message_text = conf.next_question
                else:
                    message_text = conf.gone_wrong
            else:
                message_text = conf.finished
    else:
        message_text = conf.wrong_answer
    bot.send_message(message.chat.id, message_text)


# @bot.callback_query_handler(func=lambda call: True)
# def callback_inline(call):


# class WebhookServer(object):
#     @cherrypy.expose
#     def index(self):
#         if 'content-length' in cherrypy.request.headers and \
#                         'content-type' in cherrypy.request.headers and \
#                         cherrypy.request.headers['content-type'] == 'application/json':
#             length = int(cherrypy.request.headers['content-length'])
#             json_string = cherrypy.request.body.read(length).decode("utf-8")
#             update = telebot.types.Update.de_json(json_string)
#             bot.process_new_updates([update])
#             return ''
#         else:
#             raise cherrypy.HTTPError(403)


if __name__ == "__main__":
    bot.remove_webhook()
    # time.sleep(5)
    # bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
    #
    # cherrypy.config.update({
    #     'engine.autoreload.on': False,
    #     'server.socket_host': WEBHOOK_LISTEN,
    #     'server.socket_port': WEBHOOK_PORT,
    #     'server.ssl_module': 'builtin',
    #     'server.ssl_certificate': WEBHOOK_SSL_CERT,
    #     'server.ssl_private_key': WEBHOOK_SSL_PRIV
    # })
    #
    # # RUN SERVER, RUN!
    # cherrypy.tree.mount(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})
    # cherrypy.tree.mount(GetBankPost(), WEBHOOK_URL_PATH + conf.bank_token + '/', {'/': {}})
    #
    # cherrypy.engine.start()
    # cherrypy.engine.block()
    bot.polling()
