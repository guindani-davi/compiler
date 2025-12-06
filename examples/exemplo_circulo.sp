{ Programa de exemplo em Pascal Simplificado }
{ Calcula a área de um círculo }

program exemplo_circulo;

const
    pi := 3.1415927;
    mensagem := "Calculo de area do circulo";

type
    vetor := array[10] of integer;
    ponto := record
        x : real;
        y : real;
    end;

var
    raio : real;
    area : real;
    contador : integer;
    valores : vetor;

function quadrado(n : real) : real
var
    resultado : real;
begin
    resultado := n * n;
end

begin
    write("Digite o raio: ");
    read(raio);
    
    { Calcula a área usando a função }
    area := pi * quadrado(raio);
    
    write("Area do circulo: ");
    write(area);
    
    { Exemplo de laço while }
    contador := 0;
    while contador < 10
    begin
        valores[contador] := contador * 2;
        contador := contador + 1;
    end
    
    { Exemplo de condicional }
    if area > 100
    then
    begin
        write("Circulo grande");
    end
    else
    begin
        write("Circulo pequeno");
    end
end
