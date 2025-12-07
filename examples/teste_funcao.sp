{ Exemplo com função }
program teste_funcao;

var
    x, y : integer;

function dobro(n : integer) : integer
var
    resultado : integer;
begin
    resultado := n * 2;
end

begin
    x := 5;
    y := dobro(x);
    write(y)
end
