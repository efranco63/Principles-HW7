import sys
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt


def main(filename,k):

    three11 = pd.read_csv(filename,dtype=unicode)
    k = int(k)

    #get a list of the top k agencies by volume
    heads = ['Agency','Agency Name']
    three11T = three11[heads]
    agencies = three11T.groupby('Agency').aggregate('count').sort('Agency Name',ascending=False)
    agencies_list = agencies.index.tolist()
    agencies_list = agencies_list[:k]

    for i in xrange(0,len(agencies_list)):
        df = three11[three11['Agency'] == agencies_list[i]]

        #create a dummy min date to filter out erroneous dates in the data
        min_date = datetime.strptime('05/20/2013 12:00:00 AM','%m/%d/%Y %I:%M:%S %p').time().hour

        #reset indices in order to loop through them in sequential order
        df = df.reset_index()
        df = df.drop('index',1)
        #convert to datetime.date format
        for i in xrange(0,len(df['Created Date'])):
            if type( df['Created Date'][i]) == str:
                df['Created Date'][i] = datetime.strptime(df['Created Date'][i],'%m/%d/%Y %I:%M:%S %p').time().hour
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
    plt.title('Top '+str(k)+' agency complaints by hour')
    plt.legend(agencies_list,loc='upper right',ncol=k/2,fontsize=10)
    # plt.ylim(0,max_count)
    plt.xticks(rotation=45)
    plt.show()

if __name__ == "__main__":
    filename = sys.argv[1]
    k = sys.argv[2]
    main(filename,k)
