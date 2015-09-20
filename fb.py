# -*-coding:utf-8-*-
import sys
import sleekxmpp
import cleverbot
import logging
logging.basicConfig(level=logging.DEBUG)

reload(sys)
sys.setdefaultencoding('utf8')

user = sys.argv[1] + "@chat.facebook.com"
password = sys.argv[2]
sessions = {}
dont_send = []


class EchoBot(sleekxmpp.ClientXMPP):

    def __init__(self, jid, pwd):
        sleekxmpp.ClientXMPP.__init__(self, jid, pwd)

        self.add_event_handler('session_start', self.start)
        self.add_event_handler('message', self.message)

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        if msg['from'] in dont_send:
            return
        if str(msg['body']) not in sessions:
            sessions[str(msg['from'])] = cleverbot.Cleverbot()
        print str(msg['body'])
        msg_back = str(sessions[str(msg['from'])].ask(str(msg['body'])))
        print msg_back
        self.send_message(
            mto=msg['from'],
            mbody=msg_back)

if __name__ == "__main__":
    xmpp = EchoBot(user, password)
    xmpp.register_plugin('xep_0030')  # service discovery
    xmpp.register_plugin('xep_0004')  # date form
    xmpp.register_plugin('xep_0060')  # pubsub
    xmpp.register_plugin('xep_0199')  # xmpp ping

    if xmpp.connect():
        print("xmpp start")
        xmpp.process(threaded=False)
        print("Done")
    else:
        print("unable to connected")
