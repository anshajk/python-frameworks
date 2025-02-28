from fastapi import FastAPI, Depends

app = FastAPI()


def common_dependency():
    return "Common Dependency Result"


@app.get("/dependency")
def use_dependency(data: str = Depends(common_dependency)):
    return {"data": data}
