import subprocess as cmd

cp = cmd.run("git add .", check=True, shell=True)
cp = cmd.run(f"git commit -m \"update repo\"", check=True, shell=True)
cp = cmd.run("git push", check=True, shell=True)
pawse = input("Done!")
