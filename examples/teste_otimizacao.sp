program teste_otimizacao;
var
    a, b, c, d, e : integer;
    resultado : integer;
begin
    { Atribuições iniciais }
    a := 10;
    b := 20;
    c := 30;
    
    { Atribuição não usada - código morto }
    d := 40;
    
    { Atribuição não usada - código morto }
    e := 50;
    
    { Cálculo do resultado }
    resultado := a + b;
    
    { Atribuição não usada após uso - código morto }
    a := 100;
    
    { Atribuição não usada após uso - código morto }
    b := 200;
    
    { Atribuição não usada - código morto }
    c := a + b;
    
    { Saída }
    write(resultado)
end
