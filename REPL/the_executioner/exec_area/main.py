
def _run():
# ---REPLACE-ME--- #
    return vars()

class MyExecutor:
    def __init__(self):
        self.output = []

    def print(self, *args, sep=" ", end="\n"):
        values = list(map(str, args))
        out = sep.join(values) + end
        self.output.append(out)

    def run(self):
        global print
        print = self.print
        return _run()



