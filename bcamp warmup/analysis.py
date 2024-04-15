import re
import pandas as pd
import matplotlib.pyplot as plt

def extract_years_experience(summary):
    years_pattern = r'(\d+)-(\d+) years? of experience|(\d+)\+? years? of experience'
    matches = re.findall(years_pattern, summary)
    if matches:
        years_list = [int(year) for match in matches for year in match if year != '']
        return sum(years_list) / len(years_list)
    else:
        return None

def extract_salary(summary):
    salary_pattern = r'\$?(\d+(?:,\d+)?)\s?(?:K|thousand|k|per annum|per year|per hour|/year|/hour)'
    matches = re.findall(salary_pattern, summary)
    if matches:
        salary_list = []
        for match in matches:
            if 'per hour' in summary or '/hour' in summary:
                hourly_salary = float(match.replace(',', ''))
                if hourly_salary != 0:
                    if hourly_salary < 100:
                        yearly_salary = hourly_salary * 40 * 52  # Assuming 40 hours per week and 52 weeks per year
                        salary_list.append(yearly_salary)
                    else:
                        salary_list.append(hourly_salary * 2080)  # Assuming 2080 hours per year
            elif float(match.replace(',', '')) != 0:
                salary_list.append(float(match.replace(',', '')))
        if salary_list:
            return sum(salary_list) / len(salary_list)
        else:
            return None
    else:
        return None

def calculate_relationship(job_summaries):
    x_values = []
    y_values = []
    for summary in job_summaries:
        years_experience = extract_years_experience(summary)
        salary = extract_salary(summary)
        if years_experience and salary:
            x_values.append(years_experience)
            y_values.append(salary)
    return x_values, y_values

# Assuming your CSV file is named 'postings.csv' and is in the same directory as your script
file_path = 'postings.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(file_path)

# Check if the 'job_summary' column exists in the DataFrame
if 'job_summary' not in df.columns:
    raise ValueError("The 'job_summary' column does not exist in the DataFrame.")

# Drop any rows where the 'job_summary' column contains NaN values
df.dropna(subset=['job_summary'], inplace=True)

# Call the function to calculate the relationship between years of experience and salary
x_values, y_values = calculate_relationship(df['job_summary'])

# Filter out points where the salary is less than 100
filtered_x_values = [x for x, y in zip(x_values, y_values) if y >= 500]
filtered_y_values = [y for y in y_values if y >= 500]

# Plot the filtered data
plt.scatter(filtered_x_values, filtered_y_values)
plt.xlabel('Years of Experience')
plt.ylabel('Salary')
plt.title('Relationship between Years of Experience and Salary')
plt.show()
