"""Validación estructural de un EPUB generado por build-ebooks.sh. Sólo stdlib.

Uso: python3 -I validate_epub.py <archivo.epub> <título esperado> <kindle.css>

No sustituye a epubcheck: comprueba lo que el build puede romper — contenedor,
paquete, navegación, hoja de estilos propia, metadatos, XHTML bien formado,
enlaces internos y que el libro siga siendo reflowable.
"""

import posixpath
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from urllib.parse import unquote, urlsplit

NS = {
    "c": "urn:oasis:names:tc:opendocument:xmlns:container",
    "opf": "http://www.idpf.org/2007/opf",
    "dc": "http://purl.org/dc/elements/1.1/",
    "x": "http://www.w3.org/1999/xhtml",
}
FIXED_CSS = re.compile(r"\b\d+(?:\.\d+)?(?:px|pt|cm|mm|in)\b")
FONT_TYPES = ("font/", "application/font", "application/vnd.ms-opentype", "application/x-font")


def validate(path, title, css_path):
    bad, info = [], {}
    try:
        z = zipfile.ZipFile(path)
    except zipfile.BadZipFile as e:
        return [f"no es un ZIP válido: {e}"], info
    if z.testzip() is not None:
        bad.append("ZIP con entradas corruptas")
    names = z.namelist()
    first = z.infolist()[0]
    if first.filename != "mimetype" or first.compress_type != zipfile.ZIP_STORED or z.read("mimetype") != b"application/epub+zip":
        bad.append("mimetype ausente, no es la primera entrada o está comprimido")
    if "META-INF/container.xml" not in names:
        return bad + ["falta META-INF/container.xml"], info

    rootfile = ET.fromstring(z.read("META-INF/container.xml")).find(".//c:rootfile", NS)
    opf_path = rootfile.get("full-path") if rootfile is not None else None
    if not opf_path or opf_path not in names:
        return bad + ["el package document (OPF) no existe"], info
    opf = ET.fromstring(z.read(opf_path))
    base = posixpath.dirname(opf_path)

    meta = opf.find("opf:metadata", NS)
    got = {k: (meta.findtext(f"dc:{k}", default="", namespaces=NS) or "").strip() for k in ("title", "language", "creator", "date")}
    info["metadata"] = got
    if got["title"] != title:
        bad.append(f"título {got['title']!r} ≠ {title!r}")
    if got["language"] != "es-ES":
        bad.append(f"idioma {got['language']!r} ≠ 'es-ES'")
    if got["creator"] != "Apep Core":
        bad.append(f"creator {got['creator']!r} ≠ 'Apep Core'")
    for m in meta.findall("opf:meta", NS):
        if m.get("property") == "rendition:layout" and (m.text or "").strip() == "pre-paginated":
            bad.append("fixed layout (rendition:layout pre-paginated)")

    manifest = {}
    for item in opf.find("opf:manifest", NS):
        href = posixpath.normpath(posixpath.join(base, unquote(item.get("href"))))
        manifest[href] = item
        if href not in names:
            bad.append(f"el manifest declara {href} y no está en el ZIP")
        if item.get("media-type", "").startswith(FONT_TYPES):
            bad.append(f"fuente embebida: {href}")
        if item.get("media-type") == "application/javascript" or "scripted" in (item.get("properties") or ""):
            bad.append(f"JavaScript: {href}")
    nav = [h for h, i in manifest.items() if "nav" in (i.get("properties") or "").split()]
    if not nav:
        bad.append("falta el documento de navegación (nav)")

    own_css = open(css_path, "rb").read()
    css = [h for h, i in manifest.items() if i.get("media-type") == "text/css"]
    if not any(z.read(h) == own_css for h in css):
        bad.append("la hoja de estilos propia no está empaquetada")
    for h in css:
        for n, line in enumerate(z.read(h).decode("utf-8").splitlines(), 1):
            if FIXED_CSS.search(line.split("/*")[0]):
                bad.append(f"{h}:{n} dimensión fija: {line.strip()}")

    xhtml = [h for h, i in manifest.items() if i.get("media-type") == "application/xhtml+xml"]
    ids, docs = {}, {}
    for h in xhtml:
        try:
            docs[h] = ET.fromstring(z.read(h))
        except ET.ParseError as e:
            bad.append(f"{h}: XHTML mal formado ({e})")
            continue
        ids[h] = {el.get("id") for el in docs[h].iter() if el.get("id")}
    links = 0
    for h, root in docs.items():
        styled = any(l.get("rel") == "stylesheet" for l in root.iter(f"{{{NS['x']}}}link"))
        if not styled and h not in nav:
            bad.append(f"{h}: no enlaza la hoja de estilos")
        for el in root.iter():
            style = el.get("style") or ""
            if FIXED_CSS.search(style) or el.get("width") or el.get("height"):
                bad.append(f"{h}: dimensión fija en <{el.tag.split('}')[-1]}>")
                break
        for a in root.iter(f"{{{NS['x']}}}a"):
            href = a.get("href")
            if not href or urlsplit(href).scheme:
                continue
            links += 1
            parts = urlsplit(href)
            target = posixpath.normpath(posixpath.join(posixpath.dirname(h), unquote(parts.path))) if parts.path else h
            if target not in docs:
                bad.append(f"{h}: enlace roto a {href}")
            elif parts.fragment and parts.fragment not in ids.get(target, set()):
                bad.append(f"{h}: anclaje roto {href}")
    toc = sum(1 for h in nav if h in docs for _ in docs[h].iter(f"{{{NS['x']}}}li"))
    info.update(chapters=len(xhtml), internal_links=links, toc_entries=toc)
    if toc == 0:
        bad.append("la navegación no tiene entradas")
    return bad, info


def main():
    path, title, css = sys.argv[1:4]
    bad, info = validate(path, title, css)
    for b in bad:
        print(f"  FAIL  {b}")
    if info:
        md = info.get("metadata", {})
        print(f"  {'FAIL' if bad else 'PASS'}  {md.get('title', '?')} · {md.get('date', '?')} · "
              f"{info.get('chapters', 0)} XHTML · TOC {info.get('toc_entries', 0)} entradas · "
              f"{info.get('internal_links', 0)} enlaces internos")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
