#!/usr/bin/env python3
"""
compare with CCMC web service output
"""
from datetime import datetime
import numpy as np
import pytest
from pytest import approx
from pathlib import Path

import msise00

R = Path(__file__).parent
reffn = R / "ccmc.log"


def test_ccmc():
    t = datetime(2001, 2, 2, 8, 0, 0)
    glat = 60.0
    glon = -70.0
    altkm = 400.0
    indices = {"f107s": 163.6666, "f107": 146.7, "Ap": 7}

    A = np.loadtxt(reffn, skiprows=25)

    atmos = msise00.run(t, altkm, glat, glon, indices)
    assert atmos.f107s == approx(163.6666)
    assert atmos.f107 == approx(146.7)
    assert atmos.Ap == approx(7)
    assert A[0] == approx(altkm)
    assert A[1] == approx(atmos["O"].item() / 1e6, rel=0.05)
    assert A[2] == approx(atmos["N2"].item() / 1e6, rel=0.3)
    assert A[3] == approx(atmos["O2"].item() / 1e6, rel=0.35)
    assert A[7] == approx(atmos["He"].item() / 1e6, rel=0.2)
    assert A[8] == approx(atmos["Ar"].item() / 1e6, rel=0.6)
    assert A[9] == approx(atmos["H"].item() / 1e6, rel=0.1)
    assert A[10] == approx(atmos["N"].item() / 1e6, rel=0.3)
    assert A[11] == approx(atmos["AnomalousO"].item() / 1e6, rel=0.3)

    assert A[5] == approx(atmos["Tn"].item(), rel=0.1)
    assert A[6] == approx(atmos["Texo"].item(), rel=0.1)


def test_ccmc2():
    t = datetime(2018, 5, 17, 21, 0, 0)
    glat = 55.0
    glon = 120.0
    altkm = 300.0
    indices = {"f107s": 72.6, "f107": 71.5, "Ap": 9.5}

    atmos = msise00.run(t, altkm, glat, glon, indices)

    assert 4.874e7 == approx(atmos["N2"].item() / 1e6, rel=0.2)
    assert 1.622e6 == approx(atmos["O2"].item() / 1e6, rel=0.1)

    assert 794.1 == approx(atmos["Tn"].item(), rel=0.1)
    assert 800.0 == approx(atmos["Texo"].item(), rel=0.1)


if __name__ == "__main__":
    pytest.main([__file__])
