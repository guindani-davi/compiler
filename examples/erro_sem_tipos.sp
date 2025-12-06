program erro_tipos_incompativeis;
var
    x : integer;
    y : real;
    s : integer;
begin
    x := 10;
    y := 3.14;
    s := y;  { Erro: não pode atribuir real a integer }
    write(s)
end
