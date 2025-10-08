program teste_erros;

// Teste de erros léxicos

var
    x: integer;
    y@: real;  // @ é um caractere ilegal
    z#: integer;  // # é um caractere ilegal

begin
    x := 10;
    y := 3.14$;  // $ é um caractere ilegal
    z := x & y;  // & é um caractere ilegal
    write("Teste com erro%")  // % é um caractere ilegal
end
