import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
from dotenv import load_dotenv
import os

# # Configure logging
# logging.basicConfig(level=logging.INFO)

# # load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods including OPTIONS
    allow_headers=["*"],  # Allow all headers
)


def reduce_single(n):
    totl = 0
    for i in str(n):
        totl += int(i)

    return totl




num_mapping = {
"a" : 1, "i": 1, "j":1, "q":1 , "y":1,
"b" : 2 , "k": 2, "r": 2,
"c" : 3, "g":3 , "l": 3, "s":3,
"d" : 4, "m" :4,  "t":4,
"e" : 5 , "h":5, "n":5 , "x":5,
"o" : 7, "z": 7,
"u" : 6 , "v":6 , "w": 6,
"f" : 8, "p": 8
}


gb_mb_mapping = {
    1 : [1,3,5,7,9],
    2 : [1,2,4,8],
    3 : [2,3,5,7,9],
    4 : [1,3,4,6] ,
    5 : [2,4,5,7,9] ,
    6 : [1,2,3,5,6,7],
    7 : [2,4,6,7,9] ,
    8 : [1,3,4,5,7,8] ,
    9: [2,4,6,8,9]
}



# inp = "arbaz ali"


def calcul(inp):
    total = 0
    name_dig = []
    for i in inp.lower():
        if i in num_mapping:
            var = num_mapping[i]
            name_dig.append((i, var))
            total += var

    print(total)

    if (len(str(total))) > 1:

        s= reduce_single(total)
        print(s)

        if s in gb_mb_mapping:
            ma = gb_mb_mapping[s]
            print(ma)
            print(name_dig)

            return total ,s, ma, name_dig


@app.get("/")
def home():
    return {"message": "Adad API is running"}

re = None

@app.get("/calculate_name")
async def calculate_name(request: Request):

    try:
        data = await request.json()
        name = data.get('name')
        re = calcul(name)

        if re:
            total_of_name, single_digit_number, maglub_numbers, alphabets_and_numbers = re
            response_data = {
                "total_of_name": total_of_name,
                "single_digit_number": single_digit_number,
                "maglub_numbers": maglub_numbers,
                "alphabets_and_numbers": [{pair[0]:  pair[1]} for pair in alphabets_and_numbers]
            }
            return JSONResponse(content=response_data)
        else:
            return JSONResponse(content={"error": "Invalid input or calculation failed"}, status_code=400)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)




# s= calcul(inp)
# print(s)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)
