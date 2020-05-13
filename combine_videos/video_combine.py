
import os
from moviepy.editor import (
    VideoFileClip,
    ImageSequenceClip,
    concatenate_videoclips
)
import video_processing


def process_clips(clips_in):
    return clips_out


video_directory = "20200509"

# Get list of videos
video_paths = list( filter( lambda x: ".mp4" in x, os.listdir(video_directory) ) )

# Sort by name
# video_paths.sort( key=lambda x: x )

# Sort by last modification date
video_paths.sort( key=lambda x: os.path.getmtime(os.path.join(video_directory, x) ), reverse=True )

clips = [VideoFileClip( os.path.join(video_directory, video) ) for video in video_paths]

# Throw away clips shorter than 9 seconds
# - These tend to be cars or bikes passing by quickly
clips = list( filter( lambda x: x.duration >= 9, clips ) )

chunk_size = 5
n_chunks = len(clips) // chunk_size
for i in range(n_chunks):
    print("Working on chunk {} of {}".format(i + 1, n_chunks))

    if i < n_chunks - 1:
        # Automatically set the step size
        i0 = i*chunk_size
        i1 = (i+1)*chunk_size
        chunk = clips[i0:i1]
    else:
        # On the last step, go all the way to the end of the clip array
        i0 = i*chunk_size
        chunk = clips[i0:]

    postprocessed = process_clips(chunk)

    print("Building clip...")
    final_clip = concatenate_videoclips(postprocessed)

    print("Exporting video file...")
    final_clip.write_videofile(video_directory + "_temp_{}".format(i) + ".mp4")

    print("Finished chunk {}".format(i + 1))


