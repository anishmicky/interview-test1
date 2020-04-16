import json
import requests
import pytest

@pytest.fixture()
def resp_body():
    url = "https://samples.openweathermap.org/data/2.5/forecast/hourly"
    
    # Headers.
    headers = {
    'Cache-Control': "no-cache",
    'Postman-Token': "97adc087-2174-4b7b-8e90-3b3581dc7892"
    } 

    # Body
    querystring = {"q":"London,us","appid":"b6907d289e10d714a6e88b30761fae22"}
    
    response = requests.request("GET", url, headers=headers, params=querystring)       
    
    # Validate response headers and body contents
    print(response.status_code)
    assert response.status_code == 200

    resp_body = response.json()
    return resp_body

def test_data_days_count(resp_body):
	list1=[]
	for i in resp_body['list']:
		tempvar = i['dt_txt']
		list1.append(tempvar[:10])
	set1=set(list1)
	print("The response contains "+str(len(set1))+" days data")
	assert len(set1) == 4


def test_data_interval(resp_body):
	list2=[]
	list3=[]
	for i in resp_body["list"]:
		tempvar=i['dt_txt']
		#considering only hours of the time
		list2.append(tempvar[11:13])

	#converting a string list into intger list
	for k in range(0,len(list2)):
		list3.append(int(list2[k]))

	for l in range(0,len(list3)):
		if(l+1)!=len(list3):
			if(list3[l]==23):
				continue
			else:
				#Check if each item is hourly update
				assert list3[l+1]-list3[l]==1

def test_if_temp_in_range(resp_body):
	for i in resp_body['list']:
		for j in i["main"]:
			if(j=="temp"):
				temp=i["main"][j]
			if(j=="temp_min"):
				temp_min=i["main"][j]
			if(j=="temp_max"):
				temp_max=i["main"][j]
		
		assert temp>=temp_min and temp<=temp_max


def test_if_weathercode_is_500_then_light_rain(resp_body):
	for i in resp_body['list']:
		for j in i["weather"]:
			if(j["id"]==500):
				assert j["description"] == "light rain"


def test_if_weathercode_is_800_then_clear_sky(resp_body):
	for i in resp_body['list']:
	 	for j in i["weather"]:
	 		if(j["id"]==800):
	 			assert j["description"] == "clear sky"


#run file using pytest framework 
#Command: pytest -v inter_test.py