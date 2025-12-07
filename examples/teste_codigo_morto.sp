program teste_codigo_morto;
var
    x, y, z : integer;
    resultado : integer;
begin
    x := 10;
    y := 20;
    z := 30;  { z não é usado depois }
    
    resultado := x + y;
    
    { Variável temporária nunca usada }
    x := 15;
    
    { Outra operação cujo resultado não é usado }
    y := 25 * 2;
    
    write(resultado)
end
