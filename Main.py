import numpy as np
import pandas as pd
import ternary

def generate_ternary_data():
    l = []
    for i in np.arange(0.0, 6.1, 0.2):
        for j in np.arange(0.0, 6.1, 0.2):
            l.append([i, j, 100 - (i + j)])
    lp = pd.DataFrame(l)
    lp.to_excel("Ternary-Zn-Ca.xlsx")

    tr = pd.read_excel('Ternary-Zn-Y.xlsx')
    return tr

def calculate_column_sums(df, column_list):
    return df[column_list].sum(axis=1)

def generate_ternary_phases(tr):
    sum_column_dict = {
        'Sr': ['Sr2Mg17(s)', 'Sr5Si3(s)', 'SrZn5(s)', 'Sr2Zn43Mg55(s)'],
        'Zn': ['Mg12Zn13(s)', 'Ca2Mg55Zn43(s)', 'SrZn5(s)', 'Sr2Zn43Mg55(s)', 'YZnMg12(s)', 'Zn2Zr(s)', 'ZnZr(s)',
               'Nd3Zn22(s)', 'NdZn2Mg(s)', 'Nd2Zn9Mg5(s)', 'NdZn2Al2(s)', 'GdZnMg12(s)'],
        'Nd': ['Nd5Mg41(s)', 'Nd3Al11(s)', 'Nd3Zn22(s)', 'NdZn2Mg(s)', 'Nd2Zn9Mg5(s)', 'NdZn2Al2(s)'],
        'Ca': ['Mg2Ca(s)', 'Al2Ca(s)', 'CaMgSi(s)', 'Mn2CaAl10(s)', 'Ca2Mg55Zn43(s)'],
        'Y': ['Y(s)', 'AlY(s)', 'Al3Y(s)', 'Al2Y3(s)', 'Y6Mn23(s)', 'YZnMg12(s)'],
        'Mn': ['Mn(s)', 'Al4Mn(s)', 'Al11Mn4(s)', 'Mn3Si(s)', 'Mn5Si3(s)', 'Mn2CaAl10(s)', 'Al7CuMn2(s)', 'Y6Mn23(s)',
               'Mn2Zr(s)'],
        'Zr': ['Zr(s)', 'Al3Zr(s)', 'Mn2Zr(s)', 'ZnZr(s)', 'Zn2Zr(s)'],
        'Al': ['Al30Mg23(s)', 'Al2Ca(s)', 'Mn2CaAl10(s)', 'Al7Cu3Mg6(s)', 'Al5Cu6Mg2(s)', 'Al7CuMn2(s)', 'AlY(s)',
               'Al3Y(s)', 'Al2Y3(s)', 'Al3Zr(s)', 'Nd3Al11(s)', 'NdZn2Al2(s)'],
        'Si': ['Mg2Si(s)', 'CaMgSi(s)', 'Mn3Si(s)', 'Mn5Si3(s)', 'Sr5Si3(s)'],
        'Cu': ['Mg2Cu(s)', 'Al7Cu3Mg6(s)', 'Al5Cu6Mg2(s)', 'Al7CuMn2(s)'],
        'Gd': ['GdMg5(s)', 'GdZnMg12(s)']
}

ternary_phases = {}

for phase, column_list in sum_column_dict.items():
    ternary_phases[phase] = calculate_column_sums(tr, column_list)

tr['Alkline'] = ternary_phases['Sr'] + ternary_phases['Ca']
tr['Transition'] = (
        ternary_phases['Zr'] + ternary_phases['Y'] + ternary_phases['Mn'] + ternary_phases['Zn'] +
        ternary_phases['Cu']
)
tr['Lanthanides'] = ternary_phases['Nd'] + ternary_phases['Gd']
tr['Post-transition'] = ternary_phases['Al']
tr['Metalloids'] = ternary_phases['Si']
tr["SUM"] = (
        tr["Alkline"] + tr["Transition"] + tr["Lanthanides"] + tr["Post-transition"] + tr["Metalloids"]
)

tr = tr.drop(tr.iloc[:, 12:52], axis=1)
first_col = tr.pop("Heat Treatment")
tr.insert(17, "Heat Treatment", first_col)

tr.dropna(inplace=True)
return tr

c = 0
l = []
for i, j, k in tr_plot_arr:
    if i + j > 6.01:
        l.append(c)
    c += 1

tr_plot_new = np.delete(tr_plot_arr, l, 0)
data = {}

c = 0
for (i, j, k) in ternary.simplex_iterator(30):
    data[(i, j)] = tr_plot_new[c, 2]
    c += 1

scale = 30
figure, tax = ternary.figure(scale=scale)
figure.set_size_inches(8, 6)
tax.heatmap(data, style="h")
tax.boundary()

tax.set_title("Mg-Ca-Zn Ternary Phase Diagram", fontsize=12)
tax.left_axis_label("Mg", fontsize=8, offset=0.05)
tax.right_axis_label("Y", fontsize=8, offset=0.05)
tax.bottom_axis_label("Zn", fontsize=8, offset=-0.15)

tax.get_axes().axis('off')
tax.clear_matplotlib_ticks()
tax.show()

