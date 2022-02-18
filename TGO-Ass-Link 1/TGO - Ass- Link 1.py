#Importing the required modules.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


def ing(y):                                                                     #A function to collect the ingredients.
    df = pd.DataFrame(columns=["Ingedients","Desc","Qnt","Wt"])                 #Making a dataframe to record the values.
    for i in range(len(y)):
        st=y[i].text                                                            #Collecting the text from the web-element.
        l3=st.split('\n')
        df.loc[i] = l3                                                          #Updating the row of the dataframe with the values.
    return df
        
def rep(z,li4):                                                                 #A funtion to scrap the steps of the recipie.
    st1=z[0].text
    li=st1.split('\n')  
    li2=[]
    for w in li:
        if w.startswith("Step"):
            li.remove(w)                                                       #Preparing list for the values of dataframe by removing the step tag.
            li2.append(w)                                                      #Saving the steps for col names.
    li=li4+li
    df = pd.DataFrame(columns=["Name of the Dish"]+li2)
    for i in range(1):
        df.loc[i] = li
    return df
def mkdf(df,name):                                                             #A simple funtion to make a csv out of a dataframe.
    df.to_csv(r"C:\Users\Shubham\OneDrive\Desktop\New folder"+"\\"+name,index=False)


#Lets start the main code.
#Calling driver instance fro chrome.
url="https://www.eatthismuch.com/recipe/nutrition/protein-southwest-scramble,254564/"
driver_path = r'C:\Users\Shubham\Downloads\chromedriver.exe'
driver = webdriver.Chrome(executable_path=driver_path)

#Searching the webpage
driver.get(url)

#accesing respective tags. 
a=driver.find_elements_by_class_name("modal-title")                                 #for name
st=a[0].text
l=[st]
y=driver.find_elements_by_class_name('diet_draggable')                               #for ingredients  
df=ing(y)

#Making the ingedients csv file.
mkdf(df,st+"_Ingredient.csv")

z=driver.find_elements_by_class_name("recipe_directions_list")                      #for recipe.

df=rep(z,l)

#Making the Recipe Csv.
mkdf(df,st+"_Recipe.csv")