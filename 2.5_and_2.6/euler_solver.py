import numpy as np


def all_steps(t: float, step_count: int, p, dpdt):
    """
    Like `after_t`, but returns all intermediate values.

    Note that `p` can be any ndarray, but `dpdt(p)` should have the same shape as `p`.
    """

    dt = t / step_count
    ps = np.zeros((step_count + 1,) + p.shape)
    for i in range(step_count):
        ps[i] = p
        p += dpdt(p) * dt
    ps[-1] = p
    return ps


def after_t(t: float, step_count: int, p, dpdt):
    """
    Estimates the value of `p` after `t` time has passed.

    Note that `p` can be any ndarray, but `dpdt(p)` should have the same shape as `p`.

    Equivalent to `all_steps(...)[-1]`.
    """
    p = np.copy(p)
    dt = t / step_count
    for i in range(step_count):
        p += dpdt(p) * dt
    return p
