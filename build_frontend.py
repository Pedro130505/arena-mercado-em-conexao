# -*- coding: utf-8 -*-
"""
Script construtor para gerar o Index-codigo-novo.txt e Index.html da Arena Mercado em Conexão.
Inclui:
- Ranking Geral com Pódio Olímpico e Extrato Completo
- Registro de Ações com Validação em Tempo Real
- Central de Briefings Oficiais da MeC (com Kit de Mídia, Diretrizes e Hashtags copiáveis)
- Calendário Mensal de Atividades & Cronograma de Eventos
- Painel Completo do Administrador (UFMG Hub) com gestão de briefings e calendário
"""

import json
import os

with open('Logos e manual/assets_base64.json', 'r', encoding='utf-8') as f:
    assets = json.load(f)

icon_mec_b64 = assets['icon_mec']
logo_mec_b64 = assets['logo_mec']
hub_branco_b64 = assets['hub_branco']
hub_colorido_b64 = assets['hub_colorido']

html_template = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<base target="_top">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#EC6E10">
<title>Arena | Mercado em Conexão</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Lexend:wght@400;500;600;700&family=Montserrat:wght@500;600;700;800;900&display=swap" rel="stylesheet">
<style>
:root {
  /* Marca e Ação Primária: Laranja Solar Vibrante e Âmbar MeC */
  --primary: #F59E0B;
  --primary-hover: #D97706;
  --primary-deep: #EA580C;
  --primary-dark: #C2410C;
  --header-bg: #C2410C;
  --hero-a: #EA580C;
  --hero-b: #7C2D12;

  /* Azuis Tecnológicos & Institucionais (UFMG Hub) */
  --navy: #1D4ED8;
  --navy-deep: #0F172A;
  --navy-soft: #EFF6FF;
  --blue-eng: #3B82F6;

  /* Amarelos & Dourados */
  --yellow: #FBBF24;
  --yellow-hover: #F59E0B;
  --yellow-soft: #FEF3C7;
  --orange-soft: #FFF7ED;

  /* Superfícies & Fundo: Clean Slate Suave (fundo limpo sem sepia pesado) */
  --bg: #F8FAFC;
  --surface: #FFFFFF;
  --surface-alt: #F1F5F9;
  --surface-hover: #E2E8F0;
  --text: #0F172A;
  --muted: #64748B;
  --line: #E2E8F0;
  --line-strong: #CBD5E1;

  /* Cores de Feedback & Gamificação (Multicolor) */
  --plus: #10B981;
  --plus-soft: #ECFDF5;
  --minus: #EF4444;
  --minus-soft: #FEF2F2;

  /* Paleta Pódio & Insígnias */
  --gold: #D97706;
  --gold-bg: #FEF3C7;
  --gold-border: #FCD34D;
  --silver: #475569;
  --silver-bg: #F1F5F9;
  --silver-border: #CBD5E1;
  --bronze: #C2410C;
  --bronze-bg: #FFEDD5;
  --bronze-border: #FDBA74;

  /* Badges de Categorias Multicoloridas */
  --cat-ej-bg: #EFF6FF;
  --cat-ej-text: #1D4ED8;
  --cat-ej-border: #BFDBFE;

  --cat-comp-bg: #FFF1F2;
  --cat-comp-text: #E11D48;
  --cat-comp-border: #FECDD3;

  --cat-outro-bg: #FAF5FF;
  --cat-outro-text: #7E22CE;
  --cat-outro-border: #E9D5FF;

  --accent-purple: #8B5CF6;
  --accent-purple-soft: #EDE9FE;
  --accent-cyan: #0EA5E9;
  --accent-cyan-soft: #E0F2FE;

  --on-yellow: #78350F;
  --shadow-sm: 0 1px 3px rgba(15, 23, 42, 0.07), 0 1px 2px rgba(15, 23, 42, 0.04);
  --shadow-md: 0 4px 12px -2px rgba(15, 23, 42, 0.08), 0 2px 6px -1px rgba(15, 23, 42, 0.04);
  --shadow-lg: 0 12px 28px -4px rgba(15, 23, 42, 0.12), 0 4px 8px -2px rgba(15, 23, 42, 0.06);
  box-sizing: border-box;
}

[data-theme="dark"] {
  --primary: #F59E0B;
  --primary-hover: #FBBF24;
  --primary-deep: #FB923C;
  --header-bg: #7C2D12;
  --hero-a: #431407;
  --hero-b: #0B0F19;

  --navy: #60A5FA;
  --navy-deep: #1E3A8A;
  --navy-soft: #172554;
  --blue-eng: #38BDF8;

  --yellow: #FDE047;
  --yellow-hover: #FEF08A;
  --yellow-soft: #422006;
  --orange-soft: #431407;

  --bg: #0B0F19;
  --surface: #111827;
  --surface-alt: #1F2937;
  --surface-hover: #374151;
  --text: #F8FAFC;
  --muted: #94A3B8;
  --line: #1F2937;
  --line-strong: #374151;

  --plus: #34D399;
  --plus-soft: #064E3B;
  --minus: #F87171;
  --minus-soft: #7F1D1D;

  --gold: #FBBF24;
  --gold-bg: #451A03;
  --gold-border: #78350F;
  --silver: #CBD5E1;
  --silver-bg: #1E293B;
  --silver-border: #475569;
  --bronze: #FB923C;
  --bronze-bg: #431407;
  --bronze-border: #7C2D12;

  --cat-ej-bg: #172554;
  --cat-ej-text: #93C5FD;
  --cat-ej-border: #1E40AF;

  --cat-comp-bg: #4C0519;
  --cat-comp-text: #FDA4AF;
  --cat-comp-border: #9F1239;

  --cat-outro-bg: #3B0764;
  --cat-outro-text: #D8B4FE;
  --cat-outro-border: #6B21A8;

  --accent-purple: #A78BFA;
  --accent-purple-soft: #2E1065;
  --accent-cyan: #38BDF8;
  --accent-cyan-soft: #082F49;

  --on-yellow: #0F172A;
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.4);
  --shadow-md: 0 4px 12px -2px rgba(0, 0, 0, 0.5);
  --shadow-lg: 0 12px 28px -4px rgba(0, 0, 0, 0.65);
}

*, *::before, *::after { box-sizing: inherit; }
body {
  margin: 0; background: var(--bg); color: var(--text);
  font-family: "Inter", system-ui, -apple-system, sans-serif;
  font-size: 0.96rem; line-height: 1.55;
  -webkit-font-smoothing: antialiased;
}
h1, h2, h3, .font-title { font-family: "Montserrat", sans-serif; }
.font-lexend { font-family: "Lexend", sans-serif; }
button, input, select, textarea { font: inherit; color: inherit; }
button { cursor: pointer; border: 0; background: none; }
a { color: var(--primary-deep); text-decoration: none; }
a:hover { text-decoration: underline; }
:focus-visible { outline: 3px solid var(--primary); outline-offset: 2px; }
[hidden] { display: none !important; }

/* Botões */
.btn {
  display: inline-flex; align-items: center; justify-content: center; gap: .55rem;
  border: 0; border-radius: 12px; padding: .75rem 1.35rem;
  font-family: "Montserrat", sans-serif; font-weight: 700; font-size: .92rem;
  background: var(--primary); color: #fff;
  box-shadow: 0 6px 18px -6px rgba(236,110,16,.65);
  transition: all .18s ease; text-decoration: none !important;
}
.btn:hover:not(:disabled) { background: var(--primary-hover); transform: translateY(-1px); box-shadow: 0 8px 22px -6px rgba(236,110,16,.75); }
.btn:active:not(:disabled) { transform: translateY(1px); }
.btn:disabled { opacity: .45; cursor: not-allowed; box-shadow: none; transform: none; }
.btn.block { width: 100%; }
.btn.orange { background: var(--header-bg); color: #fff; box-shadow: 0 6px 18px -6px rgba(154,51,5,.6); }
.btn.orange:hover:not(:disabled) { background: #E05814; }
.btn.navy { background: var(--navy); color: #fff; box-shadow: 0 6px 18px -6px rgba(0,75,118,.5); }
.btn.navy:hover:not(:disabled) { background: #006096; }
.btn.ghost { background: transparent; border: 1.5px solid var(--line-strong); color: var(--text); box-shadow: none; }
.btn.ghost:hover:not(:disabled) { background: var(--surface-alt); border-color: var(--primary); }
.btn.sm { padding: .45rem .85rem; font-size: .82rem; border-radius: 9px; }
.link-btn { background: none; border: 0; padding: 0; color: var(--primary-deep); font-weight: 700; text-decoration: underline; text-underline-offset: 3px; cursor: pointer; }
.ghost-btn { background: rgba(255,255,255,.15); border: 1px solid rgba(255,255,255,.3); color: #fff; border-radius: 10px; padding: .4rem .85rem; font-weight: 600; font-size: .84rem; transition: background .15s; }
.ghost-btn:hover { background: rgba(255,255,255,.25); }

/* Badges e Pílulas */
.badge-pill {
  display: inline-flex; align-items: center; gap: .35rem;
  padding: .2rem .65rem; border-radius: 99px;
  font-size: .75rem; font-weight: 700; text-transform: uppercase; letter-spacing: .04em;
}
.badge-ej { background: var(--cat-ej-bg); color: var(--cat-ej-text); border: 1px solid var(--cat-ej-border); }
.badge-comp { background: var(--cat-comp-bg); color: var(--cat-comp-text); border: 1px solid var(--cat-comp-border); }
.badge-outro { background: var(--cat-outro-bg); color: var(--cat-outro-text); border: 1px solid var(--cat-outro-border); }
.badge-gold { background: var(--gold-bg); color: var(--gold); border: 1px solid var(--gold-border); }
.badge-silver { background: var(--silver-bg); color: var(--silver); border: 1px solid var(--silver-border); }
.badge-bronze { background: var(--bronze-bg); color: var(--bronze); border: 1px solid var(--bronze-border); }
.badge-act-id {
  display: inline-flex; align-items: center; gap: .3rem;
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
  font-size: .76rem; font-weight: 700; letter-spacing: .03em;
  background: var(--surface-alt); color: var(--primary-deep);
  border: 1.5px solid var(--line); border-radius: 7px;
  padding: .15rem .55rem; cursor: pointer; user-select: all;
  transition: all .15s; vertical-align: middle;
}
.badge-act-id:hover {
  background: var(--yellow-soft); border-color: var(--primary); color: var(--primary-dark);
}
.badge-act-id svg { width: 12px; height: 12px; opacity: .75; }

.status-pill {
  display: inline-flex; align-items: center; gap: .3rem;
  font-size: .74rem; font-weight: 700; border-radius: 99px; padding: .15rem .65rem;
  white-space: nowrap;
}
.status-pill.pendente, .status-pill.em_breve { background: var(--yellow-soft); color: #B45309; }
.status-pill.validada, .status-pill.ativo, .status-pill.concluido { background: var(--plus-soft); color: var(--plus); }
.status-pill.recusada { background: var(--minus-soft); color: var(--minus); }
.status-pill.expirado { background: var(--line); color: var(--muted); }
.status-pill.cancelado { background: #E2E8F0; color: #64748B; text-decoration: line-through; }
.status-pill.andamento { background: var(--orange-soft); color: var(--primary-deep); font-weight: 800; }

/* Topbar: Laranja & Âmbar Solar Oficial Mercado em Conexão */
.topbar {
  background: linear-gradient(135deg, #9A3412 0%, #C2410C 25%, #EA580C 65%, #F59E0B 100%);
  color: #fff; position: sticky; top: 0; z-index: 20;
  box-shadow: 0 4px 20px rgba(194, 65, 12, 0.28); border-bottom: 1px solid rgba(255,255,255,0.2);
}
.topbar-inner { max-width: 1220px; margin: 0 auto; padding: .65rem 1.25rem; display: flex; align-items: center; justify-content: space-between; gap: 1rem; }
.brand-group { display: flex; align-items: center; gap: .85rem; }
.brand-logo-img { height: 34px; width: auto; object-fit: contain; filter: drop-shadow(0 2px 4px rgba(0,0,0,.2)); }
.arena-tag {
  font-family: "Montserrat", sans-serif; font-weight: 900; font-size: .74rem;
  letter-spacing: .08em; text-transform: uppercase;
  background: #FFFFFF; color: #C2410C;
  border-radius: 8px; padding: .22rem .65rem; box-shadow: 0 2px 8px rgba(0,0,0,.15);
}
.topnav { display: flex; gap: .4rem; }
.topnav button {
  display: inline-flex; align-items: center; gap: .45rem;
  color: rgba(255,255,255,.92); font-family: "Lexend", sans-serif; font-weight: 600; font-size: .9rem;
  padding: .45rem .85rem; border-radius: 10px; transition: all .15s;
}
.topnav button svg { width: 18px; height: 18px; }
.topnav button:hover { color: #fff; background: rgba(255,255,255,.2); }
.topnav button[aria-selected="true"] {
  color: #9A3412; background: #FFFFFF; font-weight: 800;
  box-shadow: 0 4px 14px rgba(0,0,0,.18);
}
.topnav .count-badge { background: #B91C1C; color: #fff; border-radius: 99px; font-size: .7rem; font-weight: 800; padding: .08rem .4rem; }

.me-area { display: flex; align-items: center; gap: .75rem; }
.me-card { display: flex; flex-direction: column; text-align: right; line-height: 1.15; }
.me-card b { font-size: .88rem; color: #fff; max-width: 20ch; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.me-card small { font-size: .74rem; opacity: .82; color: var(--yellow-soft); }

/* Bottom Nav (Mobile) */
.bottomnav {
  display: none; position: fixed; left: 0; right: 0; bottom: 0; z-index: 25;
  background: var(--surface); border-top: 1px solid var(--line);
  padding: .4rem .3rem calc(.4rem + env(safe-area-inset-bottom, 0px));
  box-shadow: 0 -4px 16px rgba(0,0,0,.08);
  grid-auto-flow: column; grid-auto-columns: 1fr;
}
.bottomnav button {
  display: grid; justify-items: center; gap: .2rem;
  font-family: "Lexend", sans-serif; font-size: .72rem; font-weight: 600; color: var(--muted);
  padding: .35rem .2rem; border-radius: 8px;
}
.bottomnav button svg { width: 22px; height: 22px; }
.bottomnav button[aria-selected="true"] { color: var(--primary-deep); font-weight: 700; }
.bottomnav .badge-num { position: absolute; top: 2px; right: 20%; background: #B91C1C; color: #fff; border-radius: 99px; font-size: .65rem; font-weight: 800; padding: .05rem .35rem; }

/* Layout Geral */
main { max-width: 1220px; margin: 0 auto; padding: 1.75rem 1.25rem 4rem; }
.page-header { display: flex; align-items: flex-end; justify-content: space-between; gap: 1rem; flex-wrap: wrap; margin-bottom: 1.4rem; }
.page-title { color: var(--text); font-size: clamp(1.5rem, 3.2vw, 2.1rem); font-weight: 900; margin: 0; line-height: 1.15; letter-spacing: -.02em; }
.page-desc { color: var(--muted); margin: .25rem 0 0; font-size: .95rem; max-width: 70ch; }
.panel { background: var(--surface); border: 1.5px solid var(--line); border-radius: 18px; padding: 1.35rem 1.45rem; box-shadow: var(--shadow-sm); }
.panel-head { display: flex; align-items: center; justify-content: space-between; gap: .75rem; margin-bottom: .85rem; }
.panel-head h3 { color: var(--text); margin: 0; font-size: 1.15rem; font-weight: 800; display: flex; align-items: center; gap: .55rem; }
.panel-head h3 svg { width: 22px; height: 22px; color: var(--primary); }

/* Banner Estatísticas da Arena */
.stats-banner { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1.5rem; }
.stat-card {
  background: var(--surface); border: 1.5px solid var(--line); border-radius: 16px; padding: 1.1rem 1.25rem;
  display: flex; align-items: center; gap: 1rem; box-shadow: var(--shadow-sm); transition: transform .15s;
}
.stat-card:hover { transform: translateY(-2px); border-color: var(--primary); }
.stat-ico {
  width: 48px; height: 48px; border-radius: 14px; display: grid; place-items: center; flex: none;
  background: linear-gradient(135deg, var(--primary), var(--primary-deep)); color: #fff;
}
.stat-ico svg { width: 24px; height: 24px; }
.stat-info b { display: block; font-family: "Montserrat", sans-serif; font-size: 1.45rem; font-weight: 900; color: var(--header-bg); line-height: 1.1; }
.stat-info span { font-size: .8rem; color: var(--muted); font-weight: 600; text-transform: uppercase; letter-spacing: .04em; }

/* Pódio Olímpico dos Líderes */
.podium-wrap { margin-bottom: 1.75rem; }
.podium-title { text-align: center; margin: 0 0 1.25rem; color: var(--text); font-size: 1.35rem; font-weight: 800; }
.podium {
  display: grid; grid-template-columns: 1fr 1.15fr 1fr; gap: .85rem; align-items: flex-end;
  max-width: 860px; margin: 0 auto;
}
.podium-step {
  border-radius: 20px 20px 16px 16px; padding: 1.5rem 1rem 1.25rem;
  text-align: center; position: relative; display: flex; flex-direction: column; align-items: center;
  box-shadow: var(--shadow-md); transition: transform .15s;
}
.podium-step:hover { transform: translateY(-3px); }
.podium-step.p1 {
  background: linear-gradient(180deg, #FFFBEB 0%, #FEF3C7 100%);
  border: 2.5px solid #F59E0B; min-height: 290px; order: 2; z-index: 2;
}
.podium-step.p2 {
  background: linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%);
  border: 2px solid #94A3B8; min-height: 245px; order: 1;
}
.podium-step.p3 {
  background: linear-gradient(180deg, #FFF7ED 0%, #FFEDD5 100%);
  border: 2px solid #D97706; min-height: 215px; order: 3;
}
[data-theme="dark"] .podium-step.p1 { background: linear-gradient(180deg, #3A2E0B 0%, #291F05 100%); border-color: #B45309; }
[data-theme="dark"] .podium-step.p2 { background: linear-gradient(180deg, #242E3D 0%, #171E28 100%); border-color: #475569; }
[data-theme="dark"] .podium-step.p3 { background: linear-gradient(180deg, #38200C 0%, #251305 100%); border-color: #9A3412; }

.podium-badge {
  width: 52px; height: 52px; border-radius: 50%; display: grid; place-items: center;
  margin-top: -38px; margin-bottom: .6rem; box-shadow: 0 6px 16px rgba(0,0,0,.15);
  font-family: "Montserrat", sans-serif; font-weight: 900; font-size: 1.3rem;
}
.p1 .podium-badge { background: linear-gradient(135deg, #FDE68A, #F59E0B); color: #78350F; border: 3px solid #FFF; width: 62px; height: 62px; font-size: 1.55rem; margin-top: -44px; }
.p2 .podium-badge { background: linear-gradient(135deg, #F1F5F9, #94A3B8); color: #1E293B; border: 2.5px solid #FFF; }
.p3 .podium-badge { background: linear-gradient(135deg, #FED7AA, #D97706); color: #7C2D12; border: 2.5px solid #FFF; }

.podium-name { font-family: "Montserrat", sans-serif; font-weight: 800; font-size: 1.05rem; margin: .2rem 0 .3rem; color: var(--header-bg); line-height: 1.2; word-break: break-word; }
.p1 .podium-name { font-size: 1.22rem; }
.podium-category { margin-bottom: .65rem; }
.podium-pts { font-family: "Montserrat", sans-serif; font-weight: 900; font-size: 1.7rem; color: var(--header-bg); margin-top: auto; }
.podium-pts small { font-size: .85rem; font-weight: 700; color: var(--muted); margin-left: .2rem; }

/* Filtro do Ranking e Busca */
.ranking-toolbar {
  display: flex; gap: .75rem; align-items: center; justify-content: space-between; flex-wrap: wrap;
  margin-bottom: 1rem; background: var(--surface); padding: .75rem 1rem; border-radius: 14px; border: 1.5px solid var(--line);
}
.search-input-wrap { display: flex; align-items: center; gap: .5rem; background: var(--surface-alt); border-radius: 10px; padding: .45rem .85rem; border: 1px solid var(--line); flex: 1; min-width: 220px; }
.search-input-wrap svg { width: 18px; height: 18px; color: var(--muted); flex: none; }
.search-input-wrap input { border: 0; background: none; width: 100%; outline: none; font-size: .9rem; }
.filter-pills { display: flex; gap: .4rem; flex-wrap: wrap; }
.filter-pill {
  padding: .35rem .75rem; border-radius: 99px; font-size: .8rem; font-weight: 700;
  border: 1px solid var(--line); color: var(--muted); background: var(--surface);
  cursor: pointer; transition: all .15s;
}
.filter-pill:hover { border-color: var(--primary); color: var(--text); }
.filter-pill.active { background: var(--header-bg); color: #fff; border-color: var(--header-bg); }

/* Card "Você está aqui" */
.my-rank-banner {
  background: linear-gradient(135deg, var(--navy), var(--navy-deep)); color: #fff;
  border-radius: 16px; padding: 1rem 1.35rem; margin-bottom: 1.25rem;
  display: flex; align-items: center; justify-content: space-between; gap: 1rem; flex-wrap: wrap;
  box-shadow: var(--shadow-md); border-left: 6px solid var(--yellow);
}
.my-rank-left { display: flex; align-items: center; gap: 1rem; }
.my-rank-pos {
  width: 46px; height: 46px; border-radius: 12px; background: var(--yellow); color: var(--on-yellow);
  display: grid; place-items: center; font-family: "Montserrat", sans-serif; font-weight: 900; font-size: 1.25rem; flex: none;
}
.my-rank-details b { font-size: 1.05rem; display: block; }
.my-rank-details span { font-size: .85rem; opacity: .88; }
.my-rank-pts { text-align: right; }
.my-rank-pts b { font-family: "Montserrat", sans-serif; font-size: 1.6rem; font-weight: 900; color: var(--yellow); display: block; line-height: 1; }
.my-rank-pts small { font-size: .78rem; opacity: .85; }

/* Lista de Ranking */
.rank-list { list-style: none; margin: 0; padding: 0; display: grid; gap: .65rem; }
.rank-card {
  background: var(--surface); border: 1.5px solid var(--line); border-radius: 14px; padding: .85rem 1.15rem;
  display: grid; grid-template-columns: auto 1fr auto auto; align-items: center; gap: 1rem;
  transition: all .15s;
}
.rank-card:hover { border-color: var(--primary); background: var(--surface-hover); }
.rank-card.mine { background: var(--yellow-soft); border-color: var(--primary); box-shadow: var(--shadow-sm); }
.rank-num {
  width: 38px; height: 38px; border-radius: 10px; display: grid; place-items: center;
  font-family: "Montserrat", sans-serif; font-weight: 800; font-size: .95rem; color: var(--muted);
  background: var(--surface-alt); border: 1px solid var(--line); flex: none;
}
.rank-card.top1 .rank-num { background: var(--gold-bg); color: var(--gold); border-color: var(--gold-border); font-size: 1.1rem; }
.rank-card.top2 .rank-num { background: var(--silver-bg); color: var(--silver); border-color: var(--silver-border); }
.rank-card.top3 .rank-num { background: var(--bronze-bg); color: var(--bronze); border-color: var(--bronze-border); }

.rank-main { min-width: 0; }
.rank-name-row { display: flex; align-items: center; gap: .5rem; flex-wrap: wrap; }
.rank-name { font-weight: 800; font-size: 1.02rem; color: var(--text); }
.rank-meta { font-size: .8rem; color: var(--muted); margin-top: .15rem; }
.rank-score { text-align: right; }
.rank-score .val { font-family: "Montserrat", sans-serif; font-weight: 900; font-size: 1.35rem; color: var(--header-bg); }
.rank-score .val small { font-size: .75rem; color: var(--muted); font-weight: 600; margin-left: .2rem; }
.rank-score .pending-badge { display: block; font-size: .72rem; color: #B45309; font-weight: 600; }

.rank-details-btn {
  background: var(--surface-alt); border: 1px solid var(--line); border-radius: 8px;
  padding: .35rem .65rem; font-size: .78rem; font-weight: 700; color: var(--muted);
  display: flex; align-items: center; gap: .3rem; transition: all .15s;
}
.rank-details-btn:hover { background: var(--primary); color: #fff; border-color: var(--primary); }

/* Extrato de Pontos Expansível */
.rank-breakdown {
  grid-column: 1 / -1; margin-top: .6rem; padding-top: .85rem; border-top: 1px dashed var(--line);
  display: none; animation: fadeIn .2s ease;
}
.rank-card.expanded .rank-breakdown { display: block; }
.breakdown-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: .5rem; }
.b-card { background: var(--surface-alt); border-radius: 10px; padding: .65rem .75rem; text-align: center; }
.b-card small { display: block; font-size: .72rem; color: var(--muted); font-weight: 700; text-transform: uppercase; margin-bottom: .15rem; }
.b-card b { font-family: "Montserrat", sans-serif; font-size: 1.1rem; color: var(--primary-deep); font-weight: 900; }
.progress-bar { height: 6px; border-radius: 99px; background: var(--line); margin-top: .4rem; overflow: hidden; }
.progress-fill { height: 100%; background: var(--primary); border-radius: 99px; }

/* Página de Ações / Tarefas */
.picker { list-style: none; margin: 1rem 0 0; padding: 0; display: grid; gap: .85rem; }
.picker > li {
  background: var(--surface); border: 1.5px solid var(--line); border-radius: 16px;
  padding: .85rem 1.15rem; transition: border-color .15s, background .15s; box-shadow: var(--shadow-sm);
}
.picker > li.on { border-color: var(--primary); background: var(--surface-alt); }
.pick-row { display: grid; grid-template-columns: auto 1fr auto; align-items: center; gap: .9rem; }
.task-ico {
  width: 44px; height: 44px; border-radius: 12px; display: grid; place-items: center;
  background: var(--orange-soft); color: var(--primary-deep); flex: none;
}
.task-ico svg { width: 22px; height: 22px; }
.pick-row .label-area { min-width: 0; }
.pick-row .label { font-weight: 700; font-size: 1.02rem; color: var(--text); }
.pick-row .condicao-tag {
  display: inline-block; font-size: .78rem; color: var(--muted); background: var(--surface);
  border: 1px solid var(--line); border-radius: 6px; padding: .15rem .45rem; margin-top: .2rem;
}
.pick-row .worth { display: inline-block; font-family: "Montserrat", sans-serif; font-weight: 800; font-size: .84rem; color: var(--primary-deep); margin-left: .5rem; }

.stepper { display: flex; align-items: center; gap: .4rem; }
.stepper button {
  width: 2.4rem; height: 2.4rem; border-radius: 10px; border: 1.5px solid var(--line);
  background: var(--surface); font-weight: 800; font-size: 1.2rem; color: var(--header-bg);
  display: grid; place-items: center; transition: all .15s;
}
.stepper button[data-act="inc"] { background: var(--primary); border-color: var(--primary); color: #fff; }
.stepper button[data-act="inc"]:hover { background: var(--primary-hover); }
.stepper button:disabled { opacity: .3; cursor: default; }
.stepper output { min-width: 2.2rem; text-align: center; font-family: "Montserrat", sans-serif; font-weight: 900; font-size: 1.15rem; }

.links-box { margin-top: .85rem; padding: 1rem; background: var(--surface); border: 1.5px dashed var(--primary); border-radius: 12px; display: grid; gap: .6rem; }
.links-box > b { font-size: .88rem; color: var(--header-bg); display: flex; align-items: center; gap: .45rem; }
.link-row { display: grid; grid-template-columns: 1.8rem 1fr; align-items: center; gap: .6rem; }
.link-row span { font-size: .84rem; font-weight: 700; color: var(--muted); text-align: right; }
.link-row input {
  width: 100%; padding: .65rem .85rem; border-radius: 10px; border: 1.5px solid var(--line);
  background: var(--surface); font-size: .9rem;
}
.link-row input:focus { border-color: var(--primary); outline: none; }
.link-row input.good { border-color: var(--plus); background: var(--plus-soft); color: var(--text); }
.link-row input.bad { border-color: var(--minus); background: var(--minus-soft); color: var(--text); }

.submit-floating-bar {
  position: sticky; bottom: 0; z-index: 15; margin-top: 1.5rem; padding: 1rem 1.25rem;
  background: var(--surface); border: 1.5px solid var(--line); border-radius: 18px;
  display: flex; align-items: center; justify-content: space-between; gap: 1rem; flex-wrap: wrap;
  box-shadow: var(--shadow-lg);
}
.submit-summary { display: flex; align-items: baseline; gap: .75rem; }
.submit-pts { font-family: "Montserrat", sans-serif; font-weight: 900; font-size: 1.7rem; color: var(--primary-deep); }
.submit-missing { font-size: .85rem; color: var(--minus); font-weight: 600; }

/* Minhas Entregas */
.hist-list { list-style: none; margin: 0; padding: 0; display: grid; gap: .75rem; }
.hist-item {
  background: var(--surface); border: 1.5px solid var(--line); border-radius: 14px; padding: 1rem 1.2rem;
  display: flex; justify-content: space-between; align-items: center; gap: 1rem; flex-wrap: wrap;
}
.hist-main { min-width: 0; }
.hist-main b { color: var(--header-bg); font-size: 1rem; }
.hist-main a { display: block; font-size: .84rem; word-break: break-all; margin: .2rem 0; }
.hist-meta { font-size: .78rem; color: var(--muted); }
.hist-status { text-align: right; }
.hist-reject-note {
  width: 100%; margin-top: .6rem; padding: .6rem .85rem; border-radius: 10px;
  background: var(--minus-soft); color: var(--minus); font-size: .85rem; border-left: 3px solid var(--minus);
}

/* ==================== CENTRAL DE BRIEFINGS & FEED ==================== */
.feed-tabs { display: flex; gap: .5rem; flex-wrap: wrap; margin-bottom: 1.25rem; }
.feed-tab-btn {
  display: inline-flex; align-items: center; gap: .45rem;
  padding: .55rem 1.2rem; border-radius: 99px; font-family: "Lexend", sans-serif; font-weight: 700; font-size: .9rem;
  background: var(--surface); border: 1.5px solid var(--line); color: var(--header-bg); cursor: pointer; transition: all .15s;
}
.feed-tab-btn:hover { border-color: var(--primary); }
.feed-tab-btn[aria-selected="true"] { background: var(--header-bg); border-color: var(--header-bg); color: #fff; box-shadow: var(--shadow-sm); }

/* Cards de Briefings Oficiais MeC */
.briefing-card {
  background: var(--surface); border: 2px solid var(--line); border-radius: 18px; padding: 1.45rem 1.5rem;
  margin-bottom: 1.25rem; box-shadow: var(--shadow-sm); transition: border-color .15s;
}
.briefing-card:hover { border-color: var(--primary); }
.briefing-card.ativo { border-left: 6px solid var(--primary); }
.briefing-card.em_breve { border-left: 6px solid var(--gold); }
.briefing-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 1rem; flex-wrap: wrap; margin-bottom: .85rem; }
.briefing-title { margin: 0; font-size: 1.3rem; font-weight: 900; color: var(--header-bg); line-height: 1.2; }
.briefing-meta { font-size: .84rem; color: var(--muted); margin-top: .25rem; font-weight: 600; }
.briefing-desc { font-size: .95rem; line-height: 1.55; margin: .85rem 0; color: var(--text); }
.briefing-box {
  background: var(--surface-alt); border-radius: 14px; padding: 1rem 1.2rem; margin: .85rem 0;
  border: 1px solid var(--line);
}
.briefing-box h4 { margin: 0 0 .4rem; font-size: .88rem; color: var(--header-bg); font-weight: 800; text-transform: uppercase; letter-spacing: .04em; }
.briefing-box p { margin: 0; font-size: .9rem; line-height: 1.5; }
.hashtag-copy-row {
  display: flex; align-items: center; justify-content: space-between; gap: .75rem; flex-wrap: wrap;
  background: var(--surface); border: 1.5px dashed var(--primary); border-radius: 12px; padding: .65rem .95rem; margin-top: .85rem;
}
.hashtag-copy-row code { font-family: "Inter", monospace; font-size: .88rem; font-weight: 700; color: var(--primary-deep); }
.briefing-actions { display: flex; align-items: center; justify-content: space-between; gap: .85rem; flex-wrap: wrap; margin-top: 1.25rem; padding-top: .85rem; border-top: 1px solid var(--line); }

/* Linha do Tempo / Cronograma Mensal MeC */
.timeline-list { list-style: none; margin: 0; padding: 0; display: grid; gap: 1rem; position: relative; }
.timeline-item {
  display: grid; grid-template-columns: 100px 1fr auto; gap: 1.25rem; align-items: center;
  background: var(--surface); border: 1.5px solid var(--line); border-radius: 16px; padding: 1.15rem 1.35rem;
  box-shadow: var(--shadow-sm); transition: transform .15s, border-color .15s;
}
.timeline-item:hover { transform: translateY(-2px); border-color: var(--primary); }
.timeline-item.andamento { border-left: 6px solid var(--primary); background: var(--surface-hover); }
.timeline-date-box {
  background: var(--surface-alt); border: 1.5px solid var(--line); border-radius: 14px; padding: .65rem .5rem;
  text-align: center; flex: none;
}
.timeline-date-box b { display: block; font-family: "Montserrat", sans-serif; font-size: 1.25rem; font-weight: 900; color: var(--header-bg); line-height: 1; }
.timeline-date-box small { font-size: .75rem; color: var(--muted); font-weight: 700; text-transform: uppercase; }
.timeline-info h4 { margin: 0 0 .25rem; font-size: 1.08rem; font-weight: 800; color: var(--header-bg); }
.timeline-info p { margin: 0; font-size: .88rem; color: var(--muted); }
.timeline-info .loc { display: inline-flex; align-items: center; gap: .3rem; font-size: .82rem; color: var(--primary-deep); font-weight: 600; margin-top: .3rem; }

/* Avisos Dinâmicos */
.avisos-feed { display: grid; gap: .75rem; margin-bottom: 1.25rem; }
.aviso-item {
  background: var(--surface); border: 1.5px solid var(--line); border-left: 5px solid var(--primary);
  border-radius: 12px; padding: .85rem 1.1rem; display: grid; grid-template-columns: auto 1fr auto; gap: .85rem; align-items: center;
}
.aviso-ico { width: 38px; height: 38px; border-radius: 10px; background: var(--orange-soft); color: var(--primary-deep); display: grid; place-items: center; flex: none; }
.aviso-ico svg { width: 20px; height: 20px; }
.aviso-content .kind { font-size: .72rem; font-weight: 800; text-transform: uppercase; letter-spacing: .05em; color: var(--primary-deep); display: block; }
.aviso-content p { margin: .15rem 0 0; font-size: .9rem; }
.aviso-pts { font-family: "Montserrat", sans-serif; font-weight: 900; font-size: 1.15rem; color: var(--primary-deep); white-space: nowrap; }

/* Admin Tabs & Painel */
.admin-tabs { display: flex; gap: .5rem; flex-wrap: wrap; margin-bottom: 1.25rem; }
.admin-tab-btn {
  display: inline-flex; align-items: center; gap: .45rem;
  padding: .55rem 1.15rem; border-radius: 99px; font-family: "Lexend", sans-serif; font-weight: 700; font-size: .88rem;
  background: var(--surface); border: 1.5px solid var(--line); color: var(--header-bg); cursor: pointer; transition: all .15s;
}
.admin-tab-btn:hover { border-color: var(--primary); }
.admin-tab-btn[aria-selected="true"] { background: var(--header-bg); border-color: var(--header-bg); color: #fff; }
.admin-tab-btn .badge-count {
  background: var(--yellow); color: var(--on-yellow); border-radius: 99px;
  font-size: .72rem; font-weight: 900; padding: .08rem .45rem;
}

.val-item {
  background: var(--surface); border: 1.5px solid var(--line); border-radius: 14px; padding: 1rem 1.25rem;
  margin-bottom: .75rem; display: grid; grid-template-columns: 1fr auto; gap: .75rem 1rem; align-items: center;
}
.val-header { display: flex; align-items: center; gap: .55rem; flex-wrap: wrap; margin-bottom: .35rem; }
.val-meta-row { display: flex; align-items: center; gap: .5rem; flex-wrap: wrap; font-size: .88rem; color: var(--muted); margin: .25rem 0; }
.val-meta-row strong { color: var(--header-bg); }
.val-actions { display: flex; gap: .45rem; flex-wrap: wrap; justify-content: flex-end; }

/* Formulários */
.field { display: block; margin-bottom: 1rem; }
.field > span { display: flex; justify-content: space-between; gap: .5rem; font-weight: 700; font-size: .88rem; margin-bottom: .35rem; color: var(--header-bg); }
.field > span small { font-weight: 500; color: var(--muted); font-size: .78rem; }
.field input, .field select, .field textarea {
  width: 100%; padding: .8rem 1rem; border-radius: 12px;
  border: 1.5px solid var(--line); background: var(--surface); color: var(--text);
  font-size: .95rem; transition: border-color .15s;
}
.field textarea { resize: vertical; min-height: 90px; }
.field input:focus, .field select:focus, .field textarea:focus { border-color: var(--primary); outline: none; box-shadow: 0 0 0 3px rgba(246,162,28,.2); }
.error-box { color: var(--minus); background: var(--minus-soft); border-radius: 10px; padding: .75rem 1rem; font-size: .9rem; margin-bottom: 1rem; border-left: 4px solid var(--minus); }

/* Auth */
.auth-wrap {
  min-height: 100vh; display: grid; grid-template-columns: 1.15fr 1fr;
  background: radial-gradient(circle at 25% 30%, #EA580C 0%, #C2410C 35%, #9A3412 65%, #1E1B4B 100%);
  color: #fff; position: relative;
}
.auth-hero { padding: 3rem clamp(1.5rem, 5vw, 4.5rem); display: flex; flex-direction: column; justify-content: space-between; }
.auth-hero-logos { display: flex; align-items: center; gap: 1.5rem; flex-wrap: wrap; }
.auth-copy { margin: 2rem 0; }
.auth-copy h1 { font-size: clamp(2.4rem, 5.5vw, 4rem); font-weight: 900; line-height: 1.05; margin: 1rem 0; letter-spacing: -.02em; }
.auth-copy h1 span.highlight { color: var(--yellow); display: block; }
.auth-copy p { font-size: 1.15rem; max-width: 42ch; opacity: .95; line-height: 1.5; }
.auth-box { display: grid; place-items: center; padding: 2rem 1.25rem; }
.auth-card {
  width: 100%; max-width: 460px; background: var(--surface); color: var(--text);
  border-radius: 20px; padding: 2.2rem 2rem; box-shadow: 0 30px 60px rgba(0,0,0,.45);
}
.auth-card h2 { color: var(--header-bg); font-size: 1.6rem; font-weight: 900; margin: 0 0 .35rem; }
.auth-card .sub { color: var(--muted); margin: 0 0 1.5rem; font-size: .92rem; }

/* Modais & Toasts */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,.65); z-index: 50; display: grid; place-items: center; padding: 1.25rem; backdrop-filter: blur(3px); }
.modal-card { width: 100%; max-width: 520px; background: var(--surface); border-radius: 18px; padding: 1.75rem; box-shadow: var(--shadow-lg); }
.toast {
  position: fixed; left: 50%; bottom: calc(1.5rem + env(safe-area-inset-bottom, 0px));
  transform: translateX(-50%); background: #2B0F02; color: #fff;
  padding: .85rem 1.4rem; border-radius: 14px; border-left: 5px solid var(--yellow);
  font-weight: 700; z-index: 60; box-shadow: 0 12px 30px rgba(0,0,0,.35); max-width: calc(100% - 2rem);
}
.toast.bad { border-left-color: var(--minus); }

@media (max-width: 900px) {
  .auth-wrap { grid-template-columns: 1fr; }
  .topnav { display: none; }
  .bottomnav { display: grid; }
  body.in-app { padding-bottom: 74px; }
  .submit-floating-bar { bottom: calc(68px + env(safe-area-inset-bottom, 0px)); }
  .toast { bottom: calc(88px + env(safe-area-inset-bottom, 0px)); }
  .podium { grid-template-columns: 1fr; max-width: 360px; }
  .podium-step.p1 { order: 1; }
  .podium-step.p2 { order: 2; }
  .podium-step.p3 { order: 3; }
  .rank-card { grid-template-columns: auto 1fr auto; }
  .rank-details-btn { grid-column: 1 / -1; justify-content: center; }
  .timeline-item { grid-template-columns: 80px 1fr; }
  .timeline-status { grid-column: 1 / -1; }
}
@keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }

/* ===== MELHORIAS DE USABILIDADE & DESIGN ===== */
.theme-btn {
  display: inline-flex; align-items: center; justify-content: center; gap: .35rem;
  background: var(--surface-alt); color: var(--text); border: 1.5px solid var(--line);
  border-radius: 10px; padding: .4rem .75rem; font-size: .84rem; font-weight: 700;
  cursor: pointer; transition: all .15s ease;
}
.theme-btn:hover { background: var(--surface-hover); border-color: var(--primary); transform: translateY(-1px); }

.pwd-field-wrap { position: relative; display: flex; align-items: center; width: 100%; }
.pwd-field-wrap input { width: 100%; padding-right: 2.75rem !important; }
.pwd-toggle-btn {
  position: absolute; right: .5rem; top: 50%; transform: translateY(-50%);
  background: none; border: 0; color: var(--muted); cursor: pointer; padding: .35rem;
  display: flex; align-items: center; justify-content: center; border-radius: 6px;
  transition: color .15s;
}
.pwd-toggle-btn:hover { color: var(--text); background: var(--surface-alt); }

.demo-logins-box {
  margin-top: 1rem; padding: .9rem 1rem; background: var(--surface-alt);
  border: 1.5px dashed var(--line-strong); border-radius: 14px;
}
.demo-label {
  display: flex; align-items: center; gap: .4rem; font-size: .78rem; font-weight: 800;
  color: var(--header-bg); text-transform: uppercase; margin-bottom: .6rem; letter-spacing: .03em;
}
.demo-buttons { display: flex; gap: .5rem; flex-wrap: wrap; }
.btn-demo {
  flex: 1; min-width: 150px; padding: .55rem .75rem; border-radius: 10px;
  border: 1.5px solid var(--line-strong); background: var(--surface); color: var(--text);
  font-size: .82rem; font-weight: 700; cursor: pointer; transition: all .15s;
  text-align: center; display: inline-flex; align-items: center; justify-content: center; gap: .35rem;
}
.btn-demo:hover {
  border-color: var(--primary); background: var(--surface-hover);
  color: var(--header-bg); transform: translateY(-1px); box-shadow: var(--shadow-sm);
}

.auth-explainer-card {
  margin-top: 1.25rem; padding: 1.15rem 1.25rem; border-radius: 14px;
  background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.16);
  color: #fff; font-size: .84rem; line-height: 1.55;
}
.auth-explainer-card h4 {
  margin: 0 0 .5rem; font-size: .92rem; font-weight: 800;
  display: flex; align-items: center; gap: .4rem; color: #FFE8A3;
}
.auth-explainer-card ul { margin: 0; padding-left: 1.2rem; }
.auth-explainer-card li { margin-bottom: .4rem; }

.platform-badge {
  display: inline-flex; align-items: center; gap: .3rem; font-size: .72rem;
  font-weight: 800; border-radius: 99px; padding: .2rem .55rem; text-transform: uppercase;
  letter-spacing: .02em; white-space: nowrap;
}
.platform-badge.instagram { background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%); color: #fff; }
.platform-badge.linkedin { background: #0077B5; color: #fff; }
.platform-badge.youtube { background: #FF0000; color: #fff; }
.platform-badge.tiktok { background: #000; color: #fff; border: 1px solid #444; }
.platform-badge.drive { background: #0F9D58; color: #fff; }
.platform-badge.web { background: var(--navy); color: #fff; }

.bulk-paste-btn {
  background: var(--navy-soft); color: var(--navy); border: 1px solid var(--blue-eng);
  border-radius: 8px; padding: .3rem .65rem; font-size: .78rem; font-weight: 700;
  cursor: pointer; display: inline-flex; align-items: center; gap: .35rem; transition: all .15s;
}
.bulk-paste-btn:hover { background: var(--navy); color: #fff; }

.pill-badge {
  display: inline-block; background: var(--line); color: var(--text);
  border-radius: 99px; padding: .1rem .45rem; font-size: .72rem; font-weight: 800; margin-left: .35rem;
}
.filter-pill.active .pill-badge { background: rgba(255,255,255,.3); color: #fff; }

.faq-list { display: flex; flex-direction: column; gap: .65rem; margin-top: 1rem; }
.faq-item {
  background: var(--surface); border: 1.5px solid var(--line); border-radius: 12px;
  overflow: hidden; transition: border-color .15s;
}
.faq-item.open { border-color: var(--primary); box-shadow: var(--shadow-sm); }
.faq-header {
  padding: .9rem 1.1rem; display: flex; justify-content: space-between; align-items: center;
  cursor: pointer; font-weight: 700; font-size: .92rem; color: var(--text);
  user-select: none;
}
.faq-header:hover { background: var(--surface-hover); }
.faq-icon { transition: transform .2s ease; font-size: .85rem; }
.faq-item.open .faq-icon { transform: rotate(180deg); }
.faq-body {
  padding: 0 1.1rem 1rem; font-size: .88rem; color: var(--muted); line-height: 1.6;
  display: none; border-top: 1px dashed var(--line); padding-top: .75rem;
}
.faq-item.open .faq-body { display: block; }

.admin-metrics-row {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: .75rem;
  margin-bottom: 1.25rem;
}
.admin-metric-card {
  background: var(--surface-alt); border: 1.5px solid var(--line); border-radius: 12px;
  padding: .85rem 1rem; text-align: center;
}
.admin-metric-card b { display: block; font-size: 1.45rem; font-family: "Montserrat", sans-serif; font-weight: 800; color: var(--text); }
.admin-metric-card small { font-size: .74rem; font-weight: 700; color: var(--muted); text-transform: uppercase; }

.score-guide-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: .85rem; margin-top: 1rem; }
.score-guide-card {
  background: var(--surface-alt); border-radius: 12px; padding: 1.1rem; border: 1.5px solid var(--line);
}
.score-guide-card h4 { margin: 0 0 .35rem; font-size: .92rem; color: var(--header-bg); display: flex; align-items: center; gap: .4rem; }
.score-guide-card p { margin: 0; font-size: .82rem; color: var(--muted); line-height: 1.45; }
.score-guide-card .guide-pts { display: inline-block; font-weight: 800; color: var(--plus); font-size: .92rem; margin-top: .4rem; }

.btn-reenviar {
  background: var(--surface-alt); color: var(--primary-deep); border: 1.5px solid var(--primary);
  border-radius: 8px; padding: .35rem .75rem; font-size: .78rem; font-weight: 700;
  cursor: pointer; display: inline-flex; align-items: center; gap: .35rem; transition: all .15s;
  margin-top: .5rem;
}
.btn-reenviar:hover { background: var(--primary); color: #fff; }


/* ===== CORES MULTICOLORIDAS POR CONTEXTO (AMARELO/LARANJA COMO PRINCIPAL) ===== */
/* Stat Cards: Líder e Pontos em Dourado e Laranja (Marca Principal), Validadas em Verde e Iniciativas em Azul */
.stat-card:nth-child(1) { border-left: 4px solid #F59E0B; }
.stat-card:nth-child(1) .stat-ico { background: linear-gradient(135deg, #F59E0B, #D97706); color: #fff; box-shadow: 0 4px 14px rgba(245, 158, 11, 0.35); }
.stat-card:nth-child(1) .stat-info b { color: #B45309; }

.stat-card:nth-child(2) { border-left: 4px solid #EA580C; }
.stat-card:nth-child(2) .stat-ico { background: linear-gradient(135deg, #EA580C, #C2410C); color: #fff; box-shadow: 0 4px 14px rgba(234, 88, 12, 0.35); }
.stat-card:nth-child(2) .stat-info b { color: #C2410C; }

.stat-card:nth-child(3) { border-left: 4px solid #10B981; }
.stat-card:nth-child(3) .stat-ico { background: linear-gradient(135deg, #10B981, #059669); color: #fff; box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35); }
.stat-card:nth-child(3) .stat-info b { color: #059669; }

.stat-card:nth-child(4) { border-left: 4px solid #0EA5E9; }
.stat-card:nth-child(4) .stat-ico { background: linear-gradient(135deg, #0EA5E9, #0284C7); color: #fff; box-shadow: 0 4px 14px rgba(14, 165, 233, 0.35); }
.stat-card:nth-child(4) .stat-info b { color: #0284C7; }

/* Pílulas de filtro contextuais: 'Todas' no Laranja Solar MeC, EJs em Azul, Competição em Carmesim */
.filter-pill[data-filter="todos"].active { background: linear-gradient(135deg, #EA580C, #C2410C); color: #fff; border-color: #C2410C; box-shadow: 0 2px 8px rgba(234,88,12,0.3); }
.filter-pill[data-filter="ej"].active { background: #2563EB; color: #fff; border-color: #2563EB; box-shadow: 0 2px 8px rgba(37,99,235,0.3); }
.filter-pill[data-filter="comp"].active { background: #E11D48; color: #fff; border-color: #E11D48; box-shadow: 0 2px 8px rgba(225,29,72,0.3); }
.filter-pill[data-filter="outro"].active { background: #7E22CE; color: #fff; border-color: #7E22CE; box-shadow: 0 2px 8px rgba(126,34,206,0.3); }

.filter-pill[data-dfilter="todas"].active { background: linear-gradient(135deg, #EA580C, #C2410C); color: #fff; border-color: #C2410C; box-shadow: 0 2px 8px rgba(234,88,12,0.3); }
.filter-pill[data-dfilter="pendente"].active { background: #D97706; color: #fff; border-color: #D97706; }
.filter-pill[data-dfilter="validada"].active { background: #059669; color: #fff; border-color: #059669; }
.filter-pill[data-dfilter="recusada"].active { background: #DC2626; color: #fff; border-color: #DC2626; }

/* Ícones de Tarefas Multicoloridos por Formato */
.picker > li:nth-child(1) .task-ico { background: #EFF6FF; color: #2563EB; }
.picker > li:nth-child(2) .task-ico { background: #F0FDF4; color: #16A34A; }
.picker > li:nth-child(3) .task-ico { background: #FAF5FF; color: #9333EA; }
.picker > li:nth-child(4) .task-ico { background: #FFF1F2; color: #E11D48; }
.picker > li:nth-child(5) .task-ico { background: #FFFBEB; color: #D97706; }

/* Abas Temáticas da Central MeC */
.feed-tab-btn[data-feed-tab="briefings"][aria-selected="true"] { background: linear-gradient(135deg, #EA580C, #F59E0B); border-color: #EA580C; color: #fff; box-shadow: 0 4px 12px rgba(234, 88, 12, 0.35); }
.feed-tab-btn[data-feed-tab="cronograma"][aria-selected="true"] { background: #0284C7; border-color: #0284C7; color: #fff; box-shadow: 0 4px 12px rgba(2, 132, 199, 0.35); }
.feed-tab-btn[data-feed-tab="avisos"][aria-selected="true"] { background: #059669; border-color: #059669; color: #fff; box-shadow: 0 4px 12px rgba(5, 150, 105, 0.35); }
.feed-tab-btn[data-feed-tab="regras"][aria-selected="true"] { background: #4338CA; border-color: #4338CA; color: #fff; box-shadow: 0 4px 12px rgba(67, 56, 202, 0.35); }

/* Métricas do Painel Admin */
.admin-metric-card:nth-child(1) { border-top: 3.5px solid #D97706; }
.admin-metric-card:nth-child(1) b { color: #D97706; }
.admin-metric-card:nth-child(2) { border-top: 3.5px solid #059669; }
.admin-metric-card:nth-child(2) b { color: #059669; }
.admin-metric-card:nth-child(3) { border-top: 3.5px solid #DC2626; }
.admin-metric-card:nth-child(3) b { color: #DC2626; }
.admin-metric-card:nth-child(4) { border-top: 3.5px solid #EA580C; }
.admin-metric-card:nth-child(4) b { color: #EA580C; }

/* Banner Você está aqui em gradiente solar Laranja/Ouro */
.my-rank-banner {
  background: linear-gradient(135deg, #7C2D12 0%, #9A3412 45%, #C2410C 80%, #EA580C 100%) !important;
  border-left: 6px solid #FBBF24 !important;
  box-shadow: 0 10px 25px -4px rgba(154, 52, 18, 0.35) !important;
  color: #fff !important;
}
.my-rank-banner .my-rank-badge {
  background: #FBBF24 !important;
  color: #78350F !important;
  font-weight: 900 !important;
}


/* ===== MÓDULO DE MÉTRICAS PÓS-PUBLICAÇÃO (STORIES 24H & POSTS 1, 2 E 3 SEMANAS) ===== */
.delivery-metrics-box {
  margin-top: .85rem; padding: .85rem 1rem; border-radius: 12px;
  background: var(--surface-alt); border: 1.5px dashed var(--line-strong);
}
.delivery-metrics-head {
  display: flex; align-items: center; justify-content: space-between; gap: .5rem;
  margin-bottom: .65rem; font-size: .82rem; font-weight: 700; color: var(--text); flex-wrap: wrap;
}
.delivery-metrics-head small { color: var(--muted); font-weight: 500; font-size: .76rem; }
.delivery-checkpoints-row {
  display: flex; gap: .6rem; flex-wrap: wrap; align-items: center;
}
.metric-chip {
  display: inline-flex; flex-direction: column; gap: .15rem;
  padding: .4rem .75rem; border-radius: 9px; font-size: .78rem; border: 1px solid transparent;
}
.metric-chip.validada { background: var(--plus-soft); border-color: var(--plus); color: #065F46; }
.metric-chip.pendente { background: var(--yellow-soft); border-color: var(--yellow-hover); color: #92400E; }
.metric-chip.recusada { background: var(--minus-soft); border-color: var(--minus); color: #991B1B; }
.metric-chip .chip-title { font-weight: 800; display: flex; align-items: center; gap: .3rem; }
.metric-chip .chip-data { font-size: .74rem; opacity: .9; }

.btn-reg-metrica {
  display: inline-flex; align-items: center; gap: .35rem;
  padding: .42rem .8rem; border-radius: 9px; font-size: .78rem; font-weight: 700;
  background: var(--surface); color: var(--primary-deep); border: 1.5px solid var(--primary);
  cursor: pointer; transition: all .15s;
}
.btn-reg-metrica:hover {
  background: linear-gradient(135deg, #F59E0B, #EA580C); color: #fff;
  transform: translateY(-1px); box-shadow: 0 4px 10px rgba(234,88,12,0.3);
}

.adm-met-card {
  background: var(--surface); border: 1.5px solid var(--line); border-radius: 14px;
  padding: 1.15rem 1.25rem; margin-bottom: 1rem; box-shadow: var(--shadow-sm);
  transition: all .15s;
}
.adm-met-card:hover { border-color: var(--line-strong); box-shadow: var(--shadow-md); }
.adm-met-grid {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: .75rem;
  background: var(--surface-alt); padding: .75rem 1rem; border-radius: 10px; margin: .75rem 0;
}

</style>
</head>
<body>

<!-- Ícones SVG reutilizáveis -->
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="i-trophy" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 21h8M12 17v4M7 4h10v5a5 5 0 0 1-10 0V4Z"/><path d="M17 5h3v2a3 3 0 0 1-3 3M7 5H4v2a3 3 0 0 0 3 3"/></symbol>
  <symbol id="i-rocket" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/></symbol>
  <symbol id="i-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="4"/><path d="m8 12 3 3 5-6"/></symbol>
  <symbol id="i-list" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></symbol>
  <symbol id="i-feed" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 11a9 9 0 0 1 9 9"/><path d="M4 4a16 16 0 0 1 16 16"/><circle cx="5" cy="19" r="1"/></symbol>
  <symbol id="i-shield" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3 4 6v6c0 4.5 3.4 8.3 8 9 4.6-.7 8-4.5 8-9V6l-8-3Z"/><path d="m9 12 2 2 4-4"/></symbol>
  <symbol id="i-sparkles" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"/></symbol>
  <symbol id="i-pin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/></symbol>
  <symbol id="i-users" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0M16 4.5a3.5 3.5 0 0 1 0 7M18 14a6 6 0 0 1 3.5 6"/></symbol>
  <symbol id="i-form" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/></symbol>
  <symbol id="i-link" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 14a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1"/><path d="M14 10a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1"/></symbol>
  <symbol id="i-mic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v4M8 22h8"/></symbol>
  <symbol id="i-store" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9 5 4h14l2 5M3 9h18v2a3 3 0 0 1-6 0 3 3 0 0 1-6 0 3 3 0 0 1-6 0V9ZM5 13v7h14v-7M10 20v-4h4v4"/></symbol>
  <symbol id="i-bolt" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 4 14h7l-1 8 9-12h-7l1-8Z"/></symbol>
  <symbol id="i-book" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5a2 2 0 0 1 2-2h14v16H6a2 2 0 0 0-2 2V5Z"/><path d="M4 19a2 2 0 0 1 2-2h14M9 7h7M9 11h5"/></symbol>
  <symbol id="i-doc" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8l-5-5Z"/><path d="M14 3v5h5M9 13h6M9 17h4"/></symbol>
  <symbol id="i-calendar" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></symbol>
  <symbol id="i-download" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></symbol>
  <symbol id="i-copy" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></symbol>
  <symbol id="i-external" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></symbol>
  <symbol id="i-search" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></symbol>
  <symbol id="i-chevron-down" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></symbol>
    <symbol id="i-eye" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></symbol>
  <symbol id="i-eye-off" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"/><path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"/><path d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"/><line x1="2" y1="2" x2="22" y2="22"/></symbol>
  <symbol id="i-info" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></symbol>
  <symbol id="i-gear" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></symbol>
</svg>

<div id="boot" style="min-height:100vh;display:grid;place-items:center;text-align:center;padding:2rem;">
  <div>
    <img src="@@ICON_MEC@@" alt="Logo Mercado em Conexão" style="width:72px;height:72px;margin-bottom:1rem;animation:pulse 1.5s infinite;">
    <h2 style="font-family:'Montserrat',sans-serif;color:var(--header-bg);margin:0;">Carregando a Arena…</h2>
    <p style="color:var(--muted);margin:.5rem 0 0;">Conectando com o UFMG Hub e planilhas</p>
  </div>
</div>

<div id="unavailable" style="min-height:100vh;display:grid;place-items:center;text-align:center;padding:2rem;" hidden>
  <div>
    <h2>Não foi possível carregar a Arena</h2>
    <p style="color:var(--muted);">Confira sua conexão e recarregue a página.</p>
    <button class="btn orange" onclick="location.reload()">Tentar novamente</button>
  </div>
</div>

<!-- ======================= AUTH (CADASTRO / LOGIN) ======================= -->
<section id="auth" class="auth-wrap" hidden>
  <div class="auth-hero">
        <div style="display:flex;justify-content:flex-end;margin-bottom:1rem;">
      <button type="button" class="theme-btn" id="auth-theme-toggle" title="Alternar Modo Claro / Escuro">🌓 Alternar Tema</button>
    </div>
    <div class="auth-hero-logos">
      <img src="@@LOGO_MEC@@" alt="Mercado em Conexão" style="height:46px;width:auto;">
      <img src="@@HUB_BRANCO@@" alt="UFMG Hub" style="height:34px;width:auto;opacity:.9;">
    </div>
    <div class="auth-copy">
      <span class="badge-pill" style="background:rgba(255,255,255,.18);color:#fff;border:1px solid rgba(255,255,255,.3);">
        <svg style="width:14px;height:14px"><use href="#i-trophy"/></svg> Gamificação Oficial
      </span>
      <h1>Arena <span class="highlight">Mercado em Conexão</span></h1>
      <p>Competição entre Empresas Juniores e Equipes de Competição. Registre ações de divulgação, acompanhe as missões do Hub e suba no ranking!</p>
    
      <div class="auth-explainer-card">
        <h4><svg style="width:16px;height:16px"><use href="#i-trophy"/></svg> Como Funciona a Competição</h4>
        <ul>
          <li><b>Gamificação Universitária:</b> EJs e Equipes de Competição somam pontos com divulgação nas redes e presença nos encontros.</li>
          <li><b>Auditoria Oficial:</b> Entregas homologadas pela comissão do UFMG Hub em até 48h úteis com extrato transparente.</li>
          <li><b>Premiação no Palco:</b> O Top 3 do pódio será premiado ao vivo no encerramento da Feira Mercado em Conexão!</li>
        </ul>
      </div>
    </div>
    <div style="font-size:.85rem;opacity:.8;">Realização e Organização: <b>UFMG Hub</b></div>
  </div>

  <div class="auth-box">
    <!-- Formulário de Cadastro -->
    <form id="signup" class="auth-card" novalidate hidden>
      <h2>Cadastre sua iniciativa</h2>
      <p class="sub">Seja Empresa Júnior ou Equipe de Competição, crie o acesso da sua organização.</p>
      <div id="signup-error" class="error-box" role="alert" hidden></div>
      <label class="field"><span>Nome da iniciativa</span><input name="nome" maxlength="80" required placeholder="Ex.: Engrenagem Jr. ou Fórmula Tesla" autocomplete="organization"></label>
      <label class="field">
        <span>Categoria / Tipo</span>
        <select name="tipo" required>
          <option value="Empresa Júnior">Empresa Júnior (EJ)</option>
          <option value="Equipe de Competição">Equipe de Competição</option>
          <option value="Projeto de Extensão / Outro">Projeto de Extensão / Coletivo</option>
        </select>
      </label>
      <label class="field"><span>Nome do representante</span><input name="representante" maxlength="80" required placeholder="Seu nome completo" autocomplete="name"></label>
      <label class="field"><span>Cargo na iniciativa</span><input name="cargo" maxlength="60" required placeholder="Ex.: Diretor de Marketing, Capitão, Presidente"></label>
      <label class="field"><span>Rede social oficial da iniciativa</span><input name="redeSocial" maxlength="150" required placeholder="@suainiciativa ou link do perfil"></label>
      <label class="field"><span>Senha de acesso</span>
        <div class="pwd-field-wrap">
          <input name="senha" type="password" minlength="6" maxlength="100" required placeholder="Mínimo 6 caracteres" id="signup-senha-input">
          <button type="button" class="pwd-toggle-btn" data-pwd-target="signup-senha-input" title="Mostrar/Ocultar Senha">
            <svg class="eye-open" style="width:18px;height:18px"><use href="#i-eye"/></svg>
            <svg class="eye-closed" style="width:18px;height:18px;display:none;"><use href="#i-eye-off"/></svg>
          </button>
        </div>
      </label>
      <button class="btn block" type="submit">Cadastrar Iniciativa</button>
      <p style="margin-top:1.25rem;text-align:center;font-size:.9rem;color:var(--muted);">
        Já possui cadastro? <button type="button" class="link-btn" data-go="login">Fazer Login</button>
      </p>
    </form>

    <!-- Formulário de Login -->
    <form id="login" class="auth-card" novalidate hidden>
      <h2>Entrar na Arena</h2>
      <p class="sub">Acesse com o nome registrado da iniciativa e sua senha.</p>
      <div id="login-error" class="error-box" role="alert" hidden></div>
      <label class="field"><span>Nome da iniciativa</span><input name="nome" maxlength="80" required placeholder="Ex.: Engrenagem Jr." autocomplete="username"></label>
      <label class="field"><span>Senha</span>
        <div class="pwd-field-wrap">
          <input name="senha" type="password" maxlength="100" required autocomplete="current-password" id="login-senha-input">
          <button type="button" class="pwd-toggle-btn" data-pwd-target="login-senha-input" title="Mostrar/Ocultar Senha">
            <svg class="eye-open" style="width:18px;height:18px"><use href="#i-eye"/></svg>
            <svg class="eye-closed" style="width:18px;height:18px;display:none;"><use href="#i-eye-off"/></svg>
          </button>
        </div>
      </label>
      <button class="btn block" type="submit" id="btn-submit-login">Entrar na Arena</button>

      <div class="demo-logins-box">
        <span class="demo-label"><svg style="width:14px;height:14px"><use href="#i-sparkles"/></svg> Teste Rápido / Demonstração (1 Clique):</span>
        <div class="demo-buttons">
          <button type="button" class="btn-demo" id="btn-demo-ej" title="Acessar como Iniciativa">🏢 Iniciativa (Engrenagem Jr.)</button>
          <button type="button" class="btn-demo" id="btn-demo-admin" title="Acessar como Gestão Hub">🛡️ Gestão Hub (Admin)</button>
        </div>
      </div>
      <p style="margin-top:1.25rem;text-align:center;font-size:.9rem;color:var(--muted);">
        Ainda não cadastrou sua equipe? <button type="button" class="link-btn" data-go="signup">Cadastrar Iniciativa</button>
      </p>
    </form>
  </div>
</section>

<!-- ======================= APP PRINCIPAL ======================= -->
<div id="app" hidden>
  <header class="topbar">
    <div class="topbar-inner">
      <div class="brand-group">
        <img src="@@ICON_MEC@@" alt="Mercado em Conexão" class="brand-logo-img">
        <span class="arena-tag">Arena</span>
      </div>
      <nav class="topnav" role="tablist" id="topnav-desktop"></nav>
      <div class="me-area">
        <button class="theme-btn" id="theme-toggle" type="button" title="Alternar Modo Claro / Escuro" style="padding:.35rem .6rem;">🌓</button>
        <div class="me-card">
          <b id="me-name">Iniciativa</b>
          <small id="me-cat">Empresa Júnior</small>
        </div>
        <button class="ghost-btn" id="logout" type="button" title="Sair da conta">Sair</button>
      </div>
    </div>
  </header>

  <main>
    <!-- ==================== ABA 1: RANKING (Destaque Principal) ==================== -->
    <section id="page-ranking" hidden>
      <div class="page-header" style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:1rem;">
        <div>
          <h1 class="page-title">Ranking Geral da Arena</h1>
          <p class="page-desc">Classificação em tempo real das iniciativas. Conquiste pontos com publicações, presença no evento e desafios do Hub.</p>
        </div>
        <button type="button" class="btn sm" id="btn-open-score-guide" style="align-self:center; background: linear-gradient(135deg, #F59E0B, #EA580C); color: #fff; box-shadow: 0 4px 14px rgba(234,88,12,0.35);">
          <svg style="width:16px;height:16px;"><use href="#i-info"/></svg> Como Funciona a Pontuação?
        </button>
      </div>

      <!-- Banner de Estatísticas da Arena -->
      <div class="stats-banner" id="stats-banner">
        <div class="stat-card">
          <div class="stat-ico"><svg><use href="#i-trophy"/></svg></div>
          <div class="stat-info"><b id="stat-lider">—</b><span>Líder Atual</span></div>
        </div>
        <div class="stat-card">
          <div class="stat-ico"><svg><use href="#i-sparkles"/></svg></div>
          <div class="stat-info"><b id="stat-pts">0</b><span>Pontos em Disputa</span></div>
        </div>
        <div class="stat-card">
          <div class="stat-ico"><svg><use href="#i-check"/></svg></div>
          <div class="stat-info"><b id="stat-val">0</b><span>Ações Validadas</span></div>
        </div>
        <div class="stat-card">
          <div class="stat-ico"><svg><use href="#i-users"/></svg></div>
          <div class="stat-info"><b id="stat-total">0</b><span>Iniciativas Ativas</span></div>
        </div>
      </div>

      <!-- Pódio Olímpico Top 3 -->
      <div class="podium-wrap" id="podium-wrap">
        <h3 class="podium-title">🏆 Pódio dos Líderes</h3>
        <div class="podium" id="podium-cards"></div>
      </div>

      <!-- Card "Você está aqui" -->
      <div class="my-rank-banner" id="my-rank-banner" hidden>
        <div class="my-rank-left">
          <div class="my-rank-pos" id="my-pos-num">#</div>
          <div class="my-rank-details">
            <b id="my-rank-title">Sua Iniciativa</b>
            <span id="my-rank-diff">Calculando posição...</span>
          </div>
        </div>
        <div class="my-rank-pts">
          <b id="my-rank-pts-val">0 pts</b>
          <small id="my-rank-pending-val"></small>
        </div>
      </div>

      <!-- Barra de Filtros e Busca -->
      <div class="ranking-toolbar">
        <div class="search-input-wrap">
          <svg><use href="#i-search"/></svg>
          <input type="text" id="rank-search" placeholder="Buscar iniciativa por nome...">
        </div>
        <div class="filter-pills" id="rank-filters">
          <button type="button" class="filter-pill active" data-filter="todos">Todas as Iniciativas <span class="pill-badge" id="count-todos">0</span></button>
          <button type="button" class="filter-pill" data-filter="ej">🏢 Empresas Juniores <span class="pill-badge" id="count-ej">0</span></button>
          <button type="button" class="filter-pill" data-filter="comp">🏎️ Equipes de Competição <span class="pill-badge" id="count-comp">0</span></button>
          <button type="button" class="filter-pill" data-filter="outro">💡 Outros <span class="pill-badge" id="count-outro">0</span></button>
        </div>
      </div>

      <!-- Tabela / Cards de Ranking -->
      <div class="panel">
        <ul class="rank-list" id="rank-list"></ul>
      </div>
    </section>

    <!-- ==================== ABA 2: REGISTRAR AÇÕES (Envio de Links) ==================== -->
    <section id="page-tarefas" hidden>
      <div class="page-header">
        <div>
          <h1 class="page-title">Registrar Ações e Divulgações</h1>
          <p class="page-desc">Adicione cada ação realizada pela sua equipe e informe o link da publicação. Lembre-se de manter o perfil público e marcar a <b>@mercadoemconexao</b>.</p>
        </div>
      </div>

      <!-- Banner Informativo de Homologação -->
      <div class="panel" style="background:var(--navy-soft);border:1.5px solid var(--blue-eng);padding:1rem 1.25rem;border-radius:14px;margin-bottom:1.25rem;display:flex;align-items:center;gap:1rem;">
        <div style="font-size:1.8rem;">🛡️</div>
        <div style="font-size:.86rem;line-height:1.5;color:var(--text);">
          <b>Homologação Oficial do UFMG Hub:</b> Todas as entregas são auditadas em até 48h úteis. Certifique-se de que o perfil e os links estejam <b>públicos</b> e contenham as marcações oficiais <code>@ufmghub @mercadodeconexao #ArenaMEC</code>.
        </div>
      </div>

      <ul id="task-picker" class="picker"></ul>

      <!-- Barra flutuante de envio -->
      <div class="submit-floating-bar">
        <div class="submit-summary">
          <span class="submit-pts" id="sum-pts">+0 pts</span>
          <span class="submit-missing" id="sum-missing"></span>
        </div>
        <button id="send-tasks" class="btn" type="button" disabled>
          <svg style="width:18px;height:18px"><use href="#i-rocket"/></svg> Registrar Ações
        </button>
      </div>
    </section>

    <!-- ==================== ABA 3: MINHAS ENTREGAS ==================== -->
    <section id="page-entregas" hidden>
      <div class="page-header">
        <div>
          <h1 class="page-title">Minhas Entregas</h1>
          <p class="page-desc">Acompanhe o status de validação de cada link submetido pela sua iniciativa.</p>
        </div>
      </div>

      <!-- Filtros de Status das Minhas Entregas -->
      <div class="filter-pills" id="deliveries-filters" style="margin-bottom:1.25rem;">
        <button type="button" class="filter-pill active" data-dfilter="todas">Todas as Entregas <span class="pill-badge" id="dcount-todas">0</span></button>
        <button type="button" class="filter-pill" data-dfilter="pendente">⏳ Aguardando Validação <span class="pill-badge" id="dcount-pendente">0</span></button>
        <button type="button" class="filter-pill" data-dfilter="validada">✅ Aprovadas <span class="pill-badge" id="dcount-validada">0</span></button>
        <button type="button" class="filter-pill" data-dfilter="recusada">❌ Recusadas <span class="pill-badge" id="dcount-recusada">0</span></button>
      </div>

      <div class="panel">
        <ul id="my-deliveries-list" class="hist-list"></ul>
      </div>
    </section>

    <!-- ==================== ABA 4: CENTRAL DE BRIEFINGS & ATIVIDADES MeC (Novo Feed) ==================== -->
    <section id="page-home" hidden>
      <div class="page-header">
        <div>
          <h1 class="page-title">Central MeC | Briefings & Operações</h1>
          <p class="page-desc">Consulte os briefings vigentes, cronograma de atividades mensais, kits de mídia e o regulamento do Mercado em Conexão.</p>
        </div>
      </div>

      <!-- Sub-navegação do Feed -->
      <div class="feed-tabs" id="feed-tabs">
        <button class="feed-tab-btn" data-feed-tab="briefings" aria-selected="true">
          <svg style="width:18px;height:18px"><use href="#i-sparkles"/></svg> Briefings Oficiais
        </button>
        <button class="feed-tab-btn" data-feed-tab="cronograma" aria-selected="false">
          <svg style="width:18px;height:18px"><use href="#i-calendar"/></svg> Atividades Mensais
        </button>
        <button class="feed-tab-btn" data-feed-tab="avisos" aria-selected="false">
          <svg style="width:18px;height:18px"><use href="#i-feed"/></svg> Mural de Conquistas
        </button>
        <button class="feed-tab-btn" data-feed-tab="regras" aria-selected="false">
          <svg style="width:18px;height:18px"><use href="#i-book"/></svg> Regras & Edital
        </button>
      </div>

      <!-- 1. Seção de Briefings Oficiais -->
      <div data-feed-sec="briefings">
        <div id="briefings-list"></div>
      </div>

      <!-- 2. Seção de Cronograma e Atividades Mensais -->
      <div data-feed-sec="cronograma" hidden>
        <div class="panel" style="margin-bottom:1.25rem;">
          <div class="panel-head">
            <h3><svg><use href="#i-calendar"/></svg> Calendário Oficial de Atividades | MeC</h3>
          </div>
          <p style="color:var(--muted);font-size:.9rem;margin:0 0 1.25rem;">
            Acompanhe os marcos de cada ciclo, datas limite de postagens e eventos presenciais da Feira Mercado em Conexão.
          </p>
          <ul class="timeline-list" id="timeline-list"></ul>
        </div>
      </div>

      <!-- 3. Mural de Conquistas & Avisos ao Vivo -->
      <div data-feed-sec="avisos" hidden>
        <div class="panel">
          <div class="panel-head">
            <h3><svg><use href="#i-feed"/></svg> Mural ao Vivo de Conquistas</h3>
          </div>
          <div class="avisos-feed" id="feed-avisos"></div>
        </div>
      </div>

      <!-- 4. Regras e Edital Oficial -->
      <div data-feed-sec="regras" hidden>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.25rem;">
          <div class="panel">
            <div class="panel-head">
              <h3><svg><use href="#i-book"/></svg> Regras Oficiais da Arena</h3>
            </div>
            <ol id="rules-list" style="margin:0;padding-left:1.25rem;display:grid;gap:.5rem;font-size:.92rem;"></ol>
          </div>

          <div class="panel" style="border-left:5px solid var(--primary);">
            <div class="panel-head">
              <h3><svg><use href="#i-doc"/></svg> Edital Oficial da Competição</h3>
            </div>
            <p style="font-size:.92rem;color:var(--muted);margin:0 0 1rem;">Consulte o regulamento completo, limites e critérios de desempate homologados pelo UFMG Hub.</p>
            <div id="edital-container"></div>
          </div>
        
        <!-- Copiar Marcações Oficiais e FAQ -->
        <div class="panel" style="margin-top:1.25rem;background:var(--surface-alt);border:1.5px solid var(--line);">
          <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;margin-bottom:1rem;">
            <div>
              <h3 style="margin:0;font-size:1.05rem;color:var(--header-bg);display:flex;align-items:center;gap:.4rem;">
                <svg style="width:18px;height:18px"><use href="#i-copy"/></svg> Marcações Oficiais da Campanha
              </h3>
              <p style="margin:.25rem 0 0;font-size:.85rem;color:var(--muted);">Copie em um clique todas as tags e menções obrigatórias para suas legendas.</p>
            </div>
            <button type="button" class="btn sm navy" id="btn-copy-all-tags">
              <svg style="width:16px;height:16px;"><use href="#i-copy"/></svg> Copiar Todas as Tags
            </button>
          </div>
          <div style="background:var(--surface);padding:.75rem 1rem;border-radius:10px;border:1px solid var(--line);font-family:monospace;font-size:.9rem;color:var(--navy-deep);">
            @ufmghub @mercadodeconexao #ArenaMEC #MEC2026 #HubUFMG
          </div>
        </div>

        <div class="panel" style="margin-top:1.25rem;">
          <div class="panel-head">
            <h3><svg><use href="#i-info"/></svg> Perguntas Frequentes (FAQ) da Arena</h3>
          </div>
          <div class="faq-list">
            <div class="faq-item">
              <div class="faq-header"><span>1. Como as publicações e stories são auditados?</span><span class="faq-icon">▼</span></div>
              <div class="faq-body">A comissão de gestão do UFMG Hub audita os links enviados diariamente. Verificamos se o perfil e o post estão públicos, se as menções @ufmghub e @mercadodeconexao constam na mídia ou legenda e se a hashtag #ArenaMEC foi inserida. A validação ocorre em até 48 horas úteis.</div>
            </div>
            <div class="faq-item">
              <div class="faq-header"><span>2. O que fazer se uma entrega for recusada?</span><span class="faq-icon">▼</span></div>
              <div class="faq-body">A iniciativa não perde a chance de pontuar! Basta acessar a aba <b>Minhas Entregas</b>, consultar o motivo da recusa indicado pelo avaliador e clicar em <b>Corrigir e Reenviar Link</b>. O link atualizado volta para o topo da fila de validação.</div>
            </div>
            <div class="faq-item">
              <div class="faq-header"><span>3. Quem da equipe pode submeter os links?</span><span class="faq-icon">▼</span></div>
              <div class="faq-body">Qualquer membro autorizado da iniciativa de posse da senha de acesso. Recomendamos que os envios sejam centralizados pelo representante ou diretoria de marketing para evitar submissões duplicadas.</div>
            </div>
            <div class="faq-item">
              <div class="faq-header"><span>4. Posso publicar no LinkedIn além do Instagram?</span><span class="faq-icon">▼</span></div>
              <div class="faq-body">Sim! Publicações no LinkedIn, YouTube, TikTok e matérias em blogs de extensão são aceitas e incentivadas. Basta informar o link público correspondente.</div>
            </div>
            <div class="faq-item">
              <div class="faq-header"><span>5. Como funcionam os bônus dos briefings especiais?</span><span class="faq-icon">▼</span></div>
              <div class="faq-body">A Central MeC publica periodicamente missões com diretrizes temáticas (ex: bastidores da equipe, vídeos criativos). Cumprir o briefing garante pontuação cheia e concorre ao bônus de maior engajamento semanal (+50 pts).</div>
            </div>
            <div class="faq-item">
              <div class="faq-header"><span>6. Quando e onde ocorre a premiação dos vencedores?</span><span class="faq-icon">▼</span></div>
              <div class="faq-body">A contagem oficial se encerra na véspera da Feira Mercado em Conexão. O pódio com as 3 iniciativas campeãs será homenageado no palco principal com troféus oficiais e visibilidade junto aos patrocinadores do evento.</div>
            </div>
          </div>
        </div>
</div>
      </div>
    </section>

    <!-- ==================== ABA 5: PAINEL DO HUB (ADMINISTRADOR) ==================== -->
    <section id="page-admin" hidden>
      <div class="page-header">
        <div>
          <h1 class="page-title">Painel de Gestão | UFMG Hub & MeC</h1>
          <p class="page-desc">Valide entregas com 1 clique, publique briefings e atividades mensais, lance pontos de presença e crie novas ações.</p>
        </div>
      </div>

      <!-- Abas Internas do Admin -->
      <div class="admin-tabs" id="admin-tabs"></div>

      <!-- 1. Validar Links -->
      <div data-adm="validar" class="panel">
        <div class="panel-head">
          <h3><svg><use href="#i-link"/></svg> Validação de Links Enviados</h3>
        </div>
        <p style="color:var(--muted);font-size:.88rem;margin:0 0 1rem;">
          Revise as publicações enviadas pelas iniciativas. Você pode aprovar ou recusar indicando o motivo para orientação da equipe.
        </p>

        <!-- Métricas Rápidas de Entregas -->
        <div class="admin-metrics-row">
          <div class="admin-metric-card"><b id="adm-metric-pendente">0</b><small>Aguardando Validação</small></div>
          <div class="admin-metric-card"><b id="adm-metric-validada" style="color:var(--plus);">0</b><small>Validadas</small></div>
          <div class="admin-metric-card"><b id="adm-metric-recusada" style="color:var(--minus);">0</b><small>Recusadas</small></div>
          <div class="admin-metric-card"><b id="adm-metric-total">0</b><small>Total de Entregas</small></div>
        </div>
        <div style="display:flex;gap:.6rem;flex-wrap:wrap;align-items:center;margin-bottom:1rem;">
          <select id="adm-filter-status" style="padding:.5rem .85rem;border-radius:10px;border:1.5px solid var(--line);background:var(--surface);color:var(--text);font-size:.88rem;">
            <option value="pendente">Aguardando Validação</option>
            <option value="validada">Apenas Validadas</option>
            <option value="recusada">Apenas Recusadas</option>
            <option value="todas">Todas as Entregas</option>
          </select>
          <select id="adm-filter-ini" style="padding:.5rem .85rem;border-radius:10px;border:1.5px solid var(--line);background:var(--surface);color:var(--text);font-size:.88rem;">
            <option value="">Todas as iniciativas</option>
          </select>
          <button type="button" class="btn sm" style="background:var(--plus);color:#fff;" id="adm-btn-aprovar-lote">
            <svg style="width:16px;height:16px;vertical-align:-2px"><use href="#i-check"/></svg> Aprovar Pendentes em Lote
          </button>
          <input type="search" id="adm-search-val" placeholder="🔍 Buscar por ID (#ACT-...), tarefa ou iniciativa..." style="padding:.5rem .85rem;border-radius:10px;border:1.5px solid var(--line);background:var(--surface);color:var(--text);font-size:.88rem;flex:1;min-width:240px;">
        </div>
        <div id="adm-val-list"></div>
      </div>

      <!-- 2. Gestão de Briefings & Atividades Mensais (MeC) -->
      <div data-adm="gestao-mec" hidden>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.25rem;">
          <!-- A) Criar Briefing Oficial -->
          <form class="panel" id="f-adm-briefing" novalidate>
            <div class="panel-head">
              <h3><svg><use href="#i-sparkles"/></svg> Publicar Briefing Oficial</h3>
            </div>
            <p style="font-size:.85rem;color:var(--muted);margin:0 0 1rem;">
              Oriente o time da MeC e as iniciativas sobre o tema, diretrizes e kit de artes da campanha vigente.
            </p>
            <div class="error-box" hidden></div>
            <label class="field"><span>Título do Briefing</span><input name="titulo" required placeholder="Ex.: Briefing #02: Lançamento das Inscrições da Feira"></label>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:.5rem;">
              <label class="field"><span>Fase / Mês</span><input name="fase" placeholder="Ex.: Fase 1 · Outubro"></label>
              <label class="field"><span>Período Vigente</span><input name="periodo" placeholder="Ex.: 01/10 a 10/10"></label>
            </div>
            <label class="field"><span>Descrição / Objetivo da Comunicação</span><textarea name="descricao" required placeholder="Explique a mensagem central e o público-alvo"></textarea></label>
            <label class="field"><span>Diretrizes e Requisitos</span><textarea name="diretrizes" placeholder="Ex.: Mínimo 3 cards no carrossel, uso do template oficial..."></textarea></label>
            <label class="field"><span>Link do Kit de Mídia (Drive / Canva)</span><input name="linkDrive" placeholder="https://drive.google.com/..."></label>
            <label class="field"><span>Hashtags e Marcações Oficiais</span><input name="hashtags" value="@mercadoemconexao @ufmghub #ArenaMeC #MercadoEmConexao"></label>
            <label class="field"><span>Bônus Especial de Pontuação (opcional)</span><input name="bonus" placeholder="Ex.: +50 pts para o post de maior engajamento"></label>
            <label class="field">
              <span>Status</span>
              <select name="status">
                <option value="ativo">Ativo / Vigente</option>
                <option value="em_breve">Em Breve</option>
                <option value="concluido">Concluído</option>
              </select>
            </label>
            <button class="btn block orange" type="submit">Publicar Briefing Oficial</button>

            <div style="margin-top:1.5rem;">
              <b style="font-size:.85rem;color:var(--muted);display:block;margin-bottom:.5rem;">Briefings Cadastrados:</b>
              <div id="adm-briefings-list"></div>
            </div>
          </form>

          <!-- B) Adicionar Atividade no Calendário Mensal -->
          <form class="panel" id="f-adm-cronograma" novalidate>
            <div class="panel-head">
              <h3><svg><use href="#i-calendar"/></svg> Adicionar Atividade Mensal</h3>
            </div>
            <p style="font-size:.85rem;color:var(--muted);margin:0 0 1rem;">
              Cadastre marcos, feiras, palestras e desafios no calendário oficial da MeC.
            </p>
            <div class="error-box" hidden></div>
            <label class="field"><span>Data / Dia</span><input name="data" required placeholder="Ex.: 15/10/2026 ou 15 a 17/10"></label>
            <label class="field"><span>Título da Atividade</span><input name="titulo" required placeholder="Ex.: Feira de Carreiras Mercado em Conexão"></label>
            <label class="field"><span>Local ou Formato</span><input name="local" placeholder="Ex.: Praça de Serviços - Campus Pampulha"></label>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:.5rem;">
              <label class="field">
                <span>Tipo</span>
                <select name="tipo">
                  <option value="Presencial">Presencial</option>
                  <option value="Divulgação">Divulgação / Campanha</option>
                  <option value="Palestra">Palestra / Workshop</option>
                  <option value="Competição">Competição / Desafio</option>
                </select>
              </label>
              <label class="field"><span>Pontos Associados</span><input name="pontos" placeholder="Ex.: +40 pts presenciais"></label>
            </div>
            <label class="field"><span>Descrição da Atividade</span><textarea name="descricao" placeholder="Detalhes, horários e orientações"></textarea></label>
            <label class="field">
              <span>Status</span>
              <select name="status">
                <option value="proximo">Próxima Atividade</option>
                <option value="andamento">Acontecendo Agora</option>
                <option value="concluido">Concluída</option>
              </select>
            </label>
            <button class="btn block navy" type="submit">Adicionar ao Calendário</button>

            <div style="margin-top:1.5rem;">
              <b style="font-size:.85rem;color:var(--muted);display:block;margin-bottom:.5rem;">Atividades Agendadas:</b>
              <div id="adm-crono-list"></div>
            </div>
          </form>
        </div>
      </div>

      <!-- 3. Lançar Pontos do Evento -->
      <div data-adm="pontos" hidden>
        <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(320px, 1fr));gap:1.25rem;">
          <!-- Inscrições (2 pts com teto de 200) -->
          <form class="panel" id="f-adm-inscricoes" novalidate>
            <div class="panel-head"><h3><svg><use href="#i-users"/></svg> Inscrições Atribuídas</h3></div>
            <p style="font-size:.85rem;color:var(--muted);margin:0 0 1rem;">
              Vale <b>2 pontos</b> por inscrição válida (limite máximo de 200 pontos por iniciativa na campanha).
            </p>
            <div class="error-box" hidden></div>
            <label class="field"><span>Iniciativa</span><select name="iniciativaId" class="adm-ini-select" required></select></label>
            <label class="field"><span>Quantidade de inscrições</span><input name="quantidade" type="number" min="1" required placeholder="Ex.: 15"></label>
            <button class="btn block orange" type="submit">Lançar Inscrições (+2 pts cada)</button>
          </form>

          <!-- Formulário de Pesquisa (1 pt) -->
          <form class="panel" id="f-adm-formulario" novalidate>
            <div class="panel-head"><h3><svg><use href="#i-form"/></svg> Formulário de Pesquisa</h3></div>
            <p style="font-size:.85rem;color:var(--muted);margin:0 0 1rem;">Vale <b>1 ponto</b> por resposta vinculada à iniciativa.</p>
            <div class="error-box" hidden></div>
            <label class="field"><span>Iniciativa</span><select name="iniciativaId" class="adm-ini-select" required></select></label>
            <label class="field"><span>Quantidade de respostas</span><input name="quantidade" type="number" min="1" required placeholder="Ex.: 25"></label>
            <button class="btn block orange" type="submit">Lançar Respostas (+1 pt cada)</button>
          </form>

          <!-- Palestras -->
          <form class="panel" id="f-adm-palestras" novalidate>
            <div class="panel-head"><h3><svg><use href="#i-mic"/></svg> Participação nas Palestras</h3></div>
            <p style="font-size:.85rem;color:var(--muted);margin:0 0 1rem;">Vale <b>1 ponto</b> por pessoa presente atribuída à iniciativa.</p>
            <div class="error-box" hidden></div>
            <label class="field"><span>Iniciativa</span><select name="iniciativaId" class="adm-ini-select" required></select></label>
            <label class="field"><span>Pessoas presentes nas palestras</span><input name="quantidade" type="number" min="1" required placeholder="Ex.: 20"></label>
            <button class="btn block orange" type="submit">Lançar Presença em Palestras</button>
          </form>

          <!-- Feira de Carreiras -->
          <form class="panel" id="f-adm-feira" novalidate>
            <div class="panel-head"><h3><svg><use href="#i-store"/></svg> Presença Real na Feira</h3></div>
            <p style="font-size:.85rem;color:var(--muted);margin:0 0 1rem;">Vale <b>1 ponto</b> por inscrito da iniciativa que compareceu à feira.</p>
            <div class="error-box" hidden></div>
            <label class="field"><span>Iniciativa</span><select name="iniciativaId" class="adm-ini-select" required></select></label>
            <label class="field"><span>Quantidade de visitantes na feira</span><input name="quantidade" type="number" min="1" required placeholder="Ex.: 30"></label>
            <button class="btn block orange" type="submit">Lançar Visitas na Feira</button>
          </form>

          <!-- Challenges -->
          <form class="panel" id="f-adm-challenges" novalidate>
            <div class="panel-head"><h3><svg><use href="#i-bolt"/></svg> Participação nos Challenges</h3></div>
            <p style="font-size:.85rem;color:var(--muted);margin:0 0 1rem;">Vale <b>1 ponto</b> por pessoa que competiu nos challenges.</p>
            <div class="error-box" hidden></div>
            <label class="field"><span>Iniciativa</span><select name="iniciativaId" class="adm-ini-select" required></select></label>
            <label class="field"><span>Pessoas nos challenges</span><input name="quantidade" type="number" min="1" required placeholder="Ex.: 12"></label>
            <button class="btn block orange" type="submit">Lançar Challenges</button>
          </form>

          <!-- Ação Presencial Aprovada (até 40 pts) -->
          <form class="panel" id="f-adm-presencial" novalidate>
            <div class="panel-head"><h3><svg><use href="#i-pin"/></svg> Ação Presencial Aprovada</h3></div>
            <p style="font-size:.85rem;color:var(--muted);margin:0 0 1rem;">Atribuição de <b>até 40 pontos</b> conforme o briefing.</p>
            <div class="error-box" hidden></div>
            <label class="field"><span>Iniciativa</span><select name="iniciativaId" class="adm-ini-select" required></select></label>
            <label class="field"><span>O que foi a ação</span><input name="oque" required placeholder="Ex.: Stand interativo na Praça de Serviços"></label>
            <label class="field"><span>Quando foi</span><input name="quando" required placeholder="Ex.: 26/09, das 10h às 16h"></label>
            <label class="field"><span>Pontuação (máx. 40)</span><input name="pontos" type="number" min="1" max="40" required placeholder="Ex.: 40"></label>
            <button class="btn block orange" type="submit">Lançar Ação Presencial</button>
          </form>
        </div>
      </div>

      <!-- 4. Criar Nova Ação Dinâmica & Lançamento Avulso -->
      <div data-adm="novas-acoes" hidden>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.25rem;">
          <!-- Lançamento de Pontos Avulso -->
          <form class="panel" id="f-adm-avulso" novalidate>
            <div class="panel-head">
              <h3><svg><use href="#i-sparkles"/></svg> Lançamento de Pontos Avulso</h3>
            </div>
            <p style="font-size:.85rem;color:var(--muted);margin:0 0 1rem;">
              Atribua pontos diretamente para qualquer ação extraordinária ou dinâmica que aconteça.
            </p>
            <div class="error-box" hidden></div>
            <label class="field"><span>Iniciativa</span><select name="iniciativaId" class="adm-ini-select" required></select></label>
            <label class="field"><span>Nome da Ação</span><input name="titulo" required placeholder="Ex.: Vencedor do Pitch Relâmpago"></label>
            <label class="field"><span>Justificativa / Descrição</span><textarea name="descricao" placeholder="Detalhes da conquista"></textarea></label>
            <label class="field">
              <span>Modo de Cálculo</span>
              <select name="modo" id="avulso-modo">
                <option value="fixo">Pontuação Fixa Total</option>
                <option value="quantidade">Multiplicador (Quantidade × Pontos)</option>
              </select>
            </label>
            <div id="avulso-fixo-wrap">
              <label class="field"><span>Pontuação Total</span><input name="pontos" type="number" min="1" placeholder="Ex.: 75"></label>
            </div>
            <div id="avulso-qtd-wrap" style="display:none;grid-template-columns:1fr 1fr;gap:.5rem;">
              <label class="field"><span>Quantidade</span><input name="quantidade" type="number" min="1" placeholder="Ex.: 15"></label>
              <label class="field"><span>Pontos unitários</span><input name="pontosUnitarios" type="number" min="1" placeholder="Ex.: 5"></label>
            </div>
            <label class="field"><span>Data / Momento</span><input name="quando" placeholder="Ex.: 27/09 no Palco Principal"></label>
            <button class="btn block orange" type="submit">Publicar Pontuação Avulsa</button>
          </form>

          <!-- Cadastrar Nova Tarefa de Catálogo -->
          <form class="panel" id="f-adm-catalogo" novalidate>
            <div class="panel-head">
              <h3><svg><use href="#i-rocket"/></svg> Nova Tarefa de Catálogo (com Link)</h3>
            </div>
            <p style="font-size:.85rem;color:var(--muted);margin:0 0 1rem;">
              Crie uma nova ação que ficará disponível na tela de envio de todas as iniciativas para registrarem com link.
            </p>
            <div class="error-box" hidden></div>
            <label class="field"><span>Nome da Tarefa</span><input name="nome" required placeholder="Ex.: Vídeo TikTok ou Post no LinkedIn"></label>
            <label class="field"><span>Pontos por entrega</span><input name="pontos" type="number" min="1" required placeholder="Ex.: 45"></label>
            <label class="field"><span>Condição / Regra de Validação</span><input name="condicao" required placeholder="Ex.: Mínimo 30s marcando @mercadoemconexao"></label>
            <label class="field"><span>Descrição complementar</span><textarea name="descricao" placeholder="Instruções para as iniciativas"></textarea></label>
            <button class="btn block navy" type="submit">Criar Tarefa no Catálogo</button>

            <div style="margin-top:1.25rem;">
              <b style="font-size:.85rem;color:var(--muted);display:block;margin-bottom:.5rem;">Tarefas customizadas ativas:</b>
              <div id="adm-catalogo-list"></div>
            </div>
          </form>
        </div>
      </div>

      <!-- 5. Histórico & Auditoria -->
      <div data-adm="historico" class="panel" hidden>
        <div class="panel-head"><h3><svg><use href="#i-book"/></svg> Histórico e Auditoria de Lançamentos</h3></div>
        <p style="color:var(--muted);font-size:.85rem;margin:0 0 1rem;">
          Registro de todas as pontuações e avisos lançados. Se houve algum engano na digitação, você pode <b>estornar</b> o lançamento imediatamente.
        </p>
        <ul id="adm-log-list" style="list-style:none;margin:0;padding:0;display:grid;gap:.65rem;"></ul>
      </div>

      <!-- 6. Diagnóstico & Integridade da Base -->
      
      <!-- 7. Acompanhamento de Métricas Pós-Publicação (Hub Admin) -->
      <div data-adm="metricas" class="panel" hidden>
        <div class="panel-head">
          <h3><svg><use href="#i-sparkles"/></svg> Acompanhamento de Métricas Pós-Publicação</h3>
        </div>
        <p style="color:var(--muted);font-size:.88rem;margin:0 0 1rem;">
          Acompanhe e homologue os dados de alcance e engajamento enviados pelas iniciativas (24h para stories e 1ª, 2ª e 3ª semanas para posts).
          Cada métrica validada credita automaticamente <b>+10 pts</b> (post) ou <b>+5 pts</b> (story) à iniciativa.
        </p>

        <!-- KPIs de Impacto MeC -->
        <div class="admin-metrics-row" style="margin-bottom:1.25rem;">
          <div class="admin-metric-card" style="border-top:3.5px solid #0EA5E9;"><b id="adm-met-alcance" style="color:#0284C7;">0</b><small>👁️ Alcance Total Gerado</small></div>
          <div class="admin-metric-card" style="border-top:3.5px solid #E11D48;"><b id="adm-met-engajamento" style="color:#E11D48;">0</b><small>❤️ Engajamento Total</small></div>
          <div class="admin-metric-card" style="border-top:3.5px solid #D97706;"><b id="adm-met-pendentes" style="color:#D97706;">0</b><small>⏳ Métricas Pendentes</small></div>
          <div class="admin-metric-card" style="border-top:3.5px solid #10B981;"><b id="adm-met-pontos" style="color:#059669;">0</b><small>🏆 Pontos Bônus Concedidos</small></div>
        </div>

        <!-- Filtros e Ação em Lote -->
        <div style="display:flex;gap:.6rem;flex-wrap:wrap;align-items:center;margin-bottom:1rem;">
          <select id="adm-met-filter-status" style="padding:.5rem .85rem;border-radius:10px;border:1.5px solid var(--line);background:var(--surface);color:var(--text);font-size:.88rem;">
            <option value="pendente">Aguardando Validação</option>
            <option value="validada">Apenas Validadas</option>
            <option value="recusada">Apenas Recusadas</option>
            <option value="todas">Todas as Métricas</option>
          </select>
          <select id="adm-met-filter-ini" style="padding:.5rem .85rem;border-radius:10px;border:1.5px solid var(--line);background:var(--surface);color:var(--text);font-size:.88rem;">
            <option value="">Todas as iniciativas</option>
          </select>
          <button type="button" class="btn sm" style="background:#059669;color:#fff;" id="adm-btn-aprovar-metricas-lote">
            <svg style="width:16px;height:16px;vertical-align:-2px"><use href="#i-check"/></svg> Aprovar Métricas Pendentes em Lote
          </button>
          <input type="search" id="adm-search-met" placeholder="🔍 Buscar por ID (#MTR-...), iniciativa ou tarefa..." style="padding:.5rem .85rem;border-radius:10px;border:1.5px solid var(--line);background:var(--surface);color:var(--text);font-size:.88rem;flex:1;min-width:240px;">
        </div>

        <!-- Lista de Métricas Enviadas -->
        <div id="adm-met-list" style="margin-bottom:2rem;"></div>

        <!-- Radar de Engajamento das Iniciativas -->
        <div class="panel" style="background:var(--surface-alt);border:1px solid var(--line);">
          <div class="panel-head" style="margin-bottom:.75rem;">
            <h4 style="margin:0;font-size:1.05rem;">📊 Radar de Alcance & Engajamento das Iniciativas</h4>
          </div>
          <p style="font-size:.82rem;color:var(--muted);margin:0 0 1rem;">
            Acompanhe o impacto agregado que cada iniciativa está gerando para o ecossistema do Mercado em Conexão nas redes sociais.
          </p>
          <div style="overflow-x:auto;">
            <table style="width:100%;border-collapse:collapse;font-size:.88rem;text-align:left;" id="adm-radar-table">
              <thead>
                <tr style="border-bottom:2px solid var(--line);color:var(--muted);">
                  <th style="padding:.6rem .8rem;">Iniciativa</th>
                  <th style="padding:.6rem .8rem;">Categoria</th>
                  <th style="padding:.6rem .8rem;text-align:center;">Relatórios Enviados</th>
                  <th style="padding:.6rem .8rem;text-align:right;">Alcance Total</th>
                  <th style="padding:.6rem .8rem;text-align:right;">Engajamento</th>
                  <th style="padding:.6rem .8rem;text-align:right;">Pontos de Métricas</th>
                </tr>
              </thead>
              <tbody id="adm-radar-tbody"></tbody>
            </table>
          </div>
        </div>
      </div>

      <div data-adm="diagnostico" class="panel" hidden>
        <div class="panel-head"><h3><svg><use href="#i-gear"/></svg> Diagnóstico & Integridade da Base</h3></div>
        <p style="color:var(--muted);font-size:.88rem;margin:0 0 1.25rem;">
          Ferramentas de auditoria, exportação de planilhas e contingência para assegurar a confiabilidade dos dados no banco SQLite 3 / Google Sheets.
        </p>

        <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(280px, 1fr));gap:1.25rem;">
          <div class="panel" style="background:var(--surface-alt);border:1.5px solid var(--line);">
            <div style="display:flex;align-items:center;gap:.6rem;margin-bottom:.5rem;">
              <span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:var(--plus);"></span>
              <b style="font-size:1rem;color:var(--header-bg);">Status do Banco de Dados</b>
            </div>
            <p id="diag-db-desc" style="font-size:.85rem;color:var(--muted);margin:0 0 1rem;">
              Banco de dados SQLite 3 (WAL Mode) conectado e sincronizado em tempo real para todos os acessos.
            </p>
            <div style="font-size:.82rem;background:var(--surface);padding:.6rem .8rem;border-radius:8px;border:1px solid var(--line);margin-bottom:1rem;">
              <b>Motor Ativo:</b> <span id="diag-db-engine">SQLite 3 (arena.db · WAL)</span><br>
              <b>Versão do Sistema:</b> 3.0.0 (SQLite + Anti-Fraude URL)
            </div>
          </div>

          <div class="panel" style="background:var(--surface-alt);border:1.5px solid var(--line);">
            <div style="display:flex;align-items:center;gap:.6rem;margin-bottom:.5rem;">
              <svg style="width:20px;height:20px;color:var(--primary);"><use href="#i-sparkles"/></svg>
              <b style="font-size:1rem;color:var(--header-bg);">Reparar e Formatar Datas</b>
            </div>
            <p style="font-size:.85rem;color:var(--muted);margin:0 0 1rem;">
              Converte automaticamente qualquer timestamp numérico antigo (ex.: <code>1790530...</code>) gravado no banco em data e hora brasileira legível (<code>DD/MM/AAAA HH:MM:SS</code>).
            </p>
            <button class="btn block orange sm" id="btn-reparar-datas" type="button">
              ✨ Verificar e Reparar Datas Agora
            </button>
          </div>

          <div class="panel" style="background:var(--surface-alt);border:1.5px solid var(--line);">
            <div style="display:flex;align-items:center;gap:.6rem;margin-bottom:.5rem;">
              <svg style="width:20px;height:20px;color:var(--navy);"><use href="#i-download"/></svg>
              <b style="font-size:1rem;color:var(--header-bg);">Exportar Planilhas & Backup</b>
            </div>
            <p style="font-size:.85rem;color:var(--muted);margin:0 0 1rem;">
              Baixe planilhas CSV prontas para abrir no Excel / Google Sheets ou um backup completo em JSON.
            </p>
            <div style="display:grid;gap:.5rem;">
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:.5rem;">
                <a class="btn navy sm" id="btn-export-csv-ranking" href="/api/export/csv?tabela=ranking" target="_blank" style="text-decoration:none;text-align:center;justify-content:center;">
                  📊 CSV Ranking
                </a>
                <a class="btn navy sm" id="btn-export-csv-entregas" href="/api/export/csv?tabela=entregas" target="_blank" style="text-decoration:none;text-align:center;justify-content:center;">
                  📋 CSV Entregas
                </a>
              </div>
              <button class="btn block ghost sm" id="btn-export-backup" type="button">
                📥 Baixar Backup Completo (JSON)
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>

  <!-- Navegação Inferior Mobile -->
  <nav class="bottomnav" id="bottomnav-mobile" role="tablist"></nav>
</div>

<!-- Modal: Como Funciona a Pontuação -->
<div id="modal-score-guide" class="modal-overlay" hidden>
  <div class="modal-card" style="max-width:680px;max-height:90vh;overflow-y:auto;">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;">
      <h3 style="margin:0;color:var(--header-bg);display:flex;align-items:center;gap:.5rem;">
        <svg style="width:22px;height:22px"><use href="#i-trophy"/></svg> Como Funciona a Pontuação da Arena
      </h3>
      <button type="button" class="ghost-btn" id="guide-close-btn" style="font-size:1.4rem;line-height:1;padding:.2rem .6rem;">&times;</button>
    </div>
    <p style="color:var(--muted);font-size:.88rem;margin:0 0 1rem;line-height:1.5;">
      A Arena Mercado em Conexão reconhece a mobilização da sua equipe na divulgação da feira e participação nas atividades oficiais do UFMG Hub.
    </p>

    <div class="score-guide-grid">
      <div class="score-guide-card">
        <h4>📸 Feed (Instagram / LinkedIn)</h4>
        <p>Post com arte ou foto divulgando o Mercado em Conexão marcando <code>@ufmghub</code> e <code>@mercadodeconexao</code>.</p>
        <span class="guide-pts">+40 a +50 pts por post</span>
      </div>
      <div class="score-guide-card">
        <h4>⚡ Stories Diários</h4>
        <p>Publicação temporária de 24h repostando conteúdos oficiais ou mostrando a preparação da equipe.</p>
        <span class="guide-pts">+15 pts por story</span>
      </div>
      <div class="score-guide-card">
        <h4>🤝 Presença em Reuniões do Hub</h4>
        <p>Participação de representantes nos encontros gerais, alinhamentos e capacitações da MeC.</p>
        <span class="guide-pts">+30 a +100 pts</span>
      </div>
      <div class="score-guide-card">
        <h4>🎯 Desafios de Briefing MeC</h4>
        <p>Missões especiais lançadas na Central MeC (vídeos criativos, reels de bastidores, etc.).</p>
        <span class="guide-pts">Até +150 pts + Bônus</span>
      </div>
    </div>

    <div style="margin-top:1.25rem;padding:1rem;background:var(--surface);border:1.5px solid var(--line);border-radius:12px;">
      <h4 style="margin:0 0 .5rem;font-size:.9rem;color:var(--text);">📋 Regras de Homologação dos Links:</h4>
      <ul style="margin:0;padding-left:1.2rem;font-size:.84rem;color:var(--muted);line-height:1.6;">
        <li>O perfil e a publicação devem ser <b>públicos</b> no momento da validação pela banca.</li>
        <li>É obrigatório incluir a hashtag <b>#ArenaMEC</b> e marcar as contas oficiais.</li>
        <li>Caso um link seja recusado por erro ou falta de tag, use o botão <b>Corrigir e Reenviar</b> na aba Minhas Entregas.</li>
        <li>O prazo de auditoria da banca organizadora é de até <b>48 horas úteis</b>.</li>
      </ul>
    </div>

    <div style="display:flex;justify-content:flex-end;margin-top:1.25rem;">
      <button class="btn sm" type="button" id="guide-ok-btn">Entendido, vamos pontuar!</button>
    </div>
  </div>
</div>

<!-- Modal para Corrigir e Reenviar Entrega Recusada -->
<div id="modal-reenviar-entrega" class="modal-overlay" hidden>
  <div class="modal-card">
    <h3 style="color:var(--primary-deep);margin:0 0 .5rem;display:flex;align-items:center;gap:.4rem;">
      <svg style="width:20px;height:20px"><use href="#i-rocket"/></svg> Corrigir e Reenviar Entrega
    </h3>
    <p style="color:var(--muted);font-size:.88rem;margin:0 0 1rem;">
      Atualize o link da postagem com a correção solicitada pela comissão para que ela seja reavaliada.
    </p>

    <div style="background:var(--surface-alt);padding:.85rem;border-radius:10px;margin-bottom:1rem;font-size:.85rem;">
      <div><b>Ação:</b> <span id="reenviar-task-nome">—</span> <span class="badge-pill badge-gold" id="reenviar-task-pts">+0 pts</span></div>
      <div style="margin-top:.35rem;color:var(--minus);"><b style="color:var(--minus);">Motivo da Recusa:</b> <span id="reenviar-motivo">—</span></div>
      <div style="margin-top:.35rem;color:var(--muted);font-size:.78rem;word-break:break-all;"><b>Link anterior:</b> <span id="reenviar-link-antigo">—</span></div>
    </div>

    <label class="field">
      <span>Novo link corrigido (público):</span>
      <input type="url" id="reenviar-novo-url" placeholder="https://instagram.com/p/..." required>
    </label>

    <div style="display:flex;justify-content:flex-end;gap:.6rem;margin-top:1.25rem;">
      <button class="btn ghost sm" type="button" id="reenviar-cancel-btn">Cancelar</button>
      <button class="btn sm" type="button" id="reenviar-confirm-btn" style="background:var(--primary-deep);color:#fff;">Reenviar para Validação</button>
    </div>
  </div>
</div>

<!-- Modal para Colar Vários Links de uma Vez -->

  <!-- Modal: Registrar Métricas Pós-Publicação -->
  <div id="modal-registrar-metrica" class="modal-backdrop" hidden>
    <div class="modal" role="dialog" aria-modal="true" style="max-width: 520px;">
      <div class="modal-head">
        <div>
          <span class="badge-pill" id="m-metric-tag" style="background:var(--yellow-soft);color:#B45309;margin-bottom:.3rem;display:inline-block;">📊 Métricas Pós-Publicação</span>
          <h3 id="m-metric-title" style="margin:0;font-size:1.2rem;">Registrar Métricas do Post</h3>
        </div>
        <button type="button" class="modal-close" id="m-metric-close" aria-label="Fechar">✕</button>
      </div>
      <div class="modal-body">
        <p id="m-metric-desc" style="font-size:.88rem;color:var(--muted);margin:0 0 1rem;"></p>
        
        <form id="form-registrar-metrica">
          <input type="hidden" id="metric-entrega-id" name="entregaId">
          <input type="hidden" id="metric-periodo" name="periodo">
          
          <div class="field" style="margin-bottom:.85rem;">
            <label for="metric-alcance" style="display:flex;align-items:center;gap:.35rem;font-weight:700;font-size:.86rem;margin-bottom:.3rem;">
              👁️ Alcance / Visualizações Únicas <span style="color:#DC2626;">*</span>
            </label>
            <input type="number" id="metric-alcance" name="alcance" min="0" placeholder="Ex.: 1450" required style="width:100%;padding:.65rem;border-radius:10px;border:1.5px solid var(--line-strong);font-weight:700;font-size:1rem;">
            <small style="color:var(--muted);font-size:.76rem;">Número total de contas únicas alcançadas ou visualizações consolidadas.</small>
          </div>

          <div class="field" style="margin-bottom:.85rem;">
            <label for="metric-engajamento" style="display:flex;align-items:center;gap:.35rem;font-weight:700;font-size:.86rem;margin-bottom:.3rem;">
              ❤️ Engajamento / Interações <span style="color:#DC2626;">*</span>
            </label>
            <input type="number" id="metric-engajamento" name="engajamento" min="0" placeholder="Ex.: 180" required style="width:100%;padding:.65rem;border-radius:10px;border:1.5px solid var(--line-strong);font-weight:700;font-size:1rem;">
            <small style="color:var(--muted);font-size:.76rem;">Soma de curtidas, comentários, compartilhamentos, salvamentos ou respostas aos stories.</small>
          </div>

          <div class="field" style="margin-bottom:.85rem;">
            <label for="metric-comprovante" style="display:flex;align-items:center;gap:.35rem;font-weight:700;font-size:.86rem;margin-bottom:.3rem;">
              📸 Link do Print / Comprovante dos Insights <span style="color:#DC2626;">*</span>
            </label>
            <input type="url" id="metric-comprovante" name="comprovanteUrl" placeholder="https://drive.google.com/... ou link de imagem" required style="width:100%;padding:.65rem;border-radius:10px;border:1.5px solid var(--line-strong);font-size:.88rem;">
            <small style="color:var(--muted);font-size:.76rem;">Link público do Google Drive, print no Imgur ou captura da tela de insights do post.</small>
          </div>

          <div class="field" style="margin-bottom:1.15rem;">
            <label for="metric-obs" style="font-weight:700;font-size:.86rem;margin-bottom:.3rem;display:block;">
              💬 Observações / Destaques da Ação (Opcional)
            </label>
            <textarea id="metric-obs" name="observacoes" rows="2" placeholder="Ex.: O post gerou 25 cliques no link da bio e alto engajamento com calouros..." style="width:100%;padding:.6rem;border-radius:10px;border:1.5px solid var(--line-strong);font-size:.85rem;resize:vertical;"></textarea>
          </div>

          <div style="display:flex;gap:.75rem;justify-content:flex-end;">
            <button type="button" class="btn ghost sm" id="m-metric-cancel">Cancelar</button>
            <button type="submit" class="btn sm" id="m-metric-submit" style="background:linear-gradient(135deg, #F59E0B, #EA580C);color:#fff;font-weight:800;">
              🚀 Enviar Métricas para Validação
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>

  <div id="modal-colar-links" class="modal-overlay" hidden>
  <div class="modal-card">
    <h3 style="color:var(--navy);margin:0 0 .5rem;display:flex;align-items:center;gap:.4rem;">
      <svg style="width:20px;height:20px"><use href="#i-link"/></svg> Colar Múltiplos Links
    </h3>
    <p style="color:var(--muted);font-size:.88rem;margin:0 0 1rem;">
      Cole vários links de uma vez (um por linha) para a ação: <b id="bulk-task-name" style="color:var(--text);"></b>
    </p>

    <label class="field">
      <span>Lista de URLs (uma por linha):</span>
      <textarea id="bulk-links-input" rows="6" placeholder="https://instagram.com/p/abc...&#10;https://instagram.com/p/def...&#10;https://linkedin.com/posts/..." style="font-family:monospace;font-size:.85rem;"></textarea>
    </label>

    <div style="display:flex;justify-content:flex-end;gap:.6rem;margin-top:1.25rem;">
      <button class="btn ghost sm" type="button" id="bulk-cancel-btn">Cancelar</button>
      <button class="btn sm navy" type="button" id="bulk-confirm-btn">Inserir Links</button>
    </div>
  </div>
</div>

<!-- Modal para Recusa de Entrega com Motivo -->
<div id="reject-modal" class="modal-overlay" hidden>
  <div class="modal-card">
    <h3 style="color:var(--minus);margin:0 0 .5rem;">Recusar Entrega</h3>
    <p style="color:var(--muted);font-size:.9rem;margin:0 0 1rem;">Informe à iniciativa o motivo para que ela possa corrigir o post e reenviar.</p>
    <label class="field">
      <span>Motivo da recusa:</span>
      <select id="reject-preset">
        <option value="Conta privada (não foi possível visualizar a postagem)">Conta privada (não foi possível visualizar)</option>
        <option value="Faltou marcar @mercadoemconexao">Faltou marcar @mercadoemconexao</option>
        <option value="Publicação fora do prazo estipulado">Publicação fora do prazo estipulado</option>
        <option value="Link inacessível ou quebrado">Link inacessível ou quebrado</option>
        <option value="Conteúdo não atende aos requisitos do edital">Conteúdo não atende aos requisitos do edital</option>
        <option value="outro">Outro motivo personalizado...</option>
      </select>
    </label>
    <label class="field" id="reject-custom-wrap" style="display:none;">
      <span>Descreva o motivo:</span>
      <textarea id="reject-custom-text" placeholder="Ex.: Vídeo com menos de 3 cards..."></textarea>
    </label>
    <div style="display:flex;justify-content:flex-end;gap:.6rem;margin-top:1.25rem;">
      <button class="btn ghost sm" type="button" id="reject-cancel-btn">Cancelar</button>
      <button class="btn sm" style="background:var(--minus);color:#fff;" type="button" id="reject-confirm-btn">Confirmar Recusa</button>
    </div>
  </div>
</div>

<div id="toast" class="toast" role="status" hidden></div>

<script>
(function () {
  "use strict";

  // Detecção de ambiente: Google Apps Script vs Servidor HTTP SQLite vs Arquivo Local
  var isGoogleAppsScript = !!(window.google && google.script && google.script.run);
  var isHttpServer = !isGoogleAppsScript && (window.location.protocol === "http:" || window.location.protocol === "https:");
  var S = {
    token: null,
    data: null,
    adm: null,
    page: "ranking",
    feedTab: "briefings",
    admTab: "validar",
    rankFilter: "todos",
    rankSearch: "",
    counts: {},
    urls: {},
    offset: 0,
    rejectDeliveryId: null
  };

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  function store(k, v) {
    try {
      if (v === undefined) return localStorage.getItem(k);
      if (v === null) localStorage.removeItem(k);
      else localStorage.setItem(k, v);
    } catch (e) { return null; }
  }

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function fmt(val) {
    if (!val) return "";
    if (typeof val === "string") {
      var m = val.match(/^(\\d{2}\\/\\d{2}\\/\\d{4})(?:\\s+(\\d{2}:\\d{2}(?::\\d{2})?))?/);
      if (m) {
        return m[1] + (m[2] ? " às " + m[2] : "");
      }
    }
    var d;
    if (typeof val === "number") {
      d = new Date(val);
    } else if (typeof val === "string") {
      if (/^\\d{10,}$/.test(val)) d = new Date(Number(val));
      else d = new Date(val);
    } else if (val instanceof Date) {
      d = val;
    }
    if (!d || isNaN(d.getTime())) return String(val || "");
    var pad = function (n) { return n < 10 ? "0" + n : "" + n; };
    var dia = pad(d.getDate());
    var mes = pad(d.getMonth() + 1);
    var ano = d.getFullYear();
    var hora = pad(d.getHours());
    var min = pad(d.getMinutes());
    var seg = pad(d.getSeconds());
    return dia + "/" + mes + "/" + ano + " às " + hora + ":" + min + ":" + seg;
  }

  function now() { return Date.now() + S.offset; }
  function isUrl(u) {
    u = String(u || "").trim();
    if (!/^https?:\\/\\//i.test(u) || /\\s/.test(u)) return false;
    try { var x = new URL(u); return /\\./.test(x.hostname) && x.hostname.length > 3; } catch (e) { return false; }
  }

  function copyText(txt) {
    var done = function () { toast("Copiado para a área de transferência!"); };
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(txt).then(done).catch(function () {
          fallbackCopy(txt);
          done();
        });
        return;
      }
    } catch (e) {}
    fallbackCopy(txt);
    done();
  }
  function fallbackCopy(txt) {
    var ta = document.createElement("textarea");
    ta.value = txt; ta.style.position = "fixed"; ta.style.opacity = "0";
    document.body.appendChild(ta); ta.select();
    try { document.execCommand("copy"); } catch (e) {}
    document.body.removeChild(ta);
  }

  document.addEventListener("click", function (ev) {
    var b = ev.target.closest("[data-copy-id]");
    if (b && b.dataset.copyId) {
      ev.stopPropagation();
      copyText(b.dataset.copyId);
    }
  });

  function show(id) {
    ["boot", "unavailable", "auth", "app"].forEach(function (x) { $("#" + x).hidden = x !== id; });
    document.body.classList.toggle("in-app", id === "app");
  }

  var toastTimer;
  function toast(msg, bad) {
    var t = $("#toast");
    t.textContent = msg;
    t.classList.toggle("bad", !!bad);
    t.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { t.hidden = true; }, 4000);
  }

  // ==================== COMUNICAÇÃO SERVER (SQLITE / APPS SCRIPT / MOCK) ====================
  function call(acao, dados, tent) {
    tent = tent || 0;
    var maxTentativas = 2;
    return new Promise(function (resolve, reject) {
      if (isGoogleAppsScript) {
        google.script.run
          .withSuccessHandler(function (r) {
            if (r && r.erro) { var e = new Error(r.erro); e.sair = r.sair; return reject(e); }
            resolve(r);
          })
          .withFailureHandler(function (err) {
            if (tent < maxTentativas) {
              var espera = (tent + 1) * 1200;
              setTimeout(function () {
                call(acao, dados, tent + 1).then(resolve).catch(reject);
              }, espera);
            } else {
              var msg = (err && err.message) ? err.message : "Falha na conexão com o servidor Google Apps Script. Verifique sua conexão e tente novamente.";
              reject(new Error(msg));
            }
          })
          .api(acao, dados || {}, S.token);
      } else if (isHttpServer) {
        fetch("/api", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ acao: acao, dados: dados || {}, token: S.token })
        }).then(function (resp) {
          return resp.json();
        }).then(function (r) {
          if (r && r.erro) {
            var e = new Error(r.erro);
            e.sair = r.sair;
            return reject(e);
          }
          resolve(r);
        }).catch(function (err) {
          if (tent < maxTentativas) {
            var espera = (tent + 1) * 800;
            setTimeout(function () {
              call(acao, dados, tent + 1).then(resolve).catch(reject);
            }, espera);
          } else {
            var msg = (err && err.message) ? err.message : "Falha na comunicação com o servidor SQLite.";
            reject(new Error(msg));
          }
        });
      } else {
        setTimeout(function () {
          try {
            var res = mockApi(acao, dados, S.token);
            if (res && res.erro) { var e = new Error(res.erro); e.sair = res.sair; return reject(e); }
            resolve(res);
          } catch (err) { reject(err); }
        }, 120);
      }
    });
  }

  function handle(e) {
    if (e && e.sair) { logout(); }
    toast(e.message || "Ocorreu um erro.", true);
  }

  // ==================== NAVEGAÇÃO ====================
  function pages() {
    var p = [
      { id: "ranking", label: "Ranking", icon: "i-trophy" }
    ];
    if (S.data && S.data.me && S.data.me.admin) {
      p.push({ id: "admin", label: "Painel do Hub", icon: "i-shield" });
    } else {
      p.push({ id: "tarefas", label: "Registrar Ações", icon: "i-rocket" });
      p.push({ id: "entregas", label: "Minhas Entregas", icon: "i-list" });
    }
    p.push({ id: "home", label: "Central MeC & Feed", icon: "i-feed" });
    return p;
  }

  function renderNav() {
    var me = S.data.me;
    $("#me-name").textContent = me.nome;
    $("#me-cat").textContent = me.admin ? "Administrador Hub" : (me.tipo || "Empresa Júnior");

    var pend = (S.adm && S.adm.entregas) ? S.adm.entregas.filter(function (e) { return e.status === "pendente"; }).length : 0;

    var desktopNav = pages().map(function (p) {
      var badge = (p.id === "admin" && pend) ? ' <span class="count-badge">' + pend + '</span>' : '';
      return '<button role="tab" data-page="' + p.id + '" aria-selected="' + (S.page === p.id) + '">' +
        '<svg><use href="#' + p.icon + '"/></svg>' + esc(p.label) + badge + '</button>';
    }).join("");
    $("#topnav-desktop").innerHTML = desktopNav;

    var mobileNav = pages().map(function (p) {
      var badge = (p.id === "admin" && pend) ? '<span class="badge-num">' + pend + '</span>' : '';
      return '<button role="tab" data-page="' + p.id + '" aria-selected="' + (S.page === p.id) + '" style="position:relative;">' +
        '<svg><use href="#' + p.icon + '"/></svg><span>' + esc(p.label) + '</span>' + badge + '</button>';
    }).join("");
    $("#bottomnav-mobile").innerHTML = mobileNav;

    $$("[data-page]").forEach(function (b) {
      b.addEventListener("click", function () { go(b.dataset.page); });
    });
  }

  function go(page) {
    S.page = page;
    renderNav();
    renderPage();
    window.scrollTo({ top: 0, behavior: "smooth" });
    if (page === "ranking" || page === "home") {
      loadHome().then(renderPage).catch(handle);
    }
    if (page === "admin") {
      loadAdmin().catch(handle);
    }
  }

  function renderPage() {
    ["ranking", "tarefas", "entregas", "home", "admin"].forEach(function (p) {
      var el = $("#page-" + p);
      if (el) el.hidden = S.page !== p;
    });

    if (S.page === "ranking") renderRanking();
    if (S.page === "tarefas") renderTarefas();
    if (S.page === "entregas") renderEntregas();
    if (S.page === "home") renderHome();
    if (S.page === "admin") renderAdmin();
  }


  // ===== DETECÇÃO DE PLATAFORMA DE LINKS =====
  function detectPlatform(url) {
    if (!url) return null;
    var u = url.toLowerCase();
    if (u.indexOf("instagram.com") >= 0) return { name: "Instagram", icon: "📸", cls: "instagram" };
    if (u.indexOf("linkedin.com") >= 0) return { name: "LinkedIn", icon: "💼", cls: "linkedin" };
    if (u.indexOf("youtube.com") >= 0 || u.indexOf("youtu.be") >= 0) return { name: "YouTube", icon: "▶️", cls: "youtube" };
    if (u.indexOf("tiktok.com") >= 0) return { name: "TikTok", icon: "🎵", cls: "tiktok" };
    if (u.indexOf("drive.google.com") >= 0 || u.indexOf("docs.google.com") >= 0) return { name: "Drive", icon: "📁", cls: "drive" };
    if (isUrl(url)) return { name: "Web", icon: "🌐", cls: "web" };
    return null;
  }

  // ===== GERENCIAMENTO DE TEMA (CLARO / ESCURO) =====
  function initTheme() {
    var saved = localStorage.getItem("arena-theme");
    if (!saved) {
      if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
        saved = "dark";
      } else {
        saved = "light";
      }
    }
    applyTheme(saved);
  }

  function applyTheme(theme) {
    if (theme === "dark") {
      document.documentElement.setAttribute("data-theme", "dark");
    } else {
      document.documentElement.removeAttribute("data-theme");
    }
    localStorage.setItem("arena-theme", theme);
    var icon = theme === "dark" ? "☀️" : "🌙";
    var b1 = $("#theme-toggle");
    if (b1) b1.textContent = icon;
    var b2 = $("#auth-theme-toggle");
    if (b2) b2.textContent = icon + (theme === "dark" ? " Modo Claro" : " Modo Escuro");
  }

  function toggleTheme() {
    var cur = document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "light";
    applyTheme(cur === "dark" ? "light" : "dark");
  }

  // ==================== ABA 1: RANKING ====================
  function renderRanking() {
    var d = S.data;
    if (!d) return;

    var stats = d.estatisticas || {};
    $("#stat-lider").textContent = stats.liderNome || "—";
    $("#stat-pts").textContent = (stats.totalPontos || 0).toLocaleString("pt-BR") + " pts";
    $("#stat-val").textContent = (stats.totalValidadas || 0);
    $("#stat-total").textContent = (stats.totalIniciativas || 0);

        var r = d.ranking || [];

    // Contadores dinâmicos para as pílulas de filtro
    var countTodos = r.length;
    var countEj = 0, countComp = 0, countOutro = 0;
    r.forEach(function (u) {
      var t = (u.tipo || "").toLowerCase();
      if (t.indexOf("empresa júnior") >= 0 || t.indexOf("ej") >= 0) countEj++;
      else if (t.indexOf("competição") >= 0) countComp++;
      else countOutro++;
    });
    if ($("#count-todos")) $("#count-todos").textContent = countTodos;
    if ($("#count-ej")) $("#count-ej").textContent = countEj;
    if ($("#count-comp")) $("#count-comp").textContent = countComp;
    if ($("#count-outro")) $("#count-outro").textContent = countOutro;


    // Render Pódio (Top 3)
    if (r.length >= 1) {
      $("#podium-wrap").hidden = false;
      var top1 = r[0];
      var top2 = r[1] || null;
      var top3 = r[2] || null;

      var stepHtml = function (u, pos, cls) {
        if (!u) return '<div class="podium-step ' + cls + '" style="opacity:.4;"><span class="podium-badge">' + pos + 'º</span><b class="podium-name">Vago</b></div>';
        var catClass = (u.tipo === "Equipe de Competição") ? "badge-comp" : "badge-ej";
        return '<div class="podium-step ' + cls + '">' +
          '<span class="podium-badge">' + (pos === 1 ? '🥇' : (pos === 2 ? '🥈' : '🥉')) + '</span>' +
          '<span class="badge-pill ' + catClass + '" style="margin-bottom:.3rem;">' + esc(u.tipo || "EJ") + '</span>' +
          '<b class="podium-name">' + esc(u.nome) + '</b>' +
          '<span style="font-size:.8rem;color:var(--muted);">' + esc(u.representante) + '</span>' +
          '<span class="podium-pts">' + u.pontos.toLocaleString("pt-BR") + '<small>pts</small></span>' +
        '</div>';
      };

      $("#podium-cards").innerHTML = stepHtml(top2, 2, "p2") + stepHtml(top1, 1, "p1") + stepHtml(top3, 3, "p3");
    } else {
      $("#podium-wrap").hidden = true;
    }

    // Card "Você está aqui"
    var me = d.me;
    var myIndex = -1;
    r.forEach(function (u, i) { if (u.id === me.id) myIndex = i; });
    var banner = $("#my-rank-banner");
    if (myIndex >= 0) {
      banner.hidden = false;
      var myPos = myIndex + 1;
      $("#my-pos-num").textContent = myPos + "º";
      $("#my-rank-title").textContent = me.nome + " (" + (me.tipo || "EJ") + ")";
      var myPts = r[myIndex].pontos;
      $("#my-rank-pts-val").textContent = myPts.toLocaleString("pt-BR") + " pts";

      if (r[myIndex].pontosPendentes > 0) {
        $("#my-rank-pending-val").textContent = "(+" + r[myIndex].pontosPendentes + " pts em análise)";
      } else {
        $("#my-rank-pending-val").textContent = "";
      }

      if (myPos === 1) {
        $("#my-rank-diff").textContent = "🏆 Você está liderando a Arena! Continue mantendo o ritmo!";
      } else {
        var dif = r[myIndex - 1].pontos - myPts;
        $("#my-rank-diff").textContent = "Faltam " + dif + " pts para alcançar o " + myIndex + "º lugar (" + r[myIndex - 1].nome + ").";
      }
    } else {
      banner.hidden = true;
    }

    // Filtragem e busca
    var query = (S.rankSearch || "").toLowerCase().trim();
    var filtered = r.filter(function (u) {
      if (S.rankFilter === "ej" && u.tipo !== "Empresa Júnior") return false;
      if (S.rankFilter === "comp" && u.tipo !== "Equipe de Competição") return false;
      if (S.rankFilter === "outro" && (u.tipo === "Empresa Júnior" || u.tipo === "Equipe de Competição")) return false;
      if (query && !u.nome.toLowerCase().includes(query) && !u.representante.toLowerCase().includes(query)) return false;
      return true;
    });

    if (!filtered.length) {
      $("#rank-list").innerHTML = '<li style="text-align:center;padding:2rem;color:var(--muted);">Nenhuma iniciativa encontrada para este filtro.</li>';
      return;
    }

    $("#rank-list").innerHTML = filtered.map(function (u, i) {
      var realPos = r.indexOf(u) + 1;
      var topCls = realPos === 1 ? "top1" : (realPos === 2 ? "top2" : (realPos === 3 ? "top3" : ""));
      var mineCls = u.id === me.id ? "mine" : "";
      var catClass = (u.tipo === "Equipe de Competição") ? "badge-comp" : "badge-ej";
      var b = u.breakdown || {};

      var pendingText = u.pontosPendentes ? '<span class="pending-badge">+' + u.pontosPendentes + ' pts pendentes</span>' : '';

      return '<li class="rank-card ' + topCls + ' ' + mineCls + '" id="card-ini-' + esc(u.id) + '">' +
        '<div class="rank-num">' + (realPos <= 3 ? (realPos === 1 ? '🥇' : (realPos === 2 ? '🥈' : '🥉')) : realPos + 'º') + '</div>' +
        '<div class="rank-main">' +
          '<div class="rank-name-row">' +
            '<span class="rank-name">' + esc(u.nome) + '</span>' +
            '<span class="badge-pill ' + catClass + '">' + esc(u.tipo || "EJ") + '</span>' +
            (u.id === me.id ? '<span class="badge-pill" style="background:var(--header-bg);color:#fff;">Sua equipe</span>' : '') +
          '</div>' +
          '<div class="rank-meta">' + esc(u.representante) + (u.cargo ? ' · ' + esc(u.cargo) : '') + (u.redeSocial ? ' · <a href="https://instagram.com/' + esc(u.redeSocial.replace('@', '')) + '" target="_blank" rel="noopener">' + esc(u.redeSocial) + '</a>' : '') + '</div>' +
        '</div>' +
        '<div class="rank-score">' +
          '<span class="val">' + u.pontos.toLocaleString("pt-BR") + '<small>pts</small></span>' +
          pendingText +
        '</div>' +
        '<button class="rank-details-btn" data-toggle-breakdown="' + esc(u.id) + '" type="button">' +
          'Extrato <svg style="width:14px;height:14px;"><use href="#i-chevron-down"/></svg>' +
        '</button>' +
        '<div class="rank-breakdown">' +
          '<div class="breakdown-grid">' +
            '<div class="b-card"><small>📱 Redes Sociais</small><b>+' + (b.redes || 0) + '</b></div>' +
            '<div class="b-card">' +
              '<small>👥 Inscrições (máx 200)</small><b>' + (b.inscricoes || 0) + '/200</b>' +
              '<div class="progress-bar"><div class="progress-fill" style="width:' + Math.min(100, ((b.inscricoes || 0)/200)*100) + '%;"></div></div>' +
            '</div>' +
            '<div class="b-card"><small>📋 Formulário</small><b>+' + (b.formulario || 0) + '</b></div>' +
            '<div class="b-card"><small>🏛️ Presencial</small><b>+' + (b.presencial || 0) + '</b></div>' +
            '<div class="b-card"><small>🎤 Palestras</small><b>+' + (b.palestras || 0) + '</b></div>' +
            '<div class="b-card"><small>🎪 Feira</small><b>+' + (b.feira || 0) + '</b></div>' +
            '<div class="b-card"><small>⚡ Challenges</small><b>+' + (b.challenges || 0) + '</b></div>' +
            '<div class="b-card"><small>✨ Avulso / Hub</small><b>+' + (b.avulso || 0) + '</b></div>' +
          '</div>' +
        '</div>' +
      '</li>';
    }).join("");

    $$("[data-toggle-breakdown]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var card = $("#card-ini-" + btn.dataset.toggleBreakdown);
        if (card) card.classList.toggle("expanded");
      });
    });
  }

  // Busca e Filtros do Ranking
  $("#rank-search").addEventListener("input", function (e) {
    S.rankSearch = e.target.value;
    renderRanking();
  });
  $$("#rank-filters .filter-pill").forEach(function (btn) {
    btn.addEventListener("click", function () {
      $$("#rank-filters .filter-pill").forEach(function (b) { b.classList.remove("active"); });
      btn.classList.add("active");
      S.rankFilter = btn.dataset.filter;
      renderRanking();
    });
  });

  // ==================== ABA 2: REGISTRAR AÇÕES ====================
  function renderTarefas() {
    var d = S.data;
    if (!d) return;

    var tarefas = d.tarefas || [];
    $("#task-picker").innerHTML = tarefas.map(function (t) {
      var n = S.counts[t.id] || 0;
      var urls = S.urls[t.id] || [];
      var linksHtml = "";

      if (n > 0) {
        var inputs = "";
        for (var i = 0; i < n; i++) {
          var v = urls[i] || "";
          var cls = v ? (isUrl(v) ? "good" : "bad") : "";
          var plat = detectPlatform(v);
          var platBadge = plat ? '<span class="platform-badge ' + plat.cls + '">' + plat.icon + ' ' + plat.name + '</span>' : '';
          inputs += '<div class="link-row">' +
            '<span>' + (i + 1) + '.</span>' +
            '<div style="flex:1;display:flex;align-items:center;gap:.5rem;">' +
              '<input type="url" inputmode="url" placeholder="https://instagram.com/p/..." data-tid="' + esc(t.id) + '" data-idx="' + i + '" value="' + esc(v) + '" class="' + cls + '" style="flex:1;">' +
              platBadge +
            '</div>' +
          '</div>';
        }
        linksHtml = '<div class="links-box">' +
          '<b><svg style="width:16px;height:16px;"><use href="#i-link"/></svg> Cole o link público da postagem</b>' +
          inputs +
          '<p style="margin:0;font-size:.78rem;color:var(--muted);">Apenas publicações com link válido são contabilizadas.</p>' +
        '</div>';
      }

      var customBadge = t.personalizada ? ' <span class="badge-pill" style="background:var(--navy-soft);color:var(--navy);">Ação Especial Hub</span>' : '';

      return '<li class="' + (n ? "on" : "") + '">' +
        '<div class="pick-row">' +
          '<div class="task-ico"><svg><use href="#i-rocket"/></svg></div>' +
          '<div class="label-area">' +
            '<div class="label">' + esc(t.nome) + customBadge + '<span class="worth">+' + t.pontos + ' pts</span></div>' +
            '<div style="display:flex;align-items:center;gap:.6rem;flex-wrap:wrap;margin-top:.25rem;">' +
              '<span class="condicao-tag"><b>Regra:</b> ' + esc(t.condicao || "Conforme edital") + '</span>' +
              '<button type="button" class="bulk-paste-btn" data-bulk-tid="' + esc(t.id) + '" data-bulk-name="' + esc(t.nome) + '"><svg style="width:14px;height:14px"><use href="#i-copy"/></svg> Colar Vários</button>' +
            '</div>' +
          '</div>' +
          '<div class="stepper">' +
            '<button type="button" data-act="dec" data-tid="' + esc(t.id) + '" ' + (n ? "" : "disabled") + '>−</button>' +
            '<output>' + n + '</output>' +
            '<button type="button" data-act="inc" data-tid="' + esc(t.id) + '">+</button>' +
          '</div>' +
        '</div>' +
        linksHtml +
      '</li>';
    }).join("");

    $$("#task-picker [data-act]").forEach(function (b) {
      b.addEventListener("click", function () {
        var id = b.dataset.tid;
        var n = S.counts[id] || 0;
        n = b.dataset.act === "inc" ? Math.min(n + 1, 20) : Math.max(n - 1, 0);
        S.counts[id] = n;
        S.urls[id] = (S.urls[id] || []).slice(0, n);
        renderTarefas();
      });
    });

    $$("#task-picker input[data-tid]").forEach(function (inp) {
      inp.addEventListener("input", function () {
        var id = inp.dataset.tid;
        var idx = +inp.dataset.idx;
        S.urls[id] = S.urls[id] || [];
        S.urls[id][idx] = inp.value.trim();
        inp.classList.toggle("good", isUrl(inp.value));
        inp.classList.toggle("bad", !!inp.value.trim() && !isUrl(inp.value));
        updateSubmitBar();
      });
    });

    updateSubmitBar();
  }

  function getPendingSubmissions() {
    var itens = [], pts = 0, valid = 0, missing = 0, bad = 0;
    (S.data.tarefas || []).forEach(function (t) {
      var n = S.counts[t.id] || 0;
      var urls = [];
      for (var i = 0; i < n; i++) {
        var u = (S.urls[t.id] || [])[i] || "";
        if (!u) missing++;
        else if (!isUrl(u)) bad++;
        else { urls.push(u); pts += t.pontos; valid++; }
      }
      if (urls.length) itens.push({ tarefaId: t.id, urls: urls });
    });
    return { itens: itens, pts: pts, valid: valid, missing: missing, bad: bad };
  }

  function updateSubmitBar() {
    var p = getPendingSubmissions();
    $("#sum-pts").textContent = "+" + p.pts + " pts";
    var msg = [];
    if (p.missing) msg.push(p.missing + " item(ns) sem link");
    if (p.bad) msg.push(p.bad + " link(s) inválido(s)");
    $("#sum-missing").textContent = msg.join(" · ");
    $("#send-tasks").disabled = (!p.valid || p.bad > 0);
  }

  $("#send-tasks").addEventListener("click", function () {
    var p = getPendingSubmissions();
    if (!p.valid) return;
    var btn = $("#send-tasks");
    btn.disabled = true;
    btn.textContent = "Registrando…";

    call("enviarTarefas", { itens: p.itens }).then(function (d) {
      S.data = d;
      S.counts = {};
      S.urls = {};
      toast("+" + d.enviado.pontos + " pontos registrados com sucesso!");
      renderTarefas();
    }).catch(handle).then(function () {
      btn.disabled = false;
      btn.innerHTML = '<svg style="width:18px;height:18px"><use href="#i-rocket"/></svg> Registrar Ações';
      updateSubmitBar();
    });
  });

  // ==================== ABA 3: MINHAS ENTREGAS ====================
  function renderEntregas() {
    var l = (S.data && S.data.minhasEntregas) || [];
    var STATUS_MAP = {
      pendente: "Aguardando Validação",
      validada: "Validada",
      recusada: "Recusada"
    };

    var countTodas = l.length;
    var countPendente = 0, countValidada = 0, countRecusada = 0;
    l.forEach(function (e) {
      if (e.status === "pendente") countPendente++;
      else if (e.status === "validada") countValidada++;
      else if (e.status === "recusada") countRecusada++;
    });

    if ($("#dcount-todas")) $("#dcount-todas").textContent = countTodas;
    if ($("#dcount-pendente")) $("#dcount-pendente").textContent = countPendente;
    if ($("#dcount-validada")) $("#dcount-validada").textContent = countValidada;
    if ($("#dcount-recusada")) $("#dcount-recusada").textContent = countRecusada;

    var curFilter = S.entregaFilter || "todas";
    var filteredList = l.filter(function (e) {
      if (curFilter === "todas") return true;
      return e.status === curFilter;
    });

    if (!filteredList.length) {
      $("#my-deliveries-list").innerHTML = '<li style="text-align:center;padding:2rem;color:var(--muted);">' +
        (l.length ? 'Nenhuma entrega encontrada para o filtro selecionado.' : 'Sua iniciativa ainda não realizou envios de tarefas.') +
      '</li>';
      return;
    }

    $("#my-deliveries-list").innerHTML = filteredList.map(function (e) {
      var reenviarBtn = (e.status === "recusada")
        ? '<div style="margin-top:.5rem;"><button type="button" class="btn-reenviar" data-reenviar-id="' + esc(e.id) + '" data-reenviar-tarefa="' + esc(e.tarefaNome) + '" data-reenviar-pts="' + e.pontos + '" data-reenviar-motivo="' + esc(e.motivoRecusa || 'Não informado') + '" data-reenviar-url="' + esc(e.url) + '">🔁 Corrigir e Reenviar Link</button></div>'
        : '';
      var rejectHtml = (e.status === "recusada" && e.motivoRecusa)
        ? '<div class="hist-reject-note"><b>Motivo da recusa:</b> ' + esc(e.motivoRecusa) + reenviarBtn + '</div>'
        : (e.status === "recusada" ? reenviarBtn : '');

      // Montar checkpoints de métricas pós-publicação
      var isStory = (e.tarefaId || "").indexOf("story") >= 0;
      var metricsList = e.metricas || [];
      var metricsMap = {};
      metricsList.forEach(function (m) { metricsMap[m.periodo] = m; });

      var checkpointsHtml = "";
      if (isStory) {
        // 1 Checkpoint: 24h
        var m24 = metricsMap["24h"];
        if (m24) {
          var cls = m24.status === "validada" ? "validada" : (m24.status === "recusada" ? "recusada" : "pendente");
          var stTxt = m24.status === "validada" ? "✅ 24h Validada (+5 pts)" : (m24.status === "recusada" ? "❌ 24h Recusada" : "⏳ 24h Em Análise (+5 pts)");
          var reenviarBtn = m24.status === "recusada"
            ? ' <button type="button" class="btn-reg-metrica sm" data-open-metrica data-eid="' + esc(e.id) + '" data-per="24h" data-pts="5" data-tnome="' + esc(e.tarefaNome) + '" data-url="' + esc(e.url) + '">🔁 Reenviar</button>'
            : '';
          checkpointsHtml += '<div class="metric-chip ' + cls + '">' +
            '<span class="chip-title">' + stTxt + reenviarBtn + '</span>' +
            '<span class="chip-data">👁️ ' + (m24.alcance || 0) + ' alc. • ❤️ ' + (m24.engajamento || 0) + ' eng.</span>' +
          '</div>';
        } else {
          checkpointsHtml += '<button type="button" class="btn-reg-metrica" data-open-metrica data-eid="' + esc(e.id) + '" data-per="24h" data-pts="5" data-tnome="' + esc(e.tarefaNome) + '" data-url="' + esc(e.url) + '">' +
            '➕ Registrar Insights 24h (+5 pts)' +
          '</button>';
        }
      } else {
        // 3 Checkpoints para posts: sem1, sem2, sem3
        var semanas = [
          { id: "sem1", rotulo: "1ª Semana", pts: 10 },
          { id: "sem2", rotulo: "2ª Semana", pts: 10 },
          { id: "sem3", rotulo: "3ª Semana", pts: 10 }
        ];
        checkpointsHtml = semanas.map(function (s) {
          var m = metricsMap[s.id];
          if (m) {
            var cls = m.status === "validada" ? "validada" : (m.status === "recusada" ? "recusada" : "pendente");
            var stTxt = m.status === "validada" ? ("✅ " + s.rotulo + " (+10 pts)") : (m.status === "recusada" ? ("❌ " + s.rotulo + " Recusada") : ("⏳ " + s.rotulo + " Em Análise (+10 pts)"));
            var reenviarBtn = m.status === "recusada"
              ? ' <button type="button" class="btn-reg-metrica sm" data-open-metrica data-eid="' + esc(e.id) + '" data-per="' + s.id + '" data-pts="10" data-tnome="' + esc(e.tarefaNome) + '" data-url="' + esc(e.url) + '">🔁 Reenviar</button>'
              : '';
            return '<div class="metric-chip ' + cls + '">' +
              '<span class="chip-title">' + stTxt + reenviarBtn + '</span>' +
              '<span class="chip-data">👁️ ' + (m.alcance || 0) + ' alc. • ❤️ ' + (m.engajamento || 0) + ' eng.</span>' +
            '</div>';
          } else {
            return '<button type="button" class="btn-reg-metrica" data-open-metrica data-eid="' + esc(e.id) + '" data-per="' + s.id + '" data-pts="10" data-tnome="' + esc(e.tarefaNome) + '" data-url="' + esc(e.url) + '">' +
              '➕ ' + s.rotulo + ' (+10 pts)' +
            '</button>';
          }
        }).join("");
      }

      var metricsBoxHtml = '<div class="delivery-metrics-box">' +
        '<div class="delivery-metrics-head">' +
          '<span>📊 Acompanhamento de Métricas Pós-Publicação</span>' +
          '<small>' + (isStory ? 'Stories: insights consolidados após 24h (+5 pts)' : 'Posts: envie métricas em 1, 2 e 3 semanas (+10 pts cada)') + '</small>' +
        '</div>' +
        '<div class="delivery-checkpoints-row">' + checkpointsHtml + '</div>' +
      '</div>';

      return '<li class="hist-item">' +
        '<div class="hist-main">' +
          '<div style="display:flex;align-items:center;gap:.5rem;flex-wrap:wrap;margin-bottom:.35rem;">' +
            '<button type="button" class="badge-act-id" data-copy-id="' + esc(e.id) + '" title="Clique para copiar o ID único da ação"><svg><use href="#i-copy"/></svg> ' + esc(e.id) + '</button>' +
            '<b>' + esc(e.tarefaNome) + '</b> <span class="badge-pill badge-gold">+' + e.pontos + ' pts</span>' +
          '</div>' +
          '<a href="' + esc(e.url) + '" target="_blank" rel="noopener">' + esc(e.url) + '</a>' +
          '<div class="hist-meta">' +
            '📅 Registrado em: <strong>' + esc(e.dataHora ? fmt(e.dataHora) : fmt(e.criadoEm)) + '</strong>' +
            (e.revisadoEm ? ' • <span>Revisado em: <strong>' + esc(e.revisadoDataHora ? fmt(e.revisadoDataHora) : fmt(e.revisadoEm)) + '</strong></span>' : '') +
          '</div>' +
        '</div>' +
        '<div class="hist-status">' +
          '<span class="status-pill ' + e.status + '">' + STATUS_MAP[e.status] + '</span>' +
        '</div>' +
        rejectHtml +
        metricsBoxHtml +
      '</li>';
    }).join("");
  }

  // ==================== ABA 4: CENTRAL MeC (FEED, BRIEFINGS & CRONOGRAMA) ====================
  function renderHome() {
    var d = S.data;
    if (!d) return;

    // Sub-abas do feed
    $$("[data-feed-tab]").forEach(function (b) {
      b.setAttribute("aria-selected", b.dataset.feedTab === S.feedTab);
    });
    $$("[data-feed-sec]").forEach(function (sec) {
      sec.hidden = (sec.dataset.feedSec !== S.feedTab);
    });

    // 1. Briefings Oficiais
    var bList = d.briefings || [];
    if (!bList.length) {
      $("#briefings-list").innerHTML = '<div class="panel" style="text-align:center;padding:2.5rem;color:var(--muted);">' +
        '<h3>Nenhum briefing publicado ainda</h3>' +
        '<p>A equipe do Mercado em Conexão publicará em breve os temas e diretrizes da próxima campanha.</p>' +
      '</div>';
    } else {
      $("#briefings-list").innerHTML = bList.map(function (b) {
        var statusLabel = { ativo: "Ativo / Vigente", em_breve: "Em Breve", concluido: "Concluído" }[b.status] || b.status;
        var driveBtn = isUrl(b.linkDrive)
          ? '<a href="' + esc(b.linkDrive) + '" target="_blank" rel="noopener" class="btn sm navy"><svg style="width:16px;height:16px;"><use href="#i-download"/></svg> Kit de Artes & Mídia</a>'
          : '';

        var bonusHtml = b.bonus ? '<span class="badge-pill badge-gold" style="font-size:.85rem;">🎁 Bônus: ' + esc(b.bonus) + '</span>' : '';

        return '<div class="briefing-card ' + esc(b.status) + '">' +
          '<div class="briefing-head">' +
            '<div>' +
              '<span class="badge-pill" style="background:var(--navy-soft);color:var(--navy);margin-bottom:.4rem;">' + esc(b.fase || "Campanha MeC") + '</span>' +
              '<h3 class="briefing-title">' + esc(b.titulo) + '</h3>' +
              '<div class="briefing-meta">📅 Período: ' + esc(b.periodo) + '</div>' +
            '</div>' +
            '<div><span class="status-pill ' + esc(b.status) + '">' + statusLabel + '</span></div>' +
          '</div>' +
          '<p class="briefing-desc">' + esc(b.descricao) + '</p>' +
          (b.diretrizes ? '<div class="briefing-box"><h4>📋 Diretrizes e Requisitos</h4><p>' + esc(b.diretrizes) + '</p></div>' : '') +
          (b.hashtags ? '<div class="hashtag-copy-row"><div><small style="display:block;font-size:.74rem;color:var(--muted);text-transform:uppercase;font-weight:700;">Marcações Obrigatórias:</small><code>' + esc(b.hashtags) + '</code></div><button class="btn sm ghost" type="button" data-copy="' + esc(b.hashtags) + '"><svg style="width:14px;height:14px;"><use href="#i-copy"/></svg> Copiar</button></div>' : '') +
          '<div class="briefing-actions">' +
            '<div>' + bonusHtml + '</div>' +
            '<div>' + driveBtn + '</div>' +
          '</div>' +
        '</div>';
      }).join("");

      $$("[data-copy]").forEach(function (btn) {
        btn.addEventListener("click", function () { copyText(btn.dataset.copy); });
      });
    }

    // 2. Cronograma Mensal / Linha do Tempo
    var cList = d.cronograma || [];
    if (!cList.length) {
      $("#timeline-list").innerHTML = '<li style="text-align:center;padding:2rem;color:var(--muted);">Nenhuma atividade agendada no cronograma.</li>';
    } else {
      $("#timeline-list").innerHTML = cList.map(function (c) {
        var statusLabel = { proximo: "Próxima Atividade", andamento: "Acontecendo Agora", concluido: "Concluída" }[c.status] || c.status;
        var ptsBadge = c.pontos ? '<span class="badge-pill badge-gold" style="margin-left:.4rem;">' + esc(c.pontos) + '</span>' : '';
        return '<li class="timeline-item ' + esc(c.status) + '">' +
          '<div class="timeline-date-box">' +
            '<b>' + esc(c.data.split('/')[0] || c.data) + '</b>' +
            '<small>' + esc(c.data.indexOf('/') > 0 ? c.data.split('/')[1] : 'DATA') + '</small>' +
          '</div>' +
          '<div class="timeline-info">' +
            '<div style="display:flex;align-items:center;gap:.4rem;flex-wrap:wrap;">' +
              '<span class="badge-pill badge-outro">' + esc(c.tipo || "Geral") + '</span>' +
              ptsBadge +
            '</div>' +
            '<h4>' + esc(c.titulo) + '</h4>' +
            (c.descricao ? '<p>' + esc(c.descricao) + '</p>' : '') +
            (c.local ? '<div class="loc"><svg style="width:14px;height:14px;"><use href="#i-pin"/></svg> ' + esc(c.local) + '</div>' : '') +
          '</div>' +
          '<div class="timeline-status">' +
            '<span class="status-pill ' + esc(c.status) + '">' + statusLabel + '</span>' +
          '</div>' +
        '</li>';
      }).join("");
    }

    // 3. Mural de Avisos
    var av = d.avisos || [];
    if (!av.length) {
      $("#feed-avisos").innerHTML = '<div class="aviso-item"><p style="margin:0;color:var(--muted);">Nenhum anúncio recente no momento.</p></div>';
    } else {
      $("#feed-avisos").innerHTML = av.map(function (a) {
        var dd = a.dados || {};
        var ico = "i-sparkles", kind = "Anúncio Oficial", body = "";
        if (a.tipo === "presencial") {
          ico = "i-pin"; kind = "Ação Presencial Aprovada";
          body = "<b>" + esc(a.iniciativa) + "</b> realizou: " + esc(dd.oque) + " (" + esc(dd.quando) + ")";
        } else if (a.tipo === "inscricoes") {
          ico = "i-users"; kind = "Inscrições Atribuídas";
          body = "<b>" + esc(a.iniciativa) + "</b> pontuou com " + esc(dd.quantidade) + " nova(s) inscrição(ões)!";
        } else if (a.tipo === "palestras") {
          ico = "i-mic"; kind = "Palestras da Arena";
          body = "<b>" + esc(a.iniciativa) + "</b> garantiu " + esc(dd.quantidade) + " participante(s) nas palestras!";
        } else if (a.tipo === "feira") {
          ico = "i-store"; kind = "Presença na Feira";
          body = "<b>" + esc(a.iniciativa) + "</b> levou " + esc(dd.quantidade) + " visitante(s) à feira!";
        } else if (a.tipo === "challenges") {
          ico = "i-bolt"; kind = "Challenges do Hub";
          body = "<b>" + esc(a.iniciativa) + "</b> teve " + esc(dd.quantidade) + " competidor(es) nos challenges!";
        } else if (a.tipo === "formulario") {
          ico = "i-form"; kind = "Formulário de Pesquisa";
          body = "<b>" + esc(a.iniciativa) + "</b> obteve " + esc(dd.quantidade) + " resposta(s) no formulário!";
        } else if (a.tipo === "avulso") {
          ico = "i-sparkles"; kind = "Conquista Especial";
          body = "<b>" + esc(a.iniciativa) + "</b> conquistou pontos por: " + esc(dd.titulo) + (dd.descricao ? " (" + esc(dd.descricao) + ")" : "");
        }

        return '<div class="aviso-item">' +
          '<div class="aviso-ico"><svg><use href="#' + ico + '"/></svg></div>' +
          '<div class="aviso-content"><span class="kind">' + kind + '</span><p>' + body + '</p></div>' +
          '<span class="aviso-pts">+' + a.pontos + ' pts</span>' +
        '</div>';
      }).join("");
    }

    // 4. Regras & Edital
    $("#rules-list").innerHTML = (d.regras || []).map(function (r) {
      var i = r.indexOf(":");
      return i > 0 ? '<li><b>' + esc(r.slice(0, i + 1)) + '</b>' + esc(r.slice(i + 1)) + '</li>' : '<li>' + esc(r) + '</li>';
    }).join("");

    var editalUrl = d.edital || "";
    $("#edital-container").innerHTML = isUrl(editalUrl)
      ? '<a href="' + esc(editalUrl) + '" target="_blank" rel="noopener" class="btn navy sm">Baixar Edital em PDF</a>'
      : '<span class="badge-pill" style="background:var(--line);color:var(--muted);">Link do Edital disponível em breve</span>';
  }

  // Alternância das abas internas do Feed
  $$("[data-feed-tab]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      S.feedTab = btn.dataset.feedTab;
      renderHome();
    });
  });

  // ==================== ABA 5: PAINEL DO ADMINISTRADOR ====================
  var ADM_TABS = [
    ["validar", "Validar Links", "i-check"],
    ["metricas", "📊 Acompanhamento de Métricas", "i-sparkles"],
    ["gestao-mec", "📌 Briefings & Cronograma MeC", "i-sparkles"],
    ["pontos", "Lançar Pontos do Evento", "i-trophy"],
    ["novas-acoes", "Criar Nova Ação & Avulso", "i-rocket"],
    ["historico", "Histórico e Auditoria", "i-book"],
    ["diagnostico", "🛠️ Diagnóstico & Manutenção", "i-gear"]
  ];

  function loadAdmin() {
    return call("admin").then(function (a) {
      S.adm = a;
      renderAdmin();
    });
  }

  function renderAdmin() {
    if (!S.data || !S.data.me || !S.data.me.admin) {
      S.page = "ranking";
      return renderPage();
    }
    var a = S.adm;
    var pend = a ? a.entregas.filter(function (e) { return e.status === "pendente"; }).length : 0;
    var pendMet = a && a.metricas ? a.metricas.filter(function (m) { return m.status === "pendente"; }).length : 0;

    $("#admin-tabs").innerHTML = ADM_TABS.map(function (t) {
      var badge = "";
      if (t[0] === "validar" && pend) badge = '<span class="badge-count">' + pend + '</span>';
      else if (t[0] === "metricas" && pendMet) badge = '<span class="badge-count" style="background:#059669;">' + pendMet + '</span>';
      return '<button class="admin-tab-btn" data-adm-tab="' + t[0] + '" aria-selected="' + (S.admTab === t[0]) + '">' +
        t[1] + badge + '</button>';
    }).join("");

    $$("[data-adm-tab]").forEach(function (b) {
      b.addEventListener("click", function () {
        S.admTab = b.dataset.admTab;
        renderAdmin();
      });
    });

    $$("[data-adm]").forEach(function (el) {
      el.hidden = (el.dataset.adm !== S.admTab);
    });

    if (!a) return;

    // Popula selects de iniciativas
    var opts = '<option value="">Selecione a iniciativa…</option>' + a.iniciativas.map(function (u) {
      return '<option value="' + esc(u.id) + '">' + esc(u.nome) + ' (' + esc(u.tipo || "EJ") + ')</option>';
    }).join("");
    $$(".adm-ini-select").forEach(function (s) {
      var cur = s.value;
      s.innerHTML = opts;
      s.value = cur;
    });

    var filterIni = $("#adm-filter-ini");
    var curIni = filterIni.value;
    filterIni.innerHTML = '<option value="">Todas as iniciativas</option>' + a.iniciativas.map(function (u) {
      return '<option value="' + esc(u.id) + '">' + esc(u.nome) + '</option>';
    }).join("");
    filterIni.value = curIni;

    renderAdminValidar();
    renderAdminMetricas();
    renderAdminLog();
    renderAdminCatalogo();
    renderAdminBriefings();
    renderAdminCronograma();
  }

  
  // ==================== SUB-ABA ADMIN: GESTÃO & HOMOLOGAÇÃO DE MÉTRICAS ====================
  function renderAdminMetricas() {
    var a = S.adm;
    if (!a) return;

    var kpis = a.metricasKpis || { totalAlcance: 0, totalEngajamento: 0, pendentes: 0, totalPontos: 0 };
    if ($("#adm-met-alcance")) $("#adm-met-alcance").textContent = kpis.totalAlcance.toLocaleString("pt-BR");
    if ($("#adm-met-engajamento")) $("#adm-met-engajamento").textContent = kpis.totalEngajamento.toLocaleString("pt-BR");
    if ($("#adm-met-pendentes")) $("#adm-met-pendentes").textContent = kpis.pendentes;
    if ($("#adm-met-pontos")) $("#adm-met-pontos").textContent = "+" + kpis.totalPontos + " pts";

    // Preencher select de iniciativas
    if ($("#adm-met-filter-ini") && a.iniciativas) {
      var curIni = $("#adm-met-filter-ini").value;
      $("#adm-met-filter-ini").innerHTML = '<option value="">Todas as iniciativas</option>' +
        a.iniciativas.map(function (u) {
          return '<option value="' + esc(u.id) + '">' + esc(u.nome) + '</option>';
        }).join("");
      $("#adm-met-filter-ini").value = curIni;
    }

    var list = a.metricas || [];
    var stFilter = ($("#adm-met-filter-status") && $("#adm-met-filter-status").value) || "pendente";
    var iniFilter = ($("#adm-met-filter-ini") && $("#adm-met-filter-ini").value) || "";
    var searchTxt = ($("#adm-search-met") && $("#adm-search-met").value.toLowerCase().trim()) || "";

    var filtered = list.filter(function (m) {
      if (stFilter !== "todas" && m.status !== stFilter) return false;
      if (iniFilter && m.iniciativaId !== iniFilter) return false;
      if (searchTxt) {
        var str = (m.id + " " + m.iniciativaNome + " " + m.tarefaNome + " " + m.periodoRotulo).toLowerCase();
        if (str.indexOf(searchTxt) === -1) return false;
      }
      return true;
    });

    if (!filtered.length) {
      $("#adm-met-list").innerHTML = '<div class="panel" style="text-align:center;padding:2rem;color:var(--muted);">' +
        'Nenhum registro de métrica encontrado para o filtro selecionado.' +
      '</div>';
    } else {
      $("#adm-met-list").innerHTML = filtered.map(function (m) {
        var actionsHtml = (m.status === "pendente")
          ? '<div style="display:flex;gap:.5rem;margin-top:.75rem;">' +
              '<button type="button" class="btn sm" style="background:#059669;color:#fff;" data-met-act="validar" data-met-id="' + esc(m.id) + '">✅ Aprovar (+' + m.pontos + ' pts)</button>' +
              '<button type="button" class="btn sm" style="background:#DC2626;color:#fff;" data-met-act="recusar" data-met-id="' + esc(m.id) + '">❌ Recusar</button>' +
            '</div>'
          : '<div style="margin-top:.5rem;font-size:.82rem;color:var(--muted);">' +
              (m.status === "validada" ? '<span style="color:#059669;font-weight:700;">✅ Homologado (+' + m.pontos + ' pts creditados)</span>' : '<span style="color:#DC2626;font-weight:700;">❌ Recusado: ' + esc(m.motivoRecusa || 'Não informado') + '</span>') +
              (m.revisadoEm ? ' • Revisado em ' + esc(fmt(m.revisadoEm)) : '') +
            '</div>';

        var badgeCat = (m.tipoIniciativa === "Equipe de Competição")
          ? '<span class="badge-pill badge-comp">Equipe de Competição</span>'
          : '<span class="badge-pill badge-ej">Empresa Júnior</span>';

        return '<div class="adm-met-card">' +
          '<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:.75rem;flex-wrap:wrap;">' +
            '<div>' +
              '<div style="display:flex;align-items:center;gap:.5rem;margin-bottom:.35rem;">' +
                '<span class="badge-act-id">' + esc(m.id) + '</span>' +
                '<b style="font-size:1.02rem;">' + esc(m.iniciativaNome) + '</b> ' + badgeCat +
              '</div>' +
              '<div style="font-size:.88rem;color:var(--text);">' +
                '🎯 Tarefa Original: <b>' + esc(m.tarefaNome) + '</b> • Período: <span class="badge-pill badge-gold" style="font-size:.78rem;">' + esc(m.periodoRotulo) + ' (+' + m.pontos + ' pts)</span>' +
              '</div>' +
              (m.urlOriginal ? '<div style="font-size:.82rem;margin-top:.2rem;"><a href="' + esc(m.urlOriginal) + '" target="_blank" rel="noopener" style="color:var(--primary-deep);">🔗 Ver publicação original no Instagram/Rede</a></div>' : '') +
            '</div>' +
            '<div><span class="status-pill ' + esc(m.status) + '">' + (m.status === "validada" ? "Validada" : (m.status === "recusada" ? "Recusada" : "Aguardando Validação")) + '</span></div>' +
          '</div>' +
          '<div class="adm-met-grid">' +
            '<div><small style="color:var(--muted);display:block;font-size:.74rem;">👁️ ALCANCE</small><b style="font-size:1.1rem;color:#0284C7;">' + (m.alcance || 0).toLocaleString("pt-BR") + '</b></div>' +
            '<div><small style="color:var(--muted);display:block;font-size:.74rem;">❤️ ENGAJAMENTO</small><b style="font-size:1.1rem;color:#E11D48;">' + (m.engajamento || 0).toLocaleString("pt-BR") + '</b></div>' +
            '<div><small style="color:var(--muted);display:block;font-size:.74rem;">📸 COMPROVANTE</small><a href="' + esc(m.comprovanteUrl) + '" target="_blank" rel="noopener" class="link-btn" style="font-size:.82rem;">Ver Print / Insights ↗</a></div>' +
            '<div><small style="color:var(--muted);display:block;font-size:.74rem;">📅 ENVIADO EM</small><span style="font-size:.82rem;font-weight:600;">' + esc(fmt(m.criadoEm)) + '</span></div>' +
          '</div>' +
          (m.observacoes ? '<div style="font-size:.82rem;color:var(--muted);background:var(--surface);padding:.4rem .6rem;border-radius:6px;border-left:3px solid var(--primary);margin-top:.5rem;"><b>Observações:</b> ' + esc(m.observacoes) + '</div>' : '') +
          actionsHtml +
        '</div>';
      }).join("");

      // Event listeners dos botões de ação do card de métrica
      $$("[data-met-act]").forEach(function (btn) {
        btn.addEventListener("click", function () {
          var act = btn.dataset.metAct;
          var mid = btn.dataset.metId;
          if (act === "validar") {
            btn.disabled = true;
            call("validarMetricaEntrega", { metricaId: mid, status: "validada" }).then(function (res) {
              S.adm = res;
              renderAdmin();
              toast("Métrica " + mid + " aprovada com sucesso! Pontos creditados.");
            }).catch(function (err) {
              toast(err.message, "erro");
              btn.disabled = false;
            });
          } else if (act === "recusar") {
            var motivo = prompt("Informe o motivo da recusa (para orientação da equipe):", "Print ilegível ou métrica não correspondente ao post.");
            if (motivo === null) return;
            btn.disabled = true;
            call("validarMetricaEntrega", { metricaId: mid, status: "recusada", motivoRecusa: motivo }).then(function (res) {
              S.adm = res;
              renderAdmin();
              toast("Métrica " + mid + " recusada.");
            }).catch(function (err) {
              toast(err.message, "erro");
              btn.disabled = false;
            });
          }
        });
      });
    }

    // Renderizar Radar de Engajamento por Iniciativa
    if ($("#adm-radar-tbody") && a.iniciativas) {
      var statsPorIni = {};
      a.iniciativas.forEach(function (u) {
        statsPorIni[u.id] = { nome: u.nome, tipo: u.tipo, relatorios: 0, alcance: 0, engajamento: 0, pontos: 0 };
      });
      list.forEach(function (m) {
        if (!statsPorIni[m.iniciativaId]) {
          statsPorIni[m.iniciativaId] = { nome: m.iniciativaNome, tipo: m.tipoIniciativa, relatorios: 0, alcance: 0, engajamento: 0, pontos: 0 };
        }
        var rec = statsPorIni[m.iniciativaId];
        rec.relatorios++;
        if (m.status === "validada") {
          rec.alcance += (parseInt(m.alcance, 10) || 0);
          rec.engajamento += (parseInt(m.engajamento, 10) || 0);
          rec.pontos += (parseInt(m.pontos, 10) || 0);
        }
      });
      var radarList = Object.values(statsPorIni);
      radarList.sort(function (x, y) { return (y.alcance + y.engajamento) - (x.alcance + x.engajamento); });

      $("#adm-radar-tbody").innerHTML = radarList.map(function (r) {
        var badgeCat = (r.tipo === "Equipe de Competição")
          ? '<span class="badge-pill badge-comp">Equipe de Competição</span>'
          : '<span class="badge-pill badge-ej">Empresa Júnior</span>';
        return '<tr style="border-bottom:1px solid var(--line);">' +
          '<td style="padding:.65rem .8rem;font-weight:700;">' + esc(r.nome) + '</td>' +
          '<td style="padding:.65rem .8rem;">' + badgeCat + '</td>' +
          '<td style="padding:.65rem .8rem;text-align:center;"><span class="badge-pill badge-gold">' + r.relatorios + '</span></td>' +
          '<td style="padding:.65rem .8rem;text-align:right;font-weight:700;color:#0284C7;">' + r.alcance.toLocaleString("pt-BR") + '</td>' +
          '<td style="padding:.65rem .8rem;text-align:right;font-weight:700;color:#E11D48;">' + r.engajamento.toLocaleString("pt-BR") + '</td>' +
          '<td style="padding:.65rem .8rem;text-align:right;font-weight:800;color:#059669;">+' + r.pontos + ' pts</td>' +
        '</tr>';
      }).join("");
    }
  }

  function renderAdminValidar() {
    var a = S.adm;
    if (!a) return;

    // Cálculo das métricas para o painel
    var cPen = 0, cVal = 0, cRec = 0;
    a.entregas.forEach(function (e) {
      if (e.status === "pendente") cPen++;
      else if (e.status === "validada") cVal++;
      else if (e.status === "recusada") cRec++;
    });
    if ($("#adm-metric-pendente")) $("#adm-metric-pendente").textContent = cPen;
    if ($("#adm-metric-validada")) $("#adm-metric-validada").textContent = cVal;
    if ($("#adm-metric-recusada")) $("#adm-metric-recusada").textContent = cRec;
    if ($("#adm-metric-total")) $("#adm-metric-total").textContent = a.entregas.length;

    var st = $("#adm-filter-status").value;
    var ini = $("#adm-filter-ini").value;
    var q = ($("#adm-search-val") ? $("#adm-search-val").value.trim().toLowerCase() : "");

    var list = a.entregas.filter(function (e) {
      if (st !== "todas" && e.status !== st) return false;
      if (ini && e.iniciativaId !== ini) return false;
      if (q) {
        var str = (String(e.id || "") + " " + String(e.iniciativa || "") + " " + String(e.tarefaNome || "") + " " + String(e.url || "")).toLowerCase();
        if (str.indexOf(q) < 0) return false;
      }
      return true;
    });

    if (!list.length) {
      $("#adm-val-list").innerHTML = '<p style="text-align:center;padding:2rem;color:var(--muted);">Nenhuma entrega encontrada para este filtro ou busca.</p>';
      return;
    }

    $("#adm-val-list").innerHTML = list.map(function (e) {
      var btns = "";
      if (e.status !== "validada") {
        btns += '<button class="btn sm" style="background:var(--plus);color:#fff;" data-action-val="validada" data-id="' + esc(e.id) + '">Aprovar (+' + e.pontos + ' pts)</button>';
      }
      if (e.status !== "recusada") {
        btns += '<button class="btn sm" style="background:var(--minus);color:#fff;" data-action-reject="' + esc(e.id) + '">Recusar</button>';
      }
      if (e.status !== "pendente") {
        btns += '<button class="btn sm ghost" data-action-val="pendente" data-id="' + esc(e.id) + '">Desfazer</button>';
      }

      var rejectMotivo = (e.status === "recusada" && e.motivoRecusa)
        ? '<div class="hist-reject-note"><b>Motivo da recusa:</b> ' + esc(e.motivoRecusa) + '</div>'
        : '';

      return '<div class="val-item">' +
        '<div>' +
          '<div class="val-header">' +
            '<button type="button" class="badge-act-id" data-copy-id="' + esc(e.id) + '" title="Clique para copiar o ID"><svg><use href="#i-copy"/></svg> ' + esc(e.id) + '</button>' +
            '<b>' + esc(e.iniciativa) + '</b> <span class="badge-pill badge-ej">' + esc(e.tipoIniciativa || "EJ") + '</span> <span class="status-pill ' + e.status + '">' + e.status + '</span>' +
          '</div>' +
          '<div class="val-meta-row">' +
            '<strong>' + esc(e.tarefaNome) + '</strong> • <span class="badge-gold">+' + e.pontos + ' pts</span> • <span>📅 Enviado em: <strong>' + esc(e.dataHora ? fmt(e.dataHora) : fmt(e.criadoEm)) + '</strong></span>' +
            (e.revisadoEm ? ' • <span>Revisado em: <strong>' + esc(e.revisadoDataHora ? fmt(e.revisadoDataHora) : fmt(e.revisadoEm)) + '</strong></span>' : '') +
          '</div>' +
          '<a href="' + esc(e.url) + '" target="_blank" rel="noopener" style="font-size:.85rem;word-break:break-all;">' + esc(e.url) + '</a>' +
          rejectMotivo +
        '</div>' +
        '<div class="val-actions">' + btns + '</div>' +
      '</div>';
    }).join("");

    $$("[data-action-val]").forEach(function (b) {
      b.addEventListener("click", function () {
        b.disabled = true;
        call("validarEntrega", { id: b.dataset.id, status: b.dataset.actionVal }).then(function (res) {
          S.adm = res;
          renderAdmin();
          toast("Entrega atualizada!");
        }).catch(handle);
      });
    });

    $$("[data-action-reject]").forEach(function (b) {
      b.addEventListener("click", function () {
        S.rejectDeliveryId = b.dataset.actionReject;
        $("#reject-modal").hidden = false;
      });
    });
  }

  $("#adm-filter-status").addEventListener("change", renderAdminValidar);
  $("#adm-filter-ini").addEventListener("change", renderAdminValidar);
  if ($("#adm-search-val")) $("#adm-search-val").addEventListener("input", renderAdminValidar);

  // Modal de Recusa
  $("#reject-cancel-btn").addEventListener("click", function () {
    $("#reject-modal").hidden = true;
    S.rejectDeliveryId = null;
  });
  $("#reject-preset").addEventListener("change", function () {
    $("#reject-custom-wrap").style.display = ($("#reject-preset").value === "outro") ? "block" : "none";
  });
  $("#reject-confirm-btn").addEventListener("click", function () {
    if (!S.rejectDeliveryId) return;
    var motivo = $("#reject-preset").value;
    if (motivo === "outro") {
      motivo = $("#reject-custom-text").value.trim() || "Conteúdo não atende aos requisitos";
    }
    call("validarEntrega", { id: S.rejectDeliveryId, status: "recusada", motivoRecusa: motivo }).then(function (res) {
      S.adm = res;
      $("#reject-modal").hidden = true;
      S.rejectDeliveryId = null;
      renderAdmin();
      toast("Entrega recusada com justificativa.");
    }).catch(handle);
  });

  // Formulários de Gestão do Admin
  function bindAdminForm(formId, acao, okMsg) {
    var f = $("#" + formId);
    if (!f) return;
    f.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var data = {};
      $$("input, select, textarea", f).forEach(function (el) { if (el.name) data[el.name] = el.value; });
      var err = f.querySelector(".error-box");
      if (err) err.hidden = true;
      var btn = f.querySelector("button[type=submit]");
      btn.disabled = true;

      call(acao, data).then(function (res) {
        S.adm = res;
        f.reset();
        renderAdmin();
        toast(okMsg);
      }).catch(function (e) {
        if (err) {
          err.textContent = e.message;
          err.hidden = false;
        } else {
          toast(e.message, true);
        }
      }).then(function () {
        btn.disabled = false;
      });
    });
  }

  bindAdminForm("f-adm-briefing", "salvarBriefing", "Briefing publicado com sucesso!");
  bindAdminForm("f-adm-cronograma", "salvarCronograma", "Atividade adicionada ao calendário!");
  bindAdminForm("f-adm-inscricoes", "publicarInscricoes", "Inscrições lançadas com sucesso!");
  bindAdminForm("f-adm-formulario", "publicarFormulario", "Respostas de formulário lançadas!");
  bindAdminForm("f-adm-palestras", "publicarPalestras", "Presença em palestras lançada!");
  bindAdminForm("f-adm-feira", "publicarFeira", "Visitas na feira lançadas!");
  bindAdminForm("f-adm-challenges", "publicarChallenges", "Challenges lançados!");
  bindAdminForm("f-adm-presencial", "publicarPresencial", "Ação presencial publicada com sucesso!");
  bindAdminForm("f-adm-avulso", "publicarAcaoAvulsa", "Pontuação avulsa atribuída à iniciativa!");
  bindAdminForm("f-adm-catalogo", "criarAcaoCatalogo", "Nova tarefa adicionada ao catálogo de envios!");

  $("#avulso-modo").addEventListener("change", function () {
    var isQtd = ($("#avulso-modo").value === "quantidade");
    $("#avulso-fixo-wrap").style.display = isQtd ? "none" : "block";
    $("#avulso-qtd-wrap").style.display = isQtd ? "grid" : "none";
  });

  function renderAdminBriefings() {
    var list = (S.adm && S.adm.briefings) || [];
    if (!list.length) {
      $("#adm-briefings-list").innerHTML = '<small style="color:var(--muted);">Nenhum briefing cadastrado.</small>';
      return;
    }
    $("#adm-briefings-list").innerHTML = list.map(function (b) {
      return '<div style="background:var(--surface-alt);border:1px solid var(--line);border-radius:10px;padding:.6rem .85rem;margin-bottom:.5rem;display:flex;justify-content:space-between;align-items:center;">' +
        '<div><b>' + esc(b.titulo) + '</b> (' + esc(b.fase) + ')<br><small style="color:var(--muted);">' + esc(b.periodo) + '</small></div>' +
        '<button class="btn sm ghost" data-del-briefing="' + esc(b.id) + '" style="color:var(--minus);">Remover</button>' +
      '</div>';
    }).join("");

    $$("[data-del-briefing]").forEach(function (b) {
      b.addEventListener("click", function () {
        if (!confirm("Deseja remover este briefing?")) return;
        call("removerBriefing", { id: b.dataset.delBriefing }).then(function (res) {
          S.adm = res;
          renderAdmin();
          toast("Briefing removido.");
        }).catch(handle);
      });
    });
  }

  function renderAdminCronograma() {
    var list = (S.adm && S.adm.cronograma) || [];
    if (!list.length) {
      $("#adm-crono-list").innerHTML = '<small style="color:var(--muted);">Nenhuma atividade agendada.</small>';
      return;
    }
    $("#adm-crono-list").innerHTML = list.map(function (c) {
      return '<div style="background:var(--surface-alt);border:1px solid var(--line);border-radius:10px;padding:.6rem .85rem;margin-bottom:.5rem;display:flex;justify-content:space-between;align-items:center;">' +
        '<div><b>' + esc(c.data) + '</b>: ' + esc(c.titulo) + '<br><small style="color:var(--muted);">' + esc(c.local) + '</small></div>' +
        '<button class="btn sm ghost" data-del-crono="' + esc(c.id) + '" style="color:var(--minus);">Remover</button>' +
      '</div>';
    }).join("");

    $$("[data-del-crono]").forEach(function (b) {
      b.addEventListener("click", function () {
        if (!confirm("Deseja remover esta atividade do calendário?")) return;
        call("removerCronograma", { id: b.dataset.delCrono }).then(function (res) {
          S.adm = res;
          renderAdmin();
          toast("Atividade removida.");
        }).catch(handle);
      });
    });
  }

  function renderAdminCatalogo() {
    var list = (S.adm && S.adm.catalogo) || [];
    if (!list.length) {
      $("#adm-catalogo-list").innerHTML = '<small style="color:var(--muted);">Nenhuma tarefa personalizada cadastrada.</small>';
      return;
    }
    $("#adm-catalogo-list").innerHTML = list.map(function (c) {
      return '<div style="background:var(--surface-alt);border:1px solid var(--line);border-radius:10px;padding:.5rem .75rem;margin-bottom:.4rem;display:flex;justify-content:space-between;align-items:center;">' +
        '<div><b>' + esc(c.nome) + '</b> (+' + c.pontos + ' pts)<br><small style="color:var(--muted);">' + esc(c.condicao) + '</small></div>' +
        '<button class="btn sm ghost" data-del-catalogo="' + esc(c.id) + '" style="color:var(--minus);">Desativar</button>' +
      '</div>';
    }).join("");

    $$("[data-del-catalogo]").forEach(function (b) {
      b.addEventListener("click", function () {
        if (!confirm("Deseja desativar esta tarefa do catálogo?")) return;
        call("removerAcaoCatalogo", { id: b.dataset.delCatalogo }).then(function (res) {
          S.adm = res;
          renderAdmin();
          toast("Tarefa desativada.");
        }).catch(handle);
      });
    });
  }

  function renderAdminLog() {
    var l = (S.adm && S.adm.historico) || [];
    if (!l.length) {
      $("#adm-log-list").innerHTML = '<li style="text-align:center;padding:2rem;color:var(--muted);">Nenhum lançamento no histórico.</li>';
      return;
    }

    $("#adm-log-list").innerHTML = l.map(function (a) {
      var d = a.dados || {};
      var desc = a.iniciativa ? "<b>" + esc(a.iniciativa) + "</b> · " : "";
      if (a.tipo === "tarefa") desc += "Missão do Hub: " + esc(d.sobre || "");
      else if (a.tipo === "avulso") desc += esc(d.titulo || "Ação Avulsa") + " (+" + a.pontos + " pts)";
      else desc += esc(a.tipo) + " (+" + a.pontos + " pts)";

      var estornarBtn = (a.status !== "cancelado" && a.tipo !== "tarefa")
        ? '<button class="btn sm ghost" data-cancel-aviso="' + esc(a.id) + '" style="color:var(--minus);">Estornar</button>'
        : '';

      return '<li class="hist-item">' +
        '<div>' +
          '<div style="display:flex;align-items:center;gap:.5rem;flex-wrap:wrap;margin-bottom:.3rem;">' +
            '<button type="button" class="badge-act-id" data-copy-id="' + esc(a.id) + '" title="Clique para copiar o ID"><svg><use href="#i-copy"/></svg> ' + esc(a.id) + '</button>' +
            '<span class="status-pill ' + (a.status || "ativo") + '">' + (a.status === "cancelado" ? "Estornado" : "Ativo") + '</span>' +
          '</div>' +
          '<div style="margin:.3rem 0;font-weight:600;">' + desc + '</div>' +
          '<small style="color:var(--muted);">📅 Publicado em: <strong>' + esc(a.dataHora ? fmt(a.dataHora) : fmt(a.criadoEm)) + '</strong></small>' +
        '</div>' +
        '<div>' + estornarBtn + '</div>' +
      '</li>';
    }).join("");

    $$("[data-cancel-aviso]").forEach(function (b) {
      b.addEventListener("click", function () {
        if (!confirm("Tem certeza que deseja cancelar e estornar esta pontuação do ranking?")) return;
        call("cancelarAviso", { id: b.dataset.cancelAviso }).then(function (res) {
          S.adm = res;
          renderAdmin();
          toast("Lançamento estornado do ranking.");
        }).catch(handle);
      });
    });
  }

  // Diagnóstico & Manutenção da Base
  $("#btn-reparar-datas").addEventListener("click", function () {
    var btn = $("#btn-reparar-datas");
    btn.disabled = true;
    btn.textContent = "Verificando e formatando…";
    call("repararDatas").then(function (res) {
      toast(res.mensagem || "Datas da planilha higienizadas com sucesso!");
    }).catch(handle).then(function () {
      btn.disabled = false;
      btn.textContent = "✨ Reparar Datas da Planilha Agora";
    });
  });

  $("#btn-export-backup").addEventListener("click", function () {
    var backup = {
      exportadoEm: new Date().toISOString(),
      versao: "2.1.0",
      iniciativaAdmin: (S.data && S.data.me) ? S.data.me.nome : "UFMG Hub",
      data: S.data,
      admin: S.adm
    };
    var blob = new Blob([JSON.stringify(backup, null, 2)], { type: "application/json" });
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url;
    a.download = "arena_backup_" + new Date().toISOString().slice(0, 10) + ".json";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    toast("Backup JSON exportado com sucesso!");
  });

  // ==================== AUTH ====================
  function authScreen(which) {
    show("auth");
    $("#signup").hidden = which !== "signup";
    $("#login").hidden = which !== "login";
  }
  $$("[data-go]").forEach(function (b) {
    b.addEventListener("click", function () { authScreen(b.dataset.go); });
  });

  $("#signup").addEventListener("submit", function (ev) {
    ev.preventDefault();
    var f = ev.target;
    var d = {};
    $$("input, select", f).forEach(function (el) { if (el.name) d[el.name] = el.value.trim(); });
    var err = $("#signup-error");
    err.hidden = true;
    var btn = f.querySelector("button[type=submit]");
    btn.disabled = true;
    btn.textContent = "Cadastrando…";

    call("cadastrar", d).then(function (r) {
      store("arena-token", r.token);
      start(r.token);
    }).catch(function (e) {
      err.textContent = e.message;
      err.hidden = false;
    }).then(function () {
      btn.disabled = false;
      btn.textContent = "Cadastrar Iniciativa";
    });
  });

  $("#login").addEventListener("submit", function (ev) {
    ev.preventDefault();
    var f = ev.target;
    var d = { nome: f.nome.value.trim(), senha: f.senha.value };
    var err = $("#login-error");
    err.hidden = true;
    var btn = f.querySelector("button[type=submit]");
    btn.disabled = true;
    btn.textContent = "Entrando…";

    call("entrar", d).then(function (r) {
      store("arena-token", r.token);
      start(r.token);
    }).catch(function (e) {
      err.textContent = e.message;
      err.hidden = false;
    }).then(function () {
      btn.disabled = false;
      btn.textContent = "Entrar na Arena";
    });
  });

  function logout() {
    S.token = null;
    S.data = null;
    S.adm = null;
    store("arena-token", null);
    authScreen("login");
  }
  $("#logout").addEventListener("click", logout);

  function start(token) {
    S.token = token;
    show("boot");
    loadHome().then(function () {
      show("app");
      S.page = "ranking";
      renderNav();
      renderPage();
    }).catch(function (e) {
      if (e.sair) logout();
      else show("unavailable");
    });
  }

  function loadHome() {
    return call("painel").then(function (d) {
      S.data = d;
      S.offset = d.agora - Date.now();
    });
  }

  // ==================== MOCK LOCAL PARA TESTES ====================
  function mockApi(acao, dados, token) {
    var stored = store("arena_mock_db_v3");
    var db = stored ? JSON.parse(stored) : getInitialMockDb();

    // Utilitários de formato para o mock
    var pad = function (n) { return n < 10 ? "0" + n : "" + n; };
    var nowDt = new Date();
    var nowDataHoraStr = pad(nowDt.getDate()) + "/" + pad(nowDt.getMonth() + 1) + "/" + nowDt.getFullYear() + " " + pad(nowDt.getHours()) + ":" + pad(nowDt.getMinutes()) + ":" + pad(nowDt.getSeconds());
    var yy = String(nowDt.getFullYear()).slice(-2);
    var mm = pad(nowDt.getMonth() + 1);
    var dd = pad(nowDt.getDate());
    var randChars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";

    // Migração de integridade para dados já persistidos no navegador
    if (db && db.entregas) {
      db.entregas.forEach(function (e) {
        if (!e.id || e.id.indexOf("#ACT-") !== 0) {
          var randSuffix = "";
          for (var k = 0; k < 4; k++) randSuffix += randChars.charAt(Math.floor(Math.random() * randChars.length));
          e.id = "#ACT-" + yy + mm + dd + "-" + randSuffix;
        }
        if (!e.dataHora) e.dataHora = nowDataHoraStr;
      });
    }
    if (db && db.avisos) {
      db.avisos.forEach(function (a) {
        if (!a.id || a.id.indexOf("#LNC-") !== 0) {
          var randSuffix = "";
          for (var k = 0; k < 4; k++) randSuffix += randChars.charAt(Math.floor(Math.random() * randChars.length));
          a.id = "#LNC-" + yy + mm + dd + "-" + randSuffix;
        }
        if (!a.dataHora) a.dataHora = nowDataHoraStr;
      });
    }

    function saveDb() { store("arena_mock_db_v3", JSON.stringify(db)); }

    if (acao === "cadastrar") {
      var exists = db.inis.some(function (u) { return u.nome.toLowerCase() === dados.nome.toLowerCase(); });
      if (exists) return { erro: "Iniciativa já cadastrada." };
      var newU = {
        id: "ini_" + Date.now(),
        nome: dados.nome,
        tipo: dados.tipo || "Empresa Júnior",
        representante: dados.representante,
        cargo: dados.cargo,
        redeSocial: dados.redeSocial,
        admin: dados.nome.toLowerCase() === "ufmg hub" ? "sim" : "",
        senha: dados.senha
      };
      db.inis.push(newU);
      saveDb();
      return { token: newU.id, nome: newU.nome, admin: newU.admin === "sim" };
    }

    if (acao === "entrar") {
      var u = db.inis.filter(function (x) { return x.nome.toLowerCase() === dados.nome.toLowerCase(); })[0];
      if (!u || u.senha !== dados.senha) return { erro: "Nome ou senha incorretos." };
      return { token: u.id, nome: u.nome, admin: u.admin === "sim" };
    }

    var me = db.inis.filter(function (x) { return x.id === token; })[0];
    if (!me) return { erro: "Sessão expirada.", sair: true };

    if (acao === "painel") {
      var rList = computeMockRanking(db);
      var minhas = db.entregas.filter(function (e) { return e.iniciativaId === me.id; });
      return {
        me: { id: me.id, nome: me.nome, tipo: me.tipo, representante: me.representante, cargo: me.cargo, admin: me.admin === "sim" },
        ranking: rList,
        estatisticas: {
          totalIniciativas: rList.length,
          totalPontos: rList.reduce(function (a, b) { return a + b.pontos; }, 0),
          totalValidadas: db.entregas.filter(function (e) { return e.status === "validada"; }).length,
          liderNome: rList[0] ? rList[0].nome : "—",
          liderPontos: rList[0] ? rList[0].pontos : 0
        },
        tarefaHub: db.tarefaHub,
        avisos: db.avisos.filter(function (a) { return a.status !== "cancelado"; }),
        briefings: (db.briefings || []).filter(function (b) { return b.status !== "removido"; }),
        cronograma: (db.cronograma || []).filter(function (c) { return c.status !== "removido"; }),
        regras: [
          "Perfil Público: Mantenha a conta da iniciativa pública durante toda a competição.",
          "Marcação Obrigatória: Sempre marque o perfil oficial @mercadoemconexao.",
          "Post Ativo: Não apague nem arquive a publicação do Feed após o envio.",
          "Respeito e Ética: O conteúdo não pode conter palavrões, termos ofensivos ou preconceituosos.",
          "Validação no Prazo: Envie o link do post dentro do prazo de cada tarefa para homologação dos pontos.",
          "Limite de Inscrições: A pontuação de inscrições atribuídas à iniciativa tem teto máximo de 200 pontos na campanha."
        ],
        tarefas: db.tarefasCatalogo,
        minhasEntregas: minhas,
        config: { marcacao: "Não esqueça de marcar a @mercadoemconexao!", tarefaPadrao: "Nenhuma missão aberta no momento.", pontosPorInscricao: 2, limiteInscricoes: 200 },
        agora: Date.now()
      };
    }

    if (acao === "enviarTarefas") {
      var mapaUrls = {};
      db.entregas.forEach(function (e) {
        if (e.status !== "recusada") {
          var uClean = (e.url || "").trim().replace(/\/+$/, "").replace(/[?&](utm_[^&=]+|igsh|fbclid|src|ref|share_id)=[^&=]*/gi, '').replace(/[?&]+$/, '');
          if (uClean) mapaUrls[uClean] = { id: e.id, iniciativaId: e.iniciativaId };
        }
      });
      var lote = {};
      for (var i = 0; i < (dados.itens || []).length; i++) {
        var it = dados.itens[i];
        for (var j = 0; j < (it.urls || []).length; j++) {
          var uClean = (it.urls[j] || "").trim().replace(/\/+$/, "").replace(/[?&](utm_[^&=]+|igsh|fbclid|src|ref|share_id)=[^&=]*/gi, '').replace(/[?&]+$/, '');
          if (lote[uClean]) return { erro: "Você incluiu o mesmo link mais de uma vez no mesmo envio." };
          lote[uClean] = true;
          if (mapaUrls[uClean]) {
            var anterior = mapaUrls[uClean];
            if (anterior.iniciativaId === me.id) {
              return { erro: "Você já enviou este link anteriormente (" + anterior.id + "). Aguarde a validação." };
            } else {
              return { erro: "Este link já foi registrado por outra iniciativa no sistema." };
            }
          }
        }
      }

      var novos = [];
      (dados.itens || []).forEach(function (it) {
        var t = db.tarefasCatalogo.filter(function (x) { return x.id === it.tarefaId; })[0];
        if (!t) return;
        (it.urls || []).forEach(function (u) {
          var randSuffix = "";
          for (var k = 0; k < 4; k++) randSuffix += randChars.charAt(Math.floor(Math.random() * randChars.length));
          var idUnico = "#ACT-" + yy + mm + dd + "-" + randSuffix;

          novos.push({
            id: idUnico,
            iniciativaId: me.id,
            tarefaId: t.id,
            tarefaNome: t.nome,
            pontos: t.pontos,
            url: u,
            status: "pendente",
            motivoRecusa: "",
            criadoEm: nowDt.getTime(),
            dataHora: nowDataHoraStr,
            revisadoEm: "",
            revisadoDataHora: ""
          });
        });
      });
      db.entregas = novos.concat(db.entregas);
      saveDb();
      var p = mockApi("painel", {}, token);
      p.enviado = { links: novos.length, pontos: novos.reduce(function (s, x) { return s + x.pontos; }, 0) };
      return p;
    }

    if (acao === "admin") {
      return {
        entregas: db.entregas.map(function (e) {
          var ini = db.inis.filter(function (x) { return x.id === e.iniciativaId; })[0] || {};
          return Object.assign({}, e, { iniciativa: ini.nome || "—", tipoIniciativa: ini.tipo || "EJ" });
        }),
        historico: db.avisos,
        iniciativas: db.inis.filter(function (u) { return u.admin !== "sim"; }),
        catalogo: db.tarefasCatalogo.filter(function (t) { return t.personalizada; }),
        briefings: (db.briefings || []).filter(function (b) { return b.status !== "removido"; }),
        cronograma: (db.cronograma || []).filter(function (c) { return c.status !== "removido"; }),
        agora: Date.now()
      };
    }

    if (acao === "salvarBriefing") {
      db.briefings = db.briefings || [];
      var bId = dados.id || ("#BRF-" + yy + mm + dd + "-" + ("0000" + Math.floor(Math.random() * 9999 + 1)).slice(-4));
      var bIdx = db.briefings.findIndex(function (x) { return x.id === bId; });
      var bObj = {
        id: bId,
        titulo: dados.titulo,
        fase: dados.fase || "Geral",
        periodo: dados.periodo || "Durante a Arena",
        descricao: dados.descricao,
        diretrizes: dados.diretrizes || "",
        linkDrive: dados.linkDrive || "",
        hashtags: dados.hashtags || "@mercadoemconexao #ArenaMeC",
        bonus: dados.bonus || "",
        status: dados.status || "ativo",
        criadoEm: nowDt.getTime(),
        dataHora: nowDataHoraStr
      };
      if (bIdx >= 0) db.briefings[bIdx] = bObj;
      else db.briefings.unshift(bObj);
      saveDb();
      return mockApi("admin", {}, token);
    }

    if (acao === "removerBriefing") {
      db.briefings = db.briefings || [];
      var item = db.briefings.filter(function (x) { return x.id === dados.id; })[0];
      if (item) item.status = "removido";
      saveDb();
      return mockApi("admin", {}, token);
    }

    if (acao === "salvarCronograma") {
      db.cronograma = db.cronograma || [];
      var cId = dados.id || ("#CRN-" + yy + mm + dd + "-" + ("0000" + Math.floor(Math.random() * 9999 + 1)).slice(-4));
      var cIdx = db.cronograma.findIndex(function (x) { return x.id === cId; });
      var cObj = {
        id: cId,
        data: dados.data,
        titulo: dados.titulo,
        local: dados.local || "Campus Pampulha",
        tipo: dados.tipo || "Presencial",
        pontos: dados.pontos || "",
        descricao: dados.descricao || "",
        status: dados.status || "proximo",
        criadoEm: nowDt.getTime(),
        dataHora: nowDataHoraStr
      };
      if (cIdx >= 0) db.cronograma[cIdx] = cObj;
      else db.cronograma.push(cObj);
      saveDb();
      return mockApi("admin", {}, token);
    }

    if (acao === "removerCronograma") {
      db.cronograma = db.cronograma || [];
      var item = db.cronograma.filter(function (x) { return x.id === dados.id; })[0];
      if (item) item.status = "removido";
      saveDb();
      return mockApi("admin", {}, token);
    }

    if (acao === "validarEntrega") {
      var ent = db.entregas.filter(function (x) { return x.id === dados.id; })[0];
      if (ent) {
        var rdt = new Date();
        var revStr = pad(rdt.getDate()) + "/" + pad(rdt.getMonth() + 1) + "/" + rdt.getFullYear() + " " + pad(rdt.getHours()) + ":" + pad(rdt.getMinutes()) + ":" + pad(rdt.getSeconds());
        ent.status = dados.status;
        ent.motivoRecusa = dados.motivoRecusa || "";
        ent.revisadoEm = (dados.status === "pendente") ? "" : rdt.getTime();
        ent.revisadoDataHora = (dados.status === "pendente") ? "" : revStr;
        saveDb();
      }
      return mockApi("admin", {}, token);
    }

    if (acao === "publicarInscricoes" || acao === "publicarFormulario" || acao === "publicarPalestras" || acao === "publicarFeira" || acao === "publicarChallenges") {
      var mapPts = { publicarInscricoes: 2, publicarFormulario: 1, publicarPalestras: 1, publicarFeira: 1, publicarChallenges: 1 };
      var tipoMap = { publicarInscricoes: "inscricoes", publicarFormulario: "formulario", publicarPalestras: "palestras", publicarFeira: "feira", publicarChallenges: "challenges" };
      var qtd = parseInt(dados.quantidade, 10) || 0;
      var ptsUnit = mapPts[acao];
      var targetIni = db.inis.filter(function (x) { return x.id === dados.iniciativaId; })[0];
      var adt = new Date();
      var lncDateStr = pad(adt.getDate()) + "/" + pad(adt.getMonth() + 1) + "/" + adt.getFullYear() + " " + pad(adt.getHours()) + ":" + pad(adt.getMinutes()) + ":" + pad(adt.getSeconds());
      var randSuffix = "";
      for (var k = 0; k < 4; k++) randSuffix += randChars.charAt(Math.floor(Math.random() * randChars.length));
      var idUnico = "#LNC-" + yy + mm + dd + "-" + randSuffix;

      db.avisos.unshift({
        id: idUnico,
        tipo: tipoMap[acao],
        iniciativaId: targetIni.id,
        iniciativa: targetIni.nome,
        pontos: qtd * ptsUnit,
        dados: { quantidade: qtd },
        criadoEm: adt.getTime(),
        dataHora: lncDateStr,
        expiraEm: adt.getTime() + 48 * 3600000,
        status: "ativo"
      });
      saveDb();
      return mockApi("admin", {}, token);
    }

    if (acao === "publicarPresencial") {
      var targetIni = db.inis.filter(function (x) { return x.id === dados.iniciativaId; })[0];
      var pts = Math.min(40, parseInt(dados.pontos, 10) || 0);
      var adt = new Date();
      var lncDateStr = pad(adt.getDate()) + "/" + pad(adt.getMonth() + 1) + "/" + adt.getFullYear() + " " + pad(adt.getHours()) + ":" + pad(adt.getMinutes()) + ":" + pad(adt.getSeconds());
      var randSuffix = "";
      for (var k = 0; k < 4; k++) randSuffix += randChars.charAt(Math.floor(Math.random() * randChars.length));
      var idUnico = "#LNC-" + yy + mm + dd + "-" + randSuffix;

      db.avisos.unshift({
        id: idUnico,
        tipo: "presencial",
        iniciativaId: targetIni.id,
        iniciativa: targetIni.nome,
        pontos: pts,
        dados: { oque: dados.oque, quando: dados.quando },
        criadoEm: adt.getTime(),
        dataHora: lncDateStr,
        expiraEm: adt.getTime() + 48 * 3600000,
        status: "ativo"
      });
      saveDb();
      return mockApi("admin", {}, token);
    }

    if (acao === "publicarAcaoAvulsa") {
      var targetIni = db.inis.filter(function (x) { return x.id === dados.iniciativaId; })[0];
      var pts = (dados.modo === "quantidade") ? (parseInt(dados.quantidade, 10) * parseInt(dados.pontosUnitarios, 10)) : parseInt(dados.pontos, 10);
      var adt = new Date();
      var lncDateStr = pad(adt.getDate()) + "/" + pad(adt.getMonth() + 1) + "/" + adt.getFullYear() + " " + pad(adt.getHours()) + ":" + pad(adt.getMinutes()) + ":" + pad(adt.getSeconds());
      var randSuffix = "";
      for (var k = 0; k < 4; k++) randSuffix += randChars.charAt(Math.floor(Math.random() * randChars.length));
      var idUnico = "#LNC-" + yy + mm + dd + "-" + randSuffix;

      db.avisos.unshift({
        id: idUnico,
        tipo: "avulso",
        iniciativaId: targetIni.id,
        iniciativa: targetIni.nome,
        pontos: pts,
        dados: { titulo: dados.titulo, descricao: dados.descricao, quando: dados.quando },
        criadoEm: adt.getTime(),
        dataHora: lncDateStr,
        expiraEm: adt.getTime() + 48 * 3600000,
        status: "ativo"
      });
      saveDb();
      return mockApi("admin", {}, token);
    }

    if (acao === "criarAcaoCatalogo") {
      db.tarefasCatalogo.push({
        id: "custom_" + Date.now(),
        nome: dados.nome,
        pontos: parseInt(dados.pontos, 10) || 10,
        condicao: dados.condicao,
        personalizada: true
      });
      saveDb();
      return mockApi("admin", {}, token);
    }

    if (acao === "cancelarAviso") {
      var aItem = db.avisos.filter(function (x) { return x.id === dados.id; })[0];
      if (aItem) {
        aItem.status = "cancelado";
        saveDb();
      }
      return mockApi("admin", {}, token);
    }

    if (acao === "repararDatas") {
      return { reparadas: 0, mensagem: "Todas as datas da planilha já estão perfeitamente formatadas!" };
    }

    return { erro: "Ação não encontrada." };
  }

  function computeMockRanking(db) {
    var map = {};
    db.inis.forEach(function (u) {
      if (u.admin !== "sim") {
        map[u.id] = {
          id: u.id, nome: u.nome, tipo: u.tipo || "Empresa Júnior", representante: u.representante, cargo: u.cargo, redeSocial: u.redeSocial || "",
          pontos: 0, pontosValidados: 0, pontosPendentes: 0,
          breakdown: { redes: 0, inscricoes: 0, formulario: 0, presencial: 0, palestras: 0, feira: 0, challenges: 0, avulso: 0 }
        };
      }
    });

    db.entregas.forEach(function (e) {
      var rec = map[e.iniciativaId];
      if (!rec) return;
      if (e.status === "validada") {
        rec.pontos += e.pontos;
        rec.pontosValidados += e.pontos;
        rec.breakdown.redes += e.pontos;
      } else if (e.status === "pendente") {
        rec.pontos += e.pontos;
        rec.pontosPendentes += e.pontos;
        rec.breakdown.redes += e.pontos;
      }
    });

    db.avisos.forEach(function (a) {
      if (a.status === "cancelado") return;
      var rec = map[a.iniciativaId];
      if (!rec) return;
      var pts = a.pontos || 0;
      if (a.tipo === "inscricoes") {
        var atual = rec.breakdown.inscricoes;
        var somar = Math.min(pts, Math.max(0, 200 - atual));
        rec.breakdown.inscricoes += somar;
        rec.pontos += somar;
        rec.pontosValidados += somar;
      } else {
        if (rec.breakdown[a.tipo] !== undefined) rec.breakdown[a.tipo] += pts;
        else rec.breakdown.avulso += pts;
        rec.pontos += pts;
        rec.pontosValidados += pts;
      }
    });

    var arr = Object.keys(map).map(function (k) { return map[k]; });
    arr.sort(function (a, b) { return b.pontos - a.pontos; });
    return arr;
  }

  function getInitialMockDb() {
    return {
      inis: [
        { id: "ini_1", nome: "Engrenagem Jr.", tipo: "Empresa Júnior", representante: "Mariana Costa", cargo: "Presidente", redeSocial: "@engrenagemjr", admin: "", senha: "123" },
        { id: "ini_2", nome: "Fórmula Tesla UFMG", tipo: "Equipe de Competição", representante: "Lucas Ferreira", cargo: "Capitão", redeSocial: "@formulattesla", admin: "", senha: "123" },
        { id: "ini_3", nome: "Inova Consultoria Jr.", tipo: "Empresa Júnior", representante: "Beatriz Lima", cargo: "Diretora de Marketing", redeSocial: "@inovajr", admin: "", senha: "123" },
        { id: "ini_4", nome: "Baja UFMG", tipo: "Equipe de Competição", representante: "Gabriel Santos", cargo: "Piloto & Marketing", redeSocial: "@bajaufmg", admin: "", senha: "123" },
        { id: "ini_hub", nome: "UFMG Hub", tipo: "Organização", representante: "Gestão Hub", cargo: "Administrador", redeSocial: "@ufmghub", admin: "sim", senha: "admin" }
      ],
      tarefasCatalogo: [
        { id: "story_oficial", nome: "Compartilhamento de story oficial", pontos: 5, condicao: "Conforme limite do briefing" },
        { id: "story_autoral", nome: "Story autoral", pontos: 10, condicao: "Conteúdo próprio e aderente à missão" },
        { id: "feed_estatico", nome: "Publicação estática no feed", pontos: 30, condicao: "Peça própria ou adaptação autorizada" },
        { id: "carrossel", nome: "Carrossel autoral", pontos: 50, condicao: "Mínimo de 3 cards com conteúdo informativo" },
        { id: "reel", nome: "Reel ou vídeo autoral", pontos: 100, condicao: "Conteúdo original com mensagem clara" }
      ],
      briefings: [
        {
          id: "brf_1",
          titulo: "Briefing #01: Convocação Geral das EJs e Lançamento do Ecossistema MeC",
          fase: "Fase 1 · Aquecimento",
          periodo: "27/09 a 05/10",
          descricao: "Apresente para os seguidores e discentes da UFMG a participação da sua iniciativa no Mercado em Conexão 2026. Mostre a força da sua equipe e convide os estudantes a conhecerem a Arena.",
          diretrizes: "Peça autoral no Feed ou Carrossel. Use o logotipo oficial do MeC e do UFMG Hub nas artes. Evite artes com textos cortados.",
          linkDrive: "https://drive.google.com",
          hashtags: "@mercadoemconexao @ufmghub #ArenaMeC #MercadoEmConexao #UFMGInovadora",
          bonus: "+30 pts extras para a iniciativa com o Carrossel mais informativo",
          status: "ativo",
          criadoEm: Date.now() - 10000000
        },
        {
          id: "brf_2",
          titulo: "Briefing #02: Campanha de Inscrições para a Feira de Carreiras",
          fase: "Fase 2 · Inscrições",
          periodo: "06/10 a 16/10",
          descricao: "Foco total na conversão de estudantes para se inscreverem na Feira de Carreiras com o código de indicação da sua iniciativa. Cada inscrição válida vale 2 pontos (até 200 pts!).",
          diretrizes: "Story diário com o link da bio/inscrição + Reels com membros da equipe explicando as oportunidades de estágio e trainees.",
          linkDrive: "https://drive.google.com",
          hashtags: "@mercadoemconexao #FeiraMeC2026 #CarreirasUFMG #ArenaMeC",
          bonus: "+50 pts bônus para quem atingir o teto de 200 pts de inscrições",
          status: "em_breve",
          criadoEm: Date.now() - 5000000
        }
      ],
      cronograma: [
        { id: "cr_1", data: "05/10/2026", titulo: "Abertura Oficial das Inscrições da Feira", local: "Portal Mercado em Conexão", tipo: "Divulgação", pontos: "+2 pts por inscrição", descricao: "Início oficial do link de inscrições atribuídas para as iniciativas.", status: "andamento" },
        { id: "cr_2", data: "14/10/2026", titulo: "Blitz Universitária nos DAs e Centros Acadêmicos", local: "Praça de Serviços UFMG", tipo: "Presencial", pontos: "Até +40 pts", descricao: "Ações de abordagem, panfletagem e estandes volantes das equipes.", status: "proximo" },
        { id: "cr_3", data: "22/10/2026", titulo: "Feira de Carreiras Mercado em Conexão", local: "Escola de Engenharia UFMG", tipo: "Presencial", pontos: "+1 pt por visitante", descricao: "Grande feira presencial com estandes das empresas e das iniciativas.", status: "proximo" },
        { id: "cr_4", data: "23/10/2026", titulo: "Ciclo de Palestras & Hackathon Arena", local: "Auditório Principal", tipo: "Competição", pontos: "+1 pt por participante", descricao: "Palestras magnas com executivos e desafios de inovação.", status: "proximo" }
      ],
      entregas: [
        { id: "#ACT-260927-R812", iniciativaId: "ini_1", tarefaId: "reel", tarefaNome: "Reel ou vídeo autoral", pontos: 100, url: "https://instagram.com/p/reel_engrenagem", status: "validada", criadoEm: Date.now() - 36000000, dataHora: "26/09/2026 14:15:20", revisadoEm: Date.now() - 30000000, revisadoDataHora: "26/09/2026 16:30:10" },
        { id: "#ACT-260927-C491", iniciativaId: "ini_2", tarefaId: "carrossel", tarefaNome: "Carrossel autoral", pontos: 50, url: "https://instagram.com/p/carrossel_tesla", status: "validada", criadoEm: Date.now() - 28000000, dataHora: "26/09/2026 18:22:45", revisadoEm: Date.now() - 20000000, revisadoDataHora: "26/09/2026 20:00:00" },
        { id: "#ACT-260927-S770", iniciativaId: "ini_1", tarefaId: "story_oficial", tarefaNome: "Compartilhamento de story oficial", pontos: 5, url: "https://instagram.com/stories/engrenagem", status: "pendente", criadoEm: Date.now() - 1000000, dataHora: "27/09/2026 11:40:02" }
      ],
      avisos: [
        { id: "#LNC-260926-P012", tipo: "presencial", iniciativaId: "ini_1", iniciativa: "Engrenagem Jr.", pontos: 40, dados: { oque: "Estande de Prototipagem na Feira", quando: "26/09" }, criadoEm: Date.now() - 14000000, dataHora: "26/09/2026 15:00:00", expiraEm: Date.now() + 86400000, status: "ativo" },
        { id: "#LNC-260926-I489", tipo: "inscricoes", iniciativaId: "ini_2", iniciativa: "Fórmula Tesla UFMG", pontos: 60, dados: { quantidade: 30 }, criadoEm: Date.now() - 8000000, dataHora: "26/09/2026 19:30:00", expiraEm: Date.now() + 86400000, status: "ativo" }
      ],
      tarefaHub: {
        dados: {
          sobre: "Divulgação da Abertura da Arena e do Ecossistema de Inovação",
          periodo: "27/09 a 03/10",
          recomendacoes: "Use a hashtag #ArenaMEC e mostre os bastidores da sua equipe.",
          bonus: "+50 pontos extras para o post de maior engajamento da semana"
        },
        criadoEm: Date.now() - 10000000,
        expiraEm: Date.now() + 72 * 3600000
      }
    };
  }


  // ==================== EVENT LISTENERS DE USABILIDADE ====================
  // Alternar Visibilidade de Senha (Eye toggle)
  $$(".pwd-toggle-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var targetId = btn.dataset.pwdTarget;
      var inp = $("#" + targetId);
      if (!inp) return;
      var isPwd = inp.type === "password";
      inp.type = isPwd ? "text" : "password";
      var openIcon = btn.querySelector(".eye-open");
      var closedIcon = btn.querySelector(".eye-closed");
      if (openIcon && closedIcon) {
        openIcon.style.display = isPwd ? "none" : "block";
        closedIcon.style.display = isPwd ? "block" : "none";
      }
    });
  });

  // Acesso Rápido de Teste / Demonstração (1 Clique)
  if ($("#btn-demo-ej")) {
    $("#btn-demo-ej").addEventListener("click", function () {
      var nameInp = $("#login input[name='nome']");
      var pwdInp = $("#login input[name='senha']");
      if (nameInp) nameInp.value = "Engrenagem Jr.";
      if (pwdInp) pwdInp.value = "123";
      var subBtn = $("#login button[type='submit']");
      if (subBtn) subBtn.click();
    });
  }
  if ($("#btn-demo-admin")) {
    $("#btn-demo-admin").addEventListener("click", function () {
      var nameInp = $("#login input[name='nome']");
      var pwdInp = $("#login input[name='senha']");
      if (nameInp) nameInp.value = "UFMG Hub";
      if (pwdInp) pwdInp.value = "admin";
      var subBtn = $("#login button[type='submit']");
      if (subBtn) subBtn.click();
    });
  }

  // Alternar Tema (Claro / Escuro)
  if ($("#theme-toggle")) $("#theme-toggle").addEventListener("click", toggleTheme);
  if ($("#auth-theme-toggle")) $("#auth-theme-toggle").addEventListener("click", toggleTheme);

  // Modal Guia de Pontuação
  if ($("#btn-open-score-guide")) {
    $("#btn-open-score-guide").addEventListener("click", function () {
      $("#modal-score-guide").hidden = false;
    });
  }
  if ($("#guide-close-btn")) {
    $("#guide-close-btn").addEventListener("click", function () {
      $("#modal-score-guide").hidden = true;
    });
  }
  if ($("#guide-ok-btn")) {
    $("#guide-ok-btn").addEventListener("click", function () {
      $("#modal-score-guide").hidden = true;
    });
  }

  // Copiar Todas as Tags Oficiais
  if ($("#btn-copy-all-tags")) {
    $("#btn-copy-all-tags").addEventListener("click", function () {
      copyText("@ufmghub @mercadodeconexao #ArenaMEC #MEC2026 #HubUFMG");
    });
  }

  // FAQ Accordion
  $$(".faq-header").forEach(function (h) {
    h.addEventListener("click", function () {
      var item = h.closest(".faq-item");
      if (item) item.classList.toggle("open");
    });
  });

  // Filtros de Status das Minhas Entregas
  $$("#deliveries-filters [data-dfilter]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      $$("#deliveries-filters [data-dfilter]").forEach(function (b) { b.classList.remove("active"); });
      btn.classList.add("active");
      S.entregaFilter = btn.dataset.dfilter;
      renderEntregas();
    });
  });

  // Modal de Reenviar Entrega Recusada
  document.addEventListener("click", function (ev) {
    var b = ev.target.closest(".btn-reenviar");
    if (b) {
      S.reenviarId = b.dataset.reenviarId;
      $("#reenviar-task-nome").textContent = b.dataset.reenviarTarefa;
      $("#reenviar-task-pts").textContent = "+" + b.dataset.reenviarPts + " pts";
      $("#reenviar-motivo").textContent = b.dataset.reenviarMotivo;
      $("#reenviar-link-antigo").textContent = b.dataset.reenviarUrl;
      $("#reenviar-novo-url").value = "";
      $("#modal-reenviar-entrega").hidden = false;
    }
  });

  if ($("#reenviar-cancel-btn")) {
    $("#reenviar-cancel-btn").addEventListener("click", function () {
      $("#modal-reenviar-entrega").hidden = true;
      S.reenviarId = null;
    });
  }

  if ($("#reenviar-confirm-btn")) {
    $("#reenviar-confirm-btn").addEventListener("click", function () {
      var url = $("#reenviar-novo-url").value.trim();
      if (!url || !isUrl(url)) {
        toast("Informe uma URL pública válida (ex.: https://instagram.com/p/...)", true);
        return;
      }
      call("reenviarEntrega", { entregaId: S.reenviarId, novaUrl: url }).then(function (res) {
        $("#modal-reenviar-entrega").hidden = true;
        S.reenviarId = null;
        toast("Entrega reenviada para validação com sucesso!");
        loadHome().then(renderEntregas);
      }).catch(function (err) {
        toast(err.message || "Erro ao reenviar entrega", true);
      });
    });
  }

  // Modal Colar Múltiplos Links
  document.addEventListener("click", function (ev) {
    var b = ev.target.closest(".bulk-paste-btn");
    if (b) {
      S.bulkTid = b.dataset.bulkTid;
      $("#bulk-task-name").textContent = b.dataset.bulkName;
      $("#bulk-links-input").value = "";
      $("#modal-colar-links").hidden = false;
    }
  });

  if ($("#bulk-cancel-btn")) {
    $("#bulk-cancel-btn").addEventListener("click", function () {
      $("#modal-colar-links").hidden = true;
      S.bulkTid = null;
    });
  }

  if ($("#bulk-confirm-btn")) {
    $("#bulk-confirm-btn").addEventListener("click", function () {
      var text = $("#bulk-links-input").value.trim();
      if (!text) {
        $("#modal-colar-links").hidden = true;
        return;
      }
      var lines = text.split(/\\r?\\n/).map(function (l) { return l.trim(); }).filter(function (l) { return l.length > 0; });
      if (!lines.length) {
        $("#modal-colar-links").hidden = true;
        return;
      }
      var tid = S.bulkTid;
      S.counts[tid] = lines.length;
      S.urls[tid] = lines;
      $("#modal-colar-links").hidden = true;
      S.bulkTid = null;
      renderTarefas();
      updatePointsPreview();
      toast(lines.length + " link(s) inserido(s) com sucesso!");
    });
  }

  // Aprovação em Lote pelo Admin
  if ($("#adm-btn-aprovar-lote")) {
    $("#adm-btn-aprovar-lote").addEventListener("click", function () {
      if (!S.adm || !S.adm.entregas) return;
      var pending = S.adm.entregas.filter(function (e) { return e.status === "pendente"; });
      if (!pending.length) {
        toast("Não há entregas pendentes para aprovar.");
        return;
      }
      if (!confirm("Deseja aprovar todas as " + pending.length + " entregas pendentes em lote?")) return;
      var ids = pending.map(function (e) { return e.id; });
      call("validarEntregasLote", { ids: ids, status: "validada" }).then(function (res) {
        S.adm = res;
        renderAdmin();
        toast(ids.length + " entregas aprovadas com sucesso!");
      }).catch(function (err) {
        toast(err.message || "Erro ao aprovar em lote", true);
      });
    });
  }

  // ==================== INICIALIZAÇÃO ====================
  function boot() {
    initTheme();
    var tok = store("arena-token");
    if (tok) {
      start(tok);
    } else {
      authScreen("login");
    }
  }

  
  // Event listeners para Modal de Métricas
  document.addEventListener("click", function (evt) {
    var btn = evt.target.closest("[data-open-metrica]");
    if (!btn) return;
    var eid = btn.dataset.eid;
    var per = btn.dataset.per;
    var pts = btn.dataset.pts || "10";
    var tnome = btn.dataset.tnome || "Ação";
    var url = btn.dataset.url || "";

    var perRotulo = per === "24h" ? "24 Horas Stories" : (per === "sem1" ? "1ª Semana (+7 dias)" : (per === "sem2" ? "2ª Semana (+14 dias)" : "3ª Semana (+21 dias)"));
    $("#metric-entrega-id").value = eid;
    $("#metric-periodo").value = per;
    $("#m-metric-tag").textContent = "📊 Checkpoint: " + perRotulo + " (+" + pts + " pts)";
    $("#m-metric-title").textContent = "Registrar Métricas: " + perRotulo;
    $("#m-metric-desc").innerHTML = "Ação: <b>" + esc(tnome) + "</b> (" + esc(eid) + ")<br>" + (url ? '<a href="' + esc(url) + '" target="_blank" rel="noopener" style="font-size:.82rem;color:var(--primary-deep);">' + esc(url) + '</a>' : '');

    $("#metric-alcance").value = "";
    $("#metric-engajamento").value = "";
    $("#metric-comprovante").value = "";
    $("#metric-obs").value = "";
    $("#modal-registrar-metrica").hidden = false;
  });

  if ($("#m-metric-close")) {
    $("#m-metric-close").addEventListener("click", function () { $("#modal-registrar-metrica").hidden = true; });
  }
  if ($("#m-metric-cancel")) {
    $("#m-metric-cancel").addEventListener("click", function () { $("#modal-registrar-metrica").hidden = true; });
  }

  if ($("#form-registrar-metrica")) {
    $("#form-registrar-metrica").addEventListener("submit", function (e) {
      e.preventDefault();
      var eid = $("#metric-entrega-id").value;
      var per = $("#metric-periodo").value;
      var alcance = $("#metric-alcance").value;
      var engajamento = $("#metric-engajamento").value;
      var comprovanteUrl = $("#metric-comprovante").value.trim();
      var observacoes = $("#metric-obs").value.trim();

      var submitBtn = $("#m-metric-submit");
      submitBtn.disabled = true;
      submitBtn.textContent = "Enviando dados...";

      call("registrarMetricaEntrega", {
        entregaId: eid,
        periodo: per,
        alcance: alcance,
        engajamento: engajamento,
        comprovanteUrl: comprovanteUrl,
        observacoes: observacoes
      }).then(function (res) {
        $("#modal-registrar-metrica").hidden = true;
        submitBtn.disabled = false;
        submitBtn.textContent = "🚀 Enviar Métricas para Validação";
        S.data = res;
        renderAll();
        var rotulo = res.metricaEnviada ? res.metricaEnviada.periodo : "Métrica";
        var pts = res.metricaEnviada ? res.metricaEnviada.pontos : 10;
        toast("🎉 Métricas de " + rotulo + " enviadas com sucesso! (+" + pts + " pts em análise)");
      }).catch(function (err) {
        toast(err.message, "erro");
        submitBtn.disabled = false;
        submitBtn.textContent = "🚀 Enviar Métricas para Validação";
      });
    });
  }

  // Aprovação em lote de métricas pelo Admin
  if ($("#adm-btn-aprovar-metricas-lote")) {
    $("#adm-btn-aprovar-metricas-lote").addEventListener("click", function () {
      var btn = $("#adm-btn-aprovar-metricas-lote");
      var a = S.adm;
      var pendentes = a && a.metricas ? a.metricas.filter(function (m) { return m.status === "pendente"; }) : [];
      if (!pendentes.length) {
        toast("Não há métricas pendentes para aprovação no momento.");
        return;
      }
      if (!confirm("Deseja homologar e aprovar todas as " + pendentes.length + " métricas pendentes de uma só vez?")) return;
      btn.disabled = true;
      call("validarMetricasLote", { status: "validada" }).then(function (res) {
        S.adm = res;
        renderAdmin();
        toast("Todas as " + pendentes.length + " métricas foram aprovadas com sucesso!");
        btn.disabled = false;
      }).catch(function (err) {
        toast(err.message, "erro");
        btn.disabled = false;
      });
    });
  }

  if ($("#adm-met-filter-status")) $("#adm-met-filter-status").addEventListener("change", renderAdminMetricas);
  if ($("#adm-met-filter-ini")) $("#adm-met-filter-ini").addEventListener("change", renderAdminMetricas);
  if ($("#adm-search-met")) $("#adm-search-met").addEventListener("input", renderAdminMetricas);

  boot();
})();
</script>
</body>
</html>
"""

# Injeta os assets base64
rendered = html_template.replace("@@ICON_MEC@@", icon_mec_b64)
rendered = rendered.replace("@@LOGO_MEC@@", logo_mec_b64)
rendered = rendered.replace("@@HUB_BRANCO@@", hub_branco_b64)
rendered = rendered.replace("@@HUB_COLORIDO@@", hub_colorido_b64)

with open('Index-codigo-novo.txt', 'w', encoding='utf-8') as f:
    f.write(rendered)

with open('Index.html', 'w', encoding='utf-8') as f:
    f.write(rendered)

print('Index-codigo-novo.txt and Index.html updated successfully with Briefings & Cronograma!')
print('File size:', len(rendered), 'bytes')
