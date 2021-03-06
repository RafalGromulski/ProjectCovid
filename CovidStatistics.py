import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.width', 200)
pd.set_option('display.max_columns', 15)
pd.set_option('display.max_rows', 100)

confirmed_global = r"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
deaths_global = r"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
recovered_global = r"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"

confirmed_covid = pd.read_csv(confirmed_global)
deaths_covid = pd.read_csv(deaths_global)
recovered_covid = pd.read_csv(recovered_global)


def _get_info(country, data, category):
    """
    >>> _get_info("Spain", confirmed_covid, "Confirmed").loc["2022-03-01"]
    Confirmed    11036085
    Name: 2022-03-01 00:00:00, dtype: Int64

    >>> _get_info("Sweden", deaths_covid, "Deaths").loc["2022-02-28"]
    Deaths    17142
    Name: 2022-02-28 00:00:00, dtype: Int64

    >>> _get_info(None, deaths_covid, "Deaths").loc["2022-01-06"]
    Deaths    5473369
    Name: 2022-01-06 00:00:00, dtype: Int64
    """
    if country is not None:
        data = data.query('`Country/Region` == @country')
    df = data.transpose()[4:].sum(axis="columns").astype("int64")
    df = pd.DataFrame(df)
    df.columns = [category]
    df.index = df.index.map(pd.to_datetime)
    df = df.convert_dtypes()
    return df


def covid(country=None):
    """
    >>> covid("Poland").loc["2022-04-01"]
    Confirmed    5966970
    Deaths        115247
    Recovered          0
    Name: 2022-04-01 00:00:00, dtype: Int64

    >>> covid("Italy").loc["2022-02-01"]
    Confirmed    11116422
    Deaths         146925
    Recovered           0
    Name: 2022-02-01 00:00:00, dtype: Int64

    >>> covid().loc["2022-01-01"]
    Confirmed    289928718
    Deaths         5440837
    Recovered            0
    Name: 2022-01-01 00:00:00, dtype: Int64
    """
    return pd.concat((
        _get_info(country, confirmed_covid, "Confirmed"),
        _get_info(country, deaths_covid, "Deaths"),
        _get_info(country, recovered_covid, "Recovered")
    ), axis="columns")


def covid_fatality_plot(data):
    fatality_rate = data["Deaths"] / data["Confirmed"]
    fatality_percent = fatality_rate * 100
    fatality_percent.plot(kind="line",
                          title="Percent of deaths vs new cases of Covid",
                          xlabel="Day",
                          ylabel="Percent",
                          figsize=(7, 7),
                          grid=True)
    plt.show()


def confirmed_daily_increase_plot(data):
    data["Confirmed"].diff().plot(kind="line",
                                  title="Daily increase of confirmed cases",
                                  xlabel="Day",
                                  ylabel="Confirmed cases",
                                  figsize=(7, 7),
                                  grid=True)
    plt.show()


def deaths_monthly_plot(data):
    data["Deaths"].diff().resample("M").sum().plot(kind="line",
                                                   title="Monthly increase of deaths",
                                                   xlabel="Day",
                                                   ylabel="Deaths",
                                                   figsize=(7, 7),
                                                   grid=True)
    plt.show()


def deaths_last_period_plot(data, period):
    data["Deaths"].last(period).diff().plot(kind="line",
                                            title="Increase of deaths in selected period to today",
                                            xlabel="Day",
                                            ylabel="Deaths",
                                            figsize=(7, 7),
                                            grid=True)
    plt.show()


if __name__ == "__main__":
    poland = covid("Poland")
    spain = covid("Spain")
    sweden = covid("Sweden")
    italy = covid("Italy")
    world = covid()

    covid_fatality_plot(poland)
    deaths_monthly_plot(spain)
    confirmed_daily_increase_plot(sweden)
    deaths_last_period_plot(italy, "M")  # last month
    deaths_last_period_plot(world, "3W")  # last three weeks
