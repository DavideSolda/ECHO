import clingo

class Context:
    def id(self, x):
        return x
    def seq(self, x, y):
        return [x, y]

def on_model(m):
    print(m)

ctl = clingo.Control()
ctl.load("to_sat.lp")
ctl.ground([("base", [])], context=Context())
ctl.add("check", ["t"], "#external query(t).")


print("solving phase:")

for step in range(0,6):
    print(step)
    ctl.ground([("step", [clingo.Number(step)])])
    ctl.ground([("check", [clingo.Number(step)])])
    ctl.assign_external(clingo.Function("query", [clingo.Number(step)]), True)
    with ctl.solve(yield_=True) as handle:
        for m in handle:
            if len(m.symbols(atoms=True)) == 0:
                print('no module')
            for f in m.symbols(atoms=True):
                if f.name == "holds" or f.name == "goal_to_sat" or f.name == 'occurs' or f.name == 'minimal' or f.name == 'g' or f.name == 'query' or f.name == 'not_sat':
                    print(f)
    ctl.release_external(clingo.Function("query", [clingo.Number(step)]))
