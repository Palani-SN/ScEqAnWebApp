from fastapi import FastAPI, Request
from Analysis import DynamicProgramAnalysis
app = FastAPI()


@app.post("/")
async def solutions(expression: Request):

    body = await expression.json()
    script = body["script"]
    try:
        result = DynamicProgramAnalysis(script).Run(Debug=False)
        status = True
    except:
        result = "script not correct"
        status = False

    return {"status": status, "OUT": result['OUT']}
