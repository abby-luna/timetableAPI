from fastapi import FastAPI
import getData
app = FastAPI()

@app.get("/timetable")
def timetable(src=None):
    if src==None:
        return {"Error: You must provide a source"}

    print(src)
    table = getData.Parse(src)
    table.readTables()
    return table.returnData()
