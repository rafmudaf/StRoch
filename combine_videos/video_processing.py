
import numpy as np


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
