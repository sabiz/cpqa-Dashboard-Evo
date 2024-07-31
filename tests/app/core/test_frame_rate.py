import time
from cpqa.app.core import FrameRate


def test_frame_rate(mocker):
    frame_rate = FrameRate()
    mocker.patch.object(time, "time", return_value=0)
    frame_rate.wait()
    assert frame_rate._FrameRate__last_time == 0
    mocker.patch.object(time, "time", return_value=1)
    frame_rate.wait()
    assert frame_rate._FrameRate__last_time == 1
