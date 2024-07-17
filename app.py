from flask import Flask,render_template, request
import pickle
import pandas as pd

filtered_top_50=pickle.load(open('filtered_top_50.pkl','rb'))
restro=pickle.load(open('restro.pkl','rb'))
new_df=pickle.load(open('new_df.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))

app = Flask(__name__) #Flask obj

@app.route('/')
def index():
    return render_template('index.html',
                           all_restro_names=list(restro['Name'].values),
                           restro_name=list(filtered_top_50['Name'].values),
                           area_name=list(filtered_top_50['Area'].values),
                           image_name=list(filtered_top_50['Image'].values),
                           cuisine_name=list(filtered_top_50['Cuisines'].values),
                           ratings=list(filtered_top_50['Dinner Ratings'].values),
                           cost=list(filtered_top_50['AverageCost'].values))

@app.route('/recommend',methods=['post'])
def recommend():
    user_input=request.form.get('user_input')
    area_index = new_df[new_df['Name'] == user_input].index[0]  # Getting index of the given area
    restro_df = restro.iloc[area_index]
    searchedRestro = []
    searchedRestro.append(restro_df['Name'])
    searchedRestro.append(restro_df['Area'])
    searchedRestro.append(restro_df['Cuisines'])
    searchedRestro.append(restro_df['Dinner Ratings'])
    searchedRestro.append(restro_df['AverageCost'])
    searchedRestro.append(restro_df['Image'])
    distances = similarity[area_index]
    area_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    data = []
    for i in area_list:
        item = []
        area_index = i[0]

        # Check if area_index is a valid index in new_df
        if area_index < len(new_df):
            temp_df = restro.iloc[area_index]

            item.append(temp_df['Name'])
            item.append(temp_df['Area'])
            item.append(temp_df['Cuisines'])
            item.append(temp_df['Dinner Ratings'])
            item.append(temp_df['AverageCost'])
            item.append(temp_df['Image'])
            data.append(item)
        else:
            print(f"Invalid index: {area_index}")
    print(data)
    return render_template('index.html',
                           all_restro_names=list(restro['Name'].values),
                           restro_name=list(filtered_top_50['Name'].values),
                           area_name=list(filtered_top_50['Area'].values),
                           image_name=list(filtered_top_50['Image'].values),
                           cuisine_name=list(filtered_top_50['Cuisines'].values),
                           ratings=list(filtered_top_50['Dinner Ratings'].values),
                           cost=list(filtered_top_50['AverageCost'].values),
                           data=data,
                           searched_restro=searchedRestro)



if __name__ == '__main__':
    app.run(debug=True)
