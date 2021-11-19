# A multi-process "Monte Carlo" simulator written in Python

This is a docker container to run a "Monte Carlo" simulator to model financial conditions. I said "Monte Carlo" in quotes because I deduced what a Monte Carlo simulator did based on what people used it for, and came up with this.

You can build the docker container locally by doing:

```shell
$ make build
```

From there, you can run the docker container by passing the 3 env vars below (adjusting as desired):

```shell
$ docker run --rm -e MAX_YEARS=100 -e RUNS=10000 -e LOWER_PCT=.96  monte_carlo:1.0.0
# Monte Carlo Runs: 10,008
# Run Time: 7.142 seconds
# Iters/Sec: 1401.318
#
  Relative Year    Failures    Success Confidence %
---------------  ----------  ----------------------
             58           5                 100.00%
             59           8                  99.95%
             60           6                  99.87%
             61           6                  99.81%
             62          15                  99.75%
             63          25                  99.60%
             64          17                  99.35%
             65          21                  99.18%
             66          22                  98.97%
             67          38                  98.75%
             68          41                  98.37%
             69          38                  97.96%
             70          53                  97.58%
             71          48                  97.05%
             72          60                  96.57%

* This report stops at what year the simulation success rate drops
  below 96%, or if it goes past 100 years. The last 'relative year'
  column is the year when your defined scenario conditions cause
  you to run out of money (the failure condition).
```

Have fun.
