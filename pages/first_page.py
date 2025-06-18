import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


st.set_page_config(
    page_title='Проект "Чаевые"',
    page_icon="💰",
    layout="centered"
)

# 0. Описываем проект
st.title('Данный проект показывает различные зависимости для чаевых в ресторане')

# 1. Читаем датасет tips.csv в переменную tips
tips = pd.read_csv('tips.csv', index_col=0)


# 2. Добавляем признак 'date_of_order', используя генератор date_range и рандомайзер np.random.choice
dates = pd.date_range(start='2023-01-01', end='2023-01-31')
np.random.seed(12)
tips['date_of_order'] = np.random.choice(dates, size=len(tips))
tips['date_of_order'] = tips['date_of_order'].dt.date

st.write('''
    #### 1. Ниже подробная **таблица** со всеми данными по чаевым за январь в нашем ресторане
''')
st.dataframe(tips)

# 3. Cтроим график показывающий динамику чаевых во времени.
fig_one = plt.figure(figsize=(12, 6), dpi=100)
sns.set_style("whitegrid")
sns.lineplot(data=tips, x='date_of_order', y='tip', color='r')
plt.title('The dynamics of tips over time')
plt.xlabel('Dates')
plt.ylabel('Tips, $')
plt.xticks(rotation=45)
plt.tight_layout()
plt.xticks(ticks=dates, ha='right')

st.write('''
        #### 2. Ниже график, показывающий средний размер чаевых, и трубу, \
        которая составляется максимальным и минимальным значением чаевых
''')
st.pyplot(fig_one)

# 4. Cтроим график показывающий динамику чаевых во времени, только relplot
fig_two = sns.relplot(data=tips, x='date_of_order', y='tip', color='r', height=6, aspect=2)
plt.title('The dynamics of tips over time')
plt.xlabel('Dates')
plt.ylabel('Tips, $')
plt.xticks(ticks=dates, rotation=45, ha='right')
plt.tight_layout()
plt.show()

st.write('''
        #### 3. Ниже график, показывающий все чаевых, нанесенные точкам.
        - **По оси X - даты**
        - **По оси Y - размер каждых чаевых
''')
st.pyplot(fig_two)

# 5. Рисуем гистограмму `total_bill`
fig_three = plt.figure(figsize=(12, 6), dpi=100)
sns.histplot(data=tips, x='date_of_order', y='total_bill', bins=31, kde=False, color='r')

plt.title('Distribution Total Bill')
plt.xlabel('Dates')
plt.xticks(ticks=dates, rotation=45, ha='right')
plt.ylabel('Total Bill ($)')
plt.tight_layout()

st.write('''
        #### 4. Ниже график показывает распределение всех чаевых c "температорой"
''')
st.pyplot(fig_three)


# 6. Рисуем scatterplot, показывающий связь между `total_bill` and `tip`
fig_four = plt.figure(figsize=(12, 6), dpi=100)
plt.title('Dependence of tips and total bills')
sns.scatterplot(data=tips, x='total_bill', y='tip', c='r')
plt.xlabel('Bill, $')
plt.ylabel('Tip, $')
plt.xticks(ticks=np.arange(0, 60, 5))

st.write('''
        #### 5. Ниже график показывает зависимость цены чека и размера чаевых
''')
st.pyplot(fig_four)


# 7. Рисуем аналогичный график, используя многофункциональный метод relplot
fig_five = sns.relplot(data=tips, x='total_bill', y='tip', color='r', height=5, aspect=2)
plt.title('Dependence of tips and total bills')
plt.xlabel('Bill, $')
plt.ylabel('Tip, $')
plt.xticks(ticks=np.arange(0, 60, 5))
plt.tight_layout()
plt.show()

st.write('''
        #### 6. Ниже график на вид такой же как график из п. 5, но построен методом `relplot`
''')
st.pyplot(fig_five)

# 8. Рисуем 1 график, связывающий `total_bill`, `tip`, и `size` одной функцией
fig_six = plt.figure(figsize=(12, 6), dpi=100)
sns.scatterplot(data=tips, x='total_bill', y='tip', size='size', hue='size', sizes=(50, 250))
plt.title('Dependence of tips and total bills')
plt.xlabel('Bill, $')
plt.ylabel('Tip, $')
plt.xticks(ticks=np.arange(0, 60, 5))
plt.tight_layout()

st.write('''
        #### 7. Данный график показывает зависимость между размером счета,\
        кол-вом гостей и размером чаевых
''')
st.pyplot(fig_six)

# 9. Покажем связь между днем недели и размером счета
total_bill_mean_per_day = tips.groupby('date_of_order')['total_bill'].mean().to_frame(name='mean_bill').reset_index()
total_bill_mean_per_day['Day of the week'] = pd.to_datetime(total_bill_mean_per_day['date_of_order']).dt.day_name()
fig_seven = plt.figure(figsize=(12, 6), dpi=100)
plt.title('Dependence of bill amount and day of the week', pad=10, fontsize=20)
sns.lineplot(data=total_bill_mean_per_day, x='date_of_order', y='mean_bill', marker='o', c='r')
plt.xticks(ticks=dates, rotation=45, ha='right')
plt.xlabel('Day of the week')
plt.ylabel('Average bill')
for x, y, label in zip(total_bill_mean_per_day['date_of_order'],
                       total_bill_mean_per_day['mean_bill'],
                       total_bill_mean_per_day['Day of the week']):
    plt.text(x, y, label, ha='left', va='top', fontsize=8, rotation=320)

st.write('''
        #### 8. Данный график показывает зависимость между размером чаевых\
        и днем недели
''')
st.pyplot(fig_seven)


#10. Нарисуем `scatter plot` с днем недели по оси Y, чаевыми по оси X, и цветом по полу
tips['Day of the week'] = pd.to_datetime(tips['date_of_order']).dt.day_name()
fig_eight = plt.figure(figsize=(12, 6), dpi=100)
plt.title('Dependence of tips and gender and days of the week')
sns.scatterplot(data=tips[tips['sex'] == 'Female'], x='tip', y='Day of the week', s=100, c='r', label='Female')
sns.scatterplot(data=tips[tips['sex'] == 'Male'], x='tip', y='Day of the week', c='b', s=100, label='Male')
plt.xlabel('Tips, $')
plt.xticks(ticks=np.arange(0, 12, 1))

st.write('''
        #### 9. Данный график показывает зависимость между размером чаевых,\
        днем недели и полом.
''')
st.pyplot(fig_eight)


#11. Нарисуем `box plot` c суммой всех счетов за каждый день, разбивая по `time` (Dinner/Lunch)
total_revenue_by_time_of_the_day = tips.groupby(['date_of_order', 'time'])['total_bill'].sum().reset_index()

fig_nine = plt.figure(figsize=(4, 4), dpi=100)
plt.title('Boxplot')
sns.boxplot(data=total_revenue_by_time_of_the_day, x='time', y='total_bill', palette='Set1', hue='time')
plt.xlabel('Time of the day')
plt.ylabel('Total bill')

st.write('''
        #### 9. Данный график показывает на примере `boxplot` динамику размера чеков от времени суток
''')
st.pyplot(fig_nine)


# 12. Построим аналогичный график используя многофункциональный метод [catplot]
fig_ten = sns.catplot(height=4, aspect=1, data=total_revenue_by_time_of_the_day, x='time', y='total_bill', palette='Set2', kind='box', hue='time')
plt.title('Catplot')
plt.xlabel('Time of the day')
plt.ylabel('Total bill')


st.write('''
        #### 10. Аналогичный график показывает на примере `boxplot` динамику размера чеков от времени суток, \
         но построенный метоедом `catplot`
''')
st.pyplot(fig_ten)


# 13. Нарисуем 2 гистограммы чаевых на обед и ланч. Расположим их рядом по горизонтали.
total_tips_by_time_of_the_day = tips.groupby(['date_of_order', 'time'])['tip'].sum().reset_index()
fig_eleven = sns.catplot(height=6, aspect=2, data=total_tips_by_time_of_the_day, x='date_of_order', y='tip', palette='Set1', kind='bar', hue='time')
plt.title('Catplot')
plt.xlabel('Dates')
plt.ylabel('Amount of tips')
plt.xticks(rotation=45, ha='right')

st.write('''
        #### 11. Данный график показывает разницу суммы чаевых от времени суток`
''')
st.pyplot(fig_eleven)


# 14. Нарисуем 2 scatterplots (для мужчин и женщин), показав связь размера счета и чаевых,
# дополнительно разбив по курящим/некурящим. Расположите их по горизонтали
fig_twelve = plt.figure(figsize=(12, 6), dpi=100)
plt.title('Men')
sns.scatterplot(data=tips[tips['sex'] == 'Male'], x='total_bill', y='tip', hue='smoker', s=80)


fig_thirteen = plt.figure(figsize=(12, 6), dpi=100)
plt.title('Women')
sns.scatterplot(data=tips[tips['sex'] == 'Female'], x='total_bill', y='tip', hue='smoker', s=80, palette={'Yes': 'red', 'No': 'green'})

st.write('''
        #### 12. Два графика ниже показывают связь размера счета и чаевых в зависимости от курящих и некурящих посетителей
''')
st.pyplot(fig_twelve)
st.pyplot(fig_thirteen)


# 15. Построим тепловую карту зависимостей численных переменных.
corr_matrix = tips[['total_bill', 'tip', 'size']].corr()

fig_fourteen = plt.figure(figsize=(8, 6), dpi=100)
plt.title('Dependencies of numerical variables')
sns.heatmap(data=corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)

st.write('''
        #### 13. Тепловая карта зависимостей численных переменных датасета **`tips`**
''')
st.pyplot(fig_fourteen)
