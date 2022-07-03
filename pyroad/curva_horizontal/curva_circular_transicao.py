import math

from flask import request, Blueprint

curva_circular_transicao_bp = Blueprint('curva_circular_transicao', __name__)
curva_circular_transicao_resultados_bp = Blueprint('curva_circular_transicao_resultados', __name__)


@curva_circular_transicao_bp.route('/curva-circular-transicao', methods=['POST'])
def curva_circular_simples():
    # get data from request
    AC, PI, Raio, Vp, e, lf = entrada_cct()

    # Calculo do Ls
    Ls_min, Ls_desej, Ls_max = calculo_ls(AC, Raio, Vp, e, lf)

    print(Ls_min, Ls_desej, Ls_max)

    Ls = ls_adotado()

    Lc = escolha_lc(AC, Raio, Ls)

    return Lc


@curva_circular_transicao_resultados_bp.route('/curva-circular-transicao/resultados', methods=['POST'])
def curva_circular_transicao_resultados():
    # calculate
    Xs, Ys, k, p, TT, E, teta_c, D, TS, SC, CS, ST = calculo_cct(AC, PI, Raio, Lc, Ls)

    # create dataframe
    # df = tabela(PC_int, PT_int, PC_resto, PT_resto, d_m, PC_est, PT_est)

    # return data
    saida = saida_cct(Xs, Ys, k, p, TT, E, teta_c, D, TS, SC, CS, ST)

    return saida


def entrada_cct():
    AC = request.json.get('AC')
    PI = request.json.get('PI')
    Raio = request.json.get('Raio')
    Vp = request.json.get('Vp')
    e = request.json.get('e')
    lf = request.json.get('lf')
    return AC, PI, Raio, Vp, e, lf


def calculo_ls(AC, Raio, Vp, e, lf):
    # Calculo dos Ls mínimos
    Ls_min_conforto = 0.036 * (Vp ** 3) / Raio
    Ls_min_seguranca = Vp / 1.8
    Ls_min_estetico = lf * e / (0.71 - 0.0026 * Vp)

    # Entre os três valores, pega-se o maior deles como Ls mínimo
    Ls_min = max(Ls_min_estetico, Ls_min_seguranca, Ls_min_conforto)

    # Calculando o Ls máximo
    Ls_max = Raio * AC * math.pi / 180

    # Ls desejável
    Ls_desej = 0.072 * Vp ** 3 / Raio

    return Ls_min, Ls_desej, Ls_max


def ls_adotado():
    Ls_adotado = request.json.get('LS')
    return Ls_adotado


def escolha_lc(AC, Raio, Ls):
    # Cálculo de Lc, para comparação ao adotar o Ls
    teta_s = Ls / 2 * Raio
    teta_c = AC - 2 * teta_s
    Lc = Raio * teta_c * math.pi / 180
    return Lc


def calculo_cct(AC, PI, Raio, Lc, Ls):
    # calculo dos elementos da curva circular com transição
    teta_s = Ls / 2 * Raio
    Xs = Ls * (1 - (teta_s ** 2 / 10) + (teta_s ** 4 / 216))
    Ys = Ls * ((teta_s / 3) - (teta_s ** 3 / 42))
    k = Xs - Raio * math.sin(teta_s)
    p = Ys - Raio * (1 - math.cos(teta_s))

    TT = k + (Raio + p) * math.tan(AC / 2)
    TT_int = TT // 20
    TT_resto = round(((TT / 20) - TT_int) * 20, 2)

    PI_int = PI // 20
    PI_resto = round(((PI / 20) - PI_int) * 20, 2)

    E = ((Raio + p) / (math.cos(AC / 2))) - Raio

    # Trecho Circular
    teta_c = AC - 2 * teta_s

    # Desenvolvimento Total
    D = Lc + 2 * Ls

    # Estacas Notáveis
    TS = PI - TT
    TS_int = (PI - TT) // 20
    TS_resto = round(((TS / 20) - TS_int) * 20, 2)

    SC = TS + Ls
    SC_int = SC // 20
    SC_resto = round(((SC / 20) - SC_int) * 20, 2)

    CS = SC + Lc
    CS_int = CS // 20
    CS_resto = round(((CS / 20) - CS_int) * 20, 2)

    ST = CS + Ls
    ST_int = ST // 20
    ST_resto = round(((ST / 20) - ST_int) * 20, 2)

    return Xs, Ys, k, p, TT, E, teta_c, D, TS, SC, CS, ST


# def tabela_cct(PC_int, PT_int, PC_resto, PT_resto, d_m, PC_est, PT_est):
#     df = pd.DataFrame(
#         columns=['ESTACA', 'CORDA'])
#
#     df['ESTACA'] = [PC_est] + list(range(PC_int + 1, PT_int + 1)) + [PT_est]
#     df['CORDA'] = [np.nan] + [20 - PC_resto] + [20] * (len(df) - 3) + [PT_resto]  # foi subtraído 3, pois possui o
#     # 'nan' e o PC_est e PT_est
#     df['DEFLEXÃO PARCIAL'] = df['CORDA'] * d_m
#     df['DEFLEXÃO PARCIAL_GMS'] = df['DEFLEXÃO PARCIAL'].apply(decdeg2dms)
#     df['DEFLEXÃO_TOTAL'] = df['DEFLEXÃO PARCIAL'].cumsum().apply(decdeg2dms)
#
#     print(df)
#     return df


def saida_cct(Xs, Ys, k, p, TT, E, teta_c, D, TS, SC, CS, ST):
    saida = {'Xs': Xs,
             'Ys': Ys,
             'k': k,
             'p': p,
             'TT': TT,
             'E': E,
             'teta_c': teta_c,
             'D': D,
             'TS_est': TS,
             'SC_est': SC,
             'CS_est': CS,
             'ST_est': ST}
    return saida
