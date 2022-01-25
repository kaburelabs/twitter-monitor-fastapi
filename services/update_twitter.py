# import pandas as pd
import json
import tweepy
from datetime import datetime

# import time
# import pymongo
import motor.motor_asyncio
from decouple import config
from config.settings import get_db_projects

api_key = config("api_key")
api_secret_key = config("api_secret_key")
access_token = config("access_token")
access_token_secret = config("access_token_secret")

# Connect to Twitter API using the secrets
auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

conn = get_db_projects()


async def update_summary_cards(acc_name, data):

    project_data = data.copy()

    myquery = {"project_name": acc_name}
    newvalues = {"$set": project_data}

    await conn["projects_card_data"].update_one(myquery, newvalues)

    return project_data


async def projects_list(projects_list, date):

    for project in projects_list:
        try:
            user = api.get_user(screen_name=project)
            followers = user.followers_count
            following = user.friends_count
            name = user.name
            location = user.location
            img_url = user.profile_image_url
            url = user.url
            created = user.created_at

            conn_new = mongo_connection("twitter2", project)

            entry_value = {
                "_id": date,
                "followers": user.followers_count,
                "following": user.friends_count,
            }

            await conn_new.insert_one(entry_value)

            # cond1 = project=="spacebudzNFT"
            proj = conn_summary.find_one({"project_name": project})

            if await proj:
                await update_summary_cards(
                    acc_name=project,
                    data={
                        "alias_name": name,
                        "Location": location,
                        "total_followers": followers,
                        "following": following,
                        "website_url": url,
                        "image_url": img_url,
                        "last_updated": date,
                    },
                )
            else:
                await conn_summary.insert_one(
                    {
                        "project_name": project,
                        "total_followers": followers,
                        "alias_name": name,
                        "following": following,
                        "Location": location,
                        "created_at": created,
                        "website_url": url,
                        "image_url": img_url,
                        "last_updated": date,
                        "verified": None,
                        "verification_date": None,
                        "oficial_drop": None,
                        "last_updated": date,
                    }
                )

        except:
            print(f"{project} do not have data")
            pass
