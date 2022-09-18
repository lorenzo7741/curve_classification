import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

CTG_THRESHOLD = 2

CONVEXITY_THRESHOLD = 2

def fw_curve_class(ctg, cnvxty):
    if ctg > CTG_THRESHOLD:
        if cnvxty > CONVEXITY_THRESHOLD:
            return 'convex contango'
        elif cnvxty < - CONVEXITY_THRESHOLD:
            return 'concav contango'
        else:
            return 'linear contango'
    elif ctg < - CTG_THRESHOLD:
        if cnvxty > CONVEXITY_THRESHOLD:
            return 'convex contango'
        elif cnvxty < - CONVEXITY_THRESHOLD:
            return 'concav contango'
        else:
            return 'linear contango'
    else:
        return 'plain'


def classify_fw_curve(curve):
    t1 = curve['Time'][0]
    dt_year = datetime(t1.year + 1, 1, 1) - datetime(t1.year, 1, 1)

    time_num = [(d - curve['Time'][0]).days / dt_year.days for d in curve['Time']]
    poly_interp = np.poly1d(np.polyfit(time_num, curve['Values'], 2) )
    der2_poly_interp = poly_interp.deriv(m=2)
    der_poly_interp = poly_interp.deriv(m=1)
    contango_coef = (time_num[-1] - time_num[0]) * (der_poly_interp(time_num[-1]) + der_poly_interp(time_num[0]))/2
    convexity_coef = der2_poly_interp(time_num[-1]) * (time_num[-1] - time_num[0])
    print('backguard coef: ' + str(contango_coef))
    print('concavity coef: ' + str(concavity_coef))

    myline = np.linspace(0, time_num[-1], 100)
    plt.scatter(time_num, curve['Values'], c='orange')
    plt.plot(myline, poly_interp(myline))
    plt.show()


class CmdtyCurve(pd.DataFrame):
    def __init__(self, uom='1', name=None, *args, **kw):
        super().__init__(*args, **kw)
        self.uom = uom
        self.name = name


def to_remove():
    fmt = '%d-%m-%Y'
    date_conv = lambda x: datetime.strptime(x, fmt).date()
    psv_val = pd.read_csv('psv.csv', sep=';', converters={'Time': date_conv})


if __name__ == "__main__":

    d = [datetime(y, m, 1).date() for y in [2023, 2024] for m in range(1, 13)]
    x = np.array(range(1, 25))

    ######################
    # Logaritmic Example #
    ######################
    p = np.log(x)*4 + np.random.normal(0, 1, size=[1, 24])
    curve = CmdtyCurve(data={'Time': d, 'Values': list(p[0])})
    classify_fw_curve(curve)

    #######################
    # Exponential Example #
    #######################
    p = 30+x**3/100 + np.random.normal(0, 30, size=[1, 24])
    curve = CmdtyCurve(data={'Time': d, 'Values': list(p[0])})
    classify_fw_curve(curve)

    #########################
    # Soft Increase Example #
    #########################
    p = 5+np.arctan(x)*x + np.random.normal(0, 2, size=[1, 24])
    curve = CmdtyCurve(data={'Time': d, 'Values': list(p[0])})
    classify_fw_curve(curve)

    #########################
    # Soft Decrease Example #
    #########################
    p = 5-np.arctan(-x) + np.random.normal(0, 2, size=[1, 24])
    curve = CmdtyCurve(data={'Time': d, 'Values': list(p[0])})
    classify_fw_curve(curve)
