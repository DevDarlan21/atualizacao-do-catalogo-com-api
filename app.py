import json
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'chave_secreta_para_sessoes'

# Dados dos produtos
produtos = [
    {
        "nome": "Controle Remoto Xplus Sat",
        "descricao": "Controle remoto para seu aparelho Xplus Sat!",
        "preco": "R$ 24,99",
        "imagem": "imagens/Xplus.png"
    },
    {
        "nome": "Controle Remoto GlobalSat GS-240",
        "descricao": "Controle remoto para seu aparelho GlobalSat",
        "preco": "R$ 24,99",
        "imagem": "imagens/GlobalSat.png"
    },
    # ... outros produtos ...
    {
        "nome": "Controle Remoto Tv CCE Tubo",
        "descricao": "Controle remoto para o seu televisor de tubo CCE",
        "preco": "R$ 19,99",
        "imagem": "imagens/Cce Tubo.png"
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html', produtos=produtos, carrinho=session.get('carrinho', []))

@app.route('/carrinho')
def ver_carrinho():
    carrinho = session.get('carrinho', [])
    total = sum(float(item['preco'].replace('R$ ', '').replace(',', '.')) * item['quantidade'] for item in carrinho)
    return render_template('carrinho.html', carrinho=carrinho, total=total)

@app.route('/adicionar_ao_carrinho', methods=['POST'])
def adicionar_ao_carrinho():
    produto_nome = request.form['produto_nome']
    produto_preco = request.form['produto_preco']
    quantidade = int(request.form['quantidade'])  # Obtém a quantidade

    # Inicializa o carrinho na sessão, se necessário
    if 'carrinho' not in session:
        session['carrinho'] = []

    # Verifica se o produto já está no carrinho
    for item in session['carrinho']:
        if item['nome'] == produto_nome:
            item['quantidade'] += quantidade  # Incrementa a quantidade
            break
    else:
        # Se não estiver no carrinho, adiciona um novo item
        session['carrinho'].append({"nome": produto_nome, "preco": produto_preco, "quantidade": quantidade})

    # Salva o carrinho atualizado na sessão
    session.modified = True

    return redirect(url_for('catalogo'))

@app.route('/remover_do_carrinho', methods=['POST'])
def remover_do_carrinho():
    produto_nome = request.form['produto_nome']
    quantidade = int(request.form['quantidade'])  # Obtém a quantidade

    # Verifica se o produto está no carrinho
    for item in session['carrinho']:
        if item['nome'] == produto_nome:
            item['quantidade'] -= quantidade  # Decrementa a quantidade
            if item['quantidade'] <= 0:
                session['carrinho'].remove(item)  # Remove o item se a quantidade for zero ou negativa
            break

    # Salva o carrinho atualizado na sessão
    session.modified = True

    # Redireciona para o carrinho
    return redirect(url_for('ver_carrinho'))


@app.route('/finalizar_compra')
def finalizar_compra():
    carrinho = session.get('carrinho', [])
    if not carrinho:
        return redirect(url_for('ver_carrinho'))

    # Gera a mensagem para o WhatsApp
    mensagem = "Meu Carrinho:\n"
    total = 0.0

    for item in carrinho:
        mensagem += f"{item['nome']} - {item['preco']} (Quantidade: {item['quantidade']})\n"
        total += float(item['preco'].replace('R$ ', '').replace(',', '.')) * item['quantidade']

    mensagem += f"Total: R$ {total:.2f}"

    # Substitua <número> pelo número desejado
    numero_whatsapp = "<+55 32 998501030>"  # Insira o número de telefone no formato internacional
    url_whatsapp = f"https://chat.whatsapp.com/BoyWqZL7y7vBMrEFHjsYJJ={numero_whatsapp}&text={mensagem.replace(' ', '%20').replace('\n', '%0A')}"

    # Redireciona para a URL do WhatsApp
    return redirect(url_whatsapp)


if __name__ == '__main__':
    app.run(debug=True)
