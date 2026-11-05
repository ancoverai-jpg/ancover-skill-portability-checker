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

Consulte [pesquisa e ranking](docs/research.md), [três especificações](docs/specifications.md), [matriz de qualidade](docs/quality-matrix.md) e [diagnóstico](docs/environment.md). A meta solicitada é de três projetos ou Skills novos publicados por dia, com três janelas diárias de trabalho:12h,18h e21h. Os critérios de qualidade continuam obrigatórios; a contagem considera somente publicações efetivas no GitHub. A recorrência depende do agendador Codex e de suas condições de execução, documentadas no guia.

Limites: não detecta todos os segredos embutidos, prompt injection ou comportamento malicioso; não valida todos os schemas de cada host. Não use o hash como assinatura. Licença MIT; veja [contribuição](CONTRIBUTING.md), [segurança](SECURITY.md) e [roadmap](ROADMAP.md).

## Evidência de CI — experimental

A nova [Skill ci-check-evidence](skills/ci-check-evidence/SKILL.md) compara uma política explícita de checks esperados com um snapshot fornecido de uma revisão. Mantém ausências, skips não autorizados, ambiguidades e divergências de revisão visíveis. Não executa testes nem autoriza merge. Veja [documentação e cobertura](docs/ci-check-evidence/README.pt-BR.md).

## Source Archive Review — experimental

A [Skill Source Archive Review](skills/source-archive-review/SKILL.md) compara um ZIP selecionado com arquivos e prefixos esperados, sinalizando ponteiros LFS canônicos sem extrair o conteúdo. Requer Python3.10+; não usa pacotes pip. Veja a [documentação em português](docs/source-archive-review/README.pt-BR.md). O resultado não comprova compilação, integridade de todos os arquivos ou proveniência.

Teste Python: python -B -m unittest discover -s tests -p "*_test.py". Os testes Node continuam sendo executados separadamente pelo comando habitual.

## Conferência de respostas estruturadas MCP — experimental

A [Skill mcp-structured-result-check](skills/mcp-structured-result-check/SKILL.md) compara offline structuredContent com outputSchema de uma captura selecionada do MCP2025-06-18. Diferencia incompatibilidade, falha declarada e resultado indeterminado. Requer Python3.12+ e seis dependências fixadas em ambiente isolado. [Uso e limites em português](docs/mcp-structured-result-check/README.pt-BR.md). Não comprova execução real nem conformidade completa do protocolo.

Política vigente em04/11/2026: três novas unidades por dia, somente nas janelas12h,18h e21h de São Paulo. Horários iniciam trabalho, sem promessa de publicação imediata. Após três, somente manutenção/preparação. O checker Node usa YAML; o helper MCP requer as dependênciasPython próprias.
