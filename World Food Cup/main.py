import pandas as pd
import matplotlib.pyplot as plt

def melt_df(modded_df):
    melted_df = pd.melt(modded_df,
                        id_vars = ["ID","INT_FAMILIARITY", "INT_INTEREST", "GENDER", "AGE", "HOUSEHOLD_INCOME",
                                   "EDUCATION","REGION"],
                        var_name = "COUNTRY",
                        value_name = "RATING")
    return melted_df

def calc_country_percent(place, melt):
    country_df = melt.loc[melt["COUNTRY"] == place, :]
    country_tot =(country_df["RATING"].astype(int)).astype(bool).sum()

    country_5 = country_df.apply(lambda x: True if x["RATING"] == 5 else False, axis=1)
    country_5_count = country_5.sum()

    country_5_perc = country_5_count / country_tot * 100
    return country_5_perc

if __name__ == "__main__":
    url = (r"https://raw.githubusercontent.com/fivethirtyeight/data/master/food-world-cup/food-world-cup-data.csv")
    df = pd.read_csv(url, encoding="latin-1")

    # changing column names to shorten
    df.columns = ["ID", 'INT_FAMILIARITY', 'INT_INTEREST', "ALGERIA", "ARGENTINA", "AUSTRALIA", "BELGIUM",
                  "BOSNIA_AND_HERZEGOVINA", "BRAZIL", "CAMEROON", "CHILE", "COLUMBIA", "COSTA RICA", "CROATIA",
                  "ECUADOR",
                  "ENGLAND", "FRANCE", "GERMANY", "GHANA", "GREECE", "HONDURAS", "IRAN", "ITALY", "IVORY COAST",
                  "JAPAN",
                  "MEXICO", "NETHERLANDS", "NIGERIA", "PORTUGAL", "RUSSIA", "SOUTH KOREA", "SPAIN", "SWITZERLAND",
                  "UNITED_STATES", "URUAGUAY", "CHINA", "INDIA", "THAILAND", "TURKEY", "CUBA", "ETHIOPIA", "VIETNAM",
                  "IRELAND",
                  "GENDER", "AGE", "HOUSEHOLD_INCOME", "EDUCATION", "REGION"]

    mod_df = df.fillna("0")

    country_perc = {}  # countries and scores
    country_score = []  # intermediate list for scores

    # Populating the country name list
    country_name = list(df.columns)
    country_name = country_name[3:43]
#    print(len(country_name))

    melted = melt_df(mod_df)

    # Stores scores in a list
    for i in range(len(country_name)):
         country_score.append(calc_country_percent(country_name[i], melted))

    # Populate the country_perc dict
    country_perc["Country"] = country_name
    country_perc["5-Ratings"] = country_score

    # Export as CSV
    # output = pd.DataFrame(country_perc, columns=["Country", "5-Ratings"])
    # output.to_csv(r"C:\Users\Cliff Chen\Desktop\Country_Food_5_Ratings_Proportions.csv", index = False, header=True)

    # mod_df.to_csv(r"C:\Users\Cliff Chen\Desktop\Country (ALL) Scores.csv", index = False, header=True)

    # melted.to_csv(r"C:\Users\Cliff Chen\Desktop\Melted Scores CSV.csv", index = False, header=True)

    # Creating Final DataFrame
    world_df = pd.DataFrame(country_perc).loc[:, ["Country", "5-Ratings"]]
    print(world_df)

    # Plotting the Data in a Bar Graph
    plt.figure(figsize=(20,8))
    plt.bar(world_df["Country"], world_df["5-Ratings"])
    plt.xticks(world_df["Country"], rotation="vertical", size=12)
    plt.ylabel("5-Ratings (%)")
    plt.xlabel("Country")
    plt.title("Proportion of 5-Ratings for Desire to Try Each Country's Cuisine")
    plt.grid(axis="y")
    plt.show()

