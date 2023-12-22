CourseSnipe
==================
A CLI utility, written in Python, which allows you to monitor courses and enroll automatically through REM.

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



## Additional Commands

To remove a course, do:

```shell script
$ csnipe remove CATALOGUE_NUMBER
```


To view your monitored courses, do:

```shell script
$ csnipe list
```


If you don't want to see a browser, do:

```shell script
$ csnipe run -h
```


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

