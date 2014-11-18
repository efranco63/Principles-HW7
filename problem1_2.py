import sys
import pandas as pd
import scipy as sp
import numpy as np
import matplotlib.pyplot as plt

def main(filename,k):
    k = int(k)
    three11 = pd.read_csv(filename,dtype=unicode)
    heads = ['Agency','Agency Name']
    three11 = three11[heads]

    # group by agency
    agencies = three11.groupby('Agency').aggregate('count').sort('Agency Name',ascending=False)
    agencies_list = agencies.index.tolist()
    agencies_counts = agencies['Agency Name'].tolist()

    agencies[:k].plot(kind='bar',legend=False,color=('DodgerBlue','Orange','Green','0.7'),rot=45,title='Top '+str(k)+ ' Agencies by Volume')
    plt.xlabel('Agency')
    plt.ylabel('Volume')

    plt.show()

if __name__ == "__main__":
    filename = sys.argv[1]
    k = sys.argv[2]
    main(filename,k)
