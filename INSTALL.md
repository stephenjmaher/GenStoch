## Installation and requirements

The GenStoch package is a package for generating stochastic programming instances that is written in Python 3.

1. Create and activate the virtual environment (a new directory called "venv" gets created)

```
   virtualenv -p python3 venv
   source venv/bin/activate
```

2. Install the requirements (at this stage it is only numpy.)

```
   pip install .
```

3. Add the path to `instancegen` to your `PYTHONPATH`

4. You are done.

5. To exit the virtual environment, call

```
   deactivate
```

## Using GenStoch

The way to use GenStoch is though the scripts in the _scripts_ directory. After activating the virtual environment:

```
   source venv/bin/activate
```

A stochastic programming instance for sslp_2_25_50 instance comprised of 5 scenarios with right hand side stochasticity
is achieved by calling

```
   python scripts/smps_instance_generator.py sslp sslp2_25_50 5 rhs
```

If objective or coefficient stochasticity is required, then you replace _rhs_ with _obj_ or _coef_ respectively.

The stages file for the noswot instance is generated by calling

```
   python scripts/smps_write_tim_file.py noswot noswot
```