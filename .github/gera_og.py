#!/usr/bin/env python3
"""Gera og.png (1200x630) da LP do Ruah Desk 360 a partir das TELAS REAIS do produto.

Identidade: tokens do design system do produto (tokens.json) — fundo escuro #0b0f14,
surface #141a21, verde de acento #2fcf6f, tinta #e9eef3, muted #9ba7b4, fonte Plus Jakarta Sans.

Uso (na VPS):  uv run --with pillow --with fonttools --with brotli python3 .github/gera_og.py
(O woff2 do produto é convertido para ttf em memória porque o Pillow não lê woff2.)
"""
import io
import os

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TELA = os.path.join(RAIZ, "assets/telas/dashboard-escuro.webp")
FONTE_WOFF2 = os.path.join(RAIZ, "assets/fontes/pjs-var.woff2")
SAIDA = os.path.join(RAIZ, "og.png")

L, A = 1200, 630
BG = (11, 15, 20)          # --bg escuro do DS
SURFACE = (20, 26, 33)     # --surface-1 escuro
BORDA = (35, 43, 53)       # --border escuro
INK = (233, 238, 243)      # --ink escuro
MUTED = (155, 167, 180)    # --ink-muted escuro
VERDE = (47, 207, 111)     # --accent escuro
OURO = (224, 173, 76)      # --dourado escuro


def fonte(peso: int, tamanho: int) -> ImageFont.FreeTypeFont:
    """Plus Jakarta Sans (variável) — instancia o peso pedido."""
    ttf = TTFont(FONTE_WOFF2)
    ttf.flavor = None
    buf = io.BytesIO()
    ttf.save(buf)
    buf.seek(0)
    f = ImageFont.truetype(buf, tamanho)
    try:
        f.set_variation_by_axes([peso])
    except Exception:
        pass
    return f


im = Image.new("RGB", (L, A), BG)
d = ImageDraw.Draw(im)

# fio de acento (o verde do produto marcando a peça)
d.rectangle([64, 78, 64 + 64, 78 + 6], fill=VERDE)

# marca + título
d.text((64, 108), "Ruah Desk 360", font=fonte(800, 62), fill=INK)

COL_DIR = 520  # a coluna de texto não invade o cartão da tela (ele começa em x=616)


def quebra(txt, f, largura_max):
    """Quebra o texto na largura da coluna — nada de texto vazando por baixo do cartão."""
    palavras, linhas, atual = txt.split(), [], ""
    for p in palavras:
        teste = (atual + " " + p).strip()
        if d.textlength(teste, font=f) <= largura_max or not atual:
            atual = teste
        else:
            linhas.append(atual)
            atual = p
    if atual:
        linhas.append(atual)
    return linhas


f_sub = fonte(500, 26)
y_sub = 190
for ln in quebra("Atendimento comercial por WhatsApp com IA", f_sub, COL_DIR):
    d.text((66, y_sub), ln, font=f_sub, fill=MUTED)
    y_sub += 34


# as três frases do produto (as mesmas da LP, sem promessa nova)
linhas = [
    ("1", "A IA atende e qualifica"),
    ("2", "A fila distribui por assunto"),
    ("3", "Cada negociação fica registrada"),
]
y = max(262, y_sub + 16)
for num, txt in linhas:
    d.ellipse([66, y + 6, 66 + 26, y + 32], fill=(20, 26, 33), outline=VERDE, width=2)
    d.text((72, y + 9), num, font=fonte(700, 15), fill=VERDE)
    d.text((106, y + 4), txt, font=fonte(600, 24), fill=INK)
    y += 50

# rodapé da peça
d.text((64, A - 62), "ruahdesk360.com.br", font=fonte(600, 22), fill=VERDE)
d.text((300, A - 60), "· demonstração com dados fictícios de uma operação em uso",
       font=fonte(400, 19), fill=(110, 120, 132))
d.rectangle([64, A - 22, L - 64, A - 20], fill=(35, 43, 53))

# a tela REAL do produto, em cartão flutuante (princípio do DS: flutuar, não encaixotar)
tela = Image.open(TELA).convert("RGB")
tw = 520
th = round(tela.height * tw / tela.width)
tela = tela.resize((tw, th), Image.LANCZOS)
x0, y0 = L - 64 - tw, 84
# sombra
sombra = Image.new("RGB", (tw + 40, th + 40), BG)
im.paste(sombra, (x0 - 20, y0 - 12))
d.rectangle([x0 - 1, y0 - 1, x0 + tw, y0 + th], outline=BORDA, width=1)
im.paste(tela, (x0, y0))
# selo do acento sobre o cartão
d.rectangle([x0 - 1, y0 - 1, x0 + 3, y0 + th], fill=VERDE)

im.save(SAIDA, "PNG", optimize=True)
print(f"ok: {SAIDA} {im.size} {os.path.getsize(SAIDA)} bytes")
