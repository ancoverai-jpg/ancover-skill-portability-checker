# Ancover — Comparação de catálogos de ferramentas MCP
Skill experimental para comparar offline duas capturas completas de declarações de ferramentas. Detecta inclusão, remoção e mudanças de descrição, schemas, anotações e campos extras, inclusive mantendo o mesmo nome.

Requer Python3.12+ e somente biblioteca padrão. Não instala dependências nem conecta servidores. No diretório confiável do pacote:
```sh
python -I -B skills/mcp-tool-catalog-diff/scripts/compare.py examples/catalog-before.json examples/catalog-after.json
```
O exemplo sintético retorna REVIEW_REQUIRED/1: uma ferramenta passa a exigir revision. Comparar o primeiro arquivo consigo mesmo retorna UNCHANGED/0. Entrada inválida ou fora do perfil retorna INDETERMINATE/2.

As capturas contêm profile=ancover-mcp-tool-catalog-v1, serverKey idêntico, complete=true e tools. Preserve origem, revisão, horário e protocolo em evidência privada; colete todas as páginas antes de montar o arquivo. nextCursor não é aceito. Falha de descoberta não equivale a lista vazia. Identidade e completude são afirmações do operador, não verificações independentes.

O relatório usa índices de array iniciados em zero e hashes de nomes, sem imprimir nomes, definições, valores ou caminhos. Consulte as declarações alteradas localmente pelos índices. Hashes ainda podem identificar entradas conhecidas; não publique capturas privadas automaticamente. Ordem de chaves e da lista de ferramentas é ignorada. Ordem dos demais arrays, texto exato, ausência/null e grafia numérica permanecem relevantes:1,1.0 e1e0 diferem. Não há promessa de igualdade semântica ou padrão universal de fingerprint.

Limites:1MiB por arquivo regular,256 ferramentas,12000 nós, profundidade48, tokens numéricos de128 caracteres. JSON duplicado, nomes repetidos, entrada parcial ou escopo diferente ficam indeterminados. Não chama ferramentas, segue URLs, altera aprovações ou atualiza baseline. Não prova segurança, compatibilidade, identidade autenticada ou correção de cache/transporte.

Veja [Skill](../../skills/mcp-tool-catalog-diff/SKILL.md), [perfil](../../skills/mcp-tool-catalog-diff/references/profile.md), [pesquisa](research.md) e [validação](validation.md). Gatilhos conversacionais Codex e execução Claude Code: NOT_TESTED quando indisponíveis. Atualize/remova somente a instalação selecionada, preservando configurações pessoais. Licença MIT; nenhuma dependência nova.
