"""Dashboard acadêmico para apresentação — Streamlit + Pandas + Plotly.
Coloque 'Sistema Academico (1).xlsx' na mesma pasta deste arquivo.
"""
import html
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

st.set_page_config(page_title="Sistema Acadêmico | Inteligência Acadêmica", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

BASE = Path(__file__).resolve().parent / "Sistema Academico (1).xlsx"
ABA = "base_dados_academicos"
NECESSARIAS = ["id_aluno", "curso", "disciplina", "situacao_matricula", "situacao_disciplina", "media_final", "frequencia_pct"]
C = {"fundo": "#0f172a", "painel": "#1e293b", "texto": "#f8fafc", "muted": "#94a3b8", "borda": "#334155", "azul": "#60a5fa", "verde": "#34d399", "laranja": "#fbbf24", "vermelho": "#fb7185", "roxo": "#a78bfa"}

st.markdown("""
<style>
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {background:#0f172a!important;color:#f8fafc!important;}
[data-testid="stSidebar"] {background:#162338!important;border-right:1px solid #334155;}
.block-container {max-width:1500px;padding-top:1.4rem;padding-bottom:3rem;}
.hero {background:linear-gradient(112deg,#1e3a8a,#1d4ed8 57%,#3730a3);padding:25px 30px;border-radius:20px;margin-bottom:19px;border:1px solid #3b82f6;}
.hero h1 {font-size:2.05rem;margin:0;color:#fff!important;letter-spacing:-.7px;}
.hero p {margin:7px 0 0;color:#dbeafe!important;}
.section-title {font-size:1.23rem;font-weight:750;color:#f8fafc;margin:24px 0 12px;}
.metric-card {background:#1e293b;border:1px solid #334155;border-radius:15px;padding:17px 19px;min-height:118px;}
.metric-label {font-size:.81rem;color:#94a3b8;font-weight:600;}
.metric-value {font-size:1.82rem;color:#f8fafc;font-weight:800;margin-top:10px;}
.metric-hint {font-size:.73rem;color:#94a3b8;margin-top:3px;}
.insight {background:#1e293b;border:1px solid #334155;border-left:4px solid #60a5fa;padding:15px 19px;border-radius:12px;margin:9px 0;line-height:1.65;color:#e2e8f0;}
div[data-testid="stPlotlyChart"] {background:#1e293b;border:1px solid #334155;border-radius:15px;padding:8px;}
[data-testid="stMetricValue"] {color:#f8fafc!important;}
[data-testid="stMetricLabel"] {color:#94a3b8!important;}
[data-testid="stTabs"] button {font-weight:650;}
</style>
""", unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def carregar(caminho: str, atualizado_em: float) -> pd.DataFrame:
    return pd.read_excel(caminho, sheet_name=ABA)

if not BASE.exists():
    st.error(f"Planilha não encontrada: {BASE.name}. Coloque-a na mesma pasta do arquivo Python.")
    st.stop()
try:
    df = carregar(str(BASE), BASE.stat().st_mtime)
except Exception as erro:
    st.error(f"Não foi possível ler a aba '{ABA}': {erro}")
    st.stop()
faltantes = [c for c in NECESSARIAS if c not in df.columns]
if faltantes:
    st.error("Colunas ausentes na planilha: " + ", ".join(faltantes))
    st.stop()
for campo in ["curso", "disciplina", "situacao_matricula", "situacao_disciplina"]:
    df[campo] = df[campo].astype("string").str.strip()
for campo in ["media_final", "frequencia_pct"]:
    df[campo] = pd.to_numeric(df[campo], errors="coerce")
# Na base original frequência é uma fração (0 a 1).
df["frequencia_percentual"] = df["frequencia_pct"] * (100 if not df["frequencia_pct"].dropna().gt(1).any() else 1)


def num(v, casas=1):
    return f"{v:.{casas}f}".replace(".", ",") if pd.notna(v) else "—"


def pct(parte, todo):
    return parte / todo * 100 if todo else 0.0


def titulo(s):
    st.markdown(f'<div class="section-title">{html.escape(s)}</div>', unsafe_allow_html=True)


def card(label, value, color, hint=""):
    st.markdown(f'<div class="metric-card" style="border-top:4px solid {color}"><div class="metric-label">{html.escape(label)}</div><div class="metric-value">{html.escape(str(value))}</div><div class="metric-hint">{html.escape(hint)}</div></div>', unsafe_allow_html=True)


def tema(fig, altura=390):
    fig.update_layout(template="plotly_dark", paper_bgcolor=C["painel"], plot_bgcolor=C["painel"], font=dict(color=C["texto"], size=12), height=altura, margin=dict(l=30, r=35, t=44, b=44), legend=dict(orientation="h", y=1.15, x=0))
    fig.update_xaxes(gridcolor=C["borda"], zerolinecolor=C["borda"])
    fig.update_yaxes(gridcolor=C["borda"], zerolinecolor=C["borda"])
    return fig


def consolidar(base):
    return (base.groupby("curso", dropna=True)
            .agg(Alunos=("id_aluno", "nunique"), Media=("media_final", "mean"), Frequencia=("frequencia_percentual", "mean"), Registros=("id_aluno", "size"))
            .reset_index())


def comparar(base, eixo, altura=410, chave=None):
    agg = base.groupby(eixo, dropna=True).agg(Media=("media_final", "mean"), Frequencia=("frequencia_percentual", "mean")).reset_index().sort_values(eixo)
    if agg.empty:
        st.info("Sem registros para este comparativo.")
        return
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=agg[eixo], y=agg["Frequencia"], name="Frequência média (%)", marker_color=C["azul"], opacity=.84, hovertemplate="%{x}<br>Frequência: %{y:.1f}%<extra></extra>"), secondary_y=False)
    fig.add_trace(go.Scatter(x=agg[eixo], y=agg["Media"], name="Média final", mode="lines+markers", line=dict(color=C["roxo"], width=3), marker=dict(size=9), hovertemplate="%{x}<br>Média: %{y:.2f}<extra></extra>"), secondary_y=True)
    tema(fig, altura)
    fig.update_yaxes(title_text="Frequência (%)", range=[0, 100], secondary_y=False)
    fig.update_yaxes(title_text="Nota média (0–10)", range=[0, 10], showgrid=False, secondary_y=True)
    fig.update_xaxes(title_text="Curso" if eixo == "curso" else "Disciplina", tickangle=-20 if eixo == "disciplina" else 0)
    st.plotly_chart(fig, use_container_width=True, key=chave or f"comparativo_{eixo}")


def radar_cursos(base):
    resumo = consolidar(base).sort_values("curso")
    if len(resumo) < 3:
        st.info("O radar é mais informativo quando há pelo menos três cursos no filtro. Na aba Cursos, veja o comparativo detalhado.")
        return
    nomes = resumo["curso"].tolist()
    freqs = resumo["Frequencia"].fillna(0).tolist()
    notas = (resumo["Media"].fillna(0) * 10).tolist()
    fig = go.Figure()
    for valores, legenda, cor in [(freqs, "Frequência (%)", C["azul"]), (notas, "Nota média (×10)", C["roxo"])]:
        fig.add_trace(go.Scatterpolar(r=valores + [valores[0]], theta=nomes + [nomes[0]], fill="toself", name=legenda, line_color=cor, opacity=.67))
    tema(fig, 460)
    fig.update_layout(polar=dict(bgcolor=C["painel"], radialaxis=dict(visible=True, range=[0, 100], gridcolor=C["borda"]), angularaxis=dict(gridcolor=C["borda"])))
    st.plotly_chart(fig, use_container_width=True, key="radar_cursos")
    st.caption("No radar, a nota de 0 a 10 é multiplicada por 10 apenas para comparação visual com frequência (%).")

st.markdown('<div class="hero"><h1>🎓 Sistema Acadêmico</h1><p>Inteligência acadêmica • Desempenho, frequência, aprovação e acompanhamento</p></div>', unsafe_allow_html=True)

st.sidebar.header("🎛️ Filtros de análise")
cursos = sorted(df["curso"].dropna().unique().tolist())
curso = st.sidebar.selectbox("Curso", ["Todos"] + cursos)
base_curso = df if curso == "Todos" else df.loc[df["curso"] == curso]
disciplinas = sorted(base_curso["disciplina"].dropna().unique().tolist())
disciplina = st.sidebar.selectbox("Disciplina", ["Todas"] + disciplinas)
base = base_curso if disciplina == "Todas" else base_curso.loc[base_curso["disciplina"] == disciplina]
base = base.copy()
st.sidebar.divider()
st.sidebar.subheader("⚙️ Critérios de alerta (exploratórios)")
nota_min = st.sidebar.slider("Nota mínima de referência", min_value=0.0, max_value=10.0, value=6.0, step=0.5)
freq_min = st.sidebar.slider("Frequência mínima de referência (%)", min_value=50, max_value=100, value=75, step=5)
st.sidebar.caption("Os limites são parâmetros para análise, não regras oficiais de aprovação/reprovação da instituição.")
st.sidebar.divider()
st.sidebar.caption("Fonte: aba base_dados_academicos • Métricas recalculadas pelo filtro selecionado.")

if base.empty:
    st.warning("Não há registros para os filtros selecionados.")
    st.stop()

status = base[["id_aluno", "situacao_matricula"]].drop_duplicates()
alunos = base["id_aluno"].nunique()
ativos = status.loc[status["situacao_matricula"] == "Ativo", "id_aluno"].nunique()
trancados = status.loc[status["situacao_matricula"] == "Trancado", "id_aluno"].nunique()
evadidos = status.loc[status["situacao_matricula"] == "Evadido", "id_aluno"].nunique()
media = base["media_final"].mean()
frequencia = base["frequencia_percentual"].mean()
validos = base["situacao_disciplina"].isin(["Aprovado", "Reprovado"])
aprov = (base["situacao_disciplina"] == "Aprovado").sum()
reprov = (base["situacao_disciplina"] == "Reprovado").sum()
# Critério no nível do aluno: pelo menos um registro abaixo dos limiares selecionados.
risco_linhas = (base["media_final"].lt(nota_min) | base["frequencia_percentual"].lt(freq_min))
risco_ids = base.loc[risco_linhas, "id_aluno"].dropna().unique()
risco_alunos = len(risco_ids)

abas = st.tabs(["📊 Visão geral", "🏆 Análise por curso", "📚 Disciplinas", "🚦 Acompanhamento", "🗂️ Dados e metodologia"])

with abas[0]:
    titulo("Visão executiva")
    cols = st.columns(5)
    for col, args in zip(cols, [("👥 Alunos", f"{alunos:,}".replace(",", "."), C["azul"], "Alunos únicos"), ("🟢 Ativos", ativos, C["verde"], "Matrícula ativa"), ("⏸️ Trancados", trancados, C["laranja"], "Matrícula trancada"), ("🚪 Evadidos", evadidos, C["vermelho"], "Matrícula evadida"), ("📚 Nota média", num(media, 2), C["roxo"], "Média dos registros")]):
        with col: card(*args)
    titulo("Indicadores acadêmicos")
    mc = st.columns(5)
    for col, label, value in zip(mc, ["Evasão", "Trancamento", "Frequência média", "Aprovação", "Reprovação"], [f"{num(pct(evadidos, alunos))}%", f"{num(pct(trancados, alunos))}%", f"{num(frequencia, 1)}%", f"{num(pct(aprov, validos.sum()), 1)}%", f"{num(pct(reprov, validos.sum()), 1)}%"]):
        with col: st.metric(label, value)
    st.caption("Evasão/trancamento: alunos únicos. Aprovação/reprovação: registros de disciplina com situação final.")
    titulo("Comparativo: frequência e nota média")
    comparar(base, "curso", chave="comparativo_visao_geral")
    left, right = st.columns([1.1, 1])
    with left:
        titulo("Situação das matrículas")
        dist = status.groupby("situacao_matricula")["id_aluno"].nunique().reset_index(name="Alunos")
        pie = px.pie(dist, names="situacao_matricula", values="Alunos", hole=.63, color="situacao_matricula", color_discrete_map={"Ativo": C["verde"], "Trancado": C["laranja"], "Evadido": C["vermelho"]})
        tema(pie, 355)
        st.plotly_chart(pie, use_container_width=True, key="situacao_matriculas")
    with right:
        titulo("Leituras automáticas")
        resumo = consolidar(base).dropna(subset=["Media", "Frequencia"])
        if not resumo.empty:
            menor_f = resumo.loc[resumo["Frequencia"].idxmin()]
            menor_n = resumo.loc[resumo["Media"].idxmin()]
            insights = [f"📉 Menor frequência média: <b>{html.escape(str(menor_f['curso']))}</b> ({num(menor_f['Frequencia'])}%).", f"📘 Menor nota média: <b>{html.escape(str(menor_n['curso']))}</b> ({num(menor_n['Media'], 2)}).", f"🚦 <b>{risco_alunos}</b> alunos têm pelo menos um registro abaixo dos limites de referência ({num(pct(risco_alunos, alunos))}% do recorte)."]
            for insight in insights: st.markdown(f'<div class="insight">{insight}</div>', unsafe_allow_html=True)
        st.caption("Insights descritivos do recorte filtrado; não indicam causalidade.")

with abas[1]:
    titulo("Ranking de cursos por nota média")
    rk = consolidar(base).dropna(subset=["Media"]).sort_values("Media", ascending=True)
    ranking = px.bar(rk, x="Media", y="curso", orientation="h", color="Media", color_continuous_scale=[[0, C["roxo"]], [1, C["azul"]]], text="Media", hover_data={"Frequencia": ":.1f", "Alunos": True})
    ranking.update_traces(texttemplate="%{x:.2f}", textposition="outside", cliponaxis=False)
    tema(ranking, max(320, 90 + len(rk) * 65))
    ranking.update_xaxes(range=[0, 10], title="Média final (0–10)")
    ranking.update_yaxes(title=None)
    ranking.update_layout(coloraxis_showscale=False)
    st.plotly_chart(ranking, use_container_width=True, key="ranking_cursos")
    titulo("Frequência e nota — dois eixos")
    comparar(base, "curso", chave="comparativo_aba_cursos")
    titulo("Radar comparativo")
    radar_cursos(base)
    titulo("Tabela resumida por curso")
    tabela = consolidar(base).rename(columns={"curso": "Curso", "Media": "Média final", "Frequencia": "Frequência (%)"}).round(2)
    st.dataframe(tabela, use_container_width=True, hide_index=True)

with abas[2]:
    titulo("Desempenho por disciplina")
    st.caption("Escolha um curso na barra lateral para comparar suas disciplinas. Os indicadores gerais respeitam os filtros de curso e disciplina.")
    # Conserva visão do curso inteiro mesmo com uma disciplina selecionada, para contextualização.
    universo = base_curso if curso != "Todos" else base
    disciplina_resumo = (universo.groupby(["curso", "disciplina"], dropna=True)
                         .agg(Alunos=("id_aluno", "nunique"), Media=("media_final", "mean"), Frequencia=("frequencia_percentual", "mean"), Reprovacao=("situacao_disciplina", lambda s: pct((s == "Reprovado").sum(), s.isin(["Aprovado", "Reprovado"]).sum())))
                         .reset_index())
    if curso != "Todos":
        comparar(universo, "disciplina", 465, chave="comparativo_disciplinas")
    titulo("Mapa de calor das disciplinas")
    if disciplina_resumo.empty:
        st.info("Não há disciplinas disponíveis.")
    else:
        # Heatmap por curso, ou por disciplina do curso escolhido (com métricas percentuais normalizadas).
        eixo = "disciplina" if curso != "Todos" else "curso"
        agrup = disciplina_resumo.groupby(eixo).agg(Frequencia=("Frequencia", "mean"), Nota=("Media", "mean"), Reprovacao=("Reprovacao", "mean")).reset_index()
        # Na visão Todos, calcular médias por curso diretamente da base para não ponderar todas disciplinas igualmente.
        if curso == "Todos":
            agrup = base.groupby("curso").agg(Frequencia=("frequencia_percentual", "mean"), Nota=("media_final", "mean"), Reprovacao=("situacao_disciplina", lambda s: pct((s == "Reprovado").sum(), s.isin(["Aprovado", "Reprovado"]).sum()))).reset_index()
        # Constrói a matriz por posição, evitando alinhamento incorreto de índices
        # (que deixava todos os valores como NaN e o mapa visualmente vazio).
        mapa = agrup.set_index(eixo)[["Frequencia", "Nota", "Reprovacao"]].copy()
        mapa["Nota"] = mapa["Nota"] * 10
        mapa = mapa.rename(columns={
            "Frequencia": "Frequência (%)",
            "Nota": "Média (nota × 10)",
            "Reprovacao": "Reprovação (%)",
        })
        mapa = mapa.apply(pd.to_numeric, errors="coerce")
        mapa = mapa.dropna(how="all")
        if mapa.empty:
            st.info("Não há valores numéricos disponíveis para o mapa de calor com os filtros atuais.")
        else:
            fig_h = go.Figure(go.Heatmap(
                z=mapa.to_numpy(dtype=float),
                x=mapa.columns.tolist(),
                y=mapa.index.astype(str).tolist(),
                colorscale="RdYlGn", zmin=0, zmax=100,
                text=mapa.round(1).to_numpy(dtype=float),
                texttemplate="%{text:.1f}",
                hovertemplate="%{y}<br>%{x}: %{z:.1f}<extra></extra>",
                colorbar=dict(title="Valor (%)"),
            ))
            tema(fig_h, max(360, 130 + len(mapa) * 39))
            fig_h.update_yaxes(autorange="reversed")
            st.plotly_chart(fig_h, use_container_width=True, key="mapa_calor")
        st.caption("Cores do mapa representam magnitude, não qualidade: na coluna Reprovação, percentuais maiores indicam mais reprovações. A média (0–10) foi convertida para 0–100 somente para comparação visual.")
    titulo("Detalhamento por disciplina")
    st.dataframe(disciplina_resumo.rename(columns={"curso": "Curso", "disciplina": "Disciplina", "Media": "Média final", "Frequencia": "Frequência (%)", "Reprovacao": "Reprovação (%)"}).round(2), use_container_width=True, hide_index=True)

with abas[3]:
    titulo("Acompanhamento acadêmico — análise exploratória")
    st.info("Critérios configuráveis na barra lateral. Um aluno aparece em alerta se tiver ao menos um registro de disciplina com nota ou frequência abaixo do limite escolhido. Não é um diagnóstico individual nem uma previsão de evasão.")
    a, b, c = st.columns(3)
    with a: card("🚦 Alunos em alerta", risco_alunos, C["laranja"], "Ao menos um registro abaixo do limite")
    with b: card("📊 Proporção de alunos", f"{num(pct(risco_alunos, alunos))}%", C["vermelho"], "No recorte selecionado")
    with c: card("📘 Registros sinalizados", int(risco_linhas.sum()), C["roxo"], "Registros de disciplina")
    titulo("Registros por motivo do alerta")
    abaixo_nota = base["media_final"].lt(nota_min)
    abaixo_freq = base["frequencia_percentual"].lt(freq_min)
    motivos = pd.DataFrame({"Motivo": ["Abaixo da nota", "Abaixo da frequência", "Ambos os critérios"], "Registros": [int(abaixo_nota.sum()), int(abaixo_freq.sum()), int((abaixo_nota & abaixo_freq).sum())]})
    motivos_fig = px.bar(motivos, x="Motivo", y="Registros", color="Motivo", text="Registros", color_discrete_sequence=[C["roxo"], C["laranja"], C["vermelho"]])
    tema(motivos_fig, 340)
    motivos_fig.update_layout(showlegend=False)
    st.plotly_chart(motivos_fig, use_container_width=True, key="motivos_alerta")
    st.caption("As categorias 'abaixo da nota' e 'abaixo da frequência' podem se sobrepor. Não some as barras.")
    titulo("Alertas agregados por curso")
    sinalizados = base.assign(em_alerta=risco_linhas).groupby("curso").agg(Registros=("id_aluno", "size"), Registros_alerta=("em_alerta", "sum"))
    sinalizados["Alunos_em_alerta"] = base.loc[risco_linhas].groupby("curso")["id_aluno"].nunique()
    sinalizados = sinalizados.fillna(0).reset_index()
    st.dataframe(sinalizados.rename(columns={"curso": "Curso", "Registros": "Registros", "Registros_alerta": "Registros em alerta", "Alunos_em_alerta": "Alunos em alerta"}), hide_index=True, use_container_width=True)

with abas[4]:
    titulo("Dados filtrados")
    st.write(f"**{len(base):,} registros de disciplina** • **{alunos} alunos únicos** • **{base['curso'].nunique()} cursos**".replace(",", "."))
    st.dataframe(base, use_container_width=True, height=380, hide_index=True)
    st.download_button("⬇️ Baixar dados filtrados (CSV)", data=base.to_csv(index=False, sep=";").encode("utf-8-sig"), file_name="dados_academicos_filtrados.csv", mime="text/csv")
    titulo("Como os indicadores são calculados")
    st.markdown("""
- **Alunos:** contagem de `id_aluno` distintos no recorte.
- **Evasão / trancamento:** alunos na situação correspondente divididos pelos alunos distintos do recorte.
- **Nota e frequência médias:** média aritmética dos registros de disciplina selecionados (não é média de médias por aluno).
- **Aprovação / reprovação:** proporção de registros com situação final Aprovado ou Reprovado; não corresponde à porcentagem de alunos aprovados.
- **Radar:** usa frequência percentual e nota média multiplicada por 10; é uma comparação visual, não uma métrica composta.
- **Alertas:** condições analíticas configuráveis, avaliadas por registro de disciplina; um aluno é contado uma só vez se qualquer registro for sinalizado.
""")
    st.warning("Antes da apresentação, confirme com a instituição os critérios oficiais de nota mínima e frequência, pois os limiares do painel são apenas referências configuráveis.")

st.divider()
st.caption("Sistema Acadêmico • Python + Streamlit + Plotly • Dashboard para análise e apresentação")
