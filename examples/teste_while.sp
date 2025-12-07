{ Exemplo com while e expressões }
program teste_while;
var
    a, b : integer;
begin
    a := 10;
    b := 5;
    while a > b
    begin
        write(a);
        a := a - 1
    end;
    write("Fim")
end
