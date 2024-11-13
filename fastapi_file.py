from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import subprocess

app = FastAPI()
scheduler = BackgroundScheduler()
scheduler.start()

def scraping_task():
    try:
        result = subprocess.run(['python', 'scraper.py'], 
                              capture_output=True, 
                              text=True,
                              check=True)
        
        print(f"Scraping executed at: {datetime.now()}")
        print(f"Output: {result.stdout}")
        
        return {
            "status": "success",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "output": result.stdout
        }
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return {
            "status": "error",
            "error": e.stderr
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }

@app.get("/scrape")
async def start_scraping():
    scheduler.remove_all_jobs()
    
    scheduler.add_job(
        scraping_task,
        'interval',
        hours=2,
        id='scraping_job',
        next_run_time=datetime.now()
    )
    
    return {
        "message": "Scraping scheduled",
        "frequency": "Every 2 hours",
        "first_run": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }