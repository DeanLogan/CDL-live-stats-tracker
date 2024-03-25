import subprocess

def stream_youtube_video():
    video_url = "https://www.youtube.com/watch?v=FjclYlb8dRY&list=WL&index=61&t=127s"
    ffmpeg_command = f"youtube-dl -q -o - {video_url} | ffmpeg -i pipe:0 -f mp4 -vcodec rawvideo -"

    process = subprocess.Popen(ffmpeg_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    
    process.stdout.close()
    process.stderr.close()

stream_youtube_video()
