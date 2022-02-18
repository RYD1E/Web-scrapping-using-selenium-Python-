#Importing the required modules.


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd


def food_data(i):                                                            #A function to collect the nutritional info, tags, category of the food.
    url="https://www.nutritionix.com"+i
    driver.get(url)

    try:                                                                     #Try n except for timeouts while scrapping.
        element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "nutritionLabel")))
        try:                                                                  #Try n except for index error if : element not found in the webpage or blocked by the site.
            x=driver.find_elements_by_class_name("nutritionLabel")
            x[0].text
            st=x[0].text
            a=st.split('\n')
            b=[a]
            y=driver.find_elements_by_class_name("box-content")
            z=driver.find_elements_by_class_name("nutrient-claims")
            z1=z[0].text
            z1=[list(z1.split('\n'))]
            l2=[y[1].text]+z1
            l=[i[len("/uk/food/"):],url]+b+l2                                   #concatinating the lists with names and links to nutritional info, tags, category of the food
            return l
        except IndexError:                                                      #putting null in dataframe if errors occur.
            l=[i[len("/uk/food/"):],url]+['null']+['null']+['null']
            return l

    except TimeoutException:
        l=[i[len("/uk/food/"):],url]+['null']+['null']+['null']
        return l


def link_scrp():                                                                                    #A function to collect the links.
    myset=set()                                                                                    
    s=set()
    for page in range(1,100):                                                                       #Currently using 100 but it won't run more than the number of pages.
        print('Scrapping page: '+ str(page))
        path="https://www.nutritionix.com/uk/database/common-foods?page="+str(page)
        driver.get(path)
        try:                                                                                        #Using try for n except for detemining the last page and timeout errors too.
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "item-row")))
            myLinks=driver.find_elements_by_class_name("item-row")
            for link in myLinks:
                print(link)
                if(str(link.get_attribute("href")).startswith('/uk/food/')):                        #Taking links from the elements.
                    myset.add(link.get_attribute("href"))
                    s.add(link.get_attribute("href"))                                               #recording all the links.
                li=list(myset)                                                                      #if this remains empty it means we were at the last page.
                if li==[]:
                    break

        except TimeoutException:
            print("Scrapped!")
            driver.close()
            break
        finally:      
            myset=set()                                                                     #Emptying the set to iterate again.
    links= list(s)
    return links                                                                            #returning links to the list.

def dataf(links):                                                                           #A function to prepare the dataframe.    
    li=['Name','Link','Nutritional Values',"Category","Tags"]
    df = pd.DataFrame(columns=li)
    j=0                                                                                     #For indexing
    for i in links:
        df.loc[j] = food_data(i)                                                            #for putting data row-wise.
        j=j+1
    return df


#Lets make the instace and call the functions.
driver_path = r'C:\Users\Shubham\Downloads\chromedriver.exe'
driver = webdriver.Chrome(executable_path=driver_path)

#scrapping links.
links=link_scrp()

#making dataframe.
df=dataf(links)

#Exporting the dataframe to CSV.
df.to_csv(r"C:\Users\Shubham\OneDrive\Desktop\New folder\Links.csv",index=False)

driver.quit()