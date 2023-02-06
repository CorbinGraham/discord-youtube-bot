import pafy
import vlc

class YoutubePlayer:
  def __init__(self):
    self.vlc_player = vlc.Instance()
    self.play_queue = []

# Cleans the passed youtube URL for playing.
def enqueue_play(self, url):
  optimal_youtube_url = pafy.new(url).getbest()
  play_url = optimal_youtube_url.url
  self.play_queue << play_url

# Creates a headless VLC that will stream the audio from the cleaned URL
def play_enqueued(self, url):
  player = self.vlc_player.media_player_new()
  Media = self.vlc_player.media_new(url)
  Media.get_mrl()
  player.set_media(Media)
  player.play()
