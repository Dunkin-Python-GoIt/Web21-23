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
         "hashed_password": "$2b$12$jJi2emcE1WpfTB7WtC2AROE5kxfZ33Ul4AjgsTw/QK/egX/2qyXP2",
         "role": "admin"},
        {"username":"user",
         "hashed_password": "$2b$12$zm011VDvKRfMugnsEbDx7O8xY7HqtKrdRw1TClKVCqhKyIrLU9gWC",
         "role": "user"},
    ]
}



def get_db():
    return fake_dbs