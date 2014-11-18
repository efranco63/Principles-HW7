import sys
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import csv

def main(filename,filename2):
    with open(filename) as f:
        data = csv.DictReader(f)
        zips = []
        for line in data:
            zipcode = line['Incident Zip']
            if '-' in zipcode: 
                x = zipcode.index('-')
                zipcode = zipcode[:x]
            if zipcode.isdigit():
                zips.append(zipcode)
            
    zips = pd.Series(zips).astype(int)
    zips = zips.value_counts()

    zips = pd.DataFrame(zips,columns=['Zip Code'])
        
    zip_pop = pd.read_csv(filename2)

    zip_pop = zip_pop.set_index('Zip Code ZCTA').astype(int)
    zips = zips.join(zip_pop)

    zips = zips[pd.notnull(zips['2010 Census Population'])]
        
    plt.scatter(zips['2010 Census Population'],zips['Zip Code'])
    plt.title('Number of Complaints by Population by Zip Code')
    plt.ylabel('Number of Complaints')
    plt.xlabel('Population')
    plt.xlim(-5000,)
    plt.ylim(-500,)
    plt.show()

if __name__ == "__main__":
    filename = sys.argv[1]
    filename2 = sys.argv[2]
    main(filename,filename2)
