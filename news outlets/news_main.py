# import warnings
# warnings.filterwarnings("ignore")

# k_list = ['beyond meat']
# Soy/pea/chickpea protein, 

from news_utls import *
import os
import warnings
import time
warnings.filterwarnings("ignore")
# k_list = "beyond meat".lower().split(', ')
k_list = "beyond meat, gene editing, vertical farm, phage therapy, mRNA vaccine, pfizer, moderna, novavax, editas, astrazeneca, alta, Intense pulsed light, plazma process, Bitter blocker, Phage encapsulation, Gut Microbiome, Translucent egg, Tenebrio molitor, Polyhydroxyalkanoate".lower().split(', ')
scraper_appender(5, k_list)

# os.system('Simple_Dash.py')
time.sleep(10000)




# from news_utls import *
# NewsUtls("beyond meat").get_data(5, 'BBC')