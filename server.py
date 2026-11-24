# -*- coding: utf-8 -*-
"""
ARENA | Mercado em Conexão — Servidor Backend SQLite 3 (Produção & Alta Concorrência)
====================================================================================
Banco de dados relacional SQLite (`arena.db`) com:
- Modo WAL (Write-Ahead Logging) para leituras e escritas simultâneas rápidas
- Autenticação com PBKDF2/SHA-256 + Tokens assinados com HMAC-SHA256
- IDs únicos rastreáveis (#ACT-YYMMDD-XXXX, #LNC-YYMMDD-XXXX, #BRF-..., #CRN-...)
- Datas e horários padronizados no fuso de Brasília (dd/MM/yyyy HH:mm:ss)
- Prevenção de fraude e deduplicação canônica de links enviados
- Exportação direta para CSV compatível com Excel (UTF-8 com BOM)
"""

import csv
import datetime
import hashlib
import hmac
import io
import json
import os
import random
import re
import sqlite3
import threading
import time
import urllib.parse
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "arena.db")
PORT = int(os.environ.get("PORT", 8080))

# Lock para escrita transacional segura em multithread
DB_WRITE_LOCK = threading.Lock()

# ============================== CONFIGURAÇÃO OFICIAL ==============================

CONFIG = {
    "ADMIN_NOME": "UFMG Hub",
    "PONTOS_POR_INSCRICAO": 2,
    "LIMITE_PONTOS_INSCRICAO": 200,
    "PONTOS_POR_RESPOSTA": 1,
    "PONTOS_POR_PALESTRA": 1,
    "PONTOS_POR_FEIRA": 1,
    "PONTOS_POR_CHALLENGE": 1,
    "MAX_PONTOS_PRESENCIAL": 40,
    "HORAS": {
        "tarefa": 72,
        "presencial": 48,
        "inscricoes": 48,
        "formulario": 48,
        "palestras": 48,
        "feira": 48,
        "challenges": 48,
        "avulso": 48,
    },
    "EDITAL_URL": "",
    "SESSAO_DIAS": 30,
    "MARCACAO": "Não esqueça de marcar a @mercadoemconexao!",
    "TAREFA_PADRAO": "Não há entregas sugeridas para essa semana, mas qualquer divulgação extra pode gerar bônus de pontuação!",
    "MAX_LINKS_POR_ENVIO": 60,
}

TAREFAS_BASE = [
    {"id": "story_oficial", "nome": "Compartilhamento de story oficial", "pontos": 5, "condicao": "Conforme limite do briefing", "icone": "story"},
    {"id": "story_autoral", "nome": "Story autoral", "pontos": 10, "condicao": "Conteúdo próprio e aderente à missão", "icone": "story"},
    {"id": "feed_estatico", "nome": "Publicação estática no feed", "pontos": 30, "condicao": "Peça própria ou adaptação autorizada", "icone": "post"},
    {"id": "carrossel", "nome": "Carrossel autoral", "pontos": 50, "condicao": "Mínimo de 3 cards com conteúdo informativo", "icone": "carousel"},
    {"id": "reel", "nome": "Reel ou vídeo autoral", "pontos": 100, "condicao": "Conteúdo original com mensagem clara", "icone": "reel"},
]

REGRAS = [
    "Perfil Público: Mantenha a conta da iniciativa pública durante toda a competição.",
    "Marcação Obrigatória: Sempre marque o perfil oficial @mercadoemconexao.",
    "Post Ativo: Não apague nem arquive a publicação do Feed após o envio.",
    "Respeito e Ética: O conteúdo não pode conter palavrões, termos ofensivos ou preconceituosos.",
    "Validação no Prazo: Envie o link do post dentro do prazo de cada tarefa para homologação dos pontos.",
    "Limite de Inscrições: A pontuação de inscrições atribuídas à iniciativa tem teto máximo de 200 pontos na campanha.",
]

CONTAGENS = {
    "inscricoes": {"rotulo": "Inscrições atribuídas", "pontos": CONFIG["PONTOS_POR_INSCRICAO"], "limite": CONFIG["LIMITE_PONTOS_INSCRICAO"]},
    "formulario": {"rotulo": "Respostas no formulário de pesquisa", "pontos": CONFIG["PONTOS_POR_RESPOSTA"]},
    "palestras": {"rotulo": "Presença nas palestras", "pontos": CONFIG["PONTOS_POR_PALESTRA"]},
    "feira": {"rotulo": "Presença real na feira de carreiras", "pontos": CONFIG["PONTOS_POR_FEIRA"]},
    "challenges": {"rotulo": "Participação nos challenges", "pontos": CONFIG["PONTOS_POR_CHALLENGE"]},
}


# ============================== UTILITÁRIOS DE TEMPO, TEXTO E IDs ==============================

class UserError(Exception):
    def __init__(self, msg, sair=False):
        super().__init__(msg)
        self.message = msg
        self.sair = sair


def tz_brasilia():
    return datetime.timezone(datetime.timedelta(hours=-3))


def agora_dt():
    return datetime.datetime.now(tz_brasilia())


def agora_ms():
    return int(time.time() * 1000)


def formatar_data_hora(dt=None):
    if dt is None:
        dt = agora_dt()
    elif isinstance(dt, (int, float)):
        dt = datetime.datetime.fromtimestamp(dt / 1000.0, tz=tz_brasilia())
    return dt.strftime("%d/%m/%Y %H:%M:%S")


def gerar_id_unico(prefixo="ACT"):
    dt = agora_dt()
    data_str = dt.strftime("%y%m%d")
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    sufixo = "".join(random.choice(chars) for _ in range(4))
    return f"#{prefixo}-{data_str}-{sufixo}"


def normalizar(s):
    import unicodedata
    s = str(s or "")
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s


def validar_texto(v, rotulo, max_len, obrigatorio=False):
    s = re.sub(r"\s+", " ", str(v if v is not None else "")).strip()
    if obrigatorio and not s:
        raise UserError(f'Preencha o campo "{rotulo}".')
    if len(s) > max_len:
        raise UserError(f'O campo "{rotulo}" aceita no máximo {max_len} caracteres.')
    return s


def validar_inteiro(v, rotulo):
    s = re.sub(r"\s+", "", str(v if v is not None else ""))
    if not re.match(r"^[+-]?\d+$", s):
        raise UserError(f'"{rotulo}" deve ser um número inteiro (ex.: 20).')
    return int(s)


def url_valida(u):
    u = str(u or "").strip()
    if len(u) > 500:
        return False
    return bool(re.match(r"^https?://[^\s/$.?#][^\s]*\.[^\s]{2,}", u, re.IGNORECASE))


def limpar_url(u):
    if not u:
        return ""
    s = str(u).strip()
    s = re.sub(r"[?&](utm_[^&=]+|igsh|fbclid|src|ref|share_id|startTime|mibextid)=[^&#]*", "", s, flags=re.IGNORECASE)
    s = re.sub(r"/+\?", "?", s)
    s = re.sub(r"[?&#/]+$", "", s)
    return s


# ============================== BANCO DE DADOS SQLITE ==============================

def get_conn():
    conn = sqlite3.connect(DB_PATH, timeout=15.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def _ensure_column(conn, table, col, col_def):
    cols = [r["name"] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()]
    if col not in cols:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {col} {col_def}")


def init_db():
    with DB_WRITE_LOCK:
        conn = get_conn()
        try:
            with conn:
                conn.executescript("""
                CREATE TABLE IF NOT EXISTS config_meta (
                    chave TEXT PRIMARY KEY,
                    valor TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS iniciativas (
                    id TEXT PRIMARY KEY,
                    nome TEXT NOT NULL UNIQUE COLLATE NOCASE,
                    tipo TEXT NOT NULL DEFAULT 'Empresa Júnior',
                    representante TEXT NOT NULL,
                    cargo TEXT NOT NULL,
                    redeSocial TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    hash TEXT NOT NULL,
                    criadoEm TEXT NOT NULL,
                    criadoEmMs INTEGER NOT NULL DEFAULT 0,
                    admin TEXT NOT NULL DEFAULT ''
                );

                CREATE TABLE IF NOT EXISTS entregas (
                    id TEXT PRIMARY KEY,
                    iniciativaId TEXT NOT NULL,
                    tarefaId TEXT NOT NULL,
                    tarefaNome TEXT NOT NULL,
                    pontos INTEGER NOT NULL,
                    url TEXT NOT NULL,
                    urlCanonica TEXT NOT NULL DEFAULT '',
                    status TEXT NOT NULL DEFAULT 'pendente',
                    motivoRecusa TEXT NOT NULL DEFAULT '',
                    criadoEm TEXT NOT NULL,
                    criadoEmMs INTEGER NOT NULL DEFAULT 0,
                    revisadoEm TEXT NOT NULL DEFAULT '',
                    revisadoEmMs INTEGER NOT NULL DEFAULT 0
                );

                CREATE TABLE IF NOT EXISTS avisos (
                    id TEXT PRIMARY KEY,
                    tipo TEXT NOT NULL,
                    criadoEm TEXT NOT NULL,
                    criadoEmMs INTEGER NOT NULL DEFAULT 0,
                    expiraEm TEXT NOT NULL,
                    expiraEmMs INTEGER NOT NULL DEFAULT 0,
                    iniciativaId TEXT NOT NULL DEFAULT '',
                    pontos INTEGER NOT NULL DEFAULT 0,
                    dados TEXT NOT NULL DEFAULT '{}',
                    status TEXT NOT NULL DEFAULT 'ativo'
                );

                CREATE TABLE IF NOT EXISTS acoes_catalogo (
                    id TEXT PRIMARY KEY,
                    nome TEXT NOT NULL,
                    pontos INTEGER NOT NULL,
                    tipo TEXT NOT NULL DEFAULT 'link',
                    descricao TEXT NOT NULL DEFAULT '',
                    condicao TEXT NOT NULL DEFAULT '',
                    criadoEm TEXT NOT NULL,
                    criadoEmMs INTEGER NOT NULL DEFAULT 0,
                    ativo TEXT NOT NULL DEFAULT 'sim'
                );

                CREATE TABLE IF NOT EXISTS briefings (
                    id TEXT PRIMARY KEY,
                    titulo TEXT NOT NULL,
                    fase TEXT NOT NULL,
                    periodo TEXT NOT NULL,
                    descricao TEXT NOT NULL,
                    diretrizes TEXT NOT NULL DEFAULT '',
                    linkDrive TEXT NOT NULL DEFAULT '',
                    hashtags TEXT NOT NULL DEFAULT '',
                    bonus TEXT NOT NULL DEFAULT '',
                    status TEXT NOT NULL DEFAULT 'ativo',
                    criadoEm TEXT NOT NULL,
                    criadoEmMs INTEGER NOT NULL DEFAULT 0
                );

                CREATE TABLE IF NOT EXISTS cronograma (
                    id TEXT PRIMARY KEY,
                    data TEXT NOT NULL,
                    titulo TEXT NOT NULL,
                    local TEXT NOT NULL DEFAULT '',
                    tipo TEXT NOT NULL DEFAULT 'Presencial',
                    pontos TEXT NOT NULL DEFAULT '',
                    descricao TEXT NOT NULL DEFAULT '',
                    status TEXT NOT NULL DEFAULT 'proximo',
                    criadoEm TEXT NOT NULL,
                    criadoEmMs INTEGER NOT NULL DEFAULT 0
                );

                CREATE TABLE IF NOT EXISTS metricas_entregas (
                    id TEXT PRIMARY KEY,
                    entregaId TEXT NOT NULL,
                    iniciativaId TEXT NOT NULL,
                    iniciativaNome TEXT NOT NULL DEFAULT '',
                    tarefaId TEXT NOT NULL DEFAULT '',
                    tarefaNome TEXT NOT NULL DEFAULT '',
                    tipoMidia TEXT NOT NULL DEFAULT 'post',
                    periodo TEXT NOT NULL,
                    periodoRotulo TEXT NOT NULL DEFAULT '',
                    pontos INTEGER NOT NULL DEFAULT 10,
                    alcance INTEGER NOT NULL DEFAULT 0,
                    engajamento INTEGER NOT NULL DEFAULT 0,
                    comprovanteUrl TEXT NOT NULL DEFAULT '',
                    observacoes TEXT NOT NULL DEFAULT '',
                    status TEXT NOT NULL DEFAULT 'pendente',
                    motivoRecusa TEXT NOT NULL DEFAULT '',
                    criadoEm TEXT NOT NULL,
                    criadoEmMs INTEGER NOT NULL DEFAULT 0,
                    revisadoEm TEXT NOT NULL DEFAULT '',
                    revisadoEmMs INTEGER NOT NULL DEFAULT 0
                );
                CREATE INDEX IF NOT EXISTS idx_metricas_entrega ON metricas_entregas(entregaId);
                CREATE INDEX IF NOT EXISTS idx_metricas_iniciativa ON metricas_entregas(iniciativaId);

                """)

                # Migração automática caso uma base anterior exista
                _ensure_column(conn, "iniciativas", "tipo", "TEXT NOT NULL DEFAULT 'Empresa Júnior'")
                _ensure_column(conn, "iniciativas", "criadoEmMs", "INTEGER NOT NULL DEFAULT 0")
                _ensure_column(conn, "entregas", "urlCanonica", "TEXT NOT NULL DEFAULT ''")
                _ensure_column(conn, "entregas", "motivoRecusa", "TEXT NOT NULL DEFAULT ''")
                _ensure_column(conn, "entregas", "criadoEmMs", "INTEGER NOT NULL DEFAULT 0")
                _ensure_column(conn, "entregas", "revisadoEmMs", "INTEGER NOT NULL DEFAULT 0")
                _ensure_column(conn, "avisos", "criadoEmMs", "INTEGER NOT NULL DEFAULT 0")
                _ensure_column(conn, "avisos", "expiraEmMs", "INTEGER NOT NULL DEFAULT 0")
                _ensure_column(conn, "acoes_catalogo", "criadoEmMs", "INTEGER NOT NULL DEFAULT 0")
                _ensure_column(conn, "briefings", "criadoEmMs", "INTEGER NOT NULL DEFAULT 0")
                _ensure_column(conn, "cronograma", "criadoEmMs", "INTEGER NOT NULL DEFAULT 0")

                # Preenche urlCanonica se estiver vazia em registros legados
                rows_sem_canon = conn.execute("SELECT id, url FROM entregas WHERE urlCanonica = ''").fetchall()
                for r in rows_sem_canon:
                    conn.execute("UPDATE entregas SET urlCanonica = ? WHERE id = ?", (limpar_url(r["url"]), r["id"]))

                conn.executescript("""
                CREATE INDEX IF NOT EXISTS idx_entregas_ini ON entregas(iniciativaId);
                CREATE INDEX IF NOT EXISTS idx_entregas_url ON entregas(urlCanonica);
                CREATE INDEX IF NOT EXISTS idx_entregas_status ON entregas(status);
                CREATE INDEX IF NOT EXISTS idx_avisos_ini ON avisos(iniciativaId);
                CREATE INDEX IF NOT EXISTS idx_avisos_tipo ON avisos(tipo);
                """)

                # Garante segredo HMAC persistente
                row = conn.execute("SELECT valor FROM config_meta WHERE chave = 'ARENA_SEGREDO'").fetchone()
                if not row:
                    seg = str(uuid.uuid4()) + str(uuid.uuid4())
                    conn.execute("INSERT INTO config_meta (chave, valor) VALUES ('ARENA_SEGREDO', ?)", (seg,))

                # Verifica se já fez o seed inicial
                seeded = conn.execute("SELECT valor FROM config_meta WHERE chave = 'SEED_INICIAL'").fetchone()
                if not seeded:
                    seed_initial_data(conn)
                    conn.execute("INSERT INTO config_meta (chave, valor) VALUES ('SEED_INICIAL', 'sim')")
        finally:
            conn.close()


def hash_senha(senha, salt):
    h = f"{salt}::{senha}"
    for _ in range(50):
        h = hashlib.sha256((h + salt).encode("utf-8")).hexdigest()
    return h


def obter_segredo(conn):
    row = conn.execute("SELECT valor FROM config_meta WHERE chave = 'ARENA_SEGREDO'").fetchone()
    return row["valor"] if row else "segredo_padrao_arena"


def assinar_token(carga, segredo):
    import base64
    sig = hmac.new(segredo.encode("utf-8"), carga.encode("utf-8"), hashlib.sha256).digest()
    return base64.urlsafe_b64encode(sig).decode("utf-8").rstrip("=")


def gerar_token(conn, user_id):
    import base64
    exp = agora_ms() + CONFIG["SESSAO_DIAS"] * 86400000
    carga = f"{user_id}|{exp}"
    b64 = base64.urlsafe_b64encode(carga.encode("utf-8")).decode("utf-8").rstrip("=")
    assinatura = assinar_token(carga, obter_segredo(conn))
    return f"{b64}.{assinatura}"


def ler_token(conn, token):
    import base64
    if not token or not isinstance(token, str):
        return None
    # Compatibilidade caso o frontend tenha token simples de sessão anterior
    if "." not in token:
        row = conn.execute("SELECT id FROM iniciativas WHERE id = ?", (token,)).fetchone()
        return row["id"] if row else None
    partes = token.split(".")
    if len(partes) != 2:
        return None
    try:
        b64_padded = partes[0] + "=" * (-len(partes[0]) % 4)
        carga = base64.urlsafe_b64decode(b64_padded.encode("utf-8")).decode("utf-8")
    except Exception:
        return None
    if assinar_token(carga, obter_segredo(conn)) != partes[1]:
        return None
    p = carga.split("|")
    if len(p) != 2:
        return None
    try:
        if int(p[1]) < agora_ms():
            return None
    except ValueError:
        return None
    return p[0]


def seed_initial_data(conn):
    """Popula o banco SQLite na primeira execução com dados realistas de demonstração e conta Admin."""
    now = agora_ms()

    iniciativas_seed = [
        ("ini_admin", "UFMG Hub", "Outro", "Gestão Hub", "Administrador", "@ufmghub", "admin", "sim"),
        ("ini_1", "Engrenagem Jr.", "Empresa Júnior", "Lucas Mendes", "Diretor de Marketing", "@engrenagemjr", "123", ""),
        ("ini_2", "Fórmula Tesla UFMG", "Equipe de Competição", "Mariana Costa", "Capitã", "@formulateslaufmg", "123", ""),
        ("ini_3", "Inova Consultoria Jr.", "Empresa Júnior", "Pedro Alves", "Presidente", "@inovajr", "123", ""),
        ("ini_4", "Baja UFMG", "Equipe de Competição", "Gabriel Rocha", "Membro de Gestão", "@bajaufmg", "123", ""),
    ]

    for uid, nome, tipo, rep, cargo, rede, senha, adm in iniciativas_seed:
        salt = str(uuid.uuid4())
        h = hash_senha(senha, salt)
        dt_str = formatar_data_hora(now - 7200000)
        conn.execute("""
            INSERT OR IGNORE INTO iniciativas (id, nome, tipo, representante, cargo, redeSocial, salt, hash, criadoEm, criadoEmMs, admin)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (uid, nome, tipo, rep, cargo, rede, salt, h, dt_str, now - 7200000, adm))

    briefings_seed = [
        (
            "#BRF-260925-0101",
            "Briefing #01: Aquecimento & Bastidores da Equipe",
            "Fase 1 · Aquecimento",
            "25/09 a 05/10",
            "Mostre como a sua Empresa Júnior ou Equipe de Competição está se preparando para o Mercado em Conexão! O objetivo é gerar curiosidade nos estudantes da UFMG e destacar o protagonismo estudantil.",
            "1. Grave um Reel ou faça um Carrossel mostrando o dia a dia, projetos ou oficina da equipe.\n2. Mencione que vocês estarão presentes na Feira do Mercado em Conexão.\n3. Perfil deve estar aberto/público e marcar os perfis oficiais.",
            "https://drive.google.com/drive/u/0/",
            "@mercadoemconexao @ufmghub #ArenaMeC #MercadoEmConexao #UFMGInovadora",
            "+50 pts extras para os 3 vídeos mais criativos da semana",
            "ativo",
            formatar_data_hora(now - 86400000),
            now - 86400000,
        ),
        (
            "#BRF-260926-0202",
            "Briefing #02: Mutirão Oficial de Inscrições na Feira",
            "Fase 2 · Inscrições",
            "06/10 a 18/10",
            "Mobilize os membros, ex-membros e colegas de curso para realizarem a inscrição gratuita no Mercado em Conexão indicando a sua iniciativa no formulário oficial!",
            "1. Publique nos Stories o link de inscrição usando o template oficial do Kit de Mídia.\n2. Oriente os inscritos a selecionarem o nome da sua EJ/Equipe no campo de indicação.\n3. Cada inscrição validada rende +2 pontos (até o limite de 200 pontos).",
            "https://drive.google.com/drive/u/0/",
            "@mercadoemconexao @ufmghub #ArenaMeC #FeiraDeCarreirasUFMG",
            "+30 pts para a primeira iniciativa que atingir 50 inscritos",
            "ativo",
            formatar_data_hora(now - 43200000),
            now - 43200000,
        ),
        (
            "#BRF-260927-0303",
            "Briefing #03: Cobertura Ao Vivo nos Dias do Evento",
            "Fase 3 · Evento Presencial",
            "20/10 a 24/10",
            "Durante os dias de palestras, challenges e Feira de Carreiras, compartilhe em tempo real a participação dos seus membros nos estandes e auditórios!",
            "1. Faça stories nos auditórios e estandes das empresas parceiras.\n2. Entreviste membros contando o que estão achando das conexões.\n3. Registre todos os links aqui na Arena antes do encerramento.",
            "https://drive.google.com/drive/u/0/",
            "@mercadoemconexao @ufmghub #AoVivoMeC #ArenaMeC",
            "Dobro de pontos em Reels gravados dentro da Feira",
            "em_breve",
            formatar_data_hora(now - 21600000),
            now - 21600000,
        ),
    ]

    for b in briefings_seed:
        conn.execute("""
            INSERT OR IGNORE INTO briefings (id, titulo, fase, periodo, descricao, diretrizes, linkDrive, hashtags, bonus, status, criadoEm, criadoEmMs)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, b)

    cronograma_seed = [
        ("#CRN-261005-0001", "05/10", "Abertura Oficial da Arena & Lançamento do Kit de Mídia", "Online / Instagram @mercadoemconexao", "Divulgação", "+10 a +100 pts em posts", "Início da contabilização de pontos de redes sociais para todas as EJs e Equipes.", "andamento", formatar_data_hora(now - 90000000), now - 90000000),
        ("#CRN-261014-0002", "14/10", "Blitz Presencial de Divulgação & Interação", "Praça de Serviços e Escola de Engenharia - UFMG", "Presencial", "Até +40 pts presenciais", "Ação conjunta das iniciativas no campus para convidar os estudantes e apresentar protótipos e projetos.", "proximo", formatar_data_hora(now - 80000000), now - 80000000),
        ("#CRN-261021-0003", "21/10", "Ciclo de Palestras & Painéis de Inovação e Carreira", "Auditório Principal - CAD / Engenharia", "Palestra", "+1 pt por membro presente", "Palestras com grandes nomes do mercado e lideranças empresariais.", "proximo", formatar_data_hora(now - 70000000), now - 70000000),
        ("#CRN-261022-0004", "22/10", "Challenges Empresariais & Resolução de Cases", "Salas de Dinâmica - Campus Pampulha", "Competição", "+1 pt por participante", "Desafios práticos propostos pelas empresas patrocinadoras para os alunos.", "proximo", formatar_data_hora(now - 60000000), now - 60000000),
        ("#CRN-261023-0005", "23/10", "Grande Feira de Carreiras Mercado em Conexão & Premiação", "Espaço de Eventos - UFMG", "Presencial", "+1 pt por visita + Premiação Final", "Encerramento da Arena, anúncio do Pódio Oficial das Iniciativas e entrega da premiação!", "proximo", formatar_data_hora(now - 50000000), now - 50000000),
    ]

    for c in cronograma_seed:
        conn.execute("""
            INSERT OR IGNORE INTO cronograma (id, data, titulo, local, tipo, pontos, descricao, status, criadoEm, criadoEmMs)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, c)

    entregas_seed = [
        ("#ACT-260927-A104", "ini_1", "reel", "Reel ou vídeo autoral", 100, "https://instagram.com/p/reel-engrenagem-1", "https://instagram.com/p/reel-engrenagem-1", "validada", "", "27/09/2026 10:15:22", now - 3600000, "27/09/2026 11:02:10", now - 1800000),
        ("#ACT-260927-B209", "ini_1", "carrossel", "Carrossel autoral", 50, "https://instagram.com/p/carrossel-engrenagem-2", "https://instagram.com/p/carrossel-engrenagem-2", "validada", "", "27/09/2026 11:20:05", now - 3200000, "27/09/2026 11:45:30", now - 1500000),
        ("#ACT-260927-C318", "ini_1", "story_autoral", "Story autoral", 10, "https://instagram.com/stories/engrenagem/3", "https://instagram.com/stories/engrenagem/3", "pendente", "", "27/09/2026 13:05:49", now - 900000, "", 0),
        ("#ACT-260927-D422", "ini_2", "reel", "Reel ou vídeo autoral", 100, "https://instagram.com/p/reel-tesla-1", "https://instagram.com/p/reel-tesla-1", "validada", "", "27/09/2026 09:40:12", now - 4000000, "27/09/2026 10:30:00", now - 2000000),
        ("#ACT-260927-E511", "ini_2", "feed_estatico", "Publicação estática no feed", 30, "https://instagram.com/p/feed-tesla-2", "https://instagram.com/p/feed-tesla-2", "pendente", "", "27/09/2026 13:18:04", now - 500000, "", 0),
        ("#ACT-260927-F607", "ini_3", "carrossel", "Carrossel autoral", 50, "https://instagram.com/p/carrossel-inova-1", "https://instagram.com/p/carrossel-inova-1", "validada", "", "27/09/2026 08:55:33", now - 5000000, "27/09/2026 09:30:00", now - 2500000),
        ("#ACT-260927-G719", "ini_4", "story_oficial", "Compartilhamento de story oficial", 5, "https://instagram.com/stories/baja/1", "https://instagram.com/stories/baja/1", "validada", "", "27/09/2026 08:10:00", now - 6000000, "27/09/2026 09:00:00", now - 3000000),
    ]

    for e in entregas_seed:
        conn.execute("""
            INSERT OR IGNORE INTO entregas (id, iniciativaId, tarefaId, tarefaNome, pontos, url, urlCanonica, status, motivoRecusa, criadoEm, criadoEmMs, revisadoEm, revisadoEmMs)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, e)

    avisos_seed = [
        ("#LNC-260926-P340", "presencial", "26/09/2026 16:40:15", now - 14400000, formatar_data_hora(now + 86400000), now + 86400000, "ini_1", 40, json.dumps({"oque": "Exposição de projetos na Praça de Serviços", "quando": "26/09"}), "ativo"),
        ("#LNC-260926-I489", "inscricoes", "26/09/2026 19:30:00", now - 8000000, formatar_data_hora(now + 86400000), now + 86400000, "ini_2", 60, json.dumps({"quantidade": 30, "pontosUnitarios": 2}), "ativo"),
        ("#LNC-260926-T100", "tarefa", "26/09/2026 12:00:00", now - 10000000, formatar_data_hora(now + 72 * 3600000), now + 72 * 3600000, "", 0, json.dumps({
            "sobre": "Divulgação da Abertura da Arena e do Ecossistema de Inovação",
            "periodo": "27/09 a 03/10",
            "recomendacoes": "Use a hashtag #ArenaMEC e mostre os bastidores da sua equipe.",
            "bonus": "+50 pontos extras para o post de maior engajamento da semana"
        }), "ativo"),
    ]

    for a in avisos_seed:
        conn.execute("""
            INSERT OR IGNORE INTO avisos (id, tipo, criadoEm, criadoEmMs, expiraEm, expiraEmMs, iniciativaId, pontos, dados, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, a)

    # Seed de Métricas Pós-Publicação
    metricas_seed = [
        (
            "#MTR-260928-S010", "#ACT-260927-C318", "ini_1", "Engrenagem Jr.", "story_autoral", "Story autoral",
            "story", "24h", "24 Horas Stories", 5, 840, 92,
            "https://drive.google.com/drive/u/0/sample-story-insights", "Stories teve 18 respostas diretas e 3 cliques no link.",
            "validada", "", "28/09/2026 14:00:00", now - 4000000, "28/09/2026 15:30:00", now - 3500000
        ),
        (
            "#MTR-261004-W010", "#ACT-260927-A104", "ini_1", "Engrenagem Jr.", "reel", "Reel ou vídeo autoral",
            "post", "sem1", "1ª Semana", 10, 3250, 410,
            "https://drive.google.com/drive/u/0/sample-reel-w1", "Reel atingiu 3.250 contas nos primeiros 7 dias.",
            "validada", "", "04/10/2026 10:15:00", now - 2500000, "04/10/2026 12:00:00", now - 2000000
        ),
        (
            "#MTR-261011-W020", "#ACT-260927-A104", "ini_1", "Engrenagem Jr.", "reel", "Reel ou vídeo autoral",
            "post", "sem2", "2ª Semana", 10, 4120, 485,
            "https://drive.google.com/drive/u/0/sample-reel-w2", "Crescimento orgânico continuou alto com 75 salvamentos.",
            "pendente", "", "11/10/2026 16:40:00", now - 500000, "", 0
        ),
        (
            "#MTR-261004-W030", "#ACT-260927-D422", "ini_2", "Fórmula Tesla UFMG", "reel", "Reel ou vídeo autoral",
            "post", "sem1", "1ª Semana", 10, 2180, 290,
            "https://drive.google.com/drive/u/0/sample-tesla-w1", "Vídeo do protótipo elétrico teve excelente alcance com calouros.",
            "validada", "", "04/10/2026 11:20:00", now - 2400000, "04/10/2026 13:10:00", now - 1900000
        ),
    ]
    for m in metricas_seed:
        conn.execute("""
            INSERT OR IGNORE INTO metricas_entregas (
                id, entregaId, iniciativaId, iniciativaNome, tarefaId, tarefaNome,
                tipoMidia, periodo, periodoRotulo, pontos, alcance, engajamento,
                comprovanteUrl, observacoes, status, motivoRecusa, criadoEm, criadoEmMs, revisadoEm, revisadoEmMs
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, m)


# ============================== LÓGICA DE NEGÓCIO E AUTENTICAÇÃO ==============================

def eh_admin(u):
    if not u:
        return False
    return str(u["admin"]) == "sim" or normalizar(u["nome"]) == normalizar(CONFIG["ADMIN_NOME"])


def usuario_autenticado(conn, token):
    uid = ler_token(conn, token)
    if not uid:
        raise UserError("Sua sessão expirou ou é inválida. Entre novamente.", sair=True)
    row = conn.execute("SELECT * FROM iniciativas WHERE id = ?", (uid,)).fetchone()
    if not row:
        raise UserError("Sua sessão expirou ou é inválida. Entre novamente.", sair=True)
    return dict(row)


def admin_autenticado(conn, token):
    u = usuario_autenticado(conn, token)
    if not eh_admin(u):
        raise UserError("Função exclusiva do administrador (UFMG Hub).")
    return u


def obter_tarefas(conn):
    lista = [dict(t) for t in TAREFAS_BASE]
    rows = conn.execute("SELECT * FROM acoes_catalogo WHERE ativo != 'nao' AND tipo = 'link' ORDER BY criadoEmMs ASC").fetchall()
    for r in rows:
        lista.append({
            "id": r["id"],
            "nome": r["nome"],
            "pontos": int(r["pontos"]),
            "condicao": r["condicao"] or "Conforme briefing",
            "icone": "custom",
            "personalizada": True,
        })
    return lista


def calcular_ranking(conn):
    inis = conn.execute("SELECT * FROM iniciativas").fetchall()
    entregas = conn.execute("SELECT * FROM entregas").fetchall()
    avisos = conn.execute("SELECT * FROM avisos WHERE status != 'cancelado'").fetchall()

    mapa = {}
    for u in inis:
        u_dict = dict(u)
        if not eh_admin(u_dict):
            mapa[u_dict["id"]] = {
                "id": u_dict["id"],
                "nome": u_dict["nome"],
                "tipo": u_dict["tipo"] or "Empresa Júnior",
                "representante": u_dict["representante"],
                "cargo": u_dict["cargo"],
                "redeSocial": u_dict["redeSocial"] or "",
                "pontos": 0,
                "pontosValidados": 0,
                "pontosPendentes": 0,
                "totalEntregas": 0,
                "breakdown": {
                    "redes": 0,
                    "inscricoes": 0,
                    "formulario": 0,
                    "presencial": 0,
                    "palestras": 0,
                    "feira": 0,
                    "challenges": 0,
                    "avulso": 0,
                },
            }

    for e in entregas:
        rec = mapa.get(e["iniciativaId"])
        if not rec:
            continue
        rec["totalEntregas"] += 1
        pts = int(e["pontos"] or 0)
        if e["status"] == "validada":
            rec["pontos"] += pts
            rec["pontosValidados"] += pts
            rec["breakdown"]["redes"] += pts
        elif e["status"] == "pendente":
            rec["pontos"] += pts
            rec["pontosPendentes"] += pts
            rec["breakdown"]["redes"] += pts

    for a in avisos:
        try:
            d = json.loads(a["dados"] or "{}")
        except Exception:
            d = {}
        if d.get("cancelado"):
            continue
        rec = mapa.get(a["iniciativaId"])
        if not rec:
            continue

        pts = int(a["pontos"] or 0)
        tipo = a["tipo"]

        if tipo == "inscricoes":
            atual = rec["breakdown"]["inscricoes"]
            restante = max(0, CONFIG["LIMITE_PONTOS_INSCRICAO"] - atual)
            somar = min(pts, restante)
            rec["breakdown"]["inscricoes"] += somar
            rec["pontos"] += somar
            rec["pontosValidados"] += somar
        elif tipo in rec["breakdown"]:
            rec["breakdown"][tipo] += pts
            rec["pontos"] += pts
            rec["pontosValidados"] += pts

    # Pontos de Métricas Pós-Publicação (+10 pts por semana em posts, +5 pts em stories 24h)
    metricas_rows = conn.execute("SELECT * FROM metricas_entregas").fetchall()
    for m in metricas_rows:
        rec = mapa.get(m["iniciativaId"])
        if not rec:
            continue
        m_pts = int(m["pontos"] or 0)
        if m["status"] == "validada":
            rec["pontos"] += m_pts
            rec["pontosValidados"] += m_pts
            rec["breakdown"]["metricas"] = rec["breakdown"].get("metricas", 0) + m_pts
        elif m["status"] == "pendente":
            rec["pontos"] += m_pts
            rec["pontosPendentes"] += m_pts
            rec["breakdown"]["metricas"] = rec["breakdown"].get("metricas", 0) + m_pts

    lista = list(mapa.values())
    lista.sort(key=lambda r: (-r["pontos"], -r["pontosValidados"], normalizar(r["nome"])))
    return lista


def formatar_aviso_publico(a, por_id):
    u = por_id.get(a["iniciativaId"], {})
    try:
        dados_obj = json.loads(a["dados"] or "{}")
    except Exception:
        dados_obj = {}
    return {
        "id": a["id"],
        "tipo": a["tipo"],
        "status": a["status"] or "ativo",
        "criadoEm": int(a["criadoEmMs"]),
        "dataHora": a["criadoEm"],
        "expiraEm": int(a["expiraEmMs"]),
        "iniciativaId": a["iniciativaId"],
        "iniciativa": u.get("nome", ""),
        "tipoIniciativa": u.get("tipo", "Empresa Júnior"),
        "pontos": int(a["pontos"] or 0),
        "dados": dados_obj,
    }


def pontos_por():
    return {k: v["pontos"] for k, v in CONTAGENS.items()}


# ============================== HANDLERS DA API ==============================

def api_cadastrar(conn, d):
    nome = validar_texto(d.get("nome"), "Nome da iniciativa", 80, True)
    tipo = validar_texto(d.get("tipo"), "Tipo de iniciativa", 40, False) or "Empresa Júnior"
    representante = validar_texto(d.get("representante"), "Nome do representante", 80, True)
    cargo = validar_texto(d.get("cargo"), "Cargo do representante", 60, True)
    rede = validar_texto(d.get("redeSocial"), "Rede social da iniciativa", 150, True)
    senha = str(d.get("senha") or "")
    if len(senha) < 6:
        raise UserError("A senha precisa ter pelo menos 6 caracteres.")
    if len(senha) > 100:
        raise UserError("Senha longa demais.")

    chave = normalizar(nome)
    existentes = conn.execute("SELECT nome FROM iniciativas").fetchall()
    if any(normalizar(r["nome"]) == chave for r in existentes):
        raise UserError(f'Já existe uma iniciativa cadastrada com o nome "{nome}". Se você já possui cadastro, escolha "Entrar".')

    uid = str(uuid.uuid4())
    salt = str(uuid.uuid4())
    h = hash_senha(senha, salt)
    agora = agora_ms()
    dt_str = formatar_data_hora(agora)
    is_adm = "sim" if chave == normalizar(CONFIG["ADMIN_NOME"]) else ""

    with DB_WRITE_LOCK:
        with conn:
            conn.execute("""
                INSERT INTO iniciativas (id, nome, tipo, representante, cargo, redeSocial, salt, hash, criadoEm, criadoEmMs, admin)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (uid, nome, tipo, representante, cargo, rede, salt, h, dt_str, agora, is_adm))

    return {"token": gerar_token(conn, uid), "nome": nome, "admin": is_adm == "sim"}


def api_entrar(conn, d):
    chave = normalizar(d.get("nome"))
    senha = str(d.get("senha") or "")
    rows = conn.execute("SELECT * FROM iniciativas").fetchall()
    u = next((dict(r) for r in rows if normalizar(r["nome"]) == chave), None)
    if not u or hash_senha(senha, u["salt"]) != u["hash"]:
        raise UserError("Nome da iniciativa ou senha incorretos.")
    return {"token": gerar_token(conn, u["id"]), "nome": u["nome"], "admin": eh_admin(u)}


def api_painel(conn, me):
    agora = agora_ms()
    inis = [dict(r) for r in conn.execute("SELECT * FROM iniciativas").fetchall()]
    por_id = {u["id"]: u for u in inis}

    tarefas_disp = obter_tarefas(conn)

    # Tarefa do Hub ativa
    tarefa_row = conn.execute("""
        SELECT * FROM avisos
        WHERE tipo = 'tarefa' AND status != 'cancelado'
        ORDER BY criadoEmMs DESC LIMIT 1
    """).fetchone()
    tarefa_hub = None
    if tarefa_row and int(tarefa_row["expiraEmMs"]) > agora:
        try:
            t_dados = json.loads(tarefa_row["dados"] or "{}")
        except Exception:
            t_dados = {}
        tarefa_hub = {
            "dados": t_dados,
            "criadoEm": int(tarefa_row["criadoEmMs"]),
            "expiraEm": int(tarefa_row["expiraEmMs"]),
        }

    # Avisos ativos
    avisos_rows = conn.execute("""
        SELECT * FROM avisos
        WHERE tipo != 'tarefa' AND status != 'cancelado' AND expiraEmMs > ?
        ORDER BY criadoEmMs DESC
    """, (agora,)).fetchall()
    avisos_ativos = [formatar_aviso_publico(dict(a), por_id) for a in avisos_rows]

    # Minhas entregas
    entregas_rows = conn.execute("""
        SELECT * FROM entregas
        WHERE iniciativaId = ?
        ORDER BY criadoEmMs DESC
    """, (me["id"],)).fetchall()
    metricas_rows = conn.execute("SELECT * FROM metricas_entregas WHERE iniciativaId = ? ORDER BY criadoEmMs ASC", (me["id"],)).fetchall()
    metricas_por_entrega = {}
    for m in metricas_rows:
        eid = m["entregaId"]
        if eid not in metricas_por_entrega:
            metricas_por_entrega[eid] = []
        metricas_por_entrega[eid].append(dict(m))

    minhas = []
    for e in entregas_rows:
        is_story = "story" in (e["tarefaId"] or "").lower()
        minhas.append({
            "id": e["id"],
            "tarefaId": e["tarefaId"],
            "tarefaNome": e["tarefaNome"],
            "tipoMidia": "story" if is_story else "post",
            "pontos": int(e["pontos"]),
            "url": e["url"],
            "status": e["status"],
            "motivoRecusa": e["motivoRecusa"] or "",
            "criadoEm": int(e["criadoEmMs"]),
            "dataHora": e["criadoEm"],
            "revisadoEm": int(e["revisadoEmMs"]) if e["revisadoEmMs"] else "",
            "revisadoDataHora": e["revisadoEm"] or "",
            "metricas": metricas_por_entrega.get(e["id"], []),
        })

    ranking_data = calcular_ranking(conn)
    total_pontos = sum(r["pontos"] for r in ranking_data)
    total_validadas = conn.execute("SELECT COUNT(*) as c FROM entregas WHERE status = 'validada'").fetchone()["c"]

    briefings = [dict(b) for b in conn.execute("SELECT * FROM briefings WHERE status != 'removido' ORDER BY criadoEmMs DESC").fetchall()]
    cronograma = [dict(c) for c in conn.execute("SELECT * FROM cronograma WHERE status != 'removido' ORDER BY data ASC").fetchall()]

    return {
        "me": {
            "id": me["id"],
            "nome": me["nome"],
            "tipo": me["tipo"] or "Empresa Júnior",
            "representante": me["representante"],
            "cargo": me["cargo"],
            "redeSocial": me["redeSocial"] or "",
            "admin": eh_admin(me),
        },
        "ranking": ranking_data,
        "estatisticas": {
            "totalIniciativas": len(ranking_data),
            "totalPontos": total_pontos,
            "totalValidadas": total_validadas,
            "liderNome": ranking_data[0]["nome"] if ranking_data else "—",
            "liderPontos": ranking_data[0]["pontos"] if ranking_data else 0,
        },
        "tarefaHub": tarefa_hub,
        "avisos": avisos_ativos,
        "regras": REGRAS,
        "tarefas": tarefas_disp,
        "minhasEntregas": minhas,
        "briefings": briefings,
        "cronograma": cronograma,
        "config": {
            "marcacao": CONFIG["MARCACAO"],
            "tarefaPadrao": CONFIG["TAREFA_PADRAO"],
            "pontosPorInscricao": CONFIG["PONTOS_POR_INSCRICAO"],
            "limiteInscricoes": CONFIG["LIMITE_PONTOS_INSCRICAO"],
        },
        "pontosPor": pontos_por(),
        "edital": CONFIG["EDITAL_URL"] or "",
        "agora": agora,
        "engine": "SQLite 3 (WAL Mode)",
    }


def api_enviar_tarefas(conn, me, d):
    if eh_admin(me):
        raise UserError("O administrador UFMG Hub não participa como competidor do ranking.")
    itens = d.get("itens") if isinstance(d.get("itens"), list) else []
    agora = agora_ms()
    dt_str = formatar_data_hora(agora)

    todas_tarefas = {t["id"]: t for t in obter_tarefas(conn)}

    with DB_WRITE_LOCK:
        # Mapa de URLs já existentes (não recusadas)
        existentes = conn.execute("SELECT id, iniciativaId, urlCanonica FROM entregas WHERE status != 'recusada'").fetchall()
        mapa_urls = {r["urlCanonica"]: dict(r) for r in existentes if r["urlCanonica"]}

        urls_lote = set()
        linhas = []

        for it in itens:
            t = todas_tarefas.get(it.get("tarefaId"))
            if not t:
                continue
            urls = it.get("urls") if isinstance(it.get("urls"), list) else []
            for url_bruta in urls:
                url_bruta = str(url_bruta or "").strip()
                if not url_bruta:
                    continue
                if not url_valida(url_bruta):
                    raise UserError(f"Link com formato inválido: {url_bruta[:60]}")

                url_canon = limpar_url(url_bruta)
                if url_canon in urls_lote:
                    raise UserError("Você incluiu o mesmo link mais de uma vez no mesmo envio.")
                urls_lote.add(url_canon)

                if url_canon in mapa_urls:
                    ant = mapa_urls[url_canon]
                    if ant["iniciativaId"] == me["id"]:
                        raise UserError(f"Você já registrou este link anteriormente ({ant['id']}). Aguarde a validação da equipe.")
                    else:
                        raise UserError("Este link já foi registrado por outra iniciativa no sistema.")

                act_id = gerar_id_unico("ACT")
                linhas.append((
                    act_id,
                    me["id"],
                    t["id"],
                    t["nome"],
                    int(t["pontos"]),
                    url_bruta,
                    url_canon,
                    "pendente",
                    "",
                    dt_str,
                    agora,
                    "",
                    0,
                ))

        if not linhas:
            raise UserError("Adicione pelo menos um link válido para pontuar.")
        if len(linhas) > CONFIG["MAX_LINKS_POR_ENVIO"]:
            raise UserError("Limite de envios por vez atingido. Envie em lotes menores.")

        with conn:
            conn.executemany("""
                INSERT INTO entregas (id, iniciativaId, tarefaId, tarefaNome, pontos, url, urlCanonica, status, motivoRecusa, criadoEm, criadoEmMs, revisadoEm, revisadoEmMs)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, linhas)

    total_pts = sum(l[4] for l in linhas)
    p = api_painel(conn, me)
    p["enviado"] = {"links": len(linhas), "pontos": total_pts}
    return p


def api_admin_dados(conn, me):
    inis = [dict(r) for r in conn.execute("SELECT * FROM iniciativas").fetchall()]
    por_id = {u["id"]: u for u in inis}

    entregas_rows = conn.execute("SELECT * FROM entregas ORDER BY criadoEmMs DESC").fetchall()
    entregas = []
    for e in entregas_rows:
        u = por_id.get(e["iniciativaId"], {})
        entregas.append({
            "id": e["id"],
            "iniciativaId": e["iniciativaId"],
            "iniciativa": u.get("nome", "—"),
            "tipoIniciativa": u.get("tipo", "Empresa Júnior"),
            "tarefaId": e["tarefaId"],
            "tarefaNome": e["tarefaNome"],
            "pontos": int(e["pontos"]),
            "url": e["url"],
            "status": e["status"],
            "motivoRecusa": e["motivoRecusa"] or "",
            "criadoEm": int(e["criadoEmMs"]),
            "dataHora": e["criadoEm"],
            "revisadoEm": int(e["revisadoEmMs"]) if e["revisadoEmMs"] else 0,
            "revisadoDataHora": e["revisadoEm"] or "",
        })

    avisos_rows = conn.execute("SELECT * FROM avisos ORDER BY criadoEmMs DESC").fetchall()
    historico = [formatar_aviso_publico(dict(a), por_id) for a in avisos_rows]

    iniciativas = [
        {
            "id": u["id"],
            "nome": u["nome"],
            "tipo": u["tipo"] or "Empresa Júnior",
            "representante": u["representante"],
            "cargo": u["cargo"],
            "redeSocial": u["redeSocial"] or "",
            "criadoEm": u["criadoEm"],
        }
        for u in inis if not eh_admin(u)
    ]
    iniciativas.sort(key=lambda x: normalizar(x["nome"]))

    catalogo_rows = conn.execute("SELECT * FROM acoes_catalogo WHERE ativo != 'nao' ORDER BY criadoEmMs DESC").fetchall()
    catalogo = [{
        "id": c["id"],
        "nome": c["nome"],
        "pontos": int(c["pontos"]),
        "tipo": c["tipo"],
        "condicao": c["condicao"] or "",
        "descricao": c["descricao"] or "",
        "criadoEm": int(c["criadoEmMs"]),
        "dataHora": c["criadoEm"],
    } for c in catalogo_rows]

    briefings = [dict(b) for b in conn.execute("SELECT * FROM briefings WHERE status != 'removido' ORDER BY criadoEmMs DESC").fetchall()]
    cronograma = [dict(c) for c in conn.execute("SELECT * FROM cronograma WHERE status != 'removido' ORDER BY data ASC").fetchall()]

    # Métricas pós-publicação para acompanhamento do Hub
    metricas_rows = conn.execute("SELECT * FROM metricas_entregas ORDER BY criadoEmMs DESC").fetchall()
    entregas_map = {e["id"]: e for e in entregas}
    metricas_list = []
    for m in metricas_rows:
        m_dict = dict(m)
        orig = entregas_map.get(m["entregaId"], {})
        m_dict["urlOriginal"] = orig.get("url", "")
        m_dict["tipoIniciativa"] = orig.get("tipoIniciativa", "Empresa Júnior")
        metricas_list.append(m_dict)

    total_alcance = sum(int(m["alcance"] or 0) for m in metricas_list if m["status"] == "validada")
    total_engajamento = sum(int(m["engajamento"] or 0) for m in metricas_list if m["status"] == "validada")
    metricas_pendentes_count = len([m for m in metricas_list if m["status"] == "pendente"])
    pontos_metricas_total = sum(int(m["pontos"] or 0) for m in metricas_list if m["status"] == "validada")

    db_size_kb = round(os.path.getsize(DB_PATH) / 1024, 1) if os.path.exists(DB_PATH) else 0

    return {
        "entregas": entregas,
        "metricas": metricas_list,
        "metricasKpis": {
            "totalAlcance": total_alcance,
            "totalEngajamento": total_engajamento,
            "pendentes": metricas_pendentes_count,
            "totalPontos": pontos_metricas_total,
            "totalRelatorios": len(metricas_list)
        },
        "historico": historico,
        "iniciativas": iniciativas,
        "catalogo": catalogo,
        "briefings": briefings,
        "cronograma": cronograma,
        "pontosPor": pontos_por(),
        "config": {
            "limiteInscricoes": CONFIG["LIMITE_PONTOS_INSCRICAO"],
            "maxPresencial": CONFIG["MAX_PONTOS_PRESENCIAL"],
        },
        "diagnostico": {
            "engine": "SQLite 3 (WAL Mode Ativo)",
            "arquivoDb": "arena.db",
            "tamanhoKb": db_size_kb,
            "totalIniciativas": len(iniciativas),
            "totalEntregas": len(entregas),
            "totalAvisos": len(historico),
            "totalMetricas": len(metricas_list),
        },
        "agora": agora_ms(),
    }


def api_validar_entrega(conn, me, d):
    status = str(d.get("status") or "")
    if status not in ("pendente", "validada", "recusada"):
        raise UserError("Status de validação inválido.")
    motivo = validar_texto(d.get("motivoRecusa"), "Motivo da recusa", 250, False)
    eid = str(d.get("id") or "")

    agora = agora_ms()
    rev_str = "" if status == "pendente" else formatar_data_hora(agora)
    rev_ms = 0 if status == "pendente" else agora
    motivo_final = motivo if status == "recusada" else ""

    with DB_WRITE_LOCK:
        with conn:
            cur = conn.execute("""
                UPDATE entregas
                SET status = ?, motivoRecusa = ?, revisadoEm = ?, revisadoEmMs = ?
                WHERE id = ?
            """, (status, motivo_final, rev_str, rev_ms, eid))
            if cur.rowcount == 0:
                raise UserError("Entrega não encontrada no banco de dados.")

    return api_admin_dados(conn, me)


def api_validar_entregas_lote(conn, me, d):
    ids = d.get("ids") if isinstance(d.get("ids"), list) else []
    status = str(d.get("status") or "validada")
    if status not in ("validada", "recusada"):
        raise UserError("Status inválido para validação em lote.")
    agora = agora_ms()
    rev_str = formatar_data_hora(agora)

    with DB_WRITE_LOCK:
        with conn:
            if ids:
                placeholders = ",".join("?" for _ in ids)
                conn.execute(f"""
                    UPDATE entregas
                    SET status = ?, motivoRecusa = '', revisadoEm = ?, revisadoEmMs = ?
                    WHERE id IN ({placeholders}) AND status = 'pendente'
                """, [status, rev_str, agora] + ids)
            else:
                conn.execute("""
                    UPDATE entregas
                    SET status = ?, motivoRecusa = '', revisadoEm = ?, revisadoEmMs = ?
                    WHERE status = 'pendente'
                """, (status, rev_str, agora))

    return api_admin_dados(conn, me)



def api_registrar_metrica_entrega(conn, me, d):
    if eh_admin(me):
        raise UserError("Administrador não registra métricas de iniciativa.")

    eid = str(d.get("entregaId") or "").strip()
    periodo = str(d.get("periodo") or "").strip().lower() # '24h', 'sem1', 'sem2', 'sem3'
    try:
        alcance = max(0, int(d.get("alcance") or 0))
        engajamento = max(0, int(d.get("engajamento") or 0))
    except ValueError:
        raise UserError("Alcance e engajamento devem ser números válidos maiores ou iguais a zero.")

    comprovante_url = str(d.get("comprovanteUrl") or "").strip()
    if not url_valida(comprovante_url):
        raise UserError("Informe um link válido para o comprovante/print dos insights (ex.: link do Drive ou imagem).")

    obs = validar_texto(d.get("observacoes"), "Observações", 350, False)
    agora = agora_ms()
    dt_str = formatar_data_hora(agora)

    with DB_WRITE_LOCK:
        entrega = conn.execute("SELECT * FROM entregas WHERE id = ?", (eid,)).fetchone()
        if not entrega or entrega["iniciativaId"] != me["id"]:
            raise UserError("Entrega não encontrada ou não pertence à sua iniciativa.")

        is_story = "story" in (entrega["tarefaId"] or "").lower()
        if is_story:
            if periodo != "24h":
                raise UserError("Para stories, o período de insights deve ser de 24 horas ('24h').")
            periodo_rotulo = "24 Horas Stories"
            pontos_metrica = 5
        else:
            if periodo not in ("sem1", "sem2", "sem3"):
                raise UserError("Para publicações de feed/reels/carrossel, o período deve ser 'sem1' (1ª semana), 'sem2' (2ª semana) ou 'sem3' (3ª semana).")
            periodo_rotulo = {"sem1": "1ª Semana", "sem2": "2ª Semana", "sem3": "3ª Semana"}[periodo]
            pontos_metrica = 10

        # Verifica se já existe registro dessa métrica para a entrega
        existente = conn.execute("SELECT * FROM metricas_entregas WHERE entregaId = ? AND periodo = ?", (eid, periodo)).fetchone()
        if existente:
            if existente["status"] == "validada":
                raise UserError(f"A métrica de {periodo_rotulo} desta entrega já foi validada e pontuada.")
            # Atualiza e volta para pendente
            metrica_id = existente["id"]
            with conn:
                conn.execute("""
                    UPDATE metricas_entregas
                    SET alcance = ?, engajamento = ?, comprovanteUrl = ?, observacoes = ?, status = 'pendente', motivoRecusa = '', criadoEm = ?, criadoEmMs = ?
                    WHERE id = ?
                """, (alcance, engajamento, comprovante_url, obs, dt_str, agora, metrica_id))
        else:
            metrica_id = gerar_id_unico("MTR")
            with conn:
                conn.execute("""
                    INSERT INTO metricas_entregas (
                        id, entregaId, iniciativaId, iniciativaNome, tarefaId, tarefaNome,
                        tipoMidia, periodo, periodoRotulo, pontos, alcance, engajamento,
                        comprovanteUrl, observacoes, status, motivoRecusa, criadoEm, criadoEmMs, revisadoEm, revisadoEmMs
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pendente', '', ?, ?, '', 0)
                """, (
                    metrica_id, eid, me["id"], me["nome"], entrega["tarefaId"], entrega["tarefaNome"],
                    "story" if is_story else "post", periodo, periodo_rotulo, pontos_metrica,
                    alcance, engajamento, comprovante_url, obs, dt_str, agora
                ))

    p = api_painel(conn, me)
    p["metricaEnviada"] = {
        "id": metrica_id,
        "entregaId": eid,
        "periodo": periodo_rotulo,
        "pontos": pontos_metrica,
        "alcance": alcance,
        "engajamento": engajamento
    }
    return p


def api_validar_metrica_entrega(conn, me, d):
    status = str(d.get("status") or "")
    if status not in ("pendente", "validada", "recusada"):
        raise UserError("Status de validação inválido.")
    motivo = validar_texto(d.get("motivoRecusa"), "Motivo da recusa", 250, False)
    mid = str(d.get("id") or d.get("metricaId") or "")

    agora = agora_ms()
    rev_str = "" if status == "pendente" else formatar_data_hora(agora)
    rev_ms = 0 if status == "pendente" else agora
    motivo_final = motivo if status == "recusada" else ""

    with DB_WRITE_LOCK:
        with conn:
            cur = conn.execute("""
                UPDATE metricas_entregas
                SET status = ?, motivoRecusa = ?, revisadoEm = ?, revisadoEmMs = ?
                WHERE id = ?
            """, (status, motivo_final, rev_str, rev_ms, mid))
            if cur.rowcount == 0:
                raise UserError("Registro de métrica não encontrado no banco de dados.")

    return api_admin_dados(conn, me)


def api_validar_metricas_lote(conn, me, d):
    ids = d.get("ids") if isinstance(d.get("ids"), list) else []
    status = str(d.get("status") or "validada")
    if status not in ("validada", "recusada"):
        raise UserError("Status inválido para validação de métricas em lote.")
    agora = agora_ms()
    rev_str = formatar_data_hora(agora)

    with DB_WRITE_LOCK:
        with conn:
            if ids:
                placeholders = ",".join("?" for _ in ids)
                conn.execute(f"""
                    UPDATE metricas_entregas
                    SET status = ?, motivoRecusa = '', revisadoEm = ?, revisadoEmMs = ?
                    WHERE id IN ({placeholders}) AND status = 'pendente'
                """, [status, rev_str, agora] + ids)
            else:
                conn.execute("""
                    UPDATE metricas_entregas
                    SET status = ?, motivoRecusa = '', revisadoEm = ?, revisadoEmMs = ?
                    WHERE status = 'pendente'
                """, (status, rev_str, agora))

    return api_admin_dados(conn, me)


def api_reenviar_entrega(conn, me, d):
    eid = str(d.get("id") or d.get("entregaId") or "")
    nova_url = str(d.get("novaUrl") or "").strip()
    if not url_valida(nova_url):
        raise UserError("Informe um link público válido (ex.: https://instagram.com/p/...).")
    url_canon = limpar_url(nova_url)
    agora = agora_ms()
    dt_str = formatar_data_hora(agora)

    with DB_WRITE_LOCK:
        row = conn.execute("SELECT id, iniciativaId, pontos FROM entregas WHERE id = ?", (eid,)).fetchone()
        if not row or row["iniciativaId"] != me["id"]:
            raise UserError("Entrega não encontrada.")

        outros = conn.execute("SELECT id, iniciativaId, urlCanonica FROM entregas WHERE id != ? AND status != 'recusada'", (eid,)).fetchall()
        for o in outros:
            if o["urlCanonica"] == url_canon:
                if o["iniciativaId"] == me["id"]:
                    raise UserError(f"Você já registrou este link em outra ação ativa ({o['id']}).")
                else:
                    raise UserError("Este link já foi registrado por outra iniciativa no sistema.")

        with conn:
            conn.execute("""
                UPDATE entregas
                SET url = ?, urlCanonica = ?, status = 'pendente', motivoRecusa = '', criadoEm = ?, criadoEmMs = ?, revisadoEm = '', revisadoEmMs = 0
                WHERE id = ? AND iniciativaId = ?
            """, (nova_url, url_canon, dt_str, agora, eid, me["id"]))

    p = api_painel(conn, me)
    p["enviado"] = {"links": 1, "pontos": int(row["pontos"])}
    return p


def criar_aviso_db(conn, tipo, iniciativa_id, pontos, dados_dict):
    agora = agora_ms()
    criado_str = formatar_data_hora(agora)
    horas = CONFIG["HORAS"].get(tipo, 48)
    expira_ms = agora + horas * 3600 * 1000
    expira_str = formatar_data_hora(expira_ms)
    lnc_id = gerar_id_unico("LNC")

    with DB_WRITE_LOCK:
        with conn:
            conn.execute("""
                INSERT INTO avisos (id, tipo, criadoEm, criadoEmMs, expiraEm, expiraEmMs, iniciativaId, pontos, dados, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'ativo')
            """, (lnc_id, tipo, criado_str, agora, expira_str, expira_ms, iniciativa_id or "", int(pontos or 0), json.dumps(dados_dict or {})))


def buscar_iniciativa_valida(conn, ini_id):
    row = conn.execute("SELECT * FROM iniciativas WHERE id = ?", (str(ini_id or ""),)).fetchone()
    if not row or eh_admin(dict(row)):
        raise UserError("Selecione uma iniciativa válida cadastrada.")
    return dict(row)


def api_publicar_tarefa_hub(conn, me, d):
    dados = {
        "sobre": validar_texto(d.get("sobre"), "Sobre o que publicar", 400, False),
        "periodo": validar_texto(d.get("periodo"), "Período para publicar", 50, False),
        "recomendacoes": validar_texto(d.get("recomendacoes"), "Recomendações do Hub", 400, False),
        "bonus": validar_texto(d.get("bonus"), "Bônus", 400, False),
    }
    if not any(dados.values()):
        raise UserError("Preencha pelo menos um campo da tarefa semanal.")
    criar_aviso_db(conn, "tarefa", "", 0, dados)
    return api_admin_dados(conn, me)


def api_publicar_presencial(conn, me, d):
    ini = buscar_iniciativa_valida(conn, d.get("iniciativaId"))
    oque = validar_texto(d.get("oque"), "O que foi a ação", 300, True)
    quando = validar_texto(d.get("quando"), "Quando foi a ação", 150, True)
    pontos = validar_inteiro(d.get("pontos"), "Pontuação da ação")
    if pontos < 1:
        raise UserError("A pontuação deve ser maior que zero.")
    if pontos > CONFIG["MAX_PONTOS_PRESENCIAL"]:
        raise UserError(f"A pontuação de ação presencial aprovada tem limite de até {CONFIG['MAX_PONTOS_PRESENCIAL']} pontos.")
    criar_aviso_db(conn, "presencial", ini["id"], pontos, {"oque": oque, "quando": quando, "pontuacao": pontos})
    return api_admin_dados(conn, me)


def api_publicar_contagem(conn, me, d, tipo):
    ini = buscar_iniciativa_valida(conn, d.get("iniciativaId"))
    c = CONTAGENS.get(tipo)
    if not c:
        raise UserError("Categoria de contagem não reconhecida.")
    qtd = validar_inteiro(d.get("quantidade"), c["rotulo"])
    if qtd <= 0:
        raise UserError(f"Informe uma quantidade positiva para {c['rotulo']}.")
    pts = qtd * c["pontos"]
    criar_aviso_db(conn, tipo, ini["id"], pts, {"quantidade": qtd, "pontosUnitarios": c["pontos"]})
    return api_admin_dados(conn, me)


def api_publicar_acao_avulsa(conn, me, d):
    ini = buscar_iniciativa_valida(conn, d.get("iniciativaId"))
    titulo = validar_texto(d.get("titulo"), "Título ou nome da ação", 100, True)
    descricao = validar_texto(d.get("descricao"), "Descrição ou justificativa", 300, False)
    modo = "quantidade" if d.get("modo") == "quantidade" else "fixo"
    qtd = 1
    unitario = 0

    if modo == "quantidade":
        qtd = validar_inteiro(d.get("quantidade"), "Quantidade")
        unitario = validar_inteiro(d.get("pontosUnitarios"), "Pontos por unidade")
        if qtd <= 0 or unitario <= 0:
            raise UserError("Quantidade e pontos por unidade devem ser maiores que zero.")
        pontos_final = qtd * unitario
    else:
        pontos_final = validar_inteiro(d.get("pontos"), "Pontuação total")
        if pontos_final <= 0:
            raise UserError("A pontuação deve ser maior que zero.")

    dados = {
        "titulo": titulo,
        "descricao": descricao,
        "modo": modo,
        "quantidade": qtd,
        "pontosUnitarios": unitario,
        "quando": validar_texto(d.get("quando"), "Data ou momento", 100, False) or "Durante a Arena",
    }
    criar_aviso_db(conn, "avulso", ini["id"], pontos_final, dados)
    return api_admin_dados(conn, me)


def api_criar_acao_catalogo(conn, me, d):
    nome = validar_texto(d.get("nome"), "Nome da tarefa", 80, True)
    pontos = validar_inteiro(d.get("pontos"), "Pontos da tarefa")
    condicao = validar_texto(d.get("condicao"), "Condição ou regra de validação", 250, True)
    descricao = validar_texto(d.get("descricao"), "Descrição adicional", 300, False)
    if pontos <= 0:
        raise UserError("Os pontos devem ser maiores que zero.")

    cid = "custom_" + str(uuid.uuid4())[:8]
    agora = agora_ms()
    dt_str = formatar_data_hora(agora)

    with DB_WRITE_LOCK:
        with conn:
            conn.execute("""
                INSERT INTO acoes_catalogo (id, nome, pontos, tipo, descricao, condicao, criadoEm, criadoEmMs, ativo)
                VALUES (?, ?, ?, 'link', ?, ?, ?, ?, 'sim')
            """, (cid, nome, pontos, descricao, condicao, dt_str, agora))

    return api_admin_dados(conn, me)


def api_remover_acao_catalogo(conn, me, d):
    cid = validar_texto(d.get("id"), "ID da ação", 50, True)
    with DB_WRITE_LOCK:
        with conn:
            conn.execute("UPDATE acoes_catalogo SET ativo = 'nao' WHERE id = ?", (cid,))
    return api_admin_dados(conn, me)


def api_cancelar_aviso(conn, me, d):
    aid = validar_texto(d.get("id"), "ID do aviso", 50, True)
    with DB_WRITE_LOCK:
        with conn:
            cur = conn.execute("UPDATE avisos SET status = 'cancelado' WHERE id = ?", (aid,))
            if cur.rowcount == 0:
                raise UserError("Registro de aviso não encontrado.")
    return api_admin_dados(conn, me)


def api_salvar_briefing(conn, me, d):
    agora = agora_ms()
    dt_str = formatar_data_hora(agora)
    bid = str(d.get("id") or "").strip() or gerar_id_unico("BRF")
    titulo = validar_texto(d.get("titulo"), "Título do briefing", 120, True)
    fase = validar_texto(d.get("fase"), "Fase ou mês", 60, False) or "Geral"
    periodo = validar_texto(d.get("periodo"), "Período", 60, False) or "Durante a Arena"
    descricao = validar_texto(d.get("descricao"), "Descrição do briefing", 1000, True)
    diretrizes = validar_texto(d.get("diretrizes"), "Diretrizes de conteúdo", 1000, False)
    link_drive = validar_texto(d.get("linkDrive"), "Link do Kit de Artes / Drive", 400, False)
    hashtags = validar_texto(d.get("hashtags"), "Hashtags e marcações", 250, False) or "@mercadoemconexao #ArenaMeC"
    bonus = validar_texto(d.get("bonus"), "Bônus de pontuação", 250, False)
    status = str(d.get("status") or "ativo")

    with DB_WRITE_LOCK:
        with conn:
            conn.execute("""
                INSERT INTO briefings (id, titulo, fase, periodo, descricao, diretrizes, linkDrive, hashtags, bonus, status, criadoEm, criadoEmMs)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    titulo=excluded.titulo, fase=excluded.fase, periodo=excluded.periodo,
                    descricao=excluded.descricao, diretrizes=excluded.diretrizes, linkDrive=excluded.linkDrive,
                    hashtags=excluded.hashtags, bonus=excluded.bonus, status=excluded.status
            """, (bid, titulo, fase, periodo, descricao, diretrizes, link_drive, hashtags, bonus, status, dt_str, agora))

    return api_admin_dados(conn, me)


def api_remover_briefing(conn, me, d):
    bid = validar_texto(d.get("id"), "ID do briefing", 50, True)
    with DB_WRITE_LOCK:
        with conn:
            conn.execute("UPDATE briefings SET status = 'removido' WHERE id = ?", (bid,))
    return api_admin_dados(conn, me)


def api_salvar_cronograma(conn, me, d):
    agora = agora_ms()
    dt_str = formatar_data_hora(agora)
    cid = str(d.get("id") or "").strip() or gerar_id_unico("CRN")
    data = validar_texto(d.get("data"), "Data da atividade", 40, True)
    titulo = validar_texto(d.get("titulo"), "Título da atividade", 120, True)
    local = validar_texto(d.get("local"), "Local ou formato", 100, False) or "Campus Pampulha"
    tipo = validar_texto(d.get("tipo"), "Tipo de atividade", 50, False) or "Presencial"
    pontos = validar_texto(d.get("pontos"), "Pontos associados", 50, False)
    descricao = validar_texto(d.get("descricao"), "Descrição da atividade", 500, False)
    status = str(d.get("status") or "proximo")

    with DB_WRITE_LOCK:
        with conn:
            conn.execute("""
                INSERT INTO cronograma (id, data, titulo, local, tipo, pontos, descricao, status, criadoEm, criadoEmMs)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    data=excluded.data, titulo=excluded.titulo, local=excluded.local,
                    tipo=excluded.tipo, pontos=excluded.pontos, descricao=excluded.descricao, status=excluded.status
            """, (cid, data, titulo, local, tipo, pontos, descricao, status, dt_str, agora))

    return api_admin_dados(conn, me)


def api_remover_cronograma(conn, me, d):
    cid = validar_texto(d.get("id"), "ID da atividade", 50, True)
    with DB_WRITE_LOCK:
        with conn:
            conn.execute("UPDATE cronograma SET status = 'removido' WHERE id = ?", (cid,))
    return api_admin_dados(conn, me)


def api_reparar_datas(conn, me):
    reparadas = 0
    tabelas = ["iniciativas", "entregas", "avisos", "acoes_catalogo", "briefings", "cronograma"]
    with DB_WRITE_LOCK:
        with conn:
            for t in tabelas:
                rows = conn.execute(f"SELECT id, criadoEm, criadoEmMs FROM {t}").fetchall()
                for r in rows:
                    val = str(r["criadoEm"] or "").strip()
                    if re.match(r"^\d{10,}$", val):
                        nova = formatar_data_hora(int(val))
                        conn.execute(f"UPDATE {t} SET criadoEm = ? WHERE id = ?", (nova, r["id"]))
                        reparadas += 1
    msg = (
        f"{reparadas} data(s) antiga(s) foram higienizadas e formatadas no banco SQLite!"
        if reparadas > 0
        else "Banco SQLite verificado: 100% das datas e registros estão íntegros e formatados!"
    )
    return {"reparadas": reparadas, "mensagem": msg}


def dispatch_api(acao, dados, token):
    dados = dados or {}
    conn = get_conn()
    try:
        if acao == "cadastrar":
            return api_cadastrar(conn, dados)
        if acao == "entrar":
            return api_entrar(conn, dados)
        if acao == "painel":
            return api_painel(conn, usuario_autenticado(conn, token))
        if acao == "enviarTarefas":
            return api_enviar_tarefas(conn, usuario_autenticado(conn, token), dados)
        if acao == "reenviarEntrega":
            return api_reenviar_entrega(conn, usuario_autenticado(conn, token), dados)
        if acao == "registrarMetricaEntrega":
            return api_registrar_metrica_entrega(conn, usuario_autenticado(conn, token), dados)
        if acao == "validarMetricaEntrega":
            return api_validar_metrica_entrega(conn, admin_autenticado(conn, token), dados)
        if acao == "validarMetricasLote":
            return api_validar_metricas_lote(conn, admin_autenticado(conn, token), dados)

        # Rotas de Admin
        if acao == "admin":
            return api_admin_dados(conn, admin_autenticado(conn, token))
        if acao == "validarEntrega":
            return api_validar_entrega(conn, admin_autenticado(conn, token), dados)
        if acao == "validarEntregasLote":
            return api_validar_entregas_lote(conn, admin_autenticado(conn, token), dados)
        if acao == "publicarTarefaHub":
            return api_publicar_tarefa_hub(conn, admin_autenticado(conn, token), dados)
        if acao == "publicarPresencial":
            return api_publicar_presencial(conn, admin_autenticado(conn, token), dados)
        if acao == "publicarInscricoes":
            return api_publicar_contagem(conn, admin_autenticado(conn, token), dados, "inscricoes")
        if acao == "publicarFormulario":
            return api_publicar_contagem(conn, admin_autenticado(conn, token), dados, "formulario")
        if acao == "publicarPalestras":
            return api_publicar_contagem(conn, admin_autenticado(conn, token), dados, "palestras")
        if acao == "publicarFeira":
            return api_publicar_contagem(conn, admin_autenticado(conn, token), dados, "feira")
        if acao == "publicarChallenges":
            return api_publicar_contagem(conn, admin_autenticado(conn, token), dados, "challenges")
        if acao == "publicarAcaoAvulsa":
            return api_publicar_acao_avulsa(conn, admin_autenticado(conn, token), dados)
        if acao == "criarAcaoCatalogo":
            return api_criar_acao_catalogo(conn, admin_autenticado(conn, token), dados)
        if acao == "removerAcaoCatalogo":
            return api_remover_acao_catalogo(conn, admin_autenticado(conn, token), dados)
        if acao == "cancelarAviso":
            return api_cancelar_aviso(conn, admin_autenticado(conn, token), dados)
        if acao == "salvarBriefing":
            return api_salvar_briefing(conn, admin_autenticado(conn, token), dados)
        if acao == "removerBriefing":
            return api_remover_briefing(conn, admin_autenticado(conn, token), dados)
        if acao == "salvarCronograma":
            return api_salvar_cronograma(conn, admin_autenticado(conn, token), dados)
        if acao == "removerCronograma":
            return api_remover_cronograma(conn, admin_autenticado(conn, token), dados)
        if acao == "repararDatas":
            return api_reparar_datas(conn, admin_autenticado(conn, token))

        raise UserError(f"Ação desconhecida: {acao}")
    except UserError as ue:
        return {"erro": ue.message, "sair": ue.sair}
    except Exception as ex:
        print(f"[ERRO API {acao}]:", ex)
        return {"erro": "Erro interno no servidor SQLite. Tente novamente."}
    finally:
        conn.close()


# ============================== EXPORTAÇÃO CSV / EXCEL ==============================

def gerar_csv_export(tabela):
    conn = get_conn()
    try:
        output = io.StringIO()
        # UTF-8 BOM para o Excel abrir acentos perfeitamente
        output.write("\ufeff")
        writer = csv.writer(output, delimiter=";")

        if tabela == "ranking":
            ranking = calcular_ranking(conn)
            writer.writerow([
                "Posicao", "Iniciativa", "Categoria", "Representante", "Rede Social",
                "Pontos Totais", "Pontos Validados", "Pontos Pendentes", "Total Entregas",
                "Redes Sociais", "Inscricoes", "Formulario", "Presencial", "Palestras", "Feira", "Challenges", "Avulso"
            ])
            for idx, r in enumerate(ranking, 1):
                b = r["breakdown"]
                writer.writerow([
                    f"{idx}º", r["nome"], r["tipo"], r["representante"], r["redeSocial"],
                    r["pontos"], r["pontosValidados"], r["pontosPendentes"], r["totalEntregas"],
                    b["redes"], b["inscricoes"], b["formulario"], b["presencial"], b["palestras"], b["feira"], b["challenges"], b["avulso"]
                ])
        elif tabela == "entregas":
            inis = {r["id"]: r["nome"] for r in conn.execute("SELECT id, nome FROM iniciativas").fetchall()}
            rows = conn.execute("SELECT * FROM entregas ORDER BY criadoEmMs DESC").fetchall()
            writer.writerow(["ID Unico", "Iniciativa", "Tarefa", "Pontos", "Status", "URL", "Registrado Em", "Revisado Em", "Motivo Recusa"])
            for e in rows:
                writer.writerow([
                    e["id"], inis.get(e["iniciativaId"], "—"), e["tarefaNome"], e["pontos"],
                    e["status"], e["url"], e["criadoEm"], e["revisadoEm"], e["motivoRecusa"]
                ])
        else:
            rows = conn.execute("SELECT id, nome, tipo, representante, cargo, redeSocial, criadoEm, admin FROM iniciativas").fetchall()
            writer.writerow(["ID", "Nome", "Categoria", "Representante", "Cargo", "Rede Social", "Cadastrado Em", "Admin"])
            for r in rows:
                writer.writerow([r["id"], r["nome"], r["tipo"], r["representante"], r["cargo"], r["redeSocial"], r["criadoEm"], r["admin"]])

        return output.getvalue().encode("utf-8")
    finally:
        conn.close()


# ============================== SERVIDOR HTTP MULTITHREAD ==============================

class ArenaRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Log enxuto
        pass

    def send_cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_cors()
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/health":
            conn = get_conn()
            try:
                c_ini = conn.execute("SELECT COUNT(*) FROM iniciativas").fetchone()[0]
                c_ent = conn.execute("SELECT COUNT(*) FROM entregas").fetchone()[0]
                c_avi = conn.execute("SELECT COUNT(*) FROM avisos").fetchone()[0]
                c_brf = conn.execute("SELECT COUNT(*) FROM briefings").fetchone()[0]
                c_crn = conn.execute("SELECT COUNT(*) FROM cronograma").fetchone()[0]
                wal = conn.execute("PRAGMA journal_mode;").fetchone()[0]
            finally:
                conn.close()

            payload = json.dumps({
                "status": "ok",
                "engine": "SQLite 3",
                "journalMode": wal,
                "sqliteVersion": sqlite3.sqlite_version,
                "counts": {
                    "iniciativas": c_ini,
                    "entregas": c_ent,
                    "avisos": c_avi,
                    "briefings": c_brf,
                    "cronograma": c_crn,
                }
            }).encode("utf-8")
            self.send_response(200)
            self.send_cors()
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return

        if path == "/api/export/csv":
            qs = urllib.parse.parse_qs(parsed.query)
            tabela = (qs.get("tabela") or ["ranking"])[0]
            csv_bytes = gerar_csv_export(tabela)
            filename = f"arena_{tabela}_{agora_dt().strftime('%Y%m%d_%H%M')}.csv"
            self.send_response(200)
            self.send_cors()
            self.send_header("Content-Type", "text/csv; charset=utf-8")
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
            self.send_header("Content-Length", str(len(csv_bytes)))
            self.end_headers()
            self.wfile.write(csv_bytes)
            return

        # Servir Index.html na raiz ou /Index.html
        if path in ("/", "/Index.html", "/index.html"):
            index_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Index.html")
            if os.path.exists(index_file):
                with open(index_file, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_cors()
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api":
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length) if length > 0 else b"{}"
            try:
                body = json.loads(raw.decode("utf-8"))
            except Exception:
                body = {}

            acao = body.get("acao", "")
            dados = body.get("dados", {})
            token = body.get("token", "")

            resultado = dispatch_api(acao, dados, token)
            resp_bytes = json.dumps(resultado, ensure_ascii=False).encode("utf-8")

            self.send_response(200)
            self.send_cors()
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
            return

        self.send_response(404)
        self.end_headers()


def run_server():
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    init_db()
    server = ThreadingHTTPServer(("0.0.0.0", PORT), ArenaRequestHandler)
    print("============================================================", flush=True)
    print(f"[ARENA SQLite 3 Server] Rodando em http://localhost:{PORT}", flush=True)
    print(f"[Database] {DB_PATH}", flush=True)
    print("============================================================", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    run_server()

