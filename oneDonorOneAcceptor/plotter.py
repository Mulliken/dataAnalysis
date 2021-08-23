import itertools as it
from os import path

import matplotlib as mpl
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import AutoLocator
print('matplotlib: {}'.format(mpl.__version__))


mpl.style.use('default')
# prop_cycle = plt.rcParams['axes.prop_cycle']
# colors = prop_cycle.by_key()['color']
colors = ['#E24A33', '#348ABD', '#988ED5', '#777777', '#FBC15E', '#8EBA42', '#FFB5B8']
colors_mma_scien = [
    (0.9, 0.36, 0.054),
    (0.365248, 0.427802, 0.758297),
    (0.945109, 0.593901, 0.0),
    (0.645957, 0.253192, 0.685109),
    (0.285821, 0.56, 0.450773),
    (0.7, 0.336, 0.0),
    (0.491486, 0.345109, 0.8),
    (0.71788, 0.568653, 0.0),
    (0.70743, 0.224, 0.542415),
    (0.287228, 0.490217, 0.664674),
    (0.982289285128704, 0.5771321368979874, 0.011542503255145636),
    (0.5876740325800278, 0.2877284499870081, 0.7500695697462922),
    (0.4262088601796793, 0.5581552810007578, 0.2777996730417023),
    (0.9431487543762861, 0.414555896337833, 0.07140829055870854)
]

colors_mma_detai = [(0.368417, 0.506779, 0.709798), (0.880722, 0.611041, 0.142051), (0.560181, 0.691569, 0.194885),
                    (0.922526, 0.385626, 0.209179), (0.528488, 0.470624, 0.701351), (0.772079, 0.431554, 0.102387),
                    (0.363898, 0.618501, 0.782349), (0.647624, 0.37816, 0.614037), (0.571589, 0.586483, 0.0),
                    (0.915, 0.3325, 0.2125), (0.9728288904374106, 0.621644452187053, 0.07336199581899142),
                    (0.736782672705901, 0.358, 0.5030266573755369)]

font = {'family': 'Latin Modern Sans',
        'size': 10}
mpl.rc('font', **font)


def pop_grid(inPlotVars=None, xGridVars=None, yLimit=(0, 1), direc='',
             yGridVars=None, labelFontSize=3, figureWidth=3.375 * 2*1.5, aspectRatio=1.5, figName="para"):
    fig_pop = plt.figure(dpi=1000, figsize=(figureWidth, figureWidth * aspectRatio))
    yGridLen = len(yGridVars)
    xGridLen = len(xGridVars)
    gs = fig_pop.add_gridspec(xGridLen, yGridLen, hspace=0.001, wspace=0.001)
    grid = gs.subplots(sharex='col', sharey='row', squeeze=False)
    # y_ticks = [[0.3, 0.5, 0.7, 0.9], [0.3, 0.5, 0.7, 0.9, 1.0], [0.3, 0.5, 0.7, 0.9], [0.3, 0.5, 0.7, 0.9]]
    # x_ticks = [[0, 2.5], [0, 2.5, 5]]
    line_geom = ('solid', (0, (0.001, 1.5)), (0, (1.2, 1.2)), (0, (2.5, 2, 2.5, 1)))
    timeStepSize = 1
    for m, n in it.product(range(xGridLen), range(yGridLen)):
        pop = []
        legends = []
        linestyle_str = []
        for i, inPlotVar in enumerate(inPlotVars):
            file = f'{direc}/pop_{yGridVars[n]}_T{inPlotVars[i]}_E{xGridVars[m]}.dat'
            linestyle_str.append(line_geom[i])
            legends.append(f"T = {inPlotVar}")
            if path.exists(file):
                b = np.fromfile(file, np.float32)
                # b = np.insert(b, 0, 1.0)
                # b = b[::10]
                b = ([i * 0.05 / timeStepSize for i in range(len(b))], b)
                print(b[0][-1], len(b[1]))
                pop.append((b))
                print(f"{direc}/pop_{yGridVars[n]}_T{inPlotVars[i]}_E{xGridVars[m]}.dat EXISTS")
            else:
                print(f"{direc}/pop_{yGridVars[n]}_T{inPlotVars[i]}_E{xGridVars[m]}.dat NOT EXISTS")

        linestyle_str = linestyle_str * len(colors_mma_detai)
        colors_pop = colors_mma_detai * int(len(linestyle_str)/len(colors_mma_detai))

        # grid[m, n].tick_params(axis="y", direction="in", width=.5, length=1, labelleft=True)
        grid[m, n].tick_params(axis="x", direction="in", width=.5, length=1, labelbottom=False)
        # grid[m, n].set_prop_cycle(color=colors_pop, linestyle=linestyle_str)
        grid[m, n].text(0.98, 0.06, f"$\epsilon:{xGridVars[m]}$\n$\omega_c: {yGridVars[n]}$",
                        transform=grid[m, n].transAxes, ha='right', fontsize=labelFontSize)
        # grid[m,n].grid(False)
        # grid[m,n].text(.1,.8, geom[m].upper()+str(phys_d[n]),
        # transform=grid[m,n].transAxes)
        # grid[m,n].set_xticks(x_ticks[n])
        grid[m,n].xaxis.set_major_locator(plt.MaxNLocator(4))
        # grid[m,n].set_yticks(ytick[m])
        for cur in pop:
            grid[m, n].plot(*cur, lw=0.5, solid_capstyle='round', dash_capstyle='round', dash_joinstyle='bevel')

        [i.set_linewidth(.5) for i in grid[m,n].spines.values()]
        # grid[m, n].set_xlim([0, b[0][-1]])
        grid[m, n].set_ylim(yLimit)
        grid[m, n].legend(list(legends), loc="lower left", ncol=1, frameon=False,
                          handlelength=1.2, columnspacing=0.3, handletextpad=0.2,
                          fontsize=labelFontSize, borderaxespad=0)
    fig_pop.text(0, 0.5, r'$\rho_{\uparrow}$', ha='left', usetex=True, fontsize=5)
    fig_pop.text(0.55, 0, r'$t\Delta/\pi$', ha='center', usetex=True, fontsize=5)
    fig_pop.subplots_adjust(left=0.12, right=0.97, bottom=0.12, top=0.97)
    # fig_pop.show()

    # ax.set_aspect(aspect=70,adjustable='box')
    # ax.set_xlabel('$t\Delta/\pi$',usetex=True)
    # ax.text(0.98,0.06, f'$\eta_0={coup}$, $\omega_0={freq_}$, $T={tmp_}$',
    # transform=ax.transAxes,ha='right',usetex=True,fontsize=10)

    # fig_pop.tight_layout(w_pad=0,pad=0,h_pad=0,rect=[0,0,1,1])
    # fig_pop.tight_layout()
    # fig_pop.subplots_adjust(left=0,right=1,bottom=0,top=1)
    # ax.set_axis_off()

    plt.savefig(f'{figName}.png')  # ,bbox_inches='tight',pad_inches=0)
    print(f"Finished Drawing {figName}")

tempList = [5, 90, 200, 300]
energyList = np.arange(-2500, 8501, 500)
geomList = ['ic', 'star']
pop_grid(inPlotVars=tempList, xGridVars=energyList, yGridVars=geomList, yLimit=[0., 1],
         direc='./output', figName='DA1', aspectRatio=6, figureWidth=3.375)

