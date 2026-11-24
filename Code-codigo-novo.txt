/**
 * ARENA | Mercado em Conexão
 * Gamificação de iniciativas (EJs e Equipes de Competição) — backend Google Apps Script + Google Sheets.
 *
 * Como publicar:
 * 1) Copie o conteúdo deste arquivo para 'Code.gs' no Google Apps Script.
 * 2) Copie o conteúdo de 'Index-codigo-novo.txt' para 'Index.html' no Google Apps Script.
 * 3) Rode a função configurar() uma vez pelo editor para inicializar as abas da planilha.
 * 4) Implantar > Nova implantação > App da Web
 *    Executar como: Eu (sua conta) | Quem pode acessar: Qualquer pessoa.
 * 5) Acesse o link publicado e cadastre a iniciativa "UFMG Hub" com sua senha (ela se torna administradora automaticamente).
 */

// ============================== CONFIGURAÇÃO ==============================

var CONFIG = {
  ADMIN_NOME: 'UFMG Hub',                 // Iniciativa com este nome vira administradora da Arena
  NOME_PLANILHA: 'Arena | Mercado em Conexão (dados)',
  PONTOS_POR_INSCRICAO: 2,                // Conforme tabela oficial: 2 pontos por inscrição válida
  LIMITE_PONTOS_INSCRICAO: 200,           // Limite oficial da campanha: 200 pontos para inscrições
  PONTOS_POR_RESPOSTA: 1,                 // Formulário de pesquisa: 1 ponto por resposta
  PONTOS_POR_PALESTRA: 1,                 // Presença nas palestras: 1 ponto por pessoa
  PONTOS_POR_FEIRA: 1,                    // Presença real na feira: 1 ponto por pessoa
  PONTOS_POR_CHALLENGE: 1,                // Participação nos challenges: 1 ponto por pessoa
  MAX_PONTOS_PRESENCIAL: 40,              // Ação presencial aprovada: até 40 pontos
  // Duração (em horas) do aviso destacado na página inicial
  HORAS: { tarefa: 72, presencial: 48, inscricoes: 48, formulario: 48, palestras: 48, feira: 48, challenges: 48, avulso: 48 },
  // Edital da Arena: cole aqui a URL do PDF quando disponível (deixe vazio para exibir "Em breve")
  EDITAL_URL: '',
  SESSAO_DIAS: 30,                        // Duração do login salvo no navegador
  MARCACAO: 'Não esqueça de marcar a @mercadoemconexao!',
  TAREFA_PADRAO: 'Não há entregas sugeridas para essa semana, mas qualquer divulgação extra pode gerar bônus de pontuação!',
  MAX_LINKS_POR_ENVIO: 60
};

// Tarefas base de divulgação que as iniciativas podem registrar (Tabela Oficial 16.5)
var TAREFAS_BASE = [
  { id: 'story_oficial', nome: 'Compartilhamento de story oficial', pontos: 5, condicao: 'Conforme limite do briefing', icone: 'story' },
  { id: 'story_autoral', nome: 'Story autoral', pontos: 10, condicao: 'Conteúdo próprio e aderente à missão', icone: 'story' },
  { id: 'feed_estatico', nome: 'Publicação estática no feed', pontos: 30, condicao: 'Peça própria ou adaptação autorizada', icone: 'post' },
  { id: 'carrossel', nome: 'Carrossel autoral', pontos: 50, condicao: 'Mínimo de 3 cards com conteúdo informativo', icone: 'carousel' },
  { id: 'reel', nome: 'Reel ou vídeo autoral', pontos: 100, condicao: 'Conteúdo original com mensagem clara', icone: 'reel' }
];

// Regras oficiais da Arena
var REGRAS = [
  'Perfil Público: Mantenha a conta da iniciativa pública durante toda a competição.',
  'Marcação Obrigatória: Sempre marque o perfil oficial @mercadoemconexao.',
  'Post Ativo: Não apague nem arquive a publicação do Feed após o envio.',
  'Respeito e Ética: O conteúdo não pode conter palavrões, termos ofensivos ou preconceituosos.',
  'Validação no Prazo: Envie o link do post dentro do prazo de cada tarefa para homologação dos pontos.',
  'Limite de Inscrições: A pontuação de inscrições atribuídas à iniciativa tem teto máximo de 200 pontos na campanha.'
];

// Contagens de participação no evento gerenciadas pelo administrador
var CONTAGENS = {
  inscricoes: { rotulo: 'Inscrições atribuídas', pontos: CONFIG.PONTOS_POR_INSCRICAO, limite: CONFIG.LIMITE_PONTOS_INSCRICAO },
  formulario: { rotulo: 'Respostas no formulário de pesquisa', pontos: CONFIG.PONTOS_POR_RESPOSTA },
  palestras: { rotulo: 'Presença nas palestras', pontos: CONFIG.PONTOS_POR_PALESTRA },
  feira: { rotulo: 'Presença real na feira de carreiras', pontos: CONFIG.PONTOS_POR_FEIRA },
  challenges: { rotulo: 'Participação nos challenges', pontos: CONFIG.PONTOS_POR_CHALLENGE }
};

// Estrutura das abas na planilha de banco de dados
var ABAS = {
  Iniciativas: ['id', 'nome', 'tipo', 'representante', 'cargo', 'redeSocial', 'salt', 'hash', 'criadoEm', 'admin'],
  Entregas: ['id', 'iniciativaId', 'tarefaId', 'tarefaNome', 'pontos', 'url', 'status', 'motivoRecusa', 'criadoEm', 'revisadoEm'],
  Avisos: ['id', 'tipo', 'criadoEm', 'expiraEm', 'iniciativaId', 'pontos', 'dados', 'status'],
  AcoesCatalogo: ['id', 'nome', 'pontos', 'tipo', 'descricao', 'condicao', 'criadoEm', 'ativo'],
  Briefings: ['id', 'titulo', 'fase', 'periodo', 'descricao', 'diretrizes', 'linkDrive', 'hashtags', 'bonus', 'status', 'criadoEm'],
  Cronograma: ['id', 'data', 'titulo', 'local', 'tipo', 'pontos', 'descricao', 'status', 'criadoEm'],
  MetricasEntregas: ['id', 'entregaId', 'iniciativaId', 'iniciativaNome', 'tarefaId', 'tarefaNome', 'tipoMidia', 'periodo', 'periodoRotulo', 'pontos', 'alcance', 'engajamento', 'comprovanteUrl', 'observacoes', 'status', 'motivoRecusa', 'criadoEm', 'revisadoEm']
};

// ============================== ENTRADA WEB ==============================

function doGet() {
  return HtmlService.createHtmlOutputFromFile('Index')
    .setTitle('Arena | Mercado em Conexão')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1, viewport-fit=cover')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

/** Rode uma vez pelo editor do Apps Script para criar/atualizar as abas da planilha e formatar datas. */
function configurar() {
  var ss = planilha_();
  Object.keys(ABAS).forEach(function (nome) { aba_(ss, nome); });
  segredo_();
  repararDatasLegadas_();
  Logger.log('Planilha configurada e higienizada com sucesso: ' + ss.getUrl());
  return ss.getUrl();
}

// ============================== API CENTRAL ==============================

/** Ponto único de entrada chamado pelo cliente frontend (google.script.run.api). */
function api(acao, dados, token) {
  dados = dados || {};
  try {
    switch (acao) {
      // Autenticação
      case 'cadastrar': return comLock_(function () { return cadastrar_(dados); });
      case 'entrar': return entrar_(dados);

      // Painel principal e tarefas
      case 'painel': return painel_(usuario_(token));
      case 'enviarTarefas': return comLock_(function () { return enviarTarefas_(usuario_(token), dados); });
      case 'reenviarEntrega': return comLock_(function () { return reenviarEntrega_(usuario_(token), dados); });

      // Área administrativa do UFMG Hub
      case 'admin': return adminDados_(admin_(token));
      case 'validarEntrega': return comLock_(function () { return validarEntrega_(admin_(token), dados); });
      case 'validarEntregasLote': return comLock_(function () { return validarEntregasLote_(admin_(token), dados); });
      case 'publicarTarefaHub': return comLock_(function () { return publicarTarefaHub_(admin_(token), dados); });
      case 'publicarPresencial': return comLock_(function () { return publicarPresencial_(admin_(token), dados); });
      case 'publicarInscricoes': return comLock_(function () { return publicarContagem_(admin_(token), dados, 'inscricoes'); });
      case 'publicarFormulario': return comLock_(function () { return publicarContagem_(admin_(token), dados, 'formulario'); });
      case 'publicarPalestras': return comLock_(function () { return publicarContagem_(admin_(token), dados, 'palestras'); });
      case 'publicarFeira': return comLock_(function () { return publicarContagem_(admin_(token), dados, 'feira'); });
      case 'publicarChallenges': return comLock_(function () { return publicarContagem_(admin_(token), dados, 'challenges'); });

      // Novas ações dinâmicas criadas pelo Admin
      case 'publicarAcaoAvulsa': return comLock_(function () { return publicarAcaoAvulsa_(admin_(token), dados); });
      case 'criarAcaoCatalogo': return comLock_(function () { return criarAcaoCatalogo_(admin_(token), dados); });
      case 'removerAcaoCatalogo': return comLock_(function () { return removerAcaoCatalogo_(admin_(token), dados); });
      case 'cancelarAviso': return comLock_(function () { return cancelarAviso_(admin_(token), dados); });

      // Gestão de Briefings e Atividades do Mês (MeC)
      case 'salvarBriefing': return comLock_(function () { return salvarBriefing_(admin_(token), dados); });
      case 'removerBriefing': return comLock_(function () { return removerBriefing_(admin_(token), dados); });
      case 'salvarCronograma': return comLock_(function () { return salvarCronograma_(admin_(token), dados); });
      case 'removerCronograma': return comLock_(function () { return removerCronograma_(admin_(token), dados); });

      // Diagnóstico e Auditoria da Base
      case 'repararDatas': return comLock_(function () { return repararDatasLegadas_(admin_(token)); });
      case 'registrarMetricaEntrega': return comLock_(function () { return registrarMetricaEntrega_(usuario_(token), dados); });
      case 'validarMetricaEntrega': return comLock_(function () { return validarMetricaEntrega_(admin_(token), dados); });
      case 'validarMetricasLote': return comLock_(function () { return validarMetricasLote_(admin_(token), dados); });

      default: throw erro_('Ação desconhecida: ' + acao);
    }
  } catch (e) {
    if (e && e.usuario) return { erro: e.message, sair: !!e.sair };
    console.error(e);
    return { erro: e && e.message ? e.message : 'Algo deu errado no servidor. Tente de novo em instantes.' };
  }
}

// ============================== CADASTRO & LOGIN ==============================

function cadastrar_(d) {
  var nome = texto_(d.nome, 'Nome da iniciativa', 80, true);
  var tipo = texto_(d.tipo, 'Tipo de iniciativa', 40, false) || 'Empresa Júnior';
  var representante = texto_(d.representante, 'Nome do representante', 80, true);
  var cargo = texto_(d.cargo, 'Cargo do representante', 60, true);
  var rede = texto_(d.redeSocial, 'Rede social da iniciativa', 150, true);
  var senha = String(d.senha || '');
  if (senha.length < 6) throw erro_('A senha precisa ter pelo menos 6 caracteres.');
  if (senha.length > 100) throw erro_('Senha longa demais.');

  var inis = lerTudo_('Iniciativas');
  var chave = normalizar_(nome);
  if (inis.some(function (u) { return normalizar_(u.nome) === chave; })) {
    throw erro_('Já existe uma iniciativa cadastrada com o nome "' + nome + '". Se você já possui cadastro, escolha "Entrar".');
  }

  var salt = Utilities.getUuid();
  var agora = new Date();
  var criadoEmFormatado = Utilities.formatDate(agora, "America/Sao_Paulo", "dd/MM/yyyy HH:mm:ss");
  var u = {
    id: Utilities.getUuid(),
    nome: nome,
    tipo: tipo,
    representante: representante,
    cargo: cargo,
    redeSocial: rede,
    salt: salt,
    hash: hashSenha_(senha, salt),
    criadoEm: criadoEmFormatado,
    admin: chave === normalizar_(CONFIG.ADMIN_NOME) ? 'sim' : ''
  };

  inserir_('Iniciativas', u);
  return { token: gerarToken_(u.id), nome: u.nome, admin: ehAdmin_(u) };
}

function entrar_(d) {
  var chave = normalizar_(d.nome);
  var senha = String(d.senha || '');
  var u = lerTudo_('Iniciativas').filter(function (x) { return normalizar_(x.nome) === chave; })[0];
  if (!u || hashSenha_(senha, u.salt) !== u.hash) {
    throw erro_('Nome da iniciativa ou senha incorretos.');
  }
  return { token: gerarToken_(u.id), nome: u.nome, admin: ehAdmin_(u) };
}

// ============================== PAINEL PRINCIPAL ==============================

function painel_(me) {
  var agora = Date.now();
  var inis = lerTudo_('Iniciativas');
  var entregas = lerTudo_('Entregas');
  var avisos = lerTudo_('Avisos');
  var catalogo = lerTudo_('AcoesCatalogo');
  var porId = mapa_(inis);

  // Tarefas disponíveis (base + catálogo dinâmico de links criado pelo admin)
  var tarefasDisponiveis = obterTarefas_(catalogo);

  // Tarefa do Hub em vigor (a mais recente ativa)
  var tarefaAtiva = avisos.filter(function (a) { return a.tipo === 'tarefa' && a.status !== 'cancelado'; })
    .sort(function (a, b) { return num_(b.criadoEm) - num_(a.criadoEm); })[0];
  var tarefaHub = null;
  if (tarefaAtiva && num_(tarefaAtiva.expiraEm) > agora) {
    tarefaHub = { dados: json_(tarefaAtiva.dados), criadoEm: num_(tarefaAtiva.criadoEm), expiraEm: num_(tarefaAtiva.expiraEm) };
  }

  // Avisos ativos acima do feed (não expirados e não cancelados)
  var ativos = avisos.filter(function (a) {
    return a.tipo !== 'tarefa' && a.status !== 'cancelado' && timestampMs_(a.expiraEm) > agora;
  })
  .sort(function (a, b) { return timestampMs_(b.criadoEm) - timestampMs_(a.criadoEm); })
  .map(function (a) { return avisoPublico_(a, porId); });

  // Métricas de entregas da iniciativa
  var todasMetricas = lerTudo_('MetricasEntregas');
  var metricasPorEntrega = {};
  todasMetricas.filter(function (m) { return m.iniciativaId === me.id; }).forEach(function (m) {
    if (!metricasPorEntrega[m.entregaId]) metricasPorEntrega[m.entregaId] = [];
    metricasPorEntrega[m.entregaId].push({
      id: m.id,
      entregaId: m.entregaId,
      periodo: m.periodo,
      periodoRotulo: m.periodoRotulo,
      tipoMidia: m.tipoMidia,
      pontos: num_(m.pontos),
      alcance: num_(m.alcance),
      engajamento: num_(m.engajamento),
      comprovanteUrl: m.comprovanteUrl,
      observacoes: m.observacoes || '',
      status: m.status,
      motivoRecusa: m.motivoRecusa || '',
      criadoEm: timestampMs_(m.criadoEm),
      dataHora: dataHoraString_(m.criadoEm),
      revisadoEm: timestampMs_(m.revisadoEm),
      revisadoDataHora: dataHoraString_(m.revisadoEm)
    });
  });

  // Entregas da própria iniciativa logada
  var minhas = entregas.filter(function (e) { return e.iniciativaId === me.id; })
    .sort(function (a, b) { return timestampMs_(b.criadoEm) - timestampMs_(a.criadoEm); })
    .map(function (e) {
      var isStory = (e.tarefaId || '').toLowerCase().indexOf('story') >= 0;
      return {
        id: e.id,
        tarefaId: e.tarefaId,
        tarefaNome: e.tarefaNome,
        pontos: num_(e.pontos),
        url: e.url,
        status: e.status,
        motivoRecusa: e.motivoRecusa || '',
        criadoEm: timestampMs_(e.criadoEm),
        dataHora: dataHoraString_(e.criadoEm),
        revisadoEm: timestampMs_(e.revisadoEm),
        revisadoDataHora: dataHoraString_(e.revisadoEm),
        tipoMidia: isStory ? 'story' : 'post',
        metricas: metricasPorEntrega[e.id] || []
      };
    });

  // Cálculo consolidado do ranking
  var rankingData = ranking_(inis, entregas, avisos);

  // Estatísticas gerais da Arena
  var totalPontosGeral = rankingData.reduce(function (acc, r) { return acc + r.pontos; }, 0);
  var totalValidadas = entregas.filter(function (e) { return e.status === 'validada'; }).length;

  return {
    me: {
      id: me.id,
      nome: me.nome,
      tipo: me.tipo || 'Empresa Júnior',
      representante: me.representante,
      cargo: me.cargo,
      redeSocial: me.redeSocial || '',
      admin: ehAdmin_(me)
    },
    ranking: rankingData,
    estatisticas: {
      totalIniciativas: rankingData.length,
      totalPontos: totalPontosGeral,
      totalValidadas: totalValidadas,
      liderNome: rankingData.length ? rankingData[0].nome : '—',
      liderPontos: rankingData.length ? rankingData[0].pontos : 0
    },
    tarefaHub: tarefaHub,
    avisos: ativos,
    regras: REGRAS,
    tarefas: tarefasDisponiveis,
    minhasEntregas: minhas,
    briefings: lerTudo_('Briefings').filter(function (b) { return b.status !== 'removido'; }).sort(function (a, b) { return num_(b.criadoEm) - num_(a.criadoEm); }),
    cronograma: lerTudo_('Cronograma').filter(function (c) { return c.status !== 'removido'; }).sort(function (a, b) { return String(a.data).localeCompare(String(b.data)); }),
    config: {
      marcacao: CONFIG.MARCACAO,
      tarefaPadrao: CONFIG.TAREFA_PADRAO,
      pontosPorInscricao: CONFIG.PONTOS_POR_INSCRICAO,
      limiteInscricoes: CONFIG.LIMITE_PONTOS_INSCRICAO
    },
    pontosPor: pontosPor_(),
    edital: CONFIG.EDITAL_URL || '',
    agora: agora
  };
}

// ============================== CÁLCULO DO RANKING ==============================

function ranking_(inis, entregas, avisos) {
  var map = {};
  inis.forEach(function (u) {
    if (!ehAdmin_(u)) {
      map[u.id] = {
        id: u.id,
        nome: u.nome,
        tipo: u.tipo || 'Empresa Júnior',
        representante: u.representante,
        cargo: u.cargo,
        redeSocial: u.redeSocial || '',
        pontos: 0,
        pontosValidados: 0,
        pontosPendentes: 0,
        totalEntregas: 0,
        breakdown: {
          redes: 0,
          inscricoes: 0,
          formulario: 0,
          presencial: 0,
          palestras: 0,
          feira: 0,
          challenges: 0,
          avulso: 0,
          metricas: 0
        }
      };
    }
  });

  // 1. Somatório das entregas de tarefas por link
  entregas.forEach(function (e) {
    var rec = map[e.iniciativaId];
    if (!rec) return;
    rec.totalEntregas++;
    var pts = num_(e.pontos);
    if (e.status === 'validada') {
      rec.pontos += pts;
      rec.pontosValidados += pts;
      rec.breakdown.redes += pts;
    } else if (e.status === 'pendente') {
      // No modelo dinâmico da Arena, pontuação provisória entra no ranking até eventual recusa
      rec.pontos += pts;
      rec.pontosPendentes += pts;
      rec.breakdown.redes += pts;
    }
  });

  // 2. Somatório das pontuações de avisos/lançamentos atribuídos pelo Administrador
  avisos.forEach(function (a) {
    if (a.status === 'cancelado') return;
    var d = json_(a.dados);
    if (d.cancelado) return;
    var rec = map[a.iniciativaId];
    if (!rec) return;

    var pts = num_(a.pontos);
    var tipo = a.tipo;

    if (tipo === 'inscricoes') {
      // Teto oficial de 200 pontos de inscrições por iniciativa
      var atual = rec.breakdown.inscricoes;
      var restante = Math.max(0, CONFIG.LIMITE_PONTOS_INSCRICAO - atual);
      var somar = Math.min(pts, restante);
      rec.breakdown.inscricoes += somar;
      rec.pontos += somar;
      rec.pontosValidados += somar;
    } else if (tipo === 'formulario') {
      rec.breakdown.formulario += pts;
      rec.pontos += pts;
      rec.pontosValidados += pts;
    } else if (tipo === 'presencial') {
      rec.breakdown.presencial += pts;
      rec.pontos += pts;
      rec.pontosValidados += pts;
    } else if (tipo === 'palestras') {
      rec.breakdown.palestras += pts;
      rec.pontos += pts;
      rec.pontosValidados += pts;
    } else if (tipo === 'feira') {
      rec.breakdown.feira += pts;
      rec.pontos += pts;
      rec.pontosValidados += pts;
    } else if (tipo === 'challenges') {
      rec.breakdown.challenges += pts;
      rec.pontos += pts;
      rec.pontosValidados += pts;
    } else if (tipo === 'avulso') {
      rec.breakdown.avulso += pts;
      rec.pontos += pts;
      rec.pontosValidados += pts;
    }
  });

  // 3. Somatório dos pontos bônus de métricas validadas (+10 post semana, +5 story 24h)
  var metricasTodas = lerTudo_('MetricasEntregas');
  metricasTodas.forEach(function (m) {
    var rec = map[m.iniciativaId];
    if (!rec) return;
    var pts = num_(m.pontos);
    if (!rec.breakdown.metricas) rec.breakdown.metricas = 0;
    if (m.status === 'validada') {
      rec.pontos += pts;
      rec.pontosValidados += pts;
      rec.breakdown.metricas += pts;
    } else if (m.status === 'pendente') {
      rec.pontos += pts;
      rec.pontosPendentes += pts;
      rec.breakdown.metricas += pts;
    }
  });

  var lista = Object.keys(map).map(function (k) { return map[k]; });
  lista.sort(function (a, b) {
    return b.pontos - a.pontos || b.pontosValidados - a.pontosValidados || a.nome.localeCompare(b.nome, 'pt-BR');
  });

  return lista;
}

// ============================== REGISTRO DE TAREFAS ==============================

function enviarTarefas_(me, d) {
  if (ehAdmin_(me)) throw erro_('O administrador UFMG Hub não participa como competidor do ranking.');
  var itens = Array.isArray(d.itens) ? d.itens : [];
  var linhas = [];
  var agora = new Date();
  var criadoEmFormatado = Utilities.formatDate(agora, "America/Sao_Paulo", "dd/MM/yyyy HH:mm:ss");

  var catalogo = lerTudo_('AcoesCatalogo');
  var todasTarefas = obterTarefas_(catalogo);

  // Mapa de URLs já existentes no banco para deduplicação e prevenção de fraude
  var entregasExistentes = lerTudo_('Entregas');
  var mapaUrlsExistentes = {};
  entregasExistentes.forEach(function (e) {
    if (e.status !== 'recusada') {
      var uLimpa = limparUrl_(e.url);
      if (uLimpa) mapaUrlsExistentes[uLimpa] = { id: e.id, iniciativaId: e.iniciativaId, tarefaNome: e.tarefaNome };
    }
  });

  var urlsLote = {};

  itens.forEach(function (it) {
    var t = todasTarefas.filter(function (x) { return x.id === it.tarefaId; })[0];
    if (!t) return;
    (Array.isArray(it.urls) ? it.urls : []).forEach(function (urlBruta) {
      urlBruta = String(urlBruta || '').trim();
      if (!urlBruta) return;
      if (!urlValida_(urlBruta)) throw erro_('Link com formato inválido: ' + urlBruta.slice(0, 60));

      var urlCanonica = limparUrl_(urlBruta);
      if (urlsLote[urlCanonica]) {
        throw erro_('Você incluiu o mesmo link mais de uma vez no mesmo envio.');
      }
      urlsLote[urlCanonica] = true;

      if (mapaUrlsExistentes[urlCanonica]) {
        var anterior = mapaUrlsExistentes[urlCanonica];
        if (anterior.iniciativaId === me.id) {
          throw erro_('Você já registrou este link anteriormente (' + anterior.id + '). Aguarde a validação da equipe.');
        } else {
          throw erro_('Este link já foi registrado por outra iniciativa no sistema.');
        }
      }

      linhas.push({
        id: gerarIdAcao_(),
        iniciativaId: me.id,
        tarefaId: t.id,
        tarefaNome: t.nome,
        pontos: t.pontos,
        url: urlBruta,
        status: 'pendente',
        motivoRecusa: '',
        criadoEm: criadoEmFormatado,
        revisadoEm: ''
      });
    });
  });

  if (!linhas.length) throw erro_('Adicione pelo menos um link válido para pontuar.');
  if (linhas.length > CONFIG.MAX_LINKS_POR_ENVIO) throw erro_('Limite de envios por vez atingido. Envie em lotes menores.');

  inserirVarios_('Entregas', linhas);
  var total = linhas.reduce(function (s, l) { return s + l.pontos; }, 0);
  var p = painel_(me);
  p.enviado = { links: linhas.length, pontos: total };
  return p;
}

// ============================== ÁREA DO ADMINISTRADOR ==============================

function adminDados_(me) {
  var inis = lerTudo_('Iniciativas');
  var porId = mapa_(inis);

  var entregas = lerTudo_('Entregas')
    .sort(function (a, b) { return timestampMs_(b.criadoEm) - timestampMs_(a.criadoEm); })
    .map(function (e) {
      var u = porId[e.iniciativaId] || {};
      return {
        id: e.id,
        iniciativaId: e.iniciativaId,
        iniciativa: u.nome || '—',
        tipoIniciativa: u.tipo || 'Empresa Júnior',
        tarefaId: e.tarefaId,
        tarefaNome: e.tarefaNome,
        pontos: num_(e.pontos),
        url: e.url,
        status: e.status,
        motivoRecusa: e.motivoRecusa || '',
        criadoEm: timestampMs_(e.criadoEm),
        dataHora: dataHoraString_(e.criadoEm),
        revisadoEm: timestampMs_(e.revisadoEm),
        revisadoDataHora: dataHoraString_(e.revisadoEm)
      };
    });

  var historico = lerTudo_('Avisos')
    .sort(function (a, b) { return timestampMs_(b.criadoEm) - timestampMs_(a.criadoEm); })
    .map(function (a) { return avisoPublico_(a, porId); });

  var iniciativas = inis.filter(function (u) { return !ehAdmin_(u); })
    .map(function (u) {
      return {
        id: u.id,
        nome: u.nome,
        tipo: u.tipo || 'Empresa Júnior',
        representante: u.representante,
        cargo: u.cargo,
        redeSocial: u.redeSocial || ''
      };
    })
    .sort(function (a, b) { return a.nome.localeCompare(b.nome, 'pt-BR'); });

  var catalogo = lerTudo_('AcoesCatalogo')
    .filter(function (c) { return c.ativo !== 'nao'; })
    .map(function (c) {
      return {
        id: c.id,
        nome: c.nome,
        pontos: num_(c.pontos),
        tipo: c.tipo,
        condicao: c.condicao || '',
        descricao: c.descricao || '',
        criadoEm: num_(c.criadoEm)
      };
    });

  return {
    entregas: entregas,
    historico: historico,
    iniciativas: iniciativas,
    catalogo: catalogo,
    briefings: lerTudo_('Briefings').filter(function (b) { return b.status !== 'removido'; }).sort(function (a, b) { return num_(b.criadoEm) - num_(a.criadoEm); }),
    cronograma: lerTudo_('Cronograma').filter(function (c) { return c.status !== 'removido'; }).sort(function (a, b) { return String(a.data).localeCompare(String(b.data)); }),
    metricas: (function() {
      return lerTudo_('MetricasEntregas')
        .sort(function (a, b) { return timestampMs_(b.criadoEm) - timestampMs_(a.criadoEm); })
        .map(function (m) {
          return {
            id: m.id,
            entregaId: m.entregaId,
            iniciativaId: m.iniciativaId,
            iniciativaNome: m.iniciativaNome || (porId[m.iniciativaId] ? porId[m.iniciativaId].nome : '—'),
            tarefaId: m.tarefaId,
            tarefaNome: m.tarefaNome,
            tipoMidia: m.tipoMidia || 'post',
            periodo: m.periodo,
            periodoRotulo: m.periodoRotulo,
            pontos: num_(m.pontos),
            alcance: num_(m.alcance),
            engajamento: num_(m.engajamento),
            comprovanteUrl: m.comprovanteUrl || '',
            observacoes: m.observacoes || '',
            status: m.status || 'pendente',
            motivoRecusa: m.motivoRecusa || '',
            criadoEm: timestampMs_(m.criadoEm),
            dataHora: dataHoraString_(m.criadoEm),
            revisadoEm: timestampMs_(m.revisadoEm),
            revisadoDataHora: dataHoraString_(m.revisadoEm)
          };
        });
    })(),
    metricasKpis: (function() {
      var allM = lerTudo_('MetricasEntregas');
      var alc = 0, eng = 0, pend = 0, pts = 0;
      allM.forEach(function (m) {
        if (m.status === 'validada') {
          alc += num_(m.alcance);
          eng += num_(m.engajamento);
          pts += num_(m.pontos);
        } else if (m.status === 'pendente') {
          pend++;
        }
      });
      return {
        totalAlcance: alc,
        totalEngajamento: eng,
        pendentes: pend,
        totalPontos: pts,
        totalRelatorios: allM.length
      };
    })(),
    pontosPor: pontosPor_(),
    config: {
      limiteInscricoes: CONFIG.LIMITE_PONTOS_INSCRICAO,
      maxPresencial: CONFIG.MAX_PONTOS_PRESENCIAL
    },
    agora: Date.now()
  };
}

function validarEntrega_(me, d) {
  var status = String(d.status || '');
  if (['pendente', 'validada', 'recusada'].indexOf(status) < 0) throw erro_('Status de validação inválido.');
  var motivo = texto_(d.motivoRecusa, 'Motivo da recusa', 250, false);
  var agora = new Date();
  var revisadoEmFormatado = status === 'pendente' ? '' : Utilities.formatDate(agora, "America/Sao_Paulo", "dd/MM/yyyy HH:mm:ss");
  var ok = atualizar_('Entregas', d.id, {
    status: status,
    motivoRecusa: status === 'recusada' ? motivo : '',
    revisadoEm: revisadoEmFormatado
  });
  if (!ok) throw erro_('Entrega não encontrada no sistema.');
  return adminDados_(me);
}

function validarEntregasLote_(me, d) {
  var ids = Array.isArray(d.ids) ? d.ids : [];
  var status = String(d.status || 'validada');
  if (['validada', 'recusada'].indexOf(status) < 0) throw erro_('Status inválido para validação em lote.');
  var agora = new Date();
  var revisadoEmFormatado = Utilities.formatDate(agora, 'America/Sao_Paulo', 'dd/MM/yyyy HH:mm:ss');
  var rows = lerTudo_('Entregas');
  rows.forEach(function (e) {
    if (e.status === 'pendente' && (ids.length === 0 || ids.indexOf(e.id) >= 0)) {
      atualizar_('Entregas', e.id, {
        status: status,
        motivoRecusa: '',
        revisadoEm: revisadoEmFormatado
      });
    }
  });
  return adminDados_(me);
}

function reenviarEntrega_(me, d) {
  var eid = String(d.id || '');
  var novaUrl = String(d.novaUrl || '').trim();
  if (!urlValida_(novaUrl)) throw erro_('Informe um link público válido (ex.: https://instagram.com/p/...).');
  var urlCanon = limparUrl_(novaUrl);
  var agora = new Date();
  var dtStr = Utilities.formatDate(agora, 'America/Sao_Paulo', 'dd/MM/yyyy HH:mm:ss');

  var entrega = lerTudo_('Entregas').filter(function (e) { return e.id === eid; })[0];
  if (!entrega || entrega.iniciativaId !== me.id) throw erro_('Entrega não encontrada.');

  var outros = lerTudo_('Entregas').filter(function (e) { return e.id !== eid && e.status !== 'recusada'; });
  for (var i = 0; i < outros.length; i++) {
    if (limparUrl_(outros[i].url) === urlCanon) {
      if (outros[i].iniciativaId === me.id) {
        throw erro_('Você já registrou este link em outra ação ativa (' + outros[i].id + ').');
      } else {
        throw erro_('Este link já foi registrado por outra iniciativa no sistema.');
      }
    }
  }

  atualizar_('Entregas', eid, {
    url: novaUrl,
    status: 'pendente',
    motivoRecusa: '',
    criadoEm: dtStr,
    revisadoEm: ''
  });

  var p = painel_(me);
  p.enviado = { links: 1, pontos: num_(entrega.pontos) };
  return p;
}

function publicarTarefaHub_(me, d) {
  var dados = {
    sobre: texto_(d.sobre, 'Sobre o que publicar', 400, false),
    periodo: texto_(d.periodo, 'Período para publicar', 50, false),
    recomendacoes: texto_(d.recomendacoes, 'Recomendações do Hub', 400, false),
    bonus: texto_(d.bonus, 'Bônus', 400, false)
  };
  if (!dados.sobre && !dados.periodo && !dados.recomendacoes && !dados.bonus) {
    throw erro_('Preencha pelo menos um campo da tarefa semanal.');
  }
  novoAviso_('tarefa', '', 0, dados);
  return adminDados_(me);
}

function publicarPresencial_(me, d) {
  var ini = iniciativa_(d.iniciativaId);
  var oque = texto_(d.oque, 'O que foi a ação', 300, true);
  var quando = texto_(d.quando, 'Quando foi a ação', 150, true);
  var pontos = inteiro_(d.pontos, 'Pontuação da ação');
  if (pontos < 1) throw erro_('A pontuação deve ser maior que zero.');
  if (pontos > CONFIG.MAX_PONTOS_PRESENCIAL) {
    throw erro_('A pontuação de ação presencial aprovada tem limite de até ' + CONFIG.MAX_PONTOS_PRESENCIAL + ' pontos.');
  }
  var dados = { oque: oque, quando: quando, pontuacao: pontos };
  novoAviso_('presencial', ini.id, pontos, dados);
  return adminDados_(me);
}

function publicarContagem_(me, d, tipo) {
  var ini = iniciativa_(d.iniciativaId);
  var c = CONTAGENS[tipo];
  if (!c) throw erro_('Categoria de contagem não reconhecida.');
  var qtd = inteiro_(d.quantidade, c.rotulo);
  if (qtd <= 0) throw erro_('Informe uma quantidade positiva para ' + c.rotulo + '.');

  var pts = qtd * c.pontos;
  novoAviso_(tipo, ini.id, pts, { quantidade: qtd, pontosUnitarios: c.pontos });
  return adminDados_(me);
}

// Lançamento avulso de pontos criado pelo Administrador para qualquer ação
function publicarAcaoAvulsa_(me, d) {
  var ini = iniciativa_(d.iniciativaId);
  var titulo = texto_(d.titulo, 'Título ou nome da ação', 100, true);
  var descricao = texto_(d.descricao, 'Descrição ou justificativa', 300, false);
  var modo = d.modo === 'quantidade' ? 'quantidade' : 'fixo';
  var pontosFinal = 0;
  var qtd = 1;
  var unitario = 0;

  if (modo === 'quantidade') {
    qtd = inteiro_(d.quantidade, 'Quantidade');
    unitario = inteiro_(d.pontosUnitarios, 'Pontos por unidade');
    if (qtd <= 0 || unitario <= 0) throw erro_('Quantidade e pontos por unidade devem ser maiores que zero.');
    pontosFinal = qtd * unitario;
  } else {
    pontosFinal = inteiro_(d.pontos, 'Pontuação total');
    if (pontosFinal <= 0) throw erro_('A pontuação deve ser maior que zero.');
  }

  var dados = {
    titulo: titulo,
    descricao: descricao,
    modo: modo,
    quantidade: qtd,
    pontosUnitarios: unitario,
    quando: texto_(d.quando, 'Data ou momento', 100, false) || 'Durante a Arena'
  };

  novoAviso_('avulso', ini.id, pontosFinal, dados);
  return adminDados_(me);
}

// Criação de nova tarefa de catálogo pelo Administrador (para as iniciativas enviarem link)
function criarAcaoCatalogo_(me, d) {
  var nome = texto_(d.nome, 'Nome da tarefa', 80, true);
  var pontos = inteiro_(d.pontos, 'Pontos da tarefa');
  var condicao = texto_(d.condicao, 'Condição ou regra de validação', 250, true);
  var descricao = texto_(d.descricao, 'Descrição adicional', 300, false);
  if (pontos <= 0) throw erro_('Os pontos devem ser maiores que zero.');

  var id = 'custom_' + Utilities.getUuid().slice(0, 8);
  var agora = new Date();
  var criadoEmFormatado = Utilities.formatDate(agora, "America/Sao_Paulo", "dd/MM/yyyy HH:mm:ss");
  var obj = {
    id: id,
    nome: nome,
    pontos: pontos,
    tipo: 'link',
    descricao: descricao,
    condicao: condicao,
    criadoEm: criadoEmFormatado,
    ativo: 'sim'
  };

  inserir_('AcoesCatalogo', obj);
  return adminDados_(me);
}

function removerAcaoCatalogo_(me, d) {
  var id = texto_(d.id, 'ID da ação', 50, true);
  atualizar_('AcoesCatalogo', id, { ativo: 'nao' });
  return adminDados_(me);
}

// Cancelamento / estorno de um aviso ou lançamento
function cancelarAviso_(me, d) {
  var id = texto_(d.id, 'ID do aviso', 50, true);
  var ok = atualizar_('Avisos', id, { status: 'cancelado' });
  if (!ok) throw erro_('Registro de aviso não encontrado.');
  return adminDados_(me);
}

// ============================== BRIEFINGS & ATIVIDADES MENSAIS (MeC) ==============================

function salvarBriefing_(me, d) {
  var agora = new Date();
  var criadoEmFormatado = Utilities.formatDate(agora, "America/Sao_Paulo", "dd/MM/yyyy HH:mm:ss");
  var id = d.id ? String(d.id) : ('#BRF-' + Utilities.formatDate(agora, 'America/Sao_Paulo', 'yyMMdd') + '-' + ('0000' + Math.floor(Math.random() * 9999 + 1)).slice(-4));
  var titulo = texto_(d.titulo, 'Título do briefing', 120, true);
  var fase = texto_(d.fase, 'Fase ou mês', 60, false) || 'Geral';
  var periodo = texto_(d.periodo, 'Período', 60, false) || 'Durante a Arena';
  var descricao = texto_(d.descricao, 'Descrição do briefing', 1000, true);
  var diretrizes = texto_(d.diretrizes, 'Diretrizes de conteúdo', 1000, false) || '';
  var linkDrive = texto_(d.linkDrive, 'Link do Kit de Artes / Drive', 400, false) || '';
  var hashtags = texto_(d.hashtags, 'Hashtags e marcações', 250, false) || '@mercadoemconexao #ArenaMeC';
  var bonus = texto_(d.bonus, 'Bônus de pontuação', 250, false) || '';
  var status = d.status || 'ativo';

  var obj = {
    id: id,
    titulo: titulo,
    fase: fase,
    periodo: periodo,
    descricao: descricao,
    diretrizes: diretrizes,
    linkDrive: linkDrive,
    hashtags: hashtags,
    bonus: bonus,
    status: status,
    criadoEm: criadoEmFormatado
  };

  var existentes = lerTudo_('Briefings');
  var jaExiste = existentes.some(function (x) { return x.id === id; });
  if (jaExiste) {
    atualizar_('Briefings', id, obj);
  } else {
    inserir_('Briefings', obj);
  }
  return adminDados_(me);
}

function removerBriefing_(me, d) {
  var id = texto_(d.id, 'ID do briefing', 50, true);
  atualizar_('Briefings', id, { status: 'removido' });
  return adminDados_(me);
}

function salvarCronograma_(me, d) {
  var agora = new Date();
  var criadoEmFormatado = Utilities.formatDate(agora, "America/Sao_Paulo", "dd/MM/yyyy HH:mm:ss");
  var id = d.id ? String(d.id) : ('#CRN-' + Utilities.formatDate(agora, 'America/Sao_Paulo', 'yyMMdd') + '-' + ('0000' + Math.floor(Math.random() * 9999 + 1)).slice(-4));
  var data = texto_(d.data, 'Data da atividade', 40, true);
  var titulo = texto_(d.titulo, 'Título da atividade', 120, true);
  var local = texto_(d.local, 'Local ou formato', 100, false) || 'Campus Pampulha';
  var tipo = texto_(d.tipo, 'Tipo de atividade', 50, false) || 'Presencial';
  var pontos = texto_(d.pontos, 'Pontos associados', 50, false) || '';
  var descricao = texto_(d.descricao, 'Descrição da atividade', 500, false) || '';
  var status = d.status || 'proximo';

  var obj = {
    id: id,
    data: data,
    titulo: titulo,
    local: local,
    tipo: tipo,
    pontos: pontos,
    descricao: descricao,
    status: status,
    criadoEm: criadoEmFormatado
  };

  var existentes = lerTudo_('Cronograma');
  var jaExiste = existentes.some(function (x) { return x.id === id; });
  if (jaExiste) {
    atualizar_('Cronograma', id, obj);
  } else {
    inserir_('Cronograma', obj);
  }
  return adminDados_(me);
}

function removerCronograma_(me, d) {
  var id = texto_(d.id, 'ID da atividade', 50, true);
  atualizar_('Cronograma', id, { status: 'removido' });
  return adminDados_(me);
}

function novoAviso_(tipo, iniciativaId, pontos, dados) {
  var agora = new Date();
  var criadoEmFormatado = Utilities.formatDate(agora, "America/Sao_Paulo", "dd/MM/yyyy HH:mm:ss");
  var horas = CONFIG.HORAS[tipo] || 48;
  var expiraEmFormatado = Utilities.formatDate(new Date(agora.getTime() + horas * 3600 * 1000), "America/Sao_Paulo", "dd/MM/yyyy HH:mm:ss");
  inserir_('Avisos', {
    id: gerarIdLnc_(),
    tipo: tipo,
    criadoEm: criadoEmFormatado,
    expiraEm: expiraEmFormatado,
    iniciativaId: iniciativaId || '',
    pontos: pontos || 0,
    dados: JSON.stringify(dados || {}),
    status: 'ativo'
  });
}

function avisoPublico_(a, porId) {
  var u = porId[a.iniciativaId] || {};
  return {
    id: a.id,
    tipo: a.tipo,
    status: a.status || 'ativo',
    criadoEm: timestampMs_(a.criadoEm),
    dataHora: dataHoraString_(a.criadoEm),
    expiraEm: timestampMs_(a.expiraEm),
    iniciativaId: a.iniciativaId,
    iniciativa: u.nome || '',
    tipoIniciativa: u.tipo || 'Empresa Júnior',
    pontos: num_(a.pontos),
    dados: json_(a.dados)
  };
}

function obterTarefas_(catalogo) {
  var list = TAREFAS_BASE.slice();
  (catalogo || []).forEach(function (c) {
    if (c.ativo !== 'nao' && c.tipo === 'link') {
      list.push({
        id: c.id,
        nome: c.nome,
        pontos: num_(c.pontos),
        condicao: c.condicao || 'Conforme briefing',
        icone: 'custom',
        personalizada: true
      });
    }
  });
  return list;
}

function pontosPor_() {
  var o = {};
  Object.keys(CONTAGENS).forEach(function (k) { o[k] = CONTAGENS[k].pontos; });
  return o;
}

function iniciativa_(id) {
  var u = lerTudo_('Iniciativas').filter(function (x) { return x.id === id; })[0];
  if (!u || ehAdmin_(u)) throw erro_('Selecione uma iniciativa válida cadastrada.');
  return u;
}

// ============================== SESSÃO & SEGURANÇA ==============================

function usuario_(token) {
  var id = lerToken_(token);
  var u = id && lerTudo_('Iniciativas').filter(function (x) { return x.id === id; })[0];
  if (!u) { var e = erro_('Sua sessão expirou ou é inválida. Entre novamente.'); e.sair = true; throw e; }
  return u;
}

function admin_(token) {
  var u = usuario_(token);
  if (!ehAdmin_(u)) throw erro_('Função exclusiva do administrador (UFMG Hub).');
  return u;
}

function ehAdmin_(u) {
  return u && (String(u.admin) === 'sim' || normalizar_(u.nome) === normalizar_(CONFIG.ADMIN_NOME));
}

function gerarToken_(id) {
  var carga = id + '|' + (Date.now() + CONFIG.SESSAO_DIAS * 86400000);
  return Utilities.base64EncodeWebSafe(carga) + '.' + assinar_(carga);
}

function lerToken_(token) {
  if (!token || typeof token !== 'string' || token.indexOf('.') < 0) return null;
  var partes = token.split('.');
  var carga;
  try { carga = Utilities.newBlob(Utilities.base64DecodeWebSafe(partes[0])).getDataAsString(); } catch (e) { return null; }
  if (assinar_(carga) !== partes[1]) return null;
  var p = carga.split('|');
  if (Number(p[1]) < Date.now()) return null;
  return p[0];
}

function assinar_(texto) {
  return Utilities.base64EncodeWebSafe(Utilities.computeHmacSha256Signature(texto, segredo_()));
}

function segredo_() {
  var props = PropertiesService.getScriptProperties();
  var s = props.getProperty('ARENA_SEGREDO');
  if (!s) { s = Utilities.getUuid() + Utilities.getUuid(); props.setProperty('ARENA_SEGREDO', s); }
  return s;
}

function hashSenha_(senha, salt) {
  var h = salt + '::' + senha;
  for (var i = 0; i < 50; i++) {
    h = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, h + salt, Utilities.Charset.UTF_8)
      .map(function (b) { return ('0' + (b & 255).toString(16)).slice(-2); }).join('');
  }
  return h;
}

// ============================== OPERAÇÕES DE PLANILHA ==============================

function planilha_() {
  var props = PropertiesService.getScriptProperties();
  var id = props.getProperty('ARENA_PLANILHA_ID');
  if (id) {
    try { return SpreadsheetApp.openById(id); } catch (e) { /* se id inválido, recria/reconecta */ }
  }
  var ss = null;
  try { ss = SpreadsheetApp.getActiveSpreadsheet(); } catch (e) { ss = null; }
  if (!ss) ss = SpreadsheetApp.create(CONFIG.NOME_PLANILHA);
  props.setProperty('ARENA_PLANILHA_ID', ss.getId());
  return ss;
}

function aba_(ss, nome) {
  var sh = ss.getSheetByName(nome);
  var cols = ABAS[nome];
  if (!sh) {
    sh = ss.insertSheet(nome);
    sh.getRange(1, 1, 1, cols.length).setValues([cols]).setFontWeight('bold');
    sh.setFrozenRows(1);
  } else {
    // Migração transparente de cabeçalhos sem quebrar dados existentes
    var lastCol = sh.getLastColumn();
    if (lastCol < cols.length) {
      for (var i = lastCol; i < cols.length; i++) {
        sh.getRange(1, i + 1).setValue(cols[i]).setFontWeight('bold');
      }
    }
  }
  return sh;
}

var _cache = {};
function lerTudo_(nome) {
  if (_cache[nome]) return _cache[nome];
  var sh = aba_(planilha_(), nome);
  var cols = ABAS[nome];
  var n = sh.getLastRow() - 1;
  if (n < 1) return (_cache[nome] = []);
  var maxCol = Math.max(sh.getLastColumn(), cols.length);
  var vals = sh.getRange(2, 1, n, maxCol).getValues();
  return (_cache[nome] = vals.filter(function (r) { return r[0] !== ''; }).map(function (r) {
    var o = {};
    cols.forEach(function (c, i) {
      o[c] = typeof r[i] === 'string' ? r[i] : (r[i] === null || r[i] === undefined ? '' : r[i]);
    });
    return o;
  }));
}

function inserir_(nome, obj) { inserirVarios_(nome, [obj]); }

function inserirVarios_(nome, objs) {
  var sh = aba_(planilha_(), nome);
  var cols = ABAS[nome];
  var linhas = objs.map(function (o) { return cols.map(function (c) { return celula_(o[c]); }); });
  sh.getRange(sh.getLastRow() + 1, 1, linhas.length, cols.length).setValues(linhas);
  delete _cache[nome];
}

function atualizar_(nome, id, mudancas) {
  var sh = aba_(planilha_(), nome);
  var cols = ABAS[nome];
  var n = sh.getLastRow() - 1;
  if (n < 1) return false;
  var ids = sh.getRange(2, 1, n, 1).getValues();
  for (var i = 0; i < ids.length; i++) {
    if (String(ids[i][0]) === String(id)) {
      var linhaAtual = sh.getRange(i + 2, 1, 1, cols.length).getValues()[0];
      Object.keys(mudancas).forEach(function (c) {
        var colIdx = cols.indexOf(c);
        if (colIdx >= 0) {
          linhaAtual[colIdx] = celula_(mudancas[c]);
        }
      });
      sh.getRange(i + 2, 1, 1, cols.length).setValues([linhaAtual]);
      delete _cache[nome];
      return true;
    }
  }
  return false;
}

function celula_(v) {
  if (typeof v === 'string' && /^[=+\-@]/.test(v)) return "'" + v;
  return v === undefined || v === null ? '' : v;
}

function comLock_(fn) {
  var lock = LockService.getScriptLock();
  try {
    var obteve = lock.tryLock(25000);
    if (!obteve) {
      throw erro_('O servidor está processando outra solicitação simultânea no momento. Por favor, tente novamente em alguns segundos.');
    }
  } catch (e) {
    if (e && e.usuario) throw e;
    throw erro_('O servidor está temporariamente ocupado. Tente novamente em instantes.');
  }
  try {
    _cache = {};
    return fn();
  } finally {
    try { lock.releaseLock(); } catch (e) { /* ignore */ }
  }
}

// ============================== UTILITÁRIOS ==============================

function erro_(msg) { var e = new Error(msg); e.usuario = true; return e; }

function texto_(v, rotulo, max, obrigatorio) {
  var s = String(v == null ? '' : v).replace(/\s+/g, ' ').trim();
  if (obrigatorio && !s) throw erro_('Preencha o campo "' + rotulo + '".');
  if (s.length > max) throw erro_('O campo "' + rotulo + '" aceita no máximo ' + max + ' caracteres.');
  return s;
}

function inteiro_(s, rotulo) {
  var m = String(s).replace(/\s/g, '').match(/^[+-]?\d+$/);
  if (!m) throw erro_('"' + rotulo + '" deve ser um número inteiro (ex.: 20).');
  return parseInt(m[0], 10);
}

function urlValida_(u) {
  return /^https?:\/\/[^\s/$.?#][^\s]*\.[^\s]{2,}/i.test(u) && u.length <= 500;
}

function normalizar_(s) {
  return String(s || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/\s+/g, ' ').trim().toLowerCase();
}

function mapa_(lista) { var m = {}; lista.forEach(function (x) { m[x.id] = x; }); return m; }
function num_(v) { var n = Number(v); return isNaN(n) ? 0 : n; }
function json_(s) { try { return JSON.parse(s); } catch (e) { return {}; } }

function dataHoraString_(val) {
  if (!val) return '';
  if (typeof val === 'string') {
    if (/^\d{2}\/\d{2}\/\d{4}/.test(val)) return val;
    if (/^\d{10,}$/.test(val)) {
      var d1 = new Date(Number(val));
      if (!isNaN(d1.getTime())) {
        return Utilities.formatDate(d1, "America/Sao_Paulo", "dd/MM/yyyy HH:mm:ss");
      }
    }
    var d2 = new Date(val);
    if (!isNaN(d2.getTime())) {
      return Utilities.formatDate(d2, "America/Sao_Paulo", "dd/MM/yyyy HH:mm:ss");
    }
    return val;
  }
  if (typeof val === 'number') {
    var d3 = new Date(val);
    if (!isNaN(d3.getTime())) {
      return Utilities.formatDate(d3, "America/Sao_Paulo", "dd/MM/yyyy HH:mm:ss");
    }
  }
  if (val instanceof Date) {
    if (!isNaN(val.getTime())) {
      return Utilities.formatDate(val, "America/Sao_Paulo", "dd/MM/yyyy HH:mm:ss");
    }
  }
  return String(val || '');
}

function timestampMs_(val) {
  if (!val) return 0;
  if (typeof val === 'number') return val;
  if (val instanceof Date) return val.getTime();
  if (typeof val === 'string') {
    if (/^\d{10,}$/.test(val)) return Number(val);
    var m = val.match(/^(\d{2})\/(\d{2})\/(\d{4})(?:\s+(\d{2}):(\d{2})(?::(\d{2}))?)?/);
    if (m) {
      var d = new Date(Number(m[3]), Number(m[2]) - 1, Number(m[1]),
                       Number(m[4] || 0), Number(m[5] || 0), Number(m[6] || 0));
      return d.getTime();
    }
    var dIso = new Date(val);
    if (!isNaN(dIso.getTime())) return dIso.getTime();
  }
  return 0;
}

function gerarIdAcao_() {
  var agora = new Date();
  var prefixo = Utilities.formatDate(agora, "America/Sao_Paulo", "yyMMdd");
  var chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
  var sufixo = "";
  for (var i = 0; i < 4; i++) {
    sufixo += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return "#ACT-" + prefixo + "-" + sufixo;
}

function gerarIdLnc_() {
  var agora = new Date();
  var prefixo = Utilities.formatDate(agora, "America/Sao_Paulo", "yyMMdd");
  var chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
  var sufixo = "";
  for (var i = 0; i < 4; i++) {
    sufixo += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return "#LNC-" + prefixo + "-" + sufixo;
}

function limparUrl_(u) {
  if (!u) return '';
  var s = String(u).trim();
  s = s.replace(/[?&](utm_[^&=]+|igsh|fbclid|src|ref|share_id|startTime|mibextid)=[^&#]*/gi, '');
  s = s.replace(/\/+\?/g, '?');
  s = s.replace(/[?&#\/]+$/, '');
  return s;
}

/** Varre todas as abas e higieniza qualquer timestamp numérico legado (ex.: 1790530...) para data formatada dd/MM/yyyy HH:mm:ss. */
function repararDatasLegadas_(me) {
  var ss = planilha_();
  var totalReparadas = 0;
  var colunasData = {
    Iniciativas: ['criadoEm'],
    Entregas: ['criadoEm', 'revisadoEm'],
    Avisos: ['criadoEm', 'expiraEm'],
    AcoesCatalogo: ['criadoEm'],
    Briefings: ['criadoEm'],
    Cronograma: ['criadoEm'],
    MetricasEntregas: ['criadoEm', 'revisadoEm']
  };

  Object.keys(colunasData).forEach(function (nomeAba) {
    var sh = ss.getSheetByName(nomeAba);
    if (!sh) return;
    var n = sh.getLastRow() - 1;
    if (n < 1) return;
    var cols = ABAS[nomeAba];
    var maxCols = Math.max(sh.getLastColumn(), cols.length);
    var vals = sh.getRange(2, 1, n, maxCols).getValues();
    var alterou = false;

    for (var r = 0; r < vals.length; r++) {
      colunasData[nomeAba].forEach(function (campo) {
        var cIdx = cols.indexOf(campo);
        if (cIdx >= 0 && cIdx < maxCols) {
          var val = vals[r][cIdx];
          if (val && (typeof val === 'number' || /^\d{10,}$/.test(String(val).trim()))) {
            var dataFormatada = dataHoraString_(val);
            if (dataFormatada && dataFormatada !== String(val)) {
              vals[r][cIdx] = dataFormatada;
              totalReparadas++;
              alterou = true;
            }
          }
        }
      });
    }

    if (alterou) {
      sh.getRange(2, 1, n, maxCols).setValues(vals);
    }
  });

  _cache = {};
  return {
    reparadas: totalReparadas,
    mensagem: totalReparadas > 0
      ? (totalReparadas + ' data(s) antiga(s) foram higienizadas e formatadas com sucesso na planilha!')
      : 'Todas as datas da planilha já estão perfeitamente formatadas!'
  };
}


// ============================== GESTÃO DE MÉTRICAS PÓS-PUBLICAÇÃO ==============================

function registrarMetricaEntrega_(me, d) {
  if (ehAdmin_(me)) throw erro_('Administrador não registra métricas de iniciativa.');
  var eid = String(d.entregaId || '').trim();
  var periodo = String(d.periodo || '').trim().toLowerCase();
  var alcance = Math.max(0, parseInt(d.alcance, 10) || 0);
  var engajamento = Math.max(0, parseInt(d.engajamento, 10) || 0);
  var comprovanteUrl = String(d.comprovanteUrl || '').trim();
  if (!/^https?:\/\//i.test(comprovanteUrl)) throw erro_('Informe um link válido para o comprovante/print dos insights.');
  var obs = texto_(d.observacoes, 'Observações', 350, false);

  var entregas = lerTudo_('Entregas');
  var entrega = entregas.filter(function (e) { return String(e.id) === eid; })[0];
  if (!entrega || entrega.iniciativaId !== me.id) throw erro_('Entrega não encontrada ou não pertence à sua iniciativa.');

  var isStory = (entrega.tarefaId || '').toLowerCase().indexOf('story') >= 0;
  var periodoRotulo = '';
  var pontosMetrica = 0;
  if (isStory) {
    if (periodo !== '24h') throw erro_("Para stories, o período de insights deve ser de 24 horas ('24h').");
    periodoRotulo = '24 Horas Stories';
    pontosMetrica = 5;
  } else {
    if (['sem1', 'sem2', 'sem3'].indexOf(periodo) < 0) throw erro_("Para posts/reels/carrossel, o período deve ser 'sem1', 'sem2' ou 'sem3'.");
    var mapRotulo = { sem1: '1ª Semana', sem2: '2ª Semana', sem3: '3ª Semana' };
    periodoRotulo = mapRotulo[periodo];
    pontosMetrica = 10;
  }

  var metricas = lerTudo_('MetricasEntregas');
  var existente = metricas.filter(function (m) { return String(m.entregaId) === eid && m.periodo === periodo; })[0];
  var agora = new Date();
  var criadoEmFormatado = Utilities.formatDate(agora, "America/Sao_Paulo", "dd/MM/yyyy HH:mm:ss");

  var metricaId;
  if (existente) {
    if (existente.status === 'validada') throw erro_('A métrica de ' + periodoRotulo + ' desta entrega já foi validada e pontuada.');
    metricaId = existente.id;
    atualizar_('MetricasEntregas', metricaId, {
      alcance: alcance,
      engajamento: engajamento,
      comprovanteUrl: comprovanteUrl,
      observacoes: obs,
      status: 'pendente',
      motivoRecusa: '',
      criadoEm: criadoEmFormatado
    });
  } else {
    metricaId = gerarId_('MTR');
    inserir_('MetricasEntregas', {
      id: metricaId,
      entregaId: eid,
      iniciativaId: me.id,
      iniciativaNome: me.nome,
      tarefaId: entrega.tarefaId,
      tarefaNome: entrega.tarefaNome,
      tipoMidia: isStory ? 'story' : 'post',
      periodo: periodo,
      periodoRotulo: periodoRotulo,
      pontos: pontosMetrica,
      alcance: alcance,
      engajamento: engajamento,
      comprovanteUrl: comprovanteUrl,
      observacoes: obs,
      status: 'pendente',
      motivoRecusa: '',
      criadoEm: criadoEmFormatado,
      revisadoEm: ''
    });
  }

  var p = painel_(me);
  p.metricaEnviada = {
    id: metricaId,
    entregaId: eid,
    periodo: periodoRotulo,
    pontos: pontosMetrica,
    alcance: alcance,
    engajamento: engajamento
  };
  return p;
}

function validarMetricaEntrega_(me, d) {
  var status = String(d.status || '');
  if (['pendente', 'validada', 'recusada'].indexOf(status) < 0) throw erro_('Status de validação inválido.');
  var motivo = texto_(d.motivoRecusa, 'Motivo da recusa', 250, false);
  var mid = String(d.id || d.metricaId || '');
  var agora = new Date();
  var revisadoEmFormatado = status === 'pendente' ? '' : Utilities.formatDate(agora, "America/Sao_Paulo", "dd/MM/yyyy HH:mm:ss");

  var ok = atualizar_('MetricasEntregas', mid, {
    status: status,
    motivoRecusa: status === 'recusada' ? motivo : '',
    revisadoEm: revisadoEmFormatado
  });
  if (!ok) throw erro_('Métrica não encontrada no banco de dados.');
  return adminDados_(me);
}

function validarMetricasLote_(me, d) {
  var ids = Array.isArray(d.ids) ? d.ids : [];
  var status = String(d.status || 'validada');
  if (['validada', 'recusada'].indexOf(status) < 0) throw erro_('Status inválido para validação de métricas em lote.');
  var agora = new Date();
  var revisadoEmFormatado = Utilities.formatDate(agora, "America/Sao_Paulo", "dd/MM/yyyy HH:mm:ss");

  ids.forEach(function (id) {
    atualizar_('MetricasEntregas', id, {
      status: status,
      motivoRecusa: '',
      revisadoEm: revisadoEmFormatado
    });
  });
  return adminDados_(me);
}
