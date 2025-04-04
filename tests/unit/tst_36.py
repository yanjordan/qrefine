from __future__ import division
from __future__ import absolute_import

import os
import time
import iotbx.pdb
import mmtbx.f_model
from scitbx.array_family import flex
from qrefine.tests.unit import run_tests
import mmtbx.model
from libtbx.utils import null_out
from libtbx.test_utils import approx_equal
from libtbx import easy_run

pdb_str_in = """
CRYST1   23.260   22.914   22.580  90.00  90.00  90.00 P 1
ATOM      1  N   ALA A   6      12.490  10.000  11.308  1.00 99.80           N
ATOM      2  CA  ALA A   6      11.516  11.071  11.540  1.00103.38           C
ATOM      3  C   ALA A   6      11.169  11.789  10.247  1.00105.41           C
ATOM      4  O   ALA A   6      10.000  12.117  10.000  1.00 98.78           O
ATOM      5  CB  ALA A   6      12.044  12.068  12.580  1.00114.34           C
ATOM      6  H   ALA A   6      13.260  10.127  11.670  0.00 99.80           H
ATOM      7  HA  ALA A   6      10.706  10.664  11.884  0.00103.38           H
ATOM      8  HB2 ALA A   6      12.985  12.230  12.409  0.00114.34           H
ATOM      9  HB3 ALA A   6      11.584  12.914  12.465  0.00114.34           H
TER
END
"""

pdb_str_out = """
CRYST1   23.260   22.914   22.580  90.00  90.00  90.00 P 1
SCALE1      0.042992  0.000000  0.000000        0.00000
SCALE2      0.000000  0.043641  0.000000        0.00000
SCALE3      0.000000  0.000000  0.044287        0.00000
ATOM      1  N   ALA A   6      12.490  10.000  11.308  1.00 99.80           N
ATOM      2  CA  ALA A   6      11.516  11.071  11.540  1.00103.38           C
ATOM      3  C   ALA A   6      11.169  11.789  10.247  1.00105.41           C
ATOM      4  O   ALA A   6      10.000  12.117  10.000  1.00 98.78           O
ATOM      5  CB  ALA A   6      12.044  12.068  12.580  1.00114.34           C
ATOM      6  OXT ALA A   6      12.053  12.051   9.432  1.00105.41           O
ATOM      7  H   ALA A   6      12.129   9.064  11.493  0.00 99.80           H
ATOM      8  H2  ALA A   6      12.786  10.019  10.353  0.00 99.80           H
ATOM      9  H3  ALA A   6      13.282  10.134  11.904  0.00 99.80           H
ATOM     10  HA  ALA A   6      10.602  10.628  11.934  0.00103.38           H
ATOM     11  HB1 ALA A   6      12.973  12.504  12.214  0.00114.34           H
ATOM     12  HB2 ALA A   6      12.225  11.541  13.517  0.00114.34           H
ATOM     13  HB3 ALA A   6      11.300  12.850  12.731  0.00114.34           H
TER
"""

def run(prefix):
  """
  Exercise "qr.finalise m.pdb" produces expected (and meaningful) output.
  Do not modify this test before checking the result on graphics (eg, PyMol)!
  """
  pdb_in = "%s.pdb"%prefix
  open(pdb_in, "w").write(pdb_str_in)
  cmd = "qr.finalise %s > %s.log"%(pdb_in, prefix)
  assert easy_run.call(cmd)==0
  h_answer = iotbx.pdb.input(
    source_info=None, lines = pdb_str_out).construct_hierarchy()
  h_result = iotbx.pdb.input(
    file_name = "%s_complete.pdb"%prefix).construct_hierarchy()
  open("%s_answer.pdb"%prefix, "w").write(pdb_str_out)
  #
  s1 = h_answer.atoms().extract_xyz()
  s2 = h_result.atoms().extract_xyz()
  print(s1.size(), s2.size())
  r = flex.mean(flex.sqrt((s1 - s2).dot()))
  assert r < 0.016, r
  #
  asc = h_result.atom_selection_cache()
  sel = asc.selection("element H or element D")
  assert sel.count(True) == 7
  occ = h_result.atoms().extract_occ().select(sel)
  assert flex.max(occ)<1.e-6

if(__name__ == "__main__"):
  prefix = os.path.basename(__file__).replace(".py","")
  run_tests.runner(function=run, prefix=prefix, disable=False)
