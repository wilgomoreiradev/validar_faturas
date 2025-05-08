from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import requests

GAS_URL = "https://script.google.com/macros/s/AKfycbxUJCuaEg_wlJzSE7lVBYCrh4WgJEW3g0pZVf3n6L5mhf2TeBiF0sMpfJebHsmkopzpHQ/exec"

app = Flask(__name__)

# Nome do arquivo PDF em static
PDF_FILENAME = 'Guia_Final_Validacao_Faturas_IRS_2025.pdf'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name  = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()

        # Envia para o Google Sheets via Apps Script
        try:
            resp = requests.post(GAS_URL,
                                 json={"name": name, "email": email},
                                 timeout=5)
            resp.raise_for_status()
        except Exception as e:
            app.logger.error(f"Erro ao gravar no Sheets: {e}")

        # Redireciona para disparar o download
        return redirect(url_for('thank_you'))

    return render_template('index.html')


@app.route('/thank_you')
def thank_you():
    # Página de agradecimento que irá redirecionar para o download
    return render_template('thank_you.html')


@app.route('/download')
def download():
    # Caminho absoluto para o PDF em static/
    full_path = os.path.join(app.root_path, 'static', PDF_FILENAME)

    # Verifica se o ficheiro existe
    if not os.path.isfile(full_path):
        from flask import abort
        abort(404)

    # Envia o PDF como anexo
    return send_file(full_path, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)