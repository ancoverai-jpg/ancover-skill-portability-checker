# Evidência dos checks de CI
Candidata experimental de Skill para comparar checks esperados com um snapshot explícito de uma revisão. Não executa testes nem autoriza merge.
Requer Node22+. O helper não instala dependências:
```sh
node skills/ci-check-evidence/scripts/check.mjs examples/ci-check-evidence/missing-context.json
```
O exemplo sintético retorna1 porque falta o check integration. Código0 significa somente que a política fornecida foi satisfeita. Skips permitidos continuam separados de sucessos observados.
A lista esperada, a revisão e a completude são declarações do operador. Não há autenticação independente, leitura de proteção de branch, acesso a rede, rerun ou mudança de regras. Nomes aprovados dos checks aparecem no relatório; logs e credenciais não devem entrar no arquivo.
Instalação manual: copie skills/ci-check-evidence para .agents/skills no projeto Codex ou .claude/skills no Claude Code. Para atualizar, revise a diferença, substitua essa pasta e execute o exemplo; para remover, remova somente a pasta instalada. A distribuição pelo plugin existente também pode agrupar esta Skill.
Veja [documentação](README.md), [contrato](../../skills/ci-check-evidence/references/contract.md) e [validação](validation.md). Licença MIT do repositório. Não envie tokens nem logs privados em issues; utilize relatos privados de vulnerabilidade.
Ativação conversacional e execução no Claude Code: NOT_TESTED. A candidata não conta como entrega até publicação e verificação remota.
