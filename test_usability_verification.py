# -*- coding: utf-8 -*-
"""
Bateria Completa de Validação de Usabilidade, Backend SQLite 3 e Playwright E2E
Arena | Mercado em Conexão (UFMG Hub)
"""
import json
import os
import re
import sqlite3
import sys
import urllib.request
import urllib.error
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_URL = "http://localhost:8080"
SCREENSHOTS_DIR = os.path.join(
    r"C:\Users\brand\.gemini\antigravity\brain\6df93881-4cb2-4234-9466-24b587e1fb8a",
    "screenshots_v2"
)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)


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


def run_all_verifications():
    passed = 0
    total = 0

    def check(cond, name, detail=""):
        nonlocal passed, total
        total += 1
        if cond:
            passed += 1
            print(f"  [PASS] {total:02d}. {name}")
        else:
            print(f"  [FAIL] {total:02d}. {name} -> {detail}")
            raise AssertionError(f"Falha na verificação: {name} ({detail})")

    print("=" * 75)
    print("PARTE 1: TESTES DE NOVOS ENDPOINTS SQLITE (reenviarEntrega & validarEntregasLote)")
    print("=" * 75)

    # 1. Login Admin e Iniciativa
    adm_login = api_call("entrar", {"nome": "UFMG Hub", "senha": "admin"})
    check("token" in adm_login and adm_login.get("admin") is True, "Login Admin UFMG Hub")
    adm_token = adm_login["token"]

    ini_login = api_call("entrar", {"nome": "Engrenagem Jr.", "senha": "123"})
    check("token" in ini_login, "Login Iniciativa Engrenagem Jr.")
    ini_token = ini_login["token"]

    # 2. Criar entrega para teste de recusa e reenvio
    import time
    test_ts = int(time.time())
    url_recusa = f"https://instagram.com/p/test_recusa_{test_ts}"
    res_envio = api_call("enviarTarefas", {
        "itens": [{"tarefaId": "carrossel", "urls": [url_recusa]}]
    }, ini_token)
    check("enviado" in res_envio, "Envio de tarefa para teste de reenvio")
    entrega_id = res_envio["minhasEntregas"][0]["id"]

    # 3. Admin recusa a entrega
    res_rec = api_call("validarEntrega", {
        "id": entrega_id,
        "status": "recusada",
        "motivoRecusa": "Conta privada (não foi possível visualizar a postagem)"
    }, adm_token)
    check("entregas" in res_rec, "Admin recusa entrega com motivo registrado")

    # 4. Iniciativa corrige e reenvia através do novo endpoint reenviarEntrega
    url_corrigida = f"https://instagram.com/p/test_corrigida_{test_ts}"
    res_reenvio = api_call("reenviarEntrega", {
        "entregaId": entrega_id,
        "novaUrl": url_corrigida
    }, ini_token)
    check("minhasEntregas" in res_reenvio,
          "Endpoint reenviarEntrega: painel atualizado com sucesso", str(res_reenvio.get("enviado")))
    entrega_reenviada = [e for e in res_reenvio["minhasEntregas"] if e["id"] == entrega_id][0]
    check(entrega_reenviada["status"] == "pendente" and entrega_reenviada["url"] == url_corrigida,
          "Endpoint reenviarEntrega: status 'pendente' e novaUrl gravada no SQLite")

    # 5. Criar 3 entregas e testar aprovação em lote (validarEntregasLote)
    urls_lote = [
        f"https://instagram.com/p/lote_a_{test_ts}",
        f"https://instagram.com/p/lote_b_{test_ts}",
        f"https://instagram.com/p/lote_c_{test_ts}"
    ]
    res_lote_envio = api_call("enviarTarefas", {
        "itens": [{"tarefaId": "story_oficial", "urls": urls_lote}]
    }, ini_token)
    check("enviado" in res_lote_envio, "Envio de 3 stories para teste em lote")
    ids_lote = [e["id"] for e in res_lote_envio["minhasEntregas"] if e["url"] in urls_lote]
    check(len(ids_lote) == 3, f"3 IDs de entrega gerados ({ids_lote})")

    # 6. Admin aprova as 3 entregas de uma só vez (validarEntregasLote)
    res_lote_val = api_call("validarEntregasLote", {
        "ids": ids_lote,
        "status": "validada"
    }, adm_token)
    check("entregas" in res_lote_val,
          "Endpoint validarEntregasLote: retorno do painel admin com sucesso")
    aprovadas = [e for e in res_lote_val["entregas"] if e["id"] in ids_lote and e["status"] == "validada"]
    check(len(aprovadas) == 3, f"3 entregas aprovadas de uma só vez pelo lote! ({len(aprovadas)})")

    print("\n" + "=" * 75)
    print("PARTE 2: TESTES END-TO-END DE USABILIDADE & INTERFACE NO NAVEGADOR")
    print("=" * 75)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # Contexto 1: Desktop HD (1440 x 900)
        ctx = browser.new_context(viewport={"width": 1440, "height": 900}, permissions=["clipboard-read", "clipboard-write"])
        page = ctx.new_page()

        # 7. Acesso à página inicial
        page.goto(BASE_URL, wait_until="networkidle")
        page.wait_for_selector("#login", state="visible")
        check(page.is_visible("#login"), "Tela de Login carregada e visível")
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "01_tela_login.png"), full_page=True)

        # 8. Teste de Alternância de Tema (Dark / Light) na tela de Auth
        check(page.is_visible("#auth-theme-toggle"), "Botão de tema visível na tela de autenticação")
        page.click("#auth-theme-toggle")
        page.wait_for_timeout(300)
        theme_attr = page.evaluate("() => document.documentElement.getAttribute('data-theme')")
        check(theme_attr == "dark", "Tema alterado para Dark Mode com sucesso (data-theme='dark')")
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "02_auth_dark_mode.png"), full_page=True)
        # Volta para light mode
        page.click("#auth-theme-toggle")
        page.wait_for_timeout(300)

        # 9. Teste do Botão Ver / Ocultar Senha (Eye toggle)
        eye_btn = page.locator('.pwd-toggle-btn[data-pwd-target="login-senha-input"]')
        check(eye_btn.is_visible(), "Botão de alternar visibilidade de senha (Eye toggle) visível")
        page.fill("#login-senha-input", "testeSenha123")
        type_before = page.get_attribute("#login-senha-input", "type")
        check(type_before == "password", "Campo de senha inicia com type='password'")
        eye_btn.click()
        type_after = page.get_attribute("#login-senha-input", "type")
        check(type_after == "text", "Após clique no olho, campo muda para type='text'")
        eye_btn.click()
        check(page.get_attribute("#login-senha-input", "type") == "password", "Segundo clique restaura type='password'")

        # 10. Teste do Acesso Rápido de Teste (1 Clique) - Iniciativa Engrenagem Jr.
        check(page.is_visible("#btn-demo-ej"), "Botão de Acesso Rápido 'Engrenagem Jr.' visível")
        page.click("#btn-demo-ej")
        page.wait_for_selector("#page-ranking", state="visible", timeout=10000)
        check(page.is_visible("#page-ranking"), "Login com 1 clique efetuado! Tela do Ranking carregada")
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "03_ranking_desktop_logado.png"), full_page=True)

        # 11. Teste do Modal 'Como Funciona a Pontuação?'
        check(page.is_visible("#btn-open-score-guide"), "Botão 'Como Funciona a Pontuação?' visível no cabeçalho")
        page.click("#btn-open-score-guide")
        page.wait_for_selector("#modal-score-guide", state="visible")
        check(page.is_visible("#modal-score-guide"), "Modal explicativo de pontuação aberto")
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "04_modal_como_funciona_pontuacao.png"))
        page.click("#guide-ok-btn")
        page.wait_for_selector("#modal-score-guide", state="hidden")
        check(not page.is_visible("#modal-score-guide"), "Modal fechado com sucesso pelo botão de confirmação")

        # 12. Teste dos Contadores de Categorias nas Pílulas do Ranking
        count_todos = page.text_content("#count-todos")
        count_ej = page.text_content("#count-ej")
        count_comp = page.text_content("#count-comp")
        check(int(count_todos) > 0 and int(count_ej) > 0,
              f"Pílulas com contadores dinâmicos calculados (Todas: {count_todos}, EJs: {count_ej}, Competição: {count_comp})")

        # 13. Teste do Banner 'Você está aqui'
        check(page.is_visible("#my-rank-banner"), "Banner motivacional 'Você está aqui' visível para a iniciativa logada")
        diff_text = page.text_content("#my-rank-diff")
        check(len(diff_text) > 5, f"Texto de motivação/gap exibido: '{diff_text}'")

        # 14. Navegação para 'Registrar Ações' e Verificação de Usabilidade
        page.click('button[data-page="tarefas"]')
        page.wait_for_selector("#page-tarefas", state="visible")
        check(page.is_visible("#page-tarefas"), "Aba 'Registrar Ações' carregada")

        # Aumentar quantidade da primeira tarefa para abrir input de link
        page.click('#task-picker li:first-child button[data-act="inc"]')
        page.wait_for_selector('#task-picker input[type="url"]', state="visible")
        input_url = page.locator('#task-picker input[type="url"]').first

        # Digitar link do Instagram e verificar Platform Badge
        input_url.fill("https://www.instagram.com/p/reel_teste_123")
        page.wait_for_timeout(300)
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "05_registrar_acoes_platform_badge.png"))
        # Testar modal Colar Vários Links
        bulk_btn = page.locator('.bulk-paste-btn').first
        check(bulk_btn.is_visible(), "Botão 'Colar Vários Links' visível no card da tarefa")
        bulk_btn.click()
        page.wait_for_selector("#modal-colar-links", state="visible")
        check(page.is_visible("#modal-colar-links"), "Modal 'Colar Múltiplos Links' aberto")
        page.fill("#bulk-links-input", "https://instagram.com/p/link1\nhttps://linkedin.com/posts/link2\nhttps://youtube.com/watch?v=link3")
        page.click("#bulk-confirm-btn")
        page.wait_for_selector("#modal-colar-links", state="hidden")
        check(not page.is_visible("#modal-colar-links"), "Modal Colar Vários inseriu links e fechou com sucesso")
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "06_tarefas_multiplos_links_inseridos.png"))

        # 15. Navegação para 'Minhas Entregas' e Filtros de Status
        page.click('button[data-page="entregas"]')
        page.wait_for_selector("#page-entregas", state="visible")
        check(page.is_visible("#deliveries-filters"), "Barra de filtros de status visível em Minhas Entregas")
        dcount_todas = page.text_content("#dcount-todas")
        check(int(dcount_todas) > 0, f"Contador de entregas total exibido: {dcount_todas}")

        # Clicar no filtro de Aprovadas
        page.click('button[data-dfilter="validada"]')
        page.wait_for_timeout(300)
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "07_minhas_entregas_aprovadas.png"))

        # Clicar no filtro de Recusadas (se houver, verificar botão Corrigir e Reenviar)
        page.click('button[data-dfilter="recusada"]')
        page.wait_for_timeout(300)
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "08_minhas_entregas_recusadas.png"))

        # 16. Central MeC: Copiar Todas as Tags e FAQ Accordion
        page.click('button[data-page="home"]')
        page.wait_for_selector("#page-home", state="visible")
        # Abre sub-aba Regras
        page.click('button[data-feed-tab="regras"]')
        page.wait_for_selector('[data-feed-sec="regras"]', state="visible")
        check(page.is_visible("#btn-copy-all-tags"), "Botão 'Copiar Todas as Tags' visível na Central MeC")
        page.click("#btn-copy-all-tags")
        page.wait_for_selector("#toast", state="visible", timeout=3000)
        check("copiad" in page.text_content("#toast").lower(), "Toast de feedback ao copiar tags oficiais")

        # Testar FAQ Accordion
        first_faq = page.locator(".faq-header").first
        check(first_faq.is_visible(), "Perguntas Frequentes (FAQ) visíveis")
        first_faq.click()
        page.wait_for_timeout(200)
        check(page.locator(".faq-item").first.evaluate("el => el.classList.contains('open')"),
              "FAQ Accordion expande resposta ao clique com sucesso")
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "09_central_mec_regras_faq.png"))

        # 17. Logout e Acesso Rápido Admin Hub (1 Clique)
        page.click("#logout")
        page.wait_for_selector("#login", state="visible")
        check(page.is_visible("#btn-demo-admin"), "Botão de Acesso Rápido Admin visível")
        page.click("#btn-demo-admin")
        page.wait_for_selector("#page-ranking", state="visible")
        check(page.is_visible('button[data-page="admin"]'), "Acesso concedido como Administrador (UFMG Hub)")

        # 18. Painel do Hub (Admin): Métricas e Botão Aprovar em Lote
        page.click('button[data-page="admin"]')
        page.wait_for_selector("#page-admin", state="visible")
        check(page.is_visible(".admin-metrics-row"), "Cartões de métricas rápidas visíveis no Admin")
        tot_metric = page.text_content("#adm-metric-total")
        pen_metric = page.text_content("#adm-metric-pendente")
        check(int(tot_metric) > 0, f"Métricas exibindo Total de Entregas: {tot_metric} (Pendentes: {pen_metric})")
        check(page.is_visible("#adm-btn-aprovar-lote"), "Botão 'Aprovar Pendentes em Lote' visível")
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "10_admin_metricas_e_lote.png"), full_page=True)

        ctx.close()

        # Contexto 2: Mobile Viewport (iPhone 14 / Pixel 7 - 390x844)
        ctx_mob = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, permissions=["clipboard-read", "clipboard-write"])
        page_mob = ctx_mob.new_page()

        # 19. Responsividade Mobile: Login e Bottom Navigation
        page_mob.goto(BASE_URL, wait_until="networkidle")
        page_mob.wait_for_selector("#login", state="visible")
        page_mob.screenshot(path=os.path.join(SCREENSHOTS_DIR, "11_mobile_login.png"), full_page=True)
        page_mob.click("#btn-demo-ej")
        page_mob.wait_for_selector("#page-ranking", state="visible")
        check(page_mob.is_visible("#bottomnav-mobile"), "Bottom Navigation mobile perfeitamente visível")
        page_mob.screenshot(path=os.path.join(SCREENSHOTS_DIR, "12_mobile_ranking.png"), full_page=True)

        # Navega para registrar ações no mobile
        page_mob.click('#bottomnav-mobile button[data-page="tarefas"]')
        page_mob.wait_for_selector("#page-tarefas", state="visible")
        page_mob.screenshot(path=os.path.join(SCREENSHOTS_DIR, "13_mobile_tarefas.png"), full_page=True)

        browser.close()

    print("\n" + "=" * 75)
    print(f"RESULTADO: {passed}/{total} VERIFICAÇÕES E TESTES APROVADOS COM 100% DE SUCESSO!")
    print(f"Capturas de tela salvas em: {SCREENSHOTS_DIR}")
    print("=" * 75)


if __name__ == "__main__":
    run_all_verifications()
