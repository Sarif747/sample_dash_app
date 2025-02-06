import random
import pandas as pd
from datetime import datetime, timedelta

event_types = ["Training", "Awareness Event", "Community Outreach"]
training_types = ["Connections Matter", "ASIST (Applied Suicide Intervention Skills Training)", 
                  "CRM (Community Resiliency Model)", "MHFA (Mental Health First Aid)", 
                  "QPR (Question, Persuade, Refer)", "Resilient Parent, Becoming A", 
                  "SafeTALK", "Strengthening Families Georgia"]
audiences = ["Youth-Serving Org", "Community", "First Responders", "Parents/Caregivers", 
             "Faith-Based Org", "Social Services", "Business"]
alignment = ["Prevent ACEs/Foster PCEs", "Expand Access in Rural/Under Resourced Area", 
             "Convene and Align Training Groups", "Promote Sustainable Systems/Policy Change"]
counties = ["Thomas", "Grady", "Decatur", "Mitchell", "Brooks", "Colquitt", "Miller", "Seminole", "Early"]
ethnicities = ["Native Hawaiian or Other Pacific Islander", "Asian", "American Indian or Alaska Native", 
               "White", "Black/African American", "Middle Eastern or North African", 
               "Hispanic or Latino", "Multiracial"]

def generate_random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_date = start_date + timedelta(days=random_days)
    return random_date.strftime('%m/%d/%Y')

def generate_synthetic_data(num_entries):
    synthetic_data = {
        "Date": [],
        "Name of Event or Training": [],
        "Type of Event": [],
        "Training Type (if applicable)": [],
        "Duration (Hours)": [],
        "Virtual or In-Person": [],
        "Location": [],
        "Training or Event Capacity": [],
        "Total Participants": [],
        "Total Registrants": [],
        "Percent of participants with increased knowledge, skills, and/or abilities": [],
        "Population/Audience/Sector": [],
        "Is this training a part of an organizational policy?": [],
        "Alignment with RG strategic map": [],
        "Number of Native Hawaiian or Other Pacific Islander Participants": [],
        "Number of Asian Participants": [],
        "Number of American Indian or Alaska Native Participants": [],
        "Number of White Participants": [],
        "Number of Black/African American Participants": [],
        "Middle Eastern or North African": [],
        "Number of Hispanic or Latino Participants": [],
        "Number of Multiracial Participants": [],
        "Notes and Additional Information": []
    }
    
    start_date = datetime(2023, 10, 1)
    end_date = datetime(2023, 12, 31)
    
    for _ in range(num_entries):
        synthetic_data["Date"].append(generate_random_date(start_date, end_date))
        synthetic_data["Name of Event or Training"].append(f"Event {random.randint(1, 100)}")
        synthetic_data["Type of Event"].append(random.choice(event_types))
        synthetic_data["Training Type (if applicable)"].append(random.choice(training_types) if random.random() < 0.7 else "N/A")
        synthetic_data["Duration (Hours)"].append(random.randint(1, 4))
        synthetic_data["Virtual or In-Person"].append(random.choice(["Virtual", "In-Person"]))
        synthetic_data["Location"].append(random.choice(counties))
        synthetic_data["Training or Event Capacity"].append(random.randint(20, 100))
        synthetic_data["Total Participants"].append(random.randint(10, 100))
        synthetic_data["Total Registrants"].append(random.randint(10, 100))
        synthetic_data["Percent of participants with increased knowledge, skills, and/or abilities"].append(
            f"{random.randint(50, 100)}%" if random.random() < 0.8 else "N/A")
        synthetic_data["Population/Audience/Sector"].append(random.choice(audiences))
        synthetic_data["Is this training a part of an organizational policy?"].append(random.choice(["Yes", "No"]))
        synthetic_data["Alignment with RG strategic map"].append(random.choice(alignment))
        
        ethnic_participants = {ethnicity: random.randint(0, 10) for ethnicity in ethnicities}
        synthetic_data["Number of Native Hawaiian or Other Pacific Islander Participants"].append(ethnic_participants["Native Hawaiian or Other Pacific Islander"])
        synthetic_data["Number of Asian Participants"].append(ethnic_participants["Asian"])
        synthetic_data["Number of American Indian or Alaska Native Participants"].append(ethnic_participants["American Indian or Alaska Native"])
        synthetic_data["Number of White Participants"].append(ethnic_participants["White"])
        synthetic_data["Number of Black/African American Participants"].append(ethnic_participants["Black/African American"])
        synthetic_data["Middle Eastern or North African"].append(ethnic_participants["Middle Eastern or North African"])
        synthetic_data["Number of Hispanic or Latino Participants"].append(ethnic_participants["Hispanic or Latino"])
        synthetic_data["Number of Multiracial Participants"].append(ethnic_participants["Multiracial"])
        
        synthetic_data["Notes and Additional Information"].append("No additional notes" if random.random() < 0.8 else "Special remarks")

    return pd.DataFrame(synthetic_data)

synthetic_event_data = generate_synthetic_data(100)

print(synthetic_event_data.head())

synthetic_event_data.to_csv('synthetic_event_data.csv', index=False)
