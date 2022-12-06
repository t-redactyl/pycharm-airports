#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

from sqlalchemy import create_engine


def transform_airlines_data(grouping_variable: str) -> pd.DataFrame:
    return (
        airlines[[grouping_variable, "FlightsTotal", "NumDelaysLateAircraft",
                  "NumDelaysSecurity", "NumDelaysWeather"]]
        .groupby(grouping_variable)
        .sum()
        .reset_index()
        .assign(proportion_delays_late=lambda x: x["NumDelaysLateAircraft"] / x["FlightsTotal"])
        .assign(proportion_delays_security=lambda x: x["NumDelaysSecurity"] / x["FlightsTotal"])
        .assign(proportion_delays_weather=lambda x: x["NumDelaysWeather"] / x["FlightsTotal"])
        .drop(columns=["FlightsTotal", "NumDelaysLateAircraft", "NumDelaysWeather",
                       "NumDelaysSecurity"])
    )


def reshape_airlines_data(transformed_data: pd.DataFrame, grouping_variable: str) -> pd.DataFrame:
    data = (
        pd.melt(transformed_data, id_vars=grouping_variable,
                value_vars=["proportion_delays_late", "proportion_delays_security", "proportion_delays_weather"])
        .rename(columns={
            "variable": "type_of_delay",
            "value": "proportion_delayed"
        })
        .assign(percent_delayed=lambda x: x["proportion_delayed"] * 100)
    )

    data["type_of_delay"] = data["type_of_delay"].map({"proportion_delays_late": "Flight delay",
                                                       "proportion_delays_security": "Security",
                                                       "proportion_delays_weather": "Weather"})

    return data


def create_sns_plot(data: pd.DataFrame) -> None:
    sns.set(rc={'figure.figsize': (15, 6)})
    fig1 = sns.barplot(
        data=data,
        x="AirportCode",
        y="percent_delayed",
        hue="type_of_delay"
    )
    fig1.set(xlabel="Airport", ylabel="Percentage of total flights delayed")
    plt.legend(title="Type of delay")
    plt.show()

airlines = pd.read_csv("data/airlines.csv")
#%%

if __name__ == "__main__":
    by_airline = reshape_airlines_data(transform_airlines_data("AirportCode"), "AirportCode")
    create_sns_plot(by_airline)
