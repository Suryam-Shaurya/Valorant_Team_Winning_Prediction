# Valorant Team Winning Prediction

**Site Link: https://valowinner.streamlit.app/**

## About Project

This project employs a Machine Learning model to estimate the probabilities of winning for two teams, each consisting of five players.

## Motivation

The motivation behind developing this Valorant winning prediction model stems from my passion for playing Valorant and the desire to gain insights into the strength of opponent teams before matches.
By creating this prediction model, I aim to provide myself and other Valorant enthusiasts with a tool that can estimate the chances of winning for two teams, Team A and Team B, before the match even begins. This knowledge allows players to make more informed decisions regarding strategies, agent selection, and gameplay approaches.

## Datasets

This project leverages data obtained through **web scraping** from a Valorant match tracking website. The scraped dataset, which comprises **5,517 rows** and **42 columns**, is used for training and testing. The web scraping process is implemented using Beautiful Soup 4, a Python library known for its web parsing capabilities.

## Algorithm/Technology

* Numpy
* Pandas
* Beautifulsoup4
* Logistic Regression
* SVM
* Naive Bayes
* KNN
* DecisionTreeClassifier
* RandomForestClassifier
* XGBoost
* LightGBM
* CatGBM
* Streamlit

# Examples

<figure>
<figcaption align = "center"><b>Model Prediction</b></figcaption>
<img src="https://github.com/Suryam-Shaurya/Valorant_Team_Winning_Prediction/blob/model_1/Snapshots/pred_1.png?raw=true" alt="Model_Flickr8k" >
</figure>

<figure>
<figcaption align = "center"><b>Actual</b></figcaption>
<img src="https://github.com/Suryam-Shaurya/Valorant_Team_Winning_Prediction/blob/model_1/Snapshots/actual_1.png?raw=true" alt="Model_Flickr8k" >
</figure>

The model predicted the winning chance of Team A(39.87%) is less than Team B(60.13%). Hence Team A would lose the match. In actuality, Team A lost the game with a score of 9-13.

> Please note that data for certain players may not be found due to their private account settings.

## Model

* This project presents an ensemble model composed of **four base classifiers** for  predictions. The ensemble model combines the outputs of the following four base models: 

	1\. Support Vector Classifier with **RBF** kernel</br>
	2\. LightGBM Classifier</br>
	3\. Support Vector Classifier with **linear** kernel</br>
	4\. Logistic Regression

* In the process of optimizing classifiers, **RandomSearchCV** is utilized to fine-tune specific base classifiers, while others are manually tuned.

* Performed **five-fold cross-validation** to select the best model among individual models and the ensemble, optimizing performance assessment and model selection.

## Results

* The ensemble model achieved a five-fold **cross-validation accuracy of 93.06%** and a mean training accuracy of 95.20%.
* After training on 80% of the dataset, the model achieved a training accuracy of 95.27% and a test accuracy of 94.28%.

<figure>
<figcaption align = "center"><b>Confusion Matrix</b></figcaption>
<img src="https://github.com/Suryam-Shaurya/Valorant_Team_Winning_Prediction/blob/model_1/Snapshots/result_train.png?raw=true" alt="Model_Flickr8k" >
<img src="https://github.com/Suryam-Shaurya/Valorant_Team_Winning_Prediction/blob/model_1/Snapshots/result_test.png?raw=true" alt="Model_Flickr8k" >
</figure>


## Run Command

Clone this repository, open `app.py` and run `streamlit run app.py` to use the model locally.

## References

* https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.LGBMClassifier.html
* https://scikit-learn.org/stable/supervised_learning.html
* https://docs.streamlit.io/
