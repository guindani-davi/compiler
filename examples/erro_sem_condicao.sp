program erro_condicao_tipo;
var
    x : integer;
begin
    x := 10;
    if x then begin  { Erro: condição deve ser booleana, mas x é inteiro }
        write("x eh verdadeiro")
    end
end
