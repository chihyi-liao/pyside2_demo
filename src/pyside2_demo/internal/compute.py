from typing import Any, List, Optional, Union

import numpy as np

np.set_printoptions(suppress=True)


def sma(values: List[float], n: int) -> Union[List, np.ndarray]:
    """ Simple Moving Average """
    if len(values) < n:
        return []

    cumulate_sum = np.cumsum(np.insert(values, 0, 0), dtype=float)
    move_avg = (cumulate_sum[n:] - cumulate_sum[:-n]) / float(n)
    return np.insert(move_avg, 0, [0] * (n-1))


def ewma(values, n, smoothing=2) -> Union[List, np.ndarray]:
    """ Exponentially Weighted Moving Average """
    if len(values) < n:
        return []

    alpha = smoothing / (1 + n)
    array = [sum(values[:n]) / n]
    for val in values[n:]:
        array.append((val * alpha) + array[-1] * (1 - alpha))
    return np.insert(array, 0, [0] * (n-1))


def wwsa(values, n, smoothing=1) -> Union[List, np.ndarray]:
    """ Welles Wilder’s Smoothing Average """
    if len(values) < n:
        return []

    alpha = smoothing / n
    array = [sum(values[:n]) / n]
    for val in values[n:]:
        array.append((val * alpha) + array[-1] * (1 - alpha))
    return np.insert(array, 0, [0] * (n-1))


def macd(values: List[float], fast: Optional[int] = 12,
         slow: Optional[int] = 26, n: Optional[int] = 9) -> [List[np.ndarray], List[Any], List[Any]]:
    ema_fast = np.array(ewma(values, fast))
    ema_slow = np.array(ewma(values, slow))
    if len(ema_fast) and len(ema_slow):
        macd_ = ema_fast - ema_slow
        signal = ewma(macd_, n)
        diff = macd_ - signal
        if len(diff) > 45:
            macd_[:45] = [np.nan * 45]
            signal[:45] = [np.nan * 45]
            diff[:45] = [np.nan * 45]
            return np.around(macd_, decimals=6), np.around(signal, decimals=6), np.around(diff, decimals=6)
        return [], [], []
    else:
        return [], [], []


def rsi(close_values, n: Optional[int] = 10) -> List[float]:
    result = []
    up_moves = []
    down_moves = []
    for i in range(1, len(close_values)):
        diff = round(close_values[i] - close_values[i-1], 2)
        if diff >= 0:
            up_moves.append(diff)
            down_moves.append(0)
        else:
            up_moves.append(0)
            down_moves.append(abs(diff))

    mean_up = wwsa(up_moves, n)
    mean_down = wwsa(down_moves, n)
    for avg_up, avg_down in zip(mean_up, mean_down):
        if avg_down == 0:
            result.append(None)
        else:
            rs = round(avg_up/avg_down, 2)
            result.append(round(100-(100 / (1 + rs)), 2))
    return result


def rsv(high_values: List[float], low_values: List[float],
        close_values: List[float], n: Optional[int] = 9) -> List[float]:
    result = []
    for i, value in enumerate(close_values, start=1):
        if i < n:
            continue
        n_low = min(low_values[i - n:i])
        n_high = max(high_values[i - n:i])
        if n_high - n_low == 0:
            continue
        result += [100. * (value - n_low) / (n_high - n_low)]
    return result


def kdj(high_values: List[float], low_values: List[float],
        close_values: List[float], n: Optional[int] = 9) -> [List[Any], List[Any], List[Any]]:
    data = rsv(high_values, low_values, close_values, n)
    k_data = []
    d_data = []
    j_data = []
    for i, val in enumerate(data):
        k = 50.0 if len(k_data) == 0 else k_data[i - 1]
        d = 50.0 if len(d_data) == 0 else d_data[i - 1]
        k_data += [(2 / 3 * k) + (1 / 3 * val)]
        d_data += [(2 / 3 * d) + (1 / 3 * k_data[-1])]
        j_data += [(3 * d_data[-1]) - (2 * k_data[-1])]
    return k_data, d_data, j_data


def obv(close_values: List[float], volumes: List[int]) -> List[int]:
    data = []
    for i, co in enumerate(close_values):
        if i == 0:
            data.append(0)
        else:
            vol = volumes[i]
            prev_co = close_values[i-1]
            if co == prev_co:
                vol = 0
            elif co < prev_co:
                vol = -1 * vol
            data.append(data[i-1] + vol)
    return data
