# copyright ############################### #
# This file is part of the Xaux Package.    #
# Copyright (c) CERN, 2025.                 #
# ######################################### #

import json
from pathlib import Path

from .template import JobTemplate


# Job template for Dynamic Aperture analysis
# ==========================================
class DAJob(JobTemplate):
    """Job template for Dynamic Aperture analysis.
    Only difference with the JobTemplate is that the line can have seeds.
    """

    def __init__(self, **kwargs):
        self._seed = kwargs.pop("seed", None)
        super().__init__(**kwargs)

    @property
    def seed(self):
        return self._seed

    @property
    def line(self):
        return JobTemplate.line.fget(self)

    @line.setter
    def line(self, line):
        import xtrack as xt
        if self.seed is not None:
            if isinstance(line, (xt.Line,xt.Multiline,xt.Environment)):
                raise ValueError("Line cannot be set directly if 'seed' is provided!")
            elif isinstance(line, (str, Path)):
                line = Path(line)
                if not line.exists():
                    raise ValueError(f"Line file {line} does not exist!")
                with open(line, 'r') as fid:
                    line = json.load(fid)
                self._line = xt.Line.from_dict(line[self.seed])
            elif isinstance(line, dict):
                if isinstance(line[self.seed], dict):
                    self._line = xt.Line.from_dict(line[self.seed])
                elif isinstance(line[self.seed], (xt.Line, xt.Multiline, xt.Environment)):
                    self._line = line[self.seed]
                else:
                    raise ValueError(f"Invalid seed line type {type(line['seed'])} for seed {self.seed}!")
            elif line is not None:
                raise ValueError(f"Invalid line type {type(line)}")
        else:
            JobTemplate.line.fset(self, line)
