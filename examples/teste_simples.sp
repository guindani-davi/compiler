{ Programa simples de teste }

program teste_simples;

var
    a, b, c : integer;
    resultado : real;

begin
    a := 10;
    b := 20;
    c := a + b;
    
    if c > 25
    then
    begin
        write("C e maior que 25");
    end
    
    resultado := 3.14 * 2.0;
    write(resultado);
end
