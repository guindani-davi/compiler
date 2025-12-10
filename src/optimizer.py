from code_generator import Instruction


class Optimizer:
    def __init__(self):
        self.statistics = {
            "original": 0,
            "optimized": 0,
            "removed": 0,
            "percentage": 0.0,
        }

    def otimizar(self, instructions):
        if not instructions:
            return []

        self.statistics["original"] = len(instructions)

        optimized = self.eliminar_codigo_morto(instructions)

        self.statistics["optimized"] = len(optimized)
        self.statistics["removed"] = (
            self.statistics["original"] - self.statistics["optimized"]
        )

        if self.statistics["original"] > 0:
            self.statistics["percentage"] = (
                self.statistics["removed"] / self.statistics["original"]
            ) * 100

        return optimized

    def eliminar_codigo_morto(self, instructions):
        preserve_ops = {
            "WRITE",
            "READ",
            "CALL",
            "RET",
            "JMP",
            "JNZ",
            "LBL",
            "PUSH",
            "POP",
        }

        used_vars = set()

        for instr in instructions:
            op = instr.op

            if op in preserve_ops:
                if op in {"WRITE", "JNZ", "PUSH"}:
                    if instr.addr1 and self.is_variable(instr.addr1):
                        used_vars.add(instr.addr1)

            elif op in {"MOV"}:
                if instr.addr2 and self.is_variable(instr.addr2):
                    used_vars.add(instr.addr2)

            elif op in {"ADD", "SUB", "MUL", "DIV", "GTR", "LES", "EQL", "NEQ"}:
                if instr.addr2 and self.is_variable(instr.addr2):
                    used_vars.add(instr.addr2)
                if instr.addr3 and self.is_variable(instr.addr3):
                    used_vars.add(instr.addr3)

        necessary = [False] * len(instructions)

        for i, instr in enumerate(instructions):
            op = instr.op

            if op in preserve_ops:
                necessary[i] = True

            elif op in {"MOV", "ADD", "SUB", "MUL", "DIV", "GTR", "LES", "EQL", "NEQ"}:
                dest = instr.addr1
                if dest and dest in used_vars:
                    necessary[i] = True

        changed = True
        while changed:
            changed = False
            for i, instr in enumerate(instructions):
                if not necessary[i]:
                    continue

                op = instr.op

                new_used = set()

                if op in {"MOV"}:
                    if instr.addr2 and self.is_variable(instr.addr2):
                        new_used.add(instr.addr2)

                elif op in {"ADD", "SUB", "MUL", "DIV", "GTR", "LES", "EQL", "NEQ"}:
                    if instr.addr2 and self.is_variable(instr.addr2):
                        new_used.add(instr.addr2)
                    if instr.addr3 and self.is_variable(instr.addr3):
                        new_used.add(instr.addr3)

                for var in new_used:
                    if var not in used_vars:
                        used_vars.add(var)
                        changed = True

                        for j, instr2 in enumerate(instructions):
                            if not necessary[j]:
                                if instr2.op in {
                                    "MOV",
                                    "ADD",
                                    "SUB",
                                    "MUL",
                                    "DIV",
                                    "GTR",
                                    "LES",
                                    "EQL",
                                    "NEQ",
                                }:
                                    if instr2.addr1 == var:
                                        necessary[j] = True

        optimized = []
        for i, instr in enumerate(instructions):
            if necessary[i]:
                optimized.append(instr)

        return optimized

    def is_variable(self, addr):
        if addr is None:
            return False

        addr_str = str(addr)

        if addr_str.startswith('"') or addr_str.startswith("'"):
            return False
        try:
            float(addr_str)
            return False
        except ValueError:
            pass

        # É uma variável
        return True

    def imprimir_estatisticas(self):
        print("\n" + "=" * 70)
        print("ESTATÍSTICAS DA OTIMIZAÇÃO")
        print("=" * 70)
        print(f"Instruções originais:     {self.statistics['original']}")
        print(f"Instruções otimizadas:    {self.statistics['optimized']}")
        print(f"Instruções removidas:     {self.statistics['removed']}")
        print(f"Redução:                  {self.statistics['percentage']:.1f}%")
        print("=" * 70)

    def imprimir_codigo_comparativo(self, original, otimizado):
        print("\n" + "=" * 70)
        print("COMPARAÇÃO: CÓDIGO ORIGINAL vs OTIMIZADO")
        print("=" * 70)
        print()

        print(f"{'ORIGINAL':<35} {'OTIMIZADO':<35}")
        print("-" * 70)

        max_len = max(len(original), len(otimizado))

        for i in range(max_len):
            orig = f"{i+1:4}: {original[i]}" if i < len(original) else ""
            opt = f"{i+1:4}: {otimizado[i]}" if i < len(otimizado) else ""

            if i < len(original) and i < len(otimizado):
                print(f"{orig:<35} {opt:<35}")
            elif i < len(original):
                print(f"{orig:<35} {'[REMOVIDO]':<35}")
            else:
                print(f"{'':35} {opt:<35}")

        print()
        print("=" * 70)


def otimizar_codigo(instructions, verbose=True, comparar=False):
    otimizador = Optimizer()
    otimizado = otimizador.otimizar(instructions)

    if verbose:
        otimizador.imprimir_estatisticas()

    if comparar:
        otimizador.imprimir_codigo_comparativo(instructions, otimizado)

    return otimizado, otimizador
