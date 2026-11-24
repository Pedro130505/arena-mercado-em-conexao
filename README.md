# 🏆 Arena | Mercado em Conexão (UFMG Hub)

> **Plataforma Oficial de Gamificação, Engajamento e Gestão de Campanhas para Empresas Juniores (EJs) e Equipes de Competição da Universidade Federal de Minas Gerais (UFMG).**

---

## 📌 Sumário
- [Visão Geral](#-visão-geral)
- [Arquitetura & Modos de Execução](#-arquitetura--modos-de-execução)
- [Banco de Dados SQLite 3](#-banco-de-dados-sqlite-3)
- [Funcionalidades Principais](#-funcionalidades-principais)
- [Sistema de Métricas Pós-Publicação](#-sistema-de-métricas-pós-publicação)
- [Como Rodar Localmente (1-Clique ou CLI)](#-como-rodar-localmente)
- [Testes Automatizados & Validação](#-testes-automatizados--validação)
- [Implantação no Google Apps Script](#-implantação-no-google-apps-script)
- [Credenciais de Demonstração](#-credenciais-de-demonstração)

---

## 📖 Visão Geral

A **Arena** é o sistema web desenvolvido sob medida para a feira e campanha do **Mercado em Conexão (MeC)**, coordenada pelo **UFMG Hub**. 

A plataforma conecta as lideranças estudantis (Empresas Juniores, Equipes de Competição e coletivos universitários), pontuando suas ações de divulgação, atração de público, participação em palestras e feiras presenciais com base na tabela oficial de pontuação (Edital 16.5).

---

## 🏛 Arquitetura & Modos de Execução

O projeto foi projetado com arquitetura dual transparente:

```
app_arena/
├── server.py              # Backend SQLite 3 em Python puro (ThreadingHTTPServer, WAL mode, REST API)
├── run.py                 # Inicializador amigável com abertura automática do navegador
├── iniciar_arena.bat      # Script 1-clique para Windows
├── arena.db               # Banco de dados relacional SQLite 3 pré-configurado
├── build_frontend.py      # Compilador do Single Page App (SPA)
├── Index.html             # Frontend compilado (HTML5, CSS3 responsivo, Vanilla JS)
├── Index-codigo-novo.txt  # Cópia para implantação no Google Apps Script
├── Code.gs                # Backend compatível com Google Apps Script / Google Sheets
└── Code-codigo-novo.txt   # Cópia para implantação no Apps Script
```

1. **Modo Python 3 + SQLite 3 (Produção Local / Servidor VPS):**
   * Servidor HTTP multithread de alta performance (`server.py`), sem necessidade de frameworks pesados ou bibliotecas externas.
   * Banco relacional local com **WAL Mode (Write-Ahead Logging)** garantindo leituras e escritas concorrentes sem travamentos.
   * Tokens de sessão criptografados com assinatura digital **HMAC-SHA256**.
   * Senhas armazenadas com algoritmo derivador **PBKDF2/SHA-256** e salt individual criptográfico (`uuid4`).

2. **Modo Google Apps Script + Planilhas Google:**
   * Backend em JavaScript nativo para a nuvem do Google (`Code.gs`), espelhando as mesmas regras de negócio e persistência na planilha Google Sheets.

---

## 🗄 Banco de Dados SQLite 3

O banco de dados relacional `arena.db` possui estrutura com índices e migrações automáticas. Se o arquivo `arena.db` não existir, o servidor o cria e popula automaticamente com o ecossistema inicial.

### Tabelas do Banco de Dados:
| Tabela | Descrição | Índices |
| :--- | :--- | :--- |
| `config_meta` | Metadados internos (Chave HMAC, status de seed) | `PRIMARY KEY (chave)` |
| `iniciativas` | Contas das equipes (`UFMG Hub`, EJs, Competição) | `PRIMARY KEY (id)`, `UNIQUE (nome COLLATE NOCASE)` |
| `entregas` | Links enviados para pontuação com status e auditoria | `idx_entregas_ini`, `idx_entregas_url`, `idx_entregas_status` |
| `avisos` | Pontuações lançadas pelo admin (inscrições, palestras, presencial) | `idx_avisos_ini`, `idx_avisos_tipo` |
| `acoes_catalogo` | Catálogo dinâmico de tarefas criadas pelo administrador | `PRIMARY KEY (id)` |
| `briefings` | Briefings oficiais estruturados por fase da campanha | `PRIMARY KEY (id)` |
| `cronograma` | Linha do tempo de atividades e eventos presenciais | `PRIMARY KEY (id)` |
| `metricas_entregas`| Relatórios de alcance e engajamento pós-publicação | `idx_metricas_entrega`, `idx_metricas_iniciativa` |

### Mecanismos de Integridade e Segurança:
* **Anti-Fraude e Deduplicação:** Normalização canônica de URLs de redes sociais (`urlCanonica`), removendo query strings (`?utm_source=...`, `&igsh=...`, etc.) e impedindo o reenvio do mesmo link por equipes distintas ou pela mesma equipe em duplicidade.
* **Teto Oficial de Inscrições:** Trava matemática estrita que bloqueia pontuação de inscrições acima do limite de 200 pontos por iniciativa.
* **Datas Brasileiras Padronizadas:** Todas as operações gravam data e hora legíveis no formato oficial `DD/MM/AAAA às HH:mm:ss`.

---

## 🚀 Funcionalidades Principais

### 1. 📢 Central MeC (Briefings Oficiais & Cronograma)
* **Briefings Estruturados por Fase:** Linha editorial, missão, diretrizes de publicação e bônus.
* **Hashtags com Cópia em 1-Clique:** Marcações oficiais (`@mercadoemconexao @ufmghub #ArenaMeC`) com cópia direta para a área de transferência.
* **Cronograma de Atividades:** Linha do tempo com datas, locais no campus (ex.: Praça de Serviços, Escola de Engenharia) e status em tempo real (*Acontecendo Agora*, *Próxima Atividade*).

### 2. 🥇 Ranking Geral com Pódio 3D
* **Pódio 3D:** Destaque visual elevado para os líderes (🥇 Ouro, 🥈 Prata, 🥉 Bronze).
* **Card "Você está aqui":** Feedback imediato para a equipe logada com posição, pontuação e distância para a equipe à frente.
* **Filtro por Categorias:** Alternância entre *Empresas Juniores (EJs)*, *Equipes de Competição* e *Todas*.
* **Extrato Detalhado:** Abertura do extrato discriminando pontos de redes, inscrições, presença, feira, palestras e métricas.

### 3. 📱 Envio de Tarefas & Gestão
* **Tabela 16.5 Oficial:** Compartilhamento de story (+5 pts), story autoral (+10 pts), post estático (+30 pts), carrossel autoral (+50 pts) e reel/vídeo autoral (+100 pts).
* **Identificador Único (#ACT-YYMMDD-XXXX):** Cada entrega recebe um código único rastreável.
* **Status em Tempo Real:** Acompanhamento entre *Aguardando Validação*, *Validada* e *Recusada* (com motivo formal e permissão de reenvio corrigido).

---

## 📊 Sistema de Métricas Pós-Publicação

Permite mensurar o impacto real de alcance e engajamento das publicações após a veiculação:

* **Posts, Carrosséis, Reels e Vídeos:** 3 checkpoints de mensuração de insights — **1ª Semana**, **2ª Semana** e **3ª Semana** (+10 pontos cada, até +30 pontos adicionais por entrega).
* **Stories:** Checkpoint após **24 Horas** da publicação (+5 pontos).
* **Painel Administrativo (`📊 Acompanhamento de Métricas`):**
  * KPIs em tempo real: Alcance Total Homologado, Engajamento Total, Fila de Pendentes e Total de Pontos Bônus.
  * Aprovação individual com 1 clique ou em lote.
  * **Radar de Engajamento:** Matriz comparativa de alcance e interações geradas por cada equipe para a campanha.

---

## ⚡ Como Rodar Localmente

### Pré-requisitos
* **Python 3.8+** instalado (nenhum pacote externo obrigatório para rodar o servidor).

### Opção 1: 1-Clique (Windows)
Dê um duplo clique no arquivo **`iniciar_arena.bat`**. O navegador abrirá automaticamente em `http://localhost:8080`.

### Opção 2: Terminal / Linha de Comando
```bash
# Iniciar o servidor com abertura automática do navegador:
python run.py

# Ou iniciar diretamente o servidor backend:
python server.py
```

Acesse no seu navegador: **`http://localhost:8080`**

---

## 🧪 Testes Automatizados & Validação

O projeto conta com suítes de testes automatizados que cobrem 100% da API, banco de dados SQLite e fluxo de interface via Playwright:

```bash
# Executa a bateria de 29 testes de banco SQLite + 5 testes E2E Playwright:
python test_sqlite_backend.py

# Executa os testes de ponta a ponta do sistema de métricas e homologação:
python test_e2e_playwright.py
```

---

## ☁️ Implantação no Google Apps Script

Caso deseje publicar a plataforma utilizando a infraestrutura do Google (Google Sheets + Google Apps Script):

1. Crie uma nova Planilha no Google Drive.
2. Acesse **Extensões > Apps Script**.
3. Copie o conteúdo de **`Code.gs`** (ou `Code-codigo-novo.txt`) para o arquivo de script.
4. Crie um arquivo HTML chamado `Index.html` e cole o conteúdo de **`Index.html`** (ou `Index-codigo-novo.txt`).
5. Execute a função `configurar()` no editor do Apps Script para criar os cabeçalhos das abas.
6. Clique em **Implantar > Nova implantação > App da Web** (Executar como: *Eu*, Quem pode acessar: *Qualquer pessoa*).

---

## 🔑 Credenciais de Demonstração

Para testes rápidos na tela de login, utilize os botões de atalho **Demo** ou as seguintes contas pré-configuradas no SQLite:

* **Administrador (UFMG Hub):**
  * **Iniciativa:** `UFMG Hub`
  * **Senha:** `admin`
* **Empresa Júnior (Competidora):**
  * **Iniciativa:** `Engrenagem Jr.`
  * **Senha:** `123`
* **Equipe de Competição (Competidora):**
  * **Iniciativa:** `Fórmula Tesla UFMG`
  * **Senha:** `123`
