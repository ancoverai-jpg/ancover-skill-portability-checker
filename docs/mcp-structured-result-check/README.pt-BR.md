# Ancover — Conferência de respostas estruturadas MCP
Skill experimental para comparar offline o objeto structuredContent capturado com o outputSchema da ferramenta selecionada. O perfil é restrito ao MCP2025-06-18 e JSON Schema2020-12; não certifica compatibilidade com versões modernas do protocolo.

Use Python3.12+ em ambiente virtual isolado e de caminho curto. Instale requirements.txt com pip --require-hashes --only-binary=:all: e execute scripts/check.py com um JSON privado. Caminhos e comandos completos estão na [Skill](../../skills/mcp-structured-result-check/SKILL.md); no Windows use Scripts/python.exe. O [exemplo sintético](../../examples/mcp-structured-result.json) retorna MATCH. Trocar count por texto retorna MISMATCH.

O arquivo contém profile, tool e callResult. Selecione a declaração e o resultado correspondentes; retire o envelope JSON-RPC. A ferramenta não prova a origem, a associação nem a atualidade da captura. Nunca substitui structuredContent por JSON em content.text. isError:true é falha da ferramenta, mesmo com dados compatíveis.

Saídas: MATCH/0, MISMATCH ou TOOL_ERROR/1, INDETERMINATE ou NOT_APPLICABLE/2. Ausência de schema não vira sucesso. Referências externas, vocabulário personalizado, outro dialeto, dependências ausentes e falhas do worker ficam indeterminados. Sem validação de format, coerção ou valores padrão. Limites:1MiB,12000 nós, profundidade48, prazo5s; não é isolamento de memória do sistema operacional.

Não realiza chamadas MCP, buscas de schemas, telemetria nem alterações no arquivo. O relatório omite conteúdo, nomes de campos, caminhos locais e exceções e inclui o SHA256 do arquivo; esse digest ainda pode identificar entradas conhecidas. A instalação explícita baixa seis dependências fixadas por hash. Consulte [perfil e limitações](../../skills/mcp-structured-result-check/references/profile.md), [pesquisa](research.md) e [validação](validation.md).

Execução do helper e instalação isolada no Codex são evidências distintas de conversa real. Gatilhos conversacionais Codex: NOT_TESTED. Claude Code: NOT_TESTED. Não há promessa de correção de negócio, sucesso real de ferramenta ou conformidade MCP completa. Licença do pacote MIT; dependências MIT e PSF-2.0 descritas na [documentação inglesa](README.md).

Para atualizar, revise o diff e os hashes, substitua apenas a instalação selecionada e repita o exemplo no ambiente isolado. Para remover, retire somente essa instalação e seu ambiente virtual dedicado; preserve configurações pessoais e ambientes compartilhados. Reinstalação manual foi exercitada; atualização automática do host: NOT_TESTED. Números não finitos no parser ficam indeterminados.
