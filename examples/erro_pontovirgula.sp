{ Programa com erros sintáticos - FALTA DE PONTO E VÍRGULA }

program erro_pontovirgula;

var
    x, y : integer  { ERRO: falta ; }
    z : real;

begin
    x := 10;
    y := 20  { ERRO: falta ; }
    z := 3.14
end
