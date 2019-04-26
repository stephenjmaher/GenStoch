# Generating Stochastic Programming Instances

A simple python package for the generation of stochastic programming instances in the [SMPS format][1]. Different to
other instance generation packages, the _GenStoch_ package requires a core (or base) file on which a stochastic program
is generated. Since the core file is in the format of an MPS file, it is possible to generate scenarios for any instance
that is currently available in MPS format.

There are two main uses of this package:

1. The generation of new stochastic programming instances for instances currently available in SMPS format.
1. The generation of a stochastic programming instance from an instance in MPS format. For this case, it must be
   possible to decompose the constraints into first and second stages.

This package currently only generates discrete scenarios for two-stage stochastic programs.

## Concept

A major part of mathematical programming research is the experimentation with solution algorithms. This experimentation
is only possible with problem instances. While there are many different instance libraries available, there is a limited
supply of stochastic programming instances in SMPS format.

An issue with the current instance sets is that the total number of unique instances can be small. For example, the SSLP
instances from the [SIPLIB](https://www2.isye.gatech.edu/~sahmed/siplib/) is comprised of 12 instances. It can be
difficult to draw conclusions regarding an algorithm performance based on such a test set alone.

This package aims to address the limited number of instances by enabling the generation of additional second stages for
the base core files. These additional second stages, while not completely new instances, can be sufficiently different
enough to create a larger test set.

The main idea of this package is to provide the framework for generating stochastic programs. As such, the main features
are the reading of the core and stages files and the available virtual functions that can be derived for the writing of
the stochastic information file.

## Features

A base `Instance` class is available in `smps_instance.py`. This class provides the reading functionality of the core
and stages (.tim) SMPS files. The base class has member variables

- `constraints`: a list of constraint names in the core file
- `variables`: a list of variable names in the core file
- `coeffs`: a dictionary storing the coefficients for the variables in the constraints. The coefficient is accessed by
  `coeff[<varname>, <consname>]`
- `rhs`: a dictionary storing the right hand sides of the constraints. The right has side is accessed by `rhs[<consname>]`
- `periods`: a list of lists storing the stages information. Each entry consists of `[stagename, varname, consname]`

The user can derive new instance classes from the base `Instance` class. The derived class implements the output
functions that are used to write the stochastic information file (.sto) and the stages file (.tim). These virtual
functions are:

- `writeRhsStochasticFile`: writes a stochastic information file with right hand side stochasticity
- `writeCoefStochasticFile`: writes a stochastic information file with stochasticity in the constraint coefficients
- `writeObjStochasticFile`: writes a stochastic information file with stochasticity in the objective function
  coefficients
- `writeStageFile`: writes a stage (.tim) file. When defining this class, the user must specify where the change point
  is for each of the stages.

Any derived classes need to be added to the `instances` dictionary in the `__init__.py` file.

The package supports the writing of stochastic files for the SSLP instances from SIPLIB and [Recoverable robust tail
assignment (RRTAP) instances][2]. Also, it is possible to write the stages file for the
[NOSWOT](http://miplib2010.zib.de/miplib2010/noswot.php) instance and for the [SNIP][3] instances.

## Scripts

Two scripts are available:

- `smps_instance_generator`: generates a stochastic programming instance given a core and stage file. This function
  calls the appropriate write function (see above), as specified by the `type` parameter ('rhs' by default). The output
  stochastic information file is based on the specification in the derived classes. For the SSLP and RRTAP, the output
  involves randomly generating right hand side, constraints or objective coefficient values using the `np.random`
  function.
- `smps_write_tim_file`: writes a stages file for a given core file. The stages file is created based on the constraint
  and variable names from the core file.

\[1\]: Birge, J. R.; Dempster, M. A.; Gassmann, H. I.; Gunn, E.; King, A. J. & Wallace, S. W. A standard input format for multiperiod stochastic linear programs IIASA, Laxenburg, Austria, IIASA, Laxenburg, Austria, WP-87-118, 1987
\[2\]: Maher, S. J.; Desaulniers, G. & Soumis, F. Recoverable robust single day aircraft maintenance routing problem Computers & Operations Research, 2014, 51, 130-145
\[3\]: Bodur, M.; Dash, S.; Günlük, O. & Luedtke, J. Strengthened Benders Cuts for Stochastic Integer Programs with Continuous Recourse INFORMS Journal on Computing, 2017, 29, 77-91
