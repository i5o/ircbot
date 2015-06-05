#!/usr/bin/env python
from twisted.internet import reactor, protocol
from twisted.words.protocols import irc
import sys

from chatterbotapi import ChatterBotFactory, ChatterBotType

factory = ChatterBotFactory()
sessions = {}


class GCIBot(irc.IRCClient):
    nickname = 'rengar'
    username = 'rengar'
    password = 'irodriguez'

    def __init__(self):
        self.channels = []

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)

    def signedOn(self):
        for c in self.factory.channels:
            self.join(c)

    def joined(self, channel):
        self.channels.append(channel)

    def privmsg(self, user, channel, msg):
        user_ = user.split('!', 1)[0]
        isForMe = msg.startswith(
            self.nickname +
               ":") or msg.startswith(
            self.nickname +
               ",") or msg.startswith(
            self.nickname +
               " ")
        if channel not in sessions:
            sessions[
                channel] = [
                    factory.create(
                        ChatterBotType.PANDORABOTS,
                        'b0dafd24ee35a477')]
            sessions[channel].append(sessions[channel][0].create_session())

        
        if not isForMe:
            return

        if msg[len(self.nickname) + 2:] == "the msg":
            self.msg(channel, "%s, blabla" % user_)
        else:
            self.msg(channel, str(sessions[channel][1].think(str(msg))))

    def alterCollidedNick(self, nickname):
        return '_' + nickname + '_'


class BotFactory(protocol.ClientFactory):

    def __init__(self, channels):
        self.channels = channels

    def buildProtocol(self, addr):
        p = GCIBot()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()


if __name__ == '__main__':
    f = BotFactory(sys.argv[1:])
    reactor.connectTCP("irc.freenode.net", 6667, f)
    print "Connected to server. Channels:"
    for channel in sys.argv[1:]:
        print channel
    reactor.run()
