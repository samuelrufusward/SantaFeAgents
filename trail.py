"""This file will generate the generic Santa Fe Trail"""
import numpy as np


def generate_trail():
    """Generates the generic santa fe trail"""
    trail = np.zeros((32, 32), dtype=int)
    trail[0, 1:4] = 1
    trail[1:5, 3] = 1
    trail[5, 3:7] = 1
    trail[5, 8:12] = 1
    trail[5:10, 12] = 1
    trail[11:15, 12] = 1
    trail[17:24, 12] = 1
    trail[24, 7:12] = 1
    trail[24, 3:5] = 1
    trail[25:29, 1] = 1
    trail[30, 2:6] = 1
    trail[28:30, 7] = 1
    trail[27, 8:15] = 1
    trail[24:27, 16] = 1
    trail[18:22, 16] = 1
    trail[15, 17] = 1
    trail[13:15, 20] = 1
    trail[7:11, 20] = 1
    trail[5, 21:23] = 1
    trail[3:5, 24] = 1
    trail[2, 25:28] = 1
    trail[3:5, 29] = 1
    trail[6, 29] = 1
    trail[9, 29] = 1
    trail[12, 29] = 1
    trail[14, 26:29] = 1
    trail[15, 23] = 1
    trail[18, 24] = 1
    trail[19, 27] = 1
    trail[22, 26] = 1
    trail[23, 23] = 1

    return trail
