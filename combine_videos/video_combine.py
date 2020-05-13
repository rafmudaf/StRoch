
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
    clips_out = video_processing.down_sample(clips_in)
    # clips_out = video_processing.drop_frames(clips_in)
    return clips_out

def process_chunk(i, filenames):
    chunk = [VideoFileClip( os.path.join(video_directory, f) ) for f in filenames]

    print("Working on chunk {} of {}".format(i + 1, n_chunks))
    chunk = process_clips(chunk)

    print("Building clip...")
    final_clip = concatenate_videoclips(chunk)

    print("Exporting video file...")
    final_clip.write_videofile(video_directory + "_temp_{}".format(i + 1) + ".mp4")
    final_clip.write_videofile(os.path.join(video_directory, "temp{}".format(i + 1) + ".mp4"))


video_directory = "20200509"

# Get list of videos
video_paths = list( filter( lambda x: ".mp4" in x, os.listdir(video_directory) ) )

# Sort by name
# video_paths.sort( key=lambda x: x )

# Sort by last modification date
video_paths.sort( key=lambda x: os.path.getmtime(os.path.join(video_directory, x) ), reverse=True )

chunk_size = 2
n_chunks = len(video_paths) // chunk_size
chunks = []
for i in range(n_chunks):
    i0 = i*chunk_size
    if i == n_chunks - 1:
        # On the last step, go all the way to the end of the clip array
        chunks.append(video_paths[i0:])
    else:
        # Otherwise, use the constant step size and fill this chunk
        i1 = (i+1)*chunk_size
        chunks.append(video_paths[i0:i1])

arguments = list(
    zip(
        [i for i in range(n_chunks)],
        chunks
    )
)
with Pool(2) as pool:
    pool.starmap(process_chunk, arguments)

temp_clips = [
    VideoFileClip(os.path.join(video_directory, "temp{}".format(i + 1) + ".mp4")) for i in range(n_chunks)
]
final = concatenate_videoclips(temp_clips)
final.write_videofile(os.path.join(video_directory, video_directory + ".raf.mp4"))
