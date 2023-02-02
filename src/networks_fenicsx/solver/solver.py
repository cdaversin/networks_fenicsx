from petsc4py import PETSc

from networks_fenicsx.mesh import mesh
from networks_fenicsx.solver import assembly
from networks_fenicsx.utils.timers import timeit
from networks_fenicsx import config


class Solver():

    def __init__(self, config: config.Config, graph: mesh.NetworkGraph, assembler: assembly.Assembler):
        self.G = graph
        self.assembler = assembler
        self.cfg = config

        if self.assembler is not None:
            self.A = assembler.assembled_matrix()
            self.b = assembler.assembled_rhs()

    @timeit
    def solve(self):

        # Configure solver
        ksp = PETSc.KSP().create(self.G.msh.comm)
        ksp.setOperators(self.A)

        ksp.setType("preonly")
        ksp.getPC().setType("lu")
        # ksp.getPC().setFactorSolverType("superlu_dist") # Not giving correct solution
        ksp.getPC().setFactorSolverType("umfpack")

        # Solve
        x = self.A.createVecLeft()
        ksp.solve(self.b, x)

        return x
