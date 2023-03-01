from gtts import gTTS
Import simplebot

@simplebot.command()
def tts(bot: DeltaBot, message: Message, replies: Replies) -> None:

def main():
  tts = gTTS('hello')
  tts.save('hello.mp3')

if __name__ == "__main__":
  main()
