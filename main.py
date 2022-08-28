import csv #For opening and processing csv files
import sys #For testing with single zipcodes

all_silver_plans = [] 
defined_rate_areas = set() 
zip_codes_rate_areas_relation = {}

def get_all_silver_plans():
    """
    This function opens a CSV file,
    gets all data with only silver as its metal level and state and rate areas.
    """
    with open('plans.csv', newline='') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['metal_level'] == 'Silver':
                all_silver_plans.append({
                    'id': row['plan_id'],
                    'rate_area': (row['state'], row['rate_area']),
                    'rate': row['rate'],
                })
                defined_rate_areas.add((row['state'], row['rate_area']))

def get_all_zipcodes_rate_areas():
    """
    This function opens a CSV file,
    Gets data relating zipcode with state and rate area
    """
    with open('zips.csv', newline='') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['zipcode'] not in zip_codes_rate_areas_relation.keys():
                zip_codes_rate_areas_relation[row['zipcode']] = set()
            zip_codes_rate_areas_relation[row['zipcode']].add((row['state'], row['rate_area']))

def get_silver_plans_by_rate_area(rate_area):
    """
    This function is for returning silver planes for the specified rate areas.
    """
    return [silver_plan for silver_plan in all_silver_plans if silver_plan['rate_area'] == rate_area]

def get_slcsp(rates):
    """
    This is the function were the slcsp is calculated and formated from the specified rates.
    """
    return '{0:.2f}'.format(float(sorted(rates)[1]))

def get_rate(zipcode):
    rate_areas = zip_codes_rate_areas_relation[zipcode]
    if len(rate_areas) != 1:    #If there is no rate areas for that zipcode we return NULL
        return ''

    rate_area = list(rate_areas)[0]
    if rate_area not in defined_rate_areas: #If the current rate area is not found in defined rate areas we return NULL
        return ''

    silver_plans_for_rate_area = get_silver_plans_by_rate_area(rate_area)

    rates = set(map(lambda plan: plan['rate'], silver_plans_for_rate_area)) #Lambda function that returns a set of rates in the specified range.

    if len(rates) > 1: 
        return get_slcsp(rates)
    else:   #If we couldn't find more than 1 rate we retun NULL since we need atleast 2 rates to calculate slcsp.
        return ''


def print_slcsp():
    """
    This function is for opening CSV,
    Processing and printing the standard output.
    """
    with open('slcsp.csv', newline='') as file:
        csv_reader = csv.DictReader(file)
        print('zipcode,rate')
        for row in csv_reader:
            print(f"{row['zipcode']},{get_rate(row['zipcode'])}")

if __name__ == "__main__":
    get_all_silver_plans()
    get_all_zipcodes_rate_areas()
    if len(sys.argv) > 1:       #Checking for extra command line arguments for applying testcases.
        zipcode = sys.argv[1]
        print('zipcode,rate')
        print(f"{zipcode},{get_rate(zipcode)}")
    else:
        print_slcsp()
    