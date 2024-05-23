fake_dbs = {
    "cars":[
        {"id": 1,
        "brand": "BMW", 
        "model": "5 series"
        },
        {"id": 2,
        "brand": "Mercedes", 
        "model": "CLK"
        }
    ],
    "users": [
        {"username":"admin",
         "hashed_password": "weqrwwetueruyr",
         "role": "admin"},
        {"username":"user",
         "hashed_password": "popgodglg;gl;g",
         "role": "user"},
    ]
}



def get_db():
    return fake_dbs