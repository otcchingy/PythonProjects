import os

applist = [ 'access           ---------Microsoft Access\n',
            'blend            ---------Visual Studio Blend\n',
            'code             ---------Visual Studio Code',
            'conda            ---------Anaconda Console Multi Operation Tool',
            'codeblocks       ---------Codeblocks Idle',
            'chrome           ---------Chrome Browser\n',
            'excel            ---------Microsoft Excel',
            'explorer         ---------Windows Exploere',
            'firefox          ---------Firefox Browser\n',
            'git              ---------Git Feature',
            'g++              ---------C++ Compiler',
            'git bash         ---------Git Bash Console',
            'git cmd          ---------Git CMD Console',
            'git gui          ---------Git GUI Application\n',
            'heroku           ---------Heroku\n',
            'mpc              ---------K-Lite Media Player Classic',
            'notepad          ---------Windows Notepad',
            '++               ---------Notepad ++ Editor\n',
            'pip              ---------Python Pip Installer',
            'psql             ---------Postgres Database Console App',
            'poweriso         ---------PowerIso Application',
            'powerpoint       ---------Microsoft PowerPoint',
            'python           ---------python Console',
            'pycharm          ---------Pycharm Idle',
            'pycharm64        ---------Pycharm Idle 64bit',
            'pyinstaller      ---------Python Executables Maker\n',
            'sqlite           ---------SQLiteBrowser',
            'vlc              ---------Video Lan Player\n',
            'vscode           ---------Visual Studio Dev Tool',
            'vsixinstaller    ---------VSIXInstaller Tool',
            'winrar           ---------WinRaR Compressed Files Manager\n',
            'winword          ---------Microsoft Word\n\n\n']

print("Code Chingy Applist: [ Version 0.1 build 00201 ]")
print("Copyright (c)  2018 @TechUP@ ..All rights Reserved\n\n")
for i in applist:
    print(i)

def applist_():
    for i in applist:
        print(i)

def HelpMe():
    while True:
        request = str(input(''))
        if request.lower() == 'applist access':
            print('Windows Access')
            print('access [access filename.extention]  NB: only access files\n')
            HelpMe()

        elif request.lower() == 'applist blend':
            print('Visual Studio Blend')
            print('blend [blend filename.extention]  NB: only blend files\n')
            HelpMe()

        elif request.lower() == 'applist conda':
            print('Anaconda Console Tool')
            print('conda Help  NB: Has many functionalities including install, download, uninstall etc\n')
            HelpMe()

        elif request.lower() == 'applist code':
            print('Visual Studio Code')
            print('code [code filename.extention]  NB: only readable files')
            print('code * to run multiple file\n')
            HelpMe()

        elif request.lower() == 'applist codeblocks':
            print('Codeblocks Idle')
            print('codeblocks [c/c++ filename.extention] NB: .cpp, .c files etc\n')
            HelpMe()

        elif request.lower() == 'applist chrome':
            print('Chrome Browser')
            print('chrome   --to start chrome browser')
            print('chrome [html filename.extention]  NB: only htm, html files\n')
            HelpMe()

        elif request.lower() == 'applist excel':
            print('Microsoft Excel')
            print('excel [excel filename.extention]  NB: for all spreadsheet files\n')
            HelpMe()

        elif request.lower() == 'applist explorer':
            print('Windows Explorer')
            print('explorer   -----open windows explorer application\n')
            HelpMe()

        elif request.lower() == 'applist firefox':
            print('Firefox Browser')
            print('firefox       ------run firefox browser')
            print('firefox [html filename.extention]  NB: htm, html files, other web file and video files\n')
            HelpMe()
            
        elif request.lower() == 'applist git':
            print('Git')
            print('git feature for version control ----commands [push, pull, fetch, commit, branch, clone etc..ask git help]\n')
            HelpMe()

        elif request.lower() == 'applist g++':
            print('C++ Compiler')
            print('g++ feature for compiling c++ files ')
            print('g++ [filename.cpp]\n')
            HelpMe()

        elif request.lower() == 'applist git bash':
            print('Git Bash')
            print('git bash console app to run git an some cmd command..allow attrib viewing\n')
            HelpMe()
            
        elif request.lower() == 'applist git cmd':
            print('Git CMD')
            print('git Cmd ----cmd app copycut of windows cmd..work perfectly with extra features\n')
            HelpMe()
            
        elif request.lower() == 'applist git gui':
            print('Git Gui')
            print('git gui  ----runs the graphical version of git in windows\n')
            HelpMe()

        elif request.lower() == 'applist heroku':
            print('Heroku Console')
            print('Heroku help  ----web deploying too..can use[run python [appname.extention], ps:scale web=0 || 1 \n')
            HelpMe()

        elif request.lower() == 'applist notepad':
            print('Notepad Text Editor')
            print('notepad  ----runs the graphical version of git in windows')
            print('notepad [filename.txt / *] -----to run aspecific fic or all \n')
            HelpMe()

        elif request.lower() == 'applist ++':
            print('Notepad++ Text Editor')
            print('++  ----runs the graphical version of git in windows')
            print('++ [filename.txt / *] -----to run aspecific fic or all \n')
            HelpMe()

        elif request.lower() == 'applist pip':
            print('Pip Installer')
            print('pip installs python modules, uninstalls and cleans dirs')
            print('pip install [module_name]\n')
            HelpMe()

        elif request.lower() == 'applist psql':
            print('Postgres Database Console App')
            print('psql [database name] [username/ownername]....then enter password to login')
            print('psql help for more help\n')
            HelpMe()

        elif request.lower() == 'applist poweriso':
            print('PowerISO')
            print('poweriso [isofilename.extention]  NB: iso files and other compressed format\n')
            HelpMe()

        elif request.lower() == 'applist powerpoint':
            print('Windows PowerPoint')
            print('powerpoint [pptfilename.extention]  NB: only readable files\n')
            HelpMe()

        elif request.lower() == 'applist pycharm':
            print('Pycharm Idle')
            print('Idle runs all readable files..c, c++, java, javascript, html etc')
            print('pycharm [filename.extention] -- NB: almost any extention except media files\n')

        elif request.lower() == 'applist pycharm64':
            print('Pycharm Idle 64bit')
            print('Idle runs all readable files..c, c++, java, javascript, html etc')
            ('pycharm64 [filename.extention] -- NB: almost any extention except media files\n')
            HelpMe()

        elif request.lower() == 'applist python':
            print('Python Console Application')
            print('python [filename.py -extentions] -- NB: all python files files')
            print('python filename.pyextention install -----to install python mudoles\n')
            HelpMe()

        elif request.lower() == 'applist pyinstaller':
            print('Python Executables Maker')
            print("pyinstaller [-F][-w][-i] 'icon-directory' 'file-directory' ---- NB: all python files files\n")
            HelpMe()

        elif request.lower() == 'applist sqlite':
            print('SQLite Studio')
            print('Open all database files')
            print('sqlite   --to sqlite studio application')
            print('sqlite [filename.extention] -- NB: all media file ---db, sqlite etc.\n')
            HelpMe()

        elif request.lower() == 'applist vlc':
            print('Video Lan Player')
            print('vlc   --to run the video lan player')
            print('vlc [filename.extention] -- NB: all media file ---mp4, mp3, jpg, png--music ,videos, pictures.\n')
            HelpMe()

        elif request.lower() == 'applist vscode':
            print('Visual Studio Dev Tool')
            print('vscode   --to run the video lan player')
            print('vscode [filename.extention] -- NB: all type of pragram codes ---py, c, cpp, java, js, etc.\n')
            HelpMe()

        elif request.lower() == 'applist vsixinstaller':
            print('VSIX Installer')
            print('vsixinstaller   --to run the video lan player')
            print('vsiximstaller [filename.extention] -- NB: only vsix files.\n')
            HelpMe()

        elif request.lower() == 'applist winrar':
            print('WinRaR')
            print('winrar [compressed-filename.extention] -- NB: almost any compressed file [zip, rar, iso etc.]\n')
            HelpMe()

        elif request.lower() == 'applist winword':
            print('Microsofr Word')
            print('word [filename.extention] -- NB: almost any readable file..doc, docx, pdf etc\n')
            HelpMe()

        elif request.lower() == 'applist':
            print('')
            applist_()
            HelpMe()

        elif request.lower() == 'help':
            print('')
            print('Using applist feature ')
            print('applist [app name]   -----for information about app')
            print('[app name]   ----to run the app in window')
            print('[app name] [related file.extention]     ------to run a file in the app')
            print('exit    ----to quit\n')
            HelpMe()

        elif request.lower() == 'exit':
            os.system('cls' if os.name=='nt' else 'clear')

        else:
            print("\n'{}' is an invalid command\n".format(request))
            HelpMe()
        break

HelpMe()
