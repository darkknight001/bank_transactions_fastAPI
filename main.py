from fastapi import  FastAPI

app = FastAPI()



@app.get('/')
def index():
    return {
            'data':{
                    'name': 'deepak',
                    'AccID': '45484531',
                    'bal': '45646.00'
                }
            }

@app.get('/about')
def about():
    return {
            'data':["test about"],
            'data2': "about 2"
    }