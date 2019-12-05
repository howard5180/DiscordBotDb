import pymysql.cursors
import pymysql
import discord
from discord.ext import commands
import re
import collections
import os

#connection to sql
def getConnection():
    connection = pymysql.connect(host=os.environ["DB_HOSTNAME"],
                                user=os.environ["DB_USERNAME"],
                                password=os.environ["DB_PASSWORD"],
                                db=os.environ["DB_NAME"],
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
    return connection

#all the sql execution
