# music_player.py
import os
import vlc
import yt_dlp

class MusicPlayer:
    def __init__(self):
        self.player = None
        self.current_volume = 70
        self.output_mode = 'default'  # 'default' or 'earphones'

    def play(self, query):
        query_lower = query.lower()
        if " on soundcloud" in query_lower:
            query = query_lower.replace(" on soundcloud", "").strip()
            self.play_soundcloud(query)
        elif " on youtube" in query_lower:
            query = query_lower.replace(" on youtube", "").strip()
            self.play_youtube(query)
        elif " on spotify" in query_lower:
            print("Spotify support coming soon!")
        elif " on apple music" in query_lower:
            print("Apple Music support coming soon!")
        elif " on amazon music" in query_lower:
            print("Amazon Music support coming soon!")
        else:
            self.play_youtube(query)

    def play_youtube(self, query):
        print(f"Searching YouTube for: {query}")
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'noplaylist': True,
            'default_search': 'ytsearch',
            'extract_flat': False
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(query, download=False)
            if result and 'entries' in result:
                url = result['entries'][0]['url']
                print(f"Playing URL: {url}")
                self.play_stream(url)

    def play_soundcloud(self, query):
        print(f"SoundCloud support not implemented yet. You asked for: {query}")
        # Placeholder for future SoundCloud API integration

    def play_stream(self, url):
        self.stop()
        instance = vlc.Instance()
        self.player = instance.media_player_new()
        media = instance.media_new(url)
        self.player.set_media(media)
        self.set_volume(self.current_volume)
        if self.output_mode == 'earphones':
            self.set_audio_output('alsa', 'hw:1,0')  # Adjust for your earphone device
        self.player.play()

    def set_volume(self, volume):
        self.current_volume = max(0, min(100, volume))
        if self.player:
            self.player.audio_set_volume(self.current_volume)
        print(f"Volume set to: {self.current_volume}%")

    def set_audio_output(self, module, device):
        if self.player:
            self.player.audio_output_device_set(module, device)
        print(f"Switched audio output to: {device}")

    def blast_it(self):
        self.output_mode = 'earphones'
        if self.player:
            self.set_audio_output('alsa', 'hw:1,0')  # Replace with correct earphone device name
        print("🔊 Output switched to earphones")

    def pause(self):
        if self.player:
            self.player.pause()
            print("⏸ Music paused")

    def resume(self):
        if self.player:
            self.player.play()
            print("▶ Music resumed")

    def stop(self):
        if self.player:
            self.player.stop()
            print("⏹ Music stopped")
            self.player = None

# For CLI testing
if __name__ == '__main__':
    m = MusicPlayer()
    m.play("Play lo-fi chill beats on YouTube")
    input("Press Enter to stop...")
    m.stop()