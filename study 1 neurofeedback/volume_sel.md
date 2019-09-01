# Selection of volumes

This part of the script defines the indices for selecting volumes in real-time, for both the baseline and imagery time period.

```python
# in volumes
RESTV = int(16000 / TR)
IMAGERYV = int(16000 / TR)
RATINGV = int(6000 / TR)
CONFV = int(6000 / TR)
FEEDBACKV = int(2000 / TR)
DELAY = int(6000 / TR) # BOLD delay
BASELINE_DELAY = int(6000 / TR)  # We ignore the first datapoints of the baseline
BASELINE_POST = int(2000 / TR) # we take two first volumes after task-onset
# volume nrs are 0-indexed, but vol 1 comes after the first TR, so we can index a volume directly by its number (e.g. vol 1 = 1, and not 0)
baseline_min_max = (DELAY+BASELINE_DELAY, RESTV+BASELINE_POST)  # 0s to 16s, we take volumes 13 to 18 after baseline-onset
imagery_min_max = (RESTV+DELAY, RESTV+IMAGERYV)  # 16s to 32s
start_trial_volume = 0 # This variable updated every trial
```

As a result, we have the following index boundaries, with respect to trial onset
* For **baseline**: *min* = 12 and *max* = 18
* For **imagery**: *min* = 22 and *max* = 32 (or 6–16)

### Defining the range

Then, a **range** for the volume indices are defined inside the script using the range() function:

```python
# baseline volumes (similar to imagery volumes)
baselineVolumes = range(start_trial_volume+baseline_min_max[0],
                        start_trial_volume+baseline_min_max[1])
```

Using `range(x,y)`, Python outputs a list of continuous integers from `x` up until `y`, but excluding `y`.
* So that `range(12,18)` outputs: `12, 13, 14, 15, 16, 17` (6 values)
* And `range(22,32)` outputs: `22, 23, 24, 25, 26, 27, 28, 29, 30, 21` (10 values)

### Selecting the volumes

With the range of indices, we can now select the actual volumes in the list of volumes (read using the *expyriment tbv extension*).
Note that the list of volumes is 0-indexed (as everything in Python). In our task, the first volume is created after 1 second. That volume, we shall call it volume = 1, at time (s) = 1, will thus be indexed as `0`:

`Volume 1 = Second 1 = Index 0`

Our functions will thus give us volumes corresponding to:

* `range(12,18)` gives us volumes **13 to 18** (6 values)

* `range(22,32)` gives us volumes **23 to 32** (10 values) (or v7 to v16 with respect to imagery onset)

### Ranges in seconds

Since volumes were collected every second, then:
* v13 to v18 correspond to time range **12s to 18s**
* v23 to v32 correspond to time range 22s to 32s (or **6s to 16s** with respect to imagery onset)

![Figure](https://i.imgur.com/JIsWTmH.png "Figure")
