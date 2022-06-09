import subprocess
def main():
    subprocess.run('wget https://drive.google.com/open?id=0BxgO-FKbbXRIYWREa2NwejlVYUU', shell=True, check=True)
    subprocess.run('wget https://drive.google.com/open?id=0BxgO-FKbbXRIY1pRaHJsYVg5dTQ', shell=True, check=True)
    subprocess.run('wget https://drive.google.com/open?id=0BxgO-FKbbXRIa0Flc3Q4bWtycGM', shell=True, check=True)
if __name__=='__main__':
    main()