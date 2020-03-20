# coding=utf-8

import fire
import os
import shutil
from termcolor import cprint

cprint("██████╗      ██████╗     ██╗    ██╗         ███████╗    ██████╗ ", 'cyan')
cprint("██╔══██╗    ██╔═══██╗    ██║    ██║         ██╔════╝    ██╔══██╗", 'cyan')
cprint("██████╔╝    ██║   ██║    ██║    ██║         █████╗      ██████╔╝", 'cyan')
cprint("██╔══██╗    ██║   ██║    ██║    ██║         ██╔══╝      ██╔══██╗", 'cyan')
cprint("██████╔╝    ╚██████╔╝    ██║    ███████╗    ███████╗    ██║  ██║", 'cyan')
cprint("╚═════╝      ╚═════╝     ╚═╝    ╚══════╝    ╚══════╝    ╚═╝  ╚═╝", 'cyan')


class Boiler:
    def requirements(self):
        """Indicates of the server can boil an app"""

        return True

    def boil(self, repository, project_name=None, tag_or_branch="master", skip_clean=0, skip_build=0):
        """Similar to deploy"""
        self.deploy(repository, project_name, tag_or_branch, skip_clean, skip_build)

    def deploy(self, repository, project_name=None, tag_or_branch="master", skip_clean=0, skip_build=0):
        """Deploy an app using docker-compose & nginx"""
        cprint("\n\rBoiling %s" % repository, 'magenta')

        # Get the right project name
        project_name = project_name if project_name is not None else self.__get_project_name(repository)

        # Step 0 - requirements
        cprint("\n\rCheck requirements", 'magenta')
        requirements = self.requirements()
        if requirements:
            cprint("All clear", 'green')
        else:
            cprint("Requirements not met", 'red')
            return

        # Step 1 - create a temporary directory
        cprint("\n\rCreate temporary directory", 'magenta')
        dir_name = self.__create_temporary_directory("boiler_%s" % project_name)
        if dir_name is None:
            cprint("Cannot create temporary directory for deployment. Do you have sufficient permissions?", 'red')
            return
        cprint("Temporary directory created", 'green')

        # Step 2 - clone the app
        cprint("\n\rClone app", 'magenta')
        os.system("git clone -b %s --single-branch --recurse-submodules %s %s/%s" %
                  (tag_or_branch, repository, dir_name, project_name))
        cprint("App cloned", 'green')

        # Step 3 - remove .git
        cprint("\n\rRemove dotgit directory", 'magenta')
        try:
            shutil.rmtree("%s/%s/.git" % (dir_name, project_name), ignore_errors=True)
        except OSError:
            cprint("Cannot rm %s/%s/.git - do you have sufficient permissions?" % (dir_name, project_name), 'red')
            return
        cprint('Okay, your app is safe - no more dotgit directory!', 'green')

        # Step 4 - extract config
        cprint("\n\rExtract config from .boiler directory", 'magenta')
        try:
            shutil.copy("%s/%s/.boiler/docker-compose.yml" % (dir_name, project_name),
                        "%s/docker-compose.yml" % dir_name)
            shutil.copy("%s/%s/.boiler/Dockerfile" % (dir_name, project_name),
                        "%s/%s/Dockerfile" % (dir_name, project_name))
        except OSError:
            cprint("Cannot copy config - do you have sufficient permissions?", 'red')
            return None
        cprint('Config copied', 'green')

        # Step 5 - extract dotenv config
        cprint("\n\rCopy dotenv config", 'magenta')
        try:
            shutil.copy("config/%s.env" % project_name,
                        "%s/.env" % dir_name)
        except OSError:
            cprint("Cannot copy dotenv config", 'red')
            return None
        cprint('Dotenv config copied! Ready to build.', 'green')

        # Can skip here
        if skip_build == 1:
            cprint('Skip build -- all done!', 'cyan')
            return

        # Step 6 - build docker image
        cprint("\n\rBuild docker image", 'magenta')
        os.chdir(dir_name)
        if os.system("docker-compose build") > 0:
            cprint('Cannot build', 'red')
        cprint('Docker image built.', 'green')

        # Step 7 - stop old container
        cprint("\n\rStop old containers", 'magenta')
        if os.system("docker-compose down") > 0:
            cprint('Cannot stop', 'red')
        cprint('Containers stopped.', 'green')

        # Step 8 - up new containers
        cprint("\n\rRaising new containers", 'magenta')
        if os.system("docker-compose up -d") > 0:
            cprint('Cannot raise', 'red')
        os.chdir("../")
        cprint('Containers up & running!', 'green')

        # Step 9 - nginx config & restart
        if os.path.exists("%s/%s/.boiler/nginx" % (dir_name, project_name)):
            try:
                cprint("\n\rCopy nginx config", 'magenta')
                shutil.copy("%s/%s/.boiler/nginx" % (dir_name, project_name),
                            "/etc/nginx/sites-available/%s" % project_name)
                shutil.copy("%s/%s/.boiler/nginx" % (dir_name, project_name),
                            "/etc/nginx/sites-enabled/%s" % project_name)
                cprint("execute `service nginx restart`")
                os.system("service nginx restart")
            except OSError:
                cprint("Cannot copy nginx config", 'red')
                return None
            cprint('Config copied!', 'green')

        # Can skip here
        if skip_clean == 1:
            cprint('Skip clean -- all done!', 'cyan')
            return

        # Step 10 - Clean app
        cprint("\n\rCleaning", 'magenta')
        try:
            shutil.rmtree("%s" % dir_name, ignore_errors=True)
        except OSError:
            cprint("Cannot rm %s" % dir_name, 'red')
            return
        cprint('App boiled! Can be served =)', 'cyan')

    def __create_temporary_directory(self, dir_name=None):
        """Create a temporary directory & return the name"""
        dir_name = self.__get_directory_name() if dir_name is None else dir_name
        if os.path.isdir(dir_name):
            shutil.rmtree("%s" % dir_name)
        try:
            os.mkdir(dir_name)
        except OSError:
            cprint("Creation of the directory %s failed" % dir_name, 'red')
            return None
        else:
            return dir_name

    def __get_project_name(self, repository):
        git_name_arr = repository.split(':')
        git_name = git_name_arr[1]
        git_name_last_fragment_arr = git_name.split('/')
        git_name_last_fragment = git_name_last_fragment_arr[len(git_name_last_fragment_arr) - 1]
        return git_name_last_fragment.replace('.git', '')


if __name__ == '__main__':
    fire.Fire(Boiler)
