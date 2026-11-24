# 🏆 Arena | Mercado em Conexão
### Sistema Oficial de Gamificação de Iniciativas (EJs & Equipes de Competição)
**Realização:** UFMG Hub & Mercado em Conexão

---

## 📌 Visão Geral do Projeto

A **Arena** é a plataforma web de gamificação desenvolvida para engajar e pontuar as **Empresas Juniores (EJs)**, **Equipes de Competição** e projetos parceiros da UFMG durante a campanha e feira do **Mercado em Conexão**.

A plataforma suporta **dois modos completos de execução**:
1. **🐍 Modo Python + SQLite (NOVO!):** Backend em **FastAPI** com banco de dados local **SQLite (`arena.db`)**, rodando localmente ou em servidor próprio/VPS via `http://localhost:8000`.
2. **☁️ Modo Google Apps Script + Planilhas:** Backend em JavaScript rodando na nuvem do Google com o **Google Sheets** como banco de dados.

---

## ⚡ Como Rodar em Python + SQLite (Passo a Passo Rápido)

### 1. Iniciar o Servidor
Você pode iniciar o servidor de duas maneiras:
- **Opção A (Windows 1-Clique):** Dê um duplo clique no arquivo **`iniciar_arena.bat`**.
- **Opção B (Terminal / Linha de Comando):**
  ```bash
  python run.py
  ```

### 2. Acessar a Plataforma
O navegador será aberto automaticamente em:
> **http://localhost:8000**

### 3. Acessos Pré-cadastrados no Banco SQLite:
O banco de dados SQLite (`arena.db`) é inicializado automaticamente com o ecossistema pronto para uso:
- **Administrador (UFMG Hub):**
  - **Iniciativa:** `UFMG Hub`
  - **Senha:** `admin123`
- **Iniciativas Competidoras (EJs & Competição):**
  - **Engrenagem Jr.:** Senha `123456`
  - **Fórmula Tesla UFMG:** Senha `123456`
  - **Inova Consultoria Jr.:** Senha `123456`
  - **Baja UFMG:** Senha `123456`
*(Você também pode cadastrar novas iniciativas normalmente na tela de cadastro!)*

## 🚀 Funcionalidades Principais da Plataforma

### 1. 📢 Central MeC | Briefings Oficiais & Atividades Mensais (NOVO!)
Desenvolvida sob medida para a equipe do **Mercado em Conexão (MeC)** e lideranças das iniciativas da UFMG:

- **Briefings Oficiais Estruturados por Fase:**
  - Identificação clara da fase da campanha (ex: *Fase 1 · Aquecimento*, *Fase 2 · Inscrições*, *Fase 3 · Reta Final*).
  - Pílula de status (*Ativo / Vigente*, *Em Breve*, *Encerrado*).
  - Descrição da missão e objetivo da comunicação para a comunidade discente.
  - **Diretrizes e Requisitos:** Regras claras de formato (mínimo de cards, templates oficiais, clareza).
  - **Hashtags com Cópia Rápida em 1 Clique:** Bloco com marcações e hashtags oficiais (`@mercadoemconexao @ufmghub #ArenaMeC #MercadoEmConexao #UFMGInovadora`) e botão de cópia instantânea para a área de transferência do celular ou desktop.
  - **Kit de Artes & Mídia:** Botão com link direto para pastas do Google Drive ou Canva com os logotipos oficiais, molduras de stories e templates editáveis.
  - **Bônus de Criatividade:** Destaque de pontos extras para os conteúdos de maior qualidade e engajamento.

- **📅 Cronograma de Atividades Mensais:**
  - Linha do tempo visual com badges de dia e mês (ex.: `05/10`, `14/10`, `22/10`).
  - Categoria da atividade (*Divulgação*, *Presencial*, *Oficinas*, *Feira*).
  - Local físico exato no campus da UFMG (ex.: *Praça de Serviços*, *Escola de Engenharia*).
  - Pontuação associada a cada marco (ex.: `+2 pts por inscrição`, `Até +40 pts presencial`, `+1 pt por visitante`).
  - Badges de andamento (*Acontecendo Agora*, *Próxima Atividade*).

- **📜 Regras & Edital Oficial:**
  - Visualização rápida da tabela de pontuação oficial 16.5, regras de comprovação, critérios de validação e prazos de envio.

---

### 2. 🏆 Ranking Geral com Pódio Olímpico 3D
- **Pódio Olímpico 3D:** Destaque visual elevado para os três primeiros colocados (🥇 1º Ouro, 🥈 2º Prata, 🥉 3º Bronze).
- **Métricas em Tempo Real:** Líder atual, total de pontos em disputa, ações validadas e total de iniciativas.
- **Card "Você está aqui":** Destaque personalizado para a iniciativa logada com sua colocação atual, pontuação e quantos pontos faltam para ultrapassar o concorrente à frente.
- **Filtro por Categorias:** Filtre instantaneamente entre *Todas as Iniciativas*, *Empresas Juniores (EJs)*, *Equipes de Competição* e *Outros*.
- **Busca Rápida:** Campo de pesquisa instantânea por nome da iniciativa ou representante.
- **Extrato Detalhado de Pontuação:** Cada card de iniciativa pode ser expandido para visualizar o detalhamento exato dos pontos:
  - 📱 Redes Sociais (Stories, Posts, Carrosséis, Reels)
  - 👥 Inscrições da Iniciativa (com barra de progresso e respeito ao teto oficial de 200 pts)
  - 📋 Formulário de Pesquisa
  - 🏛️ Ações Presenciais
  - 🎤 Participação em Palestras
  - 🎪 Visitas Reais na Feira
  - ⚡ Participação nos Challenges
  - ✨ Ações Especiais e Pontos Avulsos

---

### 3. 📱 Registro de Ações pelas Iniciativas
Conforme a tabela oficial **16.5 (Pontuação base por ação)**:

| Ação | Pontuação | Condição do Briefing |
| :--- | :---: | :--- |
| **Compartilhamento de story oficial** | `+5 pts` | Conforme limite do briefing |
| **Story autoral** | `+10 pts` | Conteúdo próprio e aderente à missão |
| **Publicação estática no feed** | `+30 pts` | Peça própria ou adaptação autorizada |
| **Carrossel autoral** | `+50 pts` | Mínimo de 3 cards com conteúdo informativo |
| **Reel ou vídeo autoral** | `+100 pts` | Conteúdo original com mensagem clara |
| **Ações Especiais Criadas pelo Admin** | Variável | Definida na criação da tarefa |

- **Condições Visíveis:** Cada card exibe a regra oficial para evitar envios fora das normas.
- **Validação em Tempo Real:** Campo de URL com detecção automática de links válidos (verde) ou incompletos (vermelho).
- **Barra Flutuante:** Cálculo dinâmico do somatório de pontos a enviar antes da confirmação.

---

### 4. 📋 Minhas Entregas (Histórico Transparente com ID Único e Auditoria)
- **🏷️ ID Único por Ação (`#ACT-YYMMDD-XXXX`):** Cada envio (story, post, reel, carrossel, ação) recebe automaticamente um identificador único exclusivo e imutável (ex.: `#ACT-260927-R812`).
  - **Cópia em 1 Clique:** Badge interativo que copia o código diretamente para a área de transferência ao clicar, facilitando o suporte e a comunicação com a organização.
- **⏰ Data e Horário Exatos com Segundos:** Exibição precisa (`📅 Registrado em: DD/MM/AAAA às HH:mm:ss`) gravada no horário oficial de Brasília e sincronizada tanto na tela quanto diretamente nas células da planilha do Google Sheets.
- **Pílulas de status:** `Aguardando Validação` (amarelo), `Validada` (verde) e `Recusada` (vermelho).
- **Auditoria de Revisão:** Quando validado ou recusado, exibe exatamente o horário da análise (`Revisado em: DD/MM/AAAA às HH:mm:ss`).
- **Motivo da Recusa Transparente:** Se o administrador recusar um link, a justificativa (ex.: *"Conta privada"*, *"Faltou marcar @mercadoemconexao"*) aparece visível para que a iniciativa possa corrigir e reenviar.

---

### 5. ⚙️ Painel de Gestão do Administrador (UFMG Hub & MeC)

#### A) Validação Ágil de Links & Busca Instantânea por ID
- **🔍 Campo de Busca Rápida:** Filtre instantaneamente as entregas digitando o **ID da Ação** (ex.: `#ACT-260927`), o **nome da iniciativa** ou o **tipo de tarefa**.
- **Contador em tempo real** de links pendentes.
- **Filtro por status** (Aguardando validação, validadas, recusadas) e por iniciativa.
- **Badges com Cópia Rápida:** O administrador visualiza o ID único e o carimbo de data/hora completo de cada envio.
- **Botões Ágeis:** **Aprovar**, **Recusar** (com seleção rápida do motivo ou texto personalizado) e **Desfazer**.

#### B) 📌 Gestão de Briefings & Cronograma da MeC
- **Publicar Briefing Oficial:** Cadastro de novos briefings com identificador único (`#BRF-...`), fase, vigência, diretrizes, tags, link de Drive/Canva de artes e bônus.
- **Adicionar Atividade Mensal:** Cadastro de datas-chave, feiras, palestras e blitzes com identificador único (`#CRN-...`), data, local, pontuação e descrição.
- **Edição e Exclusão Segura:** Permite remover briefings e eventos passados sincronizando em tempo real com o Google Sheets.

#### C) Lançamento de Presença e Métricas do Evento
- **Inscrições Válidas:** `2 pontos` por inscrição (com controle automático do teto de 200 pontos por iniciativa na campanha).
- **Formulário de Pesquisa:** `1 ponto` por resposta atribuída.
- **Participação nas Palestras:** `1 ponto` por pessoa presente.
- **Presença Real na Feira:** `1 ponto` por pessoa inscrita que compareceu.
- **Participação nos Challenges:** `1 ponto` por pessoa nos challenges.
- **Ação Presencial Aprovada:** Atribuição de **até 40 pontos** com descrição da ação e data.

#### D) ✨ Criação de Novas Ações Dinâmicas (Super Flexibilidade!)
- **Lançamento Avulso de Pontos:** O administrador pode premiar qualquer iniciativa por qualquer atividade extraordinária (ex.: *"Vencedor da Dinâmica de Estande"*, *"Desafio Relâmpago de Pitch"*), escolhendo entre pontuação fixa total ou multiplicador (Quantidade × Pontos por unidade).
- **Nova Tarefa de Catálogo:** O administrador pode cadastrar novas tarefas no catálogo (ex.: *"Vídeo no TikTok"*, *"Post no LinkedIn"*). A nova tarefa passa a aparecer imediatamente na tela de envio de todas as iniciativas para registrarem com link!

#### E) Histórico, Auditoria & Estorno
- **🏷️ ID Único por Lançamento (`#LNC-YYMMDD-XXXX`):** Cada pontuação avulsa ou métrica de presença lançada recebe seu próprio ID de auditoria.
- **Log cronológico** com data e hora completas de todas as pontuações lançadas.
- **Botão Estornar Lançamento:** Se o administrador cometeu algum erro de digitação, pode cancelar o lançamento com 1 clique e a pontuação é recalculada no ranking imediatamente.

#### F) 🛠️ Diagnóstico, Integridade da Base & Anti-Fraude (NOVO!)
- **🛡️ Prevenção de Fraude & Deduplicação de Links:** O sistema higieniza parâmetros de rastreamento (`utm_source`, `igsh`, etc.) e impede que a mesma publicação seja cadastrada mais de uma vez (por uma ou por equipes diferentes).
- **✨ Reparar e Formatar Datas da Planilha com 1 Clique:** Ferramenta que varre todas as abas e converte qualquer timestamp numérico antigo (`1790530...`) em data e hora humana legível (`DD/MM/AAAA HH:MM:SS`), mantendo o banco de dados limpo e fácil de auditar.
- **📥 Backup Completo em JSON:** Exportação instantânea de todos os dados de iniciativas, pontuações, entregas e briefings para contingência offline.
- **⚡ Escrita Atômica em Bloco:** Atualizações em linha única que reduzem o consumo de cotas do Google Sheets e aumentam a velocidade em até 70%.
- **🔄 Retry Automático com Backoff:** Resiliência contra oscilações de Wi-Fi ou cold start do servidor Google com até 2 tentativas automáticas transparentes.

---

## 🎨 Identidade Visual e Recursos de Marca

- **Paleta Oficial:** Âmbar vibrante (`#F6A21C`), Laranja profundo (`#EC6E10`), Laranja Queimado (`#C84A0C`), Azul Marinho UFMG Hub (`#004B76`), e Azul Engenharia UFMG (`#549EB7`).
- **Tipografia:** Google Fonts `Montserrat` (títulos marcantes), `Lexend` (especificada no manual oficial do Hub) e `Inter` (leitura de dados).
- **Logotipos Embutidos:** O logo oficial do **Mercado em Conexão** e do **UFMG Hub** estão embutidos em alta resolução (base64 otimizado), funcionando com carregamento ultrarrápido tanto online quanto offline.
- **Tema Escuro e Claro:** Suporte refinado a ambos os modos de visualização.

---

## 📦 Como Publicar no Google Apps Script (Passo a Passo)

### 1. Criar o Projeto no Google Drive / Sheets
1. Abra o [Google Drive](https://drive.google.com) ou crie uma nova planilha no [Google Sheets](https://sheets.new).
2. No menu superior da planilha, clique em **Extensões > Apps Script**.
3. Dê um nome ao projeto (ex.: `Arena Mercado em Conexão`).

### 2. Copiar o Código Backend
1. No editor do Apps Script, selecione o arquivo `Código.gs` (ou `Code.gs`).
2. Apague qualquer código existente e **cole todo o conteúdo de [Code.gs](Code.gs)** (ou [Code-codigo-novo.txt](Code-codigo-novo.txt)).
3. Salve o arquivo (`Ctrl + S`).

### 3. Copiar o Código Frontend
1. No menu lateral esquerdo do Apps Script, clique no ícone **+** ao lado de Arquivos e escolha **HTML**.
2. Dê o nome exato de `Index` (o Apps Script criará `Index.html`).
3. Apague todo o conteúdo padrão e **cole todo o conteúdo de [Index.html](Index.html)** (ou [Index-codigo-novo.txt](Index-codigo-novo.txt)).
4. Salve o arquivo (`Ctrl + S`).

### 4. Inicializar a Planilha
1. No topo do editor do Apps Script, no seletor de funções, selecione a função **`configurar`**.
2. Clique no botão **Executar** (`▶`).
3. Conceda as permissões de acesso solicitadas pelo Google (clique em *Avançado > Acessar projeto (não seguro)*).
4. A função criará automaticamente na sua planilha as 6 abas estruturadas:
   - `Iniciativas`
   - `Entregas`
   - `Avisos`
   - `AcoesCatalogo`
   - `Briefings` (NOVO!)
   - `Cronograma` (NOVO!)

### 5. Implantar como App da Web
1. No canto superior direito, clique em **Implantar > Nova implantação**.
2. Clique no ícone de engrenagem ao lado de "Tipo" e escolha **App da Web**.
3. Preencha as configurações:
   - **Descrição:** `Versão Final Arena Gamificação`
   - **Executar como:** `Eu (seu e-mail)`
   - **Quem pode acessar:** `Qualquer pessoa` *(essencial para que as EJs e equipes possam acessar e registrar)*
4. Clique em **Implantar** e copie a **URL do App da Web**.

### 6. Criar a Conta de Administrador
1. Acesse o link do App da Web que você copiou.
2. Na tela inicial, clique em **Cadastrar Iniciativa**.
3. Cadastre exatamente com o nome:
   - **Nome da iniciativa:** `UFMG Hub`
   - **Categoria:** `Projeto de Extensão / Coletivo` ou `Outro`
   - **Representante:** `Gestão Hub`
   - **Cargo:** `Administrador`
   - **Rede Social:** `@ufmghub`
   - **Senha:** *(crie sua senha mestra de admin)*
4. Pronto! O sistema reconhece o nome `UFMG Hub` e habilita automaticamente a aba **Painel do Hub (Admin)** para essa conta.

---

## 💻 Teste Local Imediato (Sem Apps Script)

O aplicativo conta com um motor de simulação inteligente integrado:
- Se você abrir o arquivo **`Index.html`** diretamente no seu navegador (dois cliques no arquivo), ele carrega automaticamente em modo de demonstração com iniciativas de exemplo (*Engrenagem Jr.*, *Fórmula Tesla UFMG*, *Inova Jr.*, *Baja UFMG* e *UFMG Hub*).
- Você pode navegar pelo ranking, testar a nova Central MeC com briefings e cronograma mensal, registrar ações, validar como admin e testar todas as operações localmente antes mesmo de subir para o Google!

---

Desenvolvido com foco em solidez, estética de ponta e facilidade de operação para o **UFMG Hub** e **Mercado em Conexão**! 🚀
