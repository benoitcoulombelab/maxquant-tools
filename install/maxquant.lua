help([[
For detailed instructions, go to:
    https://maxquant.net

This module sets the following environment variables:
    MAXQUANT_BASE: directory containing MaxQuant programs and bash scripts

This module loads the following modules and their requirements:
    - mono/6.12.0.122
    - python/3.8.2
]])

whatis("Version: 1.0.1")
whatis("Keywords: MaxQuant, Utility")
whatis("URL: https://maxquant.net")
whatis("Description: MaxQuant is a quantitative proteomics software package designed for analyzing large mass-spectrometric data sets.")

always_load("mono/6.12.0.122")
always_load("python/3.8.2")

local home = os.getenv("HOME") or ""
local project = pathJoin(home, "projects/def-coulomb")
local maxquant_tools = pathJoin(project, "maxquant-tools")
local maxquant = pathJoin(project, "maxquant")
prepend_path("PATH", pathJoin(maxquant_tools, "bash"))
prepend_path("PATH", pathJoin(maxquant_tools, "venv/bin"))
setenv("MAXQUANT_BASE", maxquant)
setenv("MAXQUANT_TOOLS", maxquant_tools)
