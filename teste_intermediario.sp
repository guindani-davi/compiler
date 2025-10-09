program exemplo;

const
    TAM := 10;
    PI := 3.14159;
    MENSAGEM := "Programa de exemplo";

type
    vetor := array[10] of integer;
    aluno := record
        nome: integer;
        nota: real
    end;

var
    x, y, z: integer;
    media: real;
    notas: vetor

function soma(a, b: integer): integer
var
    resultado: integer
begin
    resultado := a + b;
    soma := resultado
end

begin
    x := 5;
    y := 10;
    z := soma(x, y)
end
