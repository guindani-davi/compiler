{ Programa com erros sintáticos - ATRIBUIÇÃO INCOMPLETA }

program erro_atribuicao;

var
    x, y : integer;

begin
    x :=;     { ERRO: falta valor após := }
    y = 20;   { ERRO: deveria ser := }
    z := 30   { ERRO: variável z não declarada - erro semântico, não sintático }
end
