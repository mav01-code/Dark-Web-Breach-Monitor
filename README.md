## Dark Web Breach Monitor

### Problem Overview
Create a monitoring dashboard that leverages breach APIs like Have I Been Pwned to alert users the moment their credentials appear in any new database leak.

### Tech Stack
1) Backend & API - Flask
2) API Testing - Postman
3) Frontend - HTML, CSS
4) Real-time Monitoring - Azure Functions and line plot
5) API Integration (for data breach DB) - Have I Been Pwned?

### High Level Architecture
- Flow:
    - Register
    - Login
    - Dashboard
        - Credential Check
        - Real Time Monitoring
        - Remediation Recommendation

### Low-Level Architecture
- Monolithic Architecture - 1 DB, 1 server
- Flow:
    - User registers -> stored in register table of monitor DB using '/register' API endpoint
    - User logins -> checked from register table using '/login' API endpoint
    - Dashboard -> 
        - Credential Check (Found in breach or not) ->
            - Hash the password using SHA1
            - If the email in the session is not in table, store the hashed pass in credential table
            - Check the API using first 5 digits of hexa decimal formatted string
            - Out of the returned strings of digits, check for the remaining characters
                - If match -> Found in data breach
                - Else -> Safe
        - Real-time Monitoring
            - Using Azure Function app to create a cron job that triggers the credential table every 5 mins
            - Plot a line graph based on the monitoring logs
        - Remediation Recommendation
            - Rule based score
                - If the breach count is greater than zero, score gets updated by 45
                - If the password age is greater than or equal to 90, score is updated by 25
                - If the password age is greater than or equal to 60, score is updated by 15
                - If there is no multi factor authentication, score is updated by 30
                - If the score is greater than or equal to 70, the risk level is high
                - If the score is greater than or equal to 40, the risk level is medium
                - Else it's low

