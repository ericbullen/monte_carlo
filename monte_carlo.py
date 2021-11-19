#!/usr/bin/env python3
# -*- coding: utf-8 -*-
####################################################
# Author: Eric Bullen
# Date: 19-Nov-2021
# Description: This is a "monte carlo" simulator for
# modeling financial scenarios
#
# https://github.com/ericbullen/monte_carlo
####################################################

import locale
import logging
import math
import os
import signal
import sys
import time
import multiprocessing as mp
from collections import Counter, defaultdict
from datetime import datetime
import FinanceFuture as future

from numpy import random
from tabulate import tabulate

locale.setlocale(locale.LC_ALL, ('en_US', 'utf-8'))

# Log to the screen
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter('%(asctime)s: "%(name)s" (line: %(lineno)d) - %(levelname)s %(message)s'))

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)

def run_experiment(iterations, max_years, output_queue, seed):
    random.seed(seed)

    def signal_handler(signal, frame):
        sys.exit()

    signal.signal(signal.SIGINT, signal_handler)

    rel_years = defaultdict(int)

    # Starting at 21 years old
    birth_year = 1999
    start_age = 21
    retire_age = 67

    ff = future.FinanceFuture(max_years=max_years)

    # End year is just a arbitrary name for when a
    # epoch moment happens. In this case, it's for
    # retirement (not getting a salary).
    start_year = birth_year + start_age 
    end_year = birth_year + retire_age

    ########################################################
    # These don't change between iterations
    ff.investment_withdraw_tax_rate = 0.20
    ff.income_tax_rate = .30

    try:
        for i in range(iterations):
            table = list()

            # Init things
            ff.shuffle_rates_and_returns()

            # Reset for each scenario
            ff.investment_money = 1
            ff.pretax_salary = 55555

            # These adjust for inflation
            ff.monthly_living_expenses = 888 
            ff.monthly_petty_expenses = 222 

            retirement_401k_base = 1111
            retire_ss_payment = 888

            simulation_date = datetime(year=start_year, month=12, day=31)
            stop_working_date = datetime(year=end_year, month=1, day=1)

            ##################################################################
            for rel_year in range(max_years):
                note = ""

                simulation_date = simulation_date.replace(year=start_year + rel_year)

                # Retirement expenses
                if simulation_date >= stop_working_date:
                    # Thse are adjusted for inflation - use today's
                    # amounts, not the future's
                    ff.monthly_living_expenses = 1111
                    ff.monthly_petty_expenses = 88 
                    ff.pretax_salary = 0
                else:
                    retirement_401k_base += 11

                ######################################################################################################
                # Figure out income/expenses
                yearly_income = ff.yearly_income(simulation_date, rel_year)
                yearly_expenses = ff.yearly_expenses(simulation_date, rel_year)

                # Collect SS now, baby! (stop once I hit 90)
                if birth_year + 67 <= simulation_date.year <= birth_year + 90:
                    yearly_income += retire_ss_payment * 12

                    if simulation_date.year >= birth_year + 90:
                        note = "* I'm probably dead (90 y.o.). No more SS money."
                        retire_ss_payment = 0

                net_income = yearly_income - yearly_expenses
                ff.investment_money += net_income

                ######################################################################################################
                if simulation_date.year == end_year:
                    note = "* I retire (401k cash-out of {0})".format(ff.dollar(retirement_401k_base))

                    ff.pretax_salary = 0

                    ff.historical_returns = ff.conservative_returns

                    ff.investment_money += retirement_401k_base
                    retirement_401k_base = 0
                else:
                    if retirement_401k_base:
                        # Bump my 401k based on investment returns
                        rate = ff.curr_conservative_rate(rel_year)
                        retirement_401k_base = retirement_401k_base * (1 + rate)

                if ff.investment_money <= 0:
                    # print("out of money {0}".format(rel_year))
                    note = "* OUT OF MONEY"

                if not SIMULATE:
                    table.append(
                        [
                            "{:>5s} {:>6s}".format(str(simulation_date.year), "({:+})".format(rel_year)),
                            ff.dollar(yearly_income),
                            ff.dollar(-yearly_expenses),
                            "{0:>5s} / {1:>6s}".format(ff.pct(ff.curr_inflation_rate(rel_year)), ff.pct(ff.curr_investment_rate(rel_year))),
                            ff.dollar(ff.orig_investment_money_afi(rel_year)),
                            ff.pct(ff.pct_change(ff.investment_money, ff.orig_investment_money_afi(rel_year))),
                            ff.dollar(ff.investment_money),
                            note
                        ])

                if ff.investment_money <= 0:
                    # Simulation failed
                    break

            if SIMULATE:
                # I just want the last year when it 'died'
                rel_years[rel_year] += 1
            else:
                rel_years = table
    except:
        # This traps the sys.exit()
        raise

    output_queue.put(rel_years)


if __name__ == "__main__":
    max_years = int(os.environ.get("MAX_YEARS", 100))
    SIMULATE = False
    SIMULATE = True

    output_queue = mp.Queue()

    if SIMULATE:
        table = list()
        cnt = Counter()

        runs = int(os.environ.get("RUNS", 10000))
        success_rate = float(os.environ.get("LOWER_PCT", .96))
        worker_count = mp.cpu_count()

        # Do the monte-carlo simulation
        # http://www.cfiresim.com/docs/faq.php#investigate
        iterations_per_cpu = math.ceil(runs / float(worker_count))

        def signal_handler(signal, frame):
            pass

        signal.signal(signal.SIGINT, signal_handler)

        # Flatten the list
        start_time = time.time()

        for i in range(worker_count):
            mp.Process(target=run_experiment, args=(iterations_per_cpu, max_years, output_queue, random.randint(0, 2 ** 32))).start()

        for i in range(worker_count):
            cnt.update(output_queue.get())

        elapsed_time = time.time() - start_time

        total_count = 0
        runs = sum(cnt.values())

        for year, count in reversed(sorted(cnt.items())):
            total_count += count
            pct = total_count / runs

            if pct >= success_rate:
                # Meaning, it's successful, so add it.
                table.insert(0, [year, count, "{:>.2%}".format(pct)])

        print("#")
        print("# Monte Carlo Runs: {0}\n# Run Time: {1:0.3f} seconds\n# Iters/Sec: {2:0.3f}".format(locale.format_string("%.*f", (0, runs), True), elapsed_time,
                                                                                                    runs / elapsed_time))
        print("#")

        headers = ["Relative Year", "Failures", "Success Confidence %"]
        print(tabulate(table, headers=headers, stralign="right"))

        print("\n* This report stops at what year the simulation success rate drops\n"
              "  below {pct:.0%}, or if it goes past {years} years. The last 'relative year'\n"
              "  column is the year when your defined scenario conditions cause\n"
              "  you to run out of money (the failure condition).".format(pct=success_rate, years=max_years))

    else:
        # This is for debugging if you want to see more details
        run_experiment(iterations=1, max_years=max_years, output_queue=output_queue, seed=random.randint(0, 2 ** 32))
        table = output_queue.get()

        headers = ["Year", "Income", "Expenses", "Inf./Int. (%)", "Orig Asset AGI",
                    "Asset Value (AGI)", "Investment Money", "Note"]

        print(tabulate(table, headers=headers, stralign="right"))
