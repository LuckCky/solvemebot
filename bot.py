import telebot

import cherrypy

from utils import working_hours
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
    if working_hours():
        message_text = conf.greeting
    else:
        message_text = conf.not_welcome
    print(message.chat.id)
    bot.send_message(message.chat.id, message_text)


# @bot.callback_query_handler(func=lambda call: True)
# def callback_inline(call):


# @bot.message_handler(content_types=['text', 'audio', 'document', 'photo', 'sticker', 'video',
#                                     'voice', 'location', 'contact'])
# def button_reaction(message):

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
