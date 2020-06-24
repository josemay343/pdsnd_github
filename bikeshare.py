import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Would you like to see data from Chicago, Washington, or New York?(not case sensitive) \n").lower()
        if city not in ('chicago', 'washington', 'new york'):
            print("\nPlease enter a valid city name. (not case sensitive)")
        else:
            break

    #selects the correct filter per what was passed by the user.
    while True:
        filter_choice = input('\nWould you like to filter by month, day, both, or none?(not case sensitive)\n').lower()
        if filter_choice not in('month','day','both','none'):
            print('\nPlease enter a valid option. (not case sensitive)')
        elif filter_choice == 'both':
            month = get_month()
            day = get_day()
            break
        elif filter_choice == 'month':
            month = get_month()
            day = 'all'
            break
        elif filter_choice == 'day':
            day = get_day()
            month = 'all'
            break
        elif filter_choice == 'none':
            month = 'all'
            day = 'all'
            break



    print('-'*40)
    return city, month, day

 #retreives the month from the user per a given filter, if none was selected as filter by user then this is skipped   
def get_month():
    while True:
        month = input("\nWhich Month? January, February, March, April, May, or June?(not case sensitive)\n").lower()
        if month not in ('all','january','february', 'march','april','may','june'):
            print("\nPlease enter a valid month name. (not case sensitive)")
        else:
            return month
            break

#retreives the day from the user per a given filter, if none was selected as filter by user then this is skipped  
def get_day():
    while True:
        day = input("\nWhich day of the week? Please type full day name or you can type 'all'.(not case sensitive)\n").lower()
        if day not in ('all','monday','tuesday','wednesday','thursday','friday','saturday','sunday'):
            print('\nPlease enter a valid day. (not case sensitive)')
        else:
            return day
            break

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day, hour of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'all':
        # filter by month in a new dataframe
        df = df[df['month'] == month.title()]
    
    # filter by day if applicable
    if day != 'all':
        #filer by day in a new dataframe
        df = df[df['day_of_week'] == day.title()]
    
        
    return df
def time_stats(df):
    print('-'*40)
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].value_counts().idxmax()
    count_month = df['month'].value_counts().max()
    print('The most common month per the given filters is: {}, Count: {}'.format(common_month,count_month))

    # display the most common day of week
    common_day = df['day_of_week'].value_counts().idxmax()
    count_day = df['day_of_week'].value_counts().max()
    print('The popular day per the given filters is: {}, Count: {}'.format(common_day, count_day))

    # display the most common start hour
    common_hour = df['hour'].value_counts().idxmax()
    count_hour = df['hour'].value_counts().max()
    print('The most common hour per the given filters is: {}, Count: {}\n'.format(common_hour,count_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    print('-'*40)
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].value_counts().idxmax()
    count_ss = df['Start Station'].value_counts().max()
    print('The most common start station per the given filters is: {}, Count: {}\n'.format(start_station,count_ss))

    # display most commonly used end station
    end_station = df['End Station'].value_counts().idxmax()
    count_es = df['End Station'].value_counts().max()
    print('The most common End Station per the given filters is: {}, Count: {}\n'.format(end_station,count_es))

    # display most frequent combination of start station and end station trip
    frequent_combination = df.groupby(['Start Station','End Station']).size().idxmax() #groupby() function researched from pandas.pydata.org
    count_fc = df.groupby(['Start Station', 'End Station']).size().max()
    print('The most frequent start and end station combination per the given filters is: \n{} - Count: {}\n'.format(frequent_combination,count_fc))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    print('-'*40)
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_traveltime = df['Trip Duration'].sum(skipna = True)
    print('The Total travel time for the given filters is: {}'.format(total_traveltime))

    # display mean travel time
    mean_traveltime = df['Trip Duration'].mean(skipna = True)
    print('The mean travel time for the given filters is: {}'.format(mean_traveltime))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    print('-'*40)
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The count of user types per the given filters is:\n \n{}'.format(user_types))

    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print('\nThe count of Gender per the given filters is:\n \n{}'.format(gender_count))
    except KeyError:
        print('\n***No gender data for Washington DC***')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year = int(df['Birth Year'].min())
        recent_year = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].value_counts().idxmax())
        count_common_year = df['Birth Year'].value_counts().max()
        print('\nThe earliest, most recent, and most common birth year per the given filters is:\n \nEarliest year: {}\nMost recent year: {}\nMost common year: {} - Count: {}'.format(earliest_year,recent_year,common_year,count_common_year))
    except KeyError:
        print('\n***No birth year data for Washington DC***')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def wait_user_input():
    """ Retreives the user input based on if the user wants to display the data one section a time or all at once"""
    while True:
        display_input = input('Would you like to display the data one section at a time? Please type Yes or No. (not case sensitive)\n').lower()
        if display_input not in ('yes','no'):
            print('Please enter only "yes" or "no"')
        elif display_input == 'yes':
            return display_input
            break
        elif display_input == 'no':
            return display_input
            break

def data_viewby(df):
    """ 
    Takes in the filtered data based on the user input and give the user the option
    to display the data one section at a time or all at once
    """
    function_list = [time_stats,station_stats,trip_duration_stats,user_stats] # created a list of the stats functions
    index = 0
    for function in function_list:
        response = wait_user_input()
        if response == 'yes':
            function_list[index](df) # if the response was 'yes' then shows the next available data set
            index += 1
        elif response == 'no': # if the response from user was 'no' from the start then all the data is shown at once.
            if index == 0:
                time_stats(df)
                station_stats(df)
                trip_duration_stats(df)
                user_stats(df)
                break
            elif index == 1: # if the response was 'no' at the second entry then it displays the remaining data sets.
                function_list[index](df)
                index += 1
                function_list[index](df)
                index += 1
                function_list[index](df)
                break
            elif index == 2: # if the response was 'no' at the third entry then it displays the remaining data sets.
                function_list[index](df)
                index += 1
                function_list[index](df)
                break
            elif index == 3: # if the resopnse was 'no' at the fourth entry then it displays the remaining data set.
                function_list[index](df)

def raw_data_view(df):
    """ Displays 5 lines of raw data based on the filters passed by the user"""
    count = 0
    start = 0
    end = 5
    while True:
        if count == 0:
            raw_data = input("\nWould you like to see 5 lines of the raw data based on the given filters? Please enter Yes or No.\n").lower()
            if raw_data not in ('yes','no'):
                print('Please enter yes or no only\n')
            elif raw_data == 'yes':
                count += 1
                print(df.iloc[start:end])
                start += 5
                end += 5 
            elif raw_data == 'no':
                break
        elif count == 1:
            raw_data_next = input("\nWould you like to see the next 5 lines of the raw data based on the given filters?. Please enter Yes or No.\n").lower()
            if raw_data_next not in ('yes','no'):
                print('Please enter yes or no only\n')
            elif raw_data_next == 'yes':
                print(df.iloc[start:end])
                start += 5
                end += 5
            elif raw_data_next == 'no':
                break

def basic_stats(df):
    while True:
        answer = input('Would you like to view general statistical data based on the given filters? Enter yes or no.\n')
        if answer not in ('yes','no'):
            print('Please enter yes or no.\n')
        elif answer == 'yes':
            print(df.describe())
            break
        elif answer == 'no':
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        data_viewby(df) # Provides the user an option to display the data by section or at all once.

        print('\nEnd of data\n')
        print('-'*40)
        
        basic_stats(df) # provides general statistics of the filtered data by the user
        raw_data_view(df) # Checks if the user would like to view the raw data in increments of 5 lines per request

        while True: # Check if the user would like to restart the script or not.
            restart = input('Would you like to restart the program? Enter yes or no.\n').lower()
            if restart not in ('yes', 'no'):
                print('\nPlease enter yes or no only')
            elif restart == 'yes':
                break
            elif restart == 'no':
                exit()
        

if __name__ == "__main__":
	main()