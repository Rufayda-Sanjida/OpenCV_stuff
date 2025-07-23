get average multiple frames in real time:

Strategy:
Keep a running buffer of the last N frames (e.g., 100).

For each new frame:

Add it to the buffer.

Compute the mean of all frames in the buffer.

Display or analyze the averaged frame.

