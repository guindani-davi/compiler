program erro_funcao_parametros;

function soma(a: integer; b: integer): integer
var
    resultado : integer;
begin
    resultado := a + b
end

begin
    write(soma(10, 20, 30))  { Erro: função espera 2 argumentos, mas recebeu 3 }
end
