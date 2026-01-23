import math

def identidade():
    return [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]

def cria_transformacao():
    return identidade()

def translacao(tx, ty):
    return [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ]

def escala(sx, sy):
    return [
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ]

def rotacao(theta):
    c = math.cos(theta)
    s = math.sin(theta)
    return [
        [c, -s, 0],
        [s,  c, 0],
        [0,  0, 1]
    ]

def multiplicar_matrizes(A, B):
    resultado = [[0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                resultado[i][j] += A[i][k] * B[k][j]
    return resultado

#janela p  viewport
def janela_viewport(janela, viewport):
    Wxmin, Wymin, Wxmax, Wymax = janela
    Vxmin, Vymin, Vxmax, Vymax = viewport

    sx = (Vxmax - Vxmin) / (Wxmax - Wxmin)
    sy = (Vymax - Vymin) / (Wymax - Wymin)  # Y para baixo (sem inversão)

    m = identidade()
    m = multiplicar_matrizes(translacao(-Wxmin, -Wymin), m)
    m = multiplicar_matrizes(escala(sx, sy), m)
    m = multiplicar_matrizes(translacao(Vxmin, Vymin), m)
    return m

def aplica_transformacao(m, pontos):
    novos = []
    for x, y in pontos:
        v = [x, y, 1]
        x_novo = m[0][0] * v[0] + m[0][1] * v[1] + m[0][2]
        y_novo = m[1][0] * v[0] + m[1][1] * v[1] + m[1][2]
        novos.append((int(x_novo), int(y_novo)))
    return novos
