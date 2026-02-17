import yt_dlp



def get_top_youtube_video(query):
    # Налаштування для максимально швидкого пошуку без завантаження відео
    ydl_opts = {
        'format': 'best',
        'quiet': True,             # Не виводити зайвий текст у консоль
        'no_warnings': True,
        'noplaylist': True,        # Ігнорувати плейлисти
        'extract_flat': True,      # Тільки отримати інфо, не аналізувати кожен потік
        'skip_download': True,     # Не завантажувати файл
    }


    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Префікс ytsearch1: каже yt-dlp знайти саме 1 перше відео
        search_query = f"ytsearch1:{query}"
        info = ydl.extract_info(search_query, download=False)

        if 'entries' in info and len(info['entries']) > 0:
            video = info['entries'][0]
            # Формуємо пряме посилання
            video_url = f"https://www.youtube.com/watch?v={video['id']}"
            return video_url, video.get('title')

    
    

url = "репепт смачного печива"

video_url, video_title = get_top_youtube_video(url)

print(video_title)
print(video_url)