# -*- coding: utf-8 -*-
"""
Captura screenshots do app Arena usando Playwright para validação visual.
Inclui as novas telas da Central MeC (Briefings, Cronograma Mensal, Regras)
e a gestão administrativa de Briefings e Cronograma.
"""

import os
import shutil
from playwright.sync_api import sync_playwright

html_path = os.path.abspath('Index.html')
file_url = f'file:///{html_path.replace(os.sep, "/")}'

os.makedirs('screenshots', exist_ok=True)
artifact_screenshots_dir = r'C:\Users\brand\.gemini\antigravity\brain\6df93881-4cb2-4234-9466-24b587e1fb8a\screenshots'
os.makedirs(artifact_screenshots_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    
    # 1. Desktop - Tela de Login
    page = browser.new_page(viewport={'width': 1366, 'height': 850})
    page.goto(file_url)
    page.wait_for_selector('#login', state='visible', timeout=5000)
    page.screenshot(path='screenshots/01_auth_login.png')
    print('1. Captured login screen')

    # Fazer Login como "Engrenagem Jr." (senha "123")
    page.fill('#login input[name="nome"]', 'Engrenagem Jr.')
    page.fill('#login input[name="senha"]', '123')
    page.click('#login button[type="submit"]')
    page.wait_for_selector('#page-ranking', state='visible', timeout=5000)
    page.wait_for_timeout(600)
    page.screenshot(path='screenshots/02_ranking_desktop.png')
    print('2. Captured ranking desktop')

    # 3. Expandir extrato de pontos
    page.click('[data-toggle-breakdown="ini_1"]')
    page.wait_for_timeout(350)
    page.screenshot(path='screenshots/03_ranking_breakdown.png')
    print('3. Captured ranking breakdown expanded')

    # 4. Navegar para "Registrar Ações"
    page.click('#topnav-desktop button[data-page="tarefas"]')
    page.wait_for_selector('#page-tarefas', state='visible')
    # Adicionar 1 story autoral (+10) e 1 reel (+100)
    page.click('#task-picker li:nth-child(2) button[data-act="inc"]')
    page.click('#task-picker li:nth-child(5) button[data-act="inc"]')
    page.wait_for_timeout(350)
    page.screenshot(path='screenshots/04_registrar_acoes.png')
    print('4. Captured registrar acoes')

    # 5. Navegar para "Minhas Entregas"
    page.click('#topnav-desktop button[data-page="entregas"]')
    page.wait_for_selector('#page-entregas', state='visible')
    page.screenshot(path='screenshots/05_minhas_entregas.png')
    print('5. Captured minhas entregas')

    # 6. Central MeC - Briefings Oficiais
    page.click('#topnav-desktop button[data-page="home"]')
    page.wait_for_selector('#page-home', state='visible')
    page.wait_for_timeout(400)
    page.screenshot(path='screenshots/06_feed_briefings.png')
    print('6. Captured feed briefings')

    # 7. Central MeC - Cronograma de Atividades Mensais
    page.click('#feed-tabs button[data-feed-tab="cronograma"]')
    page.wait_for_timeout(400)
    page.screenshot(path='screenshots/07_feed_cronograma.png')
    print('7. Captured feed cronograma')

    # 8. Central MeC - Edital & Tabela de Pontos
    page.click('#feed-tabs button[data-feed-tab="regras"]')
    page.wait_for_timeout(400)
    page.screenshot(path='screenshots/08_feed_regras.png')
    print('8. Captured feed regras')

    # 9. Deslogar e logar como Administrador "UFMG Hub"
    page.click('#logout')
    page.wait_for_selector('#login', state='visible')
    page.fill('#login input[name="nome"]', 'UFMG Hub')
    page.fill('#login input[name="senha"]', 'admin')
    page.click('#login button[type="submit"]')
    page.wait_for_selector('#page-ranking', state='visible')

    # Ir para Painel do Hub (Admin) - Aba 1: Validação de Comprovações
    page.click('#topnav-desktop button[data-page="admin"]')
    page.wait_for_selector('#page-admin', state='visible')
    page.wait_for_selector('.val-item', state='visible', timeout=5000)
    page.wait_for_timeout(350)
    page.screenshot(path='screenshots/09_admin_validar.png')
    print('9. Captured admin validar')

    # Sub-aba 2: Pontos de Evento e Inscrições
    page.click('#admin-tabs button[data-adm-tab="pontos"]')
    page.wait_for_timeout(350)
    page.screenshot(path='screenshots/10_admin_pontos.png')
    print('10. Captured admin pontos')

    # Sub-aba 3: Briefings & Cronograma MeC
    page.click('#admin-tabs button[data-adm-tab="gestao-mec"]')
    page.wait_for_timeout(350)
    page.screenshot(path='screenshots/11_admin_briefings_cronograma.png')
    print('11. Captured admin briefings e cronograma')

    # Sub-aba 4: Criar Nova Ação Dinâmica
    page.click('#admin-tabs button[data-adm-tab="novas-acoes"]')
    page.wait_for_timeout(350)
    page.screenshot(path='screenshots/12_admin_novas_acoes.png')
    print('12. Captured admin novas acoes')

    # Sub-aba 6: Diagnóstico & Manutenção da Base
    page.click('#admin-tabs button[data-adm-tab="diagnostico"]')
    page.wait_for_timeout(350)
    page.screenshot(path='screenshots/15_admin_diagnostico.png')
    print('15. Captured admin diagnostico')

    # 13. Mobile Viewport (iPhone / Android) - Ranking
    mobile_page = browser.new_page(viewport={'width': 390, 'height': 844})
    mobile_page.goto(file_url)
    mobile_page.wait_for_selector('#login', state='visible')
    mobile_page.fill('#login input[name="nome"]', 'Engrenagem Jr.')
    mobile_page.fill('#login input[name="senha"]', '123')
    mobile_page.click('#login button[type="submit"]')
    mobile_page.wait_for_selector('#page-ranking', state='visible')
    mobile_page.wait_for_timeout(500)
    mobile_page.screenshot(path='screenshots/13_mobile_ranking.png')
    print('13. Captured mobile ranking')

    # 14. Mobile Viewport - Central MeC Briefings
    mobile_page.click('#bottomnav-mobile button[data-page="home"]')
    mobile_page.wait_for_selector('#page-home', state='visible')
    mobile_page.wait_for_timeout(400)
    mobile_page.screenshot(path='screenshots/14_mobile_briefing.png')
    print('14. Captured mobile briefing')

    browser.close()

# Copiar todas as imagens para a pasta de artefatos
for img in os.listdir('screenshots'):
    if img.endswith('.png'):
        src = os.path.join('screenshots', img)
        dst = os.path.join(artifact_screenshots_dir, img)
        shutil.copy2(src, dst)

print('All screenshots captured and copied to artifact directory!')
