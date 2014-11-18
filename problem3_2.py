import sys
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import csv

def main(filename,filename2):
    with open(filename) as f:
        data = csv.DictReader(f)
        zips = []
        Agents = []
        A_list = ['NYPD','DOT','DOB','TLC','DPR']
        #iterate through each row of the dataframe
        for line in data:
            # if the agency is one of the ones we are interested in
            if line['Agency'] in A_list:
                zipcode = line['Incident Zip']
                agent = line['Agency']
                # if the zipcode has a '-' in it, keep the digits preceding it
                if '-' in zipcode:
                    x = zipcode.index('-')
                    zipcode = zipcode[:x]
                # if the zipcode is a set of numbers, add the zip and its agency to their lists
                if zipcode.isdigit():
                    zips.append(int(zipcode))
                    Agents.append(agent)

    #create a data frame from the zip codes and agencies
    zips_df = pd.DataFrame()
    zips_df['zips'] = zips
    zips_df['agency'] = Agents
    zips_df['counts'] = 1

    # get counts of agencies by zipcode, counts column is a dummy that holds the counts
    zipgroups = zips_df.groupby(['zips','agency']).aggregate(sum)
    test = zipgroups.unstack().fillna(0)
    A_list = ['DOB','DOT','DPR','NYPD','TLC']

    zip_list = []
    count_list = []
    agent_list = []

    # for the unstacked counts of agencies by zipcode, append the highest count to
    # a list along with the zipcode and agency to their corresponding lists
    for i in test.iterrows():
        index,data = i
        x = data.tolist()
        #append the zip code
        zip_list.append(index)
        #append the total count count
        count_list.append(sum(x))
        #append the agency corresponding to max count
        agent_list.append(A_list[x.index(max(x))])

    # create a data frame from the 3 lists created in the previous step
    df = pd.DataFrame()
    df['zips'] = zip_list
    df['counts'] = count_list
    df['agencies'] = agent_list

    #make the zipcodes the indices of the data frame to later join with other zip code df
    df = df.set_index('zips')

    zip_pop = pd.read_csv(filename2)

    zip_pop = zip_pop.set_index('Zip Code ZCTA').astype(int)
    # join by indices
    df = df.join(zip_pop)

    df = df[pd.notnull(df['2010 Census Population'])]

    # create objects for each series plotted, each series corresponding to an agency
    temp_df = df[df['agencies']=='DOB']
    DOB = plt.scatter(temp_df['2010 Census Population'], temp_df['counts'], color='Red')
    temp_df = df[df['agencies']=='DOT']
    DOT = plt.scatter(temp_df['2010 Census Population'], temp_df['counts'], color='DarkOrange')
    temp_df = df[df['agencies']=='DPR']
    DPR = plt.scatter(temp_df['2010 Census Population'], temp_df['counts'], color='Blue')
    temp_df = df[df['agencies']=='NYPD']
    NYPD = plt.scatter(temp_df['2010 Census Population'], temp_df['counts'], color='Green')
    temp_df = df[df['agencies']=='TLC']
    TLC = plt.scatter(temp_df['2010 Census Population'], temp_df['counts'], color='BlueViolet')

    plt.legend((DOB,DOT,DPR,NYPD,TLC),
               ('DOB', 'DOT', 'DPR', 'NYPD', 'TLC'),
               ncol=2,
               scatterpoints=1,
               fontsize=10,
               loc='upper left')

    plt.title('Number of Complaints by Population by Zip Code (Color indicates Agency with highest volume)')
    plt.ylabel('Number of Complaints')
    plt.xlabel('Population')
    plt.xlim(-5000,)
    plt.ylim(-90,)
    plt.show()

if __name__ == "__main__":
    filename = sys.argv[1]
    filename2 = sys.argv[2]
    main(filename,filename2)
