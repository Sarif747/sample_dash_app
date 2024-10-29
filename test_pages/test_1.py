import pandas as pd
import random
from datetime import datetime, timedelta

def generate_synthetic_data(start_year, end_year, num_entries):
    synthetic_data = {
        "Date": [],
        "Counties Served": [],
        "Participants": [],
        "Training Type": []
    }

    counties = [
        "Clarke, Oconee, Madison, Jackson",
        "Morgan County",
        "Clarke County",
        "Madison County",
        "Madison, Elbert, Oglethorpe",
        "Barrow, Jackson, Walton, Oconee",
        "Greene County",
        "Newton County",
        "Jasper County",
        "Hall County",
        "Habersham County",
        "All 12 counties in the region"
    ]

    training_types = ["CRMI", "YMHAW", "CRMW", "CMW", "ACE/CRM", "CSFT"]

    for _ in range(num_entries):
        random_days = random.randint(0, (datetime(end_year, 12, 31) - datetime(start_year, 1, 1)).days)
        random_date = (datetime(start_year, 1, 1) + timedelta(days=random_days)).strftime("%B %d, %Y")

        synthetic_data["Date"].append(random_date)
        synthetic_data["Counties Served"].append(random.choice(counties))
        synthetic_data["Participants"].append(random.randint(5, 50))  # Ensuring no None values
        synthetic_data["Training Type"].append(random.choice(training_types))

    return synthetic_data

synthetic_data = generate_synthetic_data(2019, 2024, 50)

df = pd.DataFrame(synthetic_data)

print(df)
