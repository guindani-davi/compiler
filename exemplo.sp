program exemplo;

// Este é um comentário de linha

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
    notas: vetor;

function soma(a, b: integer): integer
var
    resultado: integer;
begin
    resultado := a + b;
    soma := resultado
end

begin
    { Comentário de bloco 
      em múltiplas linhas }
    
    x := 5;
    y := 10;
    z := soma(x, y);
    
    write("Digite um numero: ");
    read(x);
    
    if x > 0 then
        write("Positivo")
    else
        write("Negativo ou zero");
    
    (* Outro tipo de comentário *)
    while x <> 0 begin
        x := x - 1;
        write(x)
    end
    
end
