# webcsv: Simple CSV Web Viewer

Simple python app to view CSV files on the browser. The CSV data will be rendered with an HTML table. This app uses Flask & Runapp\<Gunicorn\> (ryt/runapp) for Deployment.

## Test/Development Instructions

Run the app with the default Flask development server on port 5000.

```
$ python3 webcsv.py
```

## Deployment Instructions
Create & start a deployment, gunicorn (daemon/process), with app:

```
$ cd webcsv
$ ./runapp start
```

Stop deployment/app process:

```
$ ./runapp stop
```

Check running deployment/app process:

```
$ ./runapp list
```

Restart deployment/app process:

```
$ ./runapp restart
```

If app is not running after restart, check & re-deploy:

```
$ ./runapp list
$ ./runapp start
```

--

<small>Copyright &copy; 2024 Ray Mentose.</small>

