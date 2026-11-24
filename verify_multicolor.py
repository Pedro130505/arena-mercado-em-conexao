# -*- coding: utf-8 -*-
"""
Script de verificação visual automatizada com Playwright para o tema calibrado:
Amarelo/Laranja como cor principal da marca + cores ricas de apoio.
"""
import os
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT_DIR = r"C:\Users\brand\.gemini\antigravity\brain\6df93881-4cb2-4234-9466-24b587e1fb8a\screenshots_v4"
os.makedirs(OUT_DIR, exist_ok=True)
BASE_URL = "http://localhost:8080"

def run_visual_verification():
    print(f"Iniciando verificação visual em {BASE_URL}...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            viewport={"width": 1440, "height": 900},
            permissions=["clipboard-read", "clipboard-write"]
        )
        page = ctx.new_page()

        # 1. Tela de Login (Warm Solar Orange Gradient)
        page.goto(BASE_URL, wait_until="networkidle")
        page.wait_for_selector("#login", state="visible")
        path_login = os.path.join(OUT_DIR, "tuned_01_login.png")
        page.screenshot(path=path_login, full_page=True)
        print(f"[OK] Screenshot 1 salva: {path_login}")

        # 2. Login com Iniciativa (Engrenagem Jr.)
        page.click("#btn-demo-ej")
        page.wait_for_selector("#page-ranking", state="visible", timeout=10000)
        page.wait_for_timeout(800)

        # 3. Ranking com Topbar Laranja/Âmbar, Stat Cards (Ouro/Laranja protagonistas + Verde/Azul) e Pílulas
        path_ranking = os.path.join(OUT_DIR, "tuned_02_ranking.png")
        page.screenshot(path=path_ranking, full_page=True)
        print(f"[OK] Screenshot 2 salva: {path_ranking}")

        # 4. Navegar para Minhas Entregas
        page.click('button[data-page="entregas"]')
        page.wait_for_selector("#page-entregas", state="visible")
        page.wait_for_timeout(600)
        path_entregas = os.path.join(OUT_DIR, "tuned_03_minhas_entregas.png")
        page.screenshot(path=path_entregas, full_page=True)
        print(f"[OK] Screenshot 3 salva: {path_entregas}")

        # 5. Navegar para Central MeC
        page.click('button[data-page="home"]')
        page.wait_for_selector("#page-home", state="visible")
        page.wait_for_timeout(600)
        path_mec = os.path.join(OUT_DIR, "tuned_04_central_mec.png")
        page.screenshot(path=path_mec, full_page=True)
        print(f"[OK] Screenshot 4 salva: {path_mec}")

        # 6. Sair e Entrar como Admin
        page.click("#logout")
        page.wait_for_selector("#login", state="visible", timeout=10000)
        page.wait_for_timeout(300)
        page.click("#btn-demo-admin")
        page.wait_for_selector("#page-ranking", state="visible", timeout=10000)
        page.wait_for_selector('button[data-page="admin"]', state="visible", timeout=10000)
        page.click('button[data-page="admin"]')
        page.wait_for_selector("#page-admin", state="visible")
        page.wait_for_timeout(800)
        path_admin = os.path.join(OUT_DIR, "tuned_05_admin.png")
        page.screenshot(path=path_admin, full_page=True)
        print(f"[OK] Screenshot 5 salva: {path_admin}")

        ctx.close()

        # 7. Mobile Viewport (iPhone 14 / Pixel - 390x844)
        ctx_mob = browser.new_context(
            viewport={"width": 390, "height": 844},
            is_mobile=True,
            permissions=["clipboard-read", "clipboard-write"]
        )
        page_mob = ctx_mob.new_page()
        page_mob.goto(BASE_URL, wait_until="networkidle")
        page_mob.wait_for_selector("#login", state="visible")
        page_mob.click("#btn-demo-ej")
        page_mob.wait_for_selector("#page-ranking", state="visible", timeout=10000)
        page_mob.wait_for_timeout(800)
        path_mobile = os.path.join(OUT_DIR, "tuned_06_mobile_ranking.png")
        page_mob.screenshot(path=path_mobile, full_page=True)
        print(f"[OK] Screenshot 6 salva: {path_mobile}")

        ctx_mob.close()
        browser.close()

    print("\nTodas as 6 capturas de tela foram geradas com sucesso!")

if __name__ == "__main__":
    run_visual_verification()
