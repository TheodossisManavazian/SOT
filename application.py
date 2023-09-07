import config
from sot_service.routes import base_controller, ticker_controller, jaat_controller
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn

splash = """
  ______    ______  ________              ______   ________  _______   __     __  ______   ______   ________ 
 /      \  /      \|        \            /      \ |        \|       \ |  \   |  \|      \ /      \ |        
|  $$$$$$\|  $$$$$$\ \$$$$$$$$           |  $$$$$$\| $$$$$$$$| $$$$$$$\| $$   | $$ \$$$$$$|  $$$$$$\| $$$$$$$$
| $$___\$$| $$  | $$  | $$              | $$___\$$| $$__    | $$__| $$| $$   | $$  | $$  | $$   \$$| $$__    
 \$$    \ | $$  | $$  | $$               \$$    \ | $$  \   | $$    $$ \$$\ /  $$  | $$  | $$      | $$  \   
 _\$$$$$$\| $$  | $$  | $$               _\$$$$$$\| $$$$$   | $$$$$$$\  \$$\  $$   | $$  | $$   __ | $$$$$   
|  \__| $$| $$__/ $$  | $$              |  \__| $$| $$_____ | $$  | $$   \$$ $$   _| $$_ | $$__/  \| $$_____ 
 \$$    $$ \$$    $$  | $$ ______  ______\$$    $$| $$     \| $$  | $$    \$$$   |   $$ \ \$$    $$| $$     
  \$$$$$$   \$$$$$$    \$$|      \|       \$$$$$$  \$$$$$$$$ \$$   \$$     \$     \$$$$$$  \$$$$$$  \$$$$$$$$
                           \$$$$$$ \$$$$$$                                                                   
"""

app = FastAPI()

origins = [config.FAST_API_ORIGIN]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include controllers here
app.include_router(base_controller.router)
app.include_router(ticker_controller.router)
app.include_router(jaat_controller.router)


if __name__ == '__main__':
    print(f"{splash} \n application starting...")
    uvicorn.run("application:app", host='127.0.0.1', port=8000, log_level="info", reload=True)
