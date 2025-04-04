import json, re

def getAllocatedTimes(allocatedTime):
        texts = []
        for item in allocatedTime:
            value = allocatedTime[item]
            if(value['checked']):
                texts.append(f"{item} : {value['start']} - {value['end']}")
        
        return ",".join(texts)

def scrape_JSON(text):
    # pattern = r"```json\n(.*?)\n```"
    # match = re.search(pattern, text, re.DOTALL)

    # if match:
    #     json_part = match.group(1)
    #     try:
    #         data = json.loads(json_part)
    #         return {"success" : True, "data" : data}
    #     except json.JSONDecodeError as e:
    #         return {"success" : False}
    # else:
    #     return {"success" : False}

    return json.loads(text)

from datetime import datetime, timedelta

def get_allocated_dates(start_date, end_date, schedule):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    allocated_dates = []

    
    current_date = start_date
    while current_date <= end_date:
        day_name = current_date.strftime("%A") 
        if day_name in schedule:
            day_info = schedule[day_name]
            if day_info['checked']:
                allocated_dates.append({
                    'date': current_date.strftime("%Y-%m-%d"),
                    'start': day_info['start'],
                    'end': day_info['end']
                })
        current_date += timedelta(days=1)

    return allocated_dates

