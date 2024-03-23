import requests
import eyed3
import re
import sys
import time

def extract_song_id(share_link):
    """从网易云音乐分享链接中提取歌曲ID"""
    match = re.search(r"(?:id=|/)(\d+)", share_link)
    if match:
        return match.group(1)
    else:
        print("无法从链接中提取歌曲ID。")
        sys.exit()

def download_song(song_id, output_file):
    """下载网易云音乐的歌曲并保存为MP3文件"""
    url = f"https://music.163.com/song/media/outer/url?id={song_id}.mp3"
    start_time = time.time()  # 记录下载开始时间
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 检查请求是否成功
    except requests.RequestException as e:
        print(f"下载失败：{e}")
        return

    with open(output_file, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    end_time = time.time()  # 记录下载结束时间
    print(f"歌曲已保存为: {output_file}")
    print(f"下载耗时: {end_time - start_time:.2f} 秒")

def update_mp3_metadata(song_info, output_file):
    """更新MP3文件的元数据"""
    audiofile = eyed3.load(output_file)
    if audiofile is not None and audiofile.tag is not None:
        audiofile.tag.artist = song_info["artist"]
        audiofile.tag.title = song_info["title"]
        audiofile.tag.save()
        print("MP3元数据已更新。")
    else:
        print("无法更新MP3元数据。")

def main():
    share_link = input("请输入网易云音乐的音乐分享链接：")
    song_id = extract_song_id(share_link)
    output_file = f"{song_id}.mp3"
    
    # 下载歌曲
    download_song(song_id, output_file)
    
    # 更新元数据（可选，需要先获取歌曲信息）
    # song_info = {"artist": "Artist Name", "title": "Song Title"}
    # update_mp3_metadata(song_info, output_file)

if __name__ == "__main__":
    main()



