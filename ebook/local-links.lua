-- local-links.lua — sólo para el EPUB.
-- Un enlace relativo a otro archivo del repositorio (README.md, COOKBOOK.md,
-- ../docs/...) no existe dentro del ebook y quedaría roto. Se conserva su texto
-- como referencia y se quita el enlace. Los anclajes internos (#…) y los enlaces
-- con esquema (https:, mailto:…) no se tocan.

function Link(el)
  local target = el.target
  if target:match("^#") or target:match("^%a[%w+.-]*:") then
    return nil
  end
  return pandoc.Span(el.content, { class = "local-ref" })
end
