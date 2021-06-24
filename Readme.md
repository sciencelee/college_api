# College Recommendation API
The purpose of this project is to serve as a backend api for the webapp at www.collegereco.com.  The front end application is the work of Roman Turner https://github.com/RomanTurner/college-rec

![Find alternative colleges based on your current choices](static/college.jpg)

## Background
The hackathon was focused on developers from different ares focusing on working together to solve a problem.  I partnered with a software developer who used the API created here to feed the app front end (ReactJS)

The idea was born from my own experience teaching high school Juniors/Seniors who obsessed over adjusting filters on Collge Board and other sites to find comparable colleges.  My students typically applied to more than 10 schools.  It was an experience for students to find 10 schools they would be happy attending.  This application is intened to offer some guidance on that front.

The project allows a user to choose three colleges (Reach/Target/Safety) and receive other recommendations for colleges you may wish to explore.

I also wrote a blog concerning the creation of the flask API.
https://levelup.gitconnected.com/making-a-restful-api-with-python-and-flask-13483c2556b


## Web app
The MVP for this project can be found at www.collegereco.com.

The hackathon was two days long.  CSS and UI is not final, but we hope to get back soon to make it beautiful.

## Content of this repository
- Flask app
    - app.py - main file with all routes for API
    - requirements.txt 
    - Procfile (as required by Heroku)
    - static folder
        - df_final_names.pkl - pickle contains names and original info from College Scorecard
        - scaled_df.pkl - stripped down to 200+ features with min max scaling for model.

- Recommendation model - I chose to just leave the ipynb in the static folder with the app.  In a larger app, I would have made a separate repo.
    - static folder
        - college_rec.ipynb. - feature selection generates pickle files

## Data
The original data is from [College Scorecard](https://data.ed.gov/dataset/college-scorecard-all-data-files-through-6-2020/resources).

There are more than 2000 features available for each college.  Most are not likely ones that would be of interest to a typical student.  The features selected were focused on the following:
- location of the school (state and region)
- ACT/SAT for entry
- Perecentage of students in each college/discipline/major
- Acceptance rate
- Pell grant scholarship rate
- Tuition
- Undergrad population
- School focus
- School size
- Urban vs rural (city size)
- Men/women only
- HBCU
- Religious affiliation

The chosen features have a dramatic affect on the output of the model.  It would be wise to go back and study the effects and chosen features to eliminate bias.

## Recommendation Model
I built a simple content based rec system.  The recommender simply finds a close match using the features and the euclidean distance to find the most similar schools to the input.  I got similiar results with Minkowski distance formula.

I looked at the top 10 recommedations for each user selected school.  If the school matched more than one of the user input schools, I gave priority to that recommenation. Otherwise, I returned the top one or two recommendations for each school.

## The API
The backend RESTful API which serves up the model results to the frontend is written in Flask.  
The API is hosted on Heroku at https://college-rec-system.herokuapp.com/
It has a two routes/endpoints:

`/colleges/` : This endpoint uses the GET method to send a list of all colleges contained in the model.  The frontend grabs the colleges on load so that we are working from the same array of schools.

`/model/` :  This endpoint uses POST method.  The frontend sends in JSON containing three schools in format 
```
[
      {
        'dream':'Loyola University Chicago',
        'target':'DePaul University',
        'safety':'University of Illinois at Urbana-Champaign'
      },
]
```
and returns five schools in the following format:
```
{
 "results":[
     {"admission_rate":0.3895,"avg_tuition":60619.0,"city":"Waco","schoolname":"Baylor     
          University","state":"TX","student_pop":14159.0,"url":"www.baylor.edu"},  
     {"admission_rate":0.4602,"avg_tuition":67393.0,"city":"Bronx","schoolname":"Fordham 
          University","state":"NY","student_pop":9392.0,"url":"www.fordham.edu"},
     {"admission_rate":0.8118,"avg_tuition":41961.0,"city":"Philadelphia","schoolname":"La Salle 
          University","state":"PA","student_pop":3766.0,"url":"www.lasalle.edu"},
     {"admission_rate":0.8675,"avg_tuition":42413.0,"city":"Chicago","schoolname":"Columbia College 
          Chicago","state":"IL","student_pop":6496.0,"url":"www.colum.edu"},
     {"admission_rate":0.5649,"avg_tuition":36048.0,"city":"University Park","schoolname":"Pennsylvania State 
          University-Main Campus","state":"PA","student_pop":40108.0,"url":"www.psu.edu/"}
    ]
}

```


The API uses CORS preflight to validate the response.

## Future work
This model is overly simplistic as written.  I would like to do a collaborative recommendation system which would require access to student choices or applications to select colleges.  Students who were interested in Yale, would probably be interested in Harvard as well.  


The CSS and UI needs to be addressed to move this from being an interesting MVP to a useful tool for students.


```python

```
