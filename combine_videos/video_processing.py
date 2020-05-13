
import numpy as np
from moviepy.editor import ImageSequenceClip


def filter_time_energy_frames(video_clip):
    """
    Calculates the "energy" of each frame based on a backwards in time finite difference.

    Args:
        video_clip (VideoFileClip)

    Returns:
        list(float): The time-locations of the frames with energies greater than 0.0
    """

    # set the time step
    dt = 1 / video_clip.fps

    # keep the first frame
    energy_band_pass_times = [0.0]
    previous_frame = video_clip.get_frame(0.0)

    # loop over all frames to calculate the energy
    # based on a backward difference
    for i, current_frame in enumerate(video_clip.iter_frames()):
        if i==0:
            continue

        energy = np.abs(previous_frame - current_frame) / dt

        if sum(sum(sum(energy))) > 0:
            energy_band_pass_times.append( i * dt )

        previous_frame = current_frame

    return energy_band_pass_times

def down_sample(clips_in):
    # Drop every other frame
    clips_out = []
    for i, clip in enumerate(clips_in):
        total_frames = int(clip.fps * clip.duration)
        times_to_keep = [ i * (1 / clip.fps) for i in range(0, total_frames, 2)]
        image_sequence = ImageSequenceClip(
            [clip.get_frame(t) for t in times_to_keep],
            fps=clip.fps
        )
        clips_out.append(image_sequence)
    return clips_out

def drop_frames(clips_in):
    # Drop frames with a low time-energy
    # - This is meant to be a measure of how much movement is happening in a clip
    # - We dont really want to see people standing still. It may be worthwhile to go back and review these clips,
    #   but for the sake of viewing the clips quickly to identify videos of interest we only want to see movement
    clips_out = []
    for i, clip in enumerate(clips_in):
        print("Processing clip {} of {}".format(i + 1, len(clips_in)))

        times_to_keep = filter_time_energy_frames(clip)
        image_sequence = ImageSequenceClip(
            [clip.get_frame(t) for t in times_to_keep],
            fps=clip.fps
        )
        clips_out.append(image_sequence)
    return clips_out