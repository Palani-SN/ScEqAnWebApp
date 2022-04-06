# LogExAnWebApp (Logical Expression Analysis Web Applications)

- A Solver for finding worst case values of any mathematical equation f(x, ..,z) with respect to x, ..,z.
- Check out the example code in repo ( https://github.com/Palani-SN/ScEqAnWebApp ) for reference
- ScEqAn Script Syntax reference

![](https://github.com/Palani-SN/ScEqAnWebApp/blob/main/SyntaxReference.JPG?raw=true)
 
- **Note : For the usage bath front end and back end should be running at the same time.**

## API (Rest API service using fast API)

- run the script using the command **uvicorn backend:app** in path **fast_api/**

- get results in the form of JSON (refer the Schema.jsonrc)
  - METHOD : POST
  - URL :  localhost:8000
  - REQUEST : 
```json
{
    "script": "[A] = 3.14 * r{2.0, 7.0} * r;\n[C] = 2 * 3.14 * r;"
}
```                                                                                    
  - RESPONSE : 
```json
{
    "status": true,
    "OUT": [
        {
            "VAR": "A",
            "MAX": 153.86,
            "MIN": 12.56,
            "IN": [
                {
                    "VAR": "r",
                    "MAX": 7.0,
                    "MIN": 2.0
                }
            ]
        },
        {
            "VAR": "C",
            "MAX": 43.96,
            "MIN": 12.56,
            "IN": [
                {
                    "VAR": "r",
                    "MAX": 7.0,
                    "MIN": 2.0
                }
            ]
        }
    ]
}
```

## UI (frontend service using react)

- run the script using the command **npm start** in path **react_ui/**
- enter the expression in the text box shown in **http://localhost:3000/**

![](https://github.com/Palani-SN/ScEqAnWebApp/blob/main/InputExample.JPG?raw=true)

- click find to get the results as shown below

![](https://github.com/Palani-SN/ScEqAnWebApp/blob/main/OutputImage.JPG?raw=true)

- Export the plots as PDF/JPEG/PNG etc..




