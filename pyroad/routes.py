import math

import numpy as np
import pandas as pd
from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin

from pyroad.util import format_zeros, round_values
from pyroad.util.Angulo import Angulo

app = Flask(__name__)
CORS(app)


@cross_origin()
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route('/curva-circular-simples', methods=['POST'])
def curva_circular_simples():
    # get data from request
    AC, PI, Raio, Vp, e_max = entrada_ccs()

    # calculate
    D, E, G_20_str, PC_est, PI_estaca, PT_est, T_estaca, d_20_str, d_m_str, ft_max, raio_min, PC_int, PT_int, PC_resto, PT_resto, d_m = calculo_ccs(
        AC, PI, Raio,
        Vp, e_max)

    # create dataframe
    df = tabela(PC_int, PT_int, PC_resto, PT_resto, d_m, PC_est, PT_est)

    # return data
    saida = saida_ccs(D, E, G_20_str, PC_est, PI_estaca, PT_est, T_estaca, d_20_str, d_m_str, ft_max, raio_min, df)

    return saida


def entrada_ccs():
    AC = request.json.get('AC')
    PI = request.json.get('PI')
    Raio = request.json.get('Raio')
    Vp = request.json.get('Vp')
    e_max = request.json.get('e_max')
    return AC, PI, Raio, Vp, e_max


def calculo_ccs(AC, PI, Raio, Vp, e_max):
    ft_max = round(0.19 - Vp / 1600, 2)
    raio_min = round(Vp ** 2 / (127 * ((e_max / 100) + ft_max)), 2)
    AC_rad = math.radians(AC)
    T = Raio * math.tan(AC_rad / 2)
    D = round(Raio * AC * math.pi / 180, 2)
    E = round(T * math.tan(AC_rad / 4), 2)
    G_20 = round(1145.92 / Raio, 5)
    G_20_str = str(G_20) + str('°')
    d_20 = round(G_20 / 2, 5)
    d_20_str = str(d_20) + str('°')
    d_m = round(d_20 / 20, 5)
    d_m_str = str(d_m) + str('°')
    T_int = T // 20
    T_resto = round(((T / 20) - T_int) * 20, 2)
    T_estaca = str(T_int) + str(' + ') + str(T_resto)
    PI_int = PI // 20
    PI_resto = round(((PI / 20) - PI_int) * 20, 2)
    PI_estaca = str(PI_int) + str(' + ') + str(PI_resto)
    PC = PI - T
    PC_int = PC // 20
    PC_resto = round(((PC / 20) - PC_int) * 20, 2)
    PC_est = str(PC_int) + str(' + ') + str(PC_resto)
    PT = PC + D
    PT_int = PT // 20
    PT_resto = round(((PT / 20) - PT_int) * 20, 2)
    PT_est = str(PT_int) + str(' + ') + str(PT_resto)

    return D, E, G_20_str, PC_est, PI_estaca, PT_est, T_estaca, d_20_str, d_m_str, ft_max, raio_min, int(PC_int), int(
        PT_int), PC_resto, PT_resto, d_m


def tabela(PC_int, PT_int, PC_resto, PT_resto, d_m, PC_est, PT_est):
    estaca_str = 'ESTACA'
    corda_str = 'CORDA (m)'
    deflexao_parcial_str = 'DEFLEXÃO PARCIAL (°)'
    deflecao_parcial_gmc_str = 'DEFLEXÃO PARCIAL (° \' ")'
    deflexao_total_str = 'DEFLEXÃO TOTAL (° \' ")'

    df = pd.DataFrame(columns=[estaca_str, corda_str])

    df[estaca_str] = [PC_est] + list(range(PC_int + 1, PT_int + 1)) + [PT_est]
    df[corda_str] = [np.nan] + [20 - PC_resto] + [20] * (len(df) - 3) + [PT_resto]  # foi subtraído 3, pois possui o
    # 'nan' e o PC_est e PT_est
    df[deflexao_parcial_str] = df[corda_str] * d_m
    df[deflecao_parcial_gmc_str] = df[deflexao_parcial_str].apply(decdeg2dms)
    df[deflexao_total_str] = df[deflexao_parcial_str].cumsum().apply(decdeg2dms)
    df = df.fillna('-').applymap(round_values).applymap(format_zeros)

    print(df)
    return df


def saida_ccs(D, E, G_20_str, PC_est, PI_estaca, PT_est, T_estaca, d_20_str, d_m_str, ft_max, raio_min, df):
    saida = {'ft_max': ft_max,
             'raio_min': raio_min,
             'T_estaca': T_estaca,
             'D': D,
             'E': E,
             'G_20': G_20_str,
             'd_20': d_20_str,
             'd_m': d_m_str,
             'PI_est': PI_estaca,
             'PC_est': PC_est,
             'PT_est': PT_est,
             'tabela': df.to_html(index=False)}
    return saida


# transform decimal degrees to decimal minutes and seconds
def decdeg2dms(dd):
    mnt, sec = divmod(dd * 3600, 60)
    deg, mnt = divmod(mnt, 60)
    return Angulo(deg, mnt, sec)
