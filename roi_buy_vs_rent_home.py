"""
# Usage

Change the parameters of function `compute_least_price_to_sell()` and run
`python3 roi_buy_vs_rent_home.py`


# Assumptions

1. Inflation grows in a constant rate
2. Rent grows in a constant rate
3. HOA grows in a constant rate
4. Home insurance grows in a constant rate
5. Down payment opportunity cost is considered as to invest the down payment to
   SP500, with a constant given annual rate of return


# Outputs

* Monthly mortgage payment
* Buy house gross pay in n years holding
* Rent house gross pay in n years
* Remaining principal on mortgage
* Minimum price to sell after holding n years for breaking even
"""

import math

def compute_mortgage_monthly_payment(*, p, r, n):
    return p * r * (1 + r) ** n / ((1 + r) ** n - 1)

def compute_remaining_principal_on_mortgage(*, m, r, n):
    return (m/r) * (1 - (1 / (1 + r) ** n))

def compute_least_price_to_sell(
        *, house_price, rent_price, down_payment_ratio, interest_rate_yearly,
        num_year_mortgage_expired, num_year_held, rent_increase_rate_yearly,
        inflation_rate_yearly, hoa, hoa_increase_rate_yearly,
        property_tax_rate, home_insurance_rate, extra_down_payment,
        sp500_roi_yearly):

    mortgage_monthly_payment = compute_mortgage_monthly_payment(
            p=house_price * (1 - down_payment_ratio),
            r=interest_rate_yearly / 12,
            n=num_year_mortgage_expired * 12)
    print("Monthly mortgage payment: ${}".format(round(mortgage_monthly_payment, 2)))

    down_payment = house_price * down_payment_ratio + extra_down_payment
    down_payment_opportunity_cost = down_payment
    buy_house_cost = 0
    rent_house_cost = 0
    mortgage_pay = mortgage_monthly_payment * 12
    hoa_pay = hoa * 12
    property_tax_pay = house_price * property_tax_rate
    home_insurance_pay = house_price * home_insurance_rate
    rent_pay = rent_price * 12
    for i in range(1, num_year_held + 1):
        down_payment_opportunity_cost *= (1 + sp500_roi_yearly)
        mortgage_pay /= (1 + inflation_rate_yearly)
        hoa_pay *= (1 + hoa_increase_rate_yearly) / (1 + inflation_rate_yearly)
        property_tax_pay /= (1 + inflation_rate_yearly)
        home_insurance_pay /= (1 + inflation_rate_yearly)
        rent_pay *= (1 + rent_increase_rate_yearly) / (1 + inflation_rate_yearly)
        buy_house_cost += (mortgage_pay + hoa_pay + property_tax_pay +
                           home_insurance_pay)
        rent_house_cost += rent_pay

    print("Buy house gross pay in {} years holding: ${}".format(
        num_year_held, round(buy_house_cost, 2)))
    print("Rent house gross pay in {} years: ${}".format(
        num_year_held, round(rent_house_cost, 2)))

    remaining_principal_on_mortgage = compute_remaining_principal_on_mortgage(
        m=mortgage_monthly_payment,
        r=interest_rate_yearly / 12,
        n=(num_year_mortgage_expired-num_year_held) * 12)
    print("Remaining principal on mortgage: ${}".format(
        round(remaining_principal_on_mortgage, 2)))

    min_price_to_sell = (remaining_principal_on_mortgage + buy_house_cost -
        rent_house_cost + down_payment_opportunity_cost)
    print("Minimum price to sell after holding {} years for breaking even: ${}".format(
        num_year_held, round(min_price_to_sell, 2)))
    return min_price_to_sell


compute_least_price_to_sell(house_price=1000000,
                            rent_price=2000.0,
                            down_payment_ratio=20/100,
                            interest_rate_yearly=4.5/100,
                            num_year_mortgage_expired=30,
                            num_year_held=7,
                            rent_increase_rate_yearly=10/100,
                            inflation_rate_yearly=2/100,
                            hoa=0,
                            hoa_increase_rate_yearly=1.15/100,
                            property_tax_rate=0.93/100,
                            home_insurance_rate=(0.5 + 0.1)/100,
                            extra_down_payment=0,
                            sp500_roi_yearly=0.1)
