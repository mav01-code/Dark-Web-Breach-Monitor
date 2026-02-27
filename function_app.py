import azure.functions as func
import logging
import hashlib
import requests
import mysql.connector
import os

app = func.FunctionApp()

def get_connection():
    return mysql.connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"]
    )

@app.timer_trigger(schedule="0 */5 * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False)
def Monitor(myTimer: func.TimerRequest) -> None:

    logging.info("Breach Monitor started...")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT EMAIL, PASSWORD FROM CREDENTIALS")
    records = cursor.fetchall()

    headers = {"User-Agent": "AzureBreachMonitor"}
    breaches_found = 0
    credentials_checked = len(records)

    for email, stored_hash in records:
        first5 = stored_hash[:5]
        remaining = stored_hash[5:]

        response = requests.get(
            f"https://api.pwnedpasswords.com/range/{first5}",
            headers=headers
        )

        for line in response.text.splitlines():
            suffix, count = line.split(":")
            if suffix.upper() == remaining:
                logging.warning(f"BREACH FOUND for {email}")
                breaches_found += 1
                # Later: Send Notification Hub alert

    # Log monitoring activity
    cursor.execute("INSERT INTO MONITOR_LOGS (BREACHES_FOUND, CREDENTIALS_CHECKED) VALUES (%s, %s)", 
                   (breaches_found, credentials_checked))
    conn.commit()
    conn.close()
    logging.info(f"Breach Monitor completed. Checked: {credentials_checked}, Breaches: {breaches_found}")