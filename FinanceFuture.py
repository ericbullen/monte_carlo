import locale
import numpy as np
from numpy import random

class FinanceFuture(object):
    def __init__(self, max_years, rand_seed=None):
        if rand_seed is not None:
            self.rand_seed = rand_seed
            random.seed(self.rand_seed)

        self.max_years = max_years

        ##################################################################################################################
        # Data
        # 100 years
        self.inflation_rates = list()
        self.property_growth_rates = list()
        self.conservative_returns = list()
        self.historical_returns = list()

        self.cascaded_inflation_rates = list()
        self.cascaded_property_growth_rates = list()
        self.cascaded_historical_returns = list()
        self.cascaded_conservative_returns = list()

        ##############################
        # Mean: 3.30396, STDev: 4.8447
        self.base_inflation_rates = np.array([1.0, 1.0, 7.9, 17.4, 18.0, 14.6, 15.6, -10.5, -6.1, 1.8, 0.0, 2.3, 1.1, -1.7, -1.7,
                                              0.0, -2.3, -9.0, -9.9, -5.1, 3.1, 2.2, 1.5, 3.6, -2.1, -1.4, 0.7, 5.0, 10.9, 6.1,
                                              1.7, 2.3, 8.3, 14.4, 8.1, -1.2, 1.3, 7.9, 1.9, 0.8, 0.7, -0.4, 1.5, 3.3, 2.8, 0.7,
                                              1.7, 1.0, 1.0, 1.3, 1.3, 1.6, 2.9, 3.1, 4.2, 5.5, 5.7, 4.4, 3.2, 6.2, 11.0, 9.1,
                                              5.8, 6.5, 7.6, 11.3, 13.5, 10.3, 6.2, 3.2, 4.3, 3.6, 1.9, 3.6, 4.1, 4.8, 5.4, 4.2,
                                              3.0, 3.0, 2.6, 2.8, 3.0, 2.3, 1.6, 2.2, 3.4, 2.8, 1.6, 2.3, 2.7, 3.4, 3.2, 2.8,
                                              3.8, -0.4, 1.6, 3.2, 2.1, 1.5, 1.6], dtype=np.float16)

        # Inflation since 1983 - more realistic
        # Mean: 2.72667, STDev: 1.30279
        self.base_inflation_rates = np.array([0.73, 0.76, 1.50, 1.74, 2.96, 1.50, 2.72, 0.09, 4.08, 2.54, 3.42, 3.26, 1.88, 2.38,
                                              1.55, 3.39, 2.68, 1.61, 1.70, 3.32, 2.54, 2.67, 2.75, 2.90, 3.06, 6.11, 4.65, 4.42,
                                              4.43, 1.10, 3.80, 3.95, 3.79], dtype=np.float16)

        self.base_inflation_rates = [random.normal(2.72667, 1.30279) for i in range(self.max_years)]

        ######################################
        # Grants pass propety assessment rates
        # Mean: 2.87, STDev: 1.3945
        self.base_property_growth_rates = [random.normal(2.87, 1.3945) for i in range(self.max_years)]
        self.base_property_growth_rates = np.array([4.2, 2.8, 3.7, 2.0, 3.1, 1.1, 5.8, 2.2, 2.2, 1.6], dtype=np.float16)

        ###################################
        # S&P 500 annual returns since 1970
        # Mean: 11.842, STDev: 17.2141
        self.snp_500_historical_returns = [random.normal(11.842, 17.2141) for i in range(self.max_years)]
        self.snp_500_historical_returns = np.array([3.56, 14.22, 18.76, -14.31, -25.90, 37.00, 23.83, -6.98, 6.51, 18.52, 31.74,
                                                    -4.70, 20.42, 22.34, 6.15, 31.24, 18.49, 5.81, 16.54, 31.48, -3.06, 30.23,
                                                    7.49, 9.97, 1.33, 37.20, 22.68, 33.10, 28.34, 20.89, -9.03, -11.85, -21.97,
                                                    28.36, 10.74, 4.83, 15.61, 5.48, -36.55, 25.94, 14.82, 2.10, 15.89, 32.15, 13.48], dtype=np.float16)

        ###############################
        # The wilshire 5000 index fund
        # Mean: 12.3976, STDev: 16.6083
        self.wilshire_5000_historical_returns = [random.normal(12.3976, 16.6083) for i in range(self.max_years)]
        self.wilshire_5000_historical_returns = np.array([13.51, 32.18, 15.82, 1.97, 14.91, 26.49, -37.02, 5.39, 15.64, 4.77, 10.74,
                                                          28.50, -22.15, -12.02, -9.06, 21.07, 28.62, 33.19, 22.88, 37.45, 1.18, 9.89,
                                                          7.42, 30.22, -3.32, 31.36, 16.22, 4.71, 18.06, 31.23, 6.21, 21.29, 20.97,
                                                          -5.21, 31.92, 18.05, 5.87, -7.84], dtype=np.float16)

        #############################
        # Dow Jones, too
        # Mean: 9.897, STDev: 15.2716
        self.djia_historical_returns = [random.normal(9.897, 15.2716) for i in range(self.max_years)]
        self.djia_historical_returns = np.array([38.32, 17.86, -17.27, -3.15, 4.19, 14.93, -9.23, 19.61, 20.27, -3.74, 27.66, 22.58,
                                                 2.26, 11.85, 26.96, -4.34, 20.32, 4.17, 13.72, 2.14, 33.45, 26.01, 22.64, 16.10,
                                                 25.22, -6.18, -7.10, -16.76, 25.32, 3.15, -0.61, 16.29, 6.43, -33.84, 18.82, 11.02,
                                                 5.53, 7.26, 26.50, 7.52], dtype=np.float16)

        ###############################
        # And of course the nasdaq
        # Mean: 14.4695, STDev: 25.2583
        self.nasdaq_historical_returns = [random.normal(14.4695, 25.2583) for i in range(self.max_years)]
        self.nasdaq_historical_returns = np.array([29.76, 26.10, 7.33, 12.31, 28.11, 33.88, -3.21, 18.67, 19.87, -11.22, 31.36, 7.36,
                                                   -5.26, 15.41, 19.26, -17.80, 56.84, 15.45, 14.75, -3.20, 39.92, 22.71, 21.64, 39.63,
                                                   85.59, -39.29, -21.05, -31.53, 50.01, 8.59, 1.37, 9.52, 9.81, -40.54, 43.89, 16.91,
                                                   -1.80, 15.91, 38.32, 13.40], dtype=np.float16)

        ########################################################
        # A retirement fund recommended by USNews & World Report
        # Mean: 5.18, STDev: 6.14295
        self.vtinx_historical_returns = [random.normal(5.18, 6.14295) for i in range(self.max_years)]
        self.vtinx_historical_returns = np.array([-0.17, 5.54, 5.87, 8.23, 5.25, 9.39, 14.28, -10.93, 8.17, 6.38, 3.33, 6.82], dtype=np.float16)

        # This is a good one it looks like
        self.vone_historical_returns = []

        #########################################################
        # Set the non-retirement investment returns you want here
        self.base_historical_returns = self.djia_historical_returns
        self.base_historical_returns = self.wilshire_5000_historical_returns
        self.base_historical_returns = self.snp_500_historical_returns
        self.base_historical_returns = self.vtinx_historical_returns

        #############################################################################
        # Conservative returns. Retirement returns should be between 6% & 7% annually
        self.base_conservative_returns = self.djia_historical_returns
        self.base_conservative_returns = self.snp_500_historical_returns
        self.base_conservative_returns = self.wilshire_5000_historical_returns
        self.base_conservative_returns = self.vtinx_historical_returns

        #############################################################################
        # Expenses
        self.investment_withdraw_tax_rate = 0
        self.income_tax_rate = 0

        ###############################################
        self.pretax_salary = 0
        self.base_investment_money = 0
        self.investment_money = 0

        # Misc
        self._monthly_petty_expenses = 0
        self._monthly_living_expenses = 0
        self._yearly_mortgage_payment = 0

        # Now, get all the rates prepped
        self.prep_rates()
        self.shuffle_rates_and_returns()

    @property
    def monthly_petty_expenses(self):
        return self._monthly_petty_expenses

    @property
    def monthly_living_expenses(self):
        return self._monthly_living_expenses

    @monthly_petty_expenses.setter
    def monthly_petty_expenses(self, value):
        self._monthly_petty_expenses = value
        self.yearly_withdraw_amount = (self._monthly_petty_expenses + self._monthly_living_expenses) * 12

    @monthly_living_expenses.setter
    def monthly_living_expenses(self, value):
        self._monthly_living_expenses = value
        self.yearly_withdraw_amount = (self._monthly_petty_expenses + self._monthly_living_expenses) * 12

    def prep_rates(self):
        # Data munging now
        self.base_inflation_rates = list(map(lambda num: num / 100, self.base_inflation_rates))
        self.base_property_growth_rates = list(map(lambda num: num / 100, self.base_property_growth_rates))
        self.base_conservative_returns = list(map(lambda num: num / 100, [rate for rate in self.base_conservative_returns if -100 <= rate <= 100]))
        self.base_historical_returns = list(map(lambda num: num / 100, [rate for rate in self.base_historical_returns if -100 <= rate <= 100]))

        inflation_len = len(self.base_inflation_rates) - 1
        prop_rate_len = len(self.base_property_growth_rates) - 1
        historical_len = len(self.base_historical_returns) - 1
        conservative_len = len(self.base_conservative_returns) - 1

        # Extend it out to max_years in length
        self.base_inflation_rates.extend([random.choice(self.base_inflation_rates) for _x in range(self.max_years - inflation_len)])
        self.base_property_growth_rates.extend([random.choice(self.base_property_growth_rates) for _x in range(self.max_years - prop_rate_len)])
        self.base_historical_returns.extend([random.choice(self.base_historical_returns) for _x in range(self.max_years - historical_len)])
        self.base_conservative_returns.extend([random.choice(self.base_conservative_returns) for _x in range(self.max_years - conservative_len)])

    def shuffle_rates_and_returns(self):
        ###############################################
        # Cleaning up, and prepping the data
        self.inflation_rates = random.permutation(self.base_inflation_rates)
        self.property_growth_rates = random.permutation(self.base_property_growth_rates)
        self.historical_returns = random.permutation(self.base_historical_returns)
        self.conservative_returns = random.permutation(self.base_conservative_returns)

        self.cascaded_inflation_rates = self.cascade(self.inflation_rates, len(self.inflation_rates))
        self.cascaded_property_growth_rates = self.cascade(self.property_growth_rates, len(self.property_growth_rates))
        self.cascaded_historical_returns = self.cascade(self.historical_returns, len(self.historical_returns))
        self.cascaded_conservative_returns = self.cascade(self.conservative_returns, len(self.conservative_returns))

    def cascade(self, sequence, end):
        # return functools.reduce(operator.mul, [rate + 1 for rate in sequence[0:end]])
        new_seq = list()
        end += 1

        sequence = sequence[0:end]

        new_seq.append(1 + sequence[0])

        for index in range(1, len(sequence)):
            prev_rate = new_seq[index - 1]
            curr_rate = sequence[index]

            result = prev_rate * (1 + curr_rate)
            new_seq.append(result)

        return new_seq

    # Cascade's solid code
    # pp(cascade(None, [0.1, 0.1, 0.1, 0.1, -0.1, 0.1, 0.1, 0.1, 0.1, 0.1], 10))
    # sys.exit()

    def curr_conservative_rate(self, rel_year):
        return self.conservative_returns[rel_year % self.max_years]

    def curr_investment_rate(self, rel_year):
        return self.historical_returns[rel_year % self.max_years]

    def curr_inflation_rate(self, rel_year):
        return self.inflation_rates[rel_year % self.max_years]

    def yearly_withdraw_amount_afi(self, rel_year):
        return self.yearly_withdraw_amount * self.cascaded_inflation_rates[rel_year % self.max_years]

    def withdraw_income_tax(self, rel_year):
        return self.yearly_withdraw_amount_afi(rel_year) * self.investment_withdraw_tax_rate

    def yearly_expenses(self, run_date, rel_year):
        withdraw_amt_afi = self.yearly_withdraw_amount_afi(rel_year)
        inc_tax = self.withdraw_income_tax(rel_year)

        return withdraw_amt_afi + inc_tax

    def yearly_income(self, run_date, rel_year):
        inv_money = self.investment_money
        curr_inv_rate = self.curr_investment_rate(rel_year)
        yearly_salaries = self.yearly_salaries()

        return (inv_money * curr_inv_rate) + yearly_salaries

    def yearly_salaries(self):
        return (self.pretax_salary - (self.pretax_salary * self.income_tax_rate))

    def orig_investment_money_afi(self, rel_year):
        return self.base_investment_money * self.cascaded_inflation_rates[rel_year % self.max_years]

    def dollar(self, value):
        return locale.currency(value, grouping=True)

    def ppmt(self, rate, per, nper, pv, fv=None, type=None):
        """Calculates the payment on the principal for
        a given investment, with periodic constant
        payments and a constant interest rate """

        return self.pmt(rate, nper, pv, fv, type) - self.ipmt(rate, per, nper, pv, fv, type)

    def ipmt(self, rate, per, nper, pv, fv=None, type=None):
        """Calculates the interest payment for a given
        period of an investment, with periodic constant
        payments and a constant interest rate """

        if fv is None:
            fv = 0

        if type is None:
            type = 0

        return (pv * rate * ((rate + 1) ** (nper + 1) - (rate + 1) ** per)) / ((rate + 1) * ((rate + 1) ** nper - 1))

    # Payment Functions
    def cumipmt(self, rate, nper, pv, start_period, end_period, type=None):
        """Calculates the cumulative interest paid
        between two specified periods """

        if type is None:
            type = 0

        return sum([self.ipmt(rate, per, nper, pv, 0, type) for per in range(start_period, end_period + 1)])

    def cumprinc(self, rate, nper, pv, start_period, end_period, type=None):
        """Calculates the cumulative principal paid on
        a loan, between two specified periods """

        if type is None:
            type = 0

        return sum([self.ppmt(rate, per, nper, pv, 0, type) for per in range(start_period, end_period + 1)])

    def pct(self, value, places=None):
        if not places:
            places = 2

        return "{:>.{}%}".format(value, places)

    def nf(self, value, places=0):
        return locale.format("%.*f", (places, value), True)

    def pct_change(self, from_val, to_val):
        if to_val == 0:
            return 0
        else:
            return (from_val / to_val) - 1

    @classmethod
    def pmt(cls, rate, nper, pv, fv=None, type=None):
        """Calculates the payments required to reduce a
        loan, from a supplied present value to a
        specified future value """
        if type is None:
            type = 0

        if fv is None:
            fv = 0

        if rate == 0:
            return (-fv - pv) / nper
        else:
            return (rate * (fv + pv * (1 + rate) ** nper)) / ((1 + type * rate) * (-1 + (1 + rate) ** nper))

