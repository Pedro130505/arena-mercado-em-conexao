# -*- coding: utf-8 -*-
"""
ARENA | Mercado em Conexão — Inicializador do Servidor Python + SQLite
"""
import sys
import os
import webbrowser
import threading
import time

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from server import run_server, PORT, DB_PATH

def open_browser():
    time.sleep(1.2)
    try:
        webbrowser.open(f"http://localhost:{PORT}")
    except Exception:
        pass

if __name__ == "__main__":
    print("=" * 65)
    print(" [ARENA] MERCADO EM CONEXAO")
    print(" Sistema de Gamificacao (Python 3 + SQLite 3)")
    print("=" * 65)
    print(f" -> Servidor rodando em: http://localhost:{PORT}")
    print(f" -> Banco de dados: {DB_PATH}")
    print(" -> Pressione CTRL+C no terminal para encerrar o servidor.\n")

    threading.Thread(target=open_browser, daemon=True).start()

    try:
        run_server()
    except KeyboardInterrupt:
        print("\n[ARENA] Servidor encerrado pelo usuario.")
