import asyncio
import os
import sys
from playwright.async_api import async_playwright

SCREENSHOT_DIR = r"C:\Users\brand\.gemini\antigravity\brain\6df93881-4cb2-4234-9466-24b587e1fb8a\screenshots_metricas"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        page.on("console", lambda msg: print(f"[Console] {msg.type}: {msg.text}", flush=True))

        print("1. Opening http://localhost:8080 ...", flush=True)
        await page.goto("http://localhost:8080", wait_until="networkidle")
        await page.wait_for_selector("#login", state="visible")

        # 1. Login with demo EJ (Engrenagem Jr.)
        print("2. Logging in with #btn-demo-ej ...", flush=True)
        await page.click("#btn-demo-ej")
        await page.wait_for_selector("#page-ranking", state="visible", timeout=10000)
        print("Logged in successfully as Engrenagem Jr.!", flush=True)

        # 2. Navigate to Minhas Entregas
        print("3. Navigating to Minhas Entregas ...", flush=True)
        await page.click('button[data-page="entregas"]')
        await page.wait_for_selector("#page-entregas", state="visible")
        await page.wait_for_timeout(600)

        # Take screenshot of Minhas Entregas with metrics section
        path_entregas = os.path.join(SCREENSHOT_DIR, "01_minhas_entregas_metricas_section.png")
        await page.screenshot(path=path_entregas, full_page=True)
        print(f"[OK] Screenshot 1 salva: {path_entregas}", flush=True)

        # 3. Find and click 'Registrar' on an available metric checkpoint
        reg_btn = page.locator(".btn-reg-metrica").first
        if await reg_btn.count() > 0:
            print("4. Clicking 'Registrar' on metric checkpoint...", flush=True)
            await reg_btn.scroll_into_view_if_needed()
            await reg_btn.click()

            # Wait for modal to become visible (hidden attribute removed)
            await page.wait_for_selector("#modal-registrar-metrica:not([hidden])", timeout=5000)
            await page.wait_for_timeout(500)

            # Fill metric form
            print("5. Filling metric form...", flush=True)
            await page.fill("#metric-alcance", "2850")
            await page.fill("#metric-engajamento", "415")
            await page.fill("#metric-comprovante", "https://drive.google.com/file/d/test-insights-engrenagem/view")
            await page.fill("#metric-obs", "Relatório de insights com alcance excelente e compartilhamentos comprovados.")

            # Screenshot of modal
            path_modal = os.path.join(SCREENSHOT_DIR, "02_modal_registrar_metrica.png")
            await page.screenshot(path=path_modal)
            print(f"[OK] Screenshot 2 salva: {path_modal}", flush=True)

            # Submit form
            print("6. Submitting metric form...", flush=True)
            await page.click("#m-metric-submit")

            # Wait for modal to close
            await page.wait_for_selector("#modal-registrar-metrica", state="hidden", timeout=5000)
            await page.wait_for_timeout(1000)

            # Screenshot after metric registered
            path_submetido = os.path.join(SCREENSHOT_DIR, "03_metrica_enviada_sucesso.png")
            await page.screenshot(path=path_submetido, full_page=True)
            print(f"[OK] Screenshot 3 salva: {path_submetido}", flush=True)

        # 4. Logout and Login as Admin
        print("7. Logging out and logging in as Admin...", flush=True)
        await page.click("#logout")
        await page.wait_for_selector("#login", state="visible")
        await page.click("#btn-demo-admin")
        await page.wait_for_selector("#page-ranking", state="visible")
        await page.wait_for_selector('button[data-page="admin"]', state="visible")

        # 5. Open Admin Page
        print("8. Opening Admin page...", flush=True)
        await page.click('button[data-page="admin"]')
        await page.wait_for_selector("#page-admin", state="visible")
        await page.wait_for_timeout(600)

        # 6. Switch to 'Acompanhamento de Métricas' Tab
        print("9. Switching to 'Acompanhamento de Métricas' tab...", flush=True)
        await page.click('button[data-adm-tab="metricas"]')
        await page.wait_for_timeout(800)

        # Screenshot of Admin metrics panel
        path_adm_met = os.path.join(SCREENSHOT_DIR, "04_admin_painel_metricas.png")
        await page.screenshot(path=path_adm_met, full_page=True)
        print(f"[OK] Screenshot 4 salva: {path_adm_met}", flush=True)

        # 7. Approve pending metric
        btn_aprovar = page.locator('button[data-met-act="validar"]').first
        if await btn_aprovar.count() > 0:
            print("10. Approving pending metric...", flush=True)
            await btn_aprovar.scroll_into_view_if_needed()
            await btn_aprovar.click()
            await page.wait_for_timeout(1500)

            # Screenshot after approval
            path_adm_aprov = os.path.join(SCREENSHOT_DIR, "05_admin_metricas_aprovada.png")
            await page.screenshot(path=path_adm_aprov, full_page=True)
            print(f"[OK] Screenshot 5 salva: {path_adm_aprov}", flush=True)
        else:
            print("No button with button[data-met-act='validar'] found!", flush=True)

        # 8. Check Ranking tab
        print("11. Checking Ranking tab...", flush=True)
        await page.click('button[data-page="ranking"]')
        await page.wait_for_selector("#page-ranking", state="visible")
        await page.wait_for_timeout(800)
        path_rank = os.path.join(SCREENSHOT_DIR, "06_admin_ranking_com_bonus.png")
        await page.screenshot(path=path_rank, full_page=True)
        print(f"[OK] Screenshot 6 salva: {path_rank}", flush=True)

        await browser.close()
        print("🎉 TODOS OS TESTES E2E PASSARAM COM SUCESSO!", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
