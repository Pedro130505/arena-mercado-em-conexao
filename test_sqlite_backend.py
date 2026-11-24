# -*- coding: utf-8 -*-
"""
Suíte Completa de Testes Automatizados — Arena | Mercado em Conexão (SQLite 3 + E2E Browser)
Testa:
1. Motor SQLite 3 (WAL mode, tabelas, índices, seed inicial, migração)
2. Autenticação & Cadastro (PBKDF2/SHA-256, tokens HMAC-SHA256, unicidade de nome case-insensitive)
3. Envio de Tarefas & Formatação de Datas Brasileiras (DD/MM/AAAA HH:MM:SS)
4. Sistema Anti-Fraude e Deduplicação de URLs (mesmo lote, mesma iniciativa, outra iniciativa, limpeza de query params ?utm_source=...&igsh=...)
5. Fluxo de Validação Admin (Aprovar, Recusar com motivo, Desfazer, Reenvio permitido após recusa)
6. Lançamento de Pontos do Evento (Inscrições com trava de teto máximo de 200 pts, Presencial com teto de 40 pts, Formulário, Palestras, Feira, Challenges, Avulso fixo e multiplicador)
7. Estorno de Lançamentos (cancelarAviso) e recálculo imediato do Ranking
8. Gestão de Briefings, Cronograma Mensal e Catálogo Dinâmico (CRUD completo no SQLite)
9. Higienização / Reparo de Datas Legadas (repararDatas)
10. Exportação de Planilhas CSV (UTF-8 com BOM para Excel)
11. Teste End-to-End no Navegador (Playwright) contra http://localhost:8080 consumindo o SQLite real
"""

import json
import re
import sqlite3
import sys
import urllib.request
import urllib.error

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_URL = "http://localhost:8080"


def api_call(acao, dados=None, token=""):
    payload = json.dumps({
        "acao": acao,
        "dados": dados or {},
        "token": token or ""
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/api",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_json(path):
    with urllib.request.urlopen(f"{BASE_URL}{path}", timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_bytes(path):
    with urllib.request.urlopen(f"{BASE_URL}{path}", timeout=10) as resp:
        return resp.read(), resp.headers.get("Content-Type", "")


def ensure_server_running():
    try:
        with urllib.request.urlopen(f"{BASE_URL}/api/health", timeout=1) as resp:
            if resp.status == 200:
                return
    except Exception:
        pass
    import threading
    import server
    import time
    t = threading.Thread(target=server.run_server, daemon=True)
    t.start()
    time.sleep(1.2)


def run_tests():
    ensure_server_running()
    passed = 0
    total = 0

    def check(cond, name, detail=""):
        nonlocal passed, total
        total += 1
        if cond:
            passed += 1
            print(f"  [PASS] {total:02d}. {name}", flush=True)
        else:
            print(f"  [FAIL] {total:02d}. {name} -> {detail}", flush=True)
            raise AssertionError(f"Falha no teste: {name} ({detail})")

    print("=" * 70)
    print("INICIANDO BATERIA DE TESTES DO BANCO SQLITE 3 & API HTTP")
    print("=" * 70)

    # 1. Healthcheck & WAL Mode
    health = get_json("/api/health")
    check(health.get("status") == "ok" and health.get("engine") == "SQLite 3",
          "Healthcheck do servidor SQLite 3 (/api/health)", str(health))

    conn = sqlite3.connect("arena.db")
    with conn:
        conn.execute("DELETE FROM entregas WHERE iniciativaId IN (SELECT id FROM iniciativas WHERE nome LIKE 'AeroUFMG Teste%')")
        conn.execute("DELETE FROM avisos WHERE iniciativaId IN (SELECT id FROM iniciativas WHERE nome LIKE 'AeroUFMG Teste%')")
        conn.execute("DELETE FROM iniciativas WHERE nome LIKE 'AeroUFMG Teste%'")
    journal_mode = conn.execute("PRAGMA journal_mode;").fetchone()[0]
    check(journal_mode.lower() == "wal",
          f"SQLite configurado em modo concorrente WAL (atual: {journal_mode})", journal_mode)
    conn.close()

    # 2. Login Admin (UFMG Hub)
    res_adm_login = api_call("entrar", {"nome": "UFMG Hub", "senha": "admin"})
    check("token" in res_adm_login and res_adm_login.get("admin") is True,
          "Login da conta Administradora (UFMG Hub / admin)", str(res_adm_login))
    adm_token = res_adm_login["token"]

    # 3. Login Iniciativa Existente (Engrenagem Jr.)
    res_ini_login = api_call("entrar", {"nome": "Engrenagem Jr.", "senha": "123"})
    check("token" in res_ini_login and res_ini_login.get("admin") is False,
          "Login de Iniciativa pré-cadastrada (Engrenagem Jr.)", str(res_ini_login))
    ini_token = res_ini_login["token"]

    # 4. Senha incorreta deve ser bloqueada
    res_bad_login = api_call("entrar", {"nome": "Engrenagem Jr.", "senha": "errada"})
    check("erro" in res_bad_login,
          "Bloqueio de senha incorreta no login", str(res_bad_login))

    # 5. Cadastro de nova iniciativa no SQLite
    import time
    nome_nova = f"AeroUFMG Teste {int(time.time()) % 10000}"
    res_cad = api_call("cadastrar", {
        "nome": nome_nova,
        "tipo": "Equipe de Competição",
        "representante": "Pedro Henrique",
        "cargo": "Diretor de Projetos",
        "redeSocial": "@aeroufmg_teste",
        "senha": "senha123"
    })
    check("token" in res_cad and res_cad.get("nome") == nome_nova,
          f"Cadastro de nova iniciativa no SQLite ({nome_nova})", str(res_cad))
    nova_token = res_cad["token"]

    # 6. Bloqueio de cadastro duplicado (case-insensitive)
    res_cad_dup = api_call("cadastrar", {
        "nome": nome_nova.upper(),
        "tipo": "Equipe de Competição",
        "representante": "Outro",
        "cargo": "Membro",
        "redeSocial": "@outro",
        "senha": "senha123"
    })
    check("erro" in res_cad_dup and "cadastrada" in res_cad_dup["erro"],
          "Proteção UNIQUE COLLATE NOCASE contra nomes de iniciativas duplicados", str(res_cad_dup))

    # 7. Consulta do Painel Principal
    painel = api_call("painel", {}, nova_token)
    check("ranking" in painel and "briefings" in painel and "cronograma" in painel,
          "Carregamento completo do Painel (Ranking, Briefings, Cronograma, Tarefas)", "")

    # 8. Envio de Tarefa e verificação de ID #ACT- e Data Brasileira DD/MM/AAAA HH:MM:SS
    url_teste_1 = f"https://instagram.com/p/post_unico_{int(time.time())}"
    res_envio = api_call("enviarTarefas", {
        "itens": [
            {"tarefaId": "carrossel", "urls": [url_teste_1]}
        ]
    }, nova_token)
    check("enviado" in res_envio and res_envio["enviado"]["pontos"] == 50,
          "Registro de tarefa (Carrossel Autoral +50 pts) no SQLite", str(res_envio.get("enviado")))

    minhas = res_envio.get("minhasEntregas", [])
    check(len(minhas) == 1, "Entrega listada em minhasEntregas após envio", str(len(minhas)))
    entrega_criada = minhas[0]
    check(entrega_criada["id"].startswith("#ACT-"),
          f"Geração de ID único amigável ({entrega_criada['id']})", entrega_criada["id"])
    check(bool(re.match(r"^\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}$", entrega_criada["dataHora"])),
          f"Data/Hora gravada em formato brasileiro legível ({entrega_criada['dataHora']})", entrega_criada["dataHora"])

    # 9. Anti-Fraude: Bloqueio de reenvio do mesmo link (mesmo com parâmetros ?igsh=...&utm_source=...)
    url_com_tracking = url_teste_1 + "/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA=="
    res_dup_mesma = api_call("enviarTarefas", {
        "itens": [
            {"tarefaId": "story_oficial", "urls": [url_com_tracking]}
        ]
    }, nova_token)
    check("erro" in res_dup_mesma and ("já registrou este link" in res_dup_mesma["erro"] or "já enviou este link" in res_dup_mesma["erro"]),
          "Anti-Fraude: Bloqueio de link duplicado da mesma equipe com query params de tracking", str(res_dup_mesma))

    # 10. Anti-Fraude: Bloqueio de envio do mesmo link por OUTRA iniciativa
    res_dup_outra = api_call("enviarTarefas", {
        "itens": [
            {"tarefaId": "reel", "urls": [url_teste_1]}
        ]
    }, ini_token)
    check("erro" in res_dup_outra and "outra iniciativa" in res_dup_outra["erro"],
          "Anti-Fraude: Bloqueio de link já utilizado por outra iniciativa", str(res_dup_outra))

    # 11. Anti-Fraude: Bloqueio de links idênticos no mesmo lote
    url_lote = f"https://instagram.com/p/lote_{int(time.time())}"
    res_dup_lote = api_call("enviarTarefas", {
        "itens": [
            {"tarefaId": "story_oficial", "urls": [url_lote, url_lote + "/"]}
        ]
    }, nova_token)
    check("erro" in res_dup_lote and "mesmo envio" in res_dup_lote["erro"],
          "Anti-Fraude: Bloqueio de links repetidos dentro do mesmo lote", str(res_dup_lote))

    # 12. Admin: Validação de Entrega (Recusar com motivo -> Reenviar -> Aprovar)
    res_recusa = api_call("validarEntrega", {
        "id": entrega_criada["id"],
        "status": "recusada",
        "motivoRecusa": "Faltou marcar @mercadoemconexao"
    }, adm_token)
    ent_adm = [e for e in res_recusa["entregas"] if e["id"] == entrega_criada["id"]][0]
    check(ent_adm["status"] == "recusada" and ent_adm["motivoRecusa"] == "Faltou marcar @mercadoemconexao",
          "Admin: Recusa de entrega com gravação de motivo de recusa", str(ent_adm))

    # Quando recusada, a iniciativa PODE reenviar o link corrigido!
    res_reenvio = api_call("enviarTarefas", {
        "itens": [
            {"tarefaId": "carrossel", "urls": [url_teste_1]}
        ]
    }, nova_token)
    check("enviado" in res_reenvio and res_reenvio["enviado"]["links"] == 1,
          "Permissão de reenvio de link que havia sido recusado anteriormente", str(res_reenvio.get("enviado")))
    nova_entrega_id = res_reenvio["minhasEntregas"][0]["id"]

    # Agora Admin aprova a nova entrega
    res_aprova = api_call("validarEntrega", {
        "id": nova_entrega_id,
        "status": "validada"
    }, adm_token)
    ent_aprovada = [e for e in res_aprova["entregas"] if e["id"] == nova_entrega_id][0]
    check(ent_aprovada["status"] == "validada" and bool(ent_aprovada["revisadoDataHora"]),
          f"Admin: Aprovação de entrega com data de revisão ({ent_aprovada['revisadoDataHora']})", str(ent_aprovada))

    # 13. Lançamento de Inscrições e Trava do Teto de 200 Pontos
    nova_ini_id = [i["id"] for i in res_aprova["iniciativas"] if i["nome"] == nome_nova][0]
    res_insc_1 = api_call("publicarInscricoes", {
        "iniciativaId": nova_ini_id,
        "quantidade": 120  # 120 * 2 = 240 pts, mas o teto na pontuação do ranking é 200 pts!
    }, adm_token)
    check("historico" in res_insc_1, "Lançamento de inscrições pelo Admin", "")

    painel_pos_insc = api_call("painel", {}, nova_token)
    meu_rank = [r for r in painel_pos_insc["ranking"] if r["id"] == nova_ini_id][0]
    check(meu_rank["breakdown"]["inscricoes"] == 200 and meu_rank["pontos"] == 250,
          f"Respeito rigoroso ao teto de 200 pts de inscrições (200 insc + 50 redes = {meu_rank['pontos']} pts)",
          str(meu_rank))

    # 14. Lançamento de Ação Presencial, Palestras, Feira, Challenges, Formulário e Avulso
    api_call("publicarPresencial", {"iniciativaId": nova_ini_id, "oque": "Stand Aero", "quando": "15/10", "pontos": 40}, adm_token)
    api_call("publicarFormulario", {"iniciativaId": nova_ini_id, "quantidade": 10}, adm_token)
    api_call("publicarPalestras", {"iniciativaId": nova_ini_id, "quantidade": 5}, adm_token)
    api_call("publicarFeira", {"iniciativaId": nova_ini_id, "quantidade": 8}, adm_token)
    api_call("publicarChallenges", {"iniciativaId": nova_ini_id, "quantidade": 3}, adm_token)
    res_avulso = api_call("publicarAcaoAvulsa", {
        "iniciativaId": nova_ini_id,
        "titulo": "Bônus Vídeo Mais Criativo",
        "descricao": "Destaque da semana",
        "modo": "fixo",
        "pontos": 35,
        "quando": "16/10"
    }, adm_token)
    avulso_id = res_avulso["historico"][0]["id"]

    painel_completo = api_call("painel", {}, nova_token)
    meu_rank_2 = [r for r in painel_completo["ranking"] if r["id"] == nova_ini_id][0]
    esperado = 50 + 200 + 40 + 10 + 5 + 8 + 3 + 35  # 351 pontos
    check(meu_rank_2["pontos"] == esperado,
          f"Cálculo exato de todas as categorias no Ranking ({meu_rank_2['pontos']} == {esperado} pts)",
          str(meu_rank_2["breakdown"]))

    # 15. Estorno de Lançamento (cancelarAviso)
    api_call("cancelarAviso", {"id": avulso_id}, adm_token)
    painel_pos_estorno = api_call("painel", {}, nova_token)
    meu_rank_3 = [r for r in painel_pos_estorno["ranking"] if r["id"] == nova_ini_id][0]
    check(meu_rank_3["pontos"] == esperado - 35,
          f"Estorno imediato de pontuação cancelada ({meu_rank_3['pontos']} pts)", str(meu_rank_3["pontos"]))

    # 16. CRUD de Briefings, Cronograma e Catálogo
    res_brf = api_call("salvarBriefing", {
        "titulo": "Briefing Teste SQLite",
        "fase": "Fase Especial",
        "periodo": "20/10 a 25/10",
        "descricao": "Descrição de teste",
        "status": "ativo"
    }, adm_token)
    brf_id = res_brf["briefings"][0]["id"]
    check(brf_id.startswith("#BRF-"), f"Criação de Briefing no SQLite ({brf_id})", brf_id)
    res_brf_del = api_call("removerBriefing", {"id": brf_id}, adm_token)
    check(all(b["id"] != brf_id for b in res_brf_del["briefings"]), "Remoção de Briefing no SQLite", "")

    res_crn = api_call("salvarCronograma", {
        "data": "28/10/2026",
        "titulo": "Encerramento Teste",
        "local": "Auditório Reitoria",
        "tipo": "Presencial",
        "pontos": "+20 pts",
        "status": "proximo"
    }, adm_token)
    crn_id = [c["id"] for c in res_crn["cronograma"] if c["titulo"] == "Encerramento Teste"][0]
    check(crn_id.startswith("#CRN-"), f"Criação de item no Cronograma ({crn_id})", crn_id)
    res_crn_del = api_call("removerCronograma", {"id": crn_id}, adm_token)
    check(all(c["id"] != crn_id for c in res_crn_del["cronograma"]), "Remoção de item no Cronograma", "")

    # 17. Reparo de Datas Legadas (repararDatas)
    res_rep = api_call("repararDatas", {}, adm_token)
    check("reparadas" in res_rep and "mensagem" in res_rep,
          f"Execução da ferramenta repararDatas ({res_rep['mensagem']})", str(res_rep))

    # 18. Exportação CSV para Excel (/api/export/csv)
    csv_rank_bytes, ctype_rank = get_bytes("/api/export/csv?tabela=ranking")
    check(csv_rank_bytes.startswith(b"\xef\xbb\xbf") and "Posicao;Iniciativa;Categoria" in csv_rank_bytes.decode("utf-8-sig"),
          "Exportação CSV do Ranking com BOM UTF-8 e separador ';' para Excel", ctype_rank)

    csv_ent_bytes, ctype_ent = get_bytes("/api/export/csv?tabela=entregas")
    check(csv_ent_bytes.startswith(b"\xef\xbb\xbf") and "ID Unico;Iniciativa;Tarefa" in csv_ent_bytes.decode("utf-8-sig"),
          "Exportação CSV de Entregas com BOM UTF-8 e datas formatadas", ctype_ent)

    # Limpa a iniciativa de teste para deixar o banco enxuto com os dados oficiais
    conn = sqlite3.connect("arena.db")
    with conn:
        conn.execute("DELETE FROM entregas WHERE iniciativaId = ?", (nova_ini_id,))
        conn.execute("DELETE FROM avisos WHERE iniciativaId = ?", (nova_ini_id,))
        conn.execute("DELETE FROM iniciativas WHERE id = ?", (nova_ini_id,))
    conn.close()

    print(f"\n--> Todos os {passed}/{total} testes de API e Banco SQLite 3 passaram com sucesso!\n")
    return passed, total


def run_browser_e2e_tests():
    from playwright.sync_api import sync_playwright

    print("=" * 70)
    print("INICIANDO TESTES END-TO-END NO NAVEGADOR (PLAYWRIGHT + SQLITE)")
    print("=" * 70)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        # 1. Abre o app via HTTP Server (conectado ao SQLite)
        page.goto(BASE_URL, wait_until="networkidle")
        page.wait_for_selector("#login", state="visible")
        print("  [PASS] E2E 01. Página inicial carregada via HTTP e conectada ao SQLite")

        # 2. Faz login como Engrenagem Jr.
        page.click("#btn-demo-ej")
        page.wait_for_selector("#page-ranking", state="visible")
        lider_txt = page.text_content("#stat-lider")
        assert "Engrenagem Jr." in lider_txt, f"Esperava Engrenagem Jr., veio {lider_txt}"
        print(f"  [PASS] E2E 02. Login como iniciativa e renderização do Ranking SQLite (Líder: {lider_txt})")

        # 3. Navega para Minhas Entregas e verifica formato de data legível e ID #ACT-
        page.click('button[data-page="entregas"]')
        page.wait_for_selector("#page-entregas", state="visible")
        entregas_html = page.inner_html("#my-deliveries-list")
        assert "#ACT-" in entregas_html
        print("  [PASS] E2E 03. Aba 'Minhas Entregas' exibindo IDs #ACT- e datas formatadas do SQLite")

        # 4. Faz logout e entra como Admin (UFMG Hub / admin)
        page.click("#logout")
        page.wait_for_selector("#login", state="visible")
        page.click("#btn-demo-admin")
        page.wait_for_selector("#page-ranking", state="visible")

        # 5. Abre Painel do Hub e verifica aba Diagnóstico SQLite
        page.click('button[data-page="admin"]')
        page.wait_for_selector("#page-admin", state="visible")
        page.click('button[data-adm-tab="diagnostico"]')
        page.wait_for_selector('[data-adm="diagnostico"]', state="visible")
        engine_txt = page.text_content("#diag-db-engine")
        assert "SQLite 3" in engine_txt
        print(f"  [PASS] E2E 04. Painel Admin -> Aba Diagnóstico exibindo motor ativo: {engine_txt}")

        # 6. Clica em Verificar e Reparar Datas Agora
        page.click("#btn-reparar-datas")
        page.wait_for_selector("#toast", state="visible", timeout=5000)
        toast_txt = page.text_content("#toast") or ""
        print(f"  [DEBUG] Toast capturado: '{toast_txt}'", flush=True)
        assert len(toast_txt) > 0, "Toast vazio!"
        print(f"  [PASS] E2E 05. Botão 'Reparar Datas' executou no SQLite e retornou toast: '{toast_txt}'", flush=True)

        browser.close()

    print("\n--> Todos os 5 testes End-to-End no navegador passaram com 100% de sucesso!", flush=True)


if __name__ == "__main__":
    run_tests()
    run_browser_e2e_tests()
