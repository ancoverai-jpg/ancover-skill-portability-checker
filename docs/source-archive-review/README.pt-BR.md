# Revisão de arquivo ZIP de código-fonte
Skill experimental para conferir o ZIP que será distribuído, comparando arquivos e prefixos esperados e sinalizando ponteiros LFS canônicos. Não extrai o ZIP nem executa código.
Requer Python3.10+, sem pacotes pip:
```sh
python -B examples/source-archive-review/make_demo.py archive-demo
python -B skills/source-archive-review/scripts/check.py archive-demo/expectations.json archive-demo/source.zip
```
O gerador cria uma pasta nova; o exemplo retorna1 porque faltam fontes. O helper aceita ZIP até16MiB, armazenado/deflate. Ele analisa metadados e entradas pequenas; não verifica todos os CRCs, compilação, assinatura, proveniência ou segredos.
As expectativas e a revisão são declarações do operador. Um prefixo não vazio não prova que o submódulo está completo. A saída0 significa somente que essa política explícita foi satisfeita.
Instalação: copie skills/source-archive-review para .agents/skills no Codex ou .claude/skills no Claude Code; também pode usar o plugin existente. Atualize após revisar diferenças e remova somente essa pasta para desinstalar. Licença MIT.
Veja [documentação](README.md), [perfil](../../skills/source-archive-review/references/profile.md) e [validação](validation.md). Ativação conversacional e execução no Claude Code: NOT_TESTED. Não faça downloads LFS nem altere configurações de distribuição automaticamente.
