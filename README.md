CourseSnipe
==================
A CLI utility, written in Python, which allows you to monitor courses and enroll automatically through REM. 

Many improvements over similar tools have been made in CourseSnipe. By checking VSB for availablity instead of REM, the interval between requests can be reduced several times over. In essence, this means that your chances of finding a seat in a given section can increased quite dramatically, depending on your risk tolerance. Also, because of the greatly reduced interval, monitoring multiple courses at once is not only feasible but practical. The session data is saved, so you don't have to reauthenticate with Duo every time you restart the script. 


## Getting Started

1. Install the module via pip

```shell script
$ pip install CourseSnipe
```

2. Set your username and password

```shell script
$ csnipe set-user USERNAME
$ csnipe set-pass
```

3. Add your desired course(s), where CATALOGUE_NUMBER is the catalogue number of the course you want to add 

```shell script
$ csnipe add CATALOGUE_NUMBER
```

4. Run CourseSnipe to begin active monitoring

```shell script
$ csnipe run
```

The first time you run this script, you will have to authenticate with Duo. Afterwards, this will not be necessary.

## Additional Commands

To remove a course from the list of monitored courses, do:

```shell script
$ csnipe remove CATALOGUE_NUMBER
```

To add a transfer into a given section, do:

```shell script
$ csnipe transfer CATALOGUE_NUMBER
```

To view your monitored courses, do:

```shell script
$ csnipe list
```

If you don't want to see the browser when running CourseSnipe, do:

```shell script
$ csnipe run -h
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
