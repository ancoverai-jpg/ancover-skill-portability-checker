# Ancover Skill Portability Checker

Ferramentas experimentais para mantenedores que distribuem Skills em Codex e Claude Code.

O piloto **Skill Preflight** inspeciona um pacote local, identifica problemas delimitados de portabilidade e gera JSON com hash do conteúdo. Ele não executa o pacote nem certifica segurança ou compatibilidade com os agentes.

Requisitos: Node.js 22+ e pnpm 11.25.0. Na raiz deste projeto:

```sh
git clone https://github.com/ancoverai-jpg/ancover-skill-portability-checker.git
cd ancover-skill-portability-checker
pnpm install --frozen-lockfile --ignore-scripts
node --test tests/*.test.mjs
node skills/skill-preflight/scripts/check.mjs .
node scripts/program.mjs cycle
```

Substitua `.` pelo diretório absoluto do pacote. Saídas: 0 para aprovação dessas regras estáticas, 1 para achados e 2 para erro de entrada ou ambiente. Não há telemetria. A instalação baixa dependências; o verificador funciona offline.

O mesmo diretório `skills/` atende aos manifestos portátil, Codex e Claude Code. A Skill `portfolio-research` orienta pesquisa e manutenção. As instruções de instalação e a cobertura real de cada ambiente estão no [guia de operação](docs/operations.md) e no [relatório de validação](docs/validation.md).

Consulte [pesquisa e ranking](docs/research.md), [três especificações](docs/specifications.md), [matriz de qualidade](docs/quality-matrix.md) e [diagnóstico](docs/environment.md). A meta solicitada é de pelo menos cinco projetos ou Skills novos publicados por dia, com cinco janelas diárias de trabalho. Os critérios de qualidade continuam obrigatórios; a contagem considera somente publicações efetivas no GitHub. A recorrência depende do agendador Codex e de suas condições de execução, documentadas no guia.

Limites: não detecta todos os segredos embutidos, prompt injection ou comportamento malicioso; não valida todos os schemas de cada host. Não use o hash como assinatura. Licença MIT; veja [contribuição](CONTRIBUTING.md), [segurança](SECURITY.md) e [roadmap](ROADMAP.md).
