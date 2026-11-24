import base64
from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import json
import random
import re
import time
import unicodedata
import uuid
import zoneinfo

from database import get_connection, get_prop, set_prop

try:
    TZ_SP = zoneinfo.ZoneInfo("America/Sao_Paulo")
except Exception:
    TZ_SP = timezone(timedelta(hours=-3))

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
    "TAREFA_PADRAO": (
        "Não há entregas sugeridas para essa semana, mas qualquer divulgação"
        " extra pode gerar bônus de pontuação!"
    ),
    "MAX_LINKS_POR_ENVIO": 60,
}

TAREFAS_BASE = [
    {
        "id": "story_oficial",
        "nome": "Compartilhamento de story oficial",
        "pontos": 5,
        "condicao": "Conforme limite do briefing",
        "icone": "story",
    },
    {
        "id": "story_autoral",
        "nome": "Story autoral",
        "pontos": 10,
        "condicao": "Conteúdo próprio e aderente à missão",
        "icone": "story",
    },
    {
        "id": "feed_estatico",
        "nome": "Publicação estática no feed",
        "pontos": 30,
        "condicao": "Peça própria ou adaptação autorizada",
        "icone": "post",
    },
    {
        "id": "carrossel",
        "nome": "Carrossel autoral",
        "pontos": 50,
        "condicao": "Mínimo de 3 cards com conteúdo informativo",
        "icone": "carousel",
    },
    {
        "id": "reel",
        "nome": "Reel ou vídeo autoral",
        "pontos": 100,
        "condicao": "Conteúdo original com mensagem clara",
        "icone": "reel",
    },
]

REGRAS = [
    (
        "Perfil Público: Mantenha a conta da iniciativa pública durante toda a"
        " competição."
    ),
    "Marcação Obrigatória: Sempre marque o perfil oficial @mercadoemconexao.",
    "Post Ativo: Não apague nem arquive a publicação do Feed após o envio.",
    (
        "Respeito e Ética: O conteúdo não pode conter palavrões, termos"
        " ofensivos ou preconceituosos."
    ),
    (
        "Validação no Prazo: Envie o link do post dentro do prazo de cada"
        " tarefa para homologação dos pontos."
    ),
    (
        "Limite de Inscrições: A pontuação de inscrições atribuídas à iniciativa"
        " tem teto máximo de 200 pontos na campanha."
    ),
]

CONTAGENS = {
    "inscricoes": {
        "rotulo": "Inscrições atribuídas",
        "pontos": CONFIG["PONTOS_POR_INSCRICAO"],
        "limite": CONFIG["LIMITE_PONTOS_INSCRICAO"],
    },
    "formulario": {
        "rotulo": "Respostas no formulário de pesquisa",
        "pontos": CONFIG["PONTOS_POR_RESPOSTA"],
    },
    "palestras": {
        "rotulo": "Presença nas palestras",
        "pontos": CONFIG["PONTOS_POR_PALESTRA"],
    },
    "feira": {
        "rotulo": "Presença real na feira de carreiras",
        "pontos": CONFIG["PONTOS_POR_FEIRA"],
    },
    "challenges": {
        "rotulo": "Participação nos challenges",
        "pontos": CONFIG["PONTOS_POR_CHALLENGE"],
    },
}


# ============================== UTILITÁRIOS ==============================


class ArenaException(Exception):

    def __init__(self, message: str, sair: bool = False):
        super().__init__(message)
        self.message = message
        self.sair = sair


def erro(msg: str, sair: bool = False):
    return ArenaException(msg, sair=sair)


def normalizar(s: str) -> str:
    if not s:
        return ""
    s_norm = unicodedata.normalize("NFD", str(s))
    s_no_accents = "".join(c for c in s_norm if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", s_no_accents).strip().lower()


def texto(v: Any, rotulo: str, max_len: int, obrigatorio: bool) -> str:
    s = re.sub(r"\s+", " ", str(v if v is not None else "")).strip()
    if obrigatorio and not s:
        raise erro(f'Preencha o campo "{rotulo}".')
    if len(s) > max_len:
        raise erro(f'O campo "{rotulo}" aceita no máximo {max_len} caracteres.')
    return s


def inteiro(s: Any, rotulo: str) -> int:
    m = re.match(r"^[+-]?\d+$", str(s or "").replace(" ", ""))
    if not m:
        raise erro(f'"{rotulo}" deve ser um número inteiro (ex.: 20).')
    return int(m.group(0))


def url_valida(u: str) -> bool:
    if not u or len(u) > 500:
        return False
    return bool(
        re.match(r"^https?://[^\s/$.?#][^\s]*\.[^\s]{2,}", u, re.IGNORECASE)
    )


def now_sp() -> datetime:
    return datetime.now(TZ_SP)


def format_date_sp(dt: datetime = None) -> str:
    if dt is None:
        dt = now_sp()
    return dt.strftime("%d/%m/%Y %H:%M:%S")


def format_date_ymd_sp(dt: datetime = None) -> str:
    if dt is None:
        dt = now_sp()
    return dt.strftime("%y%m%d")


def timestamp_ms(val: Any) -> int:
    if not val:
        return 0
    if isinstance(val, (int, float)):
        return int(val)
    if isinstance(val, str):
        val = val.strip()
        if val.isdigit() and len(val) >= 10:
            return int(val)
        m = re.match(
            r"^(\d{2})/(\d{2})/(\d{4})(?:\s+(\d{2}):(\d{2})(?::(\d{2}))?)?", val
        )
        if m:
            day, month, year = int(m.group(1)), int(m.group(2)), int(m.group(3))
            hour = int(m.group(4) or 0)
            minute = int(m.group(5) or 0)
            second = int(m.group(6) or 0)
            dt = datetime(year, month, day, hour, minute, second, tzinfo=TZ_SP)
            return int(dt.timestamp() * 1000)
        try:
            dt = datetime.fromisoformat(val)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=TZ_SP)
            return int(dt.timestamp() * 1000)
        except Exception:
            return 0
    return 0


def data_hora_string(val: Any) -> str:
    if not val:
        return ""
    if isinstance(val, str):
        if re.match(r"^\d{2}/\d{2}/\d{4}", val):
            return val
        if val.isdigit() and len(val) >= 10:
            dt = datetime.fromtimestamp(int(val) / 1000, tz=TZ_SP)
            return dt.strftime("%d/%m/%Y %H:%M:%S")
        try:
            dt = datetime.fromisoformat(val)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=TZ_SP)
            return dt.astimezone(TZ_SP).strftime("%d/%m/%Y %H:%M:%S")
        except Exception:
            return val
    if isinstance(val, (int, float)):
        dt = datetime.fromtimestamp(val / 1000, tz=TZ_SP)
        return dt.strftime("%d/%m/%Y %H:%M:%S")
    return str(val)


def gerar_id_acao() -> str:
    prefixo = format_date_ymd_sp()
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    sufixo = "".join(random.choice(chars) for _ in range(4))
    return f"#ACT-{prefixo}-{sufixo}"


def gerar_id_lnc() -> str:
    prefixo = format_date_ymd_sp()
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    sufixo = "".join(random.choice(chars) for _ in range(4))
    return f"#LNC-{prefixo}-{sufixo}"


def gerar_id_brf() -> str:
    prefixo = format_date_ymd_sp()
    sufixo = f"{random.randint(1, 9999):04d}"
    return f"#BRF-{prefixo}-{sufixo}"


def gerar_id_crn() -> str:
    prefixo = format_date_ymd_sp()
    sufixo = f"{random.randint(1, 9999):04d}"
    return f"#CRN-{prefixo}-{sufixo}"


def num(v: Any) -> int:
    try:
        return int(v)
    except (ValueError, TypeError):
        try:
            return int(float(v))
        except (ValueError, TypeError):
            return 0


def json_parse(s: Any) -> dict:
    if isinstance(s, dict):
        return s
    try:
        return json.loads(s) if s else {}
    except Exception:
        return {}


# ============================== SESSÃO E SEGURANÇA ==============================


def segredo() -> str:
    s = get_prop("ARENA_SEGREDO")
    if not s:
        s = str(uuid.uuid4()) + str(uuid.uuid4())
        set_prop("ARENA_SEGREDO", s)
    return s


def base64_url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")


def base64_url_decode(s: str) -> bytes:
    pad = len(s) % 4
    if pad:
        s += "=" * (4 - pad)
    return base64.urlsafe_b64decode(s)


def assinar(texto_str: str) -> str:
    sig = hmac.new(
        segredo().encode("utf-8"), texto_str.encode("utf-8"), hashlib.sha256
    ).digest()
    return base64_url_encode(sig)


def gerar_token(user_id: str) -> str:
    exp = int(time.time() * 1000) + CONFIG["SESSAO_DIAS"] * 86400 * 1000
    carga = f"{user_id}|{exp}"
    carga_b64 = base64_url_encode(carga.encode("utf-8"))
    sig = assinar(carga)
    return f"{carga_b64}.{sig}"


def ler_token(token: str) -> Optional[str]:
    if not token or "." not in token:
        return None
    partes = token.split(".", 1)
    try:
        carga = base64_url_decode(partes[0]).decode("utf-8")
    except Exception:
        return None
    if assinar(carga) != partes[1]:
        return None
    p = carga.split("|", 1)
    if len(p) != 2:
        return None
    try:
        if int(p[1]) < int(time.time() * 1000):
            return None
    except ValueError:
        return None
    return p[0]


def hash_senha(senha: str, salt: str) -> str:
    h = salt + "::" + senha
    for _ in range(50):
        h = hashlib.sha256((h + salt).encode("utf-8")).hexdigest().lower()
    return h


def eh_admin(u: dict) -> bool:
    if not u:
        return False
    return (
        str(u.get("admin", "")).lower() == "sim"
        or normalizar(u.get("nome", "")) == normalizar(CONFIG["ADMIN_NOME"])
    )


def usuario(token: str) -> dict:
    uid = ler_token(token)
    if not uid:
        raise erro(
            "Sua sessão expirou ou é inválida. Entre novamente.", sair=True
        )
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM iniciativas WHERE id = ?", (uid,)
    ).fetchone()
    conn.close()
    if not row:
        raise erro(
            "Sua sessão expirou ou é inválida. Entre novamente.", sair=True
        )
    return dict(row)


def admin(token: str) -> dict:
    u = usuario(token)
    if not eh_admin(u):
        raise erro("Função exclusiva do administrador (UFMG Hub).")
    return u


def iniciativa(id_ini: str) -> dict:
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM iniciativas WHERE id = ?", (id_ini,)
    ).fetchone()
    conn.close()
    if not row:
        raise erro("Selecione uma iniciativa válida cadastrada.")
    u = dict(row)
    if eh_admin(u):
        raise erro("Selecione uma iniciativa válida cadastrada.")
    return u


# ============================== CADASTRO & LOGIN ==============================


def cadastrar(d: dict) -> dict:
    nome = texto(d.get("nome"), "Nome da iniciativa", 80, True)
    tipo = texto(d.get("tipo"), "Tipo de iniciativa", 40, False) or "Empresa Júnior"
    representante = texto(
        d.get("representante"), "Nome do representante", 80, True
    )
    cargo = texto(d.get("cargo"), "Cargo do representante", 60, True)
    rede = texto(
        d.get("redeSocial"), "Rede social da iniciativa", 150, True
    )
    senha = str(d.get("senha") or "")
    if len(senha) < 6:
        raise erro("A senha precisa ter pelo menos 6 caracteres.")
    if len(senha) > 100:
        raise erro("Senha longa demais.")

    conn = get_connection()
    cur = conn.cursor()

    chave = normalizar(nome)
    rows = cur.execute("SELECT nome FROM iniciativas").fetchall()
    for r in rows:
        if normalizar(r["nome"]) == chave:
            conn.close()
            raise erro(
                f'Já existe uma iniciativa cadastrada com o nome "{nome}". Se'
                ' você já possui cadastro, escolha "Entrar".'
            )

    salt = str(uuid.uuid4())
    uid = str(uuid.uuid4())
    is_adm = "sim" if chave == normalizar(CONFIG["ADMIN_NOME"]) else ""
    now_ms = int(time.time() * 1000)

    cur.execute(
        """
        INSERT INTO iniciativas (id, nome, tipo, representante, cargo, redeSocial, salt, hash, criadoEm, admin)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            uid,
            nome,
            tipo,
            representante,
            cargo,
            rede,
            salt,
            hash_senha(senha, salt),
            now_ms,
            is_adm,
        ),
    )
    conn.commit()
    conn.close()

    u = {"id": uid, "nome": nome, "admin": is_adm}
    return {"token": gerar_token(uid), "nome": nome, "admin": eh_admin(u)}


def entrar(d: dict) -> dict:
    chave = normalizar(d.get("nome"))
    senha = str(d.get("senha") or "")
    conn = get_connection()
    rows = conn.execute("SELECT * FROM iniciativas").fetchall()
    conn.close()

    user_found = None
    for r in rows:
        if normalizar(r["nome"]) == chave:
            user_found = dict(r)
            break

    if not user_found or hash_senha(senha, user_found["salt"]) != user_found["hash"]:
        raise erro("Nome da iniciativa ou senha incorretos.")

    return {
        "token": gerar_token(user_found["id"]),
        "nome": user_found["nome"],
        "admin": eh_admin(user_found),
    }


# ============================== PAINEL PRINCIPAL & RANKING ==============================


def ranking(
    inis: List[dict], entregas: List[dict], avisos: List[dict]
) -> List[dict]:
    res_map = {}
    for u in inis:
        if not eh_admin(u):
            res_map[u["id"]] = {
                "id": u["id"],
                "nome": u["nome"],
                "tipo": u.get("tipo") or "Empresa Júnior",
                "representante": u.get("representante", ""),
                "cargo": u.get("cargo", ""),
                "redeSocial": u.get("redeSocial", ""),
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

    # 1. Entregas de tarefas
    for e in entregas:
        rec = res_map.get(e["iniciativaId"])
        if not rec:
            continue
        rec["totalEntregas"] += 1
        pts = num(e.get("pontos"))
        if e.get("status") == "validada":
            rec["pontos"] += pts
            rec["pontosValidados"] += pts
            rec["breakdown"]["redes"] += pts
        elif e.get("status") == "pendente":
            rec["pontos"] += pts
            rec["pontosPendentes"] += pts
            rec["breakdown"]["redes"] += pts

    # 2. Avisos / Lançamentos do Hub
    for a in avisos:
        if a.get("status") == "cancelado":
            continue
        d = json_parse(a.get("dados"))
        if d.get("cancelado"):
            continue
        rec = res_map.get(a.get("iniciativaId"))
        if not rec:
            continue

        pts = num(a.get("pontos"))
        tipo = a.get("tipo")

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
        else:
            rec["breakdown"]["avulso"] += pts
            rec["pontos"] += pts
            rec["pontosValidados"] += pts

    lista = list(res_map.values())
    lista.sort(
        key=lambda x: (
            -x["pontos"],
            -x["pontosValidados"],
            normalizar(x["nome"]),
        )
    )
    return lista


def obter_tarefas(catalogo: List[dict]) -> List[dict]:
    lst = [dict(t) for t in TAREFAS_BASE]
    for c in catalogo:
        if c.get("ativo") != "nao" and c.get("tipo") == "link":
            lst.append(
                {
                    "id": c["id"],
                    "nome": c["nome"],
                    "pontos": num(c.get("pontos")),
                    "condicao": c.get("condicao") or "Conforme briefing",
                    "icone": "custom",
                    "personalizada": True,
                }
            )
    return lst


def aviso_publico(a: dict, por_id: dict) -> dict:
    u = por_id.get(a.get("iniciativaId")) or {}
    return {
        "id": a["id"],
        "tipo": a.get("tipo"),
        "status": a.get("status") or "ativo",
        "criadoEm": timestamp_ms(a.get("criadoEm")),
        "dataHora": data_hora_string(a.get("criadoEm")),
        "expiraEm": timestamp_ms(a.get("expiraEm")),
        "iniciativaId": a.get("iniciativaId"),
        "iniciativa": u.get("nome", ""),
        "tipoIniciativa": u.get("tipo", "Empresa Júnior"),
        "pontos": num(a.get("pontos")),
        "dados": json_parse(a.get("dados")),
    }


def painel(me: dict) -> dict:
    agora = int(time.time() * 1000)
    conn = get_connection()
    inis = [dict(r) for r in conn.execute("SELECT * FROM iniciativas").fetchall()]
    entregas = [
        dict(r) for r in conn.execute("SELECT * FROM entregas").fetchall()
    ]
    avisos = [dict(r) for r in conn.execute("SELECT * FROM avisos").fetchall()]
    catalogo = [
        dict(r) for r in conn.execute("SELECT * FROM acoes_catalogo").fetchall()
    ]
    briefings = [
        dict(r)
        for r in conn.execute(
            "SELECT * FROM briefings WHERE status != 'removido'"
        ).fetchall()
    ]
    cronograma = [
        dict(r)
        for r in conn.execute(
            "SELECT * FROM cronograma WHERE status != 'removido'"
        ).fetchall()
    ]
    conn.close()

    por_id = {u["id"]: u for u in inis}
    tarefas_disponiveis = obter_tarefas(catalogo)

    # Tarefa do Hub em vigor
    tarefas_ativas = [
        a
        for a in avisos
        if a.get("tipo") == "tarefa" and a.get("status") != "cancelado"
    ]
    tarefas_ativas.sort(
        key=lambda x: timestamp_ms(x.get("criadoEm")), reverse=True
    )
    tarefa_hub = None
    if (
        tarefas_ativas
        and timestamp_ms(tarefas_ativas[0].get("expiraEm")) > agora
    ):
        t_act = tarefas_ativas[0]
        tarefa_hub = {
            "dados": json_parse(t_act.get("dados")),
            "criadoEm": timestamp_ms(t_act.get("criadoEm")),
            "expiraEm": timestamp_ms(t_act.get("expiraEm")),
        }

    # Avisos ativos no feed
    ativos = [
        aviso_publico(a, por_id)
        for a in avisos
        if a.get("tipo") != "tarefa"
        and a.get("status") != "cancelado"
        and timestamp_ms(a.get("expiraEm")) > agora
    ]
    ativos.sort(key=lambda x: x["criadoEm"], reverse=True)

    # Minhas entregas
    minhas = [e for e in entregas if e.get("iniciativaId") == me["id"]]
    minhas.sort(
        key=lambda x: timestamp_ms(x.get("criadoEm")), reverse=True
    )
    minhas_formatadas = [
        {
            "id": e["id"],
            "tarefaId": e["tarefaId"],
            "tarefaNome": e["tarefaNome"],
            "pontos": num(e.get("pontos")),
            "url": e["url"],
            "status": e.get("status"),
            "motivoRecusa": e.get("motivoRecusa", ""),
            "criadoEm": timestamp_ms(e.get("criadoEm")),
            "dataHora": data_hora_string(e.get("criadoEm")),
            "revisadoEm": timestamp_ms(e.get("revisadoEm")),
            "revisadoDataHora": data_hora_string(e.get("revisadoEm")),
        }
        for e in minhas
    ]

    ranking_data = ranking(inis, entregas, avisos)
    total_pontos = sum(r["pontos"] for r in ranking_data)
    total_validadas = sum(1 for e in entregas if e.get("status") == "validada")

    briefings.sort(key=lambda b: timestamp_ms(b.get("criadoEm")), reverse=True)
    cronograma.sort(key=lambda c: str(c.get("data", "")))

    return {
        "me": {
            "id": me["id"],
            "nome": me["nome"],
            "tipo": me.get("tipo") or "Empresa Júnior",
            "representante": me.get("representante", ""),
            "cargo": me.get("cargo", ""),
            "redeSocial": me.get("redeSocial", ""),
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
        "avisos": ativos,
        "regras": REGRAS,
        "tarefas": tarefas_disponiveis,
        "minhasEntregas": minhas_formatadas,
        "briefings": briefings,
        "cronograma": cronograma,
        "config": {
            "marcacao": CONFIG["MARCACAO"],
            "tarefaPadrao": CONFIG["TAREFA_PADRAO"],
            "pontosPorInscricao": CONFIG["PONTOS_POR_INSCRICAO"],
            "limiteInscricoes": CONFIG["LIMITE_PONTOS_INSCRICAO"],
        },
        "pontosPor": {k: v["pontos"] for k, v in CONTAGENS.items()},
        "edital": CONFIG["EDITAL_URL"] or "",
        "agora": agora,
    }


# ============================== REGISTRO DE TAREFAS ==============================


def enviar_tarefas(me: dict, d: dict) -> dict:
    if eh_admin(me):
        raise erro(
            "O administrador UFMG Hub não participa como competidor do"
            " ranking."
        )

    itens = d.get("itens") if isinstance(d.get("itens"), list) else []
    conn = get_connection()
    catalogo = [
        dict(r) for r in conn.execute("SELECT * FROM acoes_catalogo").fetchall()
    ]
    todas_tarefas = obter_tarefas(catalogo)
    mapa_t = {t["id"]: t for t in todas_tarefas}

    criado_em = format_date_sp()
    novas = []

    for it in itens:
        t = mapa_t.get(it.get("tarefaId"))
        if not t:
            continue
        urls = it.get("urls") if isinstance(it.get("urls"), list) else []
        for url_str in urls:
            url_str = str(url_str or "").strip()
            if not url_str:
                continue
            if not url_valida(url_str):
                raise erro(f"Link com formato inválido: {url_str[:60]}")
            novas.append(
                (
                    gerar_id_acao(),
                    me["id"],
                    t["id"],
                    t["nome"],
                    t["pontos"],
                    url_str,
                    "pendente",
                    "",
                    criado_em,
                    "",
                )
            )

    if not novas:
        raise erro("Adicione pelo menos um link válido para pontuar.")
    if len(novas) > CONFIG["MAX_LINKS_POR_ENVIO"]:
        raise erro(
            "Limite de envios por vez atingido. Envie em lotes menores."
        )

    cur = conn.cursor()
    cur.executemany(
        """
        INSERT INTO entregas (id, iniciativaId, tarefaId, tarefaNome, pontos, url, status, motivoRecusa, criadoEm, revisadoEm)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        novas,
    )
    conn.commit()
    conn.close()

    total_pts = sum(n[4] for n in novas)
    p = painel(me)
    p["enviado"] = {"links": len(novas), "pontos": total_pts}
    return p


# ============================== ÁREA ADMINISTRATIVA ==============================


def admin_dados(me: dict) -> dict:
    conn = get_connection()
    inis = [dict(r) for r in conn.execute("SELECT * FROM iniciativas").fetchall()]
    entregas = [
        dict(r) for r in conn.execute("SELECT * FROM entregas").fetchall()
    ]
    avisos = [dict(r) for r in conn.execute("SELECT * FROM avisos").fetchall()]
    catalogo = [
        dict(r)
        for r in conn.execute(
            "SELECT * FROM acoes_catalogo WHERE ativo != 'nao'"
        ).fetchall()
    ]
    briefings = [
        dict(r)
        for r in conn.execute(
            "SELECT * FROM briefings WHERE status != 'removido'"
        ).fetchall()
    ]
    cronograma = [
        dict(r)
        for r in conn.execute(
            "SELECT * FROM cronograma WHERE status != 'removido'"
        ).fetchall()
    ]
    conn.close()

    por_id = {u["id"]: u for u in inis}

    entregas_fmt = []
    for e in entregas:
        u = por_id.get(e["iniciativaId"]) or {}
        entregas_fmt.append(
            {
                "id": e["id"],
                "iniciativaId": e["iniciativaId"],
                "iniciativa": u.get("nome", "—"),
                "tipoIniciativa": u.get("tipo", "Empresa Júnior"),
                "tarefaId": e["tarefaId"],
                "tarefaNome": e["tarefaNome"],
                "pontos": num(e.get("pontos")),
                "url": e["url"],
                "status": e["status"],
                "motivoRecusa": e.get("motivoRecusa", ""),
                "criadoEm": timestamp_ms(e.get("criadoEm")),
                "dataHora": data_hora_string(e.get("criadoEm")),
                "revisadoEm": timestamp_ms(e.get("revisadoEm")),
                "revisadoDataHora": data_hora_string(e.get("revisadoEm")),
            }
        )
    entregas_fmt.sort(key=lambda x: x["criadoEm"], reverse=True)

    historico = [aviso_publico(a, por_id) for a in avisos]
    historico.sort(key=lambda x: x["criadoEm"], reverse=True)

    iniciativas = [
        {
            "id": u["id"],
            "nome": u["nome"],
            "tipo": u.get("tipo", "Empresa Júnior"),
            "representante": u.get("representante", ""),
            "cargo": u.get("cargo", ""),
            "redeSocial": u.get("redeSocial", ""),
        }
        for u in inis
        if not eh_admin(u)
    ]
    iniciativas.sort(key=lambda x: normalizar(x["nome"]))

    catalogo_fmt = [
        {
            "id": c["id"],
            "nome": c["nome"],
            "pontos": num(c.get("pontos")),
            "tipo": c.get("tipo"),
            "condicao": c.get("condicao", ""),
            "descricao": c.get("descricao", ""),
            "criadoEm": num(c.get("criadoEm")),
        }
        for c in catalogo
    ]

    briefings.sort(key=lambda b: timestamp_ms(b.get("criadoEm")), reverse=True)
    cronograma.sort(key=lambda c: str(c.get("data", "")))

    return {
        "entregas": entregas_fmt,
        "historico": historico,
        "iniciativas": iniciativas,
        "catalogo": catalogo_fmt,
        "briefings": briefings,
        "cronograma": cronograma,
        "pontosPor": {k: v["pontos"] for k, v in CONTAGENS.items()},
        "config": {
            "limiteInscricoes": CONFIG["LIMITE_PONTOS_INSCRICAO"],
            "maxPresencial": CONFIG["MAX_PONTOS_PRESENCIAL"],
        },
        "agora": int(time.time() * 1000),
    }


def validar_entrega(me: dict, d: dict) -> dict:
    status = str(d.get("status") or "")
    if status not in ["pendente", "validada", "recusada"]:
        raise erro("Status de validação inválido.")
    motivo = texto(d.get("motivoRecusa"), "Motivo da recusa", 250, False)
    revisado = "" if status == "pendente" else format_date_sp()
    motivo_final = motivo if status == "recusada" else ""

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE entregas
        SET status = ?, motivoRecusa = ?, revisadoEm = ?
        WHERE id = ?
    """,
        (status, motivo_final, revisado, d.get("id")),
    )
    if cur.rowcount == 0:
        conn.close()
        raise erro("Entrega não encontrada no sistema.")
    conn.commit()
    conn.close()
    return admin_dados(me)


def novo_aviso(tipo: str, iniciativa_id: str, pontos: int, dados: dict):
    agora_dt = now_sp()
    criado_em = format_date_sp(agora_dt)
    horas = CONFIG["HORAS"].get(tipo, 48)
    expira_em = format_date_sp(agora_dt + timedelta(hours=horas))
    aviso_id = gerar_id_lnc()

    conn = get_connection()
    conn.execute(
        """
        INSERT INTO avisos (id, tipo, criadoEm, expiraEm, iniciativaId, pontos, dados, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            aviso_id,
            tipo,
            criado_em,
            expira_em,
            iniciativa_id or "",
            pontos or 0,
            json.dumps(dados or {}),
            "ativo",
        ),
    )
    conn.commit()
    conn.close()


def publicar_tarefa_hub(me: dict, d: dict) -> dict:
    dados = {
        "sobre": texto(d.get("sobre"), "Sobre o que publicar", 400, False),
        "periodo": texto(d.get("periodo"), "Período para publicar", 50, False),
        "recomendacoes": texto(
            d.get("recomendacoes"), "Recomendações do Hub", 400, False
        ),
        "bonus": texto(d.get("bonus"), "Bônus", 400, False),
    }
    if not any(dados.values()):
        raise erro("Preencha pelo menos um campo da tarefa semanal.")
    novo_aviso("tarefa", "", 0, dados)
    return admin_dados(me)


def publicar_presencial(me: dict, d: dict) -> dict:
    ini = iniciativa(d.get("iniciativaId"))
    oque = texto(d.get("oque"), "O que foi a ação", 300, True)
    quando = texto(d.get("quando"), "Quando foi a ação", 150, True)
    pontos = inteiro(d.get("pontos"), "Pontuação da ação")
    if pontos < 1:
        raise erro("A pontuação deve ser maior que zero.")
    if pontos > CONFIG["MAX_PONTOS_PRESENCIAL"]:
        raise erro(
            f"A pontuação de ação presencial aprovada tem limite de até"
            f" {CONFIG['MAX_PONTOS_PRESENCIAL']} pontos."
        )
    novo_aviso(
        "presencial",
        ini["id"],
        pontos,
        {"oque": oque, "quando": quando, "pontuacao": pontos},
    )
    return admin_dados(me)


def publicar_contagem(me: dict, d: dict, tipo: str) -> dict:
    ini = iniciativa(d.get("iniciativaId"))
    c = CONTAGENS.get(tipo)
    if not c:
        raise erro("Categoria de contagem não reconhecida.")
    qtd = inteiro(d.get("quantidade"), c["rotulo"])
    if qtd <= 0:
        raise erro(f"Informe uma quantidade positiva para {c['rotulo']}.")
    pts = qtd * c["pontos"]
    novo_aviso(
        tipo,
        ini["id"],
        pts,
        {"quantidade": qtd, "pontosUnitarios": c["pontos"]},
    )
    return admin_dados(me)


def publicar_acao_avulsa(me: dict, d: dict) -> dict:
    ini = iniciativa(d.get("iniciativaId"))
    titulo = texto(d.get("titulo"), "Título ou nome da ação", 100, True)
    descricao = texto(
        d.get("descricao"), "Descrição ou justificativa", 300, False
    )
    modo = "quantidade" if d.get("modo") == "quantidade" else "fixo"
    quando = (
        texto(d.get("quando"), "Data ou momento", 100, False)
        or "Durante a Arena"
    )

    if modo == "quantidade":
        qtd = inteiro(d.get("quantidade"), "Quantidade")
        unitario = inteiro(d.get("pontosUnitarios"), "Pontos por unidade")
        if qtd <= 0 or unitario <= 0:
            raise erro(
                "Quantidade e pontos por unidade devem ser maiores que zero."
            )
        pontos_final = qtd * unitario
    else:
        qtd = 1
        unitario = 0
        pontos_final = inteiro(d.get("pontos"), "Pontuação total")
        if pontos_final <= 0:
            raise erro("A pontuação deve ser maior que zero.")

    dados = {
        "titulo": titulo,
        "descricao": descricao,
        "modo": modo,
        "quantidade": qtd,
        "pontosUnitarios": unitario,
        "quando": quando,
    }
    novo_aviso("avulso", ini["id"], pontos_final, dados)
    return admin_dados(me)


def criar_acao_catalogo(me: dict, d: dict) -> dict:
    nome = texto(d.get("nome"), "Nome da tarefa", 80, True)
    pontos = inteiro(d.get("pontos"), "Pontos da tarefa")
    condicao = texto(
        d.get("condicao"), "Condição ou regra de validação", 250, True
    )
    descricao = texto(d.get("descricao"), "Descrição adicional", 300, False)
    if pontos <= 0:
        raise erro("Os pontos devem ser maiores que zero.")

    id_cat = "custom_" + str(uuid.uuid4())[:8]
    now_ms = int(time.time() * 1000)

    conn = get_connection()
    conn.execute(
        """
        INSERT INTO acoes_catalogo (id, nome, pontos, tipo, descricao, condicao, criadoEm, ativo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (id_cat, nome, pontos, "link", descricao, condicao, now_ms, "sim"),
    )
    conn.commit()
    conn.close()
    return admin_dados(me)


def remover_acao_catalogo(me: dict, d: dict) -> dict:
    id_cat = texto(d.get("id"), "ID da ação", 50, True)
    conn = get_connection()
    conn.execute(
        "UPDATE acoes_catalogo SET ativo = 'nao' WHERE id = ?", (id_cat,)
    )
    conn.commit()
    conn.close()
    return admin_dados(me)


def cancelar_aviso(me: dict, d: dict) -> dict:
    id_aviso = texto(d.get("id"), "ID do aviso", 50, True)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE avisos SET status = 'cancelado' WHERE id = ?", (id_aviso,)
    )
    if cur.rowcount == 0:
        conn.close()
        raise erro("Registro de aviso não encontrado.")
    conn.commit()
    conn.close()
    return admin_dados(me)


def salvar_briefing(me: dict, d: dict) -> dict:
    agora_formatado = format_date_sp()
    brf_id = (
        str(d.get("id"))
        if d.get("id") and str(d.get("id")).strip()
        else gerar_id_brf()
    )
    titulo = texto(d.get("titulo"), "Título do briefing", 120, True)
    fase = texto(d.get("fase"), "Fase ou mês", 60, False) or "Geral"
    periodo = texto(d.get("periodo"), "Período", 60, False) or "Durante a Arena"
    descricao = texto(d.get("descricao"), "Descrição do briefing", 1000, True)
    diretrizes = (
        texto(d.get("diretrizes"), "Diretrizes de conteúdo", 1000, False) or ""
    )
    link_drive = (
        texto(d.get("linkDrive"), "Link do Kit de Artes / Drive", 400, False)
        or ""
    )
    hashtags = (
        texto(d.get("hashtags"), "Hashtags e marcações", 250, False)
        or "@mercadoemconexao #ArenaMeC"
    )
    bonus = texto(d.get("bonus"), "Bônus de pontuação", 250, False) or ""
    status = d.get("status") or "ativo"

    conn = get_connection()
    cur = conn.cursor()
    row = cur.execute(
        "SELECT id FROM briefings WHERE id = ?", (brf_id,)
    ).fetchone()

    if row:
        cur.execute(
            """
            UPDATE briefings
            SET titulo = ?, fase = ?, periodo = ?, descricao = ?, diretrizes = ?, linkDrive = ?, hashtags = ?, bonus = ?, status = ?
            WHERE id = ?
        """,
            (
                titulo,
                fase,
                periodo,
                descricao,
                diretrizes,
                link_drive,
                hashtags,
                bonus,
                status,
                brf_id,
            ),
        )
    else:
        cur.execute(
            """
            INSERT INTO briefings (id, titulo, fase, periodo, descricao, diretrizes, linkDrive, hashtags, bonus, status, criadoEm)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                brf_id,
                titulo,
                fase,
                periodo,
                descricao,
                diretrizes,
                link_drive,
                hashtags,
                bonus,
                status,
                agora_formatado,
            ),
        )
    conn.commit()
    conn.close()
    return admin_dados(me)


def remover_briefing(me: dict, d: dict) -> dict:
    brf_id = texto(d.get("id"), "ID do briefing", 50, True)
    conn = get_connection()
    conn.execute(
        "UPDATE briefings SET status = 'removido' WHERE id = ?", (brf_id,)
    )
    conn.commit()
    conn.close()
    return admin_dados(me)


def salvar_cronograma(me: dict, d: dict) -> dict:
    agora_formatado = format_date_sp()
    crn_id = (
        str(d.get("id"))
        if d.get("id") and str(d.get("id")).strip()
        else gerar_id_crn()
    )
    data = texto(d.get("data"), "Data da atividade", 40, True)
    titulo = texto(d.get("titulo"), "Título da atividade", 120, True)
    local = (
        texto(d.get("local"), "Local ou formato", 100, False)
        or "Campus Pampulha"
    )
    tipo = texto(d.get("tipo"), "Tipo de atividade", 50, False) or "Presencial"
    pontos = texto(d.get("pontos"), "Pontos associados", 50, False) or ""
    descricao = (
        texto(d.get("descricao"), "Descrição da atividade", 500, False) or ""
    )
    status = d.get("status") or "proximo"

    conn = get_connection()
    cur = conn.cursor()
    row = cur.execute(
        "SELECT id FROM cronograma WHERE id = ?", (crn_id,)
    ).fetchone()

    if row:
        cur.execute(
            """
            UPDATE cronograma
            SET data = ?, titulo = ?, local = ?, tipo = ?, pontos = ?, descricao = ?, status = ?
            WHERE id = ?
        """,
            (data, titulo, local, tipo, pontos, descricao, status, crn_id),
        )
    else:
        cur.execute(
            """
            INSERT INTO cronograma (id, data, titulo, local, tipo, pontos, descricao, status, criadoEm)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                crn_id,
                data,
                titulo,
                local,
                tipo,
                pontos,
                descricao,
                status,
                agora_formatado,
            ),
        )
    conn.commit()
    conn.close()
    return admin_dados(me)


def remover_cronograma(me: dict, d: dict) -> dict:
    crn_id = texto(d.get("id"), "ID da atividade", 50, True)
    conn = get_connection()
    conn.execute(
        "UPDATE cronograma SET status = 'removido' WHERE id = ?", (crn_id,)
    )
    conn.commit()
    conn.close()
    return admin_dados(me)


# ============================== API DISPATCHER ==============================


def api_dispatch(acao: str, dados: dict = None, token: str = None) -> dict:
    dados = dados or {}
    try:
        if acao == "cadastrar":
            return cadastrar(dados)
        elif acao == "entrar":
            return entrar(dados)
        elif acao == "painel":
            return painel(usuario(token))
        elif acao == "enviarTarefas":
            return enviar_tarefas(usuario(token), dados)
        elif acao == "admin":
            return admin_dados(admin(token))
        elif acao == "validarEntrega":
            return validar_entrega(admin(token), dados)
        elif acao == "publicarTarefaHub":
            return publicar_tarefa_hub(admin(token), dados)
        elif acao == "publicarPresencial":
            return publicar_presencial(admin(token), dados)
        elif acao == "publicarInscricoes":
            return publicar_contagem(admin(token), dados, "inscricoes")
        elif acao == "publicarFormulario":
            return publicar_contagem(admin(token), dados, "formulario")
        elif acao == "publicarPalestras":
            return publicar_contagem(admin(token), dados, "palestras")
        elif acao == "publicarFeira":
            return publicar_contagem(admin(token), dados, "feira")
        elif acao == "publicarChallenges":
            return publicar_contagem(admin(token), dados, "challenges")
        elif acao == "publicarAcaoAvulsa":
            return publicar_acao_avulsa(admin(token), dados)
        elif acao == "criarAcaoCatalogo":
            return criar_acao_catalogo(admin(token), dados)
        elif acao == "removerAcaoCatalogo":
            return remover_acao_catalogo(admin(token), dados)
        elif acao == "cancelarAviso":
            return cancelar_aviso(admin(token), dados)
        elif acao == "salvarBriefing":
            return salvar_briefing(admin(token), dados)
        elif acao == "removerBriefing":
            return remover_briefing(admin(token), dados)
        elif acao == "salvarCronograma":
            return salvar_cronograma(admin(token), dados)
        elif acao == "removerCronograma":
            return remover_cronograma(admin(token), dados)
        else:
            raise erro(f"Ação desconhecida: {acao}")
    except ArenaException as ae:
        return {"erro": ae.message, "sair": ae.sair}
    except Exception as e:
        import traceback

        traceback.print_exc()
        return {"erro": str(e) or "Erro interno do servidor."}
