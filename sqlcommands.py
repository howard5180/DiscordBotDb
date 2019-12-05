import pymysql.cursors
import pymysql
import discord
from discord.ext import commands
import re
import collections
import os

#connection to sql
def getconn():
    connection = pymysql.connect(host=os.environ["DB_HOSTNAME"],
                                user=os.environ["DB_USERNAME"],
                                password=os.environ["DB_PASSWORD"],
                                db=os.environ["DB_NAME"],
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
    return connection

#all the sql execution
def getElementLink(stringInput):
    if ("Fire" in stringInput):
        return "https://cdn.discordapp.com/attachments/470712762314784799/504091443242205184/fire.png" 

    if ("Earth" in stringInput):
        return "https://cdn.discordapp.com/attachments/470712762314784799/504091441908154369/earth.png" 

    if ("Lightning" in stringInput):
        return "https://cdn.discordapp.com/attachments/470712762314784799/504091445825765386/lightning.png"

    if ("Water" in stringInput):
        return "https://cdn.discordapp.com/attachments/470712762314784799/504091447809540126/water.png"

    if ("Light (Holy)" in stringInput or "Light" in stringInput or "Holy" in stringInput):
        return "https://cdn.discordapp.com/attachments/470712762314784799/504091444085129236/light.png"

    if ("Dark" in stringInput):
        return "https://cdn.discordapp.com/attachments/470712762314784799/504091435327422464/dark.png"

    if ("Hybrid" in stringInput):
        return "https://media.discordapp.net/attachments/456208112790142977/498370434912485406/IIC_90000001.png"

    if ("Support" in stringInput):
        return "https://media.discordapp.net/attachments/456208112790142977/498370436866899969/IIC_90000002.png"

    if ("Heal" in stringInput):
        return "https://media.discordapp.net/attachments/456208112790142977/498370439219904512/IIC_90000003.png"

    if ("Passive" in stringInput):
        return "https://media.discordapp.net/attachments/456208112790142977/498370434744582144/IIC_90000004.png"

    if ("List" in stringInput):
        return "https://media.discordapp.net/attachments/456208112790142977/471391949572800514/SS.png"
        
    return "https://media.discordapp.net/attachments/456208112790142977/471391949572800514/SS.png"

def getElementEmoji(stringInput):
    if ("Fire" in stringInput):
        return f"<a:Fire:492102021911019521> - {stringInput}" 

    if ("Earth" in stringInput):
        return f"<a:Earth:492101844148027412> - {stringInput}" 

    if ("Lightning" in stringInput):
        return f"<a:Lightning:492102153348055043> - {stringInput}"

    if ("Water" in stringInput):
        return f"<a:Water:492102291092930560> - {stringInput}"

    if ("Light (Holy)" in stringInput or "Light" in stringInput or "Holy" in stringInput):
        return f"<a:LightHoly:492101364998995968> - {stringInput}"

    if ("Dark" in stringInput):
        return f"<a:Dark:492101704167194625> - {stringInput}"
    
    return f"{stringInput}"    

def getElementColor(stringInput):
    if ("Fire" in stringInput):
        return 0xff0000

    if ("Earth" in stringInput):
        return 0x03FA17

    if ("Lightning" in stringInput):
        return 0xFAD603

    if ("Water" in stringInput):
        return 0x00E0FF

    if ("Light (Holy)" in stringInput or "Light" in stringInput or "Holy" in stringInput):
        return 0xFAFAB6

    if ("Dark" in stringInput):
        return 0x9013FE

    if ("Hybrid" in stringInput):
        return 0x000000

    if ("Support" in stringInput):
        return 0x00ffff

    if ("Heal" in stringInput):
        return 0x00ff00

    if ("Passive" in stringInput):
        return 0xffe599
    
    if ("List" in stringInput):
        return 0x8e8e8e
    
    return 0x000000

def getWeaponElement(stringInput):
    stringInputLower = stringInput.lower()
    returnString = ""

    if (len(stringInput) >= 4):
        if (stringInputLower == "fire"):
            returnString = "Fire"

        if (stringInputLower == "earth"):
            returnString = "Earth"

        if (stringInputLower == "lightning" or stringInputLower == "thunder"):
            returnString = "Lightning"

        if (stringInputLower == "water"):
            returnString = "Water"

        if (stringInputLower == "light"):
            returnString = "Light"

        if (stringInputLower == "dark"):
            returnString = "Dark"

    return returnString

def getWeaponClass(stringInput):
    stringInputLower = stringInput.lower()
    returnString = ""
    if (len(stringInput) >= 2):
        if (stringInputLower in "shield" or stringInput in "& shield" or stringInput in "sns"):
            returnString = "Sword & Shield"

        if (stringInputLower in "great" or stringInputLower in "gs"):
            returnString = "Great Sword"

        if (stringInputLower in "spear"):
            returnString = "Spear"

        if (stringInputLower in "dual" or stringInputLower in "dbs"):
            returnString = "Dual Blades"

        if (stringInputLower in "bow"):
            returnString = "Bow"
        
    return returnString

def getWeaponType(stringInput):
    stringInputLower = stringInput.lower()
    returnString = ""
    if (len(stringInput) >= 4):
        if (stringInputLower == "normal"):
            returnString = "Normal"

        if (stringInputLower == "astral"):
            returnString = "Astral"

        if (stringInputLower == "heat"):
            returnString = "Heat"

        if (stringInputLower == "soul"):
            returnString = "Soul"

        if (stringInputLower == "burst"):
            returnString = "Burst"
        
        if (stringInputLower == "oracle"):
            returnString = "Oracle"

    return returnString

def filterInput(inputString):
    newString = re.sub('[^A-Za-z0-9\s]+', '', inputString)

    return newString

def matchWeaponAttributes(inputWordArray):
    elementArray = []
    typeArray    = []
    classArray   = []

    for row in inputWordArray:
        if (getWeaponElement(row)):
            elementArray.append(getWeaponElement(row))
        if (getWeaponType(row)):  
            typeArray.append(getWeaponType(row))
        if (getWeaponClass(row)):  
            classArray.append(getWeaponClass(row)) 

    elementArrayFiltered = list(set(elementArray))
    typeArrayFiltered = list(set(typeArray))
    classArrayFiltered = list(set(classArray))
    
    if (len(elementArrayFiltered) == 1):
        elementString = elementArrayFiltered[0]
    else:
        elementString = ""

    if (len(typeArrayFiltered) == 1):
        typeString = typeArrayFiltered[0]
    else:
        typeString = ""

    if (len(classArrayFiltered) == 1):
        classString = classArrayFiltered[0]
    else:
        classString = ""
    
    returnDict = {"Element" : elementString, "Type" : typeString, "Class" : classString}
    return returnDict

def isExactMatch(behemothArray, inputString):
    exactMatchBehemoth = []
    for idx, line in enumerate(behemothArray, start=0):
        if(line['BeheName'].lower() == inputString.lower()):
            exactMatchBehemoth.append(line)
            return exactMatchBehemoth
    
    return False

def fetchBehemothDB(name):
    try:
        connection = getconn()
        cursor = connection.cursor()
        sql = f"SELECT B.Name AS BeheName, B.Element as BeheElement, W.Type AS WepType, W.Tier AS WepTier, W.Ability AS WepAbility, A.Ability AS ArmourAbility FROM behemothtable AS B INNER JOIN weapontable AS W ON W.IdWeapon = B.IdWeapon_BehemothTable INNER JOIN armourtable AS A ON A.IdBehemoth_ArmourTable = B.IdBehemoth WHERE B.name_clean LIKE '%{name}%' GROUP BY B.IdBehemoth"
        cursor.execute(sql) 
        result = cursor.fetchall()

        return result
    finally:
        connection.close()

def fetchWeaponDB(name):
    try:
        connection = getconn()
        cursor = connection.cursor()
        sql = f"SELECT behemothtable.Name, behemothtable.Element, weapontable.Type, weapontable.Tier, weapontable.PhysAttack, weapontable.ElemAttack, weapontable.Ability, weapontable.Obs FROM behemothtable INNER JOIN weapontable ON weapontable.IdWeapon = behemothtable.IdWeapon_BehemothTable WHERE behemothtable.name_clean LIKE '%{name}%'"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    finally:
        connection.close()

def fetchArmorDB(name):
    try:
        connection = getconn()
        cursor = connection.cursor()
        sql = f"SELECT behemothtable.Name AS BeheName, behemothtable.Element AS BeheElement, armourtable.DefElement AS ArmorElement, armourtable.HpValue AS ArmorHP, armourtable.PhysDef AS ArmorPDef, armourtable.ElemDef AS ArmorEDef, armourtable.PhysAttack AS ArmorPAtk, armourtypelist.Name AS ArmorType, armourtable.Ability AS ArmorAbility, armourtable.Obs AS ArmorObs FROM behemothtable LEFT JOIN armourtable ON armourtable.IdBehemoth_ArmourTable = behemothtable.IdBehemoth LEFT JOIN armourtypelist ON armourtypelist.IdArmourTypeList = armourtable.IdArmourtype_ArmourTable WHERE behemothtable.name_clean LIKE '%{name}%'"
        cursor.execute(sql) 
        result = cursor.fetchall()
        return result
    finally:
        connection.close()

def fetchMagiDB(name):
    try:
        connection = getconn()
        cursor = connection.cursor()
        sql = f"SELECT magitable.Name, magitable.Cooldown, magitable.HealAmount, magitable.Description, magitable.Obs, magitypelist.Name FROM magitable INNER JOIN magitypelist ON magitypelist.IdMagiType = magitable.IdMagiType_MagiTable WHERE magitable.name_clean LIKE '%{name}%'"
        cursor.execute(sql) #this returns the amount of rows affected.
        result = cursor.fetchall()
        return result
    finally:
        connection.close()

def fetchIconLinkDB(beheName, default):
    try:
        connection = getconn()
        cursor = connection.cursor()
        sql = f"(SELECT imageLink FROM icontable WHERE behemothName = '{beheName}') UNION (SELECT imageLink FROM icontable WHERE behemothName = '{default}') LIMIT 1"
        cursor.execute(sql) 
        result = cursor.fetchall()
        return result[0]['imageLink']
    finally:
        connection.close()

def fetchBehemothByTypeDB(attributesArray):
    try:
        connection = getconn()
        cursor = connection.cursor()
        sql = f"SELECT B.Name AS BeheName, B.Element as BeheElement, W.Type AS WepType, W.Tier AS WepTier, W.Ability AS WepAbility, A.Ability AS ArmourAbility FROM behemothtable AS B INNER JOIN weapontable AS W ON W.IdWeapon = B.IdWeapon_BehemothTable INNER JOIN armourtable AS A ON A.IdBehemoth_ArmourTable = B.IdBehemoth WHERE W.Type LIKE '%{attributesArray['Class']}%' AND W.Tier LIKE '%{attributesArray['Type']}%' "
        
        if (attributesArray['Element']):
            sql += f"AND B.Element = '{attributesArray['Element']}' GROUP BY B.IdBehemoth"
        else: 
            sql += f"AND B.Element LIKE '%%' GROUP BY B.IdBehemoth"

        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    finally:
        connection.close()

def weaponEmbed(behemothWeaponArray):
    elementLink = getElementLink(behemothWeaponArray[0]['Element'])
    iconImage = fetchIconLinkDB(behemothWeaponArray[0]['Name'], "DefaultWeapon")

    embed = discord.Embed(title="Weapon Information:", colour=discord.Colour(getElementColor(behemothWeaponArray[0]['Element'])), description=f"{behemothWeaponArray[0]['Name']}")
    embed.set_footer(text="SS Behemoth", icon_url=f"{elementLink}")
    embed.set_thumbnail(url=f"{iconImage}")

    embed.add_field(name="Weapon Type:", value=f"{behemothWeaponArray[0]['Tier']} {behemothWeaponArray[0]['Type']}", inline=True)
    embed.add_field(name="Behemoth Element:", value=f"{behemothWeaponArray[0]['Element']}", inline=True)
    embed.add_field(name="Physical Attack:", value=f"{behemothWeaponArray[0]['PhysAttack']}", inline=True)
    embed.add_field(name="Elemental Attack:", value=f"{behemothWeaponArray[0]['ElemAttack']}", inline=True)
    embed.add_field(name="__Weapon Ability__: (Perfect Roll)", value=f"{behemothWeaponArray[0]['Ability']}", inline=False)

    if (behemothWeaponArray[0]['Obs'] != ''):
        embed.add_field(name="__Observation__:", value=f"{behemothWeaponArray[0]['Obs']}", inline=False)

    return embed

def armorEmbed(behemothArmorArray):
    iconImage = fetchIconLinkDB(behemothArmorArray[0]['BeheName'], "DefaultArmor")
    emojiString = getElementEmoji(behemothArmorArray[0]['ArmorElement'])
    elementLink = getElementLink(behemothArmorArray[0]['BeheElement'])

    embed = discord.Embed(title="Armor Information:", colour=discord.Colour(getElementColor(behemothArmorArray[0]['BeheElement'])), description=f"{behemothArmorArray[0]['BeheName']}") 
    embed.add_field(name="Elemental Defense:", value=f"{emojiString}", inline=True) 
    
    for row in behemothArmorArray:
        embed.add_field(name=f"{row['ArmorType']}:", value=f"HP: {row['ArmorHP']}  **|**  P.Defense: {row['ArmorPDef']}  **|**  E.Defense: {row['ArmorEDef']}  **|**  P.Attack: {row['ArmorPAtk']}", inline=False)

    embed.add_field(name="__Armour Ability__: (Perfect Roll)", value=f"{behemothArmorArray[0]['ArmorAbility']}", inline=False)

    if (behemothArmorArray[0]['ArmorObs'] != ''):
        embed.add_field(name="__Observation__:", value=f"{behemothArmorArray[0]['ArmorObs']}", inline=False)
        
    embed.set_footer(text="SS Behemoth", icon_url=f"{elementLink}")
    embed.set_thumbnail(url=f"{iconImage}")

    return embed

def magiEmbedGenerator(magiArray, inputString):
    isExactMatch = False
    if (len(magiArray) == 1):
        embed = singleMagiEmbed(magiArray)
    else:
        for row in magiArray:
            if inputString.lower() == row['Name'].lower():
                embed = singleMagiEmbed(magiArray)
                isExactMatch = True
        if isExactMatch == False:
            embed = magiListEmbed(magiArray, inputString)
                
    return embed

def behemothEmbedGenerator(behemothArray, inputString):
    behemothMatchArray = isExactMatch(behemothArray, inputString)
    
    if (behemothMatchArray != False):
        embed = singleBehemothEmbed(behemothMatchArray)
        return embed
    
    if (len(behemothArray) == 1):
        embed = singleBehemothEmbed(behemothArray)
    else:
        embed = behemothListEmbed(behemothArray, inputString)
          
    return embed

def singleMagiEmbed(magiArray):
    iconImage = fetchIconLinkDB(magiArray[0]['Name'], "DefaultMagi")
    elementLink = getElementLink(magiArray[0]['magitypelist.Name'])

    embed = discord.Embed(colour=discord.Colour(getElementColor(magiArray[0]['magitypelist.Name'])))
    embed.add_field(name="Magi Information:", value=f"{magiArray[0]['Name']}", inline=True)

    if (magiArray[0]['magitypelist.Name'] != 'Passive'):
        embed.add_field(name="Cooldown:", value=f"{magiArray[0]['Cooldown']}", inline=True)
    if (magiArray[0]['magitypelist.Name'] == 'Heal'):
        embed.add_field(name="Heal Amount:", value=f"{magiArray[0]['HealAmount']}", inline=True)

    embed.add_field(name="Description", value=f"{magiArray[0]['Description']}", inline=False)

    if (magiArray[0]['Obs'] != ''):
        embed.add_field(name="__Observation__:", value=f"{magiArray[0]['Obs']}", inline=False)

    embed.add_field(name="Magi Type:", value=f"{magiArray[0]['magitypelist.Name']}", inline=True)
        
    embed.set_footer(text="SS Magi", icon_url=f"{elementLink}") 
    embed.set_thumbnail(url=f"{iconImage}")                     

    return embed

def magiListEmbed(magiArray, userSearch):
    iconImage = fetchIconLinkDB("", "DefaultMagi")
    elementLink = getElementLink('List')

    embed = discord.Embed(colour=discord.Colour(getElementColor('List')))
    embed.add_field(name="Information:", value="The following magi match your request, input a complete name for specific information:", )

    for idx, line in enumerate(magiArray, start=1):
        embed.add_field(name=f"{idx} - Magi's Name: ", value=f"   \"{line['Name']}\" - **Type**: {line['magitypelist.Name']} magi", inline=False)
        
    embed.set_footer(text=f"You searched for: {userSearch}", icon_url=f"{elementLink}")
    embed.set_thumbnail(url=f"{iconImage}")                    

    return embed

def singleBehemothEmbed(behemothArray):
    elementLink = getElementLink(behemothArray[0]['BeheElement'])
    iconImage = fetchIconLinkDB(behemothArray[0]['BeheName'], "DefaultMonster")

    embed = discord.Embed(title="Behemoth Information:", colour=discord.Colour(getElementColor(behemothArray[0]['BeheElement'])), description=f"{behemothArray[0]['BeheName']}")
    embed.set_footer(text="SS Behemoth", icon_url=f"{elementLink}")
    embed.set_thumbnail(url=f"{iconImage}")
    
    embed.add_field(name="Weapon Type:", value=f"{behemothArray[0]['WepTier']} {behemothArray[0]['WepType']}", inline=True)
    embed.add_field(name="Behemoth Element:", value=f"{behemothArray[0]['BeheElement']}", inline=True)
    embed.add_field(name="__Weapon Ability__: (Perfect Roll)", value=f"{behemothArray[0]['WepAbility']}", inline=False)
    embed.add_field(name="__Armour Ability__: (Perfect Roll)", value=f"{behemothArray[0]['ArmourAbility']}", inline=False)

    return embed

def behemothListEmbed(behemothArray, userSearch):
    iconImage = fetchIconLinkDB("", "DefaultMonster")
    elementLink = getElementLink('List')

    embed = discord.Embed(colour=discord.Colour(getElementColor('List')))
    embed.add_field(name="Information:", value="The following behemoths match your request, input a complete name for specific information:", inline=False)

    for idx, line in enumerate(behemothArray, start=1):
        embed.add_field(name=f"{idx} - Behemoth's Name: ", value=f"   \"{line['BeheName']}\" - **Weapon Type**: {line['BeheElement']} {line['WepTier']} {line['WepType']}",inline=False)
        
    embed.set_footer(text=f"You searched for: {userSearch}", icon_url=f"{elementLink}")
    embed.set_thumbnail(url=f"{iconImage}")                    

    return embed
