# Ancover Git Tracked Ignore Review

Skill experimental para conferir quais caminhos do índice do Git correspondem às regras .gitignore do repositório. A revisão ajuda quando um arquivo já indexado continua aparecendo depois da criação da regra.

Use Git confiável no PATH e Python 3.12. Execute a partir do pacote confiável e informe a raiz do checkout.

```sh
python -I -B skills/git-tracked-ignore-review/scripts/check.py RAIZ_DO_REPOSITORIO
```

Para reproduzir, inicialize um repositório descartável, crie sample.log com texto sintético e adicione o arquivo ao índice com git add -- sample.log. Crie .gitignore com uma linha *.log. Rode o helper contra a raiz desse checkout. O resultado esperado é INDEX_MATCHES, contagem 1 e saída 1. Um checkout sem correspondências retorna NO_INDEX_MATCHES e saída 0. Entrada inválida retorna INDETERMINATE e saída 2.

O escopo inclui os arquivos .gitignore disponíveis por diretório e o índice atual. Regras globais e .git/info/exclude pertencem a outro escopo. Alterações nas regras da árvore de trabalho podem aparecer antes de serem adicionadas ao índice. O relatório inclui contagem e SHA256 do conjunto de caminhos, sem imprimir nomes ou conteúdo. Digests podem identificar conjuntos conhecidos. Use o comando Git da Skill para consultar nomes em ambiente privado.

Cada consulta tem prazo de dez segundos e aceita até 1 MiB de saída após a captura. A análise se limita ao índice selecionado. Histórico e outros checkouts exigem verificações próprias. Checkout esparso e instalação avulsa da Skill estão marcados NOT_TESTED.

Instale o pacote completo por marketplace isolado ou execute o helper no checkout confiável. Para atualizar, revise o pacote e repita o exemplo. Remova apenas a instalação selecionada. [Skill](../../skills/git-tracked-ignore-review/SKILL.md) · [Pesquisa](research.md) · [Perfil](specification.md) · [Validação](validation.md). Licença MIT. Git é um requisito de sistema separado.

## Execute os exemplos reproduzíveis

~~~sh
python -I -B -m unittest discover -s tests -p git_tracked_ignore_test.py
~~~
