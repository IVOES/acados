# -*- coding: future_fstrings -*-
#
# Copyright 2019 Gianluca Frison, Dimitris Kouzoupis, Robin Verschueren,
# Andrea Zanelli, Niels van Duijkeren, Jonathan Frey, Tommaso Sartor,
# Branimir Novoselnik, Rien Quirynen, Rezart Qelibari, Dang Doan,
# Jonas Koenemann, Yutao Chen, Tobias Schöls, Jonas Schlagenhauf, Moritz Diehl
#
# This file is part of acados.
#
# The 2-Clause BSD License
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.;
#

import numpy as np
import casadi as ca
import json
import os
import sys
from .casadi_functions import *

ACADOS_PATH=os.getenv("ACADOS_SOURCE_DIR","/usr/lib")

class sim_dims:
    """
    class containing the dimensions of the optimal control problem
    """
    def __init__(self):
        self.__nx      = None
        self.__nu      = None
        self.__nz      = 0
        self.__np      = 0

    @property
    def nx(self):
        """:math:`n_x` - number of states"""
        return self.__nx

    @property
    def nz(self):
        """:math:`n_z` - number of algebraic variables"""
        return self.__nz

    @property
    def nu(self):
        """:math:`n_u` - number of inputs"""
        return self.__nu

    @property
    def np(self):
        """:math:`n_p` - number of parameters"""
        return self.__np

    @nx.setter
    def nx(self, nx):
        if type(nx) == int and nx > 0:
            self.__nx = nx
        else:
            raise Exception('Invalid nx value. Exiting.')

    @nz.setter
    def nz(self, nz):
        if type(nz) == int and nz > -1:
            self.__nz = nz
        else:
            raise Exception('Invalid nz value. Exiting.')

    @nu.setter
    def nu(self, nu):
        if type(nu) == int and nu > 0:
            self.__nu = nu
        else:
            raise Exception('Invalid nu value. Exiting.')

    @np.setter
    def np(self, np):
        if type(np) == int and np > -1:
            self.__np = np
        else:
            raise Exception('Invalid np value. Exiting.')

    def set(self, attr, value):
        setattr(self, attr, value)

    # TODO:
    # @p.setter
    # def p(self, p):
    #     if type(p) == np.ndarray:
    #         self.__p = p
    #     else:
    #         raise Exception('Invalid p value. Exiting.')

    # def set(self, attr, value):
    #     setattr(self, attr, value)


class sim_solver_options:
    """
    class containing the description of the solver options
    """
    def __init__(self):
        self.__integrator_type  = 'ERK'
        self.__tf               = None
        self.__sim_method_num_stages  = 1
        self.__sim_method_num_steps   = 1
        self.__sim_method_newton_iter = 3

    @property
    def integrator_type(self):
        """Integrator type"""
        return self.__integrator_type

    @property
    def num_stages(self):
        """Number of stages in the integrator"""
        return self.__sim_method_num_stages

    @property
    def num_steps(self):
        """Number of steps in the integrator"""
        return self.__sim_method_num_steps

    @property
    def newton_iter(self):
        """Number of Newton iterations in simulation method"""
        return self.__sim_method_newton_iter

    @property
    def T(self):
        """Time horizon"""
        return self.__Tsim

    @integrator_type.setter
    def integrator_type(self, integrator_type):
        integrator_types = ('ERK', 'IRK')

        if type(integrator_type) == str and integrator_type in integrator_types:
            self.__integrator_type = integrator_type
        else:
            raise Exception('Invalid integrator_type value. Possible values are:\n\n' \
                    + ',\n'.join(integrator_types) + '.\n\nYou have: ' + integrator_type + '.\n\nExiting.')

    @T.setter
    def T(self, T):
        self.__Tsim = T

    @num_stages.setter
    def num_stages(self, num_stages):

        if type(num_stages) == int:
            self.__sim_method_num_stages = num_stages
        else:
            raise Exception('Invalid num_stages value. num_stages must be an integer. Exiting.')

    @num_steps.setter
    def num_steps(self, num_steps):

        if type(num_steps) == int:
            self.__sim_method_num_steps = num_steps
        else:
            raise Exception('Invalid num_steps value. num_steps must be an integer. Exiting.')

    @newton_iter.setter
    def newton_iter(self, newton_iter):

        if type(newton_iter) == int:
            self.__sim_method_newton_iter = newton_iter
        else:
            raise Exception('Invalid newton_iter value. newton_iter must be an integer. Exiting.')

class acados_sim:
    """
    class containing the full description of the optimal control problem
    """
    def __init__(self, acados_path=ACADOS_PATH):
        """
        Keyword arguments:
        acados_path -- path of your acados installation
        """
        self.dims = sim_dims()
        self.model = acados_dae()
        self.solver_options = sim_solver_options()

        self.acados_include_path = f'{acados_path}/include'
        self.acados_lib_path = f'{acados_path}/lib'


    def set(self, attr, value):
        # tokenize string
        tokens = attr.split('_', 1)
        if len(tokens) > 1:
            setter_to_call = getattr(getattr(self, tokens[0]), 'set')
        else:
            setter_to_call = getattr(self, 'set')

        setter_to_call(tokens[1], value)

        return

class sim_as_object:
        def __init__(self, d):
            self.__dict__ = d
