{ Programa com erros sintáticos - IF SEM THEN }

program erro_if;

var
    x : integer;

begin
    x := 10;
    
    { ERRO: falta then }
    if x > 5
    begin
        write("Maior que 5")
    end
end
