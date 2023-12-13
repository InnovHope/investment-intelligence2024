#### About

# InnovHope Investment Intelligence

A state-of-the-art tool using the cutting-edge AI to support key decisions on strategic investments in emerging industries

## **Problem**
As a research VC consulting company, the primary goal is to provide the key recommendation for its parent company for strategic collaboration, investment, and/or acquisitions. However, with recently advancements in agriculture, food, biomedical field, many new emerging business fields changing frequently, such as `mRNA vaccine` and `vertical farm`. As a result, it becomes more challenge to conduct the research on these new fields in a timely fashion since overwhelming information has been flooded to the core research team. 

By utilizing different platform such as US Patent search portal and commercial company information platform, the research becomes even more labor-intensive job, which effects the timing of company’s strategic plan and the well-beings of employee for a long working hours. 

In addition, since there is no standard protocol for recommending candidate companies for investment, such recommendations would largely rely on the experience of people of the core research teams and as the employee leaves the company the knowledge of his/her for recommendation would be lost.
 
## **Solution**
Build a product utilizing the commerical data from `Crunchbase` with latest cloud technologies (`Amazon Web Services`) to search companies in a worldwide company candidate pool and to model the company successfulness using cutting edge machine learning algorithms.

#### Details
* Building a pipeline to bulk download, uncompress, parse, store, and prepare commerical data for ML with one click
* Training the ML model with one click in the backend
* Searching companies with terms of interest using NLP
* Visualizing results in an interactive dashboard
  * A geographic map plot of company locations
  * Summary statistics of time-related, funding-related, categorical features
  * Detailed information of the companies using dropdown selection from the search results

## **Data**
* Daily updated data from the `Crunchbase`
  * 17 csv files uncompressed from tar file
    * `acquisitions.csv`
    * `degrees.csv`
    * `funding_rounds.csv`
    * `investments.csv`
    * `jobs.csv`
    * `org_parents.csv`
    * `category_groups.csv`
    * `event_appearances.csv`
    * `funds.csv`
    * `investors.csv`
    * `organization_descriptions.csv`
    * `people.csv`
    * `events.csv`
    * `investment_partners.csv`
    * `ipos.csv`
    * `organizations.csv`
    * `people_descriptions.csv`
* Crunchbase Enterprise APIs for the informaiton of companies of interest
* Patent data from USPTO**
* News data from five major news outlets**

## **Tools and Techs**
* Python
* MySQL
* Data Cleaning + EDA
    * Jupyter
    * Pandas
    * Seaborn
    * Feature Engineering

* NLP + Modeling
    * Scikit-learn
    * spaCy
    * XGBoost
    
* Deployment
    * Flask
    * Dash
    * Geopy
    * uWSGI
    
## **Deployment**
The tool can be deployed with a debugging mode or a more production-ready mode using uwsgi. 
                 
For debugging mode:
```python
python3 index.py
```
For deployment with uwsgi:
```python
uwsgi --http-socket 0.0.0.0:3000 --wsgi-file main.py --master --processes xx --threads 2
```
`3000`: currently default port to access the tool;    
`xx`: how many CPU cores you would like to use for the tool.

** Future iterations will integrate them into the tool.
