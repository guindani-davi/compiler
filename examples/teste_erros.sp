{ Programa com erros léxicos para testar }

program teste_erros;

var
    x : integer;
    y@ : real;        { @ é um caractere ilegal }
    
begin
    x := 10;
    y := 3.14.15;     { número com dois pontos }
    
    if x =@ 10        { =@ é um token inválido }
    then
    begin
        write("Erro!");
    end
end
