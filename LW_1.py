import random
import pandas as pd
from datetime import datetime, timedelta
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox

m_names = [str(i).replace("\n", "") for i in (open('names.txt', 'r', encoding='utf-8').readlines())]
m_surnames = [str(i).replace("\n", "") for i in open('surnames.txt', 'r', encoding='utf-8').readlines()]
m_patronymics = [str(i).replace("\n", "") for i in open('patronymics.txt', 'r', encoding='utf-8').readlines()]

w_names = [str(i).replace("\n", "") for i in open('names_w.txt', 'r', encoding='utf-8').readlines()]
w_surnames = [str(i).replace("\n", "") for i in open('surnames_w.txt', 'r', encoding='utf-8').readlines()]
w_patronymics = [str(i).replace("\n", "") for i in open('patronymics_w.txt', 'r', encoding='utf-8').readlines()]

doctors = [str(i).replace("\n", "") for i in open('doctors.txt', 'r', encoding='utf-8').readlines()]
analyzes = open('analyzes.txt', 'r', encoding='utf-8').readlines()
symptoms = open('symptoms.txt', 'r', encoding='utf-8').readlines()

for i in range(50):
    analyzes[i] = analyzes[i].replace("\n", "").split(',')
    symptoms[i] = symptoms[i].replace("\n", "").split(',')

years = []
for i in range(100):
    if i < 24 and i >= 10:
        years.append(str(i))
    if i < 10:
        years.append('0'+str(i))
    if i > 79:
        years.append(str(i))
        
used_pasp = []
used_snils = []

def snilsGenerator():
    snils_format = '{Num1}-{Num2}-{Num3} {Num4}'

    nums = {
        'Num1': str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)),
        'Num2': str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)),
        'Num3': str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)),
        'Num4': str(random.randint(0, 9)) + str(random.randint(0, 9))
    }

    return snils_format.format(**nums)

def passGenerator(nat):
    if nat == 'Rus':
        num_part = str(random.randint(0, 8)) + str(random.randint(0, 9)) + str(random.choices(years)[0])
        random_part = ''.join(str(random.randint(0, 9)) for _ in range(6))
        return f"{num_part} {random_part}"
    elif nat == 'Bel':
        prefix = str(random.choices(['AB', 'BM', 'HB', 'KH', 'MC', 'KБ', 'ПП'])[0])
        random_part = ''.join(str(random.randint(0, 9)) for _ in range(7))
        return f"{prefix} {random_part}"
    elif nat == 'Kz':
        num_part = 'N' + ''.join(str(random.randint(0, 9)) for _ in range(8))
        return num_part

def ccGenerator(pay_system, bank):
    card_format = '{fig} {fig2} {fig3} {fig4}'

    system_figures = {
        'Мир': {
            'Сбербанк': '2202',
            'Тинькофф': '2200',
            'Россельхоз-Банк': '2200',
            'default': '2202'
        },
        'MasterCard': {
            'Сбербанк': '5469',
            'Тинькофф': '5489',
            'Россельхоз-Банк': '5443',
            'default': '5406'
        },
        'default': {
            'Сбербанк': '4276',
            'Тинькофф': '4277',
            'Россельхоз-Банк': '4272',
            'default': '4279'
        }
    }

    figures = system_figures.get(pay_system, system_figures['default']).get(bank, system_figures['default']['default'])

    argz = {'fig': figures, 
            'fig2': str(random.randint(1000, 9999)), 
            'fig3': str(random.randint(1000, 9999)), 
            'fig4': str(random.randint(1000, 9999))}

    return card_format.format(**argz)

def names(gender):
    if gender == 'M':
        return random.choice(m_surnames) + " " + random.choice(m_names) + " " + random.choice(m_patronymics)
    else:
        return random.choice(w_surnames) + " " + random.choice(w_names) + " " + random.choice(w_patronymics)
    
def get_time():
    iso_format = "{Year}-{Month}-{Day}T{Hour}:{Minute}+{Offset}"

    year_range = ["2020", "2021", "2022", "2023"]
    month_range = ["01","02","03","04","05","06","07","08","09","10","11","12"]
    day_range = [str(i).zfill(2) for i in range(1,29)]
    hour_range = [str(i).zfill(2) for i in range(8,21)]
    min_range = [str(i).zfill(2) for i in range(0,60)]
    offset = ["03:00"]
    
    argz = {"Year": random.choice(year_range),
            "Month": random.choice(month_range),
            "Day" : random.choice(day_range),
            "Hour": random.choice(hour_range),
            "Minute": random.choice(min_range),
            "Offset": random.choice(offset)
            }
    return iso_format.format(**argz)

def datasetGenerator(MC, Visa, Mir, Sb, Tk, RosSel, Alp):
    df = pd.DataFrame({'ФИО':[], 'Паспортные данные':[], 'СНИЛС':[], 'Симптомы':[], 'Выбор врача':[], 
                       'Дата посещения врача':[], 'Анализы':[], 'Дата получения анализов':[], 
                       'Стоимость анализов':[], 'Карта оплаты':[]})
    
    for i in range(1000):
        gender = random.choices(['M', 'F'])[0]
        nat = random.choices(['Rus', 'Bel', 'Kz'])[0]
        bank = random.choices(['Сбербанк', 'Тинькофф', 'Россельхоз-Банк', 'Альфа'], weights = [Sb, Tk, RosSel, Alp])[0]
        pay_system = random.choices(['Мир', 'MasterCard', 'Visa'], weights = [Mir, MC, Visa])[0]
        analyze_cost = random.randint(1000, 9999)
        snils = snilsGenerator()
        passport = passGenerator(nat)
        
        while snils in used_snils:
            snils = snilsGenerator()
        used_snils.append(snils)
        
        while passport in used_pasp:
            passport = passGenerator(nat)
        used_pasp.append(passport)
        
        num = random.randint(0, 49)

        symps = str(symptoms[num][0])
        ans = str(analyzes[num][0])

        for i in range(random.choices(range(5))[0]):
            n = random.randint(0, 49)
            symps += ", " + str(random.choices(symptoms[n])[0])
            ans += ", " + str(random.choices(analyzes[n])[0])

        time = get_time()
        time_new = (datetime.fromisoformat(time) + timedelta(hours=random.choices([24,48,72])[0])).isoformat()


        df.loc[len(df.index)] = [names(gender), passport, snils, symps, doctors[num].replace("\n",""), 
                               time, ans, time_new, analyze_cost, ccGenerator(pay_system, bank)]

    df.to_excel('dataset.xlsx', index=False)

#GUI

def clicked():   
    if ((int(combo1.get()) + int(combo2.get()) + int(combo3.get())) != 100) or ((int(combo4.get()) + int(combo5.get()) + int(combo6.get()) + int(combo7.get())) != 100):
        messagebox.showinfo('Ошибка', 'Сумма в процентах не равна 100')    
    else:
        datasetGenerator(int(combo1.get()), int(combo2.get()), int(combo3.get()), int(combo4.get()), 
                    int(combo5.get()), int(combo6.get()), int(combo7.get()))
        messagebox.showinfo('Готово', 'Генерация датасета завершена')
        
window = Tk()
window.title("Генератор датасетов")
window.geometry('700x500')

lbl = Label(window, text="Добрый день!", font='Consolas 16 bold')  
lbl.place(relx=0.5, rely=0.1, anchor=CENTER)

lbl2 = Label(window, text="Перед началом работы выберите необходимые параметры генерации:", font='Consolas 12')  
lbl2.place(relx=0.5, rely=0.17, anchor=CENTER)

lbl3 = Label(window, text="Платежная система:", font='Consolas 11')
lbl3.place(relx=0.5, rely=0.25, anchor=CENTER)

t1 = Label(window, text="MasterCard, %")
t1.place(relx=0.044, rely=0.3)

t2 = Label(window, text="Visa, %")
t2.place(relx=0.44, rely=0.3)

t3 = Label(window, text="Мир, %")
t3.place(relx=0.79, rely=0.3)

combo1 = Combobox(window, width=10)  
combo1['values'] = (10, 20, 30, 40, 50, 60, 70, 80)  
combo1.current(3) 
combo1.place(relx=0.05, rely=0.37)


combo2 = Combobox(window, width=10)  
combo2['values'] = (10, 20, 30, 40, 50, 60, 70, 80)  
combo2.current(3) 
combo2.place(relx=0.4, rely=0.37)

combo3 = Combobox(window, width=10)  
combo3['values'] = (10, 20, 30, 40, 50, 60, 70, 80)  
combo3.current(1) 
combo3.place(relx=0.75, rely=0.37)

lbl4 = Label(window, text="Банк:", font='Consolas 11')
lbl4.place(relx=0.5, rely=0.5, anchor=CENTER)

t4 = Label(window, text="Сбербанк, %")
t4.place(relx=0.044, rely=0.57)

t5 = Label(window, text="Тинькофф, %")
t5.place(relx=0.3, rely=0.57)

t6 = Label(window, text="Альфа-банк, %")
t6.place(relx=0.53, rely=0.57)

t7 = Label(window, text="Россельхоз-Банк, %")
t7.place(relx=0.75, rely=0.57)

combo4 = Combobox(window, width=10)  
combo4['values'] = (10, 20, 30, 40, 50, 60, 70)  
combo4.current(2) 
combo4.place(relx=0.05, rely=0.65)

combo5 = Combobox(window, width=10)  
combo5['values'] = (10, 20, 30, 40, 50, 60, 70)  
combo5.current(2) 
combo5.place(relx=0.3, rely=0.65)

combo6 = Combobox(window, width=10)  
combo6['values'] = (10, 20, 30, 40, 50, 60, 70)  
combo6.current(2) 
combo6.place(relx=0.53, rely=0.65)

combo7 = Combobox(window, width=10)  
combo7['values'] = (10, 20, 30, 40, 50, 60, 70)  
combo7.current(0) 
combo7.place(relx=0.75, rely=0.65)

btn = Button(window, text="Сгенерировать датасет", command=clicked)
btn.place(relx=0.95, rely=0.95, anchor="se", width=180) 

window.mainloop()