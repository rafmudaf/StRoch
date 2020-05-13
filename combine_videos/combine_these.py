
import os
from multiprocessing import cpu_count
from multiprocessing import Pool
from moviepy.editor import (
    VideoFileClip,
    concatenate_videoclips
)
import video_processing


def filter_clips(clips_in):
    # Throw away clips shorter than 9 seconds
    # - These tend to be cars or bikes passing by quickly
    clips_out = list( filter( lambda x: x.duration >= 9, clips_in ) )
    return clips_out

def process_clips(clips_in):
    # clips_out = video_processing.down_sample(clips_in)
    clips_out = video_processing.drop_frames(clips_in)
    return clips_out

def process_chunk(i, filenames):
    chunk = [VideoFileClip( os.path.join(video_directory, f) ) for f in filenames]

    print("Working on chunk {} of {}".format(i + 1, n_videos))
    chunk = process_clips(chunk)

    print("Building clip...")
    final_clip = concatenate_videoclips(chunk)

    print("Exporting video file...")
    final_clip.write_videofile(os.path.join(video_directory, "temp{}".format(i + 1) + ".mp4"))


video_directory = "20200511"

# List of videos
video_paths = [
    ["1f02c2d766ef592cb1666f9ee49a4731.mp4"],
    ["8e56ca92da8c577d72ee41423e07a6c1.mp4"],
    ["93954cd9dcd48ff3c64c7142bf1bc911.mp4"],
    ["c207a8bd3a60bdbd2791a2489785f537.mp4"],
    ["8997c520198a77b85ce7be65207cc76c.mp4"],
    ["b6262c1747f88d7e44cfce807c72166a.mp4"],
    ["ff4e71c01c6b324e1148f88421f142d9.mp4"],
    ["e2a2aa4f06779cae4112699ddf6426e5.mp4"],
    ["18a72c5be9cabed79a57364980518def.mp4"],
    ["99405d47f323a0f6f351e43e9b7a89e8.mp4"],
    ["e20e248a047d52b07a2a0f4b3de4b7a8.mp4"],
    ["8940549ca7e3b8804fd683fb50b61123.mp4"],
    ["21d473092e3119e9d6c0bf188fd98ef6.mp4"],
    ["60acd802e13ffd72c558279c6c568e57.mp4"],
    ["7a1acc8d32e041f521fd511c11510596.mp4"],
    ["424386d7330ce66eeb597aec6e006ef2.mp4"],
    ["edd1ae83ffd5aecc3f8474d6b550cb04.mp4"],
    ["740fc8063d58fb26c240d0ee7b1a0b22.mp4"],
    ["15ae3fc947d923feb6fe85b5bf46ee8d.mp4"],
    ["1b285d1c5cb80750a2fa1b589f83f23a.mp4"],
    ["bcf24ae0763128a8c7e7d3a77b0003a5.mp4"],
    ["2daad00f5dc78b7a7e271e33596e2f8d.mp4"],
    ["67af6e1ef2b2c830c7d0f23f90ddc709.mp4"],
    ["0723acacf7f3594b49250a5d1dee1475.mp4"],
]
n_videos = len(video_paths)

arguments = list(
    zip(
        [i for i in range(n_videos)],
        video_paths
    )
)
with Pool(2) as pool:
    pool.starmap(process_chunk, arguments)

temp_clips = [
    VideoFileClip(os.path.join(video_directory, "temp{}".format(i + 1) + ".mp4")) for i in range(n_videos)
]
final = concatenate_videoclips(temp_clips)
final.write_videofile(os.path.join(video_directory, video_directory + ".raf.mp4"))
