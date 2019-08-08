# zosia16-site
Django 2.2 version of ZOSIA registration page.

## Development

The preferred approach is to use *docker* for development. And don't worry, we try to keep it as
 easy as possible. Of course, if you're really not into containerisation, you can try running it
 without docker, but you may find it harder to debug OS related bugs. Besides, on production site
 we run this application in docker, so it's better to keep your development process similar to the 
 production one.

### Local development (without docker)
[Moved here](local_development.md)

### Full in-docker local development

#### Required software:

To run docker container you obviously need to have *Docker (Community Edition)* installed.

Additionally, you should install `docker-compose` using APT on Debian-based systems:
```
sudo apt install docker-ce docker-compose
```
 or using PIP:
```
pip install docker-compose
```

#### How can I run it?

To keep things simple we've written `dev.sh` script that will run everything for you.
 You simply have to type `./dev.sh one_click`. No root permissions are needed. All commands used 
 with the script are listed under `./dev.sh help`.

#### I have run it - what is happening?

First, script needs to build the docker image. This process uses local cache, so it takes time
 at the first run only, because docker has to pull `python` image and build every layer.
 Then two containers have started: `zosia_db_1` with Postgres database and `zosia_web_1` with our 
 web application.

We mount some local folders so as to let you develop application without rebuilding docker every 
time:
- `./app/src` as `/code/src`
- `./app/js` as `/code/js`
- `./app/static` as `/code/static`

Thanks to this, all changes you make in the code will be visible immediately inside the container.
 **Remember that it's working in both directions!** Every change you'll make in the container
 will affect your local files (from the listed folders), because these are the same files, of 
 course :P

We tried to avoid side effects in our `dev.sh` script, but sometimes it can't be achieved easily.
 Some commands may create files inside listed folders. This files will be owned by `root`,
 because they were created inside docker. You don't have to worry about them, we listed them in the
 `gitignore` list, so they shouldn't appear in `git status`.

Some of the files we create in listed folders are outputs of webpack build system (js, css files). Fortunately all
node modules that our application needs exist only inside of docker. If you want to rebuild js application, you
should run webpack inside the container using `./dev.sh js_build` for one time build or `./dev.sh js_watch` for incremental
builds on source code change. Those commands will run webpack that will use files form `./app/js` and node modules to
build minified js and css files in `./app/static` directory.

Next, we run migrations on database and, finally, start the web server. In terminal you will 
 see output/logs from django (e.g. queries to the database).

You can shut this server down anytime by clicking `CTRL+C`, but containers will be still alive.
 If you want to shut them down as well, you need to run `./dev.sh shutdown` command. And if you want
 to start the web server again, just run `./dev.sh runserver`.

### Troubleshooting

```
Creating network "zosia_default" with the default driver
ERROR: could not find an available, non-overlapping IPv4 address pool among the defaults to assign to the network
```

This error can appear during `docker-compose up` command if you have VPN activated on your system.
 There has been no solution found yet. You have to disconnect from VPN, run `docker-compose up` and 
 when containers are finally up you may enable your VPN again.
