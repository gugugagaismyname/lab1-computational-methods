# Модель: Математичне моделювання розподілу забруднюючих речовин між повітрям, водою та ґрунтом (5 семестр)
# Автор: Апанович Герман, група АІ231

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/calculate', methods=['GET'])
def calculate():

    E = float(request.args.get('E', 100))

    k_aw = 0.05
    k_ws = 0.02
    k_deg = 0.005

    Va = 1e6
    Vw = 1e3
    Vs = 1e4

    t_max = 500
    dt = 0.1
    steps = int(t_max / dt)

    Ma = 0
    Mw = 0
    Ms = 0

    for i in range(steps):

        dMa = k_aw * (Mw - Ma) - k_deg * Ma + E
        dMw = k_aw * (Ma - Mw) + k_ws * (Ms - Mw) - k_deg * Mw
        dMs = k_ws * (Mw - Ms) - k_deg * Ms

        Ma += dMa * dt
        Mw += dMw * dt
        Ms += dMs * dt

    Ca = Ma / Va
    Cw = Mw / Vw
    Cs = Ms / Vs

    return jsonify({
        "E": E,
        "Ca": Ca,
        "Cw": Cw,
        "Cs": Cs
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)