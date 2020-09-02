from AttendanceApp import app, databaseUpdater

if __name__=="__main__":
    app.run(debug=True)
    #databaseUpdater.update_database('logs_20200827-1619.csv')