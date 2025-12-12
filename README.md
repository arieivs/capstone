# 🗿 Capstone Project

The Capstone is the final project from the Lisbon Data Science Academy. For my batch, we had access to data from a retailing company (anonymised as Retailz) and the goal was to predict future prices for certain product categories for its two main competitors (referred to as competitor A and B). This ReadMe is a compilation and summary of sections from the two reports I had to submit detailing the work done during the project.

## 💡 1. Summary
This project aims at analysing and forecasting product prices from Retailz competitors.
</br>

In a industry such as retailing where pricing dynamics are constantly evolving, a prices forecasting tool can be a competitive advantage. First, an in-depth analysis of the data shared by the client was made, with the intention of understanding the influence of different factors in the final price, as well as extracting valuable business insights. The conclusions of this analysis were presented on the first report.
</br>

The second phase of the project was the modeling of the sales price to the variables found to be significant for the task. As the objective was to forecast the sales price for the two main competitors from Retailz, two different models were created, one for each competitor. Different models were experimented with and evaluated - the goal was to find the one which would minimize both the mean absolute error (MAE) and root squared mean error (RSME), while providing the most balanced performance possible across the different product categories. The final models used the Random Forest Regressor from Scikit Library and were based on the product’s SKU, date, and product’s level 2 category. The hyperparameters chosen were maximum depth 12 and minimum sample split 5. For the chosen models, the MAE and RSME obtained with the test data for competitor A were 9.76€ and 15.00€ respectively, and 10.62€ and 16.82€ for competitor B.
</br>

The models were then deployed and an API was built, allowing the users to get predictions of the selling price at these two key competitors for specific products and dates. The API has two endpoints, one which returns the forecasted selling prices, and another which can be later used to update the database with the actual price for that product on that day. The application performs a thorough input validation, to prevent processing and storing any erroneous value given either by human error or malicious intent.
</br>

## 🔍 2. Data Analysis
### 2.1. General analysis
The data provided by Retailz consisted on:
* prices of certain products in certain moments in time, both for Retailz and two of its key competitors, along with whether the product was being advertised as a promotion at that time or not
* classification of the different products into several structures, with different levels of granularity, along with the quantity sold of each product by Retailz in different moments in time
* promotional campaigns organized both by Retailz and one of its key competitors, with respective start and end date

While exploring the data at hand, there was interest in understanding how the data was distributed amongst the different companies, product categories and throughout time. Looking at the distribution per company, there is more data available from Retailz than from its competitors, potentially from the ease in acquiring such data. Regarding the prices dataset, around 56% of the data belongs to Retailz, while 35% and 9% to competitors A and B, respectively. On the campaign’s dataset, around 54% of the information is regarding Retailz’s campaigns and 46% on competitor A, while there is no information on competitor B’s campaigns.
</br>

Analysing the information available per product category, it can be seen that the number of distinct products falling within each category varies significantly, from 27 to 804 in a single category.
</br>

All datasets comprise data from the beginning of January 2023 to the end of October 2024. The amount of information available per competitor is fairly constant throughout this time period.
</br>

The data was analysed in order to understand how seasonality, promotional campaigns and customer demand impact on future prices.
</br>

In order to assess the data’s seasonality, the data was arranged per product category, down to structure level 2, or per competitor. Looking at how the prices on a given day were influenced by the prices on the previous days, a light weekly seasonality could be found. The most noticeable influence was from 6 weeks before, indicating a potential one month and a half cycle. Additionally, the prices from the previous day and four days before also seemed to be significant. The weekly seasonality was more clear when looking only at the data from competitor B. A closer look was taken to the prices around Christmas and Black Friday (24th November 2023) but no clear influence from these two events was found on the data.
</br>

To assess the influence of ongoing structured campaigns on the sales prices of different product categories, the average price per product category with and without an ongoing campaign was compared. No significant difference was found, more specifically, aggregating the products per its structure level 2, on average the price was 19 cents lower during a campaign than outside, and maximum 3,22€ lower. In relative terms, on average the price was 1% lower, maximum 6% lower.
</br>

Finally, to look into the impact of demand on pricing, sales and prices data was crosschecked. As expected, items at a higher price are purchased less than items at a lower price. The nature of the item also comes into play here, as cheapest items tend to be needed more often and/or in bigger quantities. It’s hard to evaluate the impact of demand on pricing as one would expect this relationship to go both ways, in other words, an increase in demand is probably followed by an increase in price, but an increase in price is probably also followed by a decrease in demand.
</br>

### 2.2. Business questions analysis
Following Retailz’ guidelines, the data was also analysed to look for potential business drivers, such as the level of promotional participation at Retailz, how pricing competitiveness varies over time, the average discount per competitor in different product categories, and whether there is a reactive pricing behaviour between competitors.
</br>

Thinking of promotional participation as the fraction of sales done from promotional products, throughout the period data was provided from, 23,5% of the sales were from products with an active promotion. To be noted that the sales’ quantity is given in different units depending on the product, and there is no indication on the units being used for each case. For some cases the quantity is referring to the weight, giving more relevance to denser products than to lighter ones. Since sales data is only available for Retailz, it is not possible to calculate the promotional participation from the competitors, and thus compare it between the different companies.
</br>

While comparing prices between different competitors, the focus was on the products for which information was available for all three companies. This reduced significantly the data available for the comparison, but avoided drawing wrong conclusions due to, for example, the products for which information is only available for Retailz being more expensive overall.
</br>

When looking at pricing competitiveness, it was assessed whether prices at Retailz tended to be higher than at its competitors. For each product at a given moment in time, it was identified whether Retailz was the most expensive or the cheapest. The conclusion is that, from beginning 2023 until October 2024, Retailz was the most expensive store for a given product in a given moment in time 19% of the time, and the cheapest 13% of the time. To see how this evolves in time, the relative amount of times Retailz was the most expensive and the cheapest for each month was plotted. It was seen that since the end of 2023, Retailz has consistently been the most expensive option more often than the cheapest one. This was not the case at the beginning of 2023, in other words, Retailz was more price competitive in the beginning of 2023 than in 2024.
</br>

Both the average discount and sales price per competitor was looked into, across product structures at level 1 and 2. All three companies apply higher discounts at products from categories 2 and 3, and less to products from category 1. This behaviour is even more accentuated for Retailz than for its competitors. However, due to differences in the average base price between competitors, the panorama changes when looking at the final sales price. Even though competitor B is usually not the one applying the biggest discount, it is most often the cheapest option across all product categories.
</br>

Finally, there was interest in understanding whether price changes from one of the three companies were followed by one of the others in the short-term (few days to a week periods). For this, the correlation between the price from one of the players on a given day and the price for the remaining actors on the following days was studied. No significant correlation between the prices from competitor B and the remaining two companies was found. There is a correlation between prices between Retailz and competitor A, specially for products falling into structure level 1. The correlation is more significant when comparing prices from the same day. With this in mind, it’s not clear one is influencing the other, when both might be looking out to the same signals and being influenced in similar ways by other factors.
</br>

## 🎨 3. Modelling
### 3.1. Model specifications
The chosen model was the Random Forest Regressor from the Scikit Learn library. Two identical models were trained, one fitted with data from competitor A and the other with data from competitor B, then used to forecast prices from the respective competitor. This strategy allows to tune the models to the company’s specific behaviour. Given the project’s focus in these two competitors, rather than in a sector-wide prediction of the prices evolution, this approach was the preferred one.
</br>

The pipeline built for the forecasting process included a custom transformer and the random forest regressor estimator. The custom transformer is focused on extracting new features from the time_key column, namely the year, month, day, weekday, cyclic weekday using the sine function, and whether the day is a weekend or working day. The time_key column is then removed from the dataset. The features used to train the model consisted of the time-related features extracted in the custom transformer, the product’s sku and structure. level 2. The target was the sales price, calculated from applying the discount to the base PVP price.
</br>

A grid hyperparameter search was performed, to assess the impact of the forests’ maximum depth and minimum samples split. Taking into consideration the results and further restrictions, a maximum depth of 12 and minimum samples split of 5 were used.
</br>

From the training data received at the start of the project, data previous to 01/05/2024 was used for training purposes, while the one from that day onwards until the end of October 2024 was used as the validation set. The test set consisted of the data retrieved via the calls to the API, for the cases that the actual price was also provided, whose dates ranged from 29/10/2024 to 30/12/2024.
</br>

The performance of the model’s prediction was evaluated using both the mean absolute error (MAE) and root squared mean error (RSME). These were calculated for the entire training, validation and test datasets, as well as per structure level 2. The difference between the highest and lowest error obtained for different product categories was calculated and also used as a performance metric.

### 3.2. Alternatives considered
Initially, a quick baseline was built in order to work on model deployment and to have a reference for any further improvements. The baseline consisted of using a linear regression model, without any feature engineering.
</br>

After the initial baseline, three different estimators were considered: linear regression, random forest regressor and gradient boosting regressor. These three different models were tested both after applying the custom transformer and without any treatment of the time_key data, as well as with and without information regarding the product’s structure level 2. With the linear regression model, the application of One Hot Encoding to both the product’s sku and its structure level 2 was also tested. In the case of the tree-based models, using one hot encoding was discarded due to a huge increase in training time. Both mean absolute error and root squared mean error were calculated to assess the models’ performance. The best option was to use the Random forest model after applying the custom transformer, including information regarding structure level 2.
</br>

Further investigation was made in the attempt of improving the model performance and reducing model complexity and potential overfitting:
* Categorising the products using structure level 1 and 3, instead of 2, was explored - overall there was a decrease in performance when using structure level 1, while the results when using structure 3 were fairly similar, thus structure level 2 was maintained.
* Given that there is more data available for some product categories than others, both undersampling and oversampling strategies were experimented, in order to have the same amount of samples per product category on the training datasets - none of the sampling strategies significantly improved the model’s performance.
* Since the sales price varies substantially, given the big variety of products being analysed, normalising the final price using a Standard Scaler and a Transformed Target Regressor from Scikit Learn was tested - no significant improvement in the model’s performance was observed.
* A Hyperparameter grid search was carried out to assess the impact of the minimum sample split and maximum depth; A maximum depth ranging from 10 to 13, along with minimum sample split from 3 to 5 were tested - overall it was observed that the higher the maximum depth, the better the performance, but as it is further explained in the following sections, it was kept at 12 to reduce the model's complexity. The impact of the minimum sample split varied, not causing a significant difference overall.

## 🎢 4. Deployment
The app is hosted on Railway, and it makes use of a docker container. The dockerfile uses the python 3.12 docker image as its base image, installs the necessary python libraries and launches the app by running the respective python file. The app is built with the micro web development framework Flash and is connected to a PostgreSQL database.
</br>

As previously mentioned, two pipelines were created, one fitted to competitor A data, other to competitor B. Both pipelines were serialized and deployed to the Railway’s server. The app then deserializes and uses them to make further predictions with the new data the app receives.
</br>

The app makes available an API with two POST endpoints, forecast_prices and actual_prices. The forecast_prices endpoint receives a product’s SKU and a date, and returns de forecasted prices for this product at this moment in time both for competitors A and B. The actual_prices endpoint receives, besides the product’s SKU and a date, the actual prices for competitors A and B for that product on that day, so that a comparison can be made between previous predictions and the real price.
</br>

Both endpoints perform an input validation which assures that:
* The body of the request, formatted as a JSON, has all the expected keys and no
unexpected ones.
* It’s made sure that the time_key is an integer representing a date in %Y%m%d
format. Given that there is no interest in forecasting prices for dates previous to the training data received, which starts on January 1st 2023, nor too much ahead in time as the predictions won’t be reliable, the date received is expected to be between 01/01/2023 and 31/10/2029 (5 years after the end of the training data).
* The product’s SKU ought to be a numeric code received as a string. The codification of each product into a SKU is company specific, depending on the company’s stock and inventory management. It was observed that there were SKUs from 1128 to 4735 on the training data, thus it was imposed that the received SKU ought to be between 1000 and 4999.
* It’s verified that the real sales price received by the actual_prices endpoint is a float. The price should also be positive or zero.

The product-date pairs stored in the database ought to be unique, thus in the forecast_prices endpoint a new product-date pair is expected. If a prediction has already been made for the given product-date pair, an error is thrown. In the case of the actual_prices endpoint however, an already known product-date pair is expected, the idea being that first a prediction is made, and later, once the real price is known, the database is updated with this information to potentially improve the model. That being said, if the actual_prices endpoint is called with an unknown product-date pair, it throws an error. In all the described cases in which the input given is not valid, the API responds with the HTTP code 422.
</br>

The models which were used require the product’s level 2 structure, besides the SKU and date which are given by user input. For this reason, it was necessary to add a table in the database with information regarding each product’s level 2 structure, so that this information could be retrieved and fed to the model for forecasting the price. The necessary data was uploaded to the server in a CSV format, and a python script was written to create a new table in the PostgreSQL database and fill it in with the CSV file’s information. By connecting to the host machine via SSH, the script was run to add this data to the production database.
</br>

The models’ predictions for the different product-date pairs, along with the real values received later on, are stored in the production database. This data can then be retrieved to further evaluate or improve the model.

## 🔮 5. Future Improvements
The forecast_prices endpoint was designed to receive only the product’s SKU and the date. This limited the features which could be used for predicting the prices to features related to the product structure, which could be retrieved from the SKU, and time-related features which could be extracted from the time stamp. Originally a lot of interesting data was shared, regarding marketing campaigns and demand of the different products. The impact of this data in the model performance was not analysed since it would not be available for future predictions, but it’s an analysis which could be worth doing.
</br>

There are currently some limitations in the input validation, especially when it comes to the real price received by the actual_prices endpoint. Different strategies could be developed to add an additional layer of verification to the given values. For example, a range of values could be set per product category, to only accept prices falling within that range. Another option would be to analyse the received values a posteriori, and discard those that can be considered outliers. Sanitizing these values would be important before moving to the next future improvement.
</br>

Currently there is no retraining strategy implemented. A process to retrain the model everytime the MAE or RMSE fall under a certain threshold could be set, for example. If a sudden change in pricing behaviour for a given product or given category is observed, the model could also be retrained with the more recent data. If a change in the company’s policy or marketing strategy is known, or any other factor which could lead to a change in pricing behaviour, a retraining of the model could also be set manually.
</br>

As mentioned in the beginning, two separate models were trained, one for each competitor, given the project’s focus on these two competitors. It would be interesting to discuss with the client if there is any interest in a sector-wide prediction of the prices evolution. Further explorations could be made making more use of Retailz’ data.
