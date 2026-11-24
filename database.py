import sqlite3
import json
import os
import time
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "arena.db")

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS iniciativas (
        id TEXT PRIMARY KEY,
        nome TEXT NOT NULL UNIQUE,
        tipo TEXT NOT NULL DEFAULT 'Empresa Júnior',
        representante TEXT NOT NULL,
        cargo TEXT NOT NULL,
        redeSocial TEXT NOT NULL,
        salt TEXT NOT NULL,
        hash TEXT NOT NULL,
        criadoEm INTEGER NOT NULL,
        admin TEXT DEFAULT ''
    );

    CREATE TABLE IF NOT EXISTS entregas (
        id TEXT PRIMARY KEY,
        iniciativaId TEXT NOT NULL,
        tarefaId TEXT NOT NULL,
        tarefaNome TEXT NOT NULL,
        pontos INTEGER NOT NULL,
        url TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pendente',
        motivoRecusa TEXT DEFAULT '',
        criadoEm TEXT NOT NULL,
        revisadoEm TEXT DEFAULT ''
    );

    CREATE TABLE IF NOT EXISTS avisos (
        id TEXT PRIMARY KEY,
        tipo TEXT NOT NULL,
        criadoEm TEXT NOT NULL,
        expiraEm TEXT NOT NULL,
        iniciativaId TEXT DEFAULT '',
        pontos INTEGER DEFAULT 0,
        dados TEXT DEFAULT '{}',
        status TEXT NOT NULL DEFAULT 'ativo'
    );

    CREATE TABLE IF NOT EXISTS acoes_catalogo (
        id TEXT PRIMARY KEY,
        nome TEXT NOT NULL,
        pontos INTEGER NOT NULL,
        tipo TEXT NOT NULL DEFAULT 'link',
        descricao TEXT DEFAULT '',
        condicao TEXT DEFAULT '',
        criadoEm INTEGER NOT NULL,
        ativo TEXT NOT NULL DEFAULT 'sim'
    );

    CREATE TABLE IF NOT EXISTS briefings (
        id TEXT PRIMARY KEY,
        titulo TEXT NOT NULL,
        fase TEXT DEFAULT 'Geral',
        periodo TEXT DEFAULT 'Durante a Arena',
        descricao TEXT NOT NULL,
        diretrizes TEXT DEFAULT '',
        linkDrive TEXT DEFAULT '',
        hashtags TEXT DEFAULT '',
        bonus TEXT DEFAULT '',
        status TEXT NOT NULL DEFAULT 'ativo',
        criadoEm TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS cronograma (
        id TEXT PRIMARY KEY,
        data TEXT NOT NULL,
        titulo TEXT NOT NULL,
        local TEXT DEFAULT 'Campus Pampulha',
        tipo TEXT DEFAULT 'Presencial',
        pontos TEXT DEFAULT '',
        descricao TEXT DEFAULT '',
        status TEXT NOT NULL DEFAULT 'proximo',
        criadoEm TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS config_props (
        chave TEXT PRIMARY KEY,
        valor TEXT NOT NULL
    );
    """)

    conn.commit()
    seed_initial_data(conn)
    conn.close()

def get_prop(chave: str, default: str = "") -> str:
    conn = get_connection()
    row = conn.execute("SELECT valor FROM config_props WHERE chave = ?", (chave,)).fetchone()
    conn.close()
    return row["valor"] if row else default

def set_prop(chave: str, valor: str):
    conn = get_connection()
    conn.execute("INSERT OR REPLACE INTO config_props (chave, valor) VALUES (?, ?)", (chave, valor))
    conn.commit()
    conn.close()

def seed_initial_data(conn: sqlite3.Connection):
    # Se a tabela de iniciativas estiver vazia, semeia com exemplos realistas do ecossistema MeC
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as cnt FROM iniciativas")
    if cur.fetchone()["cnt"] == 0:
        import hashlib
        import uuid

        def hash_pwd(pwd: str, salt: str) -> str:
            h = salt + "::" + pwd
            for _ in range(50):
                h = hashlib.sha256((h + salt).encode("utf-8")).hexdigest().lower()
            return h

        now_ms = int(time.time() * 1000)

        # Iniciativas de exemplo
        inis = [
            ("ini_hub", "UFMG Hub", "Organização", "Gestão Hub", "Administrador", "@ufmghub", "sim", "admin123"),
            ("ini_1", "Engrenagem Jr.", "Empresa Júnior", "Mariana Costa", "Presidente", "@engrenagemjr", "", "123456"),
            ("ini_2", "Fórmula Tesla UFMG", "Equipe de Competição", "Lucas Ferreira", "Capitão", "@formulattesla", "", "123456"),
            ("ini_3", "Inova Consultoria Jr.", "Empresa Júnior", "Beatriz Lima", "Diretora de Marketing", "@inovajr", "", "123456"),
            ("ini_4", "Baja UFMG", "Equipe de Competição", "Gabriel Santos", "Piloto & Marketing", "@bajaufmg", "", "123456")
        ]

        for uid, nome, tipo, rep, cargo, rede, adm, pwd in inis:
            salt = str(uuid.uuid4())
            hpwd = hash_pwd(pwd, salt)
            cur.execute("""
                INSERT INTO iniciativas (id, nome, tipo, representante, cargo, redeSocial, salt, hash, criadoEm, admin)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (uid, nome, tipo, rep, cargo, rede, salt, hpwd, now_ms, adm))

        # Briefings Oficiais
        briefings = [
            (
                "#BRF-260927-0001",
                "Briefing #01: Convocação Geral das EJs e Lançamento do Ecossistema MeC",
                "Fase 1 · Aquecimento",
                "27/09 a 05/10",
                "Apresente para os seguidores e discentes da UFMG a participação da sua iniciativa no Mercado em Conexão 2026. Mostre a força da sua equipe e convide os estudantes a conhecerem a Arena.",
                "Peça autoral no Feed ou Carrossel. Use o logotipo oficial do MeC e do UFMG Hub nas artes. Evite artes com textos cortados.",
                "https://drive.google.com",
                "@mercadoemconexao @ufmghub #ArenaMeC #MercadoEmConexao #UFMGInovadora",
                "+30 pts extras para a iniciativa com o Carrossel mais informativo",
                "ativo",
                "27/09/2026 10:00:00"
            ),
            (
                "#BRF-260927-0002",
                "Briefing #02: Campanha de Inscrições para a Feira de Carreiras",
                "Fase 2 · Inscrições",
                "06/10 a 16/10",
                "Foco total na conversão de estudantes para se inscreverem na Feira de Carreiras com o código de indicação da sua iniciativa. Cada inscrição válida vale 2 pontos (até 200 pts!).",
                "Story diário com o link da bio/inscrição + Reels com membros da equipe explicando as oportunidades de estágio e trainees.",
                "https://drive.google.com",
                "@mercadoemconexao #FeiraMeC2026 #CarreirasUFMG #ArenaMeC",
                "+50 pts bônus para quem atingir o teto de 200 pts de inscrições",
                "em_breve",
                "27/09/2026 10:15:00"
            )
        ]

        for b in briefings:
            cur.execute("""
                INSERT INTO briefings (id, titulo, fase, periodo, descricao, diretrizes, linkDrive, hashtags, bonus, status, criadoEm)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, b)

        # Cronograma de Atividades
        cronograma = [
            ("#CRN-260927-0001", "05/10/2026", "Abertura Oficial das Inscrições da Feira", "Portal Mercado em Conexão", "Divulgação", "+2 pts por inscrição", "Início oficial do link de inscrições atribuídas para as iniciativas.", "andamento", "27/09/2026 09:00:00"),
            ("#CRN-260927-0002", "14/10/2026", "Blitz Universitária nos DAs e Centros Acadêmicos", "Praça de Serviços UFMG", "Presencial", "Até +40 pts", "Ações de abordagem, panfletagem e estandes volantes das equipes.", "proximo", "27/09/2026 09:00:00"),
            ("#CRN-260927-0003", "22/10/2026", "Feira de Carreiras Mercado em Conexão", "Escola de Engenharia UFMG", "Presencial", "+1 pt por visitante", "Grande feira presencial com estandes das empresas e das iniciativas.", "proximo", "27/09/2026 09:00:00"),
            ("#CRN-260927-0004", "23/10/2026", "Ciclo de Palestras & Hackathon Arena", "Auditório Principal", "Competição", "+1 pt por participante", "Palestras magnas com executivos e desafios de inovação.", "proximo", "27/09/2026 09:00:00")
        ]

        for c in cronograma:
            cur.execute("""
                INSERT INTO cronograma (id, data, titulo, local, tipo, pontos, descricao, status, criadoEm)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, c)

        # Entregas de exemplo para o ranking já iniciar com movimento
        entregas = [
            ("#ACT-260927-R812", "ini_1", "reel", "Reel ou vídeo autoral", 100, "https://instagram.com/p/reel_engrenagem", "validada", "", "26/09/2026 14:15:20", "26/09/2026 16:30:10"),
            ("#ACT-260927-C491", "ini_2", "carrossel", "Carrossel autoral", 50, "https://instagram.com/p/carrossel_tesla", "validada", "", "26/09/2026 18:22:45", "26/09/2026 20:00:00"),
            ("#ACT-260927-S770", "ini_1", "story_oficial", "Compartilhamento de story oficial", 5, "https://instagram.com/stories/engrenagem", "pendente", "", "27/09/2026 11:40:02", "")
        ]

        for e in entregas:
            cur.execute("""
                INSERT INTO entregas (id, iniciativaId, tarefaId, tarefaNome, pontos, url, status, motivoRecusa, criadoEm, revisadoEm)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, e)

        # Avisos / Lançamentos presenciais e contagens
        avisos = [
            ("#LNC-260926-P012", "presencial", "26/09/2026 15:00:00", "28/09/2026 15:00:00", "ini_1", 40, json.dumps({"oque": "Estande de Prototipagem na Feira", "quando": "26/09"}), "ativo"),
            ("#LNC-260926-I489", "inscricoes", "26/09/2026 19:30:00", "28/09/2026 19:30:00", "ini_2", 60, json.dumps({"quantidade": 30, "pontosUnitarios": 2}), "ativo")
        ]

        for a in avisos:
            cur.execute("""
                INSERT INTO avisos (id, tipo, criadoEm, expiraEm, iniciativaId, pontos, dados, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, a)

        conn.commit()
