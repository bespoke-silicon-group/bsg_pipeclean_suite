# BSG Pipeclean Suite

This repository contains a collection of designs used to stress test new CAD
flows. Each design is intended stress a different aspect of the CAD flow with
increasing complexity. The structure of each design is consistent to make it
easy for CAD flows to find and link all required files for the design. For
further details on how to get a design up and running, see the
[Design Usage](#design-usage) section.

These designs make use of the [IDEA Dimensionless 
(IDF)](https://docs.google.com/document/d/1rIB81hEOSNs2F1pIF6WbIwSNe-8HbfEtZRlaMFKdhKk/edit?usp=sharing)
specification. Floorplan and timing constraint files are _dimensionless_
meaning that all units are expressed in terms of properties of the process
rather than concrete units (such as microns or picoseconds). In-order to use
these designs, you will need access to basic PDK information such as the
metal layer stack properties and unit tile sizes as well as the [FO4 value](#fo4-calculation).
For easy integration of the floorplanning file into existing CAD flows, the IDF
floorplanning files can be converted to DEF files using the IDF-to-DEF converter
provided by the [BSG IDF Tools](https://github.com/bespoke-silicon-group/bsg_idf_tools). 

## Currently Available Designs

| Design Name  | Description                                       | Number of Gates |
|:------------:|:--------------------------------------------------|:---------------:|
| small_comb   | small sized combinational only design             | ~300            |
| medium_comb  | medium sized combinational only design            | ~3K             |
| large_comb   | large sized combinational only design             | ~30K            |
| black_parrot | 64-bit RISC-V Core with Cache Coherence Directory | ~125K           |

## Design Structure

Designs are structured in a consistent manner to make it easy for CAD flows to find all required
files. Each design should have the following file and directory structure:

```
<design_name>
+-- Makefile
+-- constraints.FO4.sdc
+-- floorplan.idf.json
+-- harden_me.v
+-- macro_generate.py
+-- pickled.v
```

| File                 | Description                                                                                                                                              |
|:---------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------|
| Makefile             | Makefile to facilitate in running _macro_generate.py_ and [IDF-to-DEF converter](https://github.com/bespoke-silicon-group/bsg_idf_tools) utility script. |
| constraints.FO4.sdc  | SDC timing constraints which depends on the [FO4 value](#fo4-calculation) for the target process.                                                        |
| floorplan.idf.json   | [IDF Floorplan](https://docs.google.com/document/d/1rIB81hEOSNs2F1pIF6WbIwSNe-8HbfEtZRlaMFKdhKk/edit?usp=sharing) constraints file.                      |
| harden_me.v          | Additional design file that contains blocks that are intended to be hardened for correct quality-of-results (requires additional setup).                 |
| macro_generate.py    | Used to call macro generators for the target process (requires additional setup).                                                                        |
| pickled.v            | Main design RTL file that has been pickled into a single .v file.                                                                                        |

## Design Usage

These designs are _dimensionless_ and process agnostic, therefore to properly integrate them into a CAD flow and get the expected
quality-of-result (QoR) we need to re-dimensionalize the designs. For each design, you should do the following items and the
execute the Makefile in the design by simply running `$ make` while in the design directory.

### Macro Generation (_macro_generate.py_)

Inside the IDF Floorplan file is a "harden" section which describes components in the design that are either macro blocks or
pre-synthesized gate netlists. For macro generation, there is a python script inside each design call _macro_generate.py_. The
intention of this script is to read the IDF Floorplan file and use that info to call macro generators. However, macro generators
are process specific therefore the user is required to setup the script to shell out the correct commands. A small amount of
framework has been implemented in _macro_generate.py_ however it is up to the user to get the generators operational.

### Harened Verilog Model (_harden_me.v_)

In-order to instantiate hardened blocks they must be instantiated properly in the RTL. This will be done inside
`harden_me.v`. This file contains a collection of modules with synthesizable RTL models that are intended to
be replaced with the hardened instance (either a macro or pre-synthesized netlist). The user should use the RTL
model to ensure that the semantics of the hardened block match what the design expects.

### IDF to DEF Conversion

The easiest way to integrate the [IDF Floorplan](https://docs.google.com/document/d/1rIB81hEOSNs2F1pIF6WbIwSNe-8HbfEtZRlaMFKdhKk/edit?usp=sharing)
into a cad flow is to first convert it into a design exchange format (DEF) file. DEF files are standardized
floorplan files. By converting the IDF Floorplan to a DEF file, you will also be re-dimensionalizing the 
floorplan. Therefore, you will need access to the PDK's technology file (.tf). In the Makefile for the design,
set the `TECHNOLOGY_FILE` variable to the path of the PDK's technology file. When you run `$ make` one of the
steps is to run the IDF to DEF converter script. Alternatively, you can run `$ make TECHNOLOGY_FILE=<path>` if
you do not want to modify the Makefile.

## FO4 Calculation

For timing constraints, you will need to determine the fan-out-of-4 (FO4) value for your given process and
set the environment variable `FO4` to the FO4 value for your PDK:

```
(bash)  export FO4=<value>
(csh)   setenv FO4 <value>
```

To calculate the FO4, it is highly recommended to use a SPICE simulation (we use Synopsys HSpice) with parasitic
extracted standard cell models. The following circuit is what we use to calculate the FO4:

![image](https://drive.google.com/uc?export=view&id=1E3TDwMpNMGvCMUYx0UFR4Vp8miB60Wnl)

The actual FO4 value is the propagation delay for an inverter in the ring (averaged
between the rising and falling propagation delay, triggered at (VDD-VSS)/2). It is 
important to use many stages to make sure that the signal propagating through the ring
oscillator is going from rail-to-rail. Anecdotal, 7-stages seems to be enough for most
cases however it is always recommended to open up the waveform and verify that the
signal is reaching VDD and VSS.
