# Ruah Desk 360 — página do produto

Página pública do Ruah Desk 360 em **ruahdesk360.com.br**.

- Identidade: **design system do próprio produto** (`plus jakarta sans` servida por nós, verde `#2fcf6f`/`#157a3d`, painéis flutuantes, controles em pílula, raios 8/12/18/24).
- Zero CDN: fonte e telas saem deste repositório.
- Telas: **dados fictícios**, rotuladas como demonstração na própria página.
- Medição: GA4 `G-BBEW5PD7XH` + Ads `AW-18485463418`, **bloqueadas até o aceite** no aviso de cookies (a escolha fica em `localStorage`).
- Sem preço na página (decisão do dono).

## Estrutura
```
index.html          página (tudo em um arquivo, CSS e JS embutidos)
assets/fontes/      Plus Jakarta Sans (woff2 variável)
assets/telas/       telas reais do produto (webp)
sketches/           o estudo que originou a página
404.html CNAME robots.txt sitemap.xml favicon.svg
```
Publicação: o GitHub Pages serve do branch **`gh-pages`** (foi o push nesse branch que ligou o Pages, sem precisar da permissão `pages: write`).
O branch `main` guarda o mesmo conteudo para historico — **ao publicar, envie para os dois**:

```
git push origin main && git push origin main:gh-pages
```
