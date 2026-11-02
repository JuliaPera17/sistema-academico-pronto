# Radar Acadêmico

## Sobre o projeto

O Radar Acadêmico é um projeto desenvolvido por estudantes da Fatec Ourinhos, com o objetivo de utilizar a análise de dados para facilitar o acompanhamento da situação acadêmica dos alunos.

A proposta é reunir informações acadêmicas em um painel visual e interativo, permitindo consultar indicadores, gráficos e informações importantes sobre o desempenho e a situação dos estudantes.

O projeto busca auxiliar professores e coordenação na compreensão dos dados acadêmicos, contribuindo para a identificação de situações que merecem atenção e para a tomada de decisões.

## Objetivo

Desenvolver um produto de dados capaz de organizar e apresentar informações acadêmicas de maneira simples e visual, facilitando o acompanhamento dos estudantes e oferecendo uma visão geral do cenário acadêmico.

## Funcionalidades

O sistema apresenta recursos para consulta e visualização dos dados acadêmicos, incluindo:

- Painel com indicadores acadêmicos;
- Visualização de gráficos;
- Consulta de informações dos estudantes;
- Filtros para facilitar a análise dos dados;
- Acompanhamento de informações relacionadas à situação acadêmica, desempenho e frequência.

## Tecnologias utilizadas

- Python;
- Streamlit;
- Pandas;
- Openpyxl;
- Excel.

## Estrutura do projeto

- `app_sistema_academico_mapa_corrigido.py`: arquivo principal responsável pela aplicação;
- `Sistema Academico (1).xlsx`: base de dados utilizada pelo sistema;
- `requirements.txt`: arquivo com as bibliotecas necessárias para executar o projeto.

## Como acessar o sistema

O Radar Acadêmico está disponível online pelo endereço:

https://sistema-academico.streamlit.app/

Basta acessar o link e aguardar o carregamento da aplicação.

## Como executar o projeto localmente

1. Baixe o repositório pelo GitHub.
2. Extraia os arquivos em uma pasta do computador.
3. Abra a pasta no Visual Studio Code.
4. Abra o terminal dentro da pasta do projeto.
5. Instale as dependências utilizando o comando:

```bash
python -m pip install -r requirements.txt
```

6. Após a instalação, execute:

```bash
python -m streamlit run app_sistema_academico_mapa_corrigido.py
```

7. Aguarde o Streamlit iniciar e abra o endereço local apresentado no terminal.

Caso o comando `python` não funcione no Windows, tente utilizar `py` no lugar dele.

## Limitações do projeto

O Radar Acadêmico é um MVP acadêmico e seus resultados dependem da qualidade e das informações presentes na base de dados utilizada. Atualmente, o sistema apresenta informações descritivas e não realiza uma previsão automática de evasão escolar.

A evolução futura do projeto poderá incluir modelos de aprendizado de máquina para auxiliar na identificação de estudantes com maior risco de evasão.

## Links

- **Sistema online:** https://sistema-academico.streamlit.app/
- **Repositório GitHub:** https://github.com/JuliaPera17/sistema-academico-pronto

Projeto desenvolvido para fins acadêmicos.
