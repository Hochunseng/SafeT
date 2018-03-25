"""
Created by Apostolos Delis on 12/18/17.
Copyright © 2017 Apostolos Delis. All rights reserved.
"""
import requests
import errno
import os
import pandas as pd
import datetime
import math


class TimeString:

    def __init__(self, year, month, day):
        self.year = int(year)
        self.month = int(month)
        self.day = int(day)

    def __repr__(self):
        return str(self.month) + "/" + str(self.day) + "/" + str(self.year)

    def day(self):
        return self.day

    def month(self):
        return self.month

    def year(self):
        return self.year

    def __str__(self):
        return str(self.month) + "/" + str(self.day) + "/" + str(self.year)


class CrimeDataGenerator:
    """
    :var crime_simplification_map: dictionary that converts the crime categories to a more condensed and simplified list
    :var new_crime_categories: The new categories the the original crime labels will be mapped to
    """
    new_crime_categories = {"ASSAULT", "THEFT", "MISC", "VANDALISM", "SEXUAL CRIME",
                            "CHILD ABUSE", "FRAUD/SCAM", "DANGEROUS/VIOLENT ACTION"}

    crime_simplification_map = {

        "INTIMATE PARTNER - SIMPLE ASSAULT": "ASSAULT",
        "VEHICLE - STOLEN": "THEFT",
        "EMBEZZLEMENT, GRAND THEFT ($950.01 & OVER)": "THEFT",
        "THEFT PLAIN - PETTY ($950 & UNDER)": "THEFT",
        "SHOPLIFTING - PETTY THEFT ($950 & UNDER)": "THEFT",
        "BATTERY - SIMPLE ASSAULT": "THEFT",
        "OTHER MISCELLANEOUS CRIME": "MISC",
        "BURGLARY": "THEFT",
        "BURGLARY FROM VEHICLE": "THEFT",
        "VANDALISM - MISDEAMEANOR ($399 OR UNDER)": "VANDALISM",
        "EMBEZZLEMENT, PETTY THEFT ($950 & UNDER)": "THEFT",
        "BIKE - STOLEN": "THEFT",
        "ROBBERY": "THEFT",
        "SODOMY/SEXUAL CONTACT B/W PENIS OF ONE PERS TO ANUS OTH 0007=02": "SEXUAL CRIME",
        "THEFT-GRAND ($950.01 & OVER)EXCPT,GUNS,FOWL,LIVESTK,PROD0036": "THEFT",
        "ASSAULT WITH DEADLY WEAPON, AGGRAVATED ASSAULT": "ASSAULT",
        "OTHER ASSAULT": "ASSAULT",
        "CHILD ABUSE (PHYSICAL) - SIMPLE ASSAULT": "CHILD ABUSE",
        "INDECENT EXPOSURE": "SEXUAL CRIME",
        "SHOPLIFTING-GRAND THEFT ($950.01 & OVER)": "THEFT",
        "BATTERY WITH SEXUAL CONTACT": "SEXUAL CRIME",
        "VANDALISM - FELONY ($400 & OVER, ALL CHURCH VANDALISMS) 0114": "VANDALISM",
        "CRM AGNST CHLD (13 OR UNDER) (14-15 & SUSP 10 YRS OLDER)0060": "CHILD ABUSE",
        "LETTERS, LEWD": "SEXUAL CRIME",
        "RAPE, ATTEMPTED": "SEXUAL CRIME",
        "BURGLARY FROM VEHICLE, ATTEMPTED": "THEFT",
        "BIKE - ATTEMPTED STOLEN": "THEFT",
        "SEX, UNLAWFUL": "SEXUAL CRIME",
        "PEEPING TOM": "SEXUAL CRIME",
        "THEFT FROM PERSON - ATTEMPT": "THEFT",
        "PICKPOCKET": "THEFT",
        "ORAL COPULATION": "SEXUAL CRIME",
        "DISHONEST EMPLOYEE - PETTY THEFT": "THEFT",
        "CHILD ABUSE (PHYSICAL) - AGGRAVATED ASSAULT": "CHILD ABUSE",
        "BEASTIALITY, CRIME AGAINST NATURE SEXUAL ASSLT WITH ANIM0065": "SEXUAL CRIME",
        "VEHICLE - ATTEMPT STOLEN": "THEFT",
        "PIMPING": "SEXUAL CRIME",
        "ASSAULT WITH DEADLY WEAPON ON POLICE OFFICER": "ASSAULT",
        "SHOPLIFTING - ATTEMPT": "THEFT",
        "LEWD CONDUCT": "SEXUAL CRIME",
        "THEFT, COIN MACHINE - PETTY ($950 & UNDER)": "THEFT",
        "BATTERY ON A FIREFIGHTER": "ASSAULT",
        "BURGLARY, ATTEMPTED": "THEFT",
        "THEFT FROM MOTOR VEHICLE - PETTY ($950 & UNDER)": "THEFT",
        "DISHONEST EMPLOYEE - GRAND THEFT": "THEFT",
        "BUNCO, PETTY THEFT": "FRAUD/SCAM",
        "BUNCO, GRAND THEFT": "FRAUD/SCAM",
        "COUNTERFEIT": "FRAUD/SCAM",
        "DOCUMENT FORGERY / STOLEN FELONY": "FRAUD/SCAM",
        "ATTEMPTED ROBBERY": "THEFT",
        "CONTRIBUTING": "MISC",
        "CHILD ANNOYING (17YRS & UNDER)": "CHILD ABUSE",
        "CHILD STEALING": "CHILD ABUSE",
        "DOCUMENT WORTHLESS ($200.01 & OVER)": "FRAUD/SCAM",
        "ABORTION/ILLEGAL": "SEXUAL CRIME",
        "DEFRAUDING INNKEEPER/THEFT OF SERVICES, OVER $400": "FRAUD/SCAM",
        "PURSE SNATCHING - ATTEMPT": "THEFT",
        "CHILD NEGLECT (SEE 300 W.I.C.)": "CHILD ABUSE",
        "THEFT, PERSON": "THEFT",
        "DEFRAUDING INNKEEPER/THEFT OF SERVICES, $400 & UNDER": "FRAUD/SCAM",
        "RAPE, FORCIBLE": "SEXUAL CRIME",
        "THEFT PLAIN - ATTEMPT": "THEFT",
        "PURSE SNATCHING": "THEFT",
        "CREDIT CARDS, FRAUD USE ($950.01 & OVER)": "FRAUD/SCAM",
        "THEFT FROM MOTOR VEHICLE - ATTEMPT": "THEFT",
        "PICKPOCKET, ATTEMPT": "THEFT",
        "BRIBERY": "FRAUD/SCAM",
        "BUNCO, ATTEMPT": "FRAUD/SCAM",
        "CREDIT CARDS, FRAUD USE ($950 & UNDER": "FRAUD/SCAM",
        "CRIMINAL HOMICIDE": "ASSAULT",
        "STALKING": "DANGEROUS/VIOLENT ACTION",
        "EXTORTION": "MISC",
        "SEXUAL PENETRATION WITH A FOREIGN OBJECT": "SEXUAL CRIME",
        "THEFT OF IDENTITY": "FRAUD/SCAM",
        "ARSON": "DANGEROUS/VIOLENT ACTION",
        "VIOLATION OF RESTRAINING ORDER": "DANGEROUS/VIOLENT ACTION",
        "INTIMATE PARTNER - AGGRAVATED ASSAULT": "ASSAULT",
        "DISTURBING THE PEACE": "DANGEROUS/VIOLENT ACTION",
        "THEFT FROM MOTOR VEHICLE - GRAND ($400 AND OVER)": "DANGEROUS/VIOLENT ACTION",
        "SHOTS FIRED AT INHABITED DWELLING": "DANGEROUS/VIOLENT ACTION",
        "BOMB SCARE": "DANGEROUS/VIOLENT ACTION",
        "BRANDISH WEAPON": "DANGEROUS/VIOLENT ACTION",
        "ILLEGAL DUMPING": "MISC",
        "CRUELTY TO ANIMALS": "DANGEROUS/VIOLENT ACTION",
        "VIOLATION OF COURT ORDER": "DANGEROUS/VIOLENT ACTION",
        "FALSE IMPRISONMENT": "MISC",
        "PROWLER": "MISC",
        "UNAUTHORIZED COMPUTER ACCESS": "MISC",
        "DRUNK ROLL": "MISC",
        "BATTERY POLICE (SIMPLE)": "ASSAULT",
        "RECKLESS DRIVING": "DANGEROUS/VIOLENT ACTION",
        "KIDNAPPING": "DANGEROUS/VIOLENT ACTION",
        "THREATENING PHONE CALLS/LETTERS": "DANGEROUS/VIOLENT ACTION",
        "DISCHARGE FIREARMS/SHOTS FIRED": "DANGEROUS/VIOLENT ACTION",
        "DRIVING WITHOUT OWNER CONSENT (DWOC)": "MISC",
        "WEAPONS POSSESSION/BOMBING": "DANGEROUS/VIOLENT ACTION",
        "FAILURE TO YIELD": "DANGEROUS/VIOLENT ACTION",
        "VIOLATION OF TEMPORARY RESTRAINING ORDER": "DANGEROUS/VIOLENT ACTION",
        "KIDNAPPING - GRAND ATTEMPT": "DANGEROUS/VIOLENT ACTION",
        "CRIMINAL THREATS - NO WEAPON DISPLAYED": "DANGEROUS/VIOLENT ACTION",
        "THROWING OBJECT AT MOVING VEHICLE": "DANGEROUS/VIOLENT ACTION",
        "RESISTING ARREST": "DANGEROUS/VIOLENT ACTION",
        "TRESPASSING": "DANGEROUS/VIOLENT ACTION",
        "FALSE POLICE REPORT": "MISC",
        "LYNCHING": "DANGEROUS/VIOLENT ACTION",
        "THEFT, COIN MACHINE - ATTEMPT": "THEFT",
        "DISRUPT SCHOOL": "CHILD ABUSE",
        "PETTY THEFT - AUTO REPAIR": "THEFT",
        "SEXUAL PENETRATION W/FOREIGN OBJECT": "SEXUAL CRIME",
        "FAILURE TO DISPERSE": "DANGEROUS/VIOLENT ACTION",
        "GRAND THEFT / INSURANCE FRAUD": "FRAUD/SCAM",
        "CHILD ABANDONMENT": "CHILD ABUSE",
        "MANSLAUGHTER, NEGLIGENT": "ASSAULT",
        "DRUNK ROLL - ATTEMPT": "MISC",
        "GRAND THEFT / AUTO REPAIR": "THEFT",
        "FIREARMS RESTRAINING ORDER (FIREARMS RO)": "DANGEROUS/VIOLENT ACTION",
        "CONSPIRACY": "MISC",
        "THEFT, COIN MACHINE - GRAND ($950.01 & OVER)": "THEFT",
        "TILL TAP - ATTEMPT": "FRAUD/SCAM",
        "INCITING A RIOT": "DANGEROUS/VIOLENT ACTION",
        "BOAT - STOLEN": "THEFT",
        "INCEST (SEXUAL ACTS BETWEEN BLOOD RELATIVES)": "SEXUAL CRIME",
        "PANDERING": "MISC",
        "CONTEMPT OF COURT": "MISC",
        "REPLICA FIREARMS(SALE,DISPLAY,MANUFACTURE OR DISTRIBUTE)0132": "FRAUD/SCAM",
        "DOCUMENT WORTHLESS ($200 & UNDER)": "FRAUD/SCAM",
        "TILL TAP - GRAND THEFT ($950.01 & OVER)": "FRAUD/SCAM",
        "DISHONEST EMPLOYEE ATTEMPTED THEFT": "THEFT",
        "BLOCKING DOOR INDUCTION CENTER": "DANGEROUS/VIOLENT ACTION",
        "TRAIN WRECKING": "DANGEROUS/VIOLENT ACTION",
        "TILL TAP - PETTY ($950 & UNDER)": "FRAUD/SCAM",
        "BIGAMY": "SEXUAL CRIME",
        "SHOTS FIRED AT MOVING VEHICLE, TRAIN OR AIRCRAFT": "DANGEROUS/VIOLENT ACTION",
        None: "MISC",
        "TELEPHONE PROPERTY - DAMAGE": "DANGEROUS/VIOLENT ACTION",
        "DRUGS, TO A MINOR": "CHILD ABUSE",
        "LYNCHING - ATTEMPTED": "ASSAULT",
        "SEXUAL PENTRATION WITH A FOREIGN OBJECT": "SEXUAL CRIME"
        
    }

    def __init__(self, url, directory):
        self.json_url = url  # the url where the data is pulled from
        self.data_uncleaned = {}  # Dictionary that will store data points from the json
        self.data = {}  # what will actually get used (cleaned data)
        self.directory = directory  # The directory that will store all the json files
        self.num_json_files = 0  # How many json files are currently created from the database
        CrimeDataGenerator.make_directory(self.directory)  # In case the directory assigned doesn't exist yet

    def data(self)->dict:
        """Return a dictionary with values of lists {1:[], 2:[],...}"""
        return self.data

    def get_data_from_json(self)->dict:
        """
        :return: list of data points where each data point is a nested list of its attributes
        """
        r = requests.get(self.json_url)
        print("Importing complete, beginning to parse the data...")
        self.data_uncleaned = r.json()["data"]
        return self.data_uncleaned

    def category_completetion(self, verbose=False)->bool:
        """
        Function that first tests to see if all the crime categories in the map are valid
        and then tests to see if all the categories from the data are accounted for in the dictionary map
        :param verbose: Will print to the user about each test case if true
        :return: true if there are no failed test cases, false, otherwise
        """
        failures = {"first": [], "second": []}

        """First Test: check to see that all the crime_simplification_map values are from new_crime_categories"""
        for category in CrimeDataGenerator.crime_simplification_map.keys():

            if CrimeDataGenerator.crime_simplification_map[category] in CrimeDataGenerator.new_crime_categories:
                if verbose:
                    print(category, "Test case passed")
            else:
                if verbose:
                    print("ERROR: TEST CASE:", category, "FAILED")

                failures["first"].append(category)

        # Make sure that the data has been generated
        if self.data == {}:
            self.get_data_from_json()

        df = pd.DataFrame(self.data)

        """Second Test: Test to see if all the data categories from the json are accounted for in the map"""
        for category in df.loc[2].unique():
            if category in CrimeDataGenerator.crime_simplification_map.keys():
                print(category, "Test case passed")
            else:
                print(category, "FAILED")
                failures["second"].append(category)

        if verbose:
            print("Errors in:", failures)

        return failures["first"] == [] and failures["second"] == []

    def generate_cleaned_json_files(self, mapping=True, verbose=False):
        """
        Generates a new json file inside the directory given at the constructor for every 20000 lines of data
        :param mapping: if the categories from the json url should be mapped to the simplified list
        :param verbose: if the user should be notified at the completion of each data point
        """

        file = open(os.path.join(self.directory, "json_0.json"), 'w+')
        error_file = open(os.path.join(self.directory, "errors.json"), "w+")  # Error File Keeps track of bad data
        error_file.write("[\n")

        self.get_data_from_json()
        indexes = range(len(self.data_uncleaned))

        for i in indexes:

            # In order to avoid having txt files that are too big, create a new file every 20000 data points
            if i % 20000 == 0:
                file.write("}")
                file.close()
                file_name = "json_" + str(int(i / 20000)) + ".json"
                file = open(os.path.join(json_directory, file_name), 'w+')
                file.write("{\n")

            current_data_point = self.data_uncleaned[i]
            self.data[i] = current_data_point

            # Store the longitude and latitude and category of each data point
            if current_data_point[33][1] is not None and current_data_point[33][2] is not None:
                file.write("\t\"" + str(i))
                file.write("\": [\"")
                file.write(str(float(current_data_point[33][1])))
                file.write("\", \"")
                file.write(str(float(current_data_point[33][2])))
                file.write("\", \"")
                if mapping:  # and self.category_completetion()
                    file.write(CrimeDataGenerator.crime_simplification_map[current_data_point[16]])
                else:
                    file.write(str(current_data_point[16]))
                file.write("\"],\n")

                if verbose:
                    print("data point ", i, "processed")
            else:
                error_file.write(str(i) + ",\n")

        error_file.write("]")
        error_file.close()

    def generate_recent_data(self, current_date=datetime.datetime.now(), timeframe="week", mapping=True, verbose=False):
        """
        Allows user to only collect  crime data within a certain timeframe
        :param current_date: The date that you want to base the last
        :param mapping: if the categories from the json url should be mapped to the simplified list
        :param timeframe: how far back you want to pull data from
        potential data time-frames: = {"day", "week", "month", "year"}
        :param verbose: if the user should be notified at the completion of each data point
        """

        time_frames = {"week", "month", "year", "day"}
        if timeframe not in time_frames:
            print("incorrect time frame, needs to be one of the following:")
            print(time_frames)
            exit(1)

        file = open(os.path.join(self.directory, "recent_data_0.json"), 'w+')

        self.get_data_from_json()
        indexes = range(len(self.data_uncleaned))

        num_data_points = 0

        create_new_file = True
        for i in indexes:

            # In order to avoid having txt files that are too big, create a new file every 20000 data points
            if num_data_points % 20000 == 0 and create_new_file:
                file.write("}")
                file.close()
                file_name = "recent_data_" + str(int(num_data_points / 20000)) + ".json"
                file = open(os.path.join(json_directory, file_name), 'w+')
                file.write("{\n")
                create_new_file = False

            current_data_point = self.data_uncleaned[i]
            self.data[i] = current_data_point

            # Store the longitude and latitude and category of each data point
            if current_data_point[33][1] is not None and current_data_point[33][2] is not None and \
                    CrimeDataGenerator.in_correct_time_frame(datapoint=current_data_point, timeframe=timeframe,
                                                             current_date=current_date):
                file.write("\t\"" + str(num_data_points))
                file.write("\": [\"")
                file.write(str(float(current_data_point[33][1])))
                file.write("\", \"")
                file.write(str(float(current_data_point[33][2])))
                file.write("\", \"")
                if mapping:  # and self.category_completetion()
                    file.write(CrimeDataGenerator.crime_simplification_map[current_data_point[16]])
                else:
                    file.write(str(current_data_point[16]))
                file.write("\", \"")
                file.write(CrimeDataGenerator.get_crime_time(current_data_point).__str__())
                file.write("\"],\n")
                num_data_points += 1
                create_new_file = True

                if verbose:
                    print("data point: ", num_data_points, "found at index", i)

    def generate_geojson(self, current_date=datetime.datetime.now(), timeframe="week", mapping=True, verbose=False):
        """
        Creates geojson files instead of regular json files (used for the mapbox)
        :param current_date: The date that you want to base the last
        :param mapping: if the categories from the json url should be mapped to the simplified list
        :param timeframe: how far back you want to pull data from
        potential data time-frames: = {"week", "month", "year", "all"}
        :param verbose: if the user should be notified at the completion of each data point
        """
        time_frames = {"week", "month", "all", "year", "day"}
        if timeframe not in time_frames:
            print("incorrect time frame, needs to be one of the following:")
            print(time_frames)
            exit(1)

        file = open(os.path.join(self.directory, "geodata_" + timeframe + "_0.geojson"), 'w+')

        self.get_data_from_json()
        indexes = range(len(self.data_uncleaned))

        num_data_points = 0

        create_new_file = True
        for i in indexes:

            # In order to avoid having txt files that are too big, create a new file every 20000 data points
            if num_data_points % 20000 == 0 and create_new_file:

                file.write("  ]\n")
                file.write("}\n")
                file.close()

                file_name = "geodata_" + timeframe + '_' + str(int(num_data_points / 20000)) + ".geojson"
                file = open(os.path.join(json_directory, file_name), 'w+')

                file.write("{\n")
                file.write("  \"type\": \"FeatureCollection\",\n")
                file.write("  \"features\": [\n")

                create_new_file = False

            current_data_point = self.data_uncleaned[i]
            self.data[i] = current_data_point

            # Store the longitude and latitude and category of each data point
            if current_data_point[33][1] is not None and current_data_point[33][2] is not None and \
                    CrimeDataGenerator.in_correct_time_frame(datapoint=current_data_point, timeframe=timeframe,
                                                             current_date=current_date):
                file.write("    {\n")
                file.write("      \"type\": \"Feature\",\n")
                file.write("      \"properties\": {\n")
                file.write("        \"id\": " + str(num_data_points) + ",\n")
                file.write("        \"marker-color\": \"" + CrimeDataGenerator.set_marker_color(current_data_point) + "\",\n")
                file.write("        \"marker-symbol\": \"" + CrimeDataGenerator.set_marker_symbol(current_data_point) + "\",\n")
                file.write("        \"time\": \"")
                file.write(CrimeDataGenerator.get_crime_time(current_data_point).__str__() + "\",\n")
                file.write("        \"title\": \"" + current_data_point[16] + "\",\n")
                file.write("        \"category\": \"")

                if mapping:  # and self.category_completetion()
                    file.write(CrimeDataGenerator.crime_simplification_map[current_data_point[16]] + "\",\n")
                else:
                    file.write(str(current_data_point[16]) + "\",\n")

                file.write("        \"description\": \"" + CrimeDataGenerator.set_marker_description(current_data_point) + "\"\n")
                file.write("      },\n")
                file.write("      \"geometry\": {\n")
                file.write("        \"type\": \"Point\",\n")
                file.write("        \"coordinates\": [\n")
                file.write("          " + str(float(current_data_point[33][2])) + ",\n")
                file.write("          " + str(float(current_data_point[33][1])) + "\n")
                file.write("        ]\n")
                file.write("      }\n")
                file.write("    },\n")

                num_data_points += 1
                create_new_file = True  # prevent the index 0 from overwriting a lot of files before finding data

                if verbose:
                    print("data point:", num_data_points, "found at index", i)

        file.write("  ]\n")
        file.write("}\n")
        file.close()

    def coordinates_file(self, current_date=datetime.datetime.now(), timeframe="week"):
        """
        Creates a txt file that contains a list of tuples that are the coordinates of where crimes occurred
        """

        time_frames = {"week", "month", "all", "year", "day"}
        if timeframe not in time_frames:
            print("incorrect time frame, needs to be one of the following:")
            print(time_frames)
            exit(1)

        file = open(os.path.join(self.directory, "coordinates.txt"), 'w+')
        file.write("data = [\n")
        if self.data_uncleaned == {}:
            self.get_data_from_json()

        for current_data_point in self.data_uncleaned:

            if current_data_point[33][1] is not None and current_data_point[33][2] is not None and \
                    CrimeDataGenerator.in_correct_time_frame(datapoint=current_data_point, timeframe=timeframe,
                                                             current_date=current_date):

                    file.write("\t(" + str(current_data_point[33][2]) + ", " + str(current_data_point[33][1]) + "),\n")

        file.write("]")
        file.close()

    @staticmethod
    def set_marker_color(datapoint):
        """
        :param datapoint: the datapoint that we want to set the color for
        :return: the hex color for the marker on the map (based on how dangerous
        and short-term traffic increasing a crime is)
        """
        color_dictionary = {

            "ASSAULT": "#581845",
            "THEFT": "#C70039",
            "MISC": "#FFC300",
            "VANDALISM": "#FF5733",
            "SEXUAL CRIME": "#CD5C5C",
            "CHILD ABUSE": "#F08080",
            "FRAUD/SCAM": "#FFC300",
            "DANGEROUS/VIOLENT ACTION": "#922B21",

        }

        return color_dictionary[CrimeDataGenerator.crime_simplification_map[datapoint[16]]]

    @staticmethod
    def set_marker_symbol(datapoint)->str:
        """
        :param datapoint: datapoint that will get a marker symbol
        :return: a str with a one of the symbols that are supported (primarily maki icons)
        source for maki icons: https://www.mapbox.com/maki-icons/
        """
        symbol_dictionary = {

            "ASSAULT": "baseball",
            "THEFT": "museum",
            "MISC": "u",
            "VANDALISM": "fire-station",
            "SEXUAL CRIME": "lodging",
            "CHILD ABUSE": "playground",
            "FRAUD/SCAM": "bank",
            "DANGEROUS/VIOLENT ACTION": "danger"

        }

        return symbol_dictionary[CrimeDataGenerator.crime_simplification_map[datapoint[16]]]

    @staticmethod
    def set_marker_description(datapoint)->str:
        """
        sets the description of each crime
        :param datapoint: the crime that will be described
        :return: the description as a str
        """

        description = "Status: " + datapoint[26] + " Location: " + str(datapoint[13])
        return description


    @staticmethod
    def get_crime_time(datapoint):
        """
        :param datapoint: datapoint you want the date from
        :return: returns a TimeString object with a year, month, and time
        """
        return TimeString(year=datapoint[9].split('-')[0], month=datapoint[9].split('-')[1],
                          day=datapoint[9].split('-')[2].split('T')[0])

    @staticmethod
    def in_correct_time_frame(datapoint: list, timeframe: str, current_date=datetime.datetime.now())->bool:
        """
        :param datapoint: datapoint you want to check if in the valid region
        :param timeframe: whether you want to check if it is same month, day, all, or year
        :param current_date: the current date (or whatever you want to set as the date relative to the data)
        :return: true or false if the data-point occurred within the time-frame of the current date
        """
        time = CrimeDataGenerator.get_crime_time(datapoint)
        if timeframe == "all":
            return True

        elif timeframe == "day":
            return time.year == current_date.year and time.month == current_date.month and time.day == current_date.day

        elif timeframe == "week":
            return time.year == current_date.year and time.month == current_date.month and math.fabs(time.day - current_date.day) <= 7

        elif timeframe == "month":
            return time.year == current_date.year and time.month == current_date.month

        else:
            return time.year == current_date.year

    @staticmethod
    def make_directory(file_path):
        """
        Creates the directory at the path:
        :param file_path: the path of the directory that you want ot create
        """
        try:
            os.makedirs(file_path, exist_ok=True)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(file_path):
                pass
            else:
                print("Error while attempting to create a directory.")
                exit(3)


if __name__ == "__main__":

    # Define directories
    base_directory = "..."
    json_directory = ".../json_files"
    json_url = "https://data.lacity.org/api/views/y8tr-7khq/rows.json?accessType=DOWNLOAD"

    crime_data_generator = CrimeDataGenerator(json_url, json_directory)
    # crime_data_generator.generate_cleaned_json_files(mapping=True, verbose=True)
    crime_data_generator.generate_geojson(timeframe="day", mapping=True, verbose=True,
                                         current_date=TimeString(2016, 10, 30))
    # crime_data_generator.coordinates_file(current_date=TimeString(2016, 10, 30), timeframe="day")
