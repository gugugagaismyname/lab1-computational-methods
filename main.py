# Модель: Розподіл забруднюючих речовин (5 семестр)
# Автор: Апанович Герман, група АІ231

import numpy as np
import matplotlib.pyplot as plt

# Параметри моделі
k_aw = 0.05        # коефіцієнт масообміну повітря–вода
k_ws = 0.02        # коефіцієнт масообміну вода–ґрунт
k_deg = 0.005      # коефіцієнт деградації
E = 100            # емісія в атмосферу (кг/добу)

Va = 1e6           # об’єм повітря
Vw = 1e3           # об’єм води
Vs = 1e4           # об’єм ґрунту

t_max = 500
dt = 0.1
steps = int(t_max / dt)

# Початкові умови
Ma = 0
Mw = 0
Ms = 0

time = []
A = []
W = []
S = []

# Чисельне інтегрування методом Ейлера
for i in range(steps):
    dMa = k_aw * (Mw - Ma) - k_deg * Ma + E
    dMw = k_aw * (Ma - Mw) + k_ws * (Ms - Mw) - k_deg * Mw
    dMs = k_ws * (Mw - Ms) - k_deg * Ms

    Ma += dMa * dt
    Mw += dMw * dt
    Ms += dMs * dt

    time.append(i * dt)
    A.append(Ma)
    W.append(Mw)
    S.append(Ms)

# Концентрації
Ca = Ma / Va
Cw = Mw / Vw
Cs = Ms / Vs

print("Кінцеві концентрації:")
print("Ca =", Ca, "кг/м^3")
print("Cw =", Cw, "кг/м^3")
print("Cs =", Cs, "кг/м^3")

# Графік
plt.plot(time, A, label="Маса в атмосфері")
plt.plot(time, W, label="Маса у воді")
plt.plot(time, S, label="Маса в ґрунті")
plt.xlabel("Час, доби")
plt.ylabel("Маса, кг")
plt.legend()
plt.grid()
plt.show()

# Концентрації у часі
Ca_t = np.array(A) / Va
Cw_t = np.array(W) / Vw
Cs_t = np.array(S) / Vs

plt.figure()
plt.plot(time, Ca_t, label="Концентрація в атмосфері")
plt.plot(time, Cw_t, label="Концентрація у воді")
plt.plot(time, Cs_t, label="Концентрація у ґрунті")
plt.xlabel("Час, доби")
plt.ylabel("Концентрація, кг/м^3")
plt.legend()
plt.grid()
plt.show()

# Відносний розподіл маси
total_mass = np.array(A) + np.array(W) + np.array(S)

plt.figure()
plt.plot(time, np.array(A) / total_mass, label="Частка в атмосфері")
plt.plot(time, np.array(W) / total_mass, label="Частка у воді")
plt.plot(time, np.array(S) / total_mass, label="Частка у ґрунті")
plt.xlabel("Час, доби")
plt.ylabel("Відносна частка")
plt.legend()
plt.grid()
plt.show()

dA = np.gradient(A, dt)
dW = np.gradient(W, dt)
dS = np.gradient(S, dt)

plt.figure()
plt.plot(time, dA, label="dMa/dt")
plt.plot(time, dW, label="dMw/dt")
plt.plot(time, dS, label="dMs/dt")
plt.xlabel("Час, доби")
plt.ylabel("Швидкість зміни маси, кг/добу")
plt.legend()
plt.grid()
plt.show()

E_values = [50, 100, 200]
results = {}

for E_test in E_values:
    Ma = Mw = Ms = 0
    A_t, W_t, S_t = [], [], []

    for i in range(steps):
        dMa = k_aw * (Mw - Ma) - k_deg * Ma + E_test
        dMw = k_aw * (Ma - Mw) + k_ws * (Ms - Mw) - k_deg * Mw
        dMs = k_ws * (Mw - Ms) - k_deg * Ms

        Ma += dMa * dt
        Mw += dMw * dt
        Ms += dMs * dt

        A_t.append(Ma)
        W_t.append(Mw)
        S_t.append(Ms)

    results[E_test] = (A_t, W_t, S_t)

plt.figure()
for E_test in E_values:
    plt.plot(time, results[E_test][1], label=f"E = {E_test} кг/добу")

plt.xlabel("Час, доби")
plt.ylabel("Маса у воді, кг")
plt.legend()
plt.grid()
plt.show()

threshold = 1e-3
steady_time = None

for i in range(len(dA)):
    if abs(dA[i]) < threshold and abs(dW[i]) < threshold and abs(dS[i]) < threshold:
        steady_time = time[i]
        break

print("Час досягнення стаціонарного режиму:", steady_time, "діб")