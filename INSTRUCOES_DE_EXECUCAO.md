# Instruções de execução — Radar Acadêmico

## 1. Acesso online

Para acessar o Radar Acadêmico pela internet, basta entrar no endereço:

https://sistema-academico.streamlit.app/

Aguarde o carregamento da página para visualizar o painel e os recursos disponíveis.

## 2. Execução no computador

### Requisitos

- Python instalado;
- Visual Studio Code;
- Arquivos do projeto baixados do GitHub.

### Passo a passo

1. Acesse o repositório do projeto:
   https://github.com/JuliaPera17/sistema-academico-pronto

2. Clique em **Code** e depois em **Download ZIP**.

3. Extraia o arquivo baixado no computador.

4. Abra a pasta extraída no Visual Studio Code.

5. Abra o terminal pelo menu **Terminal → Novo Terminal**.

6. Instale as bibliotecas necessárias:

```bash
python -m pip install -r requirements.txt
```

7. Execute a aplicação:

```bash
python -m streamlit run app_sistema_academico_mapa_corrigido.py
```

8. Após a execução, o Streamlit apresentará um endereço local. Abra esse endereço no navegador para utilizar o sistema.

## 3. Observações

- Mantenha os arquivos do projeto na mesma pasta.
- A planilha Excel é necessária para o funcionamento da aplicação.
- Caso ocorra algum erro, confira se as dependências foram instaladas corretamente.
- O funcionamento deve ser conferido pela equipe antes de registrar os testes como aprovados.
