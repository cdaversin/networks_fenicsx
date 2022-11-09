import os
import numpy as np

from networks_fenicsx.mesh import mesh_generation
from networks_fenicsx.solver import assembly, solver
from networks_fenicsx.config import Config


# Clear fenics cache
print('Clearing cache')
os.system('dijitso clean')

cfg = Config()
cfg.outdir = "demo_tree"
cfg.export = True
cfg.clean = True
# cfg.lcar = 0.5

# Create tree
G = mesh_generation.make_tree(n=4, H=4, W=4, cfg=cfg)


class p_bc_expr:
    def eval(self, x):
        return np.full(x.shape[1], x[0])


assembler = assembly.Assembler(cfg, G)
assembler.compute_forms(p_bc_ex=p_bc_expr())
assembler.assemble()

solver = solver.Solver(cfg, G, assembler)
(fluxes, pressure) = solver.solve()
