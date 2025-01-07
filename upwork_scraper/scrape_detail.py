from selenium.webdriver.common.by import By
import pandas as pd
import json

from setup_environment import configure_logging, configure_driver, get_to_page 
# get_to_page(driver, url)
from connect_database import create_pgdatabase_engine, save_data
# save_data(df, engine, table_name, subcategory)

def extract_profile_details_data(driver): 
    """
        Extract related data from the website ranking page 
        Returns: 
         (datafram): datafram of the extracted data: [key]

    """
    pre = driver.find_element(By.TAG_NAME, 'pre').text
    profile_details = pd.json_normalize(json.loads(pre))
    return profile_details   

def preprocess_profile_data(profile_details): 
    """
        Preprocess data to ge general profile dataframe 
    """
    df_profile = pd.DataFrame()
    df_profile["uid"] = profile_details["profile.identity.uid"] # 3
    df_profile["ciphertext"] = profile_details["profile.identity.ciphertext"] # 3
    # profile.identity.recno key 
    # df_profile["first_name"] = profile_details["profile.profile.firstName"] # 1
    df_profile["name"] = profile_details["profile.profile.name"] # 1
    df_profile["profile_url"] = profile_details["profile.profileUrl"]
    df_profile["portrait_url"] = profile_details["profile.profile.portrait.portrait500"]
    
    # person.personName.lastName
    df_profile["country"] = profile_details["profile.profile.location.country"] # 1
    # df_profile["state"] = profile_details["profile.profile.location.state"] # 3
    # df_profile["city"] = profile_details["profile.profile.location.city"] # 3
    # df_profile["timezone"] = profile_details["profile.profile.location.timezoneOffset"] # 3
    # 4 online
    # 4 available
    
    df_profile["job_success "] = profile_details["profile.stats.nSS100BwScore"] # 1
    df_profile["top_rated"] = profile_details["profile.stats.topRatedStatus"] # 3
    df_profile["top_rated_plus"] = profile_details["profile.stats.topRatedPlusStatus"] # 3
     
    try: 
        df_profile["earnings"] = profile_details["profile.stats.totalEarnings"] # 1
    except KeyError:
         df_profile["earnings"] = None
    
    # df["earnings_backup"] = profile["profile.stats.totalRevenue"]  # 3 not working 
    df_profile["jobs"] = profile_details["profile.stats.totalJobsWorked"] # 1
    df_profile["hours"] = profile_details["profile.stats.totalHours"] # 1
    # df["hours_backup"] = profile["profile.stats.totalHoursActual"]  # 3 not working 

    try: 
        df_profile["availability_nid"] = profile_details["profile.availability.capacity.nid"] # 1
    except KeyError:
         df_profile["availability_nid"]  = None
    try: 
        df_profile["availability_name"] = profile_details["profile.availability.capacity.name"] # 2
    except KeyError:
         df_profile["availability_name"] = None
        
    # 4 profile.stats.responsiveState
    # 3 open to contract to hire New
    df_profile["english"] = profile_details["profile.stats.englishLevel"] # 3
    # 3 profile.profile.phoneVerified
    # 3 profile.profile.idBadgeStatus
    # df_profile["education"] = profile_details["profile.education"] # 1
    df_profile["hourly_rate"] = profile_details["profile.stats.hourlyRate.amount"] # 3
    df_profile["hourly_rate_currency"] = profile_details["profile.stats.hourlyRate.currencyCode"] # 3
    df_profile["title"] = profile_details["profile.profile.title"] # 2
    df_profile["description"] = profile_details["profile.profile.description"] # 2
    df_profile["total_feedback"] = profile_details["profile.stats.totalFeedback"] # 3
    df_profile["rating"] = profile_details["profile.stats.rating"] # 3
    # 4 profile.stats.ratingRecent
    
    return df_profile

def preprocess_educations_data(profile_details): 
    """
        Preprocess data to highest education dataframe 
    """
    education = pd.DataFrame(profile_details["profile.education"][0]) # 2
    df_education = pd.DataFrame()

    if education.empty:
        logging.info(f"profile education is null")
        df_education["uid"] = profile_details["profile.identity.uid"][0]
    else:
        df_education["education_institution"] = education["institutionName"]
        df_education["education_area"] = education["areaOfStudy"]
        df_education["education_degree"] = education["degree"]
        df_education["uid"] = profile_details["profile.identity.uid"][0]
        # df_education["uid"] = education["personUid"]
        df_education = pd.DataFrame(df_education.iloc[-1]).transpose()
        
    return df_education

def preprocess_skills_data(profile_details): 
    """
        Preprocess data to ge general profile dataframe 
    """
    skills = pd.DataFrame(profile_details["profile.profile.skills"][0]) # 2 tag 
    df_skills = pd.DataFrame()
    
    if skills.empty:
        logging.info(f"profile skills is null")
        df_skills["uid"] = profile_details["profile.identity.uid"][0]
        
    else: 
        df_skills["skills_name"] = skills["prettyName"]
        # df_skills["name"] = skills["name"]
        df_skills["uid"] = profile_details["profile.identity.uid"][0]   

    return df_skills

def preprocess_assignments_data(profile_details): 
    """
        Preprocess data to ge general profile dataframe 
    """ 
    assignments = pd.DataFrame(profile_details["profile.assignments"][0])   # 1
    df_assignments = pd.DataFrame()
    
    if assignments.empty:
        df_assignments["uid"] = profile_details["profile.identity.uid"][0]
        logging.info(f"profile assignments is null")
    else:
        df_assignments["startedOn"] = assignments["startedOn"]
        df_assignments["endedOn"] = assignments["endedOn"]
        # earning can be hidden 
        if assignments["totalCharges"].isna().all():
            df_assignments["charges_currency"] = None
            df_assignments["charges_amount"] = None 
        else: 
            df_assignments["charges_currency"] = pd.json_normalize(assignments["totalCharges"])["currencyCode"]
            df_assignments["charges_amount"] = pd.json_normalize(assignments["totalCharges"])["amount"]
        # initialAmount	
        # blendedChargeRate	

        df_assignments["total_hours"] = assignments["totalHours"]
        if assignments["hourlyRate"].isna().all():
            df_assignments["hourly_rate_currency"] = None
            df_assignments["hourly_rate_amount"] = None 
        else: 
            df_assignments["hourly_rate_currency"] = pd.json_normalize(assignments["hourlyRate"])["currencyCode"] 
            df_assignments["hourly_rate_amount"] = pd.json_normalize(assignments["hourlyRate"])["amount"] 
       
        df_assignments["type"] = assignments["type"] 
        # fixed and not fixed 
        df_assignments["title"] = assignments["title"]
        #df_assignments["feedback"] = assignments["feedback"] #["currencyCode"]
        # feedbackGive 
        # df_assignments["feedback_given"] = assignments["feedbackGiven"][0] #["score"] 
        # assignments["feedback"].map(lambda x: x["currencyCode"] if type(x) == dict else x)
        if assignments["feedback"].isna().all():
            logging.info(f"assignments feedback is null")
        else:
            feedback = pd.json_normalize(assignments["feedback"])
            df_assignments["score"] = feedback["score"]
            df_assignments["comment"] = feedback["comment"]
            df_assignments["is_public"] = feedback["commentIsPublic"]
            df_assignments["response"] = feedback["response"]
            length = df_assignments.shape[0]
            for i in range(length):
                if pd.isnull(feedback["scoreDetails"][i]) is not True: 
                    # False, Array[(Flase, False, False...)]
                    score_details = feedback["scoreDetails"][i]
                    for n in range(6): 
                        # len(score_details)
                        score_name = f"score_{score_details[n]['label'].lower()}"
                        score_value = score_details[n]['score']
                        df_assignments.at[i, score_name] = score_value
                        # assign the value to dataframe cell
        df_assignments["uid"] = profile_details["profile.identity.uid"][0]

    return df_assignments

def main():
    """
    """
    # config loggine and driver
    driver = configure_driver()

    # connect to database¶
    engine = create_pgdatabase_engine()

    # get unique ciphertext
    ranking_ciphertext = pd.read_sql(f"""
    SELECT ciphertext
    FROM ranking
    """, con=engine)
    unique_ciphertext = ranking_ciphertext[['uid', 'ciphertext']].drop_duplicates() 

    for i in range(0, len(unique_ciphertext)):
    
        ciphertext = unique_ciphertext[i]
        profile_details_url = f"https://www.upwork.com/freelancers/api/v1/freelancer/profile/{ciphertext}/details?excludeAssignments=false"
        get_to_page(driver, profile_details_url)
 
        profile_details = extract_profile_details_data(driver)

        # save profile_details as backup 
        output_name = f"data/profile_details/profile_details_{i}_{ciphertext}.csv"
        profile_details.to_csv(output_name )

        # check if there is error 
        # profile_details: This profile is no longer available.
        if profile_details.shape[1] == 1:
            logging.info(f"profile_details {i+1}: profile is no longer available ~~~~~ ")
        elif profile_details['profile.isPrivate'].item() == True:
            # error_message = profile_details["error"][0]
            # logging.info(f"profile_details {i+1}: {error_message}")
            logging.info(f"profile_details {i+1}: profile is set to private ~~~~~ ")
        else:
            df_profile = preprocess_profile_data(profile_details)
            logging.info(f"extract profile data from profile {i+1}")
            save_data(df_profile, engine, "profile_test", subcategory)
        
            df_languages =  preprocess_languages_data(profile_details)
            save_data(df_languages, engine, "language_test", subcategory)

            df_educations=  preprocess_educations_data(profile_details)
            save_data(df_educations, engine, "education_test", subcategory)
            
            df_skills = preprocess_skills_data(profile_details)
            save_data(df_skills, engine, "skill_test", subcategory)
        
            df_assignments = preprocess_assignments_data(profile_details)
            save_data(df_assignments, engine, "assignment_test", subcategory)
if __name__ == "__main__":
    main()