help([[
For detailed instructions, go to:
    https://maxquant.net

This module sets the following environment variables:
    MAXQUANT_BASE: directory containing MaxQuant programs and bash scripts

This module loads the following modules and their requirements:
    - gcc/7.3.0
    - mono/5.16.0.179
    - python/3.7.4
]])

whatis("Version: 1.0.0")
whatis("Keywords: MaxQuant, Utility")
whatis("URL: https://maxquant.net")
whatis("Description: MaxQuant is a quantitative proteomics software package designed for analyzing large mass-spectrometric data sets.")

always_load("gcc/7.3.0")
always_load("mono/5.16.0.179")
always_load("python/3.7.4")

local home = os.getenv("HOME") or ""
local venv = pathJoin(home, "maxquant-venv")
local maxquant = pathJoin(home, "projects/def-coulomb/maxquant")
local maxquant_parameters = pathJoin(home, "projects/def-coulomb/maxquant-parameters")
prepend_path("PATH", pathJoin(maxquant_parameters, "install"))
prepend_path("PATH", pathJoin(venv, "bash"))
prepend_path("PATH", pathJoin(venv, "bin"))
setenv("MAXQUANT_BASE", maxquant)
