# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 11:54:37 2024

@author: kylab
"""


import json
from win32com.shell import shell, shellcon
import win32api,win32con
import sys
import pdfkit
from string import Template
import datetime
from getHRVPlot import getHRVPlot



def calculate_age(dtob_str):
    # Parse the string into a datetime object
    dtob = datetime.datetime.strptime(dtob_str, "%Y-%m-%d")
    
    # Get today's date
    today = datetime.datetime.today()
    
    # Calculate the age
    age = today.year - dtob.year - ((today.month, today.day) < (dtob.month, dtob.day))
    
    return age

# def getHRVreportbyDataID():

    
def main(ln):
    f = open(r'./report/json.txt', encoding = 'utf8')
    
    temp=f.read()
    f.close()
    try:
        report=json.loads(temp)
    except Exception as e:
        print(e)
        sys.exit(0)
    
    language={
        "0":"zh-TW",
        "1":"id"
    }
    
    current_language=language[ln]
    
    		# 定義一個字典來存儲所有中文和印尼文字符串
    strings = {
        "zh-TW": {
    				"HR_normal": "正常",
    				"HR_fast": "偏快",
    				"HR_slow": "偏慢",
    				"RRIV_abnormal": "異常",
    				"RRIV_normal": "正常",
    				"RMSSD_abnormal": "異常",
    				"RMSSD_normal": "正常",
    				"BMI_normal": "正常範圍",
    				"BMI_obese_severe": "重度肥胖",
    				"BMI_underweight": "體重過輕",
    				"BMI_overweight": "過重",
    				"BMI_obese_moderate": "中度肥胖",
    				"ANSAGE_old": "自律神經年齡提前老化",
    				"ANSAGE_young": "自律神經年齡年輕化",
    				"ANSAGE_same": "自律神經年齡相當同年齡者",
    				"ANS_no_data": "無資料",
    				"ANS_normal": "正常",
    				"ANS_slightly_high": "稍高",
    				"ANS_high": "過高",
    				"ANS_slightly_low": "稍低",
    				"ANS_low": "過低",
    				"SYM_normal": "正常",
    				"SYM_slightly_high": "稍高",
    				"SYM_high": "過高",
    				"SYM_slightly_low": "稍低",
    				"SYM_low": "過低",
    				"VAG_normal": "正常",
    				"VAG_slightly_high": "稍高",
    				"VAG_high": "過高",
    				"VAG_slightly_low": "稍低",
    				"VAG_low": "過低",
    				"SD_normal": "正常",
    				"SD_abnormal": "異常",
    				"SYM_modulation_normal": "正常",
    				"SYM_modulation_high": "偏高",
    				"SYM_modulation_low": "偏低",
    				"Balance_normal": "自律神經平衡",
    				"Balance_slightly_sympathetic": "輕微偏向交感",
    				"Balance_sympathetic": "偏向交感",
    				"Balance_slightly_parasympathetic": "輕微偏向副交感",
    				"Balance_parasympathetic": "偏向副交感"
     		},
     		"id": {
    				"HR_normal": "Normal",
    				"HR_fast": "Cenderung Cepat",
    				"HR_slow": "Cenderung Lambat",
    				"RRIV_abnormal": "Abnormal",
    				"RRIV_normal": "Normal",
    				"RMSSD_abnormal": "Abnormal",
    				"RMSSD_normal": "Normal",
    				"BMI_normal": "Rentang Normal",
    				"BMI_obese_severe": "Obesitas Berat",
    				"BMI_underweight": "Kekurangan Berat Badan",
    				"BMI_overweight": "Kelebihan Berat Badan",
    				"BMI_obese_moderate": "Obesitas Sedang",
    				"ANSAGE_old": "Usia Saraf Otonom Menua",
    				"ANSAGE_young": "Usia Saraf Otonom Lebih Muda",
    				"ANSAGE_same": "Usia Saraf Otonom Sama dengan Usia Sesungguhnya",
    				"ANS_no_data": "Tidak Ada Data",
    				"ANS_normal": "Normal",
    				"ANS_slightly_high": "Sedikit Tinggi",
    				"ANS_high": "Terlalu Tinggi",
    				"ANS_slightly_low": "Sedikit Rendah",
    				"ANS_low": "Terlalu Rendah",
    				"SYM_normal": "Normal",
    				"SYM_slightly_high": "Sedikit Tinggi",
    				"SYM_high": "Terlalu Tinggi",
    				"SYM_slightly_low": "Sedikit Rendah",
    				"SYM_low": "Terlalu Rendah",
    				"VAG_normal": "Normal",
    				"VAG_slightly_high": "Sedikit Tinggi",
    				"VAG_high": "Terlalu Tinggi",
    				"VAG_slightly_low": "Sedikit Rendah",
    				"VAG_low": "Terlalu Rendah",
    				"SD_normal": "Normal",
    				"SD_abnormal": "Abnormal",
    				"SYM_modulation_normal": "Normal",
    				"SYM_modulation_high": "Cenderung Tinggi",
    				"SYM_modulation_low": "Cenderung Rendah",
    				"Balance_normal": "Keseimbangan Saraf Otonom",
    				"Balance_slightly_sympathetic": "Sedikit Mencondong ke Simpatik",
    				"Balance_sympathetic": "Cenderung Simpatik",
    				"Balance_slightly_parasympathetic": "Sedikit Mencondong ke Parasimpatik",
    				"Balance_parasympathetic": "Cenderung Parasimpatik"
     			}
    		}
    
    
    
    		# 代碼中使用字典來替換字符串
    if float(report['HR']) < 100 and float(report['HR']) > 60:
        HR_d = strings[current_language]["HR_normal"]
    elif float(report['HR']) > 100:
        HR_d = strings[current_language]["HR_fast"]
    elif float(report['HR']) < 60:
        HR_d = strings[current_language]["HR_slow"]
      
    if float(report['RRIV']) < 15:
        RRIV_d = strings[current_language]["RRIV_abnormal"]
    else:
        RRIV_d = strings[current_language]["RRIV_normal"]
      
    if float(report['RMSSD']) < 20:
        RMSSD_d = strings[current_language]["RMSSD_abnormal"]
    else:
        RMSSD_d = strings[current_language]["RMSSD_normal"]
      
      
      
    
    dateFormatter = "%Y-%m-%d"
    try:
        actualAGE = calculate_age(report['Birthdate'])
        report['Age']=actualAGE
        
        try:
            if int(report['ANSAGE']) > actualAGE:
                ANSAGE_d = strings[current_language]["ANSAGE_old"]
            elif int(report['ANSAGE']) < actualAGE:
                ANSAGE_d = strings[current_language]["ANSAGE_young"]
            elif int(report['ANSAGE']) == actualAGE:
                ANSAGE_d = strings[current_language]["ANSAGE_same"]
        except:
            if report['ANSAGE'] == '>80' and actualAGE < 80:
                ANSAGE_d = strings[current_language]["ANSAGE_old"]
            elif report['ANSAGE'] == '<20' and actualAGE > 20:
                ANSAGE_d = strings[current_language]["ANSAGE_young"]
            elif (report['ANSAGE'] == '<20' and actualAGE < 20) or (report['ANSAGE'] == '>80' and actualAGE > 80):
                ANSAGE_d = strings[current_language]["ANSAGE_same"]
    except:
        print('123')
       	ANSAGE_d = strings[current_language]["ANS_no_data"]
      
    if float(report['ANS_SD']) < 1.5 and float(report['ANS_SD']) > -1.5:
        ANS_d = strings[current_language]["ANS_normal"]
    elif float(report['ANS_SD']) < 1.96 and float(report['ANS_SD']) >= 1.5:
        ANS_d = strings[current_language]["ANS_slightly_high"]
    elif float(report['ANS_SD']) >= 1.96:
        ANS_d = strings[current_language]["ANS_high"]
    elif float(report['ANS_SD']) > -1.96 and float(report['ANS_SD']) <= -1.5:
        ANS_d = strings[current_language]["ANS_slightly_low"]
    elif float(report['ANS_SD']) <= -1.96:
        ANS_d = strings[current_language]["ANS_low"]
        
    if float(report['SYM_SD']) < 1.5 and float(report['SYM_SD']) > -1.5:
        SYM_d = strings[current_language]["SYM_normal"]
    elif float(report['SYM_SD']) < 1.96 and float(report['SYM_SD']) >= 1.5:
        SYM_d = strings[current_language]["SYM_slightly_high"]
    elif float(report['SYM_SD']) >= 1.96:
        SYM_d = strings[current_language]["SYM_high"]
    elif float(report['SYM_SD']) > -1.96 and float(report['SYM_SD']) <= -1.5:
        SYM_d = strings[current_language]["SYM_slightly_low"]
    elif float(report['SYM_SD']) <= -1.96:
        SYM_d = strings[current_language]["SYM_low"]
    
    if float(report['VAG_SD']) < 1.5 and float(report['VAG_SD']) > -1.5:
        VAG_d = strings[current_language]["VAG_normal"]
    elif float(report['VAG_SD']) < 1.96 and float(report['VAG_SD']) >= 1.5:
        VAG_d = strings[current_language]["VAG_slightly_high"]
    elif float(report['VAG_SD']) >= 1.96:
        VAG_d = strings[current_language]["VAG_high"]
    elif float(report['VAG_SD']) > -1.96 and float(report['VAG_SD']) <= -1.5:
        VAG_d = strings[current_language]["VAG_slightly_low"]
    elif float(report['VAG_SD']) <= -1.96:
        VAG_d = strings[current_language]["VAG_low"]
      
    if float(report['SD']) < 100 and float(report['SD']) > 20:
        SD_d = strings[current_language]["SD_normal"]
    elif float(report['SD']) >= 100:
        SD_d = strings[current_language]["SD_abnormal"]
    elif float(report['SD']) < 20:
        SD_d = strings[current_language]["SD_abnormal"]
    
    if float(report['SYM_modulation']) < 1.5 and float(report['SYM_modulation']) > -1.5:
        SYM_modulation_d = strings[current_language]["SYM_modulation_normal"]
    elif float(report['SYM_modulation']) >= 1.5:
        SYM_modulation_d = strings[current_language]["SYM_modulation_high"]
    elif float(report['SYM_modulation']) <= -1.5:
        SYM_modulation_d = strings[current_language]["SYM_modulation_low"]
      
    if float(report['Balance']) < 0.8 and float(report['Balance']) > -0.8:
       	Balance_d = strings[current_language]["Balance_normal"]
    elif float(report['Balance']) < 1.5 and float(report['Balance']) >= 0.8:
       	Balance_d = strings[current_language]["Balance_slightly_sympathetic"]
    elif float(report['Balance']) >= 1.5:
       	Balance_d = strings[current_language]["Balance_sympathetic"]
    elif float(report['Balance']) > -1.5 and float(report['Balance']) <= -0.8:
       	Balance_d = strings[current_language]["Balance_slightly_parasympathetic"]
    elif float(report['Balance']) <= -1.5:
       	Balance_d = strings[current_language]["Balance_parasympathetic"]    
    # 		
    report_Discription={
    				#HRV table
    				'HR_d':HR_d,'RMSSD_d':RMSSD_d,'RRIV_d':RRIV_d,'ANSAGE_d':ANSAGE_d,'ANS_d':ANS_d,'SYM_d':SYM_d,
                    'VAG_d':VAG_d,'SDNN_d':SD_d,'SYM_modulation_d':SYM_modulation_d,
    				'Balance_d':Balance_d}
    
    
    		
    report.update(report_Discription)
    
    
    
    if current_language=="zh-TW":
        filename=report['datadate']
        report['datatime']=report['datadate'].split(' ')[1]
        report['datadate']=report['datadate'].split(' ')[0]
    else:
        filename=report['datadate']
    
    print(report['Age'])
    
    print(report)
    
    hrv_plotter = getHRVPlot()
    
    # Generate the Five Power Plot and get the plot data
    plot_data = hrv_plotter.getFivePowerPlot(heart=int(report['Heart']), fight=int(report['Fight']), vital=int(report['Vital']), 
                                             sex=int(report['Sex']), health=int(report['Health']))
    
    # Save the plot data as a PNG file
    with open('./report/static/img/five_power_plot.png', 'wb') as f:
        f.write(plot_data)
    
    # Generate the Tai Chi Plot and get the plot data
    taichi_data = hrv_plotter.getTaiChiPlot(ratio=float(report['ratio']), age=int(report['ANSAGE']))
    
    # Save the Tai Chi plot data as a PNG file
    with open('./report/static/img/taichi_plot.png', 'wb') as f:
        f.write(taichi_data)
    
    if current_language=='id': 
        filein=open("./report/report_id.html", encoding = 'utf8')
    elif current_language=='zh-TW': 
        filein=open("./report/report_goodday.html", encoding = 'utf8')
    
    src=Template(filein.read())
    
    
    #
    Html_file= open("./report/report_a.html","w", encoding = 'utf8')
    Html_file.write((src.substitute(report)))
    Html_file.close()
    config = pdfkit.configuration(wkhtmltopdf='wkhtmltopdf\\wkhtmltopdf.exe') #windows
    #config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    options = { 'disable-smart-shrinking': ''}
    MeaDatestr=filename.replace('/','').replace(' ','').replace(':','')
    pdfkit.from_file('./report/report_a.html','C:\hrvreport'+'\\'+report['userID']+MeaDatestr+'.pdf', configuration=config, options=options)
    
    return 'C:\hrvreport'+'\\'+report['userID']+MeaDatestr+'.pdf'
    

if __name__ == "__main__":
    print(main(sys.argv[1]))

