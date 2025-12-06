program erro_variavel_nao_declarada;
var
    x : integer;
begin
    x := 10;
    y := 20;  { Erro: y não foi declarada }
    write(y)
end
