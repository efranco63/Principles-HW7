import sys
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt


def main(filename):
    three11 = pd.read_csv(filename,dtype=unicode)

    agencies_list = ['NYPD','TLC','DPR']

    for agy in agencies_list:
        #create a dummy min date to filter out erroneous dates in the data
        min_date = datetime.strptime('05/20/2013 12:00:00 AM','%m/%d/%Y %I:%M:%S %p').date()

        #keep only the rows matching the agency desired
        df = three11[three11['Agency'] == agy]

        #reset indices in order to loop through them in sequential order
        df = df.reset_index()
        df = df.drop('index',1)
        #convert to datetime.date format
        for i in xrange(0,len(df['Created Date'])):
            if type( df['Created Date'][i]) == str:
                df['Created Date'][i] = datetime.strptime(df['Created Date'][i],'%m/%d/%Y %I:%M:%S %p').date()
        #keep values that are not null for created date
        df = df[pd.notnull(df['Created Date'])]
        #filter out erroneous dates out of range
        df = df[df['Created Date'] > min_date]
        #aggregate and count by created date
        df = df.groupby('Created Date').aggregate('count')

        #create lists with dates and counts
        df_dates = df.index.tolist()
        df_counts = df['Unique Key'].tolist()

        plt.plot(df_dates,df_counts)

    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.title('NYPD, TLC, DPR complaints over time')
    plt.legend(agencies_list,loc='upper left',ncol=3,fontsize=10)
    plt.ylim(0,1200)
    plt.xticks(rotation=45)
    plt.show()

if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
