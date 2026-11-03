-- wide-tables.lua — sólo para el EPUB.
-- Una tabla ancha no cabe en una pantalla e-ink estrecha. Las tablas con al menos
-- MIN_COLUMNS columnas cuya fila más larga supera MIN_ROW_CHARS caracteres de texto
-- se presentan como fichas verticales: una por fila, con la primera celda como título
-- y cada otra celda bajo el encabezado de su columna. Mismo contenido, mismos rótulos,
-- mismo orden. Las demás tablas se dejan como tablas (las adapta kindle.css).
-- El Markdown fuente no cambia. Determinista: depende sólo de la tabla.

local MIN_COLUMNS = 4
local MIN_ROW_CHARS = 80

local stringify = pandoc.utils.stringify
local to_inlines = pandoc.utils.blocks_to_inlines

local function text_len(s)
  return utf8.len(s) or #s
end

local function row_chars(row)
  local n = 0
  for _, cell in ipairs(row.cells) do
    n = n + text_len(stringify(cell.contents))
  end
  return n
end

local function simple(row)
  for _, cell in ipairs(row.cells) do
    if cell.col_span ~= 1 or cell.row_span ~= 1 then
      return false
    end
  end
  return true
end

local function card(labels, row)
  local cells = row.cells
  local title = pandoc.Inlines {}
  if #labels[1] > 0 then
    title:extend(labels[1])
    title:extend { pandoc.Str(":"), pandoc.Space() }
  end
  title:insert(pandoc.Strong(to_inlines(cells[1].contents)))
  local items = {}
  for i = 2, #cells do
    local content = cells[i].contents
    if #content == 0 then
      content = pandoc.Blocks { pandoc.Plain { pandoc.Str("—") } }
    end
    local term = #labels[i] > 0 and labels[i] or pandoc.Inlines { pandoc.Str("—") }
    table.insert(items, { term, { content } })
  end
  return pandoc.Div({ pandoc.Para(title), pandoc.DefinitionList(items) }, { class = "table-card" })
end

function Table(tbl)
  local ncols = #tbl.colspecs
  if ncols < MIN_COLUMNS or #tbl.head.rows ~= 1 or not simple(tbl.head.rows[1]) then
    return nil
  end
  local rows = {}
  for _, body in ipairs(tbl.bodies) do
    if #body.head > 0 then
      return nil
    end
    for _, row in ipairs(body.body) do
      if #row.cells ~= ncols or not simple(row) then
        return nil
      end
      table.insert(rows, row)
    end
  end
  local widest = 0
  for _, row in ipairs(rows) do
    widest = math.max(widest, row_chars(row))
  end
  if widest <= MIN_ROW_CHARS then
    return nil
  end

  local labels = {}
  for i, cell in ipairs(tbl.head.rows[1].cells) do
    labels[i] = to_inlines(cell.contents)
  end
  local blocks = {}
  local caption = to_inlines(tbl.caption.long)
  if #caption > 0 then
    table.insert(blocks, pandoc.Div({ pandoc.Para(caption) }, { class = "table-cards-caption" }))
  end
  for _, row in ipairs(rows) do
    table.insert(blocks, card(labels, row))
  end
  return pandoc.Div(blocks, { class = "table-cards" })
end
