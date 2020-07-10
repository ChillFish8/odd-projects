import importlib
from typing import Tuple, Union, Any, Callable
import time

try:
    from colorama import Fore

    format_colour = True
except ImportError:
    format_colour = False


class Repl:
    def __init__(self):
        self.mod = importlib.import_module('main')
        with open('main.py', 'r') as file:
            self.copy = file.read()

    @staticmethod
    def compile(code: str, globals_) -> str:
        var_blocks = list(map(lambda x: "{} = {}".format(x[0], repr(x[1]))
            if not isinstance(x[1], Callable) else "", globals_.items()))
        block = "\n".join(var_blocks)
        code = block + "\n" + code
        code_lines = list(map(lambda line: (" " * 4 + line), code.splitlines()))
        code = "\n".join(code_lines)
        return code

    def replace_content(self, script) -> Tuple[Union[Exception, Any], Union[list, Any]]:
        with open('main.py', 'w') as new_file:
            new_file.write(script)
        try:
            importlib.reload(self.mod)
            inst = self.mod.MyExecutor()
            result_vars = inst.run()
            result = inst.output
        except Exception as e:
            result = e
            result_vars = ""

        with open('main.py', 'w') as file:
            file.write(self.copy)

        return result, result_vars

    def exec(self, code: str, set_vars: dict) -> Tuple[Union[Exception, Any], Union[list, Any]]:
        compiled = self.compile(code, set_vars)
        script = self.copy.replace("# ---REPLACE-ME--- #", compiled)
        return self.replace_content(script)


def main():
    repl = Repl()
    set_vars = {}
    code = ""
    debug = False
    while code != "exit()":
        if format_colour:
            code = input(Fore.RED + ">>> " + Fore.WHITE)
        else:
            code = input(">>> ")
        if code.endswith(":"):
            code += "\n"
            end = 0
            while end <= 1:
                block = input("... ")
                if not block:
                    end += 1
                code += block + "\n"

        if code == "enable_console_debug()":
            debug = True
        elif code == "disable_console_debug()":
            debug = False
        elif code != "exit()":
            start = time.perf_counter()
            results, variables = repl.exec(code, set_vars)
            stop = time.perf_counter() - start
            if isinstance(results, Exception):
                if format_colour:
                    print(Fore.MAGENTA + "Exception Raised on code:\n", Fore.CYAN + code + Fore.WHITE)
                else:
                    print("Exception Raised on code:\n", code)
            else:
                set_vars = {**set_vars, **dict(variables)}

                results = list(map(str, results))
                output = "".join(results)
                code = ""
                if format_colour:
                    result_vars = list(
                        map(lambda x: (
                                " {}" + Fore.WHITE + ":" + Fore.CYAN + " {}" + Fore.WHITE
                        ).format(x[0], repr(x[1])) if x[0] != "self" else "", variables.items()))
                    print(output)
                    if debug:
                        print(
                            Fore.MAGENTA + "# ===== Execution Stats ==== #" + Fore.CYAN)
                        print(
                            Fore.RED +
                            "  Execution took: "
                            + Fore.WHITE +
                            "{}ms\n".format(round(stop * 1000, 4))
                        )
                        print(
                            Fore.MAGENTA +
                            "# ===== Result Variables ==== #\n"
                            + Fore.CYAN,
                            result_vars[0] + "\n",
                            "\n".join(result_vars[1:])
                            + Fore.WHITE
                        )
                else:
                    result_vars = list(
                        map(lambda x: " {}: {}".format(
                            x[0], repr(x[1])) if x[0] != "self" else "", variables.items()))
                    print(output)

                    if debug:
                        print("# ===== Execution Stats ==== #")
                        print(
                            "  Execution took: "
                            "{}ms\n".format(round(stop * 1000, 4))
                        )
                        print(
                            "# ===== Result Variables ==== #\n",
                            result_vars[0] + "\n",
                            "\n".join(result_vars[1:])
                        )


if __name__ == "__main__":
    main()
