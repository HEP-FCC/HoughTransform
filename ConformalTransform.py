import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from scipy import stats
matplotlib.get_configdir()
print(plt.style.available)
plt.style.use('seaborn-poster')
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import AffinityPropagation
# %matplotlib inline


def produceCircle(a, b, R, n, T):
    t = np.linspace(0, T, n)
    x = [a + R * np.cos(i) for i in t]
    y = [b + R * np.sin(i) for i in t]

    return x, y

def conformalTransform(x, y):
    rhit_squared = (x**2 + y**2)
    if rhit_squared:
        xp = x / rhit_squared
        yp = y / rhit_squared
        return xp, yp, rhit_squared
    else:
        return 0, 0, 0

def rho(rhit_squared, xp, yp, phi):
    r = (xp * np.cos(phi) + yp * np.sin(phi))
    return r

def rho_phi(rhit_squared, xp, yp, numpoints):
    phis = np.linspace(0, 2*np.pi, numpoints)
    rhos = [rho(rhit_squared, xp, yp, phi) for phi in phis]
    return phis, rhos

def HoughTransform_phi(Rsquared, Xp, Yp, numpoints, binx, biny, myrange, plotName):

    ht_phi = []
    ht_rho = []
    for i in range(0, len(Xp)):
        phis, rhos = rho_phi(Rsquared[i], Xp[i], Yp[i], numpoints)
        ht_phi.extend(phis)
        ht_rho.extend(rhos)

    H, xedges, yedges = np.histogram2d(ht_phi, ht_rho, bins = (binx, biny))
    am = H.argmax()
    r_idx = am % H.shape[1]
    c_idx = am // H.shape[1]

    trackpos = np.argwhere(H>112)

    print("Above threshold: ", trackpos.shape)
    print(H[trackpos[0][1]][trackpos[0][1]])
    print(trackpos[0][0])
    print(trackpos)

    clustering = AffinityPropagation().fit(trackpos)
    print("labels: ", clustering.labels_)
    print("centers: ", clustering.cluster_centers_)
    # -------------------- #
    # kmeans = KMeans(n_clusters=1, random_state=0).fit(trackpos)
    # print("Labels: ", kmeans.labels_)
    # print("Cluster centers: ", kmeans.cluster_centers_)
    # -------------------- #
    # H[trackpos[0]])
    # print("x index = ", xedges[c_idx])
    # print("y index = ", yedges[r_idx])

    R_ = yedges[r_idx]
    theta_ = xedges[c_idx]

    # print("rho: ", R_)
    # print("phi: ", theta_, ", ", theta_ * 180 /np.pi, " deg")

    # print("Max R = ", max(ht_rho))
    fig_HT_phi = plt.figure()
    h=plt.hist2d(ht_phi, ht_rho, bins=(binx, biny), cmap=plt.cm.jet, range=myrange)
    plt.colorbar(h[3])
    plt.xlabel(r'$\phi$')
    plt.ylabel(r'$\rho$')
    plt.tight_layout()
    plt.show()
    # plt.savefig('plots/'+plotName+'HT.pdf')


    return R_, theta_


def DoFullHT(X, Y, mrange, rangeConf, numpoints=500, binx=200, biny = 200, plotName=""):
    # print("DoFullHT")

    # XY_p = [conformalTransform(X[i], Y[i]) for i in range(0, len(X)) if
    #         conformalTransform(X[i], Y[i])[2]]

    XY_p = [conformalTransform(x, y) for (x, y) in zip(X, Y) if
            conformalTransform(x, y)[2]]

    Xp, Yp, rhit_squared = zip(*XY_p)
    fig_conformalTransform = plt.figure()
    plt.scatter(Xp, Yp, c = 'DarkBlue', linestyle='-')
    plt.title("Conformal transform")
    plt.legend(loc='upper left')
    plt.xlabel("u")
    plt.ylabel("v")
    # print("rangeCOnf: ", rangeConf[0])
    plt.xlim(rangeConf[0])
    plt.ylim(rangeConf[1])
    plt.tight_layout()
    # plt.show()
    # plt.savefig('plots/'+plotName+'Conformal.pdf')

    R_, theta_ = HoughTransform_phi(Rsquared=rhit_squared, Xp=Xp, Yp=Yp,
                                    numpoints=numpoints,
                                    binx=binx, biny=biny, myrange=mrange, plotName = plotName)
    radius_calc = 1./(2*R_)
    a_calc = np.cos(theta_)/(2*R_)
    b_calc = np.sin(theta_)/(2*R_)

    # print("a =", a_calc)
    # print("b =", b_calc)
    # print("radius=", radius_calc)

    return radius_calc, a_calc, b_calc, theta_
