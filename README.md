#### About

<h1 align="center">InnovHope Investment Intelligence</h1>

<p align="center">A state-of-the-art tool using the cutting-edge AI to support key decisions on strategic investments in emerging industries</p>

<p align="center">
<img width="800" alt="Screenshot 2023-03-09 at 16 37 46" src="https://user-images.githubusercontent.com/108359978/224166205-2f7e6cc3-f4c2-4d29-bdb0-0f279a6e124a.png">
</p>

## Introduction

The `Innovhope Investment Intelligence (3Is)` is a dashboard-like product utilizing the commerical data from `Crunchbase` with latest cloud technologies (Amazon Web Services) to search companies in a worldwide company candidate pool and to model the company successfulness using cutting edge machine learning algorithms.    

This product is developed in close collaboration with people from InnovHope, such as [Dr. Dongjie Chen](https://www.linkedin.com/in/dj-chen/) and [Dr. Tao Lin](https://www.linkedin.com/in/phddvm/) and managed by [Dr. Xiao Zhang](https://www.linkedin.com/in/xiao-cathy-zhang-83377a51/) under the leadership of [Dr. Hong Cao](https://www.linkedin.com/in/helencao/). 

The current product is the first iteration of the project and will requires input from experienced Software Development Engineer (SDE) to conduct the code review and unit testing to increase its stability and to improve the efficiency of some functions of the product. Without the careful review by the SDE, this product remains an internal usable tools with some existing bugs.

Below is the brief manual of the functionalities of the 3Is. If you have any questions, please contact [Dr. Meng Chen](https://www.linkedin.com/in/mlchen/) by [email](mailto:meng.chen03@gmail.com).

### List of Content 
- [Functions](#Functions)
- [Important Notes](#Important-Notes)
  
## Functions
**1. Update the Crunchbase database**     
* Updating the `Crunchbase Database` is essential to maintain the competitivenss of `3Is` since the Cruchbase update its database daily; many companies from the emerging fields might updated periodically, so update function is enssential to keep the data up to date.  
* With build-in MySQL database, the Bulk-dwonload data via `Crunchbase Enterprise APIs` will be automatically downloaded, parsed, cleaned, and stored in three different relational databases: `crunchbase`, `crunchbase_sorted`, `crunchbase_ml` for raw storage, transitioanl storage, and machine learning ready, respectively.  
* To use the function, please click `UPDATE CRUNCHBASE DATABASE (AROUND 50 MINS)` botton (Figure 1), it will run in the backend for about 50 mins to update all three databases. 
<p align="center">
<img width="600" alt="image" src="https://user-images.githubusercontent.com/108359978/222528090-5af8fcfe-8b5a-4a22-80d0-12831f92469a.png">
</p>
<p align="center">
   <font size=5>Figure 1. The Button for Updating the Cruchbase Database using Enterprise Bulk Download API.</font>
</p>

**2. Update the ML model**    
* As one of the most important functions of this tool, machine learning model provides critial insights about the successfullness of the company in the future. It should be updated either by-weekly or monthly as the data in the download database has been updates. **IMPORTANT**: As the market changes as well as the emerging field switches, it is really important to update the model as the baseline chnages through time.
* To update the ML model, please click `RE-TRAIN MODELS AND SELECT THE BEST ONE` botton (Figure 2), it will retrain the model automatically in the background with updated data. Currenlty it utilize the best trained XGBoost model to predict the sucessfullness of the companies. In the future, it might require retrain entire models with different algorightms and tools to achieve better results.

<p align="center">
<img width="600" alt="image" src="https://user-images.githubusercontent.com/108359978/222528087-8e9b25df-ab3a-472f-ab4d-ce5fcae2b091.png">
</p>
<p align="center">
   <font size=5>Figure 2. The Button for Re-Training the ML Models and Choosing the Best One.</font>
</p>

**3. Search Function**   
* Search function is the first step to get the results of the companies of the interest. By search multiple terms together utilizing the Natural Language Processing (NLP) techniuqes with `phrasematcher` from package `spaCy`, the search results can be either limited to specific search terms or expanded with the search results across a variety of the different unrelated terms. This is entirely based on the requirements from the user perspectives. See below for examples.

<p align="center">
<img width="800" alt="image" src="https://user-images.githubusercontent.com/108359978/222534482-de490782-0eff-4122-b3b5-e40de508e87f.png">
</p>
<p align="center">
   <font size=5>Figure 3. Components of Search Functions.</font>
</p>

* To perform the search, please follow the steps as described below (see Figure 3 for referred components):
   * **Step 1**: Type A Tag
      * Tag can be anything, including numebers and/or strings, and it is for internal recording on the search, not affect the resutls;
   * **Step 2**: Input Your Search Terms
      * Search terms can have similar meanings, such as `covid-19 vaccine, covid19 vaccine, and Sars-Cov-2 vaccine`  ----> limiting results to covid related vaccines;
      * Search terms can also differ from each others, such as using `vertical farm` and `gene editing` ----> mixed results of vertical farm and gene editing;
      * Results will entire depending on the inputs; a good approch would be search specific term first; if there are not many results in the output, then board your search terms, such as changing `mrna vaccine, messenger rna vaccine` to `mrna, messenger rna`. As a result, you might get overwhelming results showing on the dashboard. To mitigate this, there is download button below to save all results before you want to look into the results.
   * **Step 3**: Show Results
      * After the search is completed (about 100 mins), the geographic map area will be freshed but no results will show up until the `SHOW RESULTS` button is clicked.

**4. General Results**
   * 4.1 Company Geographic Distribution
      * After the `SHOW RESULTS` button is clicked, based on the company addresses provided by Crunchase, the backend of the `3Is` will process the addresses with opensourced package of the `Geopy` to get the GPS coordiantes of the companies in the search results. It will take a while to show the results since the package of `Geopy` free to use with limited calls in a specific time frame. After it completes the process, the results will show up on the geographic map which centers the United States.
      * By hovering on the dots that represent companies on the map, the brief descriptions of the companies will be shown up.
      * **NOTE**   
         * Since the opensourced package of `Geopy` is free, there are always some errors of GPS coordinates it produced. As a result, some of the company won't be correctly plotted on the map;
         * Companies in the Crunchbase database that don't provide the addresses won't show up on the map as well.
      
<p align="center">
<img width="800" alt="image" src="https://user-images.githubusercontent.com/108359978/222528139-7a4757ab-1bce-4b94-8a32-dc250577305a.png"">
</p>
<p align="center">
   <font size=5>Figure 4. Geographic distribution of the Companies in the Search Results.</font>
</p>

   * 4.2 Summary Stats of the Results     
      * Based on the data from Crunchbase, the summary stats divided feature variables into three categories, time-related, funding-related, and categorical features. By selecting different features in each category, the user can visualize the summary stats of the each feature of searched results.
                 
<p align="center">
<img width="800" alt="image" src="https://user-images.githubusercontent.com/108359978/222528145-ea4373d8-3090-48aa-bb1e-534f8b5fa83e.png">
</p>
<p align="center">
   <font size=5>Figure 5. Summary Stats of the Companies of the Search Results.</font>
</p>

**5. Selected Companies**
   * 5.1 Detailed information of the selected companies 
      * The dropdown menu provides the user an ability to select the company from the search results. The companies were ranked based on their 3Is Investment Scores, from the highest to the lowest.
      * By selecting any company, the dashboard should display its headquarter location, `3Is Investiment Score`, `Company brief description`, and most important `People` (founders for example) of the company.
      * **NOTE**
         * The function requires the `Crunchbase Enterprise RESTful APIs` to directly connect the database of Crunchabse, some of the information cannot be retrieved using the APIs. As a result, the information of the company might not show up, such as people or company description.

* #### Examples of the dropdown selections
   * Selecting Moderna Theraputic Inc.
                 
<p align="center">
<img width="800" alt="image" src="https://user-images.githubusercontent.com/108359978/222528149-ecfcb990-04ba-439a-a873-bc296103e36c.png">
</p>
<p align="center">
   <font size=5>Figure 6. Example One: Moderna Theraputic Inc.</font>
</p>
                 

*  * Selecting CureVac
 
<p align="center">
<img width="800" alt="image" src="https://user-images.githubusercontent.com/108359978/222528150-9db3bafc-1e41-4dd6-8a42-5f0b26e03735.png">
</p>
<p align="center">
   <font size=5>Figure 7. Example Two: CureVac N.V.</font>
</p>
  
**6. Download Results**  
Click the `DOWNLOAD CSV` button to download the search results (Fig. 8).
<p align="center">
<img width="800" alt="image" src="https://user-images.githubusercontent.com/108359978/224356300-9c139340-435f-43b2-a713-4d2b63680b6a.png">            
</p>                
<p align="center">
   <font size=5>Figure 8. Download results button in red circle</font>
</p>
                 
The results will be saved as a csv file in a local machine and provide detailed information of the companies of interest (Fig. 9).
<p align="center">
<img width="1100" alt="image" src="https://user-images.githubusercontent.com/108359978/224358713-790dad57-6a6d-4eb1-9a7b-b01e0777fb0a.png">
</p>                
<p align="center">
   <font size=5>Figure 9. An example of the saved csv file</font>
</p>
                
                 
## Important Notes

1. The creator of this tool, Dr. Chen, is not a SDE by his training. There are definitely bugs remaining in the codebase, which might not effect on the service but limits the product performance. For future iterations, the Innovhope should hire a experienced SDE to improve or even rewrite some of the codebase in order to improve its search efficiency and model performance.

2. Despite the tool uses the commercial data from Crunchbase, there are some drawbacks of the product, which might be minor issues listed below but not limited to:
   * `3Is` is limited by data source from Crunchbase. It utilizes the `Crunchbase Enterprise Bulk Download APIs` to update the data and its RESTful APIs to query information, such as Organization Founder, Linkedin links, Photo links and etc, based on the search results. If the information not in the database, there is no way that the tool can locate it.
   * The `Crunchbase Enterprise RESTful APIs` have their own limitations, such as showing first 100 results of the search based on the query categories; in addition, not all informaiton in the Bulk-downloaded data can be retrivied by the APIs. Please refer the Cruchbase data for more details.

