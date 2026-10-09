local envs = {keyresult=true, example=true, further=true, aside=true, reading=true, problem=true}
function Div(el)
  local c = el.classes[1]
  if c and envs[c] and FORMAT:match("latex") then
    table.insert(el.content, 1, pandoc.RawBlock("latex", "\\begin{" .. c .. "}"))
    table.insert(el.content, pandoc.RawBlock("latex", "\\end{" .. c .. "}"))
    return el.content
  end
end
