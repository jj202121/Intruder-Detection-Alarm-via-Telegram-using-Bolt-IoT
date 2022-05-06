import conf, json, time, math, statistics,requests
from boltiot import Bolt

def compute_bounds(history_data,frame_size,factor):
        if len(history_data)<frame_size :
                return None

        if len(history_data)>frame_size :
                del history_data[0:len(history_data)-frame_size]
        Mn=statistics.mean(history_data)
        Variance=0
        for data in history_data :
                Variance += math.pow((data-Mn),2)
        Zn = factor * math.sqrt(Variance / frame_size)
        High_bound = history_data[frame_size-1]+Zn
        Low_bound = history_data[frame_size-1]-Zn
        return [High_bound,Low_bound]

mybolt = Bolt(conf.API_KEY, conf.DEVICE_ID)

def send_telegram_message(message):
    """Sends message via Telegram"""
    url = "https://api.telegram.org/" + conf.telegram_bot_id + "/sendMessage"
    data = {
        "chat_id": conf.telegram_chat_id,
        "text": message
    }
    try:
        response = requests.request(
            "POST",
            url,
            params=data
        )
        print("This is the Telegram URL")
        print(url)
        print("This is the Telegram response")
        print(response.text)
        telegram_data = json.loads(response.text)
        return telegram_data["ok"]
    except Exception as e:
    print("An error occurred in sending the alert message via Telegram")
        print(e)
        return False
        
history_data=[]

while True:
        response = mybolt.analogRead('A0')
        data = json.loads(response)
        if data['success'] != 1:
                print("There was an error while retriving the data.")
                print("This is the error:"+data['value'])
                time.sleep(10)
                continue

        print ("This is the value "+data['value'])
        sensor_value=0
        try:
                sensor_value = int(data['value'])
        except e:
                print("There was an error while parsing the response: ",e)
                continue
                
        bound = compute_bounds(history_data,conf.FRAME_SIZE,conf.MUL_FACTOR)
        if not bound:
                required_data_count=conf.FRAME_SIZE-len(history_data)
                print("Not enough data to compute Z-score. Need ",required_data>
                history_data.append(int(data['value']))
                time.sleep(10)
                continue

        try:
                if sensor_value > bound[0] :
                        print ("The light level increased suddenly")
                        response = mybolt.digitalWrite('0','HIGH')
                        message = "Alert! Intruder detected"
                        telegram_status = send_telegram_message(message)
                        print("This is the telegram status:", telegram_status)
                elif sensor_value < bound[1]:
                        print ("The light level decreased suddenly")
                        response = mybolt.digitalWrite('0','HIGH')
                        message = "Alert! Intruder detected"
                        telegram_status = send_telegram_message(message)
                        print("This is the telegram status:", telegram_status)
                history_data.append(sensor_value);
        except Exception as e:
                print ("Error",e)
        time.sleep(10)

