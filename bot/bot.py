import logging

import irc.bot
import irc.strings
import mysql.connector

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, token, channel):
        self.token = token
        self.channel = '#' + channel

        # Initialize the database connection
        self.conn = mysql.connector.connect(
            host='',
            port='',
            user='',
            password='',
            database=''
        )
        self.cursor = self.conn.cursor()

        # Define IRC server connection details
        server = 'irc.chat.twitch.tv'
        port = 6667

        # Initialize the bot
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, token)], username, username)

    def on_welcome(self, connection, event):
        # Join the channel when the bot is connected
        connection.join(self.channel)
        logger.info("Bot joined channel: %s", self.channel)

    def on_pubmsg(self, connection, event):
        # Get the sender's username and the message content
        username = event.source.nick
        message = event.arguments[0]

        # Check if the message is the "!ask" command
        if message.startswith('!ask'):
            # Extract the question from the message
            question = message[5:].strip()
            self.add_question(username, question)
            logger.info("Question added by %s: %s", username, question)
            self.connection.privmsg(self.channel, f'{username}: Question added!')

    def add_question(self, username, question):
        # Add the question and username to the database
        self.cursor.execute('INSERT INTO questions (username, question, channel) VALUES (%s, %s, %s)', (username, question, self.channel))
        self.conn.commit()

    def close(self):
        # Close the database connection when the bot shuts down
        self.conn.close()

if __name__ == "__main__":
    # Set your Twitch username, OAuth token, and channel name
    username = ''
    token = ''
    channel = ''

    # Create and run the Twitch bot
    bot = TwitchBot(username, token, channel)
    bot.start()
